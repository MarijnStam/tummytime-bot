import discord
from discord import app_commands
from fuzzywuzzy import process
from typing import List
from sqlmodel import Session

from log import app_logger as log
import models
import views
import constants
import db_helper


BOT_FARM = discord.Object(id=constants.guild_id) 
TOKEN = constants.tummy_token


class TummyBot(discord.Client):
    #We save this view here because message interaction is dependant upon its state
    new_meal_view: views.NewMealView
    registered_meals: List[models.Meal]
    session: Session
    
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)
        self.new_meal_view = None
        
    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=BOT_FARM)
        await self.tree.sync(guild=BOT_FARM)
        
intents = discord.Intents.default()
intents.message_content=True
client = TummyBot(intents=intents)

@client.event
async def on_ready():
    with Session(db_helper.engine) as session:
        client.session = session
        log.info(f'Logged in as {client.user} (ID: {client.user.id})')
        client.registered_meals = await db_helper.all_meals()

@client.event
async def on_message(message: discord.Message):
    if client.new_meal_view:
        if client.new_meal_view.input_stage == 1:
            await message.delete()
            await client.new_meal_view.capture_ingredient(message)

@client.tree.command()
async def feel(interaction: discord.Interaction):
    with Session(db_helper.engine) as session:
        client.session = session
        await interaction.response.send_message("How are you feeling? (1 - 10)", view=views.FeelView())
    
@client.tree.command()
async def new_meal(interaction: discord.Interaction):
     with Session(db_helper.engine) as session:
        client.session = session
        client.new_meal_view = views.NewMealView(interaction.user)
        await interaction.response.send_modal(client.new_meal_view.meal_name_modal)
    
@client.tree.command(name="meal", description="Register a new meal entry")
async def meal(interaction: discord.Interaction, meal_name: str):
     with Session(db_helper.engine) as session:
        client.session = session
        meal_entry_view: views.MealEntryView  = views.MealEntryView(meal=await db_helper.check_meal(meal_name=meal_name))
        await interaction.response.send_message(embed=await meal_entry_view.build_embed(title="What did you eat?"), view=meal_entry_view)

# AUTOCOMPLETE
@meal.autocomplete("meal_name")
async def team_autocomp(interaction: discord.Interaction, meal_name: str):    
    def get_matches(string, choices, limit=25):
        results = process.extract(string, choices, limit=limit)
        return results
    
    meal_name = meal_name.capitalize()
    meals = [x.name for x in client.registered_meals]
    matches = get_matches(meal_name, meals)
    return [discord.app_commands.Choice(name=x[0], value=x[0]) for x in matches if int(x[1]) > 40]
    
def start_bot():
    """Starts the Discord bot with a static token
    """    
    log.info("Starting bot")
    client.run(token=TOKEN, log_handler=None)

def get_session() -> Session:
        return client.session
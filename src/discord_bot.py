import discord
from discord import app_commands
from fuzzywuzzy import process
from typing import List

from log import app_logger as log
import models
import views
import constants

BOT_FARM = discord.Object(id=constants.guild_id) 
TOKEN = constants.tummy_token


class TummyBot(discord.Client):
    #We save this view here because message interaction is dependant upon its state
    new_meal_view: views.NewMealView        #Active new_meal_view attached, used for capturing messages
    
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.new_meal_view = None
        
    async def setup_hook(self):
        self.tree.copy_global_to(guild=BOT_FARM)
        await self.tree.sync(guild=BOT_FARM)
        
intents = discord.Intents.default()
intents.message_content=True
client = TummyBot(intents=intents)

@client.event
async def on_ready():
    log.info(f'Logged in as {client.user} (ID: {client.user.id})')

#We capture all messages here in case we are adding new ingredients to a meal
@client.event
async def on_message(message: discord.Message):
    if client.new_meal_view:
        if client.new_meal_view.input_stage == 1:
            await message.delete()
            await client.new_meal_view.capture_ingredient(message)

#Command for registering a Feel
@client.tree.command()
async def feel(interaction: discord.Interaction):
    await interaction.response.send_message("How are you feeling? (1 - 10)", view=views.FeelView())

#Command for registering a New Meal
@client.tree.command()
async def new_meal(interaction: discord.Interaction):
    client.new_meal_view = views.NewMealView(interaction.user)
    await interaction.response.send_modal(client.new_meal_view.meal_name_modal)

#TODO FIX ME      
# #Command for registering Meal Entry
# @client.tree.command(name="meal", description="Register a new meal entry")
# async def meal(interaction: discord.Interaction, meal_name: str):
#     meal_entry_view: views.MealEntryView  = views.MealEntryView(meal=await db_helper.check_meal(meal_name=meal_name))
#     await interaction.response.send_message(embed=meal_entry_view.build_embed(), view=meal_entry_view)

# AUTOCOMPLETE for Meal Entry
# @meal.autocomplete("meal_name")
# async def team_autocomp(interaction: discord.Interaction, meal_name: str):    
#     def get_matches(string, choices, limit=25):
#         results = process.extract(string, choices, limit=limit)
#         return results
       
#     meal_name = meal_name.capitalize()
#     meals = [x.name for x in client.registered_meals]
#     matches = get_matches(meal_name, meals)
        
#     return [discord.app_commands.Choice(name=x[0], value=x[0]) for x in matches if int(x[1]) > 40]
    
def start_bot():
    """Starts the Discord bot with a static token
    """    
    log.info("Starting bot")
    client.run(token=TOKEN, log_handler=None)
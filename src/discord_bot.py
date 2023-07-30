import discord
from discord import app_commands

from log import app_logger as log
import models
import views
import constants

BOT_FARM = discord.Object(id=constants.guild_id) 
TOKEN = constants.tummy_token


class TummyBot(discord.Client):
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

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=BOT_FARM)
        await self.tree.sync(guild=BOT_FARM)
        
intents = discord.Intents.default()
client = TummyBot(intents=intents)

@client.event
async def on_ready():
    log.info(f'Logged in as {client.user} (ID: {client.user.id})')
    

@client.tree.command()
async def symptoms(interaction: discord.Interaction):
    await interaction.response.send_message("How are you feeling? (1 - 10)", view=views.FeelView())
    
def start_bot():
    """Starts the Discord bot with a static token
    """    
    log.info("Starting bot")
    client.run(token=TOKEN, log_handler=None)
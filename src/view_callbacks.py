import discord
from log import app_logger as log

import views
    
async def menu_callback(self, interaction: discord.Interaction):
    log.info("Menu callback")
    
async def feel_button_feelback(self, interaction: discord.Interaction):
    assert self.view is not None
    view: views.FeelView = self.view
    self.style = discord.ButtonStyle.success
    log.info("Button callback")
    await interaction.response.edit_message(view=view)
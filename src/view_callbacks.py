import discord
from log import app_logger as log

import views
import view_components
    
async def symptoms_callback(self: 'view_components.SymptomsDropdown', interaction: discord.Interaction):
    assert self.view is not None
    view: views.FeelView = self.view
    view.symptoms = ' '.join(self.values)
    await interaction.response.defer()
    
async def feel_dropdown_callback(self: 'view_components.FeelDropdown', interaction: discord.Interaction):
    assert self.view is not None
    view: views.FeelView = self.view
    view.feel = self.values[0]
    await interaction.response.defer()
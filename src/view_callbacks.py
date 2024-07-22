import discord
from log import app_logger as log

import views
import view_components
    
async def symptoms_callback(self: 'view_components.SymptomsDropdown', interaction: discord.Interaction):
    assert self.view is not None
    view: views.FeelView = self.view
    view.symptoms = [x.capitalize() for x in self.values]
    await interaction.response.defer()
    
async def feel_dropdown_callback(self: 'view_components.FeelDropdown', interaction: discord.Interaction):
    assert self.view is not None
    view: views.FeelView = self.view
    view.feel = self.values[0].capitalize()
    await interaction.response.defer()

async def mealtype_callback(self: 'view_components.MealEntryDropdown', interaction: discord.Interaction):
    assert self.view is not None
    view: views.MealEntryView = self.view
    view.meal_type = self.values[0]
    await view.next_input_view(interaction)
    
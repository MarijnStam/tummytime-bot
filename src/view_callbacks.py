import discord
from log import app_logger as log

import views
import view_components
    
async def symptoms_callback(self: 'view_components.SymptomsDropdown', interaction: discord.Interaction):
    assert self.view is not None
    view: views.FeelView = self.view
    view.symptoms = self.values
    await interaction.response.defer()
    
async def feel_dropdown_callback(self: 'view_components.FeelDropdown', interaction: discord.Interaction):
    assert self.view is not None
    view: views.FeelView = self.view
    view.feel = self.values[0]
    await interaction.response.defer()
    
async def mealtype_callback(self: 'view_components.NewMealDropdown', interaction: discord.Interaction):
    assert self.view is not None
    view: views.NewMealView = self.view
    view.meal_type = self.values[0]
    view.input_stage = view.input_stage + 1
    await view.next_input_view(interaction)
    
async def mealname_callback(self: 'view_components.NewMealNameInput', interaction: discord.Interaction):
    assert self.view is not None
    view: views.NewMealView = self.view
    view.meal_name = self.value
    await interaction.response.defer()
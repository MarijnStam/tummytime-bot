from typing import Any, Optional
import discord
from discord.enums import TextStyle
from discord.interactions import Interaction
from discord.utils import MISSING
import view_callbacks

# Defines a custom Select containing colour options
# that the user can choose. The callback function
# of this class is called when the user changes their choice
class SymptomsDropdown(discord.ui.Select):
    def __init__(self):
        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label='Bloated', emoji='🎈'),
            discord.SelectOption(label='Nausea', emoji='🤮'),
            discord.SelectOption(label='Diarrhea',  emoji='🏃‍♂️'),
            discord.SelectOption(label='Constipated', emoji='🛑'),
        ]

        # The placeholder is what will be shown when no option is chosen
        super().__init__(placeholder='Experiencing any symptoms?', min_values=0, max_values=options.__len__(), options=options)

    async def callback(self, interaction: discord.Interaction):
        await view_callbacks.symptoms_callback(self, interaction)
        
class NewMealDropdown(discord.ui.Select):
    def __init__(self):
        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label='Breakfast', emoji='🥐'),
            discord.SelectOption(label='Lunch', emoji='🥪'),
            discord.SelectOption(label='Dinner',  emoji='🍲'),
            discord.SelectOption(label='Snack', emoji='🍫'),
        ]

        # The placeholder is what will be shown when no option is chosen
        super().__init__(placeholder='What type of meal did you eat??', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await view_callbacks.mealtype_callback(self, interaction)
        
class NewMealNameInput(discord.ui.TextInput):
    def __init__(self, row: int | None = None) -> None:
        super().__init__(label="", style=TextStyle.short, placeholder="Enter the name of your meal", required=True, row=row)
    
class FeelDropdown(discord.ui.Select):
    def __init__(self):
        # Set the options that will be presented inside the dropdown
        options = [discord.SelectOption(label=f'{x}') for x in range(1, 11)]

        # The placeholder is what will be shown when no option is chosen
        super().__init__(placeholder='How are you feeling in general?', min_values=1, max_values=1, options=options)
        
    async def callback(self, interaction: discord.Interaction):
        await view_callbacks.feel_dropdown_callback(self, interaction)
        
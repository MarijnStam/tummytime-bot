from typing import Any, Optional
import discord
from discord.enums import TextStyle
from discord.interactions import Interaction
from discord.utils import MISSING
from typing import List
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
            discord.SelectOption(label='Gassy', emoji='☁'),
        ]

        # The placeholder is what will be shown when no option is chosen
        super().__init__(placeholder='Experiencing any symptoms?', min_values=0, max_values=options.__len__(), options=options)

    async def callback(self, interaction: discord.Interaction):
        await view_callbacks.symptoms_callback(self, interaction)
        
class NewMealNameInput(discord.ui.TextInput):
    def __init__(self, row: int | None = None) -> None:
        super().__init__(label="", style=TextStyle.short, placeholder="Enter the name of your meal", required=True, row=row)

class MealEntryDropdown(discord.ui.Select):
    def __init__(self):
        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label='Breakfast', emoji='🥐'),
            discord.SelectOption(label='Lunch', emoji='🥪'),
            discord.SelectOption(label='Dinner',  emoji='🍲'),
            discord.SelectOption(label='Snack', emoji='🍫'),
        ]

        # The placeholder is what will be shown when no option is chosen
        super().__init__(placeholder='What type of meal did you eat?', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await view_callbacks.mealtype_callback(self, interaction)
    
class FeelDropdown(discord.ui.Select):
    def __init__(self):
        # Set the options that will be presented inside the dropdown
        options = [discord.SelectOption(label=f'{x}') for x in range(1, 11)]

        # The placeholder is what will be shown when no option is chosen
        super().__init__(placeholder='How are you feeling in general?', min_values=1, max_values=1, options=options)
        
    async def callback(self, interaction: discord.Interaction):
        await view_callbacks.feel_dropdown_callback(self, interaction)

class TimePicker():
    class __HourPicker(discord.ui.Select):
        def __init__(self):
            # Set the options that will be presented inside the dropdown
            options = [discord.SelectOption(label=f'{x}') for x in range(1, 13)]            

            # The placeholder is what will be shown when no option is chosen
            super().__init__(placeholder='Hour', min_values=1, max_values=1, options=options, row=0)
            
        async def callback(self, interaction: discord.Interaction):
            await interaction.response.defer()

    
    class __MinutePicker(discord.ui.Select):
        def __init__(self):
            # Set the options that will be presented inside the dropdown
            options = [
                discord.SelectOption(label='00'),
                discord.SelectOption(label='15'),
                discord.SelectOption(label='30'),
                discord.SelectOption(label='45'),
            ]

            # The placeholder is what will be shown when no option is chosen
            super().__init__(placeholder='Minute', min_values=1, max_values=1, options=options, row=1)
        
        async def callback(self, interaction: discord.Interaction):
            await interaction.response.defer()
            
    class __AMPMPicker(discord.ui.Select):
        def __init__(self):
            # Set the options that will be presented inside the dropdown
            options = [
                discord.SelectOption(label='AM'),
                discord.SelectOption(label='PM'),
            ]

            # The placeholder is what will be shown when no option is chosen
            super().__init__(placeholder='AM/PM', min_values=1, max_values=1, options=options, row=2)
        
        async def callback(self, interaction: discord.Interaction):
            await interaction.response.defer()
    
    items: List[discord.ui.Select] = []
    
    def __init__(self):
        self.items.append(self.__HourPicker()) 
        self.items.append(self.__MinutePicker()) 
        self.items.append(self.__AMPMPicker()) 
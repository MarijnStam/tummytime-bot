import discord
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
            discord.SelectOption(label='Constipated', emoji='💩'),
        ]

        # The placeholder is what will be shown when no option is chosen
        super().__init__(placeholder='Experiencing any symptoms?', min_values=0, max_values=options.__len__(), options=options)

    async def callback(self, interaction: discord.Interaction):
        await view_callbacks.symptoms_callback(self, interaction)
        
class FeelDropdown(discord.ui.Select):
    def __init__(self):
        # Set the options that will be presented inside the dropdown
        # TODO Replace with some kind of indexed for loop
        options = [
            discord.SelectOption(label='1'),
            discord.SelectOption(label='2'),
            discord.SelectOption(label='3'),
            discord.SelectOption(label='4'),
            discord.SelectOption(label='5'),
            discord.SelectOption(label='6'),
            discord.SelectOption(label='7'),
            discord.SelectOption(label='8'),
            discord.SelectOption(label='9'),
            discord.SelectOption(label='10'),
        ]

        # The placeholder is what will be shown when no option is chosen
        super().__init__(placeholder='How are you feeling in general?', min_values=1, max_values=1, options=options)
        
    async def callback(self, interaction: discord.Interaction):
        await view_callbacks.feel_button_feelback(self, interaction)
        
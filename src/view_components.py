import discord
import view_callbacks

# Defines a custom Select containing colour options
# that the user can choose. The callback function
# of this class is called when the user changes their choice
class SymptonsDropdown(discord.ui.Select):
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
        await view_callbacks.menu_callback(self, interaction)
        
class FeelButton(discord.ui.Button):
    def __init__(self, value, row):
        super().__init__(style=discord.ButtonStyle.secondary, label=f"{value}", row=row)
        
    async def callback(self, interaction: discord.Interaction):
        await view_callbacks.feel_button_feelback(self, interaction)
        
    
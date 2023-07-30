import discord
import view_components
from typing import List
        
        
class FeelView(discord.ui.View):
    feel: int
    symptoms: List[str]
    
    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.success, row=3)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Make sure to update the message with our updated selves
        await interaction.response.edit_message(view=self)
        
    @discord.ui.button(label='Reset', style=discord.ButtonStyle.danger, row=3)
    async def reset(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Make sure to update the message with our updated selves
        await interaction.response.edit_message(view=self)
    
    def __init__(self):            
        super().__init__()
        self.feel = None
        self.symptoms = None
        
        #First add the feel dropdown
        self.add_item(view_components.FeelDropdown())
            
        #Add the select menu below for extra symptoms
        self.add_item(view_components.SymptomsDropdown())
        

import discord
import view_components
from typing import List
import db_helper
        
        
class FeelView(discord.ui.View):
    feel: int
    symptoms: List[str]
    
    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.success, row=3)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Enter the values into the db and respond with the registered values
        feel = db_helper.feel_entry(self.feel, self.symptoms)
        await interaction.response.edit_message(content=f"Feel with value of **{feel.feel}/10** registered with ID: **{feel.id}**", view=None, delete_after=5)
        
    @discord.ui.button(label='Reset', style=discord.ButtonStyle.danger, row=3)
    async def reset(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Spawn a new instance of the view object to reset the view and its values
        await interaction.response.edit_message(content="How are you feeling? (1 - 10)", view=FeelView())
    
    def __init__(self):            
        super().__init__()
        self.feel = None
        self.symptoms = None
        
        #First add the feel dropdown
        self.add_item(view_components.FeelDropdown())
            
        #Add the select menu below for extra symptoms
        self.add_item(view_components.SymptomsDropdown())
        

import discord
from log import app_logger as log

import views
import view_components
    
async def symptoms_callback(self, interaction: discord.Interaction):
    assert self.view is not None
    view: views.FeelView = self.view
    
    
    #Fetch the emojis for the values that were passed
    emojis = [x.emoji for x in self.options if x.label in self.values]
    
    #First remove all existing reactions and add the new ones (does not work yet?)
    if view.symptoms:
        msg = await interaction.channel.fetch_message(interaction.message.id)
        for x in msg.reactions:
            await msg.remove_reaction(x, member=interaction.user)
            
    for x in emojis:
        await interaction.message.add_reaction(x)
        
    view.symptoms = self.values
    await interaction.response.edit_message(view=view)
    
async def feel_button_feelback(self, interaction: discord.Interaction):
    assert self.view is not None
    view: views.FeelView = self.view
    view.feel = int(self.values) 
            
    self.style = discord.ButtonStyle.success
    await interaction.response.edit_message(view=view)
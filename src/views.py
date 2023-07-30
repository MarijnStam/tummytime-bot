import discord
import view_components
        
class FeelView(discord.ui.View):
    def __init__(self):
        super().__init__()
        
        #First add the view buttons
        for x in range(1, 11):
            self.add_item(view_components.FeelButton(value=x, row =(0 if x<6 else 1)))
            
        #Add the select menu below for extra symptoms
        self.add_item(view_components.SymptonsDropdown())
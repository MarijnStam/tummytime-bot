import discord
from discord.utils import MISSING
import view_components
from typing import List, Optional
from datetime import datetime

import db_helper
        
        
class FeelView(discord.ui.View):
    feel: int
    symptoms: List[str]
    
    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.success, row=3)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Enter the values into the db and respond with the registered values
        feel = db_helper.feel_entry(self.feel, self.symptoms)
        embed=discord.Embed(
            title=f"Feelings entry registered",
            color=discord.Color.green(),
            timestamp=datetime.strptime(feel.timestamp, "%d/%m/%Y %H:%M:%S"))
        embed.add_field(name="You are feeling", value=f"**{feel.feel}/10**", inline=True)
        embed.add_field(name="Symptoms", value="\n".join(self.symptoms), inline=False)
            
        await interaction.response.edit_message(content="",embed=embed, view=None)
        
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
        
class MealNameModal(discord.ui.Modal):
    meal_view: 'NewMealView'
    text_input: 'view_components.NewMealNameInput'
    def __init__(self, meal_view: 'NewMealView'):
        super().__init__(title="New meal")  # Modal title
        self.meal_view = meal_view
        self.text_input = view_components.NewMealNameInput()
        self.add_item(self.text_input)
        
    async def on_submit(self, interaction: discord.Interaction) -> None:
        self.meal_view.meal_name = self.text_input.value
        await self.meal_view.next_input_view(interaction)
        
class NewMealView(discord.ui.View):    
    input_stage: int                        #The input stage of the view. Name of meal -> Type -> Ingredients
    meal_type: str                          #Entered type of the meal
    meal_type_dropdown: discord.ui.Select   #Dropdown for the type of meal
    meal_name_modal: discord.ui.Modal       #Modal input for the name
    meal_name: str                          #Name of the meal
    ingredients: List[str]                  #List of ingredients      
    message: discord.Message                #Original message of the interaction       
    user: discord.User                      #User who invoked the command
    
    # @discord.ui.button(label='Confirm', style=discord.ButtonStyle.success, row=1, disabled=True)
    # async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
    #     await interaction.message.delete()
        
    @discord.ui.button(label='Undo', style=discord.ButtonStyle.danger, row=1)
    async def reset(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.input_stage == 1:
            if len(self.ingredients) == 0:  #Undo the meal type selection and revert the view
                self.meal_type = ""
                self.input_stage = 0
            else:   
                self.ingredients.pop() #Otherwise just pop an ingredient off the list
            
        await self.next_input_view(interaction, undo=True)
    
    def __init__(self, user: discord.User) -> None:
        super().__init__()
        self.input_stage = 0
        self.meal_name_modal = MealNameModal(self)
        self.meal_type_dropdown = view_components.NewMealDropdown()
        self.meal_name = ""
        self.meal_type = ""
        self.ingredients = []
        self.og_message = None
        self.user = user
    
    async def next_input_view(self, interaction: discord.Interaction, undo: bool = False):
        if self.input_stage == 0:                       #Capturing meal type through SelectMenu
            self.add_item(self.meal_type_dropdown)
            await interaction.response.send_message(embed=self.build_embed(title="Select type of meal"), view=self)
            if not undo:
                self.og_message = await interaction.original_response()
            
        elif self.input_stage == 1:                     #Capturing ingredients, remove select menu on first invocation
            self.remove_item(self.meal_type_dropdown)
            e = self.build_embed(title="Add ingredients", color=discord.Color.gold(), 
                                 description="Enter ingredients into chat one by one to add to this meal")
            await interaction.response.edit_message(embed=e, view=self)
            
    async def capture_ingredient(self, message: discord.Message):
        if message.author == self.user:
            self.ingredients.append(message.content)
            e = self.build_embed(title="Add ingredients", color=discord.Color.gold(), 
                                 description="Enter ingredients into chat one by one to add to this meal")
            await self.og_message.edit(embed=e, view=self)

    def build_embed(self, title: str, color: discord.Color = discord.Color.dark_blue(), description: str = None) -> discord.Embed:
        e = discord.Embed(
            title=title,
            color=color,
            description=description)
        e.add_field(name="Name", value=self.meal_name, inline=True)
        e.add_field(name="Ingredients", value="\n".join(self.ingredients), inline=True)
        e.add_field(name="Type", value=self.meal_type, inline=False)
        
        return e
    
        


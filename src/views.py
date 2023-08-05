import discord
from discord.utils import MISSING
import view_components
from typing import List, Optional
from datetime import datetime
from log import app_logger as log

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
        self.meal_view.meal_name = self.text_input.value.capitalize()
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
    
    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.success, row=1, disabled=True)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            db_helper.new_meal(meal_name=self.meal_name, meal_ingredients=self.ingredients)
        except db_helper.AlreadyPresent as e:
            log.warning(e)
            await interaction.response.edit_message(embed=self.build_embed(title="Meal registration failed", color=discord.Color.red(), 
                                                                  description="Meal name is already present int the db"), view=self, delete_after=10)
            return
            
        await interaction.response.edit_message(embed=self.build_embed(title="New meal registered", color=discord.Color.green()), view=self, delete_after=10)
        
    @discord.ui.button(label='Undo', style=discord.ButtonStyle.danger, row=1)
    async def reset(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.input_stage == 0:
            await interaction.message.delete()
            return
        if self.input_stage == 1:
            self.ingredients.pop() #Otherwise just pop an ingredient off the list
            e = self.build_embed(title="Add ingredients", color=discord.Color.gold(), 
                                 description="Enter ingredients into chat one by one to add to this meal")
            await interaction.response.edit_message(embed=e, view=self)
    
    def __init__(self, user: discord.User) -> None:
        super().__init__()
        self.input_stage = 0
        self.meal_name_modal = MealNameModal(self)
        self.meal_name = ""
        self.ingredients = []
        self.og_message = None
        self.user = user
        #Start with the confirm button disabled
        self.confirm.disabled = True
    
    async def next_input_view(self, interaction: discord.Interaction, undo: bool = False):
        if self.input_stage == 0:                       #We get here when the Modal view has captured the meal name
            
             #Check whether the meal already exists before building the view
            if db_helper.check_meal(self.meal_name) is not None:
                await interaction.response.send_message(f"{self.meal_name} already exists in the database")
            
            #Set up for capturing ingredients of the meal through messages
            self.confirm.disabled = False
            e = self.build_embed(title="Add ingredients", color=discord.Color.gold(), 
                                 description="Enter ingredients into chat one by one to add to this meal")
            await interaction.response.send_message(embed=e, view=self)
            self.input_stage = self.input_stage + 1
            
            #Only capture the original message if this is not an undo action
            if not undo:
                self.og_message = await interaction.original_response()
            
    #Capture the ingredients from message input 
    async def capture_ingredient(self, message: discord.Message):
        if message.author == self.user:
            self.ingredients.append(message.content)
            e = self.build_embed(title="Add ingredients", color=discord.Color.gold(), 
                                 description="Enter ingredients into chat one by one to add to this meal")
            await self.og_message.edit(embed=e, view=self)

    #Helper function for building an embed for the new_meal view, updates the fields to latest values
    def build_embed(self, title: str, color: discord.Color = discord.Color.dark_blue(), description: str = None) -> discord.Embed:
        e = discord.Embed(
            title=title,
            color=color,
            description=description)
        e.add_field(name="Name", value=self.meal_name, inline=True)
        e.add_field(name="Ingredients", value="\n".join(self.ingredients), inline=True)
        
        return e
    
class MealEntryView(discord.ui.View):
    def __init__(self, *, timeout: float | None = 180):
        super().__init__(timeout=timeout)


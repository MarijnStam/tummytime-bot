from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship

    
# Join tables for setting up the many-to-many relations
class MealIngredient(SQLModel, table=True):
    meal_id: Optional[int] = Field(
        default=None, foreign_key="meal.id", primary_key=True
    )
    ingredient_id: Optional[int] = Field(
        default=None, foreign_key="ingredient.id", primary_key=True
    )
    
class MealEntryIngredients(SQLModel, table=True):
    meal_entry_id: Optional[int] = Field(
        default=None, foreign_key="mealentry.id", primary_key=True
    )
    ingredient_id: Optional[int] = Field(
        default=None, foreign_key="ingredient.id", primary_key=True
    )
    
# ------------ Ingredient Model --------------- #
# --------------------------------------------- #    
class Ingredient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    meals: List["Meal"] = Relationship(back_populates="ingredients", link_model=MealIngredient)
    meal_entries: List["MealEntry"] = Relationship(back_populates="ingredients", link_model=MealEntryIngredients)
    
# ------------- MealEntry Model --------------- #
# --------------------------------------------- #    
class MealEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: str
    meal_id: Optional[int] = Field(default=None, foreign_key="meal.id")
    meal: Optional["Meal"] = Relationship(back_populates="meal_entries")
    ingredients: List[Ingredient] = Relationship(back_populates="meal_entries", link_model=MealEntryIngredients)
    
# ---------------- Meal Model ----------------- #
# --------------------------------------------- #
class Meal(SQLModel, table=True):
    name: str = Field(index=True, unique=True)
    id: Optional[int] = Field(default=None, primary_key=True)
    ingredients: List[Ingredient] = Relationship(back_populates="meals", link_model=MealIngredient)
    meal_entries: Optional[List[MealEntry]] = Relationship(back_populates="meal")
    
# --------------- Feel Model ------------------ #
# --------------------------------------------- #       
class Feel(SQLModel, table=True):
    timestamp: str
    feel: int
    id: Optional[int] = Field(default=None, primary_key=True)

    

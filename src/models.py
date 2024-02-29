from typing import Optional, List
from dataclasses import dataclass
from enum import Enum

# --------------- ENUM TYPES ------------------ #
# --------------------------------------------- # 
class MealType(Enum):
    BREAKFAST = 1
    LUNCH = 2
    DINNER = 3
    SNACK = 4

class FeelSymptoms(Enum):
    Bloated = 1
    Nausea = 2
    Diarrhea = 3
    Constipated = 4
    Gassy = 5

# ------------ Ingredient Model --------------- #
# --------------------------------------------- #  
@dataclass  
class Ingredient:
    name: str

# ---------------- Meal Model ----------------- #
# --------------------------------------------- #
@dataclass
class Meal:
    name: str 
    ingredients: List[Ingredient]
    
# ------------- MealEntry Model --------------- #
# --------------------------------------------- #    
@dataclass
class MealEntry:
    timestamp: str
    meal: Meal
    ingredients: List[Ingredient]
    

# --------------- Feel Model ------------------ #
# --------------------------------------------- #       
@dataclass
class Feel:
    timestamp: str
    feel: int
from typing import Optional, List
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from enum import Enum, Flag

# --------------- ENUM TYPES ------------------ #
# --------------------------------------------- # 
class MealType(Enum):
    BREAKFAST = 1
    LUNCH = 2
    DINNER = 3
    SNACK = 4

class FeelSymptoms(Flag):
    Bloated     = 1
    Nausea      = 2
    Diarrhea    = 4
    Constipated = 8
    Gassy       = 16

class MealType(Flag):
    Breakfast   = 1
    Lunch       = 2
    Dinner      = 4
    Snack       = 8

# ------------ Ingredient Model --------------- #
# --------------------------------------------- #  
@dataclass_json
@dataclass  
class Ingredient:
    name: str = None
    id: int = None

# ---------------- Meal Model ----------------- #
# --------------------------------------------- #
@dataclass_json
@dataclass
class Meal:
    meal_name: str = None
    ingredients: List[Ingredient] = field(default_factory=list)
    
# ------------- MealEntry Model --------------- #
# --------------------------------------------- #    
@dataclass_json
@dataclass
class MealEntry:
    timestamp: str = None
    meal: Meal = None
    ingredients: List[Ingredient] = field(default_factory=list)
    

# --------------- Feel Model ------------------ #
# --------------------------------------------- #       
@dataclass_json
@dataclass
class Feel:
    timestamp: str = None
    feel_nr: int = None
    symptoms: FeelSymptoms = FeelSymptoms(0)
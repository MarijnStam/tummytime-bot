from sqlmodel import SQLModel, Session, create_engine, engine, select
from sqlalchemy.exc import IntegrityError
from typing import List
from datetime import datetime as time 


from models import *

db_file_name = "TummyTime.sqlite3"
sqlite_url = f"sqlite:///{db_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

class AlreadyPresent(Exception):
    pass

def create_db():
    SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session

def feel_entry(feel: int, symptoms: List[str]) -> Feel:
    with Session(engine) as session:
        db_feel = Feel(id=None, feel=feel, timestamp=timestamp())
        session.add(db_feel)
        session.commit()
        session.refresh(db_feel)
        return db_feel
    
def new_meal(meal_name: str, meal_ingredients: List[str]) -> Meal:
    with Session(engine) as session:
        meal = Meal(name=meal_name)
        
        session.add(meal)
        try:
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise AlreadyPresent(f"Meal with name {meal_name} already present in database")
            
        ingredients = [Ingredient(name=x) for x in meal_ingredients]
        #We need to check what ingredients already exist in our DB. 
        for ingredient in ingredients:
            session.add(ingredient)
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
        
                #Retrieve the ID of the already existing ingredient
                db_ingredient = session.exec(select(Ingredient).where(Ingredient.name == f"{ingredient.name}")).one_or_none()
                if db_ingredient:
                    ingredient.id = db_ingredient.id  
                else:
                    raise e.add_detail(f"Ingredient already in DB but not found under name {ingredient.name}")
                pass
            
            #Manually patch the join table
            finally:
                session.add(MealIngredient(meal_id=meal.id, ingredient_id=ingredient.id))
                session.commit()
                session.flush()

        session.refresh(meal)
        
        return meal
    
def timestamp():
    return time.now().strftime("%d/%m/%Y %H:%M:%S")
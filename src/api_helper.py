import requests
import models
import json

def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))

async def post_feel(feel: models.Feel):
    feel_dict = feel.to_dict()
    feel_dict['symptoms'] = feel.symptoms.value
    response = requests.post(url="http://127.0.0.1:8000/api/feel/", json=feel_dict)
    
async def post_ingredient(ingredient: models.Ingredient):
    response = requests.post(url="http://127.0.0.1:8000/api/ingredient/", json=ingredient.to_dict())
    response_json = response.json()
    return models.Ingredient(name=response_json['name'], id=response_json['id'])
    
async def get_ingredients():
    ingredients = []
    response = requests.get(url="http://127.0.0.1:8000/api/ingredient/")
    for ingredient in response.json():
        ingredients.append(models.Ingredient(name=ingredient['name'], id=ingredient['id']))
    return ingredients
    
async def post_meal(meal: models.Meal):
    ingredient_ids = [x.id for x in meal.ingredients]
    payload = dict(zip(["meal_name", "ingredients"], [meal.meal_name, ingredient_ids]))
    return requests.post(url="http://127.0.0.1:8000/api/meal/", json=payload)

async def get_meals():
    meals = []
    response = requests.get(url="http://127.0.0.1:8000/api/meal/")
    for meal in response.json():
        meals.append(models.Meal(meal_name=meal['meal_name']))
    return meals
    
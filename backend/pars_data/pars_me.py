import json
from recipes.models import IngredientModel


with open('ingredients.json') as json_file:
    data = json.load(json_file)
    for num in data:
        IngredientModel.objects.create(name=num['title'], measurement_unit=num['dimension'],)

import json

from django.core.management.base import BaseCommand
from models import Ingredient


class Command(BaseCommand):
    help = 'Add new ingredients model from ingredients.json'

    def pars(self):
        with open('data/ingredients.json') as json_file:
            data = json.load(json_file)
            for num in data:
                Ingredient.objects.create(
                    name=num['title'],
                    measurement_unit=num['dimension'],
                )

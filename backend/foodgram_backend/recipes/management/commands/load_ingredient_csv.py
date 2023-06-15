import csv

from django.core.management.base import BaseCommand

from foodgram_backend.settings import BASE_DIR
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Команда загрузки ингредиентов и их количества из csv'

    def handle(self, *args, **optoins):
        self.stdout.write('Идет загрузка индгридиентов в бд')
        Ingredient.objects.all().delete()
        with open(
                f'{BASE_DIR}/data/ingredients.csv',
                encoding='utf-8',
        ) as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                name = row[0]
                measurement_unit = row[1]
                Ingredient.objects.get_or_create(
                    name=name,
                    measurement_unit=measurement_unit
                )
        self.stdout.write('Загрузка завершена!')




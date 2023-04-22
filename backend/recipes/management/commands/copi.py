import csv
import os
import django

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

# settings.configure(AUTH_USER_MODEL='users.UserFoodgram')

from recipes.models import Ingredient

DATA_ROOT = os.path.join(settings.BASE_DIR, 'data')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodgram.settings')
# settings.configure(AUTH_USER_MODEL='users.UserFoodgram')


class Command(BaseCommand):
    """
    Скрипт для формирования команды добавки ингридиентов в базу из csv file
    """
    help = 'loading ingredients from data in json or csv'


    def add_arguments(self, parser):
        parser.add_argument(
            'filename',
            default='ingredients.csv',
            nargs='?',
            type=str
        )


    def handle(self, *args, **options):
        print(DATA_ROOT)
        try:
            with open(os.path.join(DATA_ROOT, options['filename']), 'r',
                      encoding='utf-8') as f:
                data = csv.reader(f)
                for row in data:
                    name, measurement_unit = row
                    Ingredient.objects.get_or_create(
                        name=name,
                        measurement_unit=measurement_unit
                    )
                print('Load ingredients.csv have successful finished')
        except FileNotFoundError:
            raise CommandError('Добавьте файл ingredients в директорию data')


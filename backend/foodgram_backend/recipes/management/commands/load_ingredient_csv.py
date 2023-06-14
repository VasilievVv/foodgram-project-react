import csv

from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = './'

    def handle(self, *args, **options):
        path = settings.BASE_DIR /


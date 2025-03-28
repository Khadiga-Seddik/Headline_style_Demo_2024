# NewsRec_App/management/commands/load_data.py

import os
import csv
import logging
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date
from ...models import News_article  # Adjust the import path

class Command(BaseCommand):
    help = 'Load data into the database'

    def add_arguments(self, parser):
        # Define the command-line argument for the file path
        parser.add_argument('file_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        file_path = options["file_path"]  # Adjust the file path based on your project structure

        with open(file_path) as f:
            reader = csv.reader(f)
            for row in reader:
                _, created = News_article.objects.get_or_create(
                    aid=row[0], # + "_1",  # Comment out the '+ "_1"' and remove the "," (comma) after row[0], before loading the baseline. 
                    title=row[1],
                    text=row[2],
                    author=row[3],
                    date=parse_date(row[4]),
                    time=row[5],
                    image_url=row[6],
                    image_caption=row[7],
                    author_bio=row[8],
                    reading_time=row[9],
                    support=row[10],
                )
                

        self.stdout.write(self.style.SUCCESS('Data loaded successfully.'))
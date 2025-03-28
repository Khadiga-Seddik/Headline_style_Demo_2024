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
                print(row[0])
                _, created = News_article.objects.get_or_create(

                    aid=row[0],
                    original_title=row[1],
                    image_url=row[2],
                    date = parse_date(row[3]),
                    article_url=row[4],
                    category=row[5],
                    text=row[6],
                    style=row[7],
                    manipulated_title=row[8],
                    title= row[9] #manipulated boring title
                )


        self.stdout.write(self.style.SUCCESS('Data loaded successfully.'))
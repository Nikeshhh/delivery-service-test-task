import csv

from django.db.transaction import atomic

from core.apps.delivery.models import Location

def load_locations_from_csv(filename: str):
    """Загружает в БД локации из CSV файла"""
    with open(filename, newline='') as loc_file:
        csv_reader = csv.reader(loc_file)
        next(csv_reader)
        with atomic():
            for row in csv_reader:
                Location.objects.create(
                    zip_code=row[0],
                    latitude=float(row[1]),
                    longitude=float(row[2]),
                    city=row[3],
                    state=row[5]
                )

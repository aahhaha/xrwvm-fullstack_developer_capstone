import json
from pathlib import Path
from .models import CarMake, CarModel

def initiate():
    data = json.loads((Path(__file__).resolve().parent.parent / 'database/data/car_records.json').read_text())
    for item in data['cars']:
        make, _ = CarMake.objects.get_or_create(name=item['make'], defaults={'description': item['make'] + ' vehicles'})
        CarModel.objects.get_or_create(car_make=make, name=item['model'], year=item['year'], defaults={'type':item['bodyType']})

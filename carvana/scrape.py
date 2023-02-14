from collections import namedtuple
import httpx
import random
import re
import json
import time
from bs4 import BeautifulSoup

VEHICLE_QUERIES = (
    'chevrolet-colorado-crew-cab/4wd',
    'chevrolet-silverado-1500-crew-cab/4wd',
    'chevrolet-suburban/4wd',
    'chevrolet-suburban-1500/4wd',
    'chevrolet-tahoe/4wd',
    'chrysler-pacifica',
    'ford-expedition/4wd',
    'ford-expedition-el/4wd',
    'ford-expedition-max/4wd',
    'ford-f150-supercrew-cab/4wd',
    'ford-ranger-supercrew/4wd',
    'gmc-canyon-crew-cab/4wd',
    'gmc-sierra-1500-crew-cab/4wd',
    'gmc-sierra-1500-limited-crew-cab/4wd',
    'honda-odyssey',
    'jeep-gladiator',
    'nissan-armada/4wd',
    'nissan-frontier-crew-cab/4wd',
    'nissan-titan-crew-cab/4wd',
    'ram-1500-crew-cab/4wd',
    'ram-1500-classic-crew-cab/4wd',
    'toyota-sienna',
    'toyota-tacoma-double-cab/4wd',
    'toyota-tundra-crewmax/4wd',
)


def models(queries=VEHICLE_QUERIES, dbug=False):
    '''helper function to scrape multiple models, returns a generator'''
    for q in queries:
        yield model(q, dbug=dbug)


def model(query: str, dbug=False):
    '''scrape a specific model as defined in the query parameter'''
    page = 0
    url = f'https://www.carvana.com/cars/{query}'

    while True:
        page += 1
        print(f'[DEBUG] scraping page {page} of query {query}')
        with httpx.Client(timeout=120) as client:
            resptext = client.get(url, params={'page': page}).text

        if dbug:
            with open('data/dbug_inventory.html', 'w+') as file:
                file.write(resptext)

        inventory = extract_inventory(resptext)
        if len(inventory) < 1:
            break

        if dbug:
            with open('data/dbug_inventory.json', 'w+') as file:
                json.dump(inventory, file)

        for inv_item in inventory:
            if dbug:
                with open('data/dbug_inventory_item.json', 'w+') as file:
                    json.dump(inv_item, file)

            # non-listings are insterspersed with listings
            id = inv_item.get('vehicleId')
            if id is None:
                continue

            yield extract_inventory_item(id, dbug=dbug)

            # sleep random time to mimic human user
            sleep_dur = random.randint(5, 15)
            print(f'sleeping for {sleep_dur} seconds')
            time.sleep(sleep_dur)


def extract_inventory(htmlpage: str):
    bs = BeautifulSoup(htmlpage, 'html.parser')
    data = bs.find('script', text=re.compile(
        'window.__PRELOADED_STATE__')).get_text()

    payload = data.split('window.__PRELOADED_STATE__ = ')[
        1].split('window.__APOLLO_STATE__')[0]

    jsonpayload = json.loads(payload)
    return jsonpayload['v2/inventory']['vehicles']


def extract_inventory_item(id, dbug=False):
    '''loads and extracts a an inventory item'''
    with httpx.Client(timeout=120) as client:
        resp_text = client.get(f'https://www.carvana.com/vehicle/{id}').text

    bs = BeautifulSoup(resp_text, 'html.parser')
    vehicle_text = bs.find('script', {"id": "__NEXT_DATA__"}).text
    vehicle_json = json.loads(vehicle_text)
    vehicle = vehicle_json['props']['pageProps']['initialState']['vehicle']['details']
    return build_listing(vehicle, dbug=dbug)


def build_listing(vehicle: dict, dbug=False):
    if dbug:
        with open('data/dbug_vehicle.json', 'w+') as file:
            json.dump(vehicle, file)

    try:
        listing = {
            'body_type': vehicle['bodyType'],
            'carvana_id': vehicle['vehicleId'],
            'city': vehicle['location']['city'],
            'drive_type': vehicle['drivetrainDescription'],
            'engine': vehicle['engineDescription'],
            'exterior_color': vehicle['exteriorColor'],
            'features': [f['displayName'] for kf in vehicle.get('kbbFeatures', {}) for f in kf.get('features', [])],
            'fuel': vehicle.get('fuelDescription'),
            'imperfections': [
                {
                    'description': i['description'],
                    'location': i['location'],
                    'title': i['title'],
                    'zone': i['zoneDescription'],
                } for i in vehicle.get('vexVdpImageData', {}).get('imperfections', [])
            ],
            'interior_color': vehicle['interiorColor'],
            'kbb_value': vehicle['kbbValue'],
            'make': vehicle['make'],
            'mfg_basic_warranty_miles': vehicle["manufacturerBasicWarrantyMiles"],
            'mg_basic_warranty_months': vehicle["manufacturerBasicWarrantyMonths"],
            'mfg_drivetrain_warranty_miles': vehicle["manufacturerDriveTrainWarrantyMiles"],
            'mfg_drivetrain_warranty_months': vehicle["manufacturerDriveTrainWarrantyMonths"],
            'mileage': vehicle['mileage'],
            'model': vehicle['model'],
            'num_keys': vehicle['numberOfKeys'],
            'options': vehicle.get('installedOptions', []),
            'price': vehicle['price'],
            'remaining_warranty_miles': vehicle["remainingWarrantyMiles"],
            'remaining_warranty_months': vehicle["remainingWarrantyMonths"],
            'remaining_drivetrain_warranty_months': vehicle["remainingDriveTrainWarrantyMiles"],
            'remaining_drivetrain_warranty_miles': vehicle["remainingDriveTrainWarrantyMonths"],
            'state': vehicle['location']['stateAbbreviation'],
            'std_equipment': vehicle.get('standardEquipment', []),
            'transmission': vehicle.get('transmission'),
            'trim': vehicle.get('trim'),
            'vin': vehicle['vin'],
            'year': vehicle['year'],
            'zip': vehicle['location']['zip5'],
        }
    except Exception as e:
        print(f'failed to build listing with id {vehicle["vehicleId"]}: {e}')
        raise e

    return listing


def _headers():
    return {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
    }

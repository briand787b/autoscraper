from collections import namedtuple
import httpx
import re
import json
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


def models(queries=VEHICLE_QUERIES):
    '''helper function to scrape multiple models, returns a generator'''
    for q in queries:
        yield model(q)


def model(query: str):
    '''scrape a specific model as defined in the query parameter'''
    page = 1
    url = f'https://www.carvana.com/cars/{query}'

    while True:
        print(f'[DEBUG] scraping page {page} of query {query}')
        with httpx.Client(timeout=120) as client:
            resp = client.get(url, params={'page': page})

        inventory = extract_inventory(resp.text)
        if len(inventory) < 1:
            return

        for vehicle in inventory:
            yield extract_inventory_item(vehicle['vehicleId'])


def extract_inventory(htmlpage: str):
    bs = BeautifulSoup(htmlpage, 'html.parser')
    data = bs.find('script', text=re.compile(
        'window.__PRELOADED_STATE__')).get_text()

    payload = data.split('window.__PRELOADED_STATE__ = ')[
        1].split('window.__APOLLO_STATE__')[0]

    jsonpayload = json.loads(payload)
    return jsonpayload['v2/inventory']['vehicles']


def extract_inventory_item(id):
    with httpx.Client(timeout=120) as client:
        resp = client.get('https://www.carvana.com/vehicle/2548188')
        # print(f'resp: {resp}')
        resp_text = resp.text
        # print(f'resp: {resptext}')

    # print("\n\n\n\n\n\n\n")
    bs = BeautifulSoup(resp_text, 'html.parser')
    # print()
    # print(f'bs: {bs}')
    vehicle_text = bs.find('script', {"id": "__NEXT_DATA__"}).text
    # print(f'vehicle_text: {vehicle_text}')
    return build_listing(json.loads(vehicle_text)['props']['pageProps']['initialState']['vehicle']['details'])


def build_listing(vehicle: dict):
    with open('data/_scrape_vehicle.json', 'w+') as file:
        json.dump(vehicle, file)

    return {
        'body_type': vehicle['bodyType'],
        'carvana_id': vehicle['vehicleId'],
        'city': vehicle['location']['city'],
        'drive_type': vehicle['drivetrainDescription'],
        'engine': vehicle['engineDescription'],
        'exterior_color': vehicle['exteriorColor'],
        'features': [f['displayName'] for kf in vehicle['kbbFeatures'] for f in kf['features']],
        'fuel': vehicle['fuelDescription'],
        'imperfections': [
            {
                'description': i['description'],
                'location': i['location'],
                'title': i['title'],
                'zone': i['zoneDescription'],
            } for i in vehicle['vexVdpImageData'].get('imperfections', [])
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
        'transmission': vehicle['transmission'],
        'trim': vehicle['trim'],
        'vin': vehicle['vin'],
        'year': vehicle['year'],
        'zip': vehicle['location']['zip5'],
    }


def _headers():
    return {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
    }

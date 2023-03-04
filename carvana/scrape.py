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
        try:
            yield model(q, dbug=dbug)
        except Exception as e:
            print(f'encountered exception while iterating queries: {e}')
            continue


def model(query: str, dbug=False):
    '''scrape a specific model as defined in the query parameter'''
    page = 0

    while True:
        page += 1
        resptext = _send_req(query=query, page=page, dbug=dbug)

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
            if dbug:
                print(f'[DEBUG] sleeping for {sleep_dur} seconds')
            time.sleep(sleep_dur)


def _send_req(query: str, page: int, dbug=False):
    '''
    _send_req is a low-level wrapper around the HTTP calls.  
    It also handles retries
    '''
    if dbug:
        print(f'[DEBUG] scraping page {page} of query {query}')
    url = f'https://www.carvana.com/cars/{query}'
    with httpx.Client(timeout=120) as client:
        attempt = 0
        while True:
            try:
                attempt += 1
                resp = client.get(url, params={'page': page})
                return resp.text
            except Exception as e:
                print(
                    f'[attempt #{attempt}] encountered problem while sending request: {e}')

                if attempt > 2:
                    raise e

                time.sleep(5)


def extract_inventory(htmlpage: str):
    bs = BeautifulSoup(htmlpage, 'html.parser')
    data = bs.find('script', text=re.compile('window.__PRELOADED_STATE__'))
    if not data:
        return None

    data_text = data.get_text()
    payload = data_text.split('window.__PRELOADED_STATE__ = ')[
        1].split('window.__APOLLO_STATE__')[0]

    jsonpayload = json.loads(payload)
    return jsonpayload['v2/inventory']['vehicles']


def extract_inventory_item(id, dbug=False):
    '''loads and extracts a an inventory item'''

    with httpx.Client(timeout=120) as client:
        attempt = 0
        while True:
            try:
                attempt += 1
                resp_text = client.get(
                    f'https://www.carvana.com/vehicle/{id}').text
                break
            except Exception as e:
                print(
                    f'[attempt #{attempt}] encountered problem while sending request: {e}')

                if attempt > 2:
                    raise e

                time.sleep(5)

    bs = BeautifulSoup(resp_text, 'html.parser')
    vehicle_text = bs.find('script', {"id": "__NEXT_DATA__"}).text
    vehicle_json = json.loads(vehicle_text)
    vehicle = vehicle_json.get('props', {}).get('pageProps', {}).get(
        'initialState', {}).get('vehicle', {}).get('details', '')
    if vehicle == '':
        return None

    return build_listing(vehicle, dbug=dbug)


def build_listing(vehicle: dict, dbug=False):
    if dbug:
        with open('data/dbug_vehicle.json', 'w+') as file:
            json.dump(vehicle, file)

    try:
        listing = {
            'body': vehicle.get('bodyType'),
            'carvana_id': vehicle['vehicleId'],
            'city': vehicle.get('location', {}).get('city'),
            'color': vehicle.get('exteriorColor'),
            'drive_type': vehicle.get('drivetrainDescription'),
            'engine': vehicle.get('engineDescription'),
            'features': [
                {
                    'id': f.get('kbbOptionId'),
                    'name': f.get('displayName'),
                } for kf in vehicle.get('kbbFeatures', {}) for f in kf.get('features', [])
            ],
            'fuel': vehicle.get('fuelDescription'),
            'highlights': [h.get('tagKey') for h in vehicle.get('highlights')],
            'imperfections': [
                {
                    'id': i.get('id'),
                    'desc': i.get('description'),
                    'loc': i.get('location'),
                    'title': i.get('title'),
                    'zone': i.get('zoneDescription'),
                } for i in vehicle.get('vexVdpImageData', {}).get('imperfections', [])
            ],
            'kbb_value': vehicle.get('kbbValue'),
            'make': vehicle['make'],
            'mfg_basic_warranty_miles': vehicle.get("manufacturerBasicWarrantyMiles"),
            'mfg_basic_warranty_months': vehicle.get("manufacturerBasicWarrantyMonths"),
            'mfg_dt_warranty_miles': vehicle.get("manufacturerDriveTrainWarrantyMiles"),
            'mfg_dt_warranty_months': vehicle.get("manufacturerDriveTrainWarrantyMonths"),
            'mileage': vehicle.get('mileage'),
            'model': vehicle['model'],
            'num_keys': vehicle.get('numberOfKeys'),
            'options': vehicle.get('installedOptions', []),
            'price': vehicle.get('price'),
            'rem_warranty_miles': vehicle.get("remainingWarrantyMiles"),
            'rem_warranty_months': vehicle.get("remainingWarrantyMonths"),
            'rem_dt_warranty_miles': vehicle.get("remainingDriveTrainWarrantyMiles"),
            'rem_dt_warranty_months': vehicle.get("remainingDriveTrainWarrantyMonths"),
            'seating': vehicle.get('seating'),
            'state': vehicle.get('location', {}).get('stateAbbreviation'),
            'std_equipment': vehicle.get('standardEquipment', []),
            'transmission': vehicle.get('transmission'),
            'trim': vehicle.get('trim'),
            'vin': vehicle['vin'],
            'year': vehicle['year'],
            'zip': vehicle.get('location', {}).get('zip5'),
        }
    except KeyError as e:
        print(f'[id={vehicle.get("vehicleId")}] missing critical key: {e}')
        return {}
    except Exception as e:
        print(
            f'failed to build listing with id {vehicle.get("vehicleId")}: {e}')
        raise e

    return listing

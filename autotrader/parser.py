#!/usr/bin/env python3

import json
import re
import sys

default_invfile = 'examples/100_items.json'


re_bed_len = re.compile('[0-9]+-Inch Bed')
re_carplay = re.compile('[c|C]ar[p|P]lay')


def main(filename: str):
    with open(filename, 'r') as f:
        payload = json.load(f)

    parse(payload)


def parse(payload: dict):
    try:
        inventory = payload['initialState']['inventory']
    except KeyError as e:
        e.add_note('did not receive full payload')
        raise

    inv_items = []
    for id, inv in inventory.items():
        inv_items.append({
            'autotrader_id': id,
            'carplay': carplay(inv),
            'color': color(inv),
            'drive_type': drive_type(inv),
            'engine': engine(inv),
            'features': features(inv),
            'make': manufacturer(inv),
            'mileage': mileage(inv),
            'model': model(inv),
            'mpg_city': mpg_city(inv),
            'mpg_hwy': mpg_hwy(inv),
            'packages': pkgs(inv),
            'price': price(inv),
            'trim': trim(inv),
            'truck_bed': truck_bed(inv),
            'truck_cab': truck_cab(inv),
            'vin': vin(inv),
            'zip': zip(inv),
        })

    print(json.dumps(inv_items[-1], indent=4))
    print(f'count: {len(inv_items)}')


def carplay(inv: dict):
    features = inv.get('features', [])
    qvFeatures = inv.get('quickViewFeatures', [])
    for f in features + qvFeatures:
        if re_carplay.search(f):
            return True

    return False


def color(inv: dict):
    color = None
    try:
        color = inv['specifications']['color']['value'].lower()
    except:
        log(inv, 'could not get color')
    finally:
        return color


def drive_type(inv: dict):
    dt = ''
    try:
        dt = inv['specifications']['driveType']['value']
    except:
        log(inv, 'could not get drive type')
    finally:
        return dt.lower()


def engine(inv: dict):
    try:
        eng = inv['engine']['name'].lower()
    except KeyError:
        try:
            eng = inv['specifications']['engine']['value'].lower()
        except KeyError:
            log(inv, log(inv, 'could not find engine key'))

    return eng


def features(inv: dict):
    try:
        feat = inv['features']
    except KeyError as e:
        log(inv, f'could not find features key: {e}')
        return None

    return feat


def log(inv: dict, msg: str):
    acc = ''
    if inv['accelerate'] == True:
        acc = ' (acc)'

    print(f'[{inv["id"]}{acc}] ' + msg)


def manufacturer(inv: dict):
    mfg = ''
    try:
        mfg = inv['make']
        mfg = mfg['name'].lower()
    except KeyError as e:
        log(inv, f'could not get manufacturer key: {e}')
    finally:
        return mfg


def mileage(inv: dict):
    try:
        m_str = inv['specifications']['mileage']['value']
        m = int(m_str.replace(',', ''))
    except Exception as e:
        log(inv, f'could not get mileage {e}')
        return None

    return m


def model(inv: dict):
    m = ''
    try:
        m = inv['model']
        m = m['name'].lower()
    except KeyError as e:
        log(inv, f'could not find model key: {e}')
    finally:
        return m


def mpg_city(inv: dict):
    try:
        mpg_str = inv['mpgCity']
    except KeyError:
        try:
            mpg_str = inv['specifications']['mpg']['value'].split(' ')[0]
        except Exception as e:
            log(inv, f'missing key for mpg (city): {e}')
            return None

    try:
        mpg = int(mpg_str)
    except TypeError:
        log(inv, f'cannnot convert {e} to int')
        return None

    return mpg


def mpg_hwy(inv: dict):
    try:
        mpg_str = inv['mpgHighway']
    except KeyError:
        try:
            mpg_str = inv['specifications']['mpg']['value'].split(' ')[3]
        except Exception as e:
            log(inv, f'missing key for mpg (hwy): {e}')
            return None

    try:
        mpg = int(mpg_str)
    except TypeError:
        log(inv, f'cannnot convert {e} to int')
        return None

    return mpg


def pkgs(inv: dict):
    return inv.get('packages')


def price(inv: dict):
    try:
        p_str = inv['pricingDetail']['salePrice']
        price = int(p_str)
        return price
    except KeyError as e:
        log(inv, f'could not find pricing key "{e}"')
    except TypeError as e:
        log(inv, f'could not convert price str {p_str} to int')


def trim(inv: dict):
    try:
        t = inv['trim']
        if type(t) == str:
            return t.lower()

        return t['name'].lower()
    except KeyError as e:
        log(inv, f'could not find trim key: {e}')


def truck_bed(inv: dict):
    try:
        return inv['truckBedLength'].lower()
    except KeyError as e:
        try:
            for feature in inv['quickViewFeatures']:
                if re_bed_len.search(feature):
                    return feature

            return None
        except KeyError as e:
            log(inv, f'could not find truck bed length key: {e}')


def truck_cab(inv: dict):
    try:
        return inv['specifications']['truckCabSize']['value'].lower()
    except KeyError as e:
        log(inv, f'could not find truck cab size field: {e}')


def vin(inv: dict):
    try:
        return inv['vin'].upper()
    except KeyError as e:
        log(inv, f'could not find vin key: {e}')


def zip(inv: dict):
    try:
        return inv['zip']
    except KeyError:
        try:
            return inv['owner']['location']['address']['zip']
        except KeyError:
            log(inv, 'could not find zip code field')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        file = sys.argv[1]
    else:
        file = default_invfile

    main(file)

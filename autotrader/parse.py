import json
import re

# TODO:
# Limit the size of feature/package list items to avoid db exeptions


re_bed_len = re.compile('[0-9]+-Inch Bed')
re_carplay = re.compile('[c|C]ar[p|P]lay')


# Entrypoints


def parse(payload: dict, debuglvl = False):
    '''
    parse is the entrypoint into this module.  It takes a dictionary,
    typically originating from a JSON document, and pulls values from it.
    '''
    try:
        inventory = payload['initialState']['inventory']
    except KeyError as e:
        e.add_note('did not receive full payload')
        raise

    inv_items = []
    for id, inv in inventory.items():
        inv_items.append({
            'autotrader_id': id,
            'color': color(inv, debuglvl),
            'condition': condition(inv, debuglvl),
            'drive_type': drive_type(inv, debuglvl),
            'engine': engine(inv, debuglvl),
            'features': features(inv, debuglvl),
            'make': manufacturer(inv, debuglvl),
            'mileage': mileage(inv, debuglvl),
            'model': model(inv, debuglvl),
            'mpg_city': mpg_city(inv, debuglvl),
            'mpg_hwy': mpg_hwy(inv, debuglvl),
            'owner': owner(inv, debuglvl),
            'packages': pkgs(inv, debuglvl),
            'price': price(inv, debuglvl),
            'trim': trim(inv, debuglvl),
            'truck_bed': truck_bed(inv, debuglvl),
            'truck_cab': truck_cab(inv, debuglvl),
            'vin': vin(inv, debuglvl),
            'year': year(inv, debuglvl),
            'zip': zip(inv, debuglvl),
        })

    if len(inv_items) < 1:
        raise Exception(
            'no items returned from scrape; this should never happen')

    if debuglvl:
        print(f'count: {len(inv_items)}')
        print(json.dumps(inv_items[-1], indent=4))

    return inv_items


# Internal


def color(inv: dict, debuglvl = False):
    try:
        return inv['specifications']['color']['value'].lower()
    except:
        log(inv, 'could not get color', debuglvl)


def condition(inv: dict, debuglvl = False):
    try:
        return inv['listingType'].lower()
    except KeyError:
        pass

    try:
        for t in inv['listingTypes']:
            t = t.lower()
            if t in ('used', 'new'):
                return t
    except KeyError as e:
        log(inv, f'could not find listing type/condition: {e}', debuglvl)


def drive_type(inv: dict, debuglvl = False):
    try:
        return inv['specifications']['driveType']['value'].lower()
    except:
        log(inv, 'could not get drive type', debuglvl)


def engine(inv: dict, debuglvl = False):
    try:
        return inv['engine']['name'].lower()
    except KeyError:
        try:
            return inv['specifications']['engine']['value'].lower()
        except KeyError:
            log(inv, 'could not find engine key', debuglvl)


def features(inv: dict, debuglvl = False):
    featrs = inv.get('features', [])
    try:
        return [f['name'] for f in featrs]
    except Exception:
        return featrs


def log(inv: dict, msg: str, debuglvl = False):
    if not debuglvl:
        return

    acc = ''
    if inv['accelerate'] == True:
        acc = ' (acc)'

    print(f'[{inv["id"]}{acc}] ' + msg)


def manufacturer(inv: dict, debuglvl = False):
    try:
        mfg = inv['make']
        if type(mfg) == str:
            return mfg.lower()

        return mfg['name'].lower()
    except KeyError as e:
        log(inv, f'could not get manufacturer key: {e}', debuglvl)


def mileage(inv: dict, debuglvl = False):
    try:
        m_str = inv['specifications']['mileage']['value']
        return int(m_str.replace(',', ''))
    except Exception as e:
        log(inv, f'could not get mileage {e}', debuglvl)


def model(inv: dict, debuglvl = False):
    try:
        mfg = inv['model']
        if type(mfg) == str:
            return mfg.lower()

        return mfg['name'].lower()
    except KeyError as e:
        log(inv, f'could not get model key: {e}', debuglvl)


def mpg_city(inv: dict, debuglvl = False):
    try:
        mpg_str = inv['mpgCity']
    except KeyError:
        try:
            mpg_str = inv['specifications']['mpg']['value'].split(' ')[0]
        except Exception as e:
            log(inv, f'missing key for mpg (city): {e}', debuglvl)
            return None

    try:
        mpg = int(mpg_str)
    except TypeError:
        log(inv, f'cannnot convert {e} to int', debuglvl)
        return None

    return mpg


def mpg_hwy(inv: dict, debuglvl = False):
    try:
        mpg_str = inv['mpgHighway']
    except KeyError:
        try:
            mpg_str = inv['specifications']['mpg']['value'].split(' ')[3]
        except Exception as e:
            log(inv, f'missing key for mpg (hwy): {e}', debuglvl)
            return None

    try:
        mpg = int(mpg_str)
    except TypeError:
        log(inv, f'cannnot convert {e} to int', debuglvl)
        return None

    return mpg


def owner(inv: dict, debuglvl = False):
    try:
        return inv['ownerName']
    except KeyError:
        try:
            return inv['owner']['name']
        except KeyError as e:
            log(inv, f'could not get owner key: {e}', debuglvl)


def pkgs(inv: dict, debuglvl = False):
    packages = inv.get('packages', [])
    try:
        return [p['name'] for p in packages]
    except Exception:
        return packages


def price(inv: dict, debuglvl = False):
    try:
        p_str = inv['pricingDetail']['salePrice']
        price = int(p_str)
        return price if price > 0 else None
    except KeyError as e:
        log(inv, f'could not find pricing key "{e}"', debuglvl)
    except TypeError as e:
        log(inv, f'could not convert price str {p_str} to int', debuglvl)


def trim(inv: dict, debuglvl = False):
    try:
        t = inv['trim']
        if type(t) == str:
            return t.lower()

        return t['name'].lower()
    except KeyError as e:
        log(inv, f'could not find trim key: {e}', debuglvl)


def truck_bed(inv: dict, debuglvl = False):
    try:
        return inv['truckBedLength'].lower()
    except KeyError as e:
        try:
            for feature in inv['quickViewFeatures']:
                if re_bed_len.search(feature):
                    return feature.lower()

            return None
        except KeyError as e:
            log(inv, f'could not find truck bed length key: {e}', debuglvl)


def truck_cab(inv: dict, debuglvl = False):
    try:
        return inv['specifications']['truckCabSize']['value'].lower()
    except KeyError as e:
        log(inv, f'could not find truck cab size field: {e}', debuglvl)


def vin(inv: dict, debuglvl = False):
    try:
        return inv['vin'].upper()
    except KeyError as e:
        log(inv, f'could not find vin key: {e}', debuglvl)


def year(inv: dict, debuglvl = False):
    try:
        return int(inv['year'])
    except KeyError:
        log(inv, 'could not get year key', debuglvl)
    except TypeError as e:
        log(inv, f'could not cast {e} to int', debuglvl)


def zip(inv: dict, debuglvl = False):
    try:
        return inv['zip']
    except KeyError:
        try:
            return inv['owner']['location']['address']['zip']
        except KeyError:
            log(inv, 'could not find zip code field', debuglvl)

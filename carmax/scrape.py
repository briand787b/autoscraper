import json
from urllib.parse import urlencode
import httpx
import random
from time import sleep

# common filters
FILTER_FOUR_WHEEL_DRIVE = '4wdawd'
FILTER_CREW_CAB = '4d-crew-cab'


def all_queries():
    '''convenience helper for querying all models with default filters'''
    return (
        ('chevrolet', 'colorado', (FILTER_CREW_CAB, FILTER_FOUR_WHEEL_DRIVE)),
        ('chevrolet', 'silverado-1500',
         (FILTER_CREW_CAB, FILTER_FOUR_WHEEL_DRIVE)),
        ('chevrolet', 'suburban', (FILTER_FOUR_WHEEL_DRIVE)),
        ('chevrolet', 'tahoe', (FILTER_FOUR_WHEEL_DRIVE)),
        ('ford', 'expedition', (FILTER_FOUR_WHEEL_DRIVE)),
        ('ford', 'f150', (FILTER_CREW_CAB, FILTER_FOUR_WHEEL_DRIVE)),
        ('honda', 'odyssey', []),
        ('nissan', 'frontier', (FILTER_CREW_CAB, FILTER_FOUR_WHEEL_DRIVE)),
        ('nissan', 'titan', (FILTER_CREW_CAB, FILTER_FOUR_WHEEL_DRIVE)),
        ('ram', '1500', (FILTER_CREW_CAB, FILTER_FOUR_WHEEL_DRIVE)),
        ('toyota', 'tacoma', (FILTER_CREW_CAB, FILTER_FOUR_WHEEL_DRIVE)),
        ('toyota', 'tundra', (FILTER_CREW_CAB, FILTER_FOUR_WHEEL_DRIVE)),
    )


def api(queries: list, chunk_size=100):
    '''
    scrapes the carmax API.  
        `queries` must be a 3-tuple with the following components:
            [0]: make
            [1]: model
            [2]: filters to search on
    '''
    for q in queries:
        yield model(q[0], q[1], *q[2], chunk_size=chunk_size)


def model(make, model, *filters, chunk_size=100, dbug=False):
    '''
    scrapes the carmax API for a specific make/model.  
        `filters` are features to search on (e.g. 4wdawd, 4d-crew-cab, etc...)
        `chunk_size` specifies how many listings to retrieve per iteration
    '''
    skip = 0
    while True:
        resp = send_req(make, model, *filters, skip=skip,
                        take=chunk_size, dbug=dbug)
        listings = parse_resp(resp)
        yield listings
        if len(listings) < chunk_size:
            break
        skip += chunk_size
        sleep_dur = random.randint(10, 30)
        print(f'sleeping for {sleep_dur} seconds')
        sleep(sleep_dur)


def send_req(make, model, *filters, skip=0, take=100, dbug=False):
    if filters is None:
        filters = []

    search = f'/cars/{make}/{model}'
    for f in filters:
        search += f'/{f}'

    print(f'search filter: {search}')
    with httpx.Client(timeout=120) as client:
        attempt = 0
        while True:
            try:
                resp = client.get(
                    f'https://www.carmax.com/cars/api/search/run?uri={search}&year=2016-2023&price=50000&skip={skip}&take={take}&radius=radius-nationwide&shipping=-1',
                    headers={
                        'Cookie': 'KmxSession_0=SessionId=f9dcadd8-9252-4d8b-a064-832e0c6d7585&logOdds=0.4298310000000001&logOddsA=-1.435489244&logOddsI=0.9258658999999999; KmxStore=StoreId=6140; KmxVisitor_0=StoreId=6140&Zip=30606&Lat=33.9447&Lon=-83.4263&ZipConfirmed=True&ZipDate=2/6/2023 3:35:12 PM&VisitorID=813d3095-16d6-4bad-9287-0eb43afb7d3b&CookieDate=2/2/2023 3:20:27 AM&IsFirstVisit=False; _abck=8261582D852BF143C3DFDD6532142EA0~-1~YAAQSg3eF4DRBiSGAQAA8uxdJwl9v43OHQkRhz6dG8fANFJBs6ZGFuKUVYYaM5MgNkbaQMnGckMpICriT0Er5l3g3tpCT9EWgrlAKa8REUJ+MqIE65mW20ZNXCidlmVUDB+1VhANrZF2fX3eLcomhfyHSLJnDf936bBmpRtJgeGFNo1MVQ8US9tRoQcx1HaHrcknEQwfJwMVG9x2nTKrNZ9hmSGLfGs+0IrVlARiwP5a6JBOdzZGHFGTsp4ElQ1B6iUdKAId58zTLJP5BciCdYq05XET7O/e37VUIFw/EX28/cFvBrDMDNSHqtzuMIE+5TOmlqW8f9FmBq6nHPhl6H9DZ6O9yJn27oVvLOw7fKfEuY9pcH2zYiyMhHAWS8mCevPXbsptLw==~-1~-1~1675311518; ak_bmsc=F804F05BB4D92BF19D8289C9D8811214~000000000000000000000000000000~YAAQSg3eF4HRBiSGAQAA8uxdJxLpAynuzFy/XeITcWS3N+ICO/2q4pA2VLLRgHHUMqhsOnQEPfEoK0i1CdRmcEHXD24UmTkbW6zSrz+ouuZP9GQyJSKPwjhPF91krD6in3EUjwt2BcGRtuss4g5M6J4lfuAyALZwONWsvNl8F0ne/Ugq9ukfyadZ95BxCwQkNZS0KzaVEk2MhRrpYnP5RCOWVre7V48Z055dgHM7eZQdSMVg2e52CzP8Kxi0l0cQ1NITvR/jHGkmW5WVRPaKK7W2JnAmEHo+yGrdeb7yCQIwFLx+/waFyqr/s0SejZx1AJwmniiG1gqVlop/ouLCwuFJouzYcgoExqCSLgHnbJbk/APed6PVYHSbVmUz8A==; bm_sz=95486236FBFC3A3C9A089C481305E67D~YAAQSg3eF4LRBiSGAQAA8uxdJxJduNMckYwZUT0gCspBheoFaxzjP9Sa3IRQMbOl62eRqUWuG+i26lN5BQHzRvHKXep6WMEIldJZV3igIa76oaY05muASRihPAyxvpogk8o+W3sOY1U+qdQx7gSfLlm3zbE9rq+ToBdDiE65XcCI09+RnrXC+wbnZDXASOmoh4BRwDcohpFfI3y5ZW/o4LL2WmUpSYZ53Mc8J6b5DgjTNK+Jg+eNXO7HJOxixFQ3R8pxCwotLjdbWLvQfjGiQUiWR9URfmVkd0Fo7YspW5CSWqw=~4539203~4273731',
                        # fails with Mozilla, but works with Postman... wtf
                        'User-Agent': 'PostmanRuntime/7.30.0',
                    })

                break
            except Exception as e:
                print(
                    f'[attempt #{attempt}] encountered problem while sending request: {e}')

                if attempt > 2:
                    raise e

    print('completed request')
    respjson = resp.json()
    if dbug:
        with open('data/response.json', 'w+') as file:
            json.dump(respjson, file)

    return respjson


def parse_resp(respjson):
    items = []
    for i in respjson['items']:
        items.append({
            'body':         i['body'].lower(),
            'carmax_id':    i['stockNumber'],
            'city':         i['storeCity'].lower(),
            'color':        i['exteriorColor'].lower(),
            'drive_type':   i['driveTrain'].lower(),
            'engine_cyl':   _attr('cylinders', int, i),
            'engine_size':  _attr('engineSize', str, i),
            'engine_type':  _attr('engineType', str, i),
            'features':     i['features'],
            'highlights':   i['highlights'],
            'make':         i['make'].lower(),
            'mileage':      i['mileage'],
            'model':        i['model'].lower(),
            'mpg_city':     _attr('mpgCity', int, i),
            'mpg_hwy':      _attr('mpgHighway', int, i),
            'msrp':         _attr('msrp', int, i),
            'packages':     i['packages'],
            'price':        int(i['basePrice']),
            'prior_uses':   [int(p) for p in i['priorUses']],
            'state':        i['stateAbbreviation'].lower(),
            'store_id':     i['storeId'],
            'trim':         _attr('trim', str, i),
            'vin':          i['vin'],
            'year':         i['year'],
            'zip':          _attr('storeZip', str, i),
        })

    return items


def _attr(key: str, valtype, listing: dict):
    '''get nullable value from listing'''
    try:
        m = listing[key]
        if m is None:
            return

        if valtype is str:
            return m.lower()
        elif valtype is int:
            return int(m)
        else:
            raise Exception(f'unexpected valtype "{valtype}"')

    except KeyError as e:
        pass
    except Exception as e:
        print(f'[{listing["vin"]}] cannot find "{key}": {e}')
        raise e

import json
from urllib.parse import urlencode
import httpx
from time import sleep


def main():
    for listings in scrape_api('ferrari', 'f40', {}):
        print(f'saving {listings} to db')


def scrape_api(make, model, *filters, chunk_size = 100):
    skip = 0
    while True:
        listings = send_req(make, model, *filters, skip=skip, take=chunk_size)
        yield listings
        if len(listings) < chunk_size:
            break
        skip += chunk_size
        sleep(1)


def send_req(make, model, *filters, skip=0, take=100):
    if filters is None:
        filters = []

    search = f'/cars/{make}/{model}'
    for f in filters:
        search += f'/{f}'

    print(f'search filter: {search}')
    with httpx.Client(timeout=10) as client:
        resp = client.get(
            f'https://www.carmax.com/cars/api/search/run?uri={search}&year=2016-2023&price=50000&skip={skip}&take={take}&radius=radius-nationwide&shipping=-1',
            headers={
                'Cookie': 'KmxSession_0=SessionId=63e9cbff-4eee-40b5-93e9-72df72bcfb79&logOdds=0.42943299999999995&logOddsA=-1.3124279159999999&logOddsI=0.7750897999999998; KmxStore=StoreId=6140; KmxVisitor_0=StoreId=6140&Zip=30606&Lat=33.9447&Lon=-83.4263&ZipConfirmed=True&ZipDate=2/5/2023 1:48:32 PM&VisitorID=813d3095-16d6-4bad-9287-0eb43afb7d3b&CookieDate=2/2/2023 3:20:27 AM&IsFirstVisit=False; _abck=8261582D852BF143C3DFDD6532142EA0~-1~YAAQXA3eFwQkxx+GAQAA59zSIQn3Phm3R3vABJi8Thi/gice6+itMcXrT+am6h95AWNHAz4c5TJZ74AyQzmRsRYrtM6g2IK9KuvG3Lf00j/BytVsbLD+6vKa4Zw3ZL+DwZ7ngDbSBrOHhIrSUrYcfhgb5YYXLOpWg1P/9MSCKE6Qc1I86ZkP442BJ6K6GP+BFXKrntPmDcHzzGArRG07c1aXDSMTjypXtFdTe8JnDjLolzlsr3m6ODvBWSGDn+gY0d5J7AVFlXGXM5H8+bxur56ANFROq0HbFLJO09dxsZR0QWzBnJnpqnXscjc4f9y7IbfXAYwPD0VnZxYLz3NIiKRjS/wAmBkBAyLeZ7npZ3wCFGvP5EpUuow6H8QL21KZdqPtCTzXUA==~-1~-1~1675311518; ak_bmsc=54B7E0014BF5C45DF15AE5257AD959D4~000000000000000000000000000000~YAAQXA3eFwYkxx+GAQAA59zSIRI1xgLiB9ndv04ieZvVA8G2qFP4QV1rIHFP3jDc6OEhD6Vd0ZzHu5bCCd5j0RtYeFrZo0yTXE3bRl1ttAPQSvyp2BR+C3YbRhIGdJTqIYVhibYJiJN38V3tJpA1X2nR++ZBUBxKjqPEprcHYchciSIVxupLe0F4eB4tppXK+M6LeX7vLvXVQna70p8Ka5nhWkccRMCuEWiBZ7SaKmswB8tOzXJ9SSQ+QBoPl0TItWzK5CUL7F/mfZRNGSA+0GdPl2VAP+MrWVgpiqdjd4ia9itfoWA6YQv5Y7Q4EoYmTvximRsGCARGpCAJrKolj+A4rO8Q2rCX1JTVF6n67xh461V/XZGJCdvSvxhsVQ==; bm_sv=21F63800FF19A2D712A92A801B6E0D64~YAAQXA3eF9bCxx+GAQAAo9vYIRJ7WtzVfceF4gIt1+vRLnf90c70IgwS442dbiWbFjrrKhRPdK3HOj7XE3A6sVye4cKKtgumhLLnijNVVEyVNNqS3abqa8qlsKMgrhK+M+QeBxHdZV26saPb7JTO0RGQgb4ufL0RwePoqSNtlO+4kNS34+ICimCMnCycstfiVKEuCD3g253JR8tT+z+h7NEszPc9QtRmGgG84qX8ngCXp2++edTD/CevMnSvTxMQ~1; bm_sz=2C9A919667AFE729DFDA52949B3EAC7A~YAAQXA3eFwckxx+GAQAA59zSIRJwmml1wVoJkElYIAWi68tsjKgdOtlBr2hEJgYPzGpWRVCHRt/IMZSeLGKY//WvMcKJe7odkKqWoKbQprI3u2rK5Y9Frge281Wlfa57AdjCbpd9o0KJsVI/KNSvNLAhLtfaOchJsq4n0ZWpVgzNrvt5jmM6MjbvACBbJD6k6so3IhuRseh2mW7t8V6z8n4/fyoxJdSk/Nzjv1jlX2RRZIRfKP/jDFrGV9zq5PZ0hjaFqREmCGGj77kRRcSVf7INLHQ5sK/eJFmvwqcSqyIUdgE=~3294771~3359537',
                # fails with Mozilla, but works with Postman... wtf
                'User-Agent': 'PostmanRuntime/7.30.0',
            },
            timeout=10,
        )

    print('completed request')
    respjson = resp.json()
    with open('data/response.json', 'w+') as file:
        json.dump(respjson, file)

    return parse_resp(respjson)


def parse_resp(bodyjson):
    items = bodyjson.get('items')
    if not items or len(items) < 1:
        return []

    return items

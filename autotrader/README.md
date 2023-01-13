# AutoTrader

## Data Collection Method
Autotrader embeds JSON data in the returned HTML.  The most efficient way to gather data appears to be from this embedded JSON blob.

## Reference Data
Autotrader frontend calls out to a JSON API to get general reference data.  This data is saved in the [ref.json](/autotrader/ref.json "ref.json") file

## Inventory
Autotrader has essentially unlimited inventory so there is no point in an unfiltered inventory search

### Filtered Inventory
By model and location:
```bash
# Using path
curl 'https://www.autotrader.com/cars-for-sale/all-cars/ford/f150/dunwoody-ga-30338'
curl 'https://www.autotrader.com/cars-for-sale/all-cars/chevrolet/colorado/dunwoody-ga-30338'

# Using query params
curl 'https://www.autotrader.com/cars-for-sale/all-cars?zip=30338&makeCodeList=CHEV&modelCodeList=COLORADO'

# Heavily filtered
curl 'https://www.autotrader.com/cars-for-sale/awd-4wd/2020/toyota/tundra/atlanta-ga-30338?requestId=FULLSIZE_CREW%2BCOMPACT_CREW&extColorsSimple=BLUE&engineCodes=8CLDR&searchRadius=0&trimCodeList=TUNDRA%7C1794%20Edition&marketExtension=include&bodyStyleSubtypeCodes=FULLSIZE_CREW%2BCOMPACT_CREW&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=25'
curl 'https://www.autotrader.com/cars-for-sale/awd-4wd/2020/toyota/tundra/atlanta-ga-30338?requestId=1224&extColorsSimple=BLUE&maxMileage=100000&bodyStyleSubtypeCodes=FULLSIZE_CREW%2BCOMPACT_CREW&engineCodes=8CLDR&vhrTypes=NO_ACCIDENTS&searchRadius=0&trimCodeList=TUNDRA%7C1794%20Edition&marketExtension=include&featureCodes=1224&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=25'
curl 'https://www.autotrader.com/cars-for-sale/truck/ford/f150/atlanta-ga-30338?requestId=2281868035&maxMileage=100000&driveGroup=AWD4WD&bodyStyleSubtypeCodes=FULLSIZE_CREW%2BCOMPACT_CREW&vhrTypes=NO_ACCIDENTS&sellerTypes=p&searchRadius=200&startYear=2018&endYear=2020&marketExtension=include&maxPrice=40000&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=25'

# Playing with filtering
curl 'https://www.autotrader.com/cars-for-sale/all-cars/ford/f150/atlanta-ga-30338?searchRadius=200&sortBy=relevance&numRecords=100'
```

### Query Parameters
| Name | Value | Desc | 
|------|-------|------|
| Search Radius | searchRadius | Max Miles From Src Zip |
| Sort | sortBy | sorting order; `key``modifier` where key in [derivedprice, distance, mileage, year, relevance(no modifier)] and modifier in [ASC, DESC] |
| Number of Records | numRecords | Number of records to retrieve per request |
| Features | featureCodes | Comma-separated list of feature ids to filter on.  examples: {appleCarPlay: 1326, androidAuto: 1327, adaptiveCruiseControl: 1313, bluetooth: 1211, backupCamera: 1224, sunroof: 1132}|
| Max Price | maxPrice | maximum price |


### Individual Listing 
By listing ID:
```bash

curl 'https://www.autotrader.com/cars-for-sale/vehicledetails.xhtml?listingId=649061993'
```

### JSON Response Data Types
#### Inventory
Payload:
```json
{
    "initialState": {
        "inventory": {
            "637625797": {
                "accelerate": false,
                "bodyStyleCodes": [
                    "COUPE"
                ],
                "dealerConfig": {},
                "description": {
                    "hasMore": true,
                    "label": "2012 Ferrari 458 Italia Automatic Great condition Recently serviced New tire New brakes  Please call for an appointment  Legacy Motor Sales ..."
                },
                "features": [
                    "Abs - 4-Wheel",
                    "Air Filtration"
                ],
                "fuelType": "Gasoline",
                "hasSpecialOffer": false,
                "id": 637625797,
                "images": {
                    "hasVideoIcon": false,
                    "primary": 0,
                    "sources": [
                        {
                            "alt": "Used 2012 Ferrari 458 Italia Coupe",
                            "src": "//images.autotrader.com/hn/c/540e8f635963446893fb4eee26353bbf.jpg"
                        }
                    ]
                },
                "isHot": false,
                "listingTypes": [
                    "USED"
                ],
                "make": "Ferrari",
                "makeCode": "FER",
                "model": "458 Italia",
                "modelCode": "458ITALIA",
                "owner": 72838337,
                "ownerName": "Legacy Motor Sales",
                "paymentServices": {
                    "activeDealerTrack": true,
                    "coxAutoDrEnabled": false,
                    "dealerSettings": {
                        "taxesFeesEnabled": true,
                        "uiEnabled": false,
                        "leaseEnabled": false,
                        "priceBreakdownEnabled": false
                    },
                    "incentivesUrl": "?listingType=Used&vin=ZFF67NFA2C0182969&dealerId=412308&partnerId=AMK",
                    "paymentCalculationUrl": "salePrice=199999&dealerZip=30093&mileage=22988&vin=ZFF67NFA2C0182969&certifiedUsed=false&listingType=Used&fueltype=Gasoline&styleId=352146&trim=Coupe&bodyType=Coupe&transmission=Automatic&msrp=0&quotePreference=All&dealerId=412308&partnerId=AMK&enableLease=false&hasSpecialOffers=false&disableIncentives=true",
                    "paymentServiceActive": true,
                    "preferredLenderSpecified": false,
                    "digitalRetailingType": "default"
                },
                "phone": {
                    "linkText": "Get this seller's phone number",
                    "privateNumber": false,
                    "value": "4707353198",
                    "isVisible": true
                },
                "priceValidUntil": "2023-03-31",
                "pricingDetail": {
                    "incentive": 199999,
                    "isMismatch": true,
                    "noPriceLabel": "Contact Dealer For Price",
                    "salePrice": 199999
                },
                "priority": "Featured",
                "productTiles": [
                    {
                        "cmp": "ec_pa_lgo",
                        "cprd": "View_CERT",
                        "epn": "carfaxVHR",
                        "image": {
                            "src": "/resources/img/na/carfax/regular-own.svg",
                            "alt": "View the Free CARFAX Report",
                            "title": "View the Free CARFAX Report"
                        },
                        "link": {
                            "href": "https://www.carfax.com/VehicleHistory/ar20/f5S_Fnw5qMvXpjZ-VrZs-e1MWGLd3zQZaoSv0DQIzvhcnMzZ5cVsVzb6xOkXWHrjLCMgDm8hncjNghjTX2VwiChDXKsGQiCXIA8",
                            "label": "View the Free CARFAX Report",
                            "offsite": true,
                            "partner": true
                        },
                        "tileType": "CARFAX_APPENDED"
                    }
                ],
                "quickViewFeatures": [
                    "Alarm System",
                    "Auxiliary Audio Input"
                ],
                "specifications": {
                    "interiorColor": {
                        "label": "Interior Color",
                        "value": "Yellow"
                    },
                    "transmission": {
                        "label": "Transmission",
                        "value": "Automatic"
                    },
                    "color": {
                        "label": "Color",
                        "value": "Yellow"
                    },
                    "mpg": {
                        "label": "MPG",
                        "value": "12 City / 18 Highway"
                    },
                    "engine": {
                        "label": "Engine",
                        "value": "8-Cylinder"
                    },
                    "driveType": {
                        "label": "Drive Type",
                        "value": "2 wheel drive - rear"
                    },
                    "mileage": {
                        "label": "miles",
                        "value": "22,988"
                    }
                },
                "stockNumber": "2969",
                "style": [
                    "Coupe"
                ],
                "title": "Used 2012 Ferrari 458 Italia Coupe",
                "trim": "Coupe",
                "type": "Used",
                "vin": "ZFF67NFA2C0182969",
                "website": {
                    "href": "/cars-for-sale/vehicledetails.xhtml?listingId=637625797&zip=30338&referrer=%2Fcars-for-sale%2Fsearchresults.xhtml%3Fzip%3D30338%26city%3DAtlanta%26incremental%3Dall%26modelCodeList%3D458ITALIA%26makeCodeList%3DFER%26sortBy%3Drelevance%26location%3D%255Bobject%2BObject%255D%26maxPrice%3D200000%26state%3DGA%26firstRecord%3D0%26marketExtension%3Dinclude%26relevanceConfig%3Drelevance-v2%26searchRadius%3D100%26isNewSearch%3Dtrue&numRecords=25&maxPrice=200000&firstRecord=0&modelCodeList=458ITALIA&makeCodeList=FER&searchRadius=100&makeCode1=FER&modelCode1=458ITALIA"
                },
                "year": 2012,
                "zip": "30093",
                "vdpBaseUrl": "/cars-for-sale/vehicledetails.xhtml?listingId=637625797&allListingType=all-cars&maxPrice=200000&makeCodeList=FER&modelCodeList=458ITALIA&city=Atlanta&state=GA&zip=30338&requestId=564749857&searchRadius=100&marketExtension=include&isNewSearch=false&showAccelerateBanner=false&sortBy=relevance&numRecords=25&referrer=%2Fcars-for-sale%2Fall-cars%2Fcars-under-200000%2Fferrari%2F458-italia%2Fatlanta-ga-30338%3FrequestId%3D564749857%26searchRadius%3D100%26marketExtension%3Dinclude%26isNewSearch%3Dtrue%26showAccelerateBanner%3Dfalse%26sortBy%3Drelevance%26numRecords%3D25"
            }
        }
    }
}
```
Fields of Interest
| Field | Type | Description |
|-------|------|-------------|
| accelerate | Boolean | Indicates if the listing is in the search results (false) or promotional (true) |
| features | String Array | List of vehicle features

#### Request Params (General)
Request params indicate the features of the search query
```json
{
    "initialState": {
        "requestParams": {
            "requestId": "564749857",
            "userAgent": "PostmanRuntime/7.30.0",
            "channel": "ATC",
            "city": "Atlanta",
            "firstRecord": 0,
            "listingTiers": [
                "Featured"
            ],
            "location": "[object Object]",
            "makeCodeList": "FER",
            "marketExtension": "include",
            "maxPrice": 200000,
            "modelCodeList": "458ITALIA",
            "numRecords": 25,
            "relevanceConfig": "relevance-v2",
            "searchRadius": 100,
            "showAccelerateBanner": false,
            "sortBy": "relevance",
            "state": "GA",
            "stats": "year,derivedprice",
            "zip": "30338",
            "newSearch": true
        },
    }
}
```

## Jargon
* vhr -> Vehicle History Record?

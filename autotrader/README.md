# AutoTrader

## Data Collection Method
Autotrader embeds JSON data in the returned HTML.  The most efficient way to gather data appears to be from this embedded JSON blob.

### Reference Data
Autotrader frontend calls out to a JSON API to get general reference data.  This data is saved in the [ref.json](/autotrader/ref.json "ref.json") file

### Inventory
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

#### Query Parameters
| Name | Value | Desc | 
|------|-------|------|
| Search Radius | searchRadius | Max Miles From Src Zip |
| Sort | sortBy | sorting order; <key><modifier> where modifier in [ASC, DESC] and key in [derivedprice, distance, mileage, year]

### Individual Listing 
By listing ID:
```bash

curl 'https://www.autotrader.com/cars-for-sale/vehicledetails.xhtml?listingId=649061993'
```

### Parsing JSON
Path to inventory (using jq):
```bash
jq '.initialState.inventory."<listing_id>"' <filename>
```

## Jargon
* vhr -> Vehicle History Record?

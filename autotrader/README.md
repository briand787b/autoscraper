# AutoTrader

## Data Collection Method
Autotrader embeds JSON data in the returned HTML.  The most efficient way to gather data appears to be from this embedded JSON blob.

### Reference Data
Autotrader frontend calls out to a JSON API to get general reference data.  This data is saved in the [link](/autotrader/ref.json ref.json) file

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
```

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
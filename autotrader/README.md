# AutoTrader

## Data Collection Method
Autotrader embeds JSON data in the returned HTML.  The most efficient way to gather data appears to be from this embedded JSON blob.

### Inventory
Autotrader has essentially unlimited inventory so there is no point in an unfiltered inventory search

### Filtered Inventory
By model and location:
(Using path)
https://www.autotrader.com/cars-for-sale/all-cars/ford/f150/dunwoody-ga-30338
https://www.autotrader.com/cars-for-sale/all-cars/chevrolet/colorado/dunwoody-ga-30338
(Using query params)
https://www.autotrader.com/cars-for-sale/all-cars?zip=30338&makeCodeList=CHEV&modelCodeList=COLORADO

### Individual Listing 
By listing ID:
https://www.autotrader.com/cars-for-sale/vehicledetails.xhtml?listingId=649061993

### Parsing JSON
Path to inventory (using jq):
jq '.initialState.inventory."<listing_id>"' <filename>
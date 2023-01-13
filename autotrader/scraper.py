#!/usr/bin/env python3

from urllib.request import urlopen

BASE_URL='https://www.autotrader.com/cars-for-sale'
ALL_BASE_PATH='/all-cars'
LISTING_BASE_PATH='/vehicledetails.xhtml'

SEARCH_PATHS=['setattr']

all_listing='https://www.autotrader.com/cars-for-sale/all-cars/ford/f150/clarkesville-ga-30523?0=vehicledetails.xhtml&searchRadius=200&marketExtension=include&bodyStyleSubtypeCodes=FULLSIZE_CREW%2BCOMPACT_CREW&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=25&requestId=FULLSIZE_CREW%2BCOMPACT_CREW'
one_listing='https://www.autotrader.com/cars-for-sale/vehicledetails.xhtml?listingId=649061993&0=vehicledetails.xhtml&allListingType=all-cars&makeCodeList=FORD&modelCodeList=F150PICKUP&city=Clarkesville&state=GA&zip=30523&searchRadius=200&marketExtension=include&bodyStyleSubtypeCodes=FULLSIZE_CREW%2BCOMPACT_CREW&isNewSearch=false&showAccelerateBanner=false&sortBy=relevance&numRecords=25&requestId=FULLSIZE_CREW%2BCOMPACT_CREW&referrer=%2Fcars-for-sale%2Fall-cars%2Fford%2Ff150%2Fclarkesville-ga-30523%3F0%3Dvehicledetails.xhtml%26searchRadius%3D200%26marketExtension%3Dinclude%26bodyStyleSubtypeCodes%3DFULLSIZE_CREW%252BCOMPACT_CREW%26isNewSearch%3Dfalse%26showAccelerateBanner%3Dfalse%26sortBy%3Drelevance%26numRecords%3D25%26requestId%3DFULLSIZE_CREW%252BCOMPACT_CREW&clickType=listing'

def main():
    scrape()

def scrape():
    """
    scrape is the entrypoint for libraries calling into this module.    
    """
    print('library entrypoint')

def vehicle_listings():
    urlopen()

if __name__ == '__main__':
    main()
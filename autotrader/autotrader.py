#!/usr/bin/env python3

import database
import scrape
import time
from sys import argv


### TODO:
# 1. add checkpoints

def main(db_pw: str):
    eng = database.engine(db_pw)
    for region in scrape.all_regions():
        for target in scrape.all_targets():
            try:
                inv_list = scrape.scrape_model(target, region)
                database.save_listings(eng, inv_list)
                time.sleep(10)
            except Exception as e:
                print(f'failed to scrape target ({target}): {e}')
                raise # I want to be alerted of any failures while testing
    

if __name__ == '__main__':
    if len(argv) != 2:
        print('please provide database password to autoscraper')
        exit(1)
    
    main(argv[1])


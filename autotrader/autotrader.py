#!/usr/bin/env python3

import db
import scrape
import time


### TODO:
# 1. add checkpoints

def main():
    # test_scrape_url()
    # test_scrape_doc()
    # exit(0)

    eng = db.engine()
    for region in scrape.all_regions():
        for target in scrape.all_targets():
            try:
                inv_list = scrape.scrape_model(target, region)
                db.save_listings(eng, inv_list)
                time.sleep(10)
            except Exception as e:
                print(f'failed to scrape target ({target}): {e}')
                raise # I want to be alerted of any failures while testing
    


def test_scrape_doc():
    eng = db.engine()
    with open('examples/resp.html', 'r') as file:
        doc = file.read()

    inv_list, _ = scrape.scrape_doc(doc)
    print(f'num items: {len(inv_list)}')
    db.save_listings(eng, inv_list)


def test_scrape_url():
    eng = db.engine()
    print('about to scrape against live site')
    for region in scrape.all_regions():
        inv_list = scrape.titan(region)
        db.save_listings(eng, inv_list)


if __name__ == '__main__':
    main()

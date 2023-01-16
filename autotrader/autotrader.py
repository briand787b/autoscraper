#!/usr/bin/env python3

import scrape
import db
from sqlalchemy.engine import Engine


### TODO:
# 1. add checkpoints

def main():
    # test_scrape_url()
    # test_scrape_doc()

    eng = db.engine()
    for target in scrape.all_targets():
        try:
            inv_list = scrape.scrape_model(target)
            db.save_listings(eng, inv_list)
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
    print('about to scrape 458 spyder records')
    inv_list = scrape.scrape_458_spyder()
    db.save_listings(eng, inv_list)


if __name__ == '__main__':
    main()

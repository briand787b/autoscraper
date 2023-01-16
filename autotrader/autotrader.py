#!/usr/bin/env python3

import scrape
import db
from sqlalchemy.engine import Engine


def main():
    eng = db.engine()
    # test_scrape_url(eng)
    # test_scrape_doc(eng)
    
    inv_list = scrape.f150()
    db.save_listings(eng, inv_list)



def test_scrape_doc(eng: Engine):
    with open('examples/resp.html', 'r') as file:
        doc = file.read()

    inv_list, _ = scrape.scrape_doc(doc)
    print(f'num items: {len(inv_list)}')
    db.save_listings(eng, inv_list)


def test_scrape_url(eng: Engine):
    print('about to scrape 458 spyder records')
    inv_list = scrape.scrape_458_spyder()
    db.save_listings(eng, inv_list)


if __name__ == '__main__':
    main()

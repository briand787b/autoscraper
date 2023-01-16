#!/usr/bin/env python3

import scrape
import db


def main():
    test_scrape_url()
    #test_scrape_doc()


def test_scrape_doc():
    eng = db.engine()

    with open('examples/resp.html', 'r') as file:
        doc = file.read()

    inv_list, _ = scrape.scrape_doc(doc)
    print(f'num items: {len(inv_list)}')
    db.save_listings(eng, inv_list)


def test_scrape_url():
    print('about to scrape 458 spyder records')
    eng = db.engine()
    inv_list = scrape.scrape_458_spyder()
    db.save_listings(eng, inv_list)


if __name__ == '__main__':
    main()

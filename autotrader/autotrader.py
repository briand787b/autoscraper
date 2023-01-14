#!/usr/bin/env python3

import scrape


def main():
    test_scrape_url()


def test_scrape_doc():
    with open('examples/resp.html', 'r') as file:
        doc = file.read()

    scrape.scrape_doc(doc)


def test_scrape_url():
    print('about to scrape 458 spyder records')
    scrape.scrape_458_spyder()


if __name__ == '__main__':
    main()

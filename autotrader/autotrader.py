#!/usr/bin/env python3

import scrape
import parse

def main():
    print('nothing to do yet...')
    doc = scrape.test_scrape_url()
    parse.parse(doc)
    
if __name__ == '__main__':
    main()
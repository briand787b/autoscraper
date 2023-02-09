#!/usr/bin/env python3

import click
import database
import scrape as sc


@click.group()
def cli():
    pass


@click.command()
@click.option('--password', help='database password')
@click.option('--host', default='localhost', help='database host [default: localhost]')
@click.option('--port', default=5432, help='database port [default: 5432]')
@click.option('--region', default='atlanta', help='region to scrape, "all" to scrape all locations [default: atlanta]')
@click.option('--model', help='vehicle model to scrape, defaults to all')
def scrape(password, host, port, region, model):
    if not password:
        raise Exception('missing mandatory password')

    eng = database.engine(password, host=host, port=port)
    regions = scraper_regions(region)
    models = scraper_models(model)

    print(f'scraping {regions} for {models}')
    for m in models:
        for r in regions:
            listings = sc.scrape_model(m, r)
            database.save_listings(eng, listings)


@click.command()
@click.option('--password', help='database password')
@click.option('--host', default='localhost', help='database host')
@click.option('--port', default=5432, help='database port')
@click.option('--output_path', help='where to write csv file to')
def write_listing_report_csv(password, host, port, output_path):
    eng = database.engine(password, host=host, port=port)
    listings = database.select_listings(eng)
    database.export_listings(listings, output_path)


cli.add_command(scrape)
cli.add_command(write_listing_report_csv)

def scraper_models(model: str | None):
    if model is None:
        return sc.all_models()
    
    return (model,)
        

def scraper_regions(friendly_name: str):
    friendly_name = friendly_name.lower()
    
    if friendly_name == 'all':
        return sc.all_regions()
    if friendly_name in ('atlanta', 'georgia', 'ga'):
        return (sc.REGION_ATLANTA,)
    if friendly_name in ('brookfield', 'connecticut', 'ct'):
        return (sc.REGION_BROOKFIELD,)

    return friendly_name


if __name__ == '__main__':
    cli()


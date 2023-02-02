#!/usr/bin/env python3

import click
import database
import scrape as sc


# TODO:
# take args to make non-local database conn work


@click.group()
def cli():
    pass


@click.command()
@click.option('--password', help='database password')
@click.option('--host', default='localhost', help='database host')
@click.option('--port', default=5432, help='database port')
@click.option('--region', default='atlanta-ga-30338', help='region to scrape, "all" to scrape all locations')
@click.option('--model', help='vehicle model to scrape, defaults to all')
def scrape(password, host, port, region, model):
    if not password:
        raise Exception('missing mandatory password')

    eng = database.engine(password, host=host, port=port)
    if model:
        models = [model]
    else:
        models = sc.all_models()

    for m in models:
        if region == 'all':
            regions = sc.all_regions()
        else:
            regions = [region]

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

if __name__ == '__main__':
    cli()

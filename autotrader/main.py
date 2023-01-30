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
@click.option('--region',  help='region to scrape')
def scrape(password, region):
    eng = database.engine(password)
    for model in sc.all_models():
        listings = sc.scrape_model(model, region)
        database.save_listings(eng, listings)


@click.command()
@click.option('--password', help='database password')
@click.option('--output_path', help='where to write csv file to')
def write_listing_report_csv(password, output_path):
    eng = database.engine(password)
    listings = database.select_listings(eng)
    database.export_listings(listings, output_path)


cli.add_command(scrape)
cli.add_command(write_listing_report_csv)

if __name__ == '__main__':
    cli()

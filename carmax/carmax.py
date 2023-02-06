#!/usr/bin/env python3

import click
import database
import scrape as sc


@click.group()
def cli():
    pass


@click.command()
@click.option('--dbpassword', help='database password')
@click.option('--dbhost', default='localhost', help='database host')
@click.option('--dbport', default=5432, help='database port')
def scrape(dbpassword, dbhost, dbport):
    if not dbpassword:
        raise Exception('missing mandatory password')

    eng = database.engine(dbpassword, host=dbhost, port=dbport)
    for model_listings in sc.api(sc.all_queries()):
        print('scraped all listings for a model')
        for listings in model_listings:
            print('saving listings for one page')
            database.save_listings(eng, listings)


# @click.command()
# @click.option('--password', help='database password')
# @click.option('--host', default='localhost', help='database host')
# @click.option('--port', default=5432, help='database port')
# @click.option('--output_path', help='where to write csv file to')
# def write_listing_report_csv(password, host, port, output_path):
#     eng = database.engine(password, host=host, port=port)
#     listings = database.select_listings(eng)
#     database.export_listings(listings, output_path)

cli.add_command(scrape)
# cli.add_command(write_listing_report_csv)

if __name__ == '__main__':
    cli()

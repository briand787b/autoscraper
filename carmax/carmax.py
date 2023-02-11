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
def scrape(password, host, port):
    '''scrapes the carmax site for listings'''
    if not password:
        raise Exception('missing mandatory password')

    scrape_core(pw=password, host=host, port=port)


def scrape_core(pw, host, port):
    '''core for scrape cmd'''
    eng = database.engine(pw, host=host, port=port)
    for model_listings in sc.api(sc.all_queries()):
        for listings in model_listings:
            print('saving listings for one page')
            database.save_listings(eng, listings)

        print('scraped all listings for a model')


cli.add_command(scrape)

if __name__ == '__main__':
    cli()

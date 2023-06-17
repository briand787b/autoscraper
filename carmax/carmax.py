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
@click.option('--debug', default=False, help='run with verbose logging')
def scrape(password, host, port, debug):
    '''scrapes the carmax site for listings'''
    if not password:
        raise Exception('missing mandatory password')

    scrape_core(pw=password, host=host, port=port, debug=debug)


def scrape_core(pw, host, port, debug):
    '''core for scrape cmd'''
    eng = database.engine(pw, host=host, port=port)
    for model_listings in sc.api(sc.all_queries(), dbug=debug):
        for listings in model_listings:
            print('saving listings for one page')
            database.save_listings(eng, listings)

        print('scraped all listings for a model')


cli.add_command(scrape)

if __name__ == '__main__':
    cli()

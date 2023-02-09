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
def scrape_cmd(dbpassword, dbhost, dbport):
    '''command shell'''
    if not dbpassword:
        raise Exception('missing mandatory password')

    scrape(pw=dbpassword, host=dbhost, port=dbport)


def scrape(pw, host, port):
    '''command core'''
    eng = database.engine(pw, host=host, port=port)
    for model_listings in sc.api(sc.all_queries()):
        print('scraped all listings for a model')
        for listings in model_listings:
            print('saving listings for one page')
            database.save_listings(eng, listings)


cli.add_command(scrape_cmd)

if __name__ == '__main__':
    cli()

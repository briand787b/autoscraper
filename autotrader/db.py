#!/usr/bin/env python3

import csv
import sqlalchemy as db
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError


# TODO:


def engine():
    return db.create_engine("sqlite:///autotrader.db", echo=True)


def create_csv(eng: Engine):
    with eng.connect() as conn:
        results = conn.execute('''
            SELECT
                id,
                autotrader_id,
                color,
                condition,
                drive_type,
                engine,
                make,
                mileage,
                model,
                mpg_city,
                mpg_hwy,
                owner,
                price,
                trim,
                truck_bed,
                truck_cab,
                vin,
                year,
                zip,
                scrape_date
        ''').all()

    with open('output/listings.csv', 'w') as file:
        w = csv.writer(file)
        w.writerow([
                'id',
                'autotrader_id',
                'color',
                'condition',
                'drive_type',
                'engine',
                'make',
                'mileage',
                'model',
                'mpg_city',
                'mpg_hwy',
                'owner',
                'price',
                'trim',
                'truck_bed',
                'truck_cab',
                'vin',
                'year',
                'zip',
                'scrape_date',
        ])
        w.writerows(results)
            

def save_listings(eng: Engine, listings: list):
    with eng.connect() as conn:
        conn.execute('''
            INSERT INTO listings
            (
                autotrader_id,
                color,
                condition,
                drive_type,
                engine,
                make,
                mileage,
                model,
                mpg_city,
                mpg_hwy,
                owner,
                price,
                trim,
                truck_bed,
                truck_cab,
                vin,
                year,
                zip
            )
            VALUES
            (
                :autotrader_id,
                :color,
                :condition,
                :drive_type,
                :engine,
                :make,
                :mileage,
                :model,
                :mpg_city,
                :mpg_hwy,
                :owner,
                :price,
                :trim,
                :truck_bed,
                :truck_cab,
                :vin,
                :year,
                :zip
            );
            ''', listings)

    save_features(eng, listings)
    save_packages(eng, listings)


def save_features(eng: Engine, listings: list):
    for listing in listings:
        vin = listing['vin']
        ftrs = listing.get('features', [])
        if type(ftrs) != list or len(ftrs) < 1:
            continue

        try:
            with eng.connect() as conn:
                conn.execute('''
                    INSERT INTO vehicle_features
                    (
                        vin,
                        feature
                    ) 
                    VALUES
                    (
                        :vin,
                        :ftr
                    );
                ''', [{'vin': vin, 'ftr': f} for f in ftrs])
        except IntegrityError:
            continue


def save_packages(eng: Engine, listings: list):
    for listing in listings:
        vin = listing['vin']
        pkgs = listing.get('packages', [])
        if type(pkgs) != list or len(pkgs) < 1:
            continue

        try:
            with eng.connect() as conn:
                conn.execute('''
                    INSERT INTO vehicle_packages
                    (
                        vin,
                        package
                    ) 
                    VALUES
                    (
                        :vin,
                        :pkg
                    );
                ''', [{'vin': vin, 'pkg': p} for p in pkgs])
        except IntegrityError:
            continue


def create_tables(eng: Engine):
    with eng.connect() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS listings (
                id            SERIAL PRIMARY KEY,
                autotrader_id VARCHAR(9),
                color         VARCHAR(55),
                condition     VARCHAR(16),
                drive_type    VARCHAR(55),
                engine        VARCHAR(55),
                make          VARCHAR(55),
                mileage       INTEGER,
                model         VARCHAR(55),
                mpg_city      INTEGER,
                mpg_hwy       INTEGER,
                owner         VARCHAR(255),
                price         INTEGER,
                trim          VARCHAR(55),
                truck_bed     VARCHAR(55),
                truck_cab     VARCHAR(55),
                vin           VARCHAR(17),
                year          INTEGER,
                zip           VARCHAR(5),
                scrape_date   DATE NOT NULL DEFAULT CURRENT_DATE
            )
        ''')

        conn.execute('''
            CREATE TABLE IF NOT EXISTS vehicle_features (
                vin          VARCHAR(17) NOT NULL,
                feature      VARCHAR(105) NOT NULL,
                scrape_date  DATE NOT NULL DEFAULT CURRENT_DATE,
                PRIMARY KEY (vin, feature)
            )
        ''')

        conn.execute('''
            CREATE TABLE IF NOT EXISTS vehicle_packages (
                vin          VARCHAR(17) NOT NULL,
                package      VARCHAR(105) NOT NULL,
                scrape_date  DATE NOT NULL DEFAULT CURRENT_DATE,
                PRIMARY KEY (vin, package)
            )
        ''')


if __name__ == '__main__':
    eng = engine()
    with eng.connect() as conn:
        conn.execute('DROP TABLE IF EXISTS listings')
        conn.execute('DROP TABLE IF EXISTS vehicle_features')
        conn.execute('DROP TABLE IF EXISTS vehicle_packages')

    create_tables(eng)
    save_listings(eng, [
        {
            "autotrader_id": "669485363",
            "color": "blue",
            "condition": "used",
            "drive_type": "2 wheel drive - rear",
            "engine": "8-cylinder turbo",
            "features": None,
            "make": 'ferrari',
            "mileage": 352,
            "model": 'F8 Tributo',
            "mpg_city": 15,
            "mpg_hwy": 19,
            "owner": 'Used Car Lot',
            "packages": [
                '302A Luxury Package',
                'Trailer Tow Pkg',
            ],
            "price": 449900,
            "trim": None,
            "truck_bed": None,
            "truck_cab": None,
            "vin": "ZFF92LLA7N0279141",
            "year": 2022,
            "zip": "75244"
        },
        {
            "autotrader_id": "669485363",
            "color": "blue",
            "condition": "used",
            "drive_type": "2 wheel drive - rear",
            "engine": "8-cylinder turbo",
            "features": None,
            "make": 'ferrari',
            "mileage": 352,
            "model": 'F8 Tributo',
            "mpg_city": 15,
            "mpg_hwy": 19,
            "owner": 'Used Car Lot',
            "packages": [
                '302A Luxury Package',
                'Trailer Tow Pkg',
            ],
            "price": 449900,
            "trim": None,
            "truck_bed": None,
            "truck_cab": None,
            "vin": "ZFF92LLA7N0279141",
            "year": 2022,
            "zip": "75244"
        },
        {
            "autotrader_id": "669485364",
            "color": "blue",
            "condition": "new",
            "drive_type": "2 wheel drive - rear",
            "engine": "8-cylinder",
            "features": [
                'Apple CarPlay',
                'Android Auto',
            ],
            "make": 'ferrari',
            "mileage": 352,
            "model": '458_italia',
            "mpg_city": 15,
            "mpg_hwy": 19,
            "owner": 'Luxury Super Cars Ltd',
            "packages": [],
            "price": 349900,
            "trim": None,
            "truck_bed": None,
            "truck_cab": None,
            "vin": "ZFF92LLA7N0279142",
            "year": 2022,
            "zip": "75244"
        },
        {
            "autotrader_id": "669485364",
            "color": "blue",
            "condition": "new",
            "drive_type": "2 wheel drive - rear",
            "engine": "8-cylinder",
            "features": [
                'Apple CarPlay',
                'Android Auto',
            ],
            "make": 'ferrari',
            "mileage": 352,
            "model": '458_italia',
            "mpg_city": 15,
            "mpg_hwy": 19,
            "owner": 'Luxury Super Cars Ltd',
            "packages": None,
            "price": 249900,
            "trim": None,
            "truck_bed": None,
            "truck_cab": None,
            "vin": "ZFF92LLA7N0279142",
            "year": 2022,
            "zip": "75244"
        }
    ])
    create_csv(eng)

    print('done!')

#!/usr/bin/env python3

import sqlalchemy as db
from sqlalchemy.engine import Engine


def engine():
    return db.create_engine("sqlite:///autotrader.db", echo=True)


def save_listings(eng: Engine, listings: list):
    print(f'first item to save: {listings[0]}')
    with eng.connect() as conn:
        conn.execute('''
            INSERT INTO listings
            (
                autotrader_id,
                carplay,
                color,
                drive_type,
                engine,
                make,
                mileage,
                model,
                mpg_city,
                mpg_hwy,
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
                :carplay,
                :color,
                :drive_type,
                :engine,
                :make,
                :mileage,
                :model,
                :mpg_city,
                :mpg_hwy,
                :price,
                :trim,
                :truck_bed,
                :truck_cab,
                :vin,
                :year,
                :zip
            )
            ''', listings)


def create_table(eng: Engine):
    with eng.connect() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS listings (
                id INTEGER NOT NULL PRIMARY KEY,
                autotrader_id VARCHAR(55),
                carplay BOOLEAN,
                color VARCHAR(55),
                drive_type VARCHAR(16),
                engine VARCHAR(24),
                make VARCHAR(55),
                mileage INTEGER,
                model VARCHAR(55),
                mpg_city INTEGER,
                mpg_hwy INTEGER,
                price INTEGER,
                trim VARCHAR(55),
                truck_bed VARCHAR(55),
                truck_cab VARCHAR(55),
                vin VARCHAR(17),
                year INTEGER,
                zip VARCHAR(5),
                created_at DATETIME NOT NULL DEFAULT current_timestamp, 
                updated_at DATETIME NOT NULL DEFAULT current_timestamp
            )
        ''')


if __name__ == '__main__':
    eng = engine()
    create_table(eng)
    save_listings(eng, [
        {
            "autotrader_id": "669485363",
            "carplay": False,
            "color": "blue",
            "drive_type": "2 wheel drive - rear",
            "engine": "8-cylinder turbo",
            "features": None,
            "make": 'ferrari',
            "mileage": 352,
            "model": 'F8 Tributo',
            "mpg_city": 15,
            "mpg_hwy": 19,
            "packages": [
                '302A Luxury Package',
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
            "carplay": True,
            "color": "blue",
            "drive_type": "2 wheel drive - rear",
            "engine": "8-cylinder",
            "features": [
                'Apple CarPlay',
            ],
            "make": 'ferrari',
            "mileage": 352,
            "model": '458_italia',
            "mpg_city": 15,
            "mpg_hwy": 19,
            "packages": [],
            "price": 249900,
            "trim": None,
            "truck_bed": None,
            "truck_cab": None,
            "vin": "ZFF92LLA7N0279142",
            "year": 2022,
            "zip": "75244"
        }
    ])

import csv
import sqlalchemy
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError


def engine(pw: str, addr='localhost', usr='autotrader'):
    return sqlalchemy.create_engine(
        f'postgresql://{usr}:{pw}@{addr}/autotrader',
        echo=True,
        future=True,
    )


def export_listings(listings=[], path='output/listings.csv'):
    with open(path, 'w') as file:
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
        w.writerows(listings)


def select_listings(eng: Engine):
    with eng.connect() as conn:
        results = conn.execute(sqlalchemy.text('''
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
            FROM listings;
        '''))

    return results


def save_listings(eng: Engine, listings: list):
    with eng.connect() as conn:
        with conn.begin():
            conn.execute(sqlalchemy.text('''
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
                '''), listings)

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
                with conn.begin():
                    conn.execute(sqlalchemy.text('''
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
                    '''), [{'vin': vin, 'ftr': f} for f in ftrs])
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
                with conn.begin():
                    conn.execute(sqlalchemy.text('''
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
                    '''), [{'vin': vin, 'pkg': p} for p in pkgs])
        except IntegrityError:
            continue


def create_tables(eng: Engine):
    with eng.connect() as conn:
        with conn.begin():
            conn.execute(sqlalchemy.text('''
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
                );
            '''))

        with conn.begin():
            conn.execute(sqlalchemy.text('''
                CREATE TABLE IF NOT EXISTS vehicle_features (
                    vin          VARCHAR(17) NOT NULL,
                    feature      VARCHAR(105) NOT NULL,
                    scrape_date  DATE NOT NULL DEFAULT CURRENT_DATE,
                    PRIMARY KEY (vin, feature)
                )
            '''))

        with conn.begin():
            conn.execute(sqlalchemy.text('''
                CREATE TABLE IF NOT EXISTS vehicle_packages (
                    vin          VARCHAR(17) NOT NULL,
                    package      VARCHAR(105) NOT NULL,
                    scrape_date  DATE NOT NULL DEFAULT CURRENT_DATE,
                    PRIMARY KEY (vin, package)
                )
            '''))

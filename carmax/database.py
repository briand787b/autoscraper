import csv
import sqlalchemy
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError

def engine(pw: str, host='localhost', port=5432, usr='carmax'):
    return sqlalchemy.create_engine(
        f'postgresql://{usr}:{pw}@{host}:{port}/carmax',
        echo=True,
        future=True,
    )


def export_listings(listings=[], path='output/listings.csv'):
    with open(path, 'w') as file:
        w = csv.writer(file)
        w.writerow([
            'id',
            'body',
            'carmax_id',
            'city',
            'color',
            'drive_type',
            'engine_cyl',
            'engine_size',
            'engine_type',
            'make',
            'model',
            'mpg_city',
            'mpg_hwy',
            'msrp',
            'price',
            'state',
            'store_id',
            'trim',
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
                body,
                carmax_id,
                city,
                color,
                drive_type,
                engine_cyl,
                engine_size,
                engine_type,
                make,
                model,
                mpg_city,
                mpg_hwy,
                msrp,
                price,
                state,
                store_id,
                trim,
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
                    body,
                    carmax_id,
                    city,
                    color,
                    drive_type,
                    engine_cyl,
                    engine_size,
                    engine_type,
                    make,
                    model,
                    mpg_city,
                    mpg_hwy,
                    msrp,
                    price,
                    state,
                    store_id,
                    trim,
                    vin,
                    year,
                    zip
                )
                VALUES
                (
                    :body,
                    :carmax_id,
                    :city,
                    :color,
                    :drive_type,
                    :engine_cyl,
                    :engine_size,
                    :engine_type,
                    :make,
                    :model,
                    :mpg_city,
                    :mpg_hwy,
                    :msrp,
                    :price,
                    :state,
                    :store_id,
                    :trim,
                    :vin,
                    :year,
                    :zip
                );
                '''), listings)

    save_features(eng, listings)
    save_packages(eng, listings)
    save_highlights(eng, listings)
    save_prior_uses(eng, listings)


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

def save_highlights(eng: Engine, listings: list):
    for listing in listings:
        vin = listing['vin']
        hs = listing.get('highlights', [])
        if type(hs) != list or len(hs) < 1:
            continue

        try:
            with eng.connect() as conn:
                with conn.begin():
                    conn.execute(sqlalchemy.text('''
                        INSERT INTO vehicle_highlights
                        (
                            vin,
                            highlight
                        ) 
                        VALUES
                        (
                            :vin,
                            :hl
                        );
                    '''), [{'vin': vin, 'hl': h} for h in hs])
        except IntegrityError:
            continue

def save_prior_uses(eng: Engine, listings: list):
    for listing in listings:
        vin = listing['vin']
        pus = listing.get('prior_uses', [])
        if type(pus) != list or len(pus) < 1:
            continue

        try:
            with eng.connect() as conn:
                with conn.begin():
                    conn.execute(sqlalchemy.text('''
                        INSERT INTO vehicle_prior_uses
                        (
                            vin,
                            code
                        ) 
                        VALUES
                        (
                            :vin,
                            :code
                        );
                    '''), [{'vin': vin, 'code': puc} for puc in pus])
        except IntegrityError:
            continue


def create_tables(eng: Engine):
    with eng.connect() as conn:
        with conn.begin():
            conn.execute(sqlalchemy.text('''
                CREATE TABLE IF NOT EXISTS listings (
                    id              SERIAL PRIMARY KEY,
                    body            VARCHAR(24),
                    carmax_id       INTEGER,
                    city            VARCHAR(55),
                    color           VARCHAR(16),
                    drive_type      VARCHAR(8),
                    engine_cyl      SMALLINT,
                    engine_size     VARCHAR(8),
                    engine_type     VARCHAR(8),
                    make            VARCHAR(55),
                    model           VARCHAR(55),
                    mpg_city        SMALLINT,
                    mpg_hwy         SMALLINT,
                    msrp            INTEGER,
                    price           INTEGER,
                    state           VARCHAR(2),
                    store_id        SMALLINT,
                    trim            VARCHAR(16),
                    vin             VARCHAR(17),
                    year            SMALLINT,
                    zip             VARCHAR(5),
                    scrape_date   DATE NOT NULL DEFAULT CURRENT_DATE
                );
            '''))

        with conn.begin():
            conn.execute(sqlalchemy.text('''
                CREATE TABLE IF NOT EXISTS vehicle_features (
                    vin          VARCHAR(17) NOT NULL,
                    feature      VARCHAR(255) NOT NULL,
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

        with conn.begin():
            conn.execute(sqlalchemy.text('''
                CREATE TABLE IF NOT EXISTS vehicle_highlights (
                    vin          VARCHAR(17) NOT NULL,
                    highlight    VARCHAR(105) NOT NULL,
                    scrape_date  DATE NOT NULL DEFAULT CURRENT_DATE,
                    PRIMARY KEY (vin, highlight)
                )
            '''))

        with conn.begin():
            conn.execute(sqlalchemy.text('''
                CREATE TABLE IF NOT EXISTS vehicle_prior_uses (
                    vin             VARCHAR(17) NOT NULL,
                    code            SMALLINT NOT NULL,
                    scrape_date     DATE NOT NULL DEFAULT CURRENT_DATE,
                    PRIMARY KEY (vin, code)
                )
            '''))

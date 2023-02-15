import csv
import sqlalchemy
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError


def engine(pw: str, host='localhost', port=5432, usr='carvana', echo=False):
    return sqlalchemy.create_engine(
        f'postgresql://{usr}:{pw}@{host}:{port}/carvana',
        echo=echo,
        future=True,
    )


def export_listings(listings=[], path='output/listings.csv'):
    with open(path, 'w') as file:
        w = csv.writer(file)
        w.writerow([
            'id',
            'body',
            'carvana_id',
            'city',
            'color',
            'drive_type',
            'engine',
            'kbb_value',
            'make',
            'mfg_basic_warranty_miles',
            'mfg_basic_warranty_months',
            'mfg_dt_warranty_miles',
            'mfg_dt_warranty_months',
            'mileage',
            'model',
            'num_keys',
            'price',
            'rem_warranty_miles',
            'rem_warranty_months',
            'rem_dt_warranty_miles',
            'rem_dt_warranty_months',
            'seating',
            'state',
            'transmission',
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
                carvana_id,
                city,
                color,
                drive_type,
                engine,
                kbb_value,
                make,
                mfg_basic_warranty_miles,
                mfg_basic_warranty_months,
                mfg_dt_warranty_miles,
                mfg_dt_warranty_months,
                mileage,
                model,
                num_keys,
                price,
                rem_warranty_miles,
                rem_warranty_months,
                rem_dt_warranty_miles,
                rem_dt_warranty_months,
                seating,
                state,
                transmission,
                trim,
                vin,
                year,
                zip,
                scrape_date
            FROM listings;
        '''))

    return results


def save_listings(eng: Engine, listings: list):
    if len(listings) < 1:
        print('no listings to save')
        return

    with eng.connect() as conn:
        with conn.begin():
            conn.execute(sqlalchemy.text('''
                INSERT INTO listings
                (
                    body,
                    carvana_id,
                    city,
                    color,
                    drive_type,
                    engine,
                    kbb_value,
                    make,
                    mfg_basic_warranty_miles,
                    mfg_basic_warranty_months,
                    mfg_dt_warranty_miles,
                    mfg_dt_warranty_months,
                    mileage,
                    model,
                    num_keys,
                    price,
                    rem_warranty_miles,
                    rem_warranty_months,
                    rem_dt_warranty_miles,
                    rem_dt_warranty_months,
                    seating,
                    state,
                    transmission,
                    trim,
                    vin,
                    year,
                    zip
                )
                VALUES
                (
                    :body,
                    :carvana_id,
                    :city,
                    :color,
                    :drive_type,
                    :engine,
                    :kbb_value,
                    :make,
                    :mfg_basic_warranty_miles,
                    :mfg_basic_warranty_months,
                    :mfg_dt_warranty_miles,
                    :mfg_dt_warranty_months,
                    :mileage,
                    :model,
                    :num_keys,
                    :price,
                    :rem_warranty_miles,
                    :rem_warranty_months,
                    :rem_dt_warranty_miles,
                    :rem_dt_warranty_months,
                    :seating,
                    :state,
                    :transmission,
                    :trim,
                    :vin,
                    :year,
                    :zip
                );
                '''), listings)

    save_features(eng, listings)
    save_highlights(eng, listings)
    save_imperfections(eng, listings)
    save_options(eng, listings)
    save_std_equipment(eng, listings)


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
                            name,
                            kbb_option_id
                        ) 
                        VALUES
                        (
                            :vin,
                            :n,
                            :k_id
                        );
                    '''), [{'vin': vin, 'n': f['name'], 'k_ikd': f['id']} for f in ftrs])
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


def save_imperfections(eng: Engine, listings: list):
    for listing in listings:
        vin = listing['vin']
        imps = listing.get('imperfections', [])
        if type(imps) != list or len(imps) < 1:
            continue

        try:
            with eng.connect() as conn:
                with conn.begin():
                    conn.execute(sqlalchemy.text('''
                        INSERT INTO vehicle_imperfections
                        (
                            vin,
                            id,
                            description,
                            loc,
                            title,
                            zone
                        ) 
                        VALUES
                        (
                            :vin,
                            :id,
                            :description,
                            :loc,
                            :title,
                            :zone
                        );
                    '''), [
                        {
                            'vin': vin,
                            'id': i.get('id'),
                            'description': i.get('desc'),
                            'loc': i.get('loc'),
                            'title': i.get('title'),
                            'zone': i.get('zone'),
                        } for i in imps])
        except IntegrityError:
            continue


def save_options(eng: Engine, listings: list):
    for listing in listings:
        vin = listing['vin']
        opts = listing.get('options', [])
        if type(opts) != list or len(opts) < 1:
            continue

        try:
            with eng.connect() as conn:
                with conn.begin():
                    conn.execute(sqlalchemy.text('''
                        INSERT INTO vehicle_options
                        (
                            vin,
                            name,
                            price
                        ) 
                        VALUES
                        (
                            :vin,
                            :name,
                            :price
                        );
                    '''), [
                        {
                            'vin': vin,
                            'name': o.get('name'),
                            'price': o.get('price')
                        } for o in opts])
        except IntegrityError:
            continue


def save_std_equipment(eng: Engine, listings: list):
    for listing in listings:
        vin = listing['vin']
        se = listing.get('std_equipment', [])
        if type(se) != list or len(se) < 1:
            continue

        try:
            with eng.connect() as conn:
                with conn.begin():
                    conn.execute(sqlalchemy.text('''
                        INSERT INTO vehicle_std_equipment
                        (
                            vin,
                            name
                        ) 
                        VALUES
                        (
                            :vin,
                            :name
                        );
                    '''), [{'vin': vin, 'name': e} for e in se])
        except IntegrityError:
            continue


def create_tables(eng: Engine):
    with eng.connect() as conn:
        with conn.begin():
            conn.execute(sqlalchemy.text('''
                CREATE TABLE IF NOT EXISTS listings (
                    id                          SERIAL PRIMARY KEY,
                    body                        VARCHAR(24),
                    carvana_id                  INTEGER,
                    city                        VARCHAR(55),
                    color                       VARCHAR(55),
                    drive_type                  VARCHAR(8),
                    engine                      VARCHAR(55),
                    kbb_value                   INTEGER,
                    make                        VARCHAR(55),
                    mfg_basic_warranty_miles    INTEGER,
                    mfg_basic_warranty_months   SMALLINT,
                    mfg_dt_warranty_miles       INTEGER,
                    mfg_dt_warranty_months      SMALLINT,
                    mileage                     INTEGER,
                    model                       VARCHAR(55),
                    num_keys                    SMALLINT,
                    price                       INTEGER,
                    rem_warranty_miles          INTEGER,
                    rem_warranty_months         SMALLINT,
                    rem_dt_warranty_miles       INTEGER,
                    rem_dt_warranty_months      SMALLINT,
                    seating                     SMALLINT,
                    state                       VARCHAR(2),
                    transmission                VARCHAR(55),
                    trim                        VARCHAR(55),
                    vin                         VARCHAR(17),
                    year                        SMALLINT,
                    zip                         VARCHAR(5),
                    scrape_date                 DATE NOT NULL DEFAULT CURRENT_DATE
                );
            '''))

        with conn.begin():
            conn.execute(sqlalchemy.text('''
                CREATE TABLE IF NOT EXISTS vehicle_features (
                    vin             VARCHAR(17) NOT NULL,
                    name            VARCHAR(255) NOT NULL,
                    kbb_option_id   INTEGER NOT NULL,
                    scrape_date     DATE NOT NULL DEFAULT CURRENT_DATE,
                    PRIMARY KEY (vin, name)
                );
            '''))

        with conn.begin():
            conn.execute(sqlalchemy.text('''
                CREATE TABLE IF NOT EXISTS vehicle_highlights (
                    vin             VARCHAR(17) NOT NULL,
                    name            VARCHAR(255) NOT NULL,
                    scrape_date     DATE NOT NULL DEFAULT CURRENT_DATE,
                    PRIMARY KEY (vin, name)
                );
            '''))

        with conn.begin():
            conn.execute(sqlalchemy.text('''
                CREATE TABLE IF NOT EXISTS vehicle_imperfections (
                    id          INTEGER PRIMARY KEY,
                    vin         VARCHAR(17) NOT NULL,
                    description VARCHAR(255) NOT NULL,
                    loc         VARCHAR(55) NOT NULL,
                    title       VARCHAR(55) NOT NULL,
                    zone        VARCHAR(105) NOT NULL,
                    scrape_date DATE NOT NULL DEFAULT CURRENT_DATE
                )
            '''))

        with conn.begin():
            conn.execute(sqlalchemy.text('''
                CREATE INDEX IF NOT EXISTS imperfections_vin_idx 
                ON vehicle_imperfections (vin);
            '''))

        with conn.begin():
            conn.execute(sqlalchemy.text('''
                CREATE TABLE IF NOT EXISTS vehicle_options (
                    vin             VARCHAR(17) NOT NULL,
                    name            VARCHAR(255) NOT NULL,
                    price           SMALLINT,
                    scrape_date     DATE NOT NULL DEFAULT CURRENT_DATE,
                    PRIMARY KEY (vin, name)
                )
            '''))

        with conn.begin():
            conn.execute(sqlalchemy.text('''
                CREATE TABLE IF NOT EXISTS vehicle_std_equipment (
                    vin             VARCHAR(17) NOT NULL,
                    name            VARCHAR(155) NOT NULL,
                    scrape_date     DATE NOT NULL DEFAULT CURRENT_DATE,
                    PRIMARY KEY (vin, name)
                )
            '''))

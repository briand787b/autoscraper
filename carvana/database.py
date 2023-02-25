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


def save_listing(eng: Engine, listing: dict):
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
                '''), listing)

    save_features(eng, listing)
    save_highlights(eng, listing)
    save_imperfections(eng, listing)
    save_options(eng, listing)
    save_std_equipment(eng, listing)


def save_features(eng: Engine, listing: dict):
    vin = listing.get('vin')
    ftrs = listing.get('features')
    if type(vin) != str or type(ftrs) != list or len(ftrs) < 1:
        return

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
                    '''), [{'vin': vin, 'n': f['name'], 'k_id': f['id']} for f in ftrs])
    except IntegrityError:
        return


def save_highlights(eng: Engine, listing: dict):
    vin = listing.get('vin')
    hs = listing.get('highlights', [])
    if type(vin) != str or type(hs) != list or len(hs) < 1:
        return

    try:
        with eng.connect() as conn:
            with conn.begin():
                conn.execute(sqlalchemy.text('''
                        INSERT INTO vehicle_highlights
                        (
                            vin,
                            name
                        ) 
                        VALUES
                        (
                            :vin,
                            :hl
                        );
                    '''), [{'vin': vin, 'hl': h} for h in hs])
    except IntegrityError:
        return


def save_imperfections(eng: Engine, listing: dict):
    vin = listing.get('vin')
    imps = listing.get('imperfections', [])
    if type(vin) != str or type(imps) != list or len(imps) < 1:
        return

    imps = filter(lambda i: len(i.get("desc", "")) > 0, imps)

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
                        'description': i["desc"] if len(i["desc"]) < 256 else i["desc"][:255],
                        'loc': i.get('loc'),
                        'title': i.get('title'),
                        'zone': i.get('zone'),
                    } for i in imps])
    except IntegrityError:
        return


def save_options(eng: Engine, listing: dict):
    vin = listing.get('vin')
    opts = listing.get('options', [])
    if type(vin) != str or type(opts) != list or len(opts) < 1:
        return

    opts = filter(lambda i: len(i.get("name", "")) > 0, opts)

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
                        'name': o["name"] if len(o["name"]) < 256 else o["name"][:255],
                        'price': o.get('price')
                    } for o in opts])
    except IntegrityError:
        return


def save_std_equipment(eng: Engine, listing: dict):
    vin = listing['vin']
    se = listing.get('std_equipment', [])
    if type(vin) != str or type(se) != list or len(se) < 1:
        return

    try:
        with eng.connect() as conn:
            with conn.begin():
                conn.execute(sqlalchemy.text('''
                        INSERT INTO vehicle_std_equipment
                        (
                            vin,
                            description
                        ) 
                        VALUES
                        (
                            :vin,
                            :description
                        );
                    '''), [{'vin': vin, 'description': e} for e in se])
    except IntegrityError:
        return


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
                    price           INTEGER,
                    scrape_date     DATE NOT NULL DEFAULT CURRENT_DATE,
                    PRIMARY KEY (vin, name)
                )
            '''))

        with conn.begin():
            conn.execute(sqlalchemy.text('''
                CREATE TABLE IF NOT EXISTS vehicle_std_equipment (
                    vin             VARCHAR(17) NOT NULL,
                    description     TEXT NOT NULL,
                    scrape_date     DATE NOT NULL DEFAULT CURRENT_DATE,
                    PRIMARY KEY (vin, description)
                )
            '''))

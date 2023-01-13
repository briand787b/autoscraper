import sqlite3

con = sqlite3.connect('inventory.db')
cur = con.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS listings (
	    id INTEGER NOT NULL PRIMARY KEY,
        autotrader_id VARCHAR(55),
        color VARCHAR(55),
        drive_type VARCHAR(16),
        engine VARCHAR(16),
        make VARCHAR(55),
        mileage INTEGER,
        model VARCHAR(55),
        mpg_city INTEGER,
        mpg_hwy INTEGER,
        price INTEGER,
	    created_at DATETIME NOT NULL DEFAULT current_timestamp, 
	    updated_at DATETIME NOT NULL DEFAULT current_timestamp
    )
''')

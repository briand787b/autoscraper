CREATE TABLE IF NOT EXISTS generations (
	id INTEGER NOT NULL PRIMARY KEY,
	generation INTEGER NOT NULL,
	vehicle_id INTEGER NOT NULL,
	alias VARCHAR(24),
    class VARCHAR(24) NOT NULL,
    start_year INTEGER NOT NULL,
    end_year INTEGER,
    created_at DATETIME NOT NULL DEFAULT current_timestamp,
    updated_at DATETIME NOT NULL DEFAULT current_timestamp
);

INSERT INTO generations
(
	generation INTEGER NOT NULL,
    vehicle_id INTEGER NOT NULL,
	alias VARCHAR(24),
    class VARCHAR(24) NOT NULL,
    start_year INTEGER NOT NULL,
    end_year INTEGER,
    attrs json
)
VALUES
(
    1,
    4,
    'GX 470',
    'Full-size luxury SUV',
    2003,
    2009,
    NULL
),
(
    2,
    4,
    'GX 460',
    'Full-size luxury SUV',
    2009,
    NULL,
    NULL
),
(
    2,
    5,
    NULL,
    'Mid-size pickup truck',
    2011,
    2023,
    NULL
),
(
    11,
    1,
    NULL,
    'Full-size pickup truck',
    2004,
    2008,
    '{"tags": ["poor_reliability"]}'
),
(--5
    12,
    1,
    NULL,
    'Full-size pickup truck',
    2009,
    2014,
    NULL
),
(
    13,
    1,
    NULL,
    'Full-size pickup truck',
    2015,
    2020,
    NULL
),
;
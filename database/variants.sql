CREATE TABLE IF NOT EXISTS variants (
	id INTEGER NOT NULL PRIMARY KEY,
	vehicle_id INTEGER NOT NULL,
	production_year INTEGER NOT NULL,
	trim VARCHAR(30),
	engine VARCHAR(30) NOT NULL,
	mpg_city INTEGER,
	mpg_hwy INTEGER,
	generation INTEGER,
	drive_line VARCHAR(3),
	attrs json,
	created_at DATETIME NOT NULL DEFAULT current_timestamp, 
	updated_at DATETIME NOT NULL DEFAULT current_timestamp
);

INSERT INTO variants
(
	vehicle_id,
	production_year,
	trim,
	engine,
	drive_line,
	mpg_city,
	mpg_hwy,
	generation,
	attrs
)
VALUES
(
	1,
	2019,
	'xlt',
	'3.5L 6-cylinder turbo gas engine',
	'4wd',
	18,
	23,
	13,
	NULL
),
(
	1,
	2019,
	'xlt',
	'2.7L 6-cylinder turbo gas engine',
	'4wd',
	18,
	23,
	13,
	NULL
),
(
	4,
	2009,
	NULL,
	'4.7L 8-cylinder gas engine',
	'4wd',
	14,
	18,
	1,
	NULL
),
(
	1,
	2017,
	'xlt',
	'3.5L 6-Cylinder Flexible Fuel Engine',
	'4wd',
	17,
	23,
	13,
	NULL
),
(--5
	1,
	2013,
	'xlt',
	'3.5L 6-Cylinder Turbo Gas Engine',
	'4wd',
	14,
	19,
	12,
	NULL
),
(
	3,
	2017,
	'limited',
	'3.5L 6-Cylinder Turbo Gas Engine',
	'4wd',
	15,
	20,
	3,
	NULL
);
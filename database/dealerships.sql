CREATE TABLE IF NOT EXISTS dealerships (
	id INTEGER NOT NULL PRIMARY KEY,
	name VARCHAR(55) NOT NULL UNIQUE,
	city VARCHAR(55),
	state VARCHAR(2),
	attrs json,
	created_at DATETIME NOT NULL DEFAULT current_timestamp, 
	updated_at DATETIME NOT NULL DEFAULT current_timestamp
);

INSERT INTO dealerships
(
	name,
	city,
	state
)
VALUES
(
	'Mall of Georgia Ford',
	'Buford',
	'GA'
),
(
	'Billy Cain Ford Lincoln',
	'Cornelia',
	'GA'
),
(
	'Private Seller',
	NULL,
	NULL
),
(
	'Don Jackson Chrysler Dodge Jeep RAM North',
	'Cumming',
	'GA'
),
(--5
	'AutoNation Hyundai Mall of Georgia',
	'Buford',
	'GA'
),
(
	'Auto Gallery Gainesville',
	'Gainesville',
	'GA'
),
(
	'Toyota of Greenville',
	'Greenville',
	'SC'
),
(
	'Cloninger Ford of Hickory',
	'Hickory',
	'NC'
),
(
	'Lexus of Greenville',
	'Greenville',
	'SC'
),
(--10
	'Victory Chevrolet',
	'Charlotte',
	'NC'
);
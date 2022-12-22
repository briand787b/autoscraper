CREATE TABLE IF NOT EXISTS vehicles (
	id INTEGER NOT NULL PRIMARY KEY,
	manufacturer VARCHAR(30) NOT NULL,
	model VARCHAR(30) NOT NULL,
	body_style VARCHAR(10) NOT NULL,
	attrs json,
	created_at DATETIME NOT NULL DEFAULT current_timestamp, 
	updated_at DATETIME NOT NULL DEFAULT current_timestamp
);

INSERT INTO vehicles
(
	manufacturer,
	model,
	body_style,
	attrs
)
VALUES
(
	'ford',
	'f-150',
	'full-size truck',
	NULL
),
(
	'chevrolet',
	'silverado',
	'full-size truck',
	NULL
),
(
	'ford',
	'expedition',
	'full-size suv',
	NULL
),
(
	'ford',
	'expedition el/max',
	'full-size suv',
	NULL
),
(--5
	'lexus',
	'gx 470',
	'Full-size luxury SUV',
	NULL
),
(
	'lexus',
	'gx 460',
	'Full-size luxury SUV',
	NULL
),
(
	'Chevrolet',
	'Colorado',
	'Mid-size pickup truck'
);

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

CREATE TABLE IF NOT EXISTS listings (
	id INTEGER NOT NULL PRIMARY KEY,
	variant_id INTEGER NOT NULL,
	dealership_id INTEGER NOT NULL,
	asking_price INTEGER NOT NULL,
	mileage INTEGER NOT NULL,
	vin VARCHAR(17) UNIQUE,
	exterior_color VARCHAR(24),
	uri TEXT NOT NULL UNIQUE,
	attrs json,
	created_at DATETIME NOT NULL DEFAULT current_timestamp,
	updated_at DATETIME NOT NULL DEFAULT current_timestamp
);

INSERT INTO listings
(
	variant_id,
	dealership_id,
	asking_price,
	mileage,
	vin,
	exterior_color,
	attrs
)
VALUES
(
	1,
	2,
	39582,
	35232,
	'black',
	'1FTEW1EP5KFC25336',
	'https://autotrader.com/1',
	'{"bed_size_ft":5.5,"packages":["Equipment Group 302A Luxury","XLT Sport Appearance Package","XLT Chrome Appearance Package","XLT Power Equipment Group"]}'
),
(
	2,
	2,
	39995,
	26648,
	'oxford white',
	'1FTEW1EP5KFA12340',
	'https://autotrader.com/2',
	'{"bed_size_ft":5.5,"packages":["Equipment Group 302A Luxury","XLT Special Edition Package","XLT Sport Appearance Package","XLT Chrome Appearance Package","XLT Power Equipment Group"]}'
),
(
	3,
	3,
	19400,
	131500,
	'burgundy',
	'JTJBT20X990174460',
	'https://autotrader.com/3',
	'{"prev_owners": 1, "packages": "towing"}'
),
(
	4,
	4,
	19995,
	127462,
	'white',
	'1FTEW1E85HFA12792',
	'https://autotrader.com/4',
	NULL
),
(--5
	5,
	5,
	16997,
	167569,
	'race red',
	'1FTFW1ET2DFA77473',
	'https://autotrader.com/5',
	'{"bed_size_ft":5.5,"packages":["Luxury Equipment Group","XLT Chrome Package","XLT Convenience Package","XLT Plus Pkg", "Trailer Tow Pkg"]}'
),
(
	6,
	6,
	27495,
	82605,
	'blue',
	'1FMJU2AT0HEA53157',
	'https://autotrader.com/6',
	NULL
),
(
	6,
	7,
	31692,
	71224,
	'Ruby Red Metallic Tinted Clearcoat Exterior',
	'1FMJU2AT8HEA06636',
	'https://autotrader.com/7',
	'{"packages":["Equipment Group 301A"]}'
),
(
	6,
	8,
	25463,
	105625
	'White Platinum Metallic Tri-Coat Exterior',
	'1FMJU2AT8HEA74466',
	'https://autotrader.com/8',
	NULL
),
(
	6,
	9,
	25999,
	89961
	'White Platinum Exterior',
	'1FMJU2AT2HEA76410',
	'https://autotrader.com/9',
	'{"packages":["Equipment Group 301A"]}'
),
(--10
	6,
	10,
	19000,
	184329
	'Magnetic Exterior',
	'1FMJU2AT8HEA01985',
	'https://www.autotrader.com/cars-for-sale/vehicledetails.xhtml?listingId=594744249&0=vehicledetails.xhtml&driveGroup=AWD4WD&makeCodeList=FORD&modelCodeList=EXPEDI&city=Clarkesville&state=GA&zip=30523&searchRadius=200&marketExtension=include&isNewSearch=false&showAccelerateBanner=false&sortBy=relevance&numRecords=25&firstRecord=25&listingTypes=USED&referrer=%2Fcars-for-sale%2Fawd-4wd%2Fford%2Fexpedition%2Fclarkesville-ga-30523%3F0%3Dvehicledetails.xhtml%26searchRadius%3D200%26marketExtension%3Dinclude%26isNewSearch%3Dfalse%26showAccelerateBanner%3Dfalse%26sortBy%3Drelevance%26numRecords%3D25%26firstRecord%3D25&clickType=listing',
	NULL
);

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

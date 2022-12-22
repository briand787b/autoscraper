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
	'Ford',
	'F-150',
	'Truck',
	NULL
),
(
	'Chevrolet',
	'Silverado',
	'Truck',
	NULL
),
(
	'Ford',
	'Expedition',
	'SUV',
	NULL
),
(
	'Lexus',
	'GX',
	'SUV',
	NULL
),
(--5
	'Chevrolet',
	'Colorado',
	'Truck'
);
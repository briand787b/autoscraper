-- head
SELECT * FROM listings LIMIT 500;
SELECT * FROM vehicle_features LIMIT 500;
SELECT * FROM vehicle_packages LIMIT 500;


-- clear db
DELETE FROM listings;
DELETE FROM vehicle_features;
DELETE FROM vehicle_packages;


-- how many records vs DISTINCT vins (listings)
SELECT 
    COUNT(*) AS num_records,
    COUNT(DISTINCT(vin)) AS DISTINCT_vins
FROM listings;


-- number of records from each table
SELECT
(SELECT COUNT(*) FROM listings) AS listings_record_count,
(SELECT COUNT(*) FROM vehicle_features) AS features_record_count,
(SELECT COUNT(*) FROM vehicle_packages) AS packages_record_count;


-- number of distinct features
SELECT
    COUNT(DISTINCT(feature))
FROM vehicle_features;


-- see most common features
SELECT
    feature,
    COUNT(*) as feature_count
FROM vehicle_features
GROUP BY feature
ORDER BY feature_count DESC
LIMIT 100;


-- sample listings table
SELECT * FROM listings LIMIT 10;


-- how many of each model do we have
SELECT
    model,
    make,
    COUNT(*) AS num_records
FROM listings
GROUP BY model, make
ORDER BY make, model;


-- avg price by model
SELECT
    ROUND(AVG(price)) AS avg_price,
    MAX(price) AS max_price,
    MIN(price) AS min_price,
    model,
    make
FROM listings
GROUP BY model, make
ORDER BY avg_price DESC;


-- how many records vs unqiue vins (features)
SELECT 
    COUNT(*) AS num_records,
    COUNT(DISTINCT(vin)) AS DISTINCT_vins
FROM vehicle_features;


-- which vins have the most features
SELECT 
    vin,
    COUNT(*) AS feature_COUNT
FROM vehicle_features
GROUP BY vin
ORDER BY feature_COUNT DESC
LIMIT 10;


-- seek out zero-price items, they should not exist
SELECT * FROM listings WHERE price = 0;


-- how does the price of a listing change over time
SELECT
    COUNT(*) AS num_listings,
    MAX(price) AS max_price,
    MIN(price) AS min_price,
    ROUND(AVG(price)) AS avg_price,
    vin
FROM listings
GROUP BY vin
HAVING max_price != min_price;


-- ensure vin consistency
SELECT
    vin, make, model, COUNT(*)
FROM listings
GROUP BY vin, make, model;


-- compare truck prices in unbiased way
SELECT
    make, model, trim, drive_type, year, engine,
    COUNT(*) AS num_records,
    ROUND(AVG(mpg_city), 2) AS avg_mpg_city,
    ROUND(AVG(mpg_hwy), 2) AS avg_mpg_hwy,
    ROUND(AVG(mileage)) AS avg_mileage,
    ROUND(AVG(price)) AS avg_price
FROM listings
WHERE 
    condition = 'used'
--    AND mileage BETWEEN 30000 AND 70000
GROUP BY make, model, drive_type, trim, year, engine
HAVING 
    drive_type = '4 wheel drive' AND
    model IN ('1500', 'silverado 1500', 'f150', 'tacoma', 'colorado', 'tundra', 'frontier', 'titan') AND
    trim IN ('xlt', 'lt', 'big horn', 'sr5', 'sv')
ORDER BY 
    year DESC,
    avg_price ASC;
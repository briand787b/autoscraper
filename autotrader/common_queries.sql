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
SELECT * FROM listings ORDER BY id DESC LIMIT 10;


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
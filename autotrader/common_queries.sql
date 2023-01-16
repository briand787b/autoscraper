-- how many records vs DISTINCT vins (listings)
SELECT 
    COUNT(*) AS num_records,
    COUNT(DISTINCT(vin)) AS DISTINCT_vins
FROM listings;


-- how many of each model do we have
SELECT
    model,
    COUNT(*)
FROM listings
GROUP BY model;


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
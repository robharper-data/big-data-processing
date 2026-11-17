Register 'fare_band.py' using streaming_python as myfunc; -- Register python UDF for fare band classification

-- ============================================================================
--                                 TASK 1
-- ============================================================================

-- 1.1 Load raw data from HDFS
trips = LOAD 'hdfs:///Input/Trips.txt'
        USING PigStorage('\t')
        as (trip_id:int, taxi_id:int, company_id:int, 
            dropoff_lat:double, dropoff_lon:double, 
            distance_km:double, fare:double);

taxis = LOAD 'hdfs:///Input/Taxis.txt'
        USING PigStorage('\t')
        as (taxi_id:int, license_plate:chararray, 
            medallion_year:int, driver_rating:double);

companies = LOAD 'hdfs:///Input/Companies.txt'
            USING PigStorage('\t')
            as (company_id:int, company_name:chararray);

-- 1.2.1 Remove records with empty fields
trips_cl1 = FILTER trips BY trip_id IS NOT NULL 
            AND taxi_id IS NOT NULL AND company_id IS NOT NULL 
            AND dropoff_lat IS NOT NULL AND dropoff_lon IS NOT NULL 
            AND distance_km IS NOT NULL AND fare IS NOT NULL;

-- 1.2.2 Remove records with negative/zero distance OR distance > 20km OR fare < 5
trips_cl2 = FILTER trips_cl1 BY distance_km > 0 AND distance_km <= 20 AND fare >= 5;

-- 1.3 Store cleane trip data to HDFS
STORE trips_cl2 INTO 'hdfs:///Output/clean_trips';

-- ============================================================================
--                                   TASK 2
-- ============================================================================
-- 2.1 Join cleaned trips with taxi and company datasets on taxi_id variable
trips_taxis = JOIN trips_cl2 BY taxi_id, taxis BY taxi_id;
trips_taxis_company = JOIN trips_taxis BY company_id, companies BY company_id;

-- 2.2 Produce enriched relation 
enriched_trips = FOREACH trips_taxis_company GENERATE 
    trips_taxis::taxis::taxi_id        AS taxi_id:int,
    companies::company_id              AS company_id:int,
    companies::company_name            AS company_name:chararray,
    trips_taxis::taxis::driver_rating  AS driver_rating:double,
    trips_taxis::trips_cl2::distance_km AS distance_km:double,
    trips_taxis::trips_cl2::fare        AS fare:double,
    trips_taxis::trips_cl2::dropoff_lat AS dropoff_lat:double,
    trips_taxis::trips_cl2::dropoff_lon AS dropoff_lon:double;

-- 2.3 Store enriched data to HDFS
STORE enriched_trips INTO 'hdfs:///Output/enriched_trips';

-- ============================================================================
--                                   TASK 3
-- ============================================================================
-- 3.1 Group the enriched trips data to perform statistical calculations
company_group = GROUP enriched_trips BY (company_id,company_name);

-- Calculate specified key metrics for each company
company_stats = FOREACH company_group GENERATE
        group.company_id                                    AS company_id,
        group.company_name                                  AS company_name,
        COUNT(enriched_trips)                               AS trip_count,
        ROUND_TO(SUM(enriched_trips.distance_km),2)         AS total_distance_km,
        ROUND_TO(AVG(enriched_trips.distance_km),2)         AS avg_distance_km,
        ROUND_TO(AVG(enriched_trips.fare),2)                AS avg_fare;

-- 3.2 Sort results by trip count (ascending) and company name (ascending)
sorted_company_stats = ORDER company_stats BY trip_count ASC, company_name ASC;

-- 3.3 Store company statistics to HDFS
STORE sorted_company_stats INTO 'hdfs:///Output/company_stats';

-- ============================================================================
--                                   TASK 4 (PG)
-- ============================================================================
-- UG Requirement
-- Classify fares into bands by applying Python UDF (fare_band.py)
trip_bands = FOREACH enriched_trips GENERATE
        *, myfunc.fare_band(fare) AS fare_band:chararray;

-- Group by company and fare abdn to count trips in each category
grouped_fare_bands = GROUP trip_bands BY (company_id, company_name, fare_band);

-- Count the number of trips in each fare band per company
aggregated_grouped_fare_bands = FOREACH grouped_fare_bands GENERATE
        group.company_id,
        group.company_name,
        group.fare_band,
        COUNT(trip_bands) AS fare_band_count:int;

-- PG Requirement
-- Group by company to prepare for pivoting into fare bands
fare_bands_grouped = GROUP aggregated_grouped_fare_bands BY (company_id, company_name);

-- Create seperate columns for LOW, MID, HIGH fare counts
-- Use nested FILTER function to seperate fare bands and 
fare_bands_by_company = FOREACH fare_bands_grouped {
    low  = FILTER aggregated_grouped_fare_bands BY fare_band == 'LOW';
    mid  = FILTER aggregated_grouped_fare_bands BY fare_band == 'MID';
    high = FILTER aggregated_grouped_fare_bands BY fare_band == 'HIGH';

-- Generate output with seperate columns for each fare band - accounting for circumstance where
-- a company has a zero count for a fare band
    GENERATE
        group.company_id  AS company_id,
        group.company_name AS company_name,
        ((SUM(low.fare_band_count)  is null) ? 0L : SUM(low.fare_band_count))  AS LOW,
        ((SUM(mid.fare_band_count)  is null) ? 0L : SUM(mid.fare_band_count))  AS MID,
        ((SUM(high.fare_band_count) is null) ? 0L : SUM(high.fare_band_count)) AS HIGH;
};

-- Output to HDFS
STORE fare_bands_by_company INTO 'hdfs:///Output/fare_bands_by_company'; -- Task 4 Final output
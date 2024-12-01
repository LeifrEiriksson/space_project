CREATE TABLE flares_daily (
    id SERIAL PRIMARY KEY, 
    flr_id VARCHAR(50) NOT NULL UNIQUE,
    instruments JSON,
    begin_time TIMESTAMP,
    peak_time TIMESTAMP,
    end_time TIMESTAMP,
    class_type VARCHAR(10),
    source_location VARCHAR(20),
    active_region_num INTEGER,
    note TEXT,
    submission_time TIMESTAMP,
    version_id INTEGER,
    link TEXT,
    linked_events JSON
);


CREATE TABLE crew_iss_daily (
    id SERIAL PRIMARY KEY, 
    name VARCHAR(100) NOT NULL,
    date_ref DATE NOT NULL 
);


CREATE TABLE neos_daily (
    id SERIAL PRIMARY KEY, 
    ref_date DATE NOT NULL, 
    neo_id BIGINT NOT NULL, 
    name VARCHAR(50), 
    is_potentially_hazardous_asteroid BOOLEAN NOT NULL, 
    orbiting_body VARCHAR(50) NOT NULL,
    close_approach_date DATE NOT NULL, 
    kilometers_per_hour FLOAT,
    kilometers_per_second FLOAT, 
    estimated_diameter_min_meters FLOAT, 
    estimated_diameter_max_meters FLOAT
);

CREATE TABLE iss_positions (
    id SERIAL PRIMARY KEY,        
    latitude FLOAT NOT NULL,        
    longitude FLOAT NOT NULL,       
    ns VARCHAR(10) NOT NULL,       
    we VARCHAR(10) NOT NULL,       
    date_hour_ref TIMESTAMP NOT NULL   
);

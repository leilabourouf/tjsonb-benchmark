CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS mobilitydb;


DROP TABLE IF EXISTS readings_mobility_small;

CREATE TABLE readings_mobility_small (
    sensor_id TEXT,
    traj TJSONB
);


DROP TABLE IF EXISTS readings_mobility_medium;

CREATE TABLE readings_mobility_medium (
    sensor_id TEXT,
    traj TJSONB
);


DROP TABLE IF EXISTS readings_mobility_large;

CREATE TABLE readings_mobility_large (
    sensor_id TEXT,
    traj TJSONB
);
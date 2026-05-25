CREATE EXTENSION IF NOT EXISTS timescaledb;


DROP TABLE IF EXISTS readings_timescale_small;

CREATE TABLE readings_timescale_small (
    sensor_id TEXT,
    ts TIMESTAMPTZ NOT NULL,
    data JSONB NOT NULL
);

SELECT create_hypertable(
    'readings_timescale_small',
    'ts',
    if_not_exists => TRUE
);


DROP TABLE IF EXISTS readings_timescale_medium;

CREATE TABLE readings_timescale_medium (
    sensor_id TEXT,
    ts TIMESTAMPTZ NOT NULL,
    data JSONB NOT NULL
);

SELECT create_hypertable(
    'readings_timescale_medium',
    'ts',
    if_not_exists => TRUE
);


DROP TABLE IF EXISTS readings_timescale_large;

CREATE TABLE readings_timescale_large (
    sensor_id TEXT,
    ts TIMESTAMPTZ NOT NULL,
    data JSONB NOT NULL
);

SELECT create_hypertable(
    'readings_timescale_large',
    'ts',
    if_not_exists => TRUE
);
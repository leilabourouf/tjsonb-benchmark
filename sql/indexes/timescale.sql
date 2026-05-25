DROP INDEX IF EXISTS idx_ts_small;
DROP INDEX IF EXISTS idx_ts_medium;
DROP INDEX IF EXISTS idx_ts_large;

DROP INDEX IF EXISTS idx_sensor_ts_small;
DROP INDEX IF EXISTS idx_sensor_ts_medium;
DROP INDEX IF EXISTS idx_sensor_ts_large;

DROP INDEX IF EXISTS idx_temp_small;
DROP INDEX IF EXISTS idx_temp_medium;
DROP INDEX IF EXISTS idx_temp_large;


-- Time indexes
CREATE INDEX idx_ts_small
ON readings_timescale_small(ts);

CREATE INDEX idx_ts_medium
ON readings_timescale_medium(ts);

CREATE INDEX idx_ts_large
ON readings_timescale_large(ts);


-- Sensor + timestamp indexes
CREATE INDEX idx_sensor_ts_small
ON readings_timescale_small(sensor_id, ts);

CREATE INDEX idx_sensor_ts_medium
ON readings_timescale_medium(sensor_id, ts);

CREATE INDEX idx_sensor_ts_large
ON readings_timescale_large(sensor_id, ts);


-- Temperature indexes
CREATE INDEX idx_temp_small
ON readings_timescale_small(
    ((data->>'temperature')::float)
);

CREATE INDEX idx_temp_medium
ON readings_timescale_medium(
    ((data->>'temperature')::float)
);

CREATE INDEX idx_temp_large
ON readings_timescale_large(
    ((data->>'temperature')::float)
);
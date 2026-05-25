SELECT DISTINCT ON (sensor_id)
       sensor_id,
       (data->>'temperature')::float
FROM readings_timescale_{size}
ORDER BY sensor_id, ts ASC;
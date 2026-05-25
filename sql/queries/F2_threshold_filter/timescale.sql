SELECT sensor_id
FROM readings_timescale_{size}
WHERE (data->>'temperature')::float > 30
GROUP BY sensor_id;
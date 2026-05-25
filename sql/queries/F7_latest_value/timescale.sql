SELECT sensor_id,
       last((data->>'temperature')::float, ts)
FROM readings_timescale_{size}
GROUP BY sensor_id
ORDER BY sensor_id;
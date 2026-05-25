SELECT sensor_id, MAX(ts) - MIN(ts)
FROM readings_timescale_{size}
GROUP BY sensor_id
ORDER BY sensor_id;
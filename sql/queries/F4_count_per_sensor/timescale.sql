SELECT sensor_id, COUNT(*)
FROM readings_timescale_{size}
GROUP BY sensor_id
ORDER BY sensor_id;
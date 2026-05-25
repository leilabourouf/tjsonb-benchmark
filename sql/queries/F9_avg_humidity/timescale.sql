SELECT sensor_id,
       ROUND(AVG((data->>'humidity')::float)::numeric, 6)
FROM readings_timescale_{size}
GROUP BY sensor_id
ORDER BY sensor_id;
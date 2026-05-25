SELECT sensor_id,
       ROUND(AVG((data->>'temperature')::float)::numeric, 6)
FROM readings_timescale_{size}
WHERE ts BETWEEN '2004-03-01' AND '2004-03-02'
GROUP BY sensor_id
ORDER BY sensor_id;
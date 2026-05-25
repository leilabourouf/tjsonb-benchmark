SELECT sensor_id,
       ROUND(twAvg(tfloat(traj, 'humidity'))::numeric, 6)
FROM readings_mobility_{size}
ORDER BY sensor_id;
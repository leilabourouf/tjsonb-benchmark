SELECT sensor_id, duration(traj, TRUE)
FROM readings_mobility_{size}
ORDER BY sensor_id;
SELECT sensor_id, numInstants(traj)
FROM readings_mobility_{size}
ORDER BY sensor_id;
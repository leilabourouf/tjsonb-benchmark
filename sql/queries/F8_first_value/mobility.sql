SELECT sensor_id,
       (startValue(traj)->>'temperature')::float
FROM readings_mobility_{size}
ORDER BY sensor_id;
SELECT sensor_id,
       (endValue(traj)->>'temperature')::float
FROM readings_mobility_{size}
ORDER BY sensor_id;
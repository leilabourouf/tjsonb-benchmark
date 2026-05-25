SELECT sensor_id
FROM readings_mobility_{size}
WHERE tfloat(traj, 'temperature') ?> 30;
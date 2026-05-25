SELECT sensor_id
FROM readings_mobility_{size}
WHERE traj && tstzspan('[2004-03-01, 2004-03-02]');
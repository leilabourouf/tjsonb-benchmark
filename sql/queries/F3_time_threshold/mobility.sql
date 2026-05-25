SELECT sensor_id
FROM readings_mobility_{size}
WHERE tfloat(
    atTime(traj, tstzspan('[2004-03-01, 2004-03-02]')),
    'temperature'
) ?> 30;
SELECT sensor_id,
       ROUND(
           twAvg(
               tfloat(
                   atTime(traj, tstzspan('[2004-03-01, 2004-03-02]')),
                   'temperature'
               )
           )::numeric, 6
       )
FROM readings_mobility_{size}
ORDER BY sensor_id;
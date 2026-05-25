SELECT DISTINCT sensor_id
FROM readings_timescale_{size}
WHERE ts BETWEEN '2004-03-01' AND '2004-03-02';
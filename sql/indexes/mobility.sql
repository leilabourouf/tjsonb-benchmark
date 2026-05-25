DROP INDEX IF EXISTS idx_traj_small;
DROP INDEX IF EXISTS idx_traj_medium;
DROP INDEX IF EXISTS idx_traj_large;


-- GiST trajectory indexes
CREATE INDEX idx_traj_small
ON readings_mobility_small
USING GIST (traj);

CREATE INDEX idx_traj_medium
ON readings_mobility_medium
USING GIST (traj);

CREATE INDEX idx_traj_large
ON readings_mobility_large
USING GIST (traj);
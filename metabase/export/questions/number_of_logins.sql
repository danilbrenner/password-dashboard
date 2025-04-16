select snapshot_ts, count(ls.*)
from stage.snapshots s
inner join stage.login_states ls on s.id = ls.snapshot_id
group by snapshot_ts;
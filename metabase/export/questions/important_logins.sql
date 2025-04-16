with latest_snapshot as (
    select id
    from mart.dim_snapshots
    order by snapshot_ts desc
    limit 1)
select
    ln.name,
    password_age,
    password_strength
from mart.fact_login_states fl
inner join mart.dim_logins ln on ln.id = fl.login_id
where
    fl.snapshot_id in (select id from latest_snapshot)
    and ln.is_important;
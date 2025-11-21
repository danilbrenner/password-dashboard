{{ config(
    materialized='table'
) }}

with login_sessions as (
    select max(export_ts) as export_ts 
    from {{ ref("fact_exchange_sessions") }} 
    where session_type = 'login')
select id as login_id, strength, changed_at
from {{ ref('stg_in_logins') }} l
inner join login_sessions ls on l.export_ts = ls.export_ts

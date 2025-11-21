{{ config(
    materialized='table'
) }}

select export_ts, 'master_password' as session_type, 1 as count
from {{ ref('stg_in_master_passwords') }}
group by export_ts
union all
select export_ts, 'login' as session_type, count(*) as count
from {{ ref('stg_in_logins') }}
group by export_ts
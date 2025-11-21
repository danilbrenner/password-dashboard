{{ config(
    materialized='table'
) }}

select hash, max(export_ts) as latest_export_ts
from {{ ref('stg_in_master_passwords') }}
group by hash

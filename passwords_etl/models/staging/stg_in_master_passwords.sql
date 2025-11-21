{{ config(
 schema='staging',
 materialized='incremental'
)}}

select hash, export_ts
from {{ref('raw_master_passwords')}}
{% if is_incremental() %}
    where export_ts > (select max(export_ts) from {{ this }})
{% endif %}
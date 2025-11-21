{{ config(
 schema='staging',
 materialized='incremental'
)}}

select id,
       name,
       username,
       changed_at,
       strength,
       export_ts 
from {{ref('raw_logins')}}
{% if is_incremental() %}
    where export_ts > (select max(export_ts) from {{ this }})
{% endif %}
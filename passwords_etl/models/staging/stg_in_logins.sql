{{ config(
 schema='staging',
 materialized='incremental'
)}}

select id,
       name,
       username,
       changed_at,
       strength,
       strptime(
               regexp_extract(filename, '([0-9]{14})'),
               '%Y%m%d%H%M%S'
       ) as export_ts
from {{ref('raw_logins')}}
{% if is_incremental() %}
    where export_ts > (select max(export_ts) from {{ this }})
{% endif %}
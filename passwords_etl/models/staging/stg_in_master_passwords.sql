{{ config(
 schema='staging',
 materialized='incremental'
)}}

select hash,
       strptime(
               regexp_extract(filename, '([0-9]{14})'),
               '%Y%m%d%H%M%S'
       ) as export_ts
from {{ref('raw_master_passwords')}}
where hash is not null 
  and trim(hash) != ''
{% if is_incremental() %}
    and export_ts > (select max(export_ts) from {{ this }})
{% endif %}
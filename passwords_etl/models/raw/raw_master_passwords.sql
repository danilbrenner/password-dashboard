{{config(
  schema='raw',
  materialized='view'
)}}

with raw_master_passwords as
         (select *, filename
          from {{source('raw', 'mp')}})
select hash, filename
{#       strptime(#}
{#               regexp_extract(filename, '([0-9]{14})'),#}
{#               '%Y%m%d%H%M%S'#}
{#       ) as export_ts#}
from raw_master_passwords
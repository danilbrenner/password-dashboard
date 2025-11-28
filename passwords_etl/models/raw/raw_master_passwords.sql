{{config(
  schema='raw',
  materialized='view'
)}}

with raw_master_passwords as
         (select *, filename
          from {{source('raw', 'mp')}})
select hash, filename
from raw_master_passwords
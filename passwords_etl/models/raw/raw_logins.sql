{{config(
  schema='raw',
  materialized='view'
)}}

with raw_logins as
         (select *, filename
          from {{source('raw', 'logins')}})
select id,
       name,
       username,
       changedat as changed_at,
       strength,
       strptime(
               regexp_extract(filename, '([0-9]{14})'),
               '%Y%m%d%H%M%S'
       )         as export_ts
from raw_logins
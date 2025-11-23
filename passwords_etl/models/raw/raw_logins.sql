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
       filename
from raw_logins
select Id, export_ts, count(*) as count
from {{ ref('stg_in_logins') }}
group by Id, export_ts
having count(*) > 1
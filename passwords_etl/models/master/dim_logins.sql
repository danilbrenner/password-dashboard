{{ config(
    materialized='table'
) }}
    
select distinct id as login_id, name, username
from {{ ref('stg_in_logins') }}

alter table raw.logins
add column user_name varchar(300);

create or replace view stage.logins as
select distinct
    l.login_id as id,
    l.name,
    l.user_name::text as user_name,
    case when il.login_id is null then false else true end as is_important
from raw.logins l
left join raw.important_logins il on l.login_id = il.login_id;

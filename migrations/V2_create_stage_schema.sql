create schema if not exists stage;

create table stage.enum_password_strength(
    id int not null primary key,
    value varchar(300) not null
);

create unique index enum_password_strength_value on stage.enum_password_strength(value);

create table stage.enum_password_age(
    id int not null primary key,
    value varchar(300) not null
);

create unique index enum_password_age_value on stage.enum_password_age(value);

insert into stage.enum_password_age(id, value) values (0, 'New');
insert into stage.enum_password_age(id, value) values (1, 'Recent');
insert into stage.enum_password_age(id, value) values (2, 'Moderate');
insert into stage.enum_password_age(id, value) values (3, 'Old');
insert into stage.enum_password_age(id, value) values (4, 'Ancient');

insert into stage.enum_password_strength(id, value) values (0, 'VeryWeak');
insert into stage.enum_password_strength(id, value) values (1, 'Weak');
insert into stage.enum_password_strength(id, value) values (2, 'Moderate');
insert into stage.enum_password_strength(id, value) values (3, 'Strong');
insert into stage.enum_password_strength(id, value) values (4, 'VeryStrong');

create view stage.logins as
select distinct
    l.login_id as id,
    l.name,
    null as user_name,
    case when il.login_id is null then false else true end as is_important
from raw.logins l
left join raw.important_logins il on l.login_id = il.login_id;

create view stage.snapshots as
select ev.sync_id as id, ev.timestamp as snapshot_ts
from raw.sync_events ev;

create view stage.login_states as
select
    l.login_id,
    l.sync_id as snapshot_id,
    l.age as password_age_id,
    a.value as password_age,
    l.strength as password_strength_id,
    s.value as password_strength
from raw.logins l
inner join stage.enum_password_age a on l.age = a.id
inner join stage.enum_password_strength s on l.strength = s.id;

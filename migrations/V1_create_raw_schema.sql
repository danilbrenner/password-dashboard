create schema if not exists raw;

create table raw.important_logins(login_id uuid primary key);

create table raw.sync_events(
    sync_id   uuid primary key,
    email     varchar(300) not null,
    timestamp timestamp not null);

create table raw.logins(
    login_id uuid not null,
    sync_id  uuid not null,
    name     varchar(300) not null,
    strength smallint not null,
    age      smallint not null,
    primary key (login_id, sync_id));

create schema if not exists mart;

create table mart.dim_logins(
    id uuid not null primary key,
    name varchar(300),
    user_name varchar(300),
    is_important boolean not null
);

create table mart.dim_snapshots(
    id uuid not null primary key,
    snapshot_ts timestamp not null
);

create unique index dim_snapshots_snapshot_ts on mart.dim_snapshots(snapshot_ts);

create table mart.fact_login_states(
    login_id uuid not null,
    snapshot_id uuid not null,
    password_age_id smallint not null,
    password_age varchar(300) not null,
    password_strength_id smallint not null,
    password_strength varchar(300) not null,
    primary key (login_id, snapshot_id),
    constraint fk_fact_login_states_login_id
      foreign key (login_id)
      references mart.dim_logins(id),
    constraint fk_fact_login_states_snapshot_id
      foreign key (snapshot_id)
      references mart.dim_snapshots(id)
);

create or replace procedure mart.sync_dim_logins()
language plpgsql
as $$
begin
    update mart.dim_logins
    set
        id = l.id,
        name = l.name,
        user_name = l.user_name,
        is_important = l.is_important
    from stage.logins l
    where l.id = mart.dim_logins.id;

    insert into mart.dim_logins
    select id, name, user_name, is_important
    from stage.logins l
    where not exists(select 1 from mart.dim_logins where id = l.id);
end;
$$;

create or replace procedure mart.sync_snapshots()
language plpgsql
as $$
begin
    create temp table new_snapshots(id uuid);

    insert into new_snapshots
    select id
    from stage.snapshots
    where id not in
    (select id from mart.dim_snapshots);

    insert into mart.dim_snapshots
    select id, snapshot_ts
    from stage.snapshots
    where id in (select id from new_snapshots);

    insert into mart.fact_login_states
    select login_id, snapshot_id, password_age_id, password_age, password_strength_id, password_strength
    from stage.login_states
    where snapshot_id in (select id from new_snapshots);

    drop table new_snapshots;
end;
$$;
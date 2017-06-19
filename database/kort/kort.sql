create sequence kort.fix_id;
create sequence kort.user_id;

create table kort.error_type (
    error_type_id integer primary key,
    type character varying(20) not null,
    description character varying(255),
    osm_tag character varying(100),
    view_type character varying(50),
    answer_placeholder character varying(100),
    vote_question character varying(255),
    bug_question character varying(255),
    vote_koin_count integer not null,
    fix_koin_count integer not null,
    required_votes integer not null,
    image character varying(255),
    constraint_re_description character varying(255),
    constraint_re text,
    constraint_lower_bound integer,
    constraint_upper_bound integer,
    unique(type)
);

create table kort.fix (
    fix_id integer primary key default nextval('kort.fix_id'),
    user_id integer,
    create_date timestamp not null default now(),
    error_id bigint not null,
    error_type character varying(20) not null,
    fix_koin_count integer not null,
    schema character varying(50) not null,
    osm_id bigint not null,
    message text,
    falsepositive boolean not null default false,
    complete boolean not null default false,
    valid boolean,
    in_osm boolean not null default false,
    constraint complete_validity CHECK ((complete and valid is not null) or not complete)
);

create table kort.user (
    user_id integer primary key default nextval('kort.user_id'),
    name varchar(100) not null,
    username varchar(100),
    email varchar(100),
    logged_in boolean,
    last_login timestamp not null DEFAULT now(),
    token text,
    oauth_provider varchar(100),
    oauth_user_id varchar(100),
    pic_url varchar(255),
    secret varchar(100) unique,
    unique(oauth_provider, oauth_user_id)
);

create table kort.badge (
    badge_id integer primary key,
    name varchar(100) not null,
    title varchar(100) not null,
    compare_value integer,
    description varchar(500) not null,
    color varchar(10) not null,
    sorting integer not null
);

create table kort.user_badge (
    user_id integer,
    badge_id integer,
    create_date timestamp not null DEFAULT now(),
    primary key (user_id, badge_id),
    foreign key (badge_id) references kort.badge (badge_id),
    foreign key (user_id) references kort.user (user_id)
);

create table kort.answer (
    answer_id integer primary key,
    type varchar(100),
    value varchar(100) unique not null,
    title varchar(100) not null,
    sorting integer not null,
    foreign key (type) references kort.error_type (type)
);


create or replace function reset_kort() returns boolean as $$
begin
    delete from kort.user_badge;
    delete from kort.fix;

    return true;
exception
    when others then
       return false;
end;
$$ language plpgsql;


CREATE OR REPLACE FUNCTION check_if_answer_is_valid_and_update_koin_counts()
RETURNS TRIGGER AS $$
DECLARE
    valid_missions_ids INTEGER[];
    koin_reward_count INT;
    no_of_validations INT := 3;
BEGIN
        SELECT array_agg(fix.fix_id)
        INTO valid_missions_ids
        FROM kort.fix
        WHERE error_id = NEW.error_id
        AND   schema = NEW.schema
        AND   osm_id = NEW.osm_id
        AND   NOT complete
        GROUP BY message having count(*) >= no_of_validations;

    IF array_length(valid_missions_ids, 1) >= no_of_validations THEN
        SELECT vote_koin_count
        INTO koin_reward_count
        FROM kort.errors
        WHERE id = NEW.error_id
        AND   schema = NEW.schema
        AND   osm_id = NEW.osm_id;

        UPDATE kort.fix
        SET     complete=TRUE,
                fix_koin_count=fix_koin_count+koin_reward_count
        WHERE fix_id IN (SELECT unnest(valid_missions_ids));

    END IF;
    return NEW;
END
$$ LANGUAGE plpgsql;


CREATE OR REPLACE TRIGGER trigger_check_if_answer_is_valid_and_update_koin_counts AFTER INSERT OR UPDATE ON kort.fix
for each row execute procedure check_if_answer_is_valid_and_update_koin_counts();

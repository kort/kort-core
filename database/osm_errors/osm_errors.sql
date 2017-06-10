create sequence osm_errors.error_id;

create table osm_errors.errors (
    schema varchar(6) not null default '100',
    error_id bigint primary key default nextval('osm_errors.error_id'),
    error_type_id integer not null,
    error_name varchar(100) not null,
    object_type keepright.osm_type not null,
    object_id bigint not null,
    lat integer not null,
    lon integer not null,
    geom geometry(Point,4326),
    msgid text,
    txt1 text,
    txt2 text,
    txt3 text,
    txt4 text,
    txt5 text,
    unique(schema, error_id),
    unique(error_type_id, object_type, object_id)
);
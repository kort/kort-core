create or replace view kort.all_errors as
select  e.source,
        e.error_id,
        e.schema,
        e.error_type_id,
        e.osm_id,
        e.osm_type,
        e.description,
        CAST(e.latitude AS NUMERIC)/10000000 latitude,
        CAST(e.longitude AS NUMERIC)/10000000 longitude,
        e.geom,
        e.txt1,
        e.txt2,
        e.txt3,
        e.txt4,
        e.txt5
from    all_errors.errors e;

create or replace view kort.errors as
select  e.error_id id,
        e.schema,
        t.type,
        e.osm_id,
        e.osm_type,
        t.description title,
        t.view_type,
        t.answer_placeholder,
        t.bug_question description,
        t.fix_koin_count,
        t.vote_koin_count,
        t.image,
        t.constraint_re_description,
        t.constraint_re,
        t.constraint_lower_bound,
        t.constraint_upper_bound,
        e.latitude,
        e.longitude,
        e.geom,
        e.txt1,
        e.txt2,
        e.txt3,
        e.txt4,
        e.txt5
from    kort.all_errors e,
        kort.error_type t
where   e.error_type_id = t.error_type_id
and     not exists (
        select 1
        from kort.fix f
        where f.error_id = e.error_id
        and   f.osm_id = e.osm_id
        and   f.schema = e.schema
        and   (f.complete or not f.valid));


create or replace view kort.all_fixes as
select f.fix_id,
       f.user_id,
       u.username,
       f.create_date,
       to_char(f.create_date, 'DD.MM.YYYY HH24:MI:SS') formatted_create_date,
       f.osm_id,
       e.osm_type,
       e.latitude,
       e.longitude,
       e.error_id,
       e.schema,
       t.type error_type,
       t.description error_type_description,
       e.source,
       t.osm_tag,
       f.message answer,
       f.falsepositive,
       a.title description,
       f.complete,
       f.valid,
       f.in_osm,
       t.required_votes,
from   kort.fix f
inner join kort.user u on f.user_id = u.user_id
inner join kort.all_errors e on e.error_id = f.error_id and e.schema = f.schema and e.osm_id = f.osm_id
inner join kort.error_type t on e.error_type_id = t.error_type_id
left  join kort.answer a on a.type = t.type and a.value = f.message;


create or replace view kort.select_answer as
select a.answer_id id,
       a.type,
       a.value,
       a.title,
       a.sorting
from   kort.answer a;

create or replace view kort.user_badges as
select b.badge_id id,
       b.name,
       b.title,
       b.description,
       b.color,
       b.sorting
from   kort.badge b
order by b.sorting;


create or replace view kort.error_types as
select t.error_type_id,
       t.type,
       t.description,
       t.view_type,
       t.answer_placeholder,
       t.vote_question,
       t.vote_koin_count,
       t.fix_koin_count,
       t.required_votes,
       t.image,
       t.constraint_re_description,
       t.constraint_re,
       t.constraint_lower_bound,
       t.constraint_upper_bound
from   kort.error_type t;


create or replace view kort.statistics as
select
(select count(*) from kort.fix) fix_count,
(select count(*) from kort.fix where complete) complete_fix_count,
(select count(*) from kort.fix where not complete) incomplete_fix_count,
(select count(*) from kort.fix where complete and valid) validated_fix_count,
(select count(*) from kort.user where oauth_provider != '') user_count,
(select count(*) from kort.user where oauth_provider = 'osm') osm_user_count,
(select count(*) from kort.user where oauth_provider = 'google') google_user_count,
(select count(*) from kort.user where oauth_provider = 'facebook') fb_user_count,
(select count(*) from kort.user_badge) badge_count,
(select count(*) from kort.fix where valid and error_type='motorway_ref') solved_motorway_ref_count,
(select count(*) from kort.fix where valid and error_type='religion') solved_religion_count,
(select count(*) from kort.fix where valid and error_type='poi_name') solved_poi_name_count,
(select count(*) from kort.fix where valid and error_type='missing_maxspeed') solved_missing_maxspeed_count,
(select count(*) from kort.fix where valid and error_type='language_unknown') solved_language_unknown_count,
(select count(*) from kort.fix where valid and error_type='missing_track_type') solved_missing_track_type_count,
(select count(*) from kort.fix where valid and error_type='way_wo_tags') solved_way_wo_tags_count,
(select count(*) from kort.fix where valid and error_type='missing_cuisine') solvedmissing_cuisine_count,
(select count(*) from kort.fix where valid and error_type='opening_hours') solved_opening_hours_count,
(select count(*) from kort.fix where valid and error_type='missing_level') solved_missing_level_count,
(select count(*) from kort.user_badge where badge_id = 1) highscore_place_1_count,
(select count(*) from kort.user_badge where badge_id = 2) highscore_place_2_count,
(select count(*) from kort.user_badge where badge_id = 3) highscore_place_3_count,
(select count(*) from kort.user_badge where badge_id = 4) total_fix_count_100_count,
(select count(*) from kort.user_badge where badge_id = 5) total_fix_count_50_count,
(select count(*) from kort.user_badge where badge_id = 6) total_fix_count_10_count,
(select count(*) from kort.user_badge where badge_id = 7) total_fix_count_1_count,
(select count(*) from kort.user_badge where badge_id = 8) fix_count_motorway_ref_100_count,
(select count(*) from kort.user_badge where badge_id = 9) fix_count_motorway_ref_50_count,
(select count(*) from kort.user_badge where badge_id = 10) fix_count_motorway_ref_5_count,
(select count(*) from kort.user_badge where badge_id = 11) fix_count_religion_100_count,
(select count(*) from kort.user_badge where badge_id = 12) fix_count_religion_50_count,
(select count(*) from kort.user_badge where badge_id = 13) fix_count_religion_5_count,
(select count(*) from kort.user_badge where badge_id = 14) fix_count_poi_name_100_count,
(select count(*) from kort.user_badge where badge_id = 15) fix_count_poi_name_50_count,
(select count(*) from kort.user_badge where badge_id = 16) fix_count_poi_name_5_count,
(select count(*) from kort.user_badge where badge_id = 17) fix_count_missing_maxspeed_100_count,
(select count(*) from kort.user_badge where badge_id = 18) fix_count_missing_maxspeed_50_count,
(select count(*) from kort.user_badge where badge_id = 19) fix_count_missing_maxspeed_5_count,
(select count(*) from kort.user_badge where badge_id = 20) fix_count_language_unknown_100_count,
(select count(*) from kort.user_badge where badge_id = 21) fix_count_language_unknown_50_count,
(select count(*) from kort.user_badge where badge_id = 22) fix_count_language_unknown_5_count,
(select count(*) from kort.user_badge where badge_id = 23) fix_count_missing_track_type_100_count,
(select count(*) from kort.user_badge where badge_id = 24) fix_count_missing_track_type_50_count,
(select count(*) from kort.user_badge where badge_id = 25) fix_count_missing_track_type_5_count,
(select count(*) from kort.user_badge where badge_id = 26) fix_count_way_wo_tags_100_count,
(select count(*) from kort.user_badge where badge_id = 27) fix_count_way_wo_tags_50_count,
(select count(*) from kort.user_badge where badge_id = 28) fix_count_way_wo_tags_5_count,
(select count(*) from kort.user_badge where badge_id = 29) fix_count_missing_cuisine_100_count,
(select count(*) from kort.user_badge where badge_id = 30) fix_count_missing_cuisine_50_count,
(select count(*) from kort.user_badge where badge_id = 31) fix_count_missing_cuisine_5_count,
(select count(*) from kort.user_badge where badge_id = 32) fix_count_missing_level_100_count,
(select count(*) from kort.user_badge where badge_id = 33) fix_count_missing_level_50_count,
(select count(*) from kort.user_badge where badge_id = 34) fix_count_missing_level_5_count,
(select count(*) from kort.user_badge where badge_id = 35) fix_count_opening_hours_100_count,
(select count(*) from kort.user_badge where badge_id = 36) fix_count_opening_hours_50_count,
(select count(*) from kort.user_badge where badge_id = 37) fix_count_opening_hours_5_count,
(select count(*) from kort.user_badge where badge_id = 38) six_per_day_count;

CREATE OR REPLACE VIEW kort.highscore_day AS
SELECT
  ROW_NUMBER() OVER(ORDER BY koin_count DESC) AS id,
  RANK() OVER(ORDER BY koin_count DESC) AS rank,
  user_id,
  username,
  fix_count AS mission_count,
  koin_count
FROM
  (
    SELECT
      u.user_id,
      u.username,
      (SELECT SUM(fix_koin_count) AS count
       FROM kort.fix f
       WHERE (f.user_id = u.user_id AND f.create_date::DATE >= current_date)) AS koin_count,
      (SELECT Count(1) AS count
       FROM kort.fix f
       WHERE (f.user_id = u.user_id AND f.create_date::DATE >= current_date)) AS fix_count
    FROM kort.user u
    WHERE (u.username IS NOT NULL)
  ) AS score
  WHERE koin_count IS NOT NULL
  ORDER BY koin_count DESC
;


CREATE OR REPLACE VIEW kort.highscore_week AS
SELECT
  ROW_NUMBER() OVER(ORDER BY koin_count DESC) AS id,
  RANK() OVER(ORDER BY koin_count DESC) AS rank,
  user_id,
  username,
  fix_count AS mission_count,
  koin_count
FROM
  (
    SELECT
      u.user_id,
      u.username,
      (SELECT SUM(fix_koin_count) AS count
       FROM kort.fix f
       WHERE (f.user_id = u.user_id AND f.create_date::DATE >= current_date-6)) AS koin_count,
      (SELECT Count(1) AS count
       FROM kort.fix f
       WHERE (f.user_id = u.user_id AND f.create_date::DATE >= current_date-6)) AS fix_count
    FROM kort.user u
    WHERE (u.username IS NOT NULL)
  ) AS score
  WHERE koin_count IS NOT NULL
  ORDER BY koin_count DESC
;

CREATE OR REPLACE VIEW kort.highscore_month AS
SELECT
  ROW_NUMBER() OVER(ORDER BY koin_count DESC) AS id,
  RANK() OVER(ORDER BY koin_count DESC) AS rank,
  user_id,
  username,
  fix_count AS mission_count,
  koin_count
FROM
  (
    SELECT
      u.user_id,
      u.username,
      (SELECT SUM(fix_koin_count) AS count
       FROM kort.fix f
       WHERE (f.user_id = u.user_id AND f.create_date::DATE >= current_date-30)) AS koin_count,
      (SELECT Count(1) AS count
       FROM kort.fix f
       WHERE (f.user_id = u.user_id AND f.create_date::DATE >= current_date-30)) AS fix_count
    FROM kort.user u
    WHERE (u.username IS NOT NULL)
  ) AS score
  WHERE koin_count IS NOT NULL
  ORDER BY koin_count DESC
;

CREATE OR REPLACE VIEW kort.highscore_all_time AS
SELECT
  ROW_NUMBER() OVER(ORDER BY koin_count DESC) AS id,
  RANK() OVER(ORDER BY koin_count DESC) AS rank,
  user_id,
  username,
  fix_count AS mission_count,
  koin_count
FROM
  (
    SELECT
      u.user_id,
      u.username,
      (SELECT SUM(fix_koin_count) AS count
       FROM kort.fix f
       WHERE f.user_id = u.user_id ) AS koin_count,
      (SELECT Count(1) AS count
       FROM kort.fix f
       WHERE f.user_id = u.user_id ) AS fix_count
    FROM kort.user u
    WHERE (u.username IS NOT NULL)
  ) AS score
  WHERE koin_count IS NOT NULL
  ORDER BY koin_count DESC
;
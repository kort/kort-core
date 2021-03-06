import logging
from connexion import NoContent
from flask import request
from geoalchemy2 import WKTElement
import osmapi
import traceback
import api.models
from sqlalchemy import func
import datetime

from sqlalchemy import tuple_
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db_session = api.models.init_db()


def get_missions(lat, lon, radius, limit, lang, user_id):
    try:
        location = WKTElement('POINT('+str(lon)+' '+str(lat)+')', srid=4326)
        no_of_errors = 10

        # get already solved error ids
        already_solved = db_session.query(api.models.Solution.error_id). \
            filter(api.models.Solution.user_id == user_id)

        # get nearest neighbors candidates from location
        q = db_session.query(api.models.kort_errors.schema, api.models.kort_errors.errorId) \
            .filter((~api.models.kort_errors.errorId.in_(already_solved))) \
            .order_by(api.models.kort_errors.geom.distance_centroid(location)) \
            .limit(limit*no_of_errors).subquery()

        # partition by error type
        q = db_session.query(api.models.kort_errors, func.row_number().over(
                partition_by=api.models.kort_errors.error_type).label("row_number")) \
            .filter(tuple_(api.models.kort_errors.schema, api.models.kort_errors.errorId).in_(q))\
            .filter(func.ST_DistanceSphere(api.models.kort_errors.geom, location) < radius).subquery()

        # set max errors of each type
        q = db_session.query(api.models.kort_errors).select_entity_from(q).filter(q.c.row_number <= limit/no_of_errors)

    except Exception as e:
        logger.error(traceback.format_exc())
    return [p.dump(lang) for p in q][:limit]


def put_mission_solution(schema_id, error_id, body):
    s = body['solution']
    user_id = s['userId']
    secret = request.headers.get('Authorization')
    user = db_session.query(api.models.User).filter(api.models.User.id == user_id). \
        filter(api.models.User.secret == secret).one_or_none()
    if not user:
        return NoContent, 401
    try:
        q = db_session.query(api.models.kort_errors).filter(api.models.kort_errors.errorId == error_id).filter(
            api.models.kort_errors.schema == schema_id)

        answer = s['value']
        solved = s['solved']
        lang = s['lang']
        if s['option']:
            answer = s['option']

        if q.count() == 1:
            error = q.first()
            error_type = error.error_type
            koins = error.fix_koin_count
            if s['stats_enabled']:
                koins += 1

            # write solution to db
            new_solution = api.models.Solution(
                userId=user_id,
                create_date=datetime.datetime.utcnow(),
                error_id=error_id,
                error_type=error_type,
                koin_count=koins if solved else 0,
                schema=schema_id,
                osmId=s['osm_id'],
                solution=answer,
                complete=False,
                valid=solved)
            db_session.add(new_solution)
            db_session.commit()

            # get new badges for this user if solved
            return create_new_achievements(user_id=user_id, lang=lang, mission_type=error_type) if solved else []
        else:
            return NoContent, 404
    except SQLAlchemyError as e:
        logger.error(traceback.format_exc())
        db_session.rollback()
        return NoContent, 404


def create_new_achievements(user_id, lang, mission_type):
    all_new_badges = []
    # get user badges
    user_badge_ids = db_session.query(api.models.UserBadge.badge_id).filter(api.models.UserBadge.user_id == user_id)

    # get no of missions in general
    q = db_session.query(api.models.Solution).filter(api.models.Solution.user_id == user_id)
    no_of_missions = q.count()
    all_new_badges.extend(
        get_not_achieved_badges_no_of_missions(user_badge_ids=user_badge_ids, no_of_missions=no_of_missions))

    # no of mission for this type of mission
    q = db_session.query(api.models.Solution).filter(api.models.Solution.user_id == user_id).\
        filter(api.models.Solution.error_type == mission_type)
    no_of_missions_type = q.count()
    all_new_badges.extend(
        get_not_achieved_badges_type_of_mission(user_badge_ids=user_badge_ids, no_of_missions_type=no_of_missions_type,
                                                mission_type=mission_type))

    # per day achievements
    q = db_session.query(func.count('*')).filter(api.models.Solution.user_id == user_id).\
        group_by(func.to_char(api.models.Solution.create_date, "DD.MM.YYYY"))
    if len(q.all()) != 0:
        max_number_of_missions_per_day = max(q.all())[0]
        if (max_number_of_missions_per_day == 6):
            new_badge = db_session.query(api.models.Badge).\
            filter(api.models.Badge.name.like('six_per_day')).all()
            all_new_badges.extend(new_badge)

    # highscore achievements
    q_highscore = db_session.query(api.models.Highscore).filter(api.models.Highscore.user_id == user_id).first()
    if q_highscore:
        rank = q_highscore.rank
        if rank >= 1 and rank <= 3:
            all_new_badges.extend(
                get_not_achieved_badges_highscore(user_badge_ids=user_badge_ids, rank=rank))

    for row in all_new_badges:
        logger.debug('new achievement '+row.title)

    # insert badges
    badgesAchieved = []
    for badge in all_new_badges:
        db_session.add(
            api.models.UserBadge(user_id=user_id, badge_id=badge.id, create_date=datetime.datetime.utcnow())
        )
        badgesAchieved.append(badge.dump(language=lang,  achieved=True, achievementDate=datetime.datetime.utcnow()))

    db_session.commit()

    return badgesAchieved


def get_not_achieved_badges_no_of_missions(user_badge_ids, no_of_missions):
    new_badges = db_session.query(api.models.Badge).\
        filter(api.models.Badge.name.like('total_fix_count_%')).\
        filter(api.models.Badge.compare_value <= no_of_missions).\
        filter(~api.models.Badge.id.in_(user_badge_ids)).all()
    return new_badges


def get_not_achieved_badges_type_of_mission(user_badge_ids, no_of_missions_type, mission_type):
    new_badges = db_session.query(api.models.Badge).\
        filter(api.models.Badge.name.like('fix_count_'+mission_type+'_%')).\
        filter(api.models.Badge.compare_value <= no_of_missions_type).\
        filter(~api.models.Badge.id.in_(user_badge_ids)).all()
    return new_badges


def get_not_achieved_badges_highscore(user_badge_ids, rank):
    new_badges = db_session.query(api.models.Badge). \
        filter(api.models.Badge.name.like('highscore_place_' + str(rank))). \
        filter(~api.models.Badge.id.in_(user_badge_ids)).all()
    return new_badges


def get_osm_geom(osm_type, osm_id):
    osm_api = osmapi.OsmApi()
    try:
        if osm_type == 'way':
            nodes = osm_api.WayFull(osm_id)
            ordered_node_list = []
            way_dict = {}
            way_order = []
            for item in nodes:
                if item.get('type') == 'node':
                    node = item.get('data')
                    lat = node.get('lat')
                    lon = node.get('lon')
                    way_dict[node.get('id')] = [lat, lon]
                elif item.get('type') == 'way':
                    way = item.get('data')
                    way_order = way.get('nd')
            for node_id in way_order:
                ordered_node_list.append(way_dict.get(node_id))
            return ordered_node_list
        elif osm_type == 'node':
            node = osm_api.NodeGet(osm_id)
            lat = node.get('lat')
            lon = node.get('lon')
            return [lat, lon]
        elif osm_type == 'relation':
            nodes = osm_api.RelationFull(osm_id)
            ordered_node_list = []
            way_dict = {}
            ways = {}
            members = []
            for item in nodes:
                if item.get('type') == 'node':
                    node = item.get('data')
                    lat = node.get('lat')
                    lon = node.get('lon')
                    way_dict[node.get('id')] = [lat, lon]
                elif item.get('type') == 'way':
                    way = item.get('data')
                    ways[way.get('id')] = way.get('nd')
                elif item.get('type') == 'relation':
                    relation = item.get('data')
                    members = relation.get('member')
            # choose only outer member since mapbox does not support multipolygons
            for rel_member in members:
                if rel_member.get('role') == 'outer': member = rel_member
            for node_id in ways.get(member.get('ref')):
                ordered_node_list.append(way_dict.get(node_id))
            return ordered_node_list
    except Exception as e:
        logger.error(traceback.format_exc())
        return []

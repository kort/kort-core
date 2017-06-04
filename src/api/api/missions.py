from connexion import NoContent
from geoalchemy2 import WKTElement
from sqlalchemy import Date, cast
import osmapi

import json
import traceback

import api.models
from sqlalchemy import func

import datetime
from datetime import date

db_session = api.models.init_db()

def get_missions(lat, lon, radius, limit, lang, user_id = -1):
    # print('get missions for language '+lang)
    # with open('data/missions.json') as json_data:
    #     d = json.load(json_data)
    #     return d
    try:
        location = WKTElement('POINT('+str(lon)+' '+str(lat)+')', srid=4326)

        already_solved = db_session.query(api.models.Solution.error_id). \
            filter(api.models.Solution.user_id == user_id)

        subquery = db_session.query(api.models.kort_errors) \
        .filter((~api.models.kort_errors.errorId.in_(already_solved))) \
        .order_by(api.models.kort_errors.geom.distance_centroid(location)) \
        .limit(limit).subquery()

        q = db_session.query(subquery.c.id)\
            .filter(func.ST_DistanceSphere(subquery.c.geom, location) < radius)


        q = db_session.query(api.models.kort_errors).filter(api.models.kort_errors.errorId.in_(q))


    except Exception as e:
        print(traceback.format_exc())
    return [p.dump(lang) for p in q][:limit]

def put_mission_solution(schema_id, error_id, lang, body):

    try:
        q = db_session.query(api.models.kort_errors).filter(api.models.kort_errors.errorId == error_id).filter(
            api.models.kort_errors.schema == schema_id)

        # 403 if user does not exist
        # TODO check if valid according to re,
        s = body['solution']

        user_id = s['userId']
        koins = s['koins']
        error_type = s['type']

        if q.count() == 1:
            # write solution to db
            new_solution = api.models.Solution(userId=user_id, create_date=datetime.datetime.utcnow(),
                                           error_id=error_id, error_type=error_type,
                                           koin_count=koins,
                                           schema=schema_id, osmId=s['osm_id'],
                                           solution=s['value'], complete=s['solved'],
                                           valid=True)
            db_session.add(new_solution)
            db_session.commit()


            # update koin count, mission count, missions today
            no_missions_today = db_session.query(api.models.Solution).\
                filter(api.models.Solution.user_id == user_id).\
                filter(cast(api.models.Solution.create_date,Date) == date.today()).\
                count()


            # get new badges for this user
            return create_new_achievements(user_id=user_id, solution=s, lang=lang, error=q.first())
        else:
            return NoContent, 404



    except Exception as e:
        print(traceback.format_exc())
        return '{}'


def create_new_achievements(user_id, solution, lang, error):
    all_new_badges = []
    # get user badges
    user_badge_ids = db_session.query(api.models.UserBadge.badge_id).filter(api.models.UserBadge.user_id == user_id)

    # get no of missions in general
    # no of missions
    q = db_session.query(api.models.Solution).filter(api.models.Solution.user_id == user_id)
    no_of_missions = q.count();
    print('no of missions', no_of_missions)

    all_new_badges.extend(
        get_not_achieved_badges_no_of_missions(user_badge_ids=user_badge_ids, no_of_missions=no_of_missions))


    # no of mission for this type of mission
    mission_type = error.type
    q = db_session.query(api.models.Solution).filter(api.models.Solution.user_id == user_id).\
        filter(api.models.Solution.error_type == mission_type)
    no_of_missions_type = q.count()
    all_new_badges.extend(
        get_not_achieved_badges_type_of_mission(user_badge_ids=user_badge_ids, no_of_missions_type=no_of_missions_type,
                                                type=mission_type))

    # per day achievements
    q = db_session.query(func.count('*')).filter(api.models.Solution.user_id == user_id).\
        group_by(func.to_char(api.models.Solution.create_date, "DD.MM.YYYY"))
    max_number_of_missions_per_day = max(q.all())[0]
    if (max_number_of_missions_per_day == 5):
        new_badge = db_session.query(api.models.Badge).\
        filter(api.models.Badge.name.like('5_per_day')).all()
        all_new_badges.extend(new_badge)


    # highscore achievements
    # TODO




    for row in all_new_badges:
        print(row.title)

    # insert badges
    badgesAchieved = []
    for badge in all_new_badges:
        db_session.add(
            api.models.UserBadge(user_id=user_id, badge_id=badge.id, create_date=datetime.datetime.utcnow())
        )
        badgesAchieved.append(badge.dump(lang, True, datetime.datetime.utcnow()))

    db_session.commit()

    return badgesAchieved


def get_not_achieved_badges_no_of_missions(user_badge_ids, no_of_missions):
    new_badges = db_session.query(api.models.Badge).\
        filter(api.models.Badge.name.like('fix_count_%')).\
        filter(api.models.Badge.compare_value <= no_of_missions).\
        filter(~api.models.Badge.id.in_(user_badge_ids)).all()
    return new_badges


def get_not_achieved_badges_type_of_mission(user_badge_ids, no_of_missions_type, type):
    new_badges = db_session.query(api.models.Badge).\
        filter(api.models.Badge.name.like('fix_count_'+type+'%')).\
        filter(api.models.Badge.compare_value <= no_of_missions_type).\
        filter(~api.models.Badge.id.in_(user_badge_ids)).all()
    return new_badges

def get_not_achieved_badges_highscore(user_badge_ids, no_of_mission_type, type):
    # TODO
    pass

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
        print(traceback.format_exc())
        return []
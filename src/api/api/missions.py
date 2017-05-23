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

def get_missions(lat, lon, radius, limit, lang):
    # print('get missions for language '+lang)
    # with open('data/missions.json') as json_data:
    #     d = json.load(json_data)
    #     return d
    try:
        location = WKTElement('POINT('+str(lon)+' '+str(lat)+')', srid=4326)

        subquery = db_session.query(api.models.kort_errors) \
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

        if q.count() == 1:
            # write solution to db
            new_solution = api.models.Solution(userId=user_id, create_date=datetime.datetime.utcnow(),
                                           error_id=error_id,
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


            db_session.query(api.models.User).filter_by(id=user_id)\
                .update({api.models.User.koin_count: api.models.User.koin_count + koins,
                         api.models.User.mission_count: api.models.User.mission_count + 1,
                         api.models.User.mission_count_today: no_missions_today})
            db_session.commit()


            # get new badges for this user
            return create_new_achievements(user_id=user_id, solution=s, lang=lang)
        else:
            return NoContent, 404



    except Exception as e:
        print(traceback.format_exc())
        return '{}'


def create_new_achievements(user_id, solution, lang):
    # no of missions
    q = db_session.query(api.models.Solution).filter(api.models.Solution.user_id == user_id)
    no_of_missions = q.count();
    print('no of missions', no_of_missions)

    # no of mission for this type of mission
    # TODO

    # no of missions within geometry
    # TODO

    # get user badges
    user_badge_ids = db_session.query(api.models.UserBadge.badge_id).filter(api.models.UserBadge.user_id == user_id)

    # get badges for different types which have not been achieved
    all_new_badges = []
    all_new_badges.extend(
        get_not_achieved_badges_no_of_missions(user_badge_ids=user_badge_ids, no_of_missions=no_of_missions))

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


def get_not_achieved_badges_type_of_mission(user_badge_ids, no_of_mission_type, type):
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
            # not yet implemented
            return []
    except Exception as e:
        print(traceback.format_exc())
        return []
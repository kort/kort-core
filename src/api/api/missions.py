from connexion import NoContent
from geoalchemy2 import Geometry
from sqlalchemy import func, Table, engine
import json
import traceback

import api.models
from src.api.i18n import I18n
import datetime

db_session = api.models.init_db()

def get_missions(lat, lon, radius, limit, lang):
    # print('get missions for language '+lang)
    # with open('data/missions.json') as json_data:
    #     d = json.load(json_data)
    #     return d
    try:
        locale = I18n.I18n()
        q = db_session.query(api.models.kort_errors)\
        .order_by(api.models.kort_errors.geom.distance_box('POINT(' + str(lon) + ' ' + str(lat) + ')')) \
        .limit(limit)
        # .filter(api.models.kort_errors.geom.ST_Distance_Sphere('POINT(' + str(lon) + ' ' + str(lat) + ')') < radius) \

    except Exception as e:
        print(traceback.format_exc())
    return [p.dump(locale.matchLanguage(lang)) for p in q][:limit]

def put_mission_solution(schema_id, error_id, solution):

    try:
        q = db_session.query(api.models.kort_errors).filter(api.models.kort_errors.errorId == error_id).filter(
            api.models.kort_errors.schema == schema_id)

        # TODO check if valid according to re,


        if q.count() == 1:
            solution = api.models.Solution(userId=solution['userId'], create_date=datetime.datetime.utcnow(),
                                           error_id=error_id,
                                           schema=schema_id, osmId=solution['osm_id'],
                                           solution=solution['value'], complete=solution['solved'],
                                           valid=True)
            db_session.add(solution)
            db_session.commit()

            # get new badges for this user
            #TODO
        else:
            return NoContent, 404



    except Exception as e:
        print(traceback.format_exc())

    with open('data/achievements.json') as json_data:
        d = json.load(json_data)
        return d
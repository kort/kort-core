from geoalchemy2 import Geometry
from sqlalchemy import func, Table, engine
import json
import traceback

import api.models
from src.api.i18n import I18n

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

def put_mission():
    pass
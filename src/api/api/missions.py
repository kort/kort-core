from geoalchemy2 import Geometry
from sqlalchemy import func, Table, engine
import json
import traceback

import api.models

db_session = api.models.init_db()

def get_mission(mission_id):
    return 'the mission'

def get_missions(lat, lon, radius, limit, lang):
    # print('get missions for language '+lang)
    # with open('data/missions.json') as json_data:
    #     d = json.load(json_data)
    #     return d
    try:
        # q = db_session.query(api.models.Mission)\
        #     .order_by(api.models.Mission.geom.distance_box('POINT('+str(lon)+' '+str(lat)+')'))\
        #     .limit(limit)
        # print([p.dump() for p in q][:limit])
        q = db_session.query(api.models.kort_errors)\
            .order_by(api.models.kort_errors.geom.distance_box('POINT(' + str(lon) + ' ' + str(lat) + ')'))\
            .limit(limit)
        for p in q:
            print(p.id, p.title, p.schema)
        print([p.dump() for p in q][:limit])

    except Exception as e:
        print(traceback.format_exc())
    return [p.dump() for p in q][:limit]
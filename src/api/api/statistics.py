import api

db_session = api.models.init_db()

def get_statistics():
    q = db_session.query(api.models.Statistics)
    return [p.dump() for p in q]

import json

import api

db_session = api.models.init_db()

def get_highscore(type, limit):
    # with open('data/highscore_'+type+'.json') as json_data:
    #     d = json.load(json_data)
    #     return d
    # return '{}'
    if type in 'day':
        q = db_session.query(api.models.HighscoreDay)
    elif type in 'week':
        q = db_session.query(api.models.HighscoreWeek)
    elif type in 'month':
        q = db_session.query(api.models.HighscoreMonth)
    else:
        q = db_session.query(api.models.Highscore)
    return [p.dump() for p in q][:limit]

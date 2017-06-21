import api

db_session = api.models.init_db()


def get_highscore(type, limit):
    if type in 'day':
        q = db_session.query(api.models.HighscoreDay)
    elif type in 'week':
        q = db_session.query(api.models.HighscoreWeek)
    elif type in 'month':
        q = db_session.query(api.models.HighscoreMonth)
    else:
        q = db_session.query(api.models.Highscore)
    return [p.dump() for p in q][:limit]

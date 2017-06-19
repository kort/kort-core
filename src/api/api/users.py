import datetime
import logging
from connexion import NoContent
from datetime import date

import api.models
from sqlalchemy import Date
from sqlalchemy import cast
from sqlalchemy import func

db_session = api.models.init_db()
from flask import request

def get_user(user_id):
    secret = request.headers.get('Authorization')
    user = db_session.query(api.models.User).filter(api.models.User.id == user_id). \
        filter(api.models.User.secret == secret).one_or_none()

    #get koin_count, mission_count_today and mission_count
    mission_count = db_session.query(api.models.Solution).filter(api.models.Solution.user_id == user_id)\
        .filter(api.models.Solution.valid).count()
    mission_count_today = db_session.query(api.models.Solution).filter(api.models.Solution.user_id == user_id)\
        .filter(api.models.Solution.valid)\
        .filter(cast(api.models.Solution.create_date, Date) == date.today()).count()
    koin_count = db_session.query(func.sum(api.models.Solution.koin_count)).filter(api.models.Solution.user_id == user_id).scalar()

    print(user)
    if user:
        return user.dump(mission_count=mission_count, mission_count_today=mission_count_today, koin_count=koin_count)
    return ('Unauthorized', 401)

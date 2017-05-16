import datetime
import logging
from connexion import NoContent
import api.models
db_session = api.models.init_db()
from flask import request

def get_user(user_id):
    secret = request.headers.get('Authorization')
    print('get user with', user_id, secret)
    user = db_session.query(api.models.User).filter(api.models.User.id == user_id). \
        filter(api.models.User.secret == secret).one_or_none()
    print(user)
    if user:
        return user.dump()
    return ('Unauthorized', 401)

import datetime
import logging
from connexion import NoContent
import api.models
db_session = api.models.init_db()
from flask import request

def get_users(limit, name=None):
    print('users')
    print('You are: {uid}'.format(uid=request.user))
    q = db_session.query(api.models.User)
    if name:
        q = q.filter(api.models.User.name == name)
    return [p.dump() for p in q][:limit]


def get_user(user_id):
    secret = request.headers.get('Authorization')
    print('get user with', user_id, secret)
    user = db_session.query(api.models.User).filter(api.models.User.id == user_id). \
        filter(api.models.User.secret == secret).one_or_none()
    print(user)
    if user:
        return user.dump()
    return ('Unauthorized', 401)


def put_user(user_id, user):
    p = db_session.query(api.models.User).filter(api.models.User.id == user_id).one_or_none()
    user['id'] = user_id
    if p is not None:
        logging.info('Updating user %s..', user_id)
        p.update(**user)
    else:
        logging.info('Creating user %s..', user_id)
        user['last_login'] = datetime.datetime.utcnow()
        db_session.add(api.models.User(**user))
    db_session.commit()
    return NoContent, (200 if p is not None else 201)


def delete_user(user_id):
    user = db_session.query(api.models.User).filter(api.models.User.id == user_id).one_or_none()
    if user is not None:
        logging.info('Deleting user %s..', user_id)
        db_session.query(api.models.User).filter(api.models.User.id == user_id).delete()
        db_session.commit()
        return NoContent, 204
    else:
        return NoContent, 404

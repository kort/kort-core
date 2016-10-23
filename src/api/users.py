import datetime
import logging
from connexion import NoContent
import models
db_session = models.init_db()

def get_users(limit, name=None):
    q = db_session.query(models.User)
    if name:
        q = q.filter(models.User.name == name)
    return [p.dump() for p in q][:limit]


def get_user(user_id):
    user = db_session.query(models.User).filter(models.User.id == user_id).one_or_none()
    return user.dump() or ('Not found', 404)


def put_user(user_id, user):
    p = db_session.query(models.User).filter(models.User.id == user_id).one_or_none()
    user['id'] = user_id
    if p is not None:
        logging.info('Updating user %s..', user_id)
        p.update(**user)
    else:
        logging.info('Creating user %s..', user_id)
        user['last_login'] = datetime.datetime.utcnow()
        db_session.add(models.User(**user))
    db_session.commit()
    return NoContent, (200 if p is not None else 201)


def delete_user(user_id):
    user = db_session.query(models.User).filter(models.User.id == user_id).one_or_none()
    if user is not None:
        logging.info('Deleting user %s..', user_id)
        db_session.query(models.User).filter(models.User.id == user_id).delete()
        db_session.commit()
        return NoContent, 204
    else:
        return NoContent, 404
#!/usr/bin/env python3
import logging
from api import models

db_session = models.init_db()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_tokeninfo(access_token: str) -> dict:
    uid = get_user_by_secret(access_token)
    if not uid:
        return 'No such token', 401
    return {'uid': uid, 'scope': ['uid']}


def get_user_by_secret(secret: str):
    user = db_session.query(models.User).filter(models.User.secret == secret).one_or_none()
    logger.info('get user token with id '+str(user.id))
    return user.id

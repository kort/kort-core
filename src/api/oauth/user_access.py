import uuid

import api.models
db_session = api.models.init_db()
import datetime
import json
import logging


def get_user_secret(provider: str, id: str) -> object:
    user = db_session.query(api.models.User).filter(api.models.User.oauth_user_id == id).filter(api.models.User.oauth_provider == provider).one_or_none()
    return user


def update_user(provider: str, secret: str, data: str):
    if provider is 'google':
        user = db_session.query(api.models.User).filter(api.models.User.secret == secret).one_or_none()
        user.pic_url = data.get('picture', user.pic_url)
        user.name = data.get('given_name', user.name)
        user.username = data.get('name', user.name)
        user.email = data.get('email', user.username)
        user.last_login = datetime.datetime.utcnow()
        db_session.commit()
    if provider is 'osm':
        user = db_session.query(api.models.User).filter(api.models.User.secret == secret).one_or_none()
        d = json.loads(data)
        user.pic_url = d.get('img', '')
        user.name = d.get('display_name', '')
        user.username = d.get('display_name', '')
        user.last_login = datetime.datetime.utcnow()
        db_session.commit()
    return user


def create_user(provider: str, data: str, token: str) -> str:
    if provider is 'google':
        secret = generate_secret()
        print('data', data, token)
        try:
            user = api.models.User(name=data.get('given_name', ''), username=data.get('name', ''), email=data.get('email', ''), oauth_provider=provider,
                                   oauth_user_id=data.get('sub', ''), pic_url=data.get('picture', ''), secret=secret, token=token)
            print(user)
            db_session.add(user)
            db_session.commit()
        except Exception as e:
            logging.exception("message")
    if provider is 'osm':
        d = json.loads(data)
        secret = generate_secret()
        user = api.models.User(name=d['display_name'], username=d['display_name'], oauth_provider=provider,
                               oauth_user_id=d['id'], pic_url=d.get('img', ''), secret=secret, token=token)
        db_session.add(user)
        db_session.commit()
    return user


def generate_secret() -> str:
    return uuid.uuid4()


import api.models
db_session = api.models.init_db()
import datetime
import json

def get_user_secret(provider: str, id: str) -> object:
    user = db_session.query(api.models.User).filter(api.models.User.oauth_user_id == id).filter(api.models.User.oauth_provider == provider).one_or_none()
    return user

def update_user(provider: str, secret: str, data: str):
    #TODO token also to be updated?
    if provider is 'google':
        user = db_session.query(api.models.User).filter(api.models.User.secret == secret).one_or_none()
        user.pic_url = data['picture']
        user.name = data['name']
        user.username = data['email']
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
    return None


def create_user(provider: str, data: str, token: str) -> str:
    if provider is 'google':
        secret = generate_secret()
        user = api.models.User(data['name'], data['email'], provider, data['id'], data['picture'], secret, token)
        db_session.add(user)
        db_session.commit()
    if provider is 'osm':
        d = json.loads(data)
        secret = generate_secret()
        user = api.models.User(d['display_name'], d['display_name'], provider, d['id'], d.get('img', ''), secret, token)
        db_session.add(user)
        db_session.commit()
    return secret

def generate_secret() -> str:
    return 'the_super_secret'+datetime.datetime.utcnow().strftime('%Y-%m-%d%H:%M:%S.%f')[:-3]


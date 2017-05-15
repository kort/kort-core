from api import models

db_session = models.init_db()

def get_tokeninfo(access_token: str) -> dict:
    uid = get_user_by_secret(access_token)
    if not uid:
        return 'No such token', 401
    return {'uid': uid, 'scope': ['uid']}

def get_user_by_secret(secret: str):
    user = db_session.query(models.User).filter(models.User.secret == secret).one_or_none()
    print(user.user_id)
    return user.user_id
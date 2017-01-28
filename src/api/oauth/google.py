from flask import Blueprint, redirect, url_for, session, request, jsonify
from flask_oauthlib.client import OAuth
import requests

google_oauth_provider = Blueprint('google_oauth_provider', __name__)


from app import app
from . import user_access
from config.config import BaseConfig

oauth = OAuth(app.app)

google = oauth.remote_app(
    'google',
    consumer_key= BaseConfig.GOOGLE_ID,
    consumer_secret= BaseConfig.GOOGLE_SECRET,
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)
verifyURL = 'https://www.googleapis.com/oauth2/v3/tokeninfo'


@google_oauth_provider.route('/google/verify', methods=['POST'])
def verifyUserId():
    print(request)
    token = request.get_json().get('tokenId')
    print(token)
    payload = {'id_token': token}
    req = requests.get(verifyURL, payload)
    data = req.json()
    print(data)
    id = data['sub']
    print(data)
    user = user_access.get_user_secret('google', id)
    if user:
        # update user details
        print('update')
        user_access.update_user('google', user.secret, data)
        print('user ', user.id, 'secret ', user.secret)
    else:
        print('create')
        user = user_access.create_user('google', data, payload['id_token'])
    return jsonify(userId=user.id, secret=user.secret)


@google_oauth_provider.route('/google/login')
def login():
    return google.authorize(callback=url_for('.authorized', _external=True))


@google_oauth_provider.route('/google/login/authorized')
def authorized():
    resp = google.authorized_response()
    print(resp)
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )

    #check if user exists or create a new one
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    user = user_access.get_user_secret('google', me.data['id'])
    if user:
        # update user details
        secret = user.secret
        user_access.update_user('google', secret, me.data)
        print('updated')
    else:
        secret = user_access.create_user('google',me.data, get_google_oauth_token()[0])
    return jsonify({"secret": secret})

@google.tokengetter
def get_google_oauth_token():
    print(session.get('google_token'))
    return session.get('google_token')





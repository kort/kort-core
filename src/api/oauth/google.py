import logging
from flask import Blueprint, redirect, url_for, session, request, jsonify
from flask_oauthlib.client import OAuth
import requests

google_oauth_provider = Blueprint('google_oauth_provider', __name__)

from app import app
from . import user_access
from config.config import BaseConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
def verify_user_id():
    token = request.get_json().get('tokenId')
    payload = {'id_token': token}
    req = requests.get(verifyURL, payload)
    data = req.json()
    id = data['sub']
    email = data['email']
    user = user_access.get_user_secret('google', id)
    user_by_mail = user_access.get_user_secret_by_mail('google', email)
    logger.debug(' user'+str(id)+'verified')
    if user:
        # update user details
        logger.debug('update user')
        user_access.update_user('google', user.secret, data)
    elif user_by_mail:
        user = user_by_mail
        logger.debug('update user')
        user_access.update_user('google', user.secret, data)
    else:
        logger.debug('create user')
        user = user_access.create_user('google', data, payload['id_token'])
    return jsonify(id=user.id, secret=user.secret)


@google_oauth_provider.route('/google/login')
def login():
    return google.authorize(callback=url_for('.authorized', _external=True))


@google_oauth_provider.route('/google/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        logger.error('google resp failed'+str(request))
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )

    # check if user exists or create a new one
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    user = user_access.get_user_secret('google', me.data['id'])
    user_by_mail = user_access.get_user_secret_by_mail('google', me.data['email'])
    if user:
        # update user details
        secret = user.secret
        user_access.update_user('google', secret, me.data)
    elif user_by_mail:
        user = user_by_mail
        secret = user.secret
        user_access.update_user('google', user.secret, me.data)
    else:
        secret = user_access.create_user('google',me.data, get_google_oauth_token()[0])
    return jsonify({"secret": secret})


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')





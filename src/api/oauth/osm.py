from flask import Blueprint, redirect, url_for, session, request, jsonify
from flask_oauthlib.client import OAuth
import requests
from requests_oauthlib import OAuth1
from xml.etree import ElementTree
import json

osm_oauth_provider = Blueprint('osm_oauth_provider', __name__)

from app import app
from . import user_access
from config.config import BaseConfig


oauth = OAuth(app.app)

osm = oauth.remote_app(
    'remote',
    consumer_key=BaseConfig.OSM_CONSUMER_KEY,
    consumer_secret=BaseConfig.OSM_CONSUMER_SECRET,
    base_url='http://www.kort.ch',
    request_token_url='https://www.openstreetmap.org/oauth/request_token',
    access_token_method='GET',
    access_token_url='https://www.openstreetmap.org/oauth/access_token',
    authorize_url='https://www.openstreetmap.org/oauth/authorize',
)


@osm_oauth_provider.route('/osm/login')
def home():
    if 'example_oauth' in session:
        resp = osm.get('me')
        return jsonify(resp.data)
    return osm.authorize(callback=url_for('.authorized', _external=True))


@osm_oauth_provider.route('/osm/login/authorized')
@osm.authorized_handler
def authorized(resp):
    if resp is None:
        return 'Access denied: error=%s' % (
            request.args['error']
        )
    if 'oauth_token' in resp:
        session['example_oauth'] = resp
        # return jsonify(resp)
        userinfo = getUserInfo(session['example_oauth'])
        user = user_access.get_user_secret('osm', userinfo['id'])
        if user:
            # update user details
            secret = user.secret
            user_access.update_user('osm', secret,  json.dumps(userinfo))
            print('updated')
        else:
            secret = user_access.create_user('osm', json.dumps(userinfo), userinfo['oauth_token'])
        return jsonify({"secret": secret})
    return str(resp)


@osm.tokengetter
def example_oauth_token():
    if 'example_oauth' in session:
        resp = session['example_oauth']
        return resp['oauth_token'], resp['oauth_token_secret']


def getUserInfo(data) -> object:
    oauth_token = data.get('oauth_token')
    oauth_token_secret = data.get('oauth_token_secret')

    userinfo = {}
    userinfo['oauth_token'] = oauth_token
    userinfo['oauth_token_secret'] = oauth_token_secret

    url = "http://api.openstreetmap.org/api/0.6/user/details"
    auth = OAuth1(BaseConfig.OSM_CONSUMER_KEY, BaseConfig.OSM_CONSUMER_SECRET, oauth_token, oauth_token_secret)
    resp = requests.get(url, auth=auth)

    tree = ElementTree.fromstring(resp.content)
    for child in tree:
        if child.tag == 'user':
            userinfo['display_name'] = child.attrib.get('display_name')
            userinfo['id'] = child.attrib.get('id')
            for innerChild in child:
                if innerChild.tag == 'img':
                    userinfo['img'] = innerChild.attrib.get('href')
    return userinfo

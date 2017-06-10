#!/usr/bin/env python3
import os
import sys

from api import models, users, missions, highscores

import connexion
from config.config import BaseConfig

db_session = models.init_db()
app = connexion.App(__name__)
app.add_api('swagger.yaml')
application = app.app

application.debug = True
application.secret_key = 'development'

# Google OAuth blueprint
from oauth.google import google_oauth_provider
application.register_blueprint(google_oauth_provider)

# OpenStreetMap OAuth blueprint
from oauth.osm import osm_oauth_provider
application.register_blueprint(osm_oauth_provider)



@application.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run()
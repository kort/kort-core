#!/usr/bin/env python3

import connexion
import models
import users
import answers
import missions
import highscores

db_session = models.init_db()
app = connexion.App(__name__)
app.add_api('swagger.yaml')

application = app.app


@application.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run()

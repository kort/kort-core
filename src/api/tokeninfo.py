#!/usr/bin/env python3
import connexion

from tokeninfo import tokenAccess
from config.config import BaseConfig

if __name__ == '__main__':
    app = connexion.App(__name__)
    app.add_api('tokeninfo.yaml')
    app.run(port=7979,host=BaseConfig.TOKENINFO_HOST)

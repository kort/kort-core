import os
import sys

from sqlalchemy import Column, DateTime, String, Integer, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


try:
    from config.config import BaseConfig
except ImportError:
    from api.config.config import BaseConfig

import datetime

Base = declarative_base()

class User(Base):

    __tablename__ = 'user'

    id                  = Column(Integer, primary_key=True)
    mission_count       = Column(Integer, nullable=False)
    koin_count          = Column(Integer, nullable=False)
    name                = Column(String, nullable=False)
    username            = Column(String, nullable=False)
    oauth_provider      = Column(String, nullable=False)
    oauth_user_id       = Column(String, nullable=False)
    pic_url             = Column(String, nullable=True)
    secret              = Column(String, nullable=True)
    token               = Column(String, nullable=True)
    logged_in           = Column(Boolean, nullable=False)
    last_login          = Column(DateTime, nullable=False)

    def __init__(self, name, username, oauth_provider, oauth_user_id, pic_url, secret, token):
        self.mission_count = 0
        self.koin_count = 0
        self.name = name
        self.username = username
        self.oauth_provider = oauth_provider
        self.oauth_user_id = oauth_user_id
        self.pic_url = pic_url
        self.secret = secret
        self.token = token
        self.logged_in = True
        self.last_login = datetime.datetime.utcnow()


    def update(self, id=None, name=None, username=None,
               last_login=None, pic_url=None, token=None,
               logged_in=None, secret=None, oauth_provider=None,
               oauth_user_id=None, mission_count=None, koin_count=None):
        if name is not None:
            self.name = name
        if username is not None:
            self.username = username
        if last_login is not None:
            self.last_login = last_login

    def dump(self):
        return dict([(k, v) for k, v in vars(self).items() if not k.startswith('_')])

def init_db():
    engine = create_engine(BaseConfig.SQLALCHEMY_DATABASE_URI, convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)
    return db_session
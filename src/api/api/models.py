from sqlalchemy import Column, DateTime, String, Integer, BigInteger, Boolean, create_engine, UniqueConstraint, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from geoalchemy2 import Geometry

from config.config import BaseConfig

import datetime

from src.api.i18n import I18n

from .MissionTypeLoader import MissionTypeLoader

Base = declarative_base()


def init_db():
    engine = create_engine(BaseConfig.SQLALCHEMY_DATABASE_URI, convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)
    return db_session


class User(Base):

    __tablename__ = 'user'
    __table_args__ = {'schema': 'kort'}

    id                  = Column('user_id', Integer, primary_key=True)
    secret              = Column(String, nullable=False, unique=True)
    koin_count          = Column(Integer, nullable=False)
    name                = Column(String, nullable=False)
    username            = Column(String, nullable=False)
    oauth_provider      = Column(String, nullable=False)
    oauth_user_id       = Column(String, nullable=False)
    pic_url             = Column(String, nullable=True)
    token               = Column(String, nullable=True)
    mission_count       = Column(Integer, nullable=False)
    mission_count_today = Column(Integer, nullable=False)
    logged_in           = Column(Boolean, nullable=False)
    last_login          = Column(DateTime, nullable=False)
    UniqueConstraint(oauth_provider, oauth_user_id, name='unique_oauth_user')

    def __init__(self, name, username, oauth_provider, oauth_user_id, pic_url, secret, token):
        self.mission_count = 0
        self.mission_count_today = 0
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

    def dump(self):
        return dict([(k, v) for k, v in vars(self).items() if not k.startswith('_')])

    def __str__(self):
        return str(self.dump())


class kort_errors(Base):

    __table_args__ = {'schema': 'kort'}
    __tablename__ = 'errors'

    errorId                  = Column('id', Integer, primary_key=True)
    schema                  = Column(String, primary_key=False)
    type                    = Column(String, primary_key=False)
    osmId                   = Column('osm_id', BigInteger, primary_key=False)
    osmType                 = Column('osm_type', String, primary_key=False)
    question                 = Column('description', String, primary_key=False)
    title                   = Column(String, primary_key=False)
    view_type               = Column(String, primary_key=False)
    answer_placeholder      = Column(String, primary_key=False)
    fix_koin_count          = Column(Integer, primary_key=False)
    geom                    = Column(Geometry, nullable=False)
    latitude                = Column(Numeric, primary_key=False)
    longitude               = Column(Numeric, primary_key=False)
    txt1                   = Column(String, primary_key=False)
    txt2                   = Column(String, primary_key=False)
    txt3                   = Column(String, primary_key=False)
    txt4                   = Column(String, primary_key=False)
    txt5                   = Column(String, primary_key=False)

    def dump(self, language):
        d = dict([(k, v) for k, v in vars(self).items() if not k.startswith('_') and not k == 'geom'])
        locale = I18n.I18n()
        lang = locale.matchLanguage(language)
        print(d)
        d['id'] = 's'+d['schema']+'id'+str(d['errorId'])
        print('ok')
        d['annotationCoordinate'] = [float(d.pop('latitude')), float(d.pop('longitude'))]
        d['geomType'] = 'point' if d['osmType'] == 'node' else 'line'
        d['koinReward'] = d.pop('fix_koin_count')


        d['question'] = locale.translateQuestion(lang, d['question'], d.pop('txt1'), d.pop('txt2'), d.pop('txt3'), d.pop('txt4'), d.pop('txt5'))
        d['title'] = locale.translate(lang, d['title'])

        metda = MissionTypeLoader()
        d['inputType'] = metda.getInputType(lang, d['type'], d.pop('view_type'))
        d['image'] = metda.getImage(d['type'])

        return d


class Answer(Base):

    __table_args__ = {'schema': 'kort'}
    __tablename__ = 'select_answer'

    id                      = Column(Integer, primary_key=True)
    type                    = Column(String, primary_key=False)
    value                    = Column(String, primary_key=False)
    title                    = Column(String, primary_key=False)
    sorting                    = Column(Integer, primary_key=False)


class Solution(Base):

    __table_args__ = {'schema': 'kort'}
    __tablename__ = 'fix'

    id                         = Column('fix_id', Integer, primary_key=True)
    user_id                    = Column(Integer, primary_key=False)
    create_date                = Column(DateTime, nullable=False)
    error_id                   = Column(Integer, primary_key=False)
    schema                     = Column(String, primary_key=False)
    osmId                      = Column('osm_id', BigInteger, primary_key=False)
    solution                   = Column('message',String, primary_key=False)
    complete                   = Column(Boolean, nullable=False)
    valid                      = Column(Boolean, nullable=False)
    in_osm                     = Column(Boolean, nullable=False)

    def __init__(self, userId, create_date, error_id, schema, osmId, solution, complete, valid):
        self.user_id = userId
        self.create_date = create_date
        self.error_id = error_id
        self.schema = schema
        self.osmId = osmId
        self.solution = solution
        self.complete = complete
        self.in_osm = False
        self.valid = valid

class Badge(Base):

    __table_args__ = {'schema': 'kort'}
    __tablename__ = 'badge'

    id                         = Column('badge_id', Integer, primary_key=True)
    name                       = Column (String, primary_key=False)
    title                      = Column (String, primary_key=False)
    compare_value              = Column (Integer, primary_key=False)
    description                = Column (String, primary_key=False)
    sorting                    = Column (Integer, primary_key=False)

    def dump(self, language, achieved, achievementDate):
        d = dict([(k, v) for k, v in vars(self).items() if not k.startswith('_')])
        locale = I18n.I18n()
        lang = locale.matchLanguage(language)

        d['achievementDate'] = achievementDate
        d['achievementTitle'] = locale.translate(lang, d.pop('title'))
        d['achieved'] = achieved
        d['achievementId'] = d.pop('id')
        d['achievementImageURI'] = d.pop('name')
        d['achievementDescription'] = locale.translate(lang, d.pop('description'))
        return d



class UserBadge(Base):

    __table_args__ = {'schema': 'kort'}
    __tablename__ = 'user_badge'

    user_id                    = Column('user_id', Integer, primary_key=True)
    badge_id                   = Column('badge_id', Integer, primary_key=True)
    create_date                = Column(DateTime, nullable=False)


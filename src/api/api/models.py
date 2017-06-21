#!/usr/bin/env python3
import logging
from sqlalchemy import Column, DateTime, String, Integer, BigInteger, Boolean, create_engine, UniqueConstraint, Numeric
from sqlalchemy import ForeignKey
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from geoalchemy2 import Geometry

from config.config import BaseConfig

import datetime

from sqlalchemy.sql.ddl import CreateSchema, DDL

from i18n import I18n

from .MissionTypeLoader import MissionTypeLoader

Base = declarative_base()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db():
    engine = create_engine(BaseConfig.SQLALCHEMY_DATABASE_URI, convert_unicode=True)

    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    Base.query = db_session.query_property()
    event.listen(Base.metadata, 'before_create', DDL("CREATE SCHEMA IF NOT EXISTS kort"))
    Base.metadata.create_all(bind=engine)
    return db_session


class User(Base):

    __tablename__ = 'user'
    __table_args__ = {'schema': 'kort'}

    id                  = Column('user_id', Integer, primary_key=True)
    secret              = Column(String, nullable=False, unique=True)
    name                = Column(String, nullable=False)
    username            = Column(String, nullable=False)
    email               = Column(String, nullable=False)
    oauth_provider      = Column(String, nullable=False)
    oauth_user_id       = Column(String, nullable=False)
    pic_url             = Column(String, nullable=True)
    token               = Column(String, nullable=True)
    loggedIn           = Column('logged_in', Boolean, nullable=False)
    last_login          = Column(DateTime, nullable=False)
    UniqueConstraint(oauth_provider, oauth_user_id, name='unique_oauth_user')

    def __init__(self, name, username, email, oauth_provider, oauth_user_id, pic_url, secret, token):
        self.name = name
        self.username = username
        self.email = email
        self.oauth_provider = oauth_provider
        self.oauth_user_id = oauth_user_id
        self.pic_url = pic_url
        self.secret = secret
        self.token = token
        self.loggedIn = True
        self.last_login = datetime.datetime.utcnow()

    def dump(self, mission_count=0, mission_count_today=0, koin_count=0):
        d = dict([(k, v) for k, v in vars(self).items() if not k.startswith('_')])
        d['mission_count'] = mission_count
        d['mission_count_today'] = mission_count_today
        d['koin_count'] = koin_count
        return d

    def __str__(self):
        return str(self.dump())


class kort_errors(Base):

    __table_args__ = {'schema': 'kort'}
    __tablename__ = 'errors'

    errorId                  = Column('id', Integer, primary_key=True)
    schema                  = Column(String, primary_key=False)
    error_type              = Column('type', String, primary_key=False)
    osmId                   = Column('osm_id', BigInteger, primary_key=False)
    osmType                 = Column('osm_type', String, primary_key=False)
    question                 = Column('description', String, primary_key=False)
    title                   = Column(String, primary_key=False)
    view_type               = Column(String, primary_key=False)
    answer_placeholder      = Column(String, primary_key=False)
    fix_koin_count          = Column(Integer, primary_key=False)
    vote_koin_count          = Column(Integer, primary_key=False)
    image                   = Column(String, primary_key=False)
    constraint_re_description = Column(String, primary_key=False)
    constraint_re           = Column(String, primary_key=False, nullable=True)
    constraint_lower_bound  = Column(Integer, primary_key=False, nullable=True)
    constraint_upper_bound  = Column(Integer, primary_key=False, nullable=True)
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
        d['id'] = 's'+d['schema']+'id'+str(d['errorId'])
        d['annotationCoordinate'] = [float(d.pop('latitude')), float(d.pop('longitude'))]
        d['geomType'] = 'point' if d['osmType'] == 'node' else 'line'
        d['koinReward'] = d.pop('fix_koin_count')
        d['koinRewardWhenComplete'] = d.pop('vote_koin_count')

        d['question'] = locale.translateQuestion(lang, d['question'], d.pop('txt1'), d.pop('txt2'), d.pop('txt3'), d.pop('txt4'), d.pop('txt5'))
        d['title'] = locale.translate(lang, d['title'])

        input_type = MissionTypeLoader()
        d['inputType'] = input_type.getInputType(lang=lang, type_id=d['error_type'], input_type_name= d.pop('view_type'),
                 re_description=d.pop('constraint_re_description'), re=d.pop('constraint_re'),
                 lower_bound=d.pop('constraint_lower_bound'), upper_bound=d.pop('constraint_upper_bound'))
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
    koin_count                 = Column('fix_koin_count', Integer, primary_key=False)
    schema                     = Column(String, primary_key=False)
    error_type                 = Column('error_type', String, primary_key=False)
    osmId                      = Column('osm_id', BigInteger, primary_key=False)
    solution                   = Column('message',String, primary_key=False)
    complete                   = Column(Boolean, nullable=False)
    valid                      = Column(Boolean, nullable=False)
    in_osm                     = Column(Boolean, nullable=False)

    def __init__(self, userId, create_date, error_id, error_type, schema, osmId, solution, koin_count, complete, valid):
        self.user_id = userId
        self.create_date = create_date
        self.error_id = error_id
        self.error_type = error_type
        self.schema = schema
        self.osmId = osmId
        self.solution = solution
        self.koin_count = koin_count
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
        d['achievementDate'] = achievementDate.strftime("%d/%m/%y") if achievementDate else None
        d['achievementTitle'] = locale.translate(lang, d.pop('title'))
        d['achieved'] = achieved
        d['achievementId'] = d.pop('id')
        d['achievementImageURI'] = d.pop('name')
        d['achievementDescription'] = locale.translate(lang, d.pop('description'))
        return d



class UserBadge(Base):

    __table_args__ = {'schema': 'kort'}
    __tablename__ = 'user_badge'

    user_id                    = Column('user_id', Integer, ForeignKey('kort.user.user_id'), primary_key=True, nullable=False)
    badge_id                   = Column('badge_id', Integer, ForeignKey('kort.badge.badge_id'), primary_key=True, nullable=False)
    create_date                = Column(DateTime, nullable=False)
    PrimaryKeyConstraint('user_id', 'badge_id', name='user_id_badge_id_pk')


class Highscore(Base):

    __table_args__ = {'schema': 'kort'}
    __tablename__ = 'highscore_all_time'

    id                         = Column(Integer, primary_key=True, nullable=False)
    rank                       = Column(Integer, primary_key=False, nullable=False)
    user_id                    = Column(Integer, primary_key=True, nullable=False)
    username                   = Column(String, nullable=False)
    mission_count              = Column(Integer, nullable=False)
    koin_count                 = Column(Integer, nullable=False)

    def dump(self):
        return dict([(k, v) for k, v in vars(self).items() if not k.startswith('_')])


class HighscoreDay(Base):

    __table_args__ = {'schema': 'kort'}
    __tablename__ = 'highscore_day'

    id                         = Column(Integer, primary_key=True, nullable=False)
    rank                       = Column(Integer, primary_key=False, nullable=False)
    user_id                    = Column(Integer, primary_key=True, nullable=False)
    username                   = Column(String, nullable=False)
    mission_count              = Column(Integer, nullable=False)
    koin_count                 = Column(Integer, nullable=False)

    def dump(self):
        return dict([(k, v) for k, v in vars(self).items() if not k.startswith('_')])


class HighscoreWeek(Base):

    __table_args__ = {'schema': 'kort'}
    __tablename__ = 'highscore_week'

    id                         = Column(Integer, primary_key=True, nullable=False)
    rank                       = Column(Integer, primary_key=False, nullable=False)
    user_id                    = Column(Integer, primary_key=True, nullable=False)
    username                   = Column(String, nullable=False)
    mission_count              = Column(Integer, nullable=False)
    koin_count                 = Column(Integer, nullable=False)

    def dump(self):
        return dict([(k, v) for k, v in vars(self).items() if not k.startswith('_')])


class HighscoreMonth(Base):

    __table_args__ = {'schema': 'kort'}
    __tablename__ = 'highscore_month'

    id                         = Column(Integer, primary_key=True, nullable=False)
    rank                       = Column(Integer, primary_key=False, nullable=False)
    user_id                    = Column(Integer, primary_key=True, nullable=False)
    username                   = Column(String, nullable=False)
    mission_count              = Column(Integer, nullable=False)
    koin_count                 = Column(Integer, nullable=False)

    def dump(self):
        return dict([(k, v) for k, v in vars(self).items() if not k.startswith('_')])

class Statistics(Base):

    __table_args__ = {'schema': 'kort'}
    __tablename__ = 'statistics'
    fix_count		    					= Column (Integer, primary_key=True)
    complete_fix_count		    			= Column (Integer, primary_key=False)
    incomplete_fix_count		    		= Column (Integer, primary_key=False)
    validated_fix_count			    		= Column (Integer, primary_key=False)
    user_count					    		= Column (Integer, primary_key=False)
    osm_user_count				    		= Column (Integer, primary_key=False)
    google_user_count			    		= Column (Integer, primary_key=False)
    fb_user_count				    		= Column (Integer, primary_key=False)
    badge_count					    		= Column (Integer, primary_key=False)
    solved_motorway_ref_count	    		= Column (Integer, primary_key=False)
    solved_religion_count		    		= Column (Integer, primary_key=False)
    solved_poi_name_count		    		= Column (Integer, primary_key=False)
    solved_missing_maxspeed_count	    	= Column (Integer, primary_key=False)
    solved_language_unknown_count		    = Column (Integer, primary_key=False)
    solved_missing_track_type_count		    = Column (Integer, primary_key=False)
    solved_way_wo_tags_count			    = Column (Integer, primary_key=False)
    solved_missing_cuisine_count			= Column (Integer, primary_key=False)
    solved_opening_hours_count			    = Column (Integer, primary_key=False)
    solved_missing_level_count			    = Column (Integer, primary_key=False)
    highscore_place_1_count				    = Column (Integer, primary_key=False)
    highscore_place_2_count				    = Column (Integer, primary_key=False)
    highscore_place_3_count				    = Column (Integer, primary_key=False)
    total_fix_count_100_count			    = Column (Integer, primary_key=False)
    total_fix_count_50_count			    = Column (Integer, primary_key=False)
    total_fix_count_10_count			    = Column (Integer, primary_key=False)
    total_fix_count_1_count				    = Column (Integer, primary_key=False)
    fix_count_motorway_ref_100_count	    = Column (Integer, primary_key=False)
    fix_count_motorway_ref_50_count		    = Column (Integer, primary_key=False)
    fix_count_motorway_ref_5_count		    = Column (Integer, primary_key=False)
    fix_count_religion_100_count		    = Column (Integer, primary_key=False)
    fix_count_religion_50_count			    = Column (Integer, primary_key=False)
    fix_count_religion_5_count			    = Column (Integer, primary_key=False)
    fix_count_poi_name_100_count		    = Column (Integer, primary_key=False)
    fix_count_poi_name_50_count			    = Column (Integer, primary_key=False)
    fix_count_poi_name_5_count			    = Column (Integer, primary_key=False)
    fix_count_missing_maxspeed_100_count    = Column (Integer, primary_key=False)
    fix_count_missing_maxspeed_50_count	    = Column (Integer, primary_key=False)
    fix_count_missing_maxspeed_5_count	    = Column (Integer, primary_key=False)
    fix_count_language_unknown_100_count    = Column (Integer, primary_key=False)
    fix_count_language_unknown_50_count	    = Column (Integer, primary_key=False)
    fix_count_language_unknown_5_count	    = Column (Integer, primary_key=False)
    fix_count_missing_track_type_100_count	= Column (Integer, primary_key=False)
    fix_count_missing_track_type_50_count	= Column (Integer, primary_key=False)
    fix_count_missing_track_type_5_count	= Column (Integer, primary_key=False)
    fix_count_way_wo_tags_100_count			= Column (Integer, primary_key=False)
    fix_count_way_wo_tags_50_count			= Column (Integer, primary_key=False)
    fix_count_way_wo_tags_5_count			= Column (Integer, primary_key=False)
    fix_count_missing_cuisine_100_count		= Column (Integer, primary_key=False)
    fix_count_missing_cuisine_50_count		= Column (Integer, primary_key=False)
    fix_count_missing_cuisine_5_count		= Column (Integer, primary_key=False)
    fix_count_missing_level_100_count		= Column (Integer, primary_key=False)
    fix_count_missing_level_50_count		= Column (Integer, primary_key=False)
    fix_count_missing_level_5_count			= Column (Integer, primary_key=False)
    fix_count_opening_hours_100_count		= Column (Integer, primary_key=False)
    fix_count_opening_hours_50_count		= Column (Integer, primary_key=False)
    fix_count_opening_hours_5_count			= Column (Integer, primary_key=False)
    six_per_day_count						= Column (Integer, primary_key=False)

    def dump(self):
        return dict([(k, v) for k, v in vars(self).items() if not k.startswith('_')])
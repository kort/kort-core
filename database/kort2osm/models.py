from geoalchemy2 import Geometry
from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from config import BaseConfig

Base = declarative_base()


def init_db():
    engine = create_engine(BaseConfig.SQLALCHEMY_DATABASE_URI, convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)
    return db_session


class kort_errors(Base):

    __table_args__ = {'schema': 'kort'}
    __tablename__ = 'all_errors'

    errorId                     = Column('error_id', Integer, primary_key=True)
    schema                      = Column(String, primary_key=False)
    source                      = Column(String, primary_key=False)
    osmId                       = Column('osm_id', BigInteger, primary_key=False)
    osmType                     = Column('osm_type', String, primary_key=False)
    question                    = Column('description', String, primary_key=False)
    geom                        = Column(Geometry, nullable=False)
    latitude                    = Column(Numeric, primary_key=False)
    longitude                   = Column(Numeric, primary_key=False)
    txt1                        = Column(String, primary_key=False)
    txt2                        = Column(String, primary_key=False)
    txt3                        = Column(String, primary_key=False)
    txt4                        = Column(String, primary_key=False)
    txt5                        = Column(String, primary_key=False)


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


class error_type(Base):

    __table_args__ = {'schema': 'kort'}
    __tablename__ = 'error_type'

    error_type_id               = Column(Integer, primary_key=True)
    type                        = Column(String, primary_key=False)
    osm_tag                     = Column(String, primary_key=False)


class User(Base):

    __tablename__ = 'user'
    __table_args__ = {'schema': 'kort'}

    id                  = Column('user_id', Integer, primary_key=True)
    username            = Column(String, nullable=False)

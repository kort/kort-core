from geoalchemy2 import Geometry
from sqlalchemy import BigInteger
from sqlalchemy import Column
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


class osm_error(Base):

    __table_args__ = {'schema': 'osm_errors'}
    __tablename__ = 'errors'
    schema                  = Column(String, primary_key=True, default='100')
    id                      = Column('error_id', Integer, primary_key=True, autoincrement=True)
    error_type_id           = Column(Integer, primary_key=False)
    object_id               = Column(BigInteger, primary_key=True)
    object_type             = Column(String, primary_key=True)
    error_name              = Column(String, primary_key=False)
    geom                    = Column(Geometry, nullable=False)
    lat                     = Column(Numeric, primary_key=False)
    lon                     = Column(Numeric, primary_key=False)
    msgid                   = Column(String, primary_key=False)
    txt1                   = Column(String, primary_key=False)
    txt2                   = Column(String, primary_key=False)
    txt3                   = Column(String, primary_key=False)
    txt4                   = Column(String, primary_key=False)
    txt5                   = Column(String, primary_key=False)
    UniqueConstraint(schema, id, name='unique_schema_id')
    UniqueConstraint(error_type_id, object_type, object_id, name='unique_errorType_osmType_osmId')
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import os
from sqlalchemy.pool import SingletonThreadPool
from sqlalchemy.orm import relationship

Base = declarative_base()

def db_connect():
    # Change in to your path
    return create_engine(
        'sqlite:////home/sid/Python/Scrapy/dashsql/dashsql/spiders/titles.db',
        connect_args={'check_same_thread':False},
        poolclass=SingletonThreadPool
    )
    # return create_engine('sqlite:///titles.db')

def create_table(engine):
    Base.metadata.create_all(engine)

class Domain(Base):
    __tablename__ = "domains"
    domain_id = Column(Integer(), primary_key=True)
    name = Column(String(), unique=True)

class Title(Base):
    __tablename__ = "titles"
    title_id = Column(Integer(), primary_key=True)
    domain_id = Column(Integer, ForeignKey('domains.domain_id'))
    title = Column(String(), unique=True)
    status = Column(Integer())
    response_len = Column(Integer())
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    domain = relationship(Domain, back_populates="titles")
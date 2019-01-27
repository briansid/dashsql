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
        'sqlite:///titles.db',
        connect_args={'check_same_thread':False},
        poolclass=SingletonThreadPool
    )

def create_table(engine):
    Base.metadata.create_all(engine)


class Domain(Base):
    __tablename__ = "domains"
    domain_id = Column(Integer(), primary_key=True)
    domain_name = Column(String(255), unique=True)
    project_name = Column(String(2))
    version = Column(String(7))
    monitoring_rate = Column(Integer())

class Subdomain(Base):
    __tablename__ = "subdomains"
    subdomain_id = Column(Integer(), primary_key=True)
    subdomain_name = Column(String(255), unique=True)
    domain_id = Column(Integer, ForeignKey('domains.domain_id'))
    project_name = Column(String(2))
    version = Column(String(7))
    monitoring_rate = Column(Integer())


class Title(Base):
    __tablename__ = "titles"
    title_id = Column(Integer(), primary_key=True)
    domain_id = Column(Integer, ForeignKey('domains.domain_id'))
    subdomain_id = Column(Integer, ForeignKey('subdomains.subdomain_id'))
    title = Column(String(255))
    status = Column(Integer())
    response_len = Column(Integer())
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


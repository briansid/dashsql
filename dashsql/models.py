from sqlalchemy import create_engine, Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.pool import SingletonThreadPool

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
    created_on = Column(DateTime(), default=datetime.now)

class Subdomain(Base):
    __tablename__ = "subdomains"
    subdomain_id = Column(Integer(), primary_key=True)
    subdomain_name = Column(String(255), unique=True)
    domain_id = Column(Integer(), ForeignKey('domains.domain_id'))
    project_name = Column(String(2))
    version = Column(String(7))
    monitoring_rate = Column(Integer())
    created_on = Column(DateTime(), default=datetime.now)


class Title(Base):
    __tablename__ = "titles"
    title_id = Column(Integer(), primary_key=True)
    domain_id = Column(Integer, ForeignKey('domains.domain_id'))
    subdomain_id = Column(Integer, ForeignKey('subdomains.subdomain_id'))
    # title = Column(String(255))
    status = Column(Integer())
    response_len = Column(Integer())
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    traffic = Column('Traffic', Integer())
    fd = Column('FD', Integer())
    pkh = Column('PKH', String())
    uptime = Column('UPTime', Integer())
    speed_test = Column('Speed Test', Integer())
    serp_desktop = Column('SERP Desktop', Integer())
    serp_mobile = Column('SERP Mobile', Integer())
    links = Column('Links', Integer())
    content = Column('Content', String())
    robots = Column('Robots', String())
    y_alert = Column('Y.Alert', String())
    g_alert = Column('G.Alert', String())
    exp_date = Column('Exp. Date', Date())
    pages = Column('Pages', Integer())
    y_index = Column('Y.Index', Integer())
    g_index = Column('G.Index', Integer())


class Archive(Base):
    __tablename__ = "archive"
    archive_id = Column(Integer(), primary_key=True)
    title_id = Column(Integer(), ForeignKey('titles.title_id'))
    # Do we need domain_id and suubdomain_id if we have title_id?
    # domain_id = Column(Integer, ForeignKey('domains.domain_id'))
    # subdomain_id = Column(Integer, ForeignKey('subdomains.subdomain_id'))
    # title = Column(String(255))
    status = Column(Integer())
    response_len = Column(Integer())
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    traffic = Column('Traffic', Integer())
    fd = Column('FD', Integer())
    pkh = Column('PKH', String())
    uptime = Column('UPTime', Integer())
    speed_test = Column('Speed Test', Integer())
    serp_desktop = Column('SERP Desktop', Integer())
    serp_mobile = Column('SERP Mobile', Integer())
    links = Column('Links', Integer())
    content = Column('Content', String())
    robots = Column('Robots', String())
    y_alert = Column('Y.Alert', String())
    g_alert = Column('G.Alert', String())
    exp_date = Column('Exp. Date', Date())
    pages = Column('Pages', Integer())
    y_index = Column('Y.Index', Integer())
    g_index = Column('G.Index', Integer())
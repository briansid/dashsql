# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime, timedelta
from dashsql.items import DashsqlItem
from sqlalchemy.orm import sessionmaker
from dashsql.models import Title, db_connect, create_table, Domain, Subdomain


class H1Spider(scrapy.Spider):
    name = 'h1'

    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def start_requests(self):
        session = self.Session()
        query = session.query(Domain)
        for q in query:
            # Check interval
            try:
                last_check = session.query(Title.updated_on).filter_by(domain_id=q.domain_id, subdomain_id=None).scalar()
            except:
                pass
            else:
                if datetime.now() < last_check+timedelta(minutes=q.monitoring_rate):
                    continue
            yield scrapy.Request('http://'+q.domain_name, meta={
                'domain_id': q.domain_id,
                'subdomain_id': None
            })
        query = session.query(Subdomain)
        for q in query:
            # Check interval
            try:
                last_check = session.query(Title.updated_on).filter_by(domain_id=q.domain_id, subdomain_id=q.subdomain_id).scalar()
            except:
                pass
            else:
                if datetime.now() < last_check+timedelta(minutes=q.monitoring_rate):
                    continue
            yield scrapy.Request('http://'+q.subdomain_name, meta={
                    'domain_id': q.domain_id,
                    'subdomain_id': q.subdomain_id,
                })

    def parse(self, response):
        i = DashsqlItem()
        i['domain_id'] = response.meta['domain_id']
        i['subdomain_id'] = response.meta['subdomain_id']
        i['title'] = response.css('title::text').get()
        i['status'] = response.status
        i['response_len'] = len(response.text)
        
        yield i

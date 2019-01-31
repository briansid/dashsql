# -*- coding: utf-8 -*-
import scrapy, random
from datetime import datetime, timedelta, date
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
                last_check = session.query(Title.updated_on).filter_by(domain_id=q.domain_id, subdomain_id=None).one()[0]
            except:
                pass
            else:
                print('last_check')
                print(last_check)
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
                last_check = session.query(Title.updated_on).filter_by(domain_id=q.domain_id, subdomain_id=q.subdomain_id).one()[0]
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
        # i['title'] = response.css('title::text').get()
        i['status'] = response.status
        i['response_len'] = len(response.text)
        i['traffic'] = random.choice([i for i in range(0,11000, 1000)])
        i['fd'] = random.choice([i for i in range(0,110,10)])
        i['pkh'] = random.choice(['ok', 'site', '192.168.0.1', 'site 192.168.0.1'])
        i['uptime'] = random.choice([0, 200])
        i['speed_test'] = random.choice([1, 2, 3, 4])
        i['serp_desktop'] = random.randint(0,250)
        i['serp_mobile'] = random.randint(0,250)
        i['links'] = random.randint(0,60)
        i['content'] = random.choice(['ok', 'change'])
        i['robots'] = random.choice(['ok', 'change'])
        i['y_alert'] = random.choice(['ok', 'change'])
        i['g_alert'] = random.choice(['ok', 'change'])
        i['exp_date'] = date(2021, 5, 2)
        i['pages'] = random.randint(0,500)
        i['y_index'] = random.randint(0,500)
        i['g_index'] = random.randint(0,500)

        yield i

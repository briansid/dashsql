# -*- coding: utf-8 -*-
import scrapy, datetime
from dashsql.items import DashsqlItem
from sqlalchemy.orm import sessionmaker
from dashsql.models import Title, db_connect, create_table, Domain


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
            yield scrapy.Request(q.name)

    def parse(self, response):
        i = DashsqlItem()
        i['title'] = response.css('title::text').get()
        i['status'] = response.status
        yield i

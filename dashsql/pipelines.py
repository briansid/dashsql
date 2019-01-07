# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from dashsql.models import Title, db_connect, create_table
from sqlalchemy.exc import IntegrityError
from datetime import datetime

class DashsqlPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)


    def process_item(self, item, spider):
        session = self.Session()
        lot = Title(**item)

        try:
            session.add(lot)
            session.commit()

        except:
            session.rollback()
            query = session.query(Title)
            q = query.filter(Title.title == item['title']).first()
            q.updated_on = datetime.now()
            session.commit()
        finally:
            session.close()

        return item

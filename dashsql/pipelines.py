# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from dashsql.models import Title, db_connect, create_table, Archive
from sqlalchemy.exc import IntegrityError
from datetime import datetime


class DashsqlPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        q = session.query(Title).filter_by(domain_id=item['domain_id'], subdomain_id=item['subdomain_id'])
        if q:
            # Copy to archive
            qdict = q.first().__dict__
            del qdict['_sa_instance_state']
            del qdict['title_id']
            print(qdict)
            a = Archive(**qdict)
            session.add(a)

            # Delete row from title
            q.delete()

            # Add new row
            title = Title(**item)
            session.add(title)
            session.commit()
        else:
            title = Title(**item)
            session.add(title)
            session.commit()

        return item

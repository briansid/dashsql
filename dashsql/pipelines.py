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
        query = session.query(Title).filter_by(domain_id=item['domain_id'], subdomain_id=item['subdomain_id'])
        q = query.first()
        if q:
            qcopy = q.__dict__.copy()
            changes = False
            for key, value in item.items():
                if qcopy[key] != value:
                    changes = True
                    break
                # Update column even if no changes
                # else:
                #     q.updated_on = datetime.now()

            if changes:
                # Copy old row to archive
                del qcopy['_sa_instance_state']
                # del qcopy['domain_id']
                # del qcopy['subdomain_id']
                a = Archive(**qcopy)
                session.add(a)
                # Update current row
                query.update(item)
                # Commit
                session.commit()
        else:
            t = Title(**item)
            session.add(t)
            session.commit()

        return item

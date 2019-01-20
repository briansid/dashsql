import sys
import getopt
from sqlalchemy.orm import sessionmaker
from models import Title, db_connect, create_table, Domain, Subdomain
from sqlalchemy.orm.exc import NoResultFound

engine = db_connect()
create_table(engine)
Session = sessionmaker(bind=engine)
session = Session()

domains = ['google.com', 'yahoo.com', 'bing.com']
subdomains = [('images.google.com', 1), ('maps.google.com', 1), ('mail.google.com', 1),
            ('view.yahoo.com', 2), ('tw.news.yahoo.com', 2), ('stores.yahoo.com', 2)]
for domain in domains:
    d = Domain(domain_name=domain)
    session.add(d)
    session.commit()

for subdomain in subdomains:
    sd = Subdomain(subdomain_name=subdomain[0], domain_id=subdomain[1])
    session.add(sd)
    session.commit()

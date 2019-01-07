import sys
import getopt
from sqlalchemy.orm import sessionmaker
from models import Title, db_connect, create_table, Domain
from sqlalchemy.orm.exc import NoResultFound

usage = """usage: domain.py [-h] [-a domain] [-r domain_id] [-b domains.txt] [-l]

optional arguments:
  -h, --help Show this help message and exit
  -a, --add Add domain to parser
  -r, --remove Remove domain from parsers
  -b, --bulk Bulk add domains to parser
  -l, --list List all domains"""

argv = sys.argv[1:]

if len(argv) == 0:
    print(usage)
    sys.exit()

try:
    opts, args = getopt.getopt(argv, "a:r:b:lh", ["add=", "remove=", "list", "bulk=", "help"])
except:
    print(usage)
    sys.exit()

engine = db_connect()
create_table(engine)
Session = sessionmaker(bind=engine)
session = Session()

for opt, arg in opts:
    if opt in ['-a', '--add']:
        if not arg.startswith('http'):
            arg = 'http://' + arg
        query = Domain(name=arg)
        session.add(query)
        session.commit()
        print('%s added' % arg)
    elif opt in ['-r', '--remove']:
        # Delete from Titles
        query = session.query(Title)
        try:
            query = query.filter(Title.domain_id == arg).one()
            session.delete(query)
            session.commit()
        except NoResultFound:
            pass

        # Delete from Domains
        query = session.query(Domain)
        query = query.filter(Domain.domain_id == arg).one()
        print('%s removed.' % query.name)
        session.delete(query)
        session.commit()
        
    elif opt in ['-b', '--bulk']:
        with open('urllist.txt') as f: 
            urls = f.readlines()
        urls = [url.strip() for url in urls]
        kv = {}
        for n, url in enumerate(urls):
            if not url.startswith('http'):
                url = 'http://' + url
            kv['url'+str(n)] = url
        print(kv)
        for k, v in kv.items():
            k = Domain(name=v)
            print(k.name)
            session.add(k)
        session.flush()
        session.commit()

        print('\n'.join(urls))
        print('Added successfully.')

    elif opt in ['-l', '--list']:
        for d in session.query(Domain):
            print('{:3} - {}'.format(d.domain_id, d.name))
    elif opt in ['-h', '--help']:
        print(usage)

session.close()
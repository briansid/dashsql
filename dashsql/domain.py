import sys, csv
import getopt
from sqlalchemy.orm import sessionmaker
from models import Title, db_connect, create_table, Domain, Subdomain
from sqlalchemy.orm.exc import NoResultFound

usage = """usage: domain.py [-h] [-a domain] [-r domain_id] [-b domains.txt] [-l]

optional arguments:
  -h, --help Show this help message and exit
  -a, --add Add domain to parser
  -l, --level Dommain Level
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
        with open(arg) as f:
            reader = csv.DictReader(f)
            for line in reader:
                if line['subdomain_name']:
                    domain_id = session.query(Domain.domain_id).filter_by(domain_name=line['domain_name']).scalar()
                    del line['domain_name']
                    line['domain_id'] = domain_id
                    sd = Subdomain(**line)
                    session.add(sd)
                    session.commit()
                else:
                    del line['subdomain_name']
                    d = Domain(**line)
                    session.add(d)
                    session.commit()
        # with open(arg) as f:
        #     urls = f.readlines()
        # urls = [url.strip() for url in urls]
        # kv = {}
        # for n, url in enumerate(urls):
        #     if not url.startswith('http'):
        #         url = 'http://' + url
        #     kv['url'+str(n)] = url
        # for k, v in kv.items():
        #     k = Domain(name=v)
        #     session.add(k)
        # session.flush()
        # session.commit()

        print('Added successfully.')

    elif opt in ['-l', '--list']:
        for d in session.query(Domain):
            print('{:3} - {}'.format(d.domain_id, d.domain_name))
    elif opt in ['-h', '--help']:
        print(usage)

session.close()
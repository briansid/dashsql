import sys, csv
import getopt
from sqlalchemy.orm import sessionmaker
from models import Title, db_connect, create_table, Domain, Subdomain
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

usage = """usage: domain.py [-h] [-a domain] [-r domain_id] [-b domains.csv] [-l domain|subdomain] [-R domains.csv] [-g filename.csv]

optional arguments:
  -h, --help Show this help message and exit
  -a, --add Add domain to parser
  -r, --remove Remove domain
  -g, --get Get all domain and subdomains in a file
  -R, --REM Bulk remove
  -b, --bulk Bulk add domains to parser
  -l, --list List all domains"""

argv = sys.argv[1:]

if len(argv) == 0:
    print(usage)
    sys.exit()

try:
    opts, args = getopt.getopt(argv, "a:r:b:l:R:g:h", ["add=", "remove=", "list=", "bulk=", "REM=", "get=", "help"])
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

    if opt in ['-g', '--get']:
        with open(arg, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(('domain_name', 'subdomain_name'))
            query = session.query(Domain.domain_name, Subdomain.subdomain_name)
            query = query.join(Subdomain)
            for q in query:
                writer.writerow(q)

            query = session.query(Domain.domain_name)
            for q in query:
                row = (q.domain_name, None)
                writer.writerow(row)

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

    elif opt in ['-R', '--REM']:
        with open(arg) as f:
            reader = csv.DictReader(f)
            for line in reader:
                if line['subdomain_name']:
                    try:
                        query = session.query(Subdomain).filter_by(subdomain_name=line['subdomain_name']).one()
                        session.delete(query)
                        session.commit()
                    except NoResultFound:
                        print('%s is not found' % line['subdomain_name'])
                        continue
                    else:
                        print('Subdomain %s successfully deleted' % line['subdomain_name'])
                else:
                    try:
                        query = session.query(Domain).filter_by(domain_name=line['domain_name']).one()
                        domain_id = query.domain_id
                        session.delete(query)
                        session.commit()
                    except NoResultFound:
                        print('%s is not found' % line['domain_name'])
                        continue
                    else:
                        print('Domain %s successfully deleted' % line['domain_name'])
                    try:
                        # Remove all the subdomains belong to this domain
                        query = session.query(Subdomain).filter_by(domain_id=domain_id)
                        for q in query:
                            session.delete(q)
                            session.commit()
                    except NoResultFound:
                        pass

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

                    try:
                        session.commit()
                        print('Subdomain %s added successfully' % line['subdomain_name'])
                    # Domain/Subdomain already exist
                    except IntegrityError as err:
                        session.rollback()
                        continue

                else:
                    del line['subdomain_name']
                    d = Domain(**line)
                    session.add(d)

                    try:
                        session.commit()
                        print('Domain %s added successfully' % line['domain_name'])
                    # Domain/Subdomain already exist
                    except IntegrityError as err:
                        session.rollback()
                        continue



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


    elif opt in ['-l', '--list']:
        if arg.lower() in ['domain', 'domains']:
            for d in session.query(Domain):
                print('{:3} - {}'.format(d.domain_id, d.domain_name))
        elif arg.lower() in ['subdomain', 'subdomains']:
            for sd in session.query(Subdomain):
                print('{:3} - {}'.format(sd.subdomain_id, sd.subdomain_name))
        else:
            print(usage)
            sys.exit()

    elif opt in ['-h', '--help']:
        print(usage)

session.close()
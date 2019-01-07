import sys
import getopt
from sqlalchemy.orm import sessionmaker
from models import Title, db_connect, create_table, Domain

usage = """usage: domain.py [-h] [-a domain] [-r domain_id] [-b domains.txt] [-l]

optional arguments:
  -h, --help Show this help message and exit
  -a, --add Add domain to parser
  -r, --remove Remove domain fom parsers
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
        q = Domain(name=arg)
        session.add(q)
        session.commit()
        print('%s added' % arg)
    elif opt in ['-r', '--remove']:
        q = session.query(Domain)
        query = query.filter(Domain.domain_id == arg)
        print('Removing %s' % query.name)
        query.delete()
        
    elif opt in ['-b', '--bulk']:
        print('Bulk add')
    elif opt in ['-l', '--list']:
        for d in session.query(Domain):
            print('{:3} - {}'.format(d.domain_id, d.name))
    elif opt in ['-h', '--help']:
        print(usage)

session.close()
#!/usr/bin/env python
import os
import sys
import transaction
from getpass import getpass
from sqlalchemy import create_engine

from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

from pyramid_signup.models import User
from pyramid_signup.models import UserGroup
from pyramid_signup.models import SUEntity

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from pcolalug.models import Base

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

def usage(argv):# pragma: no cover 
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd)) 
    sys.exit(1)

def main(argv=sys.argv): # pragma: no cover
    if len(argv) != 2:
        usage(argv)

    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)

    if settings.get('sqlalchemy.url', None):
        engine = engine_from_config(settings, 'sqlalchemy.')
    else:
        from bundle_config import config

        url = u"postgresql+psycopg2://%(username)s:%(password)s@%(host)s:%(port)s/%(database)s" % config['postgres']
        engine = create_engine(url, echo=True)

    session = DBSession(bind=engine)
    SUEntity.metadata.drop_all(engine)
    SUEntity.metadata.create_all(engine)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    username = raw_input("What is your username?: ").decode('utf-8')
    email = raw_input("What is your email?: ").decode('utf-8')
    password = getpass("What is your password?: ").decode('utf-8')


    with transaction.manager:
        group = UserGroup('admin', 'Admin Group')
        admin = User(username=username, password=password, email=email, activated=True)
        admin.groups.append(group)
        session.add(group)
        session.add(admin)

if __name__ == "__main__": # pragma: no cover
    main()

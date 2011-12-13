import cryptacular.bcrypt
import transaction

from sqlalchemy import Column
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import synonym
from sqlalchemy.types import Integer
from sqlalchemy.types import Unicode
from sqlalchemy.types import UnicodeText
from sqlalchemy.types import DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

from zope.sqlalchemy import ZopeTransactionExtension

from pyramid.security import Everyone
from pyramid.security import Authenticated
from pyramid.security import Allow

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

crypt = cryptacular.bcrypt.BCRYPTPasswordManager()


def hash_password(password):
    return unicode(crypt.encode(password))

class Presentation(Base):
    """
    A meeting we are having
    """
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(20), unique=True)
    description = Column(UnicodeText)
    presenter = Column(Unicode(200), unique=True)
    date = Column(DateTime)

class RootFactory(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'authed')
    ]

    def __init__(self, request):
        pass  # pragma: no cover

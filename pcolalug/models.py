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


class User(Base):
    """
    Application's user model.
    """
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(Unicode(20), unique=True)
    first_name = Column(Unicode(50))
    last_name = Column(Unicode(50))
    email = Column(Unicode(50))

    _password = Column('password', Unicode(60))

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = hash_password(password)

    password = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password)

    def __init__(self, username, password, email, first_name=None, last_name=None):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    @classmethod
    def get_by_username(cls, username):
        return DBSession.query(cls).filter(cls.username == username).first()

    @classmethod
    def check_password(cls, username, password):
        user = cls.get_by_username(username)
        if not user:
            return False
        return crypt.check(user.password, password)

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

def initialize_sql(engine):  # pragma: no cover
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)

    try:
        user = User.get_by_username('admin')
        if not user:
            session = DBSession()
            admin = User('admin', 'temp', 'pcolalug@gmail.com')
            session.add(admin)
            transaction.commit()
    except IntegrityError:
        # already created
        pass

from sqlalchemy import Column
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import UnicodeText
from sqlalchemy.types import DateTime
from sqlalchemy.ext.declarative import declarative_base

from pyramid_signup.models import SUEntity

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Presentation(SUEntity):
    """
    A meeting we are having
    """
    name = Column(UnicodeText)
    description = Column(UnicodeText)
    presenter = Column(UnicodeText)
    date = Column(DateTime)

from sqlalchemy import Column
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import UnicodeText
from sqlalchemy.types import Date
from sqlalchemy.types import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

import os
from lib import get_data_dir
from sqlalchemy.ext.declarative import declarative_base

from horus.models               import GroupMixin
from horus.models               import UserMixin
from horus.models               import UserGroupMixin
from horus.models               import ActivationMixin
from horus.models               import BaseModel

Base = declarative_base(cls=BaseModel)

class User(UserMixin, Base):
    pass

class Group(GroupMixin, Base):
    pass

class UserGroup(UserGroupMixin, Base):
    pass

class Activation(ActivationMixin, Base):
    pass

class File(Base):
    user_pk = Column(Integer, ForeignKey(User.pk), nullable=False)
    mimetype = Column(UnicodeText, nullable=False)
    uid = Column(UnicodeText, nullable=False)
    filename = Column(UnicodeText, nullable=False)
    size = Column(Integer, nullable=False)


    def public_url(self, request):
        if self.uid:
            return request.static_url(os.path.join(get_data_dir(), 'uploads/%s' % self.uid))

class Presentation(Base):
    """
    A meeting we are having
    """
    name = Column(UnicodeText)
    description = Column(UnicodeText)
    date = Column(Date, nullable = False)
    presenter_pk = Column(Integer, ForeignKey(User.pk), nullable=False)
    presenter = relationship(User)
    file_pk = Column(Integer, ForeignKey(File.pk))
    file = relationship(File)

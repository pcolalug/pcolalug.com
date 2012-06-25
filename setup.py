import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid_tm'
    , 'pyramid_debugtoolbar'
    , 'pyramid_jinja2'
    , 'pyramid_beaker'
    , 'pyramid_mailer'
    , 'sphinx'
    , 'gunicorn'
    , 'supervisor'
    , 'zope.interface'
    , 'pyramid'
    , 'SQLAlchemy'
    , 'transaction'
    , 'zope.sqlalchemy'
    , 'psycopg2'
    , 'cryptacular'
    , 'PyCrypto'
    , 'python-dateutil==1.5'
    , 'icalendar'
    , 'mock'
    , 'coverage'
    , 'webtest'
    , 'alembic'
    , 'pystache'
    , 'horus'
    , 'deform_jinja2'
    , 'pyramid_deform'
]

if sys.version_info[:3] < (2,5,0): # pragma: no cover
    requires.append('pysqlite')

setup(name='pcolalug',
      version='0.0',
      description='pcolalug',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='pcolalug',
      install_requires = requires,
      entry_points = """\
      [paste.app_factory]
      main = pcolalug:main
      """,
      paster_plugins=['pyramid'],
      )


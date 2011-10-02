.. pcolalug documentation master file, created by
   sphinx-quickstart on Sun Oct  2 15:28:19 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pcolalug's documentation!
====================================
===============
Getting Started
===============
Our development environment should simulate production. No use of sqlite for database.
Install and Setup your virtualenv::
    $ pip install virtualenv
    $ virtualenv --no-site-packages pcolalug.org
    $ cd pcolalug.org
    $ source bin/active
    $ mkdir src
    $ cd src
    $ git clone git@github.com:pcolalug/pcolalug.org.git

Install redis, mongodb, and postgresql, then::
    $ createdb pcolalug
    $ pip install requirements.pip
    $ python setup.py develop
    $ supervisord
    $ supervisorctl

================
Resources
================
http://www.sqlalchemy.org/docs/
https://docs.pylonsproject.org/
http://www.formencode.org/en/latest/index.html
http://sphinx.pocoo.org/
http://jinja.pocoo.org/docs/


.. toctree::
   :maxdepth: 2

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


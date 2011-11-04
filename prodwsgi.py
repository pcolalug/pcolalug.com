from pyramid.paster import get_app
import os

ROOT_PATH = os.path.dirname(__file__)

print 'loading application'

application = get_app(os.path.join(ROOT_PATH, 'production.ini'), 'main')

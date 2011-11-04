from pyramid.paster import get_app
import os

ROOT_PATH = os.path.dirname(__file__)

application = get_app(os.path.join(ROOT_PATH, 'development.ini'), 'main')

import unittest
from pyramid import testing
from pyramid.paster import get_app

from mock import patch
import os

ROOT = os.path.dirname(__file__)

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        app = get_app('development.ini')
        from webtest import TestApp
        self.app = TestApp(app)
        self.config = testing.setUp()

class ViewTests(BaseTestCase):
    @patch('urllib.urlopen')
    def test_index(self, urlopen_mock):
        """ Call the index view, make sure routes are working """
        output = open(os.path.join(ROOT, '../data/basic.ics'))
        urlopen_mock.return_value = output
        res = self.app.get('/', status=200)
        self.failUnless('John Anderson and Ian Barr' in res.body)

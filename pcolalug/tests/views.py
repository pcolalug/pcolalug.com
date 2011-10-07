import unittest
from pyramid import testing
from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory('pcolalug')

from mock import patch
import os

ROOT = os.path.dirname(__file__)

class ViewTests(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        
    def tearDown(self):
        testing.tearDown()

    @patch('urllib.urlopen')
    def test_index(self, urlopen_mock):
        """ Make sure index parses ical properly """
        from pcolalug.views import index
        output = open(os.path.join(ROOT,'data/basic.ics'))
        urlopen_mock.return_value = output

        request = testing.DummyRequest()
        response = index(request)
        self.assertEqual(len(response['events']), 3)
        self.assertEqual(response['events'][0]['summary'], 'Monthly Meeting - Software Deployment')

    def test_contact(self):
        """ Make sure we can get to contact page"""
        from pcolalug.views import contact
        request = testing.DummyRequest()
        response = contact(request)
        self.assertEqual(response, {}) 

    def test_calendar(self):
        """ Make sure we can get to calendar page"""
        from pcolalug.views import calendar
        request = testing.DummyRequest()
        response = calendar(request)
        self.assertEqual(response, {}) 

    def test_login_fails_empty(self):
        """ Make sure we can't login with empty credentials"""
        from pcolalug.views import login
        self.config.add_route('index', '/')

        request = testing.DummyRequest()
        response = login(request)
        self.assertEqual(response, {})

    def test_login_fails_bad(self):
        """ Make sure we can't login with bad credentials"""
        from pcolalug.views import login
        self.config.add_route('index', '/')

        request = testing.DummyRequest()
        request.POST = {
                    'submit': True,
                    'login': 'admin',
                    'password': 'test123',
                }

        response = login(request)
        self.assertEqual(response, {})

    def test_login(self):
        """ Make sure we can login """
        from pcolalug.views import login
        self.config.add_route('index', '/')

        request = testing.DummyRequest()
        request.POST = {
                    'submit': True,
                    'login': 'admin',
                    'password': 'temp',
                }
        response = login(request)
        self.assertEqual(response.status_int, 302)

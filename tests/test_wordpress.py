import datetime
import unittest
import os
import json

import pytz

import salvitobot
from salvitobot.wordpress import make_url


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.cwd = os.path.abspath(os.path.dirname(__file__))
        self.bot = salvitobot.Bot()

        with open(os.path.join(self.cwd, 'Quake', '1.json'), 'r') as handle:
            self.data1 = json.loads(handle.read())

    def test_make_url(self):
        salvitobot.config.wordpress_client = 'http://example.com/xmlrpc.php'

        datetime_local = datetime.datetime(2015, 2, 7, tzinfo=pytz.utc)
        post_title = 'Blah blah'

        result = make_url(post_title, datetime_local)
        expected = 'http://example.com/2015/02/07/blah-blah/'

        self.assertEqual(expected, result)

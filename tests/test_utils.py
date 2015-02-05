import datetime
import unittest
import os
import json

import pytz

from salvitobot import utils


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.cwd = os.path.abspath(os.path.dirname(__file__))

    def test_parse_quake_data(self):
        with open(os.path.join(self.cwd, 'Quake', '1.json'), 'r') as handle:
            data = json.loads(handle.read())

        result = utils.parse_quake_data(data, 'Venezuela')

        expected = datetime.datetime(2015, 2, 5, 5, 38, 57, 769999, tzinfo=pytz.utc)
        self.assertEqual(expected, result[0]['datetime_utc'])

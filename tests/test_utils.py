import datetime
import unittest
import os
import json

import pytz

from salvitobot import utils
import salvitobot
from salvitobot.exceptions import NoCountryError


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.cwd = os.path.abspath(os.path.dirname(__file__))
        self.bot = salvitobot.Bot()

        with open(os.path.join(self.cwd, 'Quake', '1.json'), 'r') as handle:
            self.data1 = json.loads(handle.read())

    def test_parse_quake_data(self):
        result = utils.parse_quake_data(self.data1, 'Venezuela')

        expected = datetime.datetime(2015, 2, 5, 5, 38, 57, 769999, tzinfo=pytz.utc)
        self.assertEqual(1, len(result))
        self.assertEqual(expected, result[0]['datetime_utc'])

    def test_parse_quake_data_two_quakes(self):
        with open(os.path.join(self.cwd, 'Quake', '2.json'), 'r') as handle:
            data = json.loads(handle.read())

        result = utils.parse_quake_data(data, 'Venezuela')
        self.assertEqual(2, len(result))

    def test_get_quake(self):
        self.bot.get_quake(my_dict=self.data1, country='Venezuela')
        result = self.bot.quake
        expected = 1
        self.assertEqual(expected, len(result))

    def test_get_quake_strange_country(self):
        self.bot.get_quake(my_dict=self.data1, country='Vulcan')
        result = self.bot.quake
        expected = 0
        self.assertEqual(expected, len(result))

    def test_get_quake_from_web(self):
        self.bot.urls = [
            'http://pastebin.com/raw.php?i=0WuxsixK',
        ]
        self.bot.get_quake(country='Venezuela')
        result = self.bot.quake
        expected = 1
        self.assertEqual(expected, len(result))

    def test_get_quake_no_country(self):
        self.assertRaises(NoCountryError, self.bot.get_quake, self.data1)

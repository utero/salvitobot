import datetime
import unittest
import os
import json

import salvitobot
from salvitobot import utils
from salvitobot.exceptions import NoCountryError
from salvitobot.exceptions import ProcedureError


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.cwd = os.path.abspath(os.path.dirname(__file__))
        self.bot = salvitobot.Bot()

        with open(os.path.join(self.cwd, 'Quake', '1.json'), 'r') as handle:
            self.data1 = json.loads(handle.read())

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

    def test_is_new_quake(self):
        self.bot.get_quake(my_dict=self.data1, country='Venezuela')
        expected = True
        result = self.bot.is_new_quake()
        self.assertEqual(expected, result)

    def test_is_new_quake_false_empty(self):
        self.bot.get_quake(my_dict=self.data1, country='Narnia')
        result = self.bot.is_new_quake()
        self.assertFalse(result)

    def test_is_new_quake_false_in_db(self):
        item = {
            'longitude': 126.3037,
            'time': 1423215548040,
            'latitude': 9.5166,
            'country': 'cortes',
            'place': '28km NNE de Cortes, Philippines',
            'tuit': 'SISMO. 4.8 grados mb en 28km NNE de Cortes, Philippines. A horas  http://earthquake.usgs.gov/earthquakes/eventpage/usc000tmn4',
            'type': 'earthquake',
            'magnitude_type': 'mb',
            'detail': 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/usc000tmn4.geojson',
            'link': 'http://earthquake.usgs.gov/earthquakes/eventpage/usc000tmn4',
            'code': 'c000tluz',
            'depth': 84.37,
            'datetime_utc': datetime.datetime(2015, 2, 6, 9, 39, 8, 39999),
            'tz': 480,
            'magnitude': 4.8,
        }
        utils.save_to_db(item, test=True)
        self.bot.get_quake(my_dict=self.data1, country='Venezuela')
        expected = False
        result = self.bot.is_new_quake(test=True)
        self.assertEqual(expected, result)

    def test_is_new_quake_no_country(self):
        self.assertRaises(ProcedureError, self.bot.is_new_quake)

    def test_extract_nearby_cities(self):
        country = 'Venezuela'
        self.bot.get_quake(my_dict=self.data1, country=country)
        result = utils.extract_nearby_cities(self.bot.quake[0], country)
        expected = "a 2 km al SO de Umuquena, a 18 km al E de La Fria y a 31 km al NE de San Juan de Colon"
        self.assertEqual(expected, result)

    def test_write_post_no_country(self):
        self.assertRaises(ProcedureError, self.bot.write_stories)

    def test_write_post_nothing_to_post(self):
        self.bot.get_quake(self.data1, country='Venezuela')
        self.bot._quakes_to_write = []
        expected = "Nothing to do."
        result = self.bot.write_stories()
        self.assertEqual(expected, result)

    def test_write_post(self):
        self.bot.get_quake(self.data1, country='Venezuela')
        self.bot.is_new_quake()
        self.bot.write_stories()
        result = self.bot.stories
        self.assertTrue(len(result) > 0)

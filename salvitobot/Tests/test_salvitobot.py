#-*- coding: utf-8 -*-
import unittest

from salvitobot.lib import DataExtractor


class SalvitoTest(unittest.TestCase):

    def test_data_extractor_magnitude(self):
        json_file = "1405369502.25.json"
        magnitude = "5.5"
        result = DataExtractor("http://aniversarioperu.me/salvitobot/1405371303.23.json")
        self.assertEqual(magnitude, result)

#-*- coding: utf-8 -*-
import unittest

from salvitobot.lib import DataExtractor


class SalvitoTest(unittest.TestCase):

    def test_data_extractor_magnitude(self):
        json_file = "1405369502.25.json"
        magnitude = "5.5"
        result = DataExtractor(json_file).magnitude
        self.assertEqual(magnitude, result)

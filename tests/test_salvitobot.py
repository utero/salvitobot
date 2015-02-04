import unittest

from salvitobot.lib import DataExtractor
from salvitobot.lib import tuit


class SalvitoTest(unittest.TestCase):

    def test_data_extractor_magnitude(self):
        magnitude = 5.5
        url = "http://aniversarioperu.me/salvitobot/1405371303.23.json"
        result = DataExtractor(url).get_items()
        result = result[0]['magnitud']
        self.assertEqual(magnitude, result)

    def test_tuit(self):
        url = "http://aniversarioperu.me/salvitobot/1405371303.23.json"
        lista = DataExtractor(url).get_items()
        debug = 1
        tuit(lista, debug)


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)

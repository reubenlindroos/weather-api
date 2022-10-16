import unittest

import api_calls


class TestApiCalls(unittest.TestCase):
    def setUp(self):
        self.handler = api_calls.APIHandler(56)

    def testGetCitiesCallType(self):
        self.assertEqual(type(self.handler.get_cities()), list)

    def testGetCitiesCallLength(self):
        self.assertNotEqual(len(self.handler.get_cities()), 0)

    def testGetWeather(self):
        self.assertIsNotNone(self.handler.get_weather("bath"))

    def testGetSingleVal(self):
        self.assertEqual(len(self.handler.get_val("bath","temperature","wednesday",9)),1)

    def testGetKeyVal(self):
        self.assertIsNotNone(len(self.handler.get_val("bath","temperature")))

    def testUpperCase(self):
        self.assertIsNotNone(self.handler.get_val("BATH","TEMPERATURE"))


if __name__ == '__main__':
    unittest.main()

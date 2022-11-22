import unittest
from src.data import get_prices, save_prices, get_today_prices, today_day


class TestQuery(unittest.TestCase):
    def test_wrong_query(self):

        self.assertIsNone(get_prices(99999), None)

    def test_correct_query(self):

        today_prices_from_bd = get_today_prices(db_format=True)[today_day()]

        today_prices_from_api = get_prices((today_day()))

        self.assertEqual(today_prices_from_bd, today_prices_from_api)

if __name__ == '__main__':
    unittest.main()

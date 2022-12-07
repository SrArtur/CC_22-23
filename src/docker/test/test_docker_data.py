import unittest
from docker_data import convert_to_kwh, parse_date
from iso8601 import is_iso8601


class TestData(unittest.TestCase):

    def test_correct_covert_to_kwh(self):
        data = 195.4
        data2 = 195.688
        data3 = 000.009

        result = convert_to_kwh(data)
        result2 = convert_to_kwh(data2)
        result3 = convert_to_kwh(data3)

        self.assertEqual(result, 0.1954)
        self.assertEqual(result2, 0.19569)
        self.assertEqual(result3, 1e-05)

    def test_wrong_parse_date(self):

        wrong_date = "2022-11-0820:16:37.000+01:00"

        self.assertFalse(is_iso8601(wrong_date))

    def test_correct_parse_date(self):
        date = "2022-11-08T20:16:37.000+01:00"

        self.assertTrue(is_iso8601(date))

        self.assertDictEqual(parse_date(date),
                             {'year': '2022', 'month': '11', 'day': '08', 'hour': '20'})
        self.assertDictEqual(parse_date(date, simplify=True),
                             {'month': '11', 'day': '08', 'hour': '20'})


if __name__ == '__main__':
    unittest.main()

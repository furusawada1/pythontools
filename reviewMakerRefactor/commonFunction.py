from datetime import date, datetime


def convert_to_date(date_input):
    """datetime形式、date形式、またはstr形式の日時情報を入力として、date形式を返す関数"""
    if date_input is None:
        print("警告: 入力がNoneです。1970-01-01を返します。")
        return date(1970, 1, 1)

    if isinstance(date_input, datetime):
        return date_input.date()
    elif isinstance(date_input, date):
        return date_input
    elif isinstance(date_input, str):
        try:
            parsed_date = datetime.strptime(date_input, "%Y-%m-%d")
        except ValueError:
            try:
                parsed_date = datetime.strptime(date_input, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                print("無効な日付形式です。YYYY-MM-DDまたはYYYY-MM-DD hh:mm:ss形式で入力してください。")
                return None
        return parsed_date.date()
    else:
        print("無効な入力です。datetime形式、date形式、またはstr形式を使用してください。")
        return None

import unittest
from datetime import datetime, date

class TestConvertToDate(unittest.TestCase):
    def test_convert_to_date_with_datetime(self):
        input_date = datetime(2022, 1, 1, 12, 0, 0)
        expected_date = date(2022, 1, 1)
        self.assertEqual(convert_to_date(input_date), expected_date)

    def test_convert_to_date_with_date(self):
        input_date = date(2022, 1, 1)
        expected_date = date(2022, 1, 1)
        self.assertEqual(convert_to_date(input_date), expected_date)

    def test_convert_to_date_with_valid_string(self):
        input_date = "2022-01-01"
        expected_date = date(2022, 1, 1)
        self.assertEqual(convert_to_date(input_date), expected_date)

    def test_convert_to_date_with_valid_string_and_time(self):
        input_date = "2022-01-01 12:00:00"
        expected_date = date(2022, 1, 1)
        self.assertEqual(convert_to_date(input_date), expected_date)

    def test_convert_to_date_with_invalid_string(self):
        input_date = "invalid date"
        self.assertIsNone(convert_to_date(input_date))

    def test_convert_to_date_with_none(self):
        input_date = None
        expected_date = date(1970, 1, 1)
        self.assertEqual(convert_to_date(input_date), expected_date)

    def test_convert_to_date_with_invalid_type(self):
        input_date = 12345
        self.assertIsNone(convert_to_date(input_date))


if __name__ == "__main__":
    unittest.main()

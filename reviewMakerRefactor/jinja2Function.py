import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, escape


class DateFilterUtility:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader("templates"))
        self.register_filters()

    def newline_to_indent(self, text):
        return text.replace("\n", "\n    ")

    def convert_to_date(self, date_str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None

    def apply_convert_to_date_without_time(self, date_str):
        dt = self.convert_to_date(date_str)
        if dt:
            return dt.strftime("%Y-%m-%d")
        return None

    def apply_convert_to_date_without_seconds(self, date_str):
        dt = self.convert_to_date(date_str)
        if dt:
            return dt.strftime("%Y-%m-%d %H:%M")
        return None

    def get_filename_from_path(self, file_path):
        return os.path.basename(file_path)

    def register_filters(self):
        self.env.filters["newline_to_indent"] = self.newline_to_indent
        self.env.filters["convert_to_date"] = self.convert_to_date
        self.env.filters["convert_to_html"] = escape
        self.env.filters["get_filename_from_path"] = self.get_filename_from_path
        self.env.filters["apply_convert_to_date_without_time"] = self.apply_convert_to_date_without_time
        self.env.filters["apply_convert_to_date_without_seconds"] = self.apply_convert_to_date_without_seconds

# from your_module import DateFilterUtility
# date_filter_util = DateFilterUtility()
# template = date_filter_util.env.get_template("your_template.html")

import unittest
import os
from datetime import datetime

class TestYourModule(unittest.TestCase):
    def test_newline_to_indent(self):
        input_text = "line1\nline2\nline3"
        expected_output = "line1\n    line2\n    line3"
        self.assertEqual(newline_to_indent(input_text), expected_output)

    def test_convert_to_date(self):
        input_date = "2022-01-01 12:00:00"
        expected_date = datetime(2022, 1, 1, 12, 0, 0)
        self.assertEqual(convert_to_date(input_date), expected_date)

    def test_apply_convert_to_date_without_time(self):
        input_date = "2022-01-01 12:00:00"
        expected_date = "2022-01-01"
        self.assertEqual(apply_convert_to_date_without_time(input_date), expected_date)

    def test_apply_convert_to_date_without_seconds(self):
        input_date = "2022-01-01 12:00:00"
        expected_date = "2022-01-01 12:00"
        self.assertEqual(apply_convert_to_date_without_seconds(input_date), expected_date)

    def test_get_filename_from_path(self):
        input_path = "/path/to/file/test.txt"
        expected_filename = "test.txt"
        self.assertEqual(get_filename_from_path(input_path), expected_filename)


if __name__ == "__main__":
    unittest.main()
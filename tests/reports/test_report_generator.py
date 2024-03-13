import datetime
import unittest
from pebblo.reports.html_to_pdf_generator.report_generator import date_formatter, get_file_size


class TestReports(unittest.TestCase):
    def setUp(self):
        self.date_obj = datetime.datetime.strptime(
            "2024-02-02 16:25:07.531509", "%Y-%m-%d %H:%M:%S.%f"
        )
        self.file_size = 2092

    def test_date_formatter(self):
        # Test if date formatter returns correct string
        output_str = date_formatter(self.date_obj)
        assert output_str == "02 February 2024 , 16:25"

    def test_file_size_conversion(self):
        # Test file size conversion
        output_size = get_file_size(self.file_size)
        assert output_size == "2.04 KB"



if __name__ == "__main__":
    unittest.main()

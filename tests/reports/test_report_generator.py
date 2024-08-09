"""
Unit test cases for reports/html_to_pdf_generator/report_generator.py file
"""

import datetime
import time
import unittest
from unittest.mock import Mock, patch

from pebblo.reports.html_to_pdf_generator.report_generator import (
    convert_html_to_pdf,
    date_formatter,
    get_file_size,
    identity_comma_separated,
)


class TestReportGenerator(unittest.TestCase):
    """Class to hold report_generator UT cases"""

    def setUp(self):
        """Setup mock data"""
        self.date_obj = datetime.datetime.strptime(
            "2024-02-02 16:25:07.531509", "%Y-%m-%d %H:%M:%S.%f"
        )
        self.file_size = 2092
        self.authorizedIdentities = ["demo-user-hr", "demo-user-engg"]

    def test_date_formatter(self):
        """Test if date formatter returns correct string"""
        output_str = date_formatter(self.date_obj, True)
        assert output_str == "02 February 2024 , 16:25" + " " + time.localtime().tm_zone

    def test_file_size_conversion(self):
        """Test file size conversion"""
        output_size = get_file_size(self.file_size)
        assert output_size == "2.04 KB"

    def test_identity_comma_separated(self):
        """Test comma separated identities"""
        output_str = identity_comma_separated(self.authorizedIdentities)
        assert output_str == "demo-user-hr, demo-user-engg"

    @patch("jinja2.Environment", return_value=Mock(get_template=Mock()))
    @patch("jinja2.FileSystemLoader")
    def test_convert_html_to_pdf(self, mock_filesystem_loader, mock_environment):
        """Test the convert_html_to_pdf function"""
        # Arrange
        data = {
            "reportSummary": {"findings": "findings"},
            "dataSources": [{"findingsDetails": "details"}],
            "loadHistory": {"history": "history"},
            "pebbloClientVersion": "client_version",
            "pebbloServerVersion": "server_version",
            "clientVersion": {},
        }
        output_path = "output_path"
        template_name = "template_name"
        search_path = "search_path"
        renderer = "renderer"
        mock_pdf_converter = Mock()

        with patch.dict(
            "pebblo.reports.html_to_pdf_generator.report_generator.library_function_mapping",
            {renderer: mock_pdf_converter},
        ):
            # Act
            convert_html_to_pdf(data, output_path, template_name, search_path, renderer)

        # Assert
        mock_filesystem_loader.assert_called_once_with(searchpath=search_path)
        mock_environment.assert_called_once_with(
            loader=mock_filesystem_loader.return_value
        )
        mock_environment.return_value.get_template.assert_called_once_with(
            template_name
        )
        mock_pdf_converter.assert_called_once()
        mock_pdf_converter.assert_called_once_with(
            mock_environment.return_value.get_template.return_value.render.return_value,
            output_path,
            search_path,
        )


if __name__ == "__main__":
    unittest.main()

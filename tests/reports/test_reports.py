import pytest
from pathlib import Path
from pebblo.reports.enums.report_libraries import ReportLibraries
from pebblo.reports.reports import Reports

@pytest.fixture
def convert_html_to_pdf(mocker):
    """
    Mock the convert_html_to_pdf function
    """
    return mocker.patch("pebblo.reports.reports.convert_html_to_pdf", return_value=[True, ""])

def test_generate_report(convert_html_to_pdf):
    # Get the template path
    template_path = (
        str(Path(__file__).parent.parent.parent.absolute())
        + "/pebblo/reports/templates/"
    )

    # Call the generate_report method
    Reports.generate_report(
        data={},
        output_path="./report.pdf",
        format_string="pdf",
        renderer=ReportLibraries.XHTML2PDF,
    )

    # Assert that the mock function was called with the correct arguments
    convert_html_to_pdf.assert_called_once_with(
        {},
        "./report.pdf",
        template_name="xhtml2pdfTemplate.html",
        search_path=template_path,
        renderer=ReportLibraries.XHTML2PDF,
    )

def test_generate_report_with_wrong_format_string(convert_html_to_pdf):
    # Call the generate_report method with wrong format_string
    Reports.generate_report(
        data={},
        output_path="./report.pdf",
        format_string="wrong_format",
        renderer=ReportLibraries.XHTML2PDF,
    )

    # Assert that the mock function was not called
    convert_html_to_pdf.assert_not_called()


def test_generate_report_with_wrong_renderer(convert_html_to_pdf):
    # Call the generate_report method with wrong renderer
    Reports.generate_report(
        data={},
        output_path="./report.pdf",
        format_string="pdf",
        renderer="wrong_renderer",
    )

    # Assert that the mock function was not called
    convert_html_to_pdf.assert_not_called()


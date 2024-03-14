"""
Defines functions to generate PDF from HTML for respective renderers
"""

import os


# Creates PDF from template using weasyprint
def weasyprint_pdf_converter(source_html, output_path, search_path):
    """PDF generator function for weasyprint renderer"""
    try:
        from weasyprint import CSS, HTML

        base_url = os.path.dirname(os.path.realpath(__file__))
        html_doc = HTML(string=source_html, base_url=base_url)
        result = html_doc.write_pdf(
            target=output_path, stylesheets=[CSS(search_path + "/index.css")]
        )
        return True, result
    except ImportError:
        error = """Could not import weasyprint package. Please install weasyprint and Pango to generate report using weasyprint.
          Follow documentation for more details - https://daxa-ai.github.io/pebblo/installation"
        """
        return False, error
    except Exception as e:
        return False, e


# Creates PDF from template using xhtml2pdf
def xhtml2pdf_pdf_converter(source_html, output_path, _):
    """PDF generator function for xhtml2pdf renderer"""
    try:
        from xhtml2pdf import pisa

        with open(output_path, "w+b") as result_file:
            pisa_status = pisa.CreatePDF(src=source_html, dest=result_file)
            result_file.close()
            return True, pisa_status.err
    except Exception as e:
        return False, e

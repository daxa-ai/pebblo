import os
from pebblo.app.utils.utils import get_full_path
from pebblo.app.libs.logger import logger


def validate_config_details(config_dict):
    SUPPORTED_RENDERERS = ['weasyprint', 'xhtml2pdf']
    SUPPORTED_FORMATS = ['pdf']

    reports_config = config_dict.get('reports', {})

    # Check if the renderer is supported
    if reports_config.get('renderer') not in SUPPORTED_RENDERERS:
        raise ValueError('Unsupported renderer specified in the configuration')

    # Check if the format is supported
    if reports_config.get('format') not in SUPPORTED_FORMATS:
        raise ValueError('Unsupported format specified in the configuration')

    # Verify the existence of the specified path
    output_dir_path = get_full_path(reports_config.get('format'))
    if not os.path.exists(output_dir_path):
        raise FileNotFoundError(f"The path '{output_dir_path}' specified for the outputDir does not exist")
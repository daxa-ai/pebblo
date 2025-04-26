import datetime
import os
import tempfile
import uuid
from pathlib import Path
from typing import List, Tuple

from fastapi import APIRouter, Form, Response, UploadFile, File
from fastapi.responses import JSONResponse
from langchain.text_splitter import RecursiveCharacterTextSplitter
from unstructured.partition.auto import partition

from pebblo.app.api.api import App
from pebblo.app.api.req_models import Framework, ReqDiscover, ReqLoaderDoc, Runtime
from pebblo.app.config.config import var_server_config_dict
from pebblo.log import get_logger

# Initialize logger
logger = get_logger(__name__)
config_details = var_server_config_dict.get()

router = APIRouter(prefix="/tools")
os.environ["OCR_AGENT"] = (
    "unstructured.partition.utils.ocr_models.paddle_ocr.OCRAgentPaddle"
)


@router.post("/scan", operation_id="get_sensitive_data_report")
async def sensitive_data_report(folder_path: str, output_path: str = None):
    """
    Processes a given folder to generate a sensitive data report.

    Args:
        folder_path (str): Path to the folder containing files to scan for sensitive data.
        output_path (str, optional): Path where intermediate files or outputs can be stored.
                                     If not provided, defaults will be used.

    Returns:
        JSON/dict: Report content if successful, or an error message with status 500 if an exception occurs.
    """
    try:
        # Create output directory if it doesn't exist
        if output_path and not os.path.exists(output_path):
            os.makedirs(output_path)

        all_files = []
        
        # Walk through all files in the folder recursively
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                # Only add valid files, ignore system files like .DS_Store
                if os.path.isfile(full_path) and not full_path.endswith(".DS_Store"):
                    all_files.append(full_path)

        # Parse the collected files to extract app name and load ID
        app_name, load_id = parse_files(all_files)

        # Determine the base path where reports are stored (fallback to current directory)
        base_path = os.path.expanduser(
            config_details.get("reports", {}).get("cacheDir", ".")
        )
        
        # Construct the full path to the report based on app name and load ID
        report_base = Path(base_path) / app_name / load_id

        # Serve the generated report
        op = serve_report(report_base / "report.json", app_name, "json")

        return op

    except Exception as e:
        # Return error response if any exception occurs
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

 

@router.post("/document_report")
async def document_report(
    files: List[UploadFile], output_format: str = Form(default="json")
):
    """Processes uploaded documents and generates reports in JSON or PDF format.

    Args:
        files (List[UploadFile]): List of uploaded files.
        output_format (str, optional): Report format ('json' or 'pdf'). Defaults to "json".

    Returns:
        JSONResponse | Response: JSON report or downloadable PDF report.
    """
    if output_format not in ["json", "pdf"]:
        return JSONResponse(
            {"error": "Invalid output_format. Choose 'json' or 'pdf'."}, status_code=400
        )

    temp_dir = tempfile.mkdtemp()
    saved_files = []

    try:
        for file in files:
            file_path = Path(temp_dir) / file.filename
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            saved_files.append(str(file_path))

        app_name, load_id = parse_files(saved_files)

        # Determine report path based on format
        base_path = os.path.expanduser(
            config_details.get("reports", {}).get("cacheDir", ".")
        )
        report_base = Path(base_path) / app_name
        if output_format == "pdf":
            return serve_report(report_base / "pebblo_report.pdf", app_name, "pdf")
        return serve_report(report_base / "report.json", app_name, "json")
    finally:
        # Cleanup temporary directory
        for file in saved_files:
            os.remove(file)
        os.rmdir(temp_dir)


def serve_report(report_path: Path, app_name: str, format_type: str):
    """Serves the report in the requested format.

    Args:
        report_path (Path): Path to the report file.
        app_name (str): Application name.
        format_type (str): 'json' or 'pdf'.

    Returns:
        JSONResponse | Response: JSON report or downloadable PDF report.
    """

    if not report_path.exists():
        logger.error(f"{format_type.upper()} report not found in {report_path}")
        return JSONResponse(
            {"error": f"{format_type.upper()} report not found in {report_path}"},
            status_code=404,
        )

    with open(report_path, "rb" if format_type == "pdf" else "r") as file:
        logger.info(f"Serving {format_type.upper()} report from {report_path}")
        content = file.read()

    if format_type == "pdf":
        logger.info(f"Serving PDF report from {report_path}")
        return Response(
            content=content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={app_name}_report.pdf",
                "X-App-Name": app_name,
            },
        )

    return JSONResponse(
        {"app_name": app_name, "output_format": format_type, "json_content": content}
    )


def extract_text(file_path: str) -> str:
    """Extracts text from a file using PaddleOCR for PDFs or Unstructured for other formats.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: Extracted text content.
    """
    # Use Unstructured for files
    elements = partition(file_path, infer_table_structure=True, strategy="hi_res")
    return " ".join(element.text for element in elements if element.text)


def parse_files(file_paths: List[str]) -> Tuple[str, str]:
    """Processes the uploaded files and generates document reports.

    Args:
        file_paths (List[str]): List of file paths.

    Returns:
        Tuple[str, str]: (app_name, load_id)
    """
    os.environ["SCARF_NO_ANALYTICS"] = "true"
    postfix = str(uuid.uuid4())[:8]

    app = App(prefix="/tools")
    app_name = f"doc-report-{postfix}"
    load_id = f"load-doc-report-{postfix}"

    # Register the app
    app_discover = ReqDiscover(
        name=app_name,
        owner="Joe Smith",
        description="Document report",
        plugin_version="0.0.1",
        runtime=Runtime(
            type="local",
            host="localhost",
            path="/tools",
            platform="mac",
            os="macOS",
            os_version="14.0",
            language="python",
            language_version="3.11",
        ),
        framework=Framework(name="doc-reporter-tool", version="0.0.1"),
        load_id=load_id,
    )
    app.discover_direct(data=app_discover)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)

    for idx, file_path in enumerate(file_paths):
        full_text = extract_text(file_path)
        chunks = text_splitter.split_text(full_text)
        logger.info(f"length of chunks {len(chunks)} for file {file_path}")
        docs = [
            {
                "doc": chunk,
                "source_path": file_path,
                "pb_id": str(uuid.uuid4()),
                "last_modified": datetime.datetime.now(),
                "file_owner": "Joe Smith",
                "loader_source_path": file_path,
                "source_size": len(chunk),
                "authorized_identities": ["joe@acmecorp.com"],
            }
            for chunk in chunks
        ]

        loader_doc = ReqLoaderDoc(
            name=app_name,
            owner="Joe Smith",
            docs=docs,
            plugin_version="0.0.1",
            load_id=load_id,
            loader_details={
                "loader": "doc-reporter-tool",
                "source_path": os.path.basename(file_path),
                "source_type": "file",
            },
            loading_end=(idx == len(file_paths) - 1),
            source_owner="Joe Smith",
            classifier_location="local",
            classifier_mode="all",
            anonymize_snippets=False,
        )
        app.loader_doc_direct(data=loader_doc)

    return app_name, load_id

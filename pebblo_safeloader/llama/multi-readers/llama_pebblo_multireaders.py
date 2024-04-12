"""
Use this script to safely read/load your pdf, doc, csv files using llama readers.
Usage:
python3 llama_pebblo_multilreaders.py --reader_type
<PDFReader/CSVReader/DocxReader> --input
<input_file/directory_path>
"""

import argparse
import os
from pathlib import Path

import shortuuid
from llama_index.readers.file import CSVReader, DocxReader, PDFReader
from llama_index.readers.pebblo import PebbloSafeReader

CSV_READER = "CSVReader"
PDF_READER = "PDFReader"
DOC_READER = "DocxReader"


def get_reader(reader_type):
    """Reaer factory function"""
    reader_factory = {
        CSV_READER: CSVReader,
        PDF_READER: PDFReader,
        DOC_READER: DocxReader,
    }
    return reader_factory[reader_type]


def pebblo_safe_read_documents(reader_type, input_path):
    """Read document using pebblo safe reader"""
    pebblo_url = os.environ.get("PEBBLO_CLASSIFIER_URL", "http://localhost:8000")
    pebblo_reader_app = f"llama-pebblo-demo-{reader_type}-{shortuuid.uuid()[:5]}"
    description = "Pebblo-Llama Integration"
    owner = "Yograj Shisode"
    reader_cls = get_reader(reader_type)
    reader_obj = reader_cls()
    pebblo_reader = PebbloSafeReader(
        reader_obj, name=pebblo_reader_app, owner=owner, description=description
    )
    pebblo_reader.load_data(file=Path(input_path))
    print(
        f"Please visit {pebblo_url}/pebblo/app/?app_name={pebblo_reader_app} for report"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r",
        "--reader_type",
        required=True,
        choices=[CSV_READER, PDF_READER, DOC_READER],
        help="Select reader type",
    )
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Input file or directory path to read/load.",
    )
    args = parser.parse_args()
    reader = args.reader_type
    input_doc_path = args.input
    pebblo_safe_read_documents(reader, input_doc_path)

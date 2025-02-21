#!/usr/bin/env python3

import argparse
import sys

from reporter.reporter import analyze_files


def main():
    parser = argparse.ArgumentParser(
        description="Data Governance Report Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s -f document1.pdf document2.pdf
    %(prog)s -f *.pdf -o pdf
    %(prog)s -f document.pdf -u http://localhost:8000/tools/document_report
        """,
    )

    parser.add_argument(
        "-f", "--files", required=True, nargs="+", help="One or more files to analyze"
    )

    parser.add_argument(
        "-o",
        "--output-format",
        choices=["json", "pdf"],
        default="json",
        help="Output format for the report (default: json)",
    )

    parser.add_argument(
        "-u",
        "--url",
        default="http://localhost:8000/tools/document_report",
        help="API endpoint URL (default: http://localhost:8000/tools/document_report)",
    )

    args = parser.parse_args()

    # Validate URL
    if not args.url.startswith(("http://", "https://")):
        print(
            f"Error: Invalid URL '{args.url}'. URL must start with http:// or https://"
        )
        sys.exit(1)

    try:
        analyze_files(args.url, args.files, args.output_format)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

import argparse
import os

import requests
from requests.exceptions import RequestException


def analyze_files(api_url, file_paths, output_format):
    """
    Uploads files to the specified FastAPI endpoint and saves the resulting report.

    :param api_url: The API endpoint URL
    :param file_paths: List of paths to files to upload
    :param output_format: Desired output format for the report
    """
    # Validate all files exist and are readable first
    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' does not exist.")
            return
        if not os.access(file_path, os.R_OK):
            print(f"Error: File '{file_path}' is not readable.")
            return

    try:
        print("1. Analyzing files...", end=" ", flush=True)

        # Prepare files for upload
        files = []
        for file_path in file_paths:
            files.append(
                ("files", (os.path.basename(file_path), open(file_path, "rb")))
            )

        # Make the request
        response = requests.post(
            api_url, files=files, data={"output_format": output_format}
        )

        if response.ok:
            print("successful")

            # Handle PDF response
            if output_format == "pdf":
                # Extract metadata from headers
                app_name = response.headers.get("X-App-Name")

                # Save the PDF
                output_path = f"{app_name}_report.pdf" if app_name else "report.pdf"

                with open(output_path, "wb") as f:
                    f.write(response.content)

                # print(f"PDF report saved to: {output_path}")
                # print(f"Metadata:")
                # print(f"  App Name: {app_name}")

            # Handle JSON response
            else:
                response_data = response.json()
                if response_data.get("json_content"):
                    output_path = f"{response_data['app_name']}_report.json"

                    with open(output_path, "w") as f:
                        f.write(response_data["json_content"])

            print(f"2. Saving report at {output_path}")

        else:
            print("failed")
            print(f"Error: Upload failed with status code {response.status_code}")
            try:
                print("Error Details:", response.json())
            except ValueError:
                print("Response (not JSON):", response.text)

    except RequestException as e:
        print("failed")
        print(f"Error: An error occurred during the request: {e}")

    finally:
        # Close all files
        for file_tuple in files:
            try:
                file_tuple[1][1].close()
            except Exception:
                pass


if __name__ == "__main__":
    # Create an argument parser for CLI usage
    parser = argparse.ArgumentParser(description="Upload files to the FastAPI server.")
    parser.add_argument(
        "-u",
        "--url",
        required=False,
        type=str,
        help="The FastAPI endpoint URL (e.g., http://127.0.0.1:8000/tools/document_report)",
        default="http://localhost:8000/tools/document_report",
    )
    parser.add_argument(
        "-f",
        "--files",
        required=True,
        nargs="+",
        type=str,
        help="One or more files to upload",
    )
    parser.add_argument(
        "-o",
        "--output-format",
        required=False,
        type=str,
        choices=["json", "pdf", "html", "markdown"],  # Add or modify formats as needed
        default="json",
        help="Specify the desired output format for the report",
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    # Validate URL
    if not args.url.startswith(("http://", "https://")):
        print(
            f"Error: Invalid URL '{args.url}'. Ensure it starts with http:// or https://."
        )
        exit(1)

    # Call the upload function
    analyze_files(args.url, args.files, args.output_format)

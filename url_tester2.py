# filename: url_tester.py

import os
import requests
from datetime import datetime
import hashlib  # for hashing content
import argparse  # for parsing command-line arguments

def test_urls(urls, output_file):
    """
    Test URLs without caching and save the results to a separate file.

    Args:
        urls (list): List of URLs to test.
        output_file (str): Path to the output file.

    Returns:
        None
    """

    # Input validation
    if not isinstance(urls, list) or len(urls) == 0:
        raise ValueError("Invalid input: 'urls' must be a non-empty list")
    if not isinstance(output_file, str):
        raise ValueError("Invalid input: 'output_file' must be a string")

    try:
        # Create the output file
        with open(output_file, "w") as f:
            for url in urls:
                try:
                    # Send an HTTP request without caching
                    headers = {"Cache-Control": "no-cache", "Pragma": "no-cache"}
                    response = requests.get(url, headers=headers)

                    # Check if the URL is valid
                    if not response.url.startswith('http'):
                        raise Exception("Invalid URL")

                    # Calculate content hash only for specified URLs
                    if url in urls:
                        content_hash = hashlib.sha256(response.content).hexdigest()
                        print(f"Content hash for {url}: {content_hash}")

                    else:
                        result = f"{url}: Failed (URL not found)\n"

                except Exception as e:
                    result = f"{url}: Error - {str(e)}\n"
                finally:
                    # Write the test result to the output file
                    with open(output_file, "a") as f_out:
                        if 'result' in locals():
                            f_out.write(result)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test URLs without caching")
    parser.add_argument("urls", nargs="+", help="One or more URLs to test")
    args = parser.parse_args()

    output_file = "test_results.txt"
    test_urls(args.urls, output_file)


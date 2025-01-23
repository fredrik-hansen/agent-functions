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

                    # Check the status code
                    if response.status_code == 200:
                        result = f"{url}: OK\n"
                        content_hash = hashlib.sha256(response.content).hexdigest()
                        print(f"Content hash for {url}: {content_hash}")

                        # Compare with earlier test results (if available)
                        compare_with_earlier_test(output_file, url, content_hash)

                    else:
                        result = f"{url}: {response.status_code}\n"

                except requests.exceptions.RequestException as e:
                    # Handle request exceptions (e.g., connection errors)
                    result = f"{url}: Error ({str(e)})\n"

                # Write the result to the output file
                f.write(result)

    except OSError as e:
        # Handle OS-related errors (e.g., permission denied, disk full)
        print(f"Error writing to {output_file}: {str(e)}")

def compare_with_earlier_test(output_file, url, content_hash):
    """
    Compare the current test result with earlier test results.

    Args:
        output_file (str): Path to the output file.
        url (str): URL being tested.
        content_hash (str): Hash of the response content.

    Returns:
        None
    """

    try:
        # Read earlier test results from a separate file
        earlier_test_results = {}
        with open(output_file + ".earlier", "r") as f:
            for line in f.readlines():
                url, hash_value = line.strip().split(": ")
                earlier_test_results[url] = hash_value

    except FileNotFoundError:
        # No earlier test results available; create a new file
        print("No earlier test results found. Creating a new file.")
        with open(output_file + ".earlier", "w") as f:
            pass
        return

    if url in earlier_test_results and content_hash != earlier_test_results[url]:
        # Content has changed since the last test!
        print(f"Content for {url} has changed!")

    elif any(content_hash == hash_value for hash_value in earlier_test_results.values()):
        # This URL's content matches another URL's content
        matching_urls = [u for u, h in earlier_test_results.items() if h == content_hash]
        print(f"{url}'s content matches {', '.join(matching_urls)}")

    with open(output_file + ".earlier", "a") as f:
        # Append the current test result to the file
        f.write(f"{url}: {content_hash}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test URLs without caching")
    parser.add_argument("urls", nargs="+", help="One or more URLs to test")
    args = parser.parse_args()

    output_file = "test_results.txt"
    test_urls(args.urls, output_file)


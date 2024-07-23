#!/usr/bin/env python3

import sys
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def remove_param_values(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    # Remove the values of all parameters
    for param in query_params:
        query_params[param] = ['']

    new_query = urlencode(query_params, doseq=True)
    new_url = urlunparse(parsed_url._replace(query=new_query))
    return new_url

def process_urls(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            url = line.strip()
            if not url:
                continue

            parsed_url = urlparse(url)
            if parsed_url.query:
                new_url = remove_param_values(url)
                outfile.write(f'{new_url}\n')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python process_urls.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    process_urls(input_file, output_file)

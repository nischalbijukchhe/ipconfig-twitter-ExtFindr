import os
import re
import subprocess
import argparse
import random

green = '\033[92m'
yellow = '\033[93m'
reset = '\033[0m'
blue = '\033[94m'

pattern = re.compile(r"\.(sql|bak|db|backup|secret|config|yml|yaml|env|ini|conf|properties|pem|key|crt|csr|p12|sqlite|sqlite3|db3|dbf|accdb|mdb|log|swp|swo|dump|json|plist|cfg|cfm|htaccess|htpasswd|cer|der|pfx|p7b|p7c|jks|keystore|rb|py|pl|sh|bash|jar|war|ear|cs|cpp|h|c|passwd|shadow|doc|docx|ppt|pptx|xls|xlsx|odt|ods|odp|pdf|zip|rar|7z|tar\.gz|tgz|tar|gz|bz2|xz|token|kdb|kdbx|gitignore|gitattributes|git/config|git/credentials|dockerignore|Dockerfile|kubeconfig)$")

def get_file_size(url):
    try:
        headers = subprocess.run(f"curl -sI {url}", shell=True, capture_output=True, text=True)
        for line in headers.stdout.splitlines():
            if "Content-Length" in line:
                size = int(line.split(":")[1].strip())
                return size
        return None
    except Exception as e:
        print(f"Error getting size for {url}: {e}")
        return None

def scan_url(url):
    try:
        result = subprocess.run(f"gau {url}", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            output = result.stdout.splitlines()
            found_extensions = []
            for line in output:
                match = pattern.search(line)
                if match:
                    found_extensions.append(line)
            return found_extensions
        else:
            return None
    except Exception as e:
        print(f"Error scanning {url}: {e}")
        return None

def print_and_save_results(url, found_extensions, output_file):
    if found_extensions:
        for ext_url in found_extensions:
            extension = ext_url.split('.')[-1]
            size = get_file_size(ext_url)
            size_info = f"[Size: {size} bytes]" if size else "[Size: Unknown]"
            print(f"{green}{ext_url} [found .{extension}] {size_info}{reset}")
            if output_file:
                with open(output_file, 'a') as f:
                    f.write(f"{ext_url} [found .{extension}] {size_info}\n")
    else:
        print(f"{yellow}{url} [Nothing unusual found]{reset}")

def scan_urls_from_file(file_path, output_file=None):
    with open(file_path, 'r') as f:
        urls = f.readlines()

    print_banner()

    if output_file:
        open(output_file, 'w').close()

    random.shuffle(urls)

    for url in urls:
        url = url.strip()
        if url:
            print(f"{blue}Scanning {url}...{reset}")
            found_extensions = scan_url(url)
            if found_extensions is not None:
                print_and_save_results(url, found_extensions, output_file)

def print_banner():
    banner = """
    _____     _  ______ _           _      
    |  ___|   | | |  ___(_)         | |     
    | |____  _| |_| |_   _ _ __   __| |_ __ 
    |  __\\ \\/ / __|  _| | | '_ \\ / _` | '__|
    | |___>  <| |_| |   | | | | | (_| | |   
    \\____/_/\\_\\\\__\\_|   |_|_| |_|\\__,_|_|   
    """
    print(banner)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bulk scan URLs for high-severity file types and output results.")
    parser.add_argument("-l", "--list", help="File containing list of URLs to scan", required=True)
    parser.add_argument("-o", "--output", help="Output file to save the results")
    args = parser.parse_args()

    scan_urls_from_file(args.list, args.output)

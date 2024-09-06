import os
import re
import requests
import argparse
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

colors = {
    'green': '\033[92m',
    'red': '\033[91m',
    'reset': '\033[0m'
}

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.1.2 Safari/602.3.12',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'
]

pattern = re.compile(r"\.(sql|bak|db|backup|secret|config|yml|yaml|env|ini|conf|properties|pem|key|crt|csr|p12|sqlite|sqlite3|db3|dbf|accdb|mdb|log|swp|swo|dump|json|xml|plist|cfg|cfm|htaccess|htpasswd|cer|der|pfx|p7b|p7c|jks|keystore|js|rb|php|py|pl|sh|bash|jar|war|ear|cs|cpp|h|c|passwd|shadow|doc|docx|ppt|pptx|xls|xlsx|odt|ods|odp|pdf|zip|rar|7z|tar\.gz|tgz|tar|gz|bz2|xz|token|kdb|kdbx|gitignore|gitattributes|git/config|git/credentials|dockerignore|Dockerfile|kubeconfig)$")

def ensure_trailing_slash(url):
    if not url.endswith('/'):
        return url + '/'
    return url

def get_file_size(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=10, headers={'User-Agent': random.choice(user_agents)})
        size = response.headers.get('Content-Length')
        if size:
            return int(size) / 1024
        else:
            response = requests.get(url, stream=True, timeout=10, headers={'User-Agent': random.choice(user_agents)})
            return len(response.content) / 1024
    except requests.RequestException:
        return None

def scan_url(url):
    try:
        response = requests.get(f"https://otx.alienvault.com/otxapi/indicators/url/{url}/url_list", timeout=10, headers={'User-Agent': random.choice(user_agents)})
        urls = response.text.splitlines()
        found_extensions = []
        for line in urls:
            match = pattern.search(line)
            if match:
                found_extensions.append(line)
        return found_extensions
    except requests.RequestException as e:
        print(f"Error scanning {url}: {e}")
        return None

def print_and_save_results(url, found_extensions, output_file):
    if found_extensions:
        for ext_url in found_extensions:
            extension = ext_url.split('.')[-1]
            size = get_file_size(ext_url)
            size_info = f" (Size: {size:.2f} KB)" if size else ""
            print(f"{colors['green']}{ext_url}{colors['reset']} [found .{extension}] {size_info}")
            if output_file:
                with open(output_file, 'a') as f:
                    f.write(f"{ext_url} [found .{extension}] {size_info}\n")
    else:
        print(f"{colors['red']}{url} [Nothing found]{colors['reset']}")

def threaded_scan(url, output_file):
    url = ensure_trailing_slash(url)
    found_extensions = scan_url(url)
    if found_extensions is not None:
        print_and_save_results(url, found_extensions, output_file)
    time.sleep(1)  # Rate limiting to avoid bulk request blocking

def scan_urls_from_file(file_path, output_file=None, max_workers=5):
    with open(file_path, 'r') as f:
        urls = f.readlines()

    urls = [url.strip() for url in urls if url.strip()]
    random.shuffle(urls)

    if output_file:
        open(output_file, 'w').close()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(threaded_scan, url, output_file): url for url in urls}
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                print(f"Error processing {futures[future]}: {exc}")

def show_help():
    help_text = """
    Usage: python extfindr.py -l <url_list_file> [-o <output_file>] [-t <num_threads>]

    Options:
    -l, --list          File containing list of URLs to scan (required)
    -o, --output        Output file to save the results (optional)
    -t, --threads       Number of concurrent threads (optional, default: 5)
    -h, --help          Show this help message
    """
    print(help_text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bulk scan URLs for high-severity file types and output results.", add_help=False)
    parser.add_argument("-l", "--list", help="File containing list of URLs to scan", required=True)
    parser.add_argument("-o", "--output", help="Output file to save the results")
    parser.add_argument("-t", "--threads", type=int, default=5, help="Number of concurrent threads")
    parser.add_argument("-h", "--help", action='store_true', help="Show help message")

    args = parser.parse_args()

    if args.help:
        show_help()
    else:
        scan_urls_from_file(args.list, args.output, max_workers=args.threads)

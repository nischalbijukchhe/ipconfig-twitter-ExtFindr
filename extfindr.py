import os
import re
import subprocess
import argparse

colors = {
    'sql': '\033[91m', 'bak': '\033[93m', 'db': '\033[95m', 'backup': '\033[91m',
    'secret': '\033[91m', 'config': '\033[94m', 'yml': '\033[96m', 'yaml': '\033[96m',
    'env': '\033[92m', 'ini': '\033[92m', 'conf': '\033[94m', 'properties': '\033[94m',
    'pem': '\033[91m', 'key': '\033[91m', 'crt': '\033[91m', 'csr': '\033[91m', 'p12': '\033[93m',
    'reset': '\033[0m', 'bold': '\033[1m', 'blue': '\033[94m', 'green': '\033[92m', 'yellow': '\033[93m'
}

pattern = re.compile(r"\.(sql|bak|db|backup|secret|config|yml|yaml|env|ini|conf|properties|pem|key|crt|csr|p12|pdf)$")

def get_color(extension):
    return colors.get(extension, colors['reset'])

def scan_url(url):
    try:
        result = subprocess.run(f"gau {url}", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            output = result.stdout.splitlines()
            found_extensions = []
            for line in output:
                match = pattern.search(line)
                if match:
                    found_extensions.append(match.group())
            return found_extensions
        else:
            return None
    except Exception as e:
        print(f"Error scanning {url}: {e}")
        return None

def print_colored_results(url, found_extensions):
    if found_extensions:
        for ext in found_extensions:
            color = get_color(ext.split('.')[-1])
            print(f"{colors['green']}{url}{colors['reset']} [found {color}{ext}{colors['reset']}]")
    else:
        print(f"{colors['yellow']}{url} [Nothing found]{colors['reset']}")

def scan_urls_from_file(file_path, output_file=None):
    found_results = []
    with open(file_path, 'r') as f:
        urls = f.readlines()

    print_banner()

    for url in urls:
        url = url.strip()
        if url:
            print(f"{colors['blue']}Scanning {url}...{colors['reset']}")
            found_extensions = scan_url(url)
            if found_extensions is not None:
                print_colored_results(url, found_extensions)
                if found_extensions:
                    found_results.append(f"{url}: {', '.join(found_extensions)}")
    
    if output_file and found_results:
        with open(output_file, 'w') as f:
            f.write("\n".join(found_results))
        print(f"{colors['bold']}Results saved to {output_file}{colors['reset']}")

def print_banner():
    banner = f"""
     {colors['bold']}_____     _  ______ _           _      
    |  ___|   | | |  ___(_)         | |     
    | |____  _| |_| |_   _ _ __   __| |_ __ 
    |  __\\ \\/ / __|  _| | | '_ \\ / _` | '__|
    | |___>  <| |_| |   | | | | | (_| | |   
    \\____/_/\\_\\\\__\\_|   |_|_| |_|\\__,_|_|   
    {colors['reset']}
    """
    print(banner)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bulk scan URLs for high-severity file types and output results.")
    parser.add_argument("-l", "--list", help="File containing list of URLs to scan", required=True)
    parser.add_argument("-o", "--output", help="Output file to save the results")
    args = parser.parse_args()

    scan_urls_from_file(args.list, args.output)

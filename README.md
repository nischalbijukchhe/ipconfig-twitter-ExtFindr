# ExtFindr

**ExtFindr** A simple Python based tool designed to scan URLs for high-severity file extensions. This script leverages `gau` to find URLs, then filters them to identify file types such as `.sql`, `.bak`, `.db`, `.config` and other potentially sensitive extensions. 

## Disclaimer

This tool is intended for educational purposes and ethical security testing only. Unauthorized use of this tool against systems or websites without proper permission is illegal and may result in severe penalties. Always ensure you have explicit permission from the owner of the system or website before running any security scans.

The developers (https://github.com/nav1n0x/ | https://x.com/nav1n0x) of this tool are not responsible for any misuse or damage caused by its use.

## Features

- **High-severity extensions**: Detects important file types like `.sql`, `.bak`, `.db`, `.config`, `.pem`, etc.
- **Supports batch processing**: Scan multiple URLs from a file in one go.
- **Save results**: Optionally export found results to a text file.

![image](https://github.com/user-attachments/assets/e7394be1-9058-4e5a-925b-334f35e37bf7)


## Requirements

- Python 3.x
- [gau](https://github.com/lc/gau)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/nav1n0x/ExtFindr.git
    cd extfindr
    ```
2. Ensure that the required tools (`gau`) is installed.

## Usage

To use **ExtFindr**, follow these steps:

1. Create a text file containing the list of URLs you want to scan. Each URL should be on a new line.

    Example (`urls.txt`):
    ```
    https://example.com
    https://targetsite.com
    https://vulnerablewebsite.com
    ```
2. Run the script with the `-l` flag to specify your URL list and optionally use the `-o` flag to save results to a file:
    ```bash
    python extfindr.py -l urls.txt -o results.txt
    ```
    - **`-l`**: Specify the input file with URLs.
    - **`-o`**: (Optional) Output file to save the results.

### Example

```bash
python extfindr.py -l urls.txt -o found_results.txt
```

```bash
python extfindr.py -h

Usage: python extfindr.py -l <url_list_file> [-o <output_file>] [-t <num_threads>]

Options:
-l, --list          File containing list of URLs to scan (required)
-o, --output        Output file to save the results (optional)
-t, --threads       Number of concurrent threads (optional, default: 5)
-h, --help          Show this help message
```
## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
Happy scanning! 🚀
```

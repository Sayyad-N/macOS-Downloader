# macOS Downloader V1.1.1

This repository contains scripts and tools to download macOS recovery images and macOS installation images. The tools are designed to help users easily obtain the necessary files for macOS recovery and installation.

## Files

### `boards.json`
This file contains a mapping of Mac board IDs to their respective macOS versions. It is used by the `macrecovery.py` script to determine which macOS version to download for a given board ID.

### `macrecovery.py`
This script is used to gather recovery information for Macs and download the necessary recovery images. It supports various macOS versions and can verify the integrity of downloaded images.

### `build-image.sh`
This script is used to create a macOS recovery image. It handles the creation, partitioning, and conversion of the recovery image.

### `start.py`
This script provides a user-friendly interface to download macOS recovery images and macOS installation images. It includes options to check the availability of required files, download recovery images, and download installation images.

## Usage

### Prerequisites
- Python 3.x
- Required Python libraries: `pyperclip`, `webbrowser`

### Installing Required Libraries
To install the required Python libraries, run:
```sh
pip install python-barcode pyperclip
```

### Running the Scripts

1. **Check File Paths**
    Select the option to check file paths to ensure all required files are available.

2. **Download macOS Recovery**
    Select the option to download macOS recovery. Follow the prompts to choose the desired macOS version.

3. **Download macOS Image**
    Select the option to download macOS image. Follow the prompts to choose the desired macOS version.

## License
This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

## Required Libraries

### `pyperclip`
This library is used to copy text to the clipboard. It is required for copying download URLs in the `start.py` script.

### `webbrowser`
This library is used to open URLs in the default web browser. It is required for opening download links in the `start.py` script.

## Author
- SayyadN 

## Resources
- macrecovery_open_core : https://tinyurl.com/bdfkbw43
- olarila_vanilla_images: https://tinyurl.com/mr442fz6
- olarila_efis : https://tinyurl.com/rkr3w93n
  


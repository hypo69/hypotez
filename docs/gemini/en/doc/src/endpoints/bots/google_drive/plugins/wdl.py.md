# Module for downloading files using `wget` 
## Overview

This module provides a function for downloading files from a given URL using the `wget` command. It handles basic error handling and returns the downloaded filename.

## Details

This code is used in the `hypotez` project for downloading WDL (Workflow Description Language) files from a URL. The `wget` command is a popular tool for downloading files from the internet, and this function provides a wrapper to simplify this process within the `hypotez` context. 

## Functions

### `wget_dl`
**Purpose**: This function downloads a file from a given URL using the `wget` command. It extracts the filename from the URL and attempts to download the file.

**Parameters**:

- `url` (str): The URL of the file to download.

**Returns**:

- str: The downloaded filename if successful, otherwise it returns a tuple containing "error" and the attempted filename.

**Raises Exceptions**:

- `Exception`: If any error occurs during the download process.

**How the Function Works**:

- The function first extracts the filename from the URL using `os.path.basename`.
- Then it constructs a `wget` command using the extracted filename and the provided URL.
- The `subprocess.check_output` function is used to execute the `wget` command. 
- If the download is successful, the function returns the filename. Otherwise, it logs the error and returns a tuple indicating the error and the attempted filename.

**Examples**:

```python
# Example 1: Successful download
filename = wget_dl("https://www.example.com/file.wdl")
print(f"File downloaded: {filename}") # Output: File downloaded: file.wdl

# Example 2: Error during download
filename, attempted_filename = wget_dl("https://www.example.com/invalid_url")
print(f"Error: Could not download file: {attempted_filename}") # Output: Error: Could not download file: invalid_url
```
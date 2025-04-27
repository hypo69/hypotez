# Tiny Utils

## Overview

**Tiny Utils** is a library of utilities providing a set of lightweight helper functions for various common tasks. The library includes utilities for data format conversion, text and file processing, string operations, date and time formatting, image processing, and more. It's organized into several modules for easy access to specific functionalities.

## Table of Contents

- [Tiny Utils](#tiny-utils)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Modules Overview](#modules-overview)
  - [Module Descriptions](#module-descriptions)
    - [Converters](#converters)
      - [Files:](#files)
    - [String Utilities](#string-utilities)
    - [File Handling Utilities](#file-handling-utilities)
    - [Date and Time Utilities](#date-and-time-utilities)
    - [FTP Utilities](#ftp-utilities)
    - [Image Utilities](#image-utilities)
    - [PDF Utilities](#pdf-utilities)
    - [Printer Utilities](#printer-utilities)
  - [Usage Examples](#usage-examples)
    - [Converting Text to PNG Image](#converting-text-to-png-image)
    - [Converting XML to Dictionary](#converting-xml-to-dictionary)
    - [JSON Parsing and Manipulation](#json-parsing-and-manipulation)
  - [Contributing](#contributing)
  - [License](#license)

## Installation

To use **Tiny Utils**, clone the repository and install the necessary dependencies as specified in the `requirements.txt` file.

```bash
git clone https://github.com/hypo69/tiny-utils.git
cd tiny_utils
pip install -r requirements.txt
```

## Modules Overview

The library contains several submodules, each handling a specific task:

- **Converters**: Modules for converting data formats such as text to image, WebP to PNG, JSON, XML, Base64 encoding, and more.
- **String Utilities**: Tools for advanced string manipulation.
- **File Handling Utilities**: Functions for processing and manipulating files.
- **Date and Time Utilities**: Tools for formatting dates and times.
- **FTP Utilities**: Functions for working with FTP servers.
- **Image Utilities**: Basic image processing functions.
- **PDF Utilities**: Utilities for processing and converting PDF files.
- **Printer Utilities**: Functions for sending data to the printer.

## Module Descriptions

### Converters

The `convertors` module contains utilities for converting data between formats. These modules can handle various data types, from CSV to JSON and text to images.

#### Files:

- `text2png.py`: Converts text data into a PNG image.
- `tts.py`: Converts text to speech and saves it as an audio file.
- `webp2png.py`: Converts images from WebP format to PNG.
- `xls.py`: Handles conversions and manipulations of XLS files.
- `xml2dict.py`: Converts XML data into a Python dictionary.
- `base64.py`: Encodes or decodes data using Base64 encoding.
- `csv.py`: Provides tools for parsing and manipulating CSV data.
- `dict.py`: Utilities for handling Python dictionaries.
- `html.py`: Converts HTML content into various formats.
- `json.py`: Utilities for parsing and manipulating JSON data.
- `md2dict.py`: Converts Markdown content into a dictionary.
- `ns.py`: Specialized utilities for namespace conversion.


### String Utilities
... (and so on for other sections)
# ## \file /src/utils/convertors/__init__.py
# # -*- coding: utf-8 -*-
# # #! .pyenv/bin/python3

# """# .. Module :: src.utils.convertors
# : Platform: Windows, Unix
# : synopsis:


    
# Module for converting various data formats
# None

# The module contains functions for converting between different data formats, such as
# CSV, JSON, XML, HTML, MD, BASE64, as well as for working with images and text. He provides
# utilities for converting data into dictionaries, lists, formats for working with tables, etc.

# Example of use
# None

# An example of using the functions of the module `src.utils.convertors`:

# .. Code-Block :: Python

# from SRC.UTILS.CONVERTORS IMPORT CSV2DICT, JSON2XLS

# # CSV transformation into a dictionary
# csv_data = csv2dict ('Data.csv')

# # JSON conversion to XLSX
# json_data = json2xls ('Data.json')

# The functions of the module cover a wide range of conversions, including work with images (for example,
# Generate the PNG image from the text), work with audio (speech in text and vice versa), as well as converting
# between various encodes and formats, such as Base64.

# Available functions
# None
# - Work with CSV: converting from CSV to the dictionary or into the namespace.
# - Work with JSON: converting from JSON to other formats (CSV, XLSX, XML).
# - Work with HTML: Convert HTML to text, creating a dictionary from HTML.
# - Work with Base64: Coding and Decoding of Data in the Base64 format.
# - Work with images: images generation, PNG conversion in Webp.
# - Work with text: transforming the text into speech and vice versa.

# Included formats
# None
# - CSV
# - Json
# - XML
# - HTML
# - Markdown
# - Base64
# - PNG
# - Webp


# None
# # import json
# import os
# import sys
# import warnings
# from pathlib import Path

# from .base64 import (
# base64_to_tmpfile,
# base64encode,
# None

# from .csv import (
# csv2dict,
# csv2ns,
# None

# from .dict import ( dict2ns,
# dict2csv,
# dict2html,
# dict2xls,
# dict2xml,
# replace_key_in_dict
# None

# from .dot import dot2png

# from .html import (
# html2escape,
# html2ns,
# html2dict,
# escape2html,
# None

# from .html2text import (
# html2text,
# html2text_file,
# google_fixed_width_font,
# google_has_height,
# google_list_style,
# google_nest_count,
# google_text_emphasis,
# dumb_css_parser,
# dumb_property_dict,
# None

# from .json import (
# json2csv,
# json2ns,
# json2xls,
# json2xml
# None

# from .md2dict import (
# md2dict,
# None

# from .ns import (
# ns2csv,
# ns2dict,
# ns2xls,
# ns2xml
# None

# from .png import (TextToImageGenerator,
# webp2png,
# None

# from .tts import (
# speech_recognizer,
# text2speech,
# None

# from .unicode import decode_unicode_escape

# from .xml2dict import xml2dict
# from .xls import xls2dict

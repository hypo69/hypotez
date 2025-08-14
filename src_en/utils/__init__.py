# # -*- coding: utf-8 -*-
# # #! .pyenv/bin/python3

# """# Module for working with utilities
# None

# Module contains a set of small, useful utilities designed to simplify
# daily programming tasks. The module includes data conversion tools,
# Work with files and output format. This allows you to accelerate the development, providing
# Simple and re -used functions.

# Example of use
# None

# An example of using the functions of the module `src.utils`:

# .. Code-Block :: Python

# from SRC.utils Import CSV2DICT, JSON2XLS, Save_text_File

# # CSV conversion in the dictionary
# csv_data = csv2dict ('Data.csv')

# # JSON conversion in XLSX
# json_data = json2xls ('Data.json')

# # Save the text to the file
# save_text_file ('output.txt', 'HELLO, World!')
# None

# # """# Collection of small utilities designed to simplify often performed programming tasks.
# Includes tools for data conversion, work with files and formatted output.
# None

# # Imports are dumped in alphabetical order
# from .convertors import (
# TextToImageGenerator,
# base64_to_tmpfile,
# base64encode,
# csv2dict,
# csv2ns,
# decode_unicode_escape,
# dict2csv,
# dict2html,
# dict2ns,
# dict2xls,
# dict2xml,
# dot2png,
# escape2html,
# html2dict,
# html2escape,
# html2ns,
# html2text,
# html2text_file,
# json2csv,
# json2ns,
# json2xls,
# json2xml,
# md2dict,
# ns2csv,
# ns2dict,
# ns2xls,
# ns2xml,
# replace_key_in_dict,
# speech_recognizer,
# text2speech,
# webp2png,
# xls2dict
# None

# from .csv import (
# read_csv_as_dict,
# read_csv_as_ns,
# read_csv_file,
# save_csv_file
# None

# from .date_time import (
# TimeoutCheck
# None

# from .file import (
# get_directory_names,
# get_filenames,
# read_text_file,
# recursively_get_file_path,
# recursively_read_text_files,
# recursively_yield_file_path,
# remove_bom,
# save_text_file
# None

# from .image import (
# save_image,
# save_image_from_url,
# random_image,
# None

# from .jjson import (
# j_dumps,
# j_loads,
# j_loads_ns
# None

# from .pdf import (
# PDFUtils
# None

# from .printer import (
# print
# None

# from .string import (
# ProductFieldsValidator,
# String format,
# normalize_string,
# normalize_int,
# normalize_float,
# normalize_boolean
# None

# from .url import (
# extract_url_params,
# is_url
# None

# from .video import (
# save_video_from_url
# None

# from .path import get_relative_path

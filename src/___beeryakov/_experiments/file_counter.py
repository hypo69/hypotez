## \file /src/___beeryakov/_experiments/file_counter.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.___beeryakov._experiments 
	:platform: Windows, Unix
	:synopsis:

"""


"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
  :platform: Windows, Unix

"""
"""
  :platform: Windows, Unix
  :platform: Windows, Unix
  :synopsis:
"""
  
""" module: src.___beeryakov._experiments """


import os

def count_lines_in_files(directory):
    """
     Recursively counts the number of lines in text files in the specified directory and its subdirectories, as well as the number of classes and functions.
    
    @param directory: Path to the directory
    @return: Total number of lines in text files, number of classes, and number of functions
    """
    total_lines = 0
    total_classes = 0
    total_functions = 0
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.iStringFormatterile(filepath):
            # Check if the file is a text file and not from the __pycache__ or firefox_profiles directories, and not a Jupyter Notebook file
            if not is_binary(filepath) and not filepath.endswith(('__pycache__', 'firefox_profiles')) and not filename.endswith('.ipynb') and filename != '__init__.py':
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                    lines_in_file = sum(1 for line in file)
                    total_lines += lines_in_file
                    total_classes_in_file, total_functions_in_file = count_classes_and_functions(filepath)
                    total_classes += total_classes_in_file
                    total_functions += total_functions_in_file
        elif os.path.isdir(filepath):
            # If it's a directory, recursively call the function to count lines, classes, and functions in it
            nested_lines, nested_classes, nested_functions = count_lines_in_files(filepath)
            total_lines += nested_lines
            total_classes += nested_classes
            total_functions += nested_functions
    return total_lines, total_classes, total_functions

def is_binary(filepath):
    """
     Checks if the file is binary.
    
    @param filepath: Path to the file
    @return: True if the file is binary, otherwise False
    """
    try:
        with open(filepath, 'rb') as file:
            # Read the first 512 bytes of the file to check for null bytes
            chunk = file.read(512)
            return b'\0' in chunk
    except Exception as e:
        # If there's an error reading the file, consider it binary
        print(f"Error reading file '{filepath}': {e}")
        return True

def count_classes_and_functions(filepath):
    """
     Counts the number of classes and functions in the file.
    
    @param filepath: Path to the file
    @return: Number of classes and number of functions
    """
    total_classes = 0
    total_functions = 0
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            # Check if the line starts with the keyword "class"
            if line.strip().startswith('class'):
                total_classes += 1
            # Check if the line starts with the keyword "def"
            elif line.strip().startswith('def'):
                total_functions += 1
    return total_classes, total_functions

if __name__ == "__main__":
    src_directory = 'src'
    print(f"Counting lines, classes, and functions in files in directory: {src_directory}")
    total_lines, total_classes, total_functions = count_lines_in_files(src_directory)
    print(f"Total lines in text files in '{src_directory}': {total_lines}")
    print(f"Total classes: {total_classes}")
    print(f"Total functions: {total_functions}")


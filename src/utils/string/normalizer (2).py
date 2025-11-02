## \file /src/utils/string/normalizer (2).py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.utils.string 
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
  
""" module: src.utils.string """


""" Модуль нормализации строк  
@file src/utils/string/normalizer.py"""


import re
from src.logger.logger import logger
from .formatter import StringFormatter

class StringNormalizer:
    """ Class for normalizing strings."""

import re
from src.logger.logger import logger

class StringNormalizer:
    @staticmethod
    def simplify_string(input_str: str) -> str:
        """ Simplifies the input string by keeping only letters, digits, and replacing spaces with underscores.

        @param input_str: The string to be simplified.
        @return: The simplified string.
        @code
            example_str = "It's a test string with 'single quotes', numbers 123 and symbols!"
            simplified_str = StringNormalizer.simplify_string(example_str)
            print(simplified_str)  # Output: Its_a_test_string_with_single_quotes_numbers_123_and_symbols
        @endcode
        """
        try:
            # Remove all characters except letters, digits, and spaces
            cleaned_str = re.sub(r'[^a-zA-Z0-9\s]', '', input_str)
            # Replace spaces with underscores
            cleaned_str = cleaned_str.replace(' ', '_')
            # Remove consecutive underscores
            cleaned_str = re.sub(r'_+', '_', cleaned_str)
            return cleaned_str
        except Exception as ex:
            logger.error("Error simplifying the string", ex)
            return input_str


# Example usage
if __name__ == "__main__":
    example_str = "It's a test string with 'single quotes', numbers 123 and symbols!"
    simplified_str = StringNormalizer.simplify_string(example_str)
    print(simplified_str)  # Output: Its_a_test_string_with_single_quotes_numbers_123_and_symbols

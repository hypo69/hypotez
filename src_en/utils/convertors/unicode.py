import re
from typing import Dict, Any

def decode_unicode_escape(input_data: Dict[str, Any] | list | str) -> Dict[str, Any] | list | str:
    """The function decodes values in the dictionary, list or line containing unicated Escape-sequence, in the readable text.

    Args:
        Input_data (dict | List | str): input data - a dictionary, a list or line that may contain unicated Escape -consuming.

    Returns:
        dict | List | STR: Converted data. In the case of a line, decoding of Escape readings is used. In the case of a dictionary or list, all values are recursively processed.

    Example of use:
    .. Code-Block :: Python
        Input_dict = {
            'Product_NAME': R '\ U05DE \ U05E7 \ "\ U05D8 \ U05D9 \ U05E6 \ U05E8 \ U05DF \ NH510M K V2',
            'Category': r '\ u05e2 \ u05e8 \ u05db \ u05ea \ u05e9 \ u05d1 \ u05d1 \ u05d9 \ u05dd',
            'Price': 123.45
        }

        Input_list = [r '\ u05e2 \ u05e8 \ u05db \ u05ea \ u05e9 \ u05d1 \ u05d1 \ u05d9 \ u05dd', r'h510m K v2 ']

        Input_string = r '\ u05de \ u05e7 \ "\ u05d8 \ u05d9 \ u05e6 \ u05e8 \ u05df \ nh510m k v2'

        # Use a function
        decoded_dict = decode_unicode_escape (Input_dict)
        decoded_list = decode_unicode_escape (input_list)
        decoded_string = decode_unicode_escape (Input_string)

        Print (decoded_dict)
        Print (decoded_list)
        Print (decoded_string)"""
    
    if isinstance(input_data, dict):
        # Recursive processing of the dictionary
        return {key: decode_unicode_escape(value) for key, value in input_data.items()}
    
    elif isinstance(input_data, list):
        # Recursive processing of list elements
        return [decode_unicode_escape(item) for item in input_data]
    
    elif isinstance(input_data, str):
        # The function decodes the line if it contains escape-performance
        try:
            # Step 1: Decoding a string with Escape-readings
            decoded_string = input_data.encode('utf-8').decode('unicode_escape')
        except UnicodeDecodeError:
            decoded_string = input_data
        
        # Step 2: Transformation of all found sequences \ uxxxx
        unicode_escape_pattern = r'\\u[0-9a-fA-F]{4}'
        decoded_string = re.sub(unicode_escape_pattern, lambda match: match.group(0).encode('utf-8').decode('unicode_escape'), decoded_string)
        
        return decoded_string
    
    else:
        # If the data type is not supported, the function will return the data unchanged
        return input_data

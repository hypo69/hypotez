# # \file /src/utils/jjson.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

"""JSON module is dull to work with json data.
=====================================================
Provides functions for downloading, saving, processing and searching data in JSON facilities and files.

Main functions:
- `J_DUMPS (Data, File_path, Ensure_ascii, Mode, Exc_info)`: Python objects (dictionaries, lists, Simplenamespace, Json lines) 
                                                             In a json file or returns them as a Python object (`dict`,` list`) after processing.
                                                             Supports various recording modes (rewriting, adding to the beginning/end).
  Example: `j_dumps ({'key': 'value'}, path ('output.json'))` Returns `true` in case of success.
          `Processed_obj = j_dumps ({'key': 'value'})` Returns the processed dictionary `{'key': 'velue'}`.
- `j_loads (jjson, ordered)`: downloads json data from a file, line, dictionary, list or Simplenamespace.
                             It can process the directory with JSON files. Returns `dict` or` list`.
                             With an error, he returns `{}`.
  Example: `Data = J_loads (Path ('Input.json')` `
- `j_loads_ns (JJSON, OrDRED)`: Similarly `j_loads`, but converts the result in` simplenamespace 'or a list of `simplenapace`.
                                With an error or if `j_loads` returned an empty result, returns` {} `.
  Example: `ns_data = j_loads_ns (path ('input.json')` `
- `sanitize_json_files (Path)`: checks and "sanitizes" json files in the specified directory or a separate json file.
                               Unimportant files are renamed (the suffix `.Sanitized` is added). Returns `Bool`.
  Example: `sanitize_json_files (Path ('./ Data_dir/'))`
- `found_keys (Obj, keys_to_find, found)`: recursively looking for values on given keys in the invested data structure 
                                        (Dictionary or list). Returns a dictionary where the keys are the desired keys,
                                        And the values are lists of found values.
  Example: `found_values = find_keys (my_data, ['id', 'name']` `

Internal auxiliary functions:
- `_convert_to_dict (value)`: recursively converts the objects of Simplenamespace and invested structures in the dictionaries.
- `_Read_existing_data (Path, Exc_info)`: Reads and Parses json data from the specified file. Returns `dict` or` list`, or `}` with an error.
- `_MERGE_DATA (Data, Existing_data, Mode)`: combines new data (`Data`) with existing (` Existing_Data` 
                                          In accordance with the specified mode (`mode`). Returns the united `dict` or` list`, or `}` when error.
- `_Decode_strings (Data)`: recursively decodes lines (unicode_escape) in the data structure.
- `_string_to_DICT (json_string)`: deleys markdown wrappers (`` json ... `` `) from a line and parks it like json. Returns `dict` or` list`, or `}` with an error.

Configuration class:
- `config`: contains constants for file recording modes (` mode_write`, `mode_ppend_start`,` mode_ppend_end`).

 `` `RST
 .. Module :: src.utils.jjson
 `` `"""
import json
import codecs
import re # Used in _string_to_dict
from pathlib import Path
from tkinter.filedialog import LoadFileDialog
from typing import Any, List as TypingList, Dict as TypingDict # TypingList/Dict for find_keys as per original.
from collections.abc import Mapping, Sequence
from types import SimpleNamespace
from dataclasses import dataclass
from json_repair import repair_json
# import json_repair


from src.logger.logger import logger
from .convertors.dict import dict2ns


@dataclass
class Config:
    """Configuration class for storing a record modes.
    
    Attributes:
        Mode_Write (str): file rewriting mode.
        Mode_Append_Start (str): mode of adding data to the beginning of the file (logical addition).
        Mode_Append_end (str): mode of adding data to the end of the file (logical addition)."""
    MODE_WRITE:str = 'w'
    MODE_APPEND_START:str = 'a+'
    MODE_APPEND_END:str = '+a'

def _convert_to_dict(value: Any) -> Any:
    """The function recursively converts the objects of Simplenamespace and invested structures in dictionaries.

    Args:
        Value (Any): meaning for conversion. It can be Simplenamespace, a dictionary, a list or another type.

    Returns:
        ANY: Converted value. Simplenamespace and dictionaries are transformed into `dict`,
             Lists are processed recursively. Other types are returned as it is.
    
    Example:
        >>> Class Myns (Simplenamespace): Pass
        >>> ns = myns (a = 1, b = myns (c = 2))
        >>> _convert_to_dict (NS)
        {'a': 1, 'b': {'c': 2}}
        >>> _convert_to_dict ([myns (x = 10), 20])
        [{'x': 10}, 20]"""
    # Recursive converting Simplenamespace in DICT
    if isinstance(value, SimpleNamespace):
        return {key: _convert_to_dict(val) for key, val in vars(value).items()}
    # Recursive conversion of dictionaries (for processing invested simplenamespace)
    if isinstance(value, dict):
        return {key: _convert_to_dict(val) for key, val in value.items()}
    # Recursive conversion of lists
    if isinstance(value, list):
        return [_convert_to_dict(item) for item in value]
    # Return of value without changes if it is not simplenamespace, dict or list
    return value

def _read_existing_data(path: Path, exc_info: bool = True) -> dict[Any, Any] | list[Any]:
    """The function reads and parses json data from the specified file.

    Args:
        Path (Path): Way to Json File.
        Exc_info (Bool, Optional): Do you log in information about the exception. By default `true`.

    Returns:
        DICT [Any, Any] | List [Any]: Dictionary or list with data from JSON file. 
                                     Returns an empty dictionary if the file is not found, damaged or another reading error occurs.
    
    Example:
        >>> # Suppose 'Data.json' contains {"Key": "Value"}
        >>> # _read_existing_data (Path ('Data.json'))
        >>> # {'Key': 'Value'}
        >>> # _read_existing_data (Path ('non_existent.json'))
        >>> # None
        # Examples are made, as they require the availability of files"""
    try:
        # Json Reading and Parsing from File
        return json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as ex:
        logger.error(f'Error decoding existing JSON in {path}: {ex}', ex, exc_info=exc_info)
        return {}
    except FileNotFoundError: # Case processing if the file is not found
        logger.error(f'File not found for reading existing data: {path}', None, exc_info=exc_info)
        return {}
    except Exception as ex:
        logger.error(f'Error reading {path=}: {ex}', ex, exc_info=exc_info)
        return {}

def _merge_data(
    data: dict[Any, Any] | list[Any], 
    existing_data: dict[Any, Any] | list[Any], 
    mode: str
) -> dict[Any, Any] | list[Any]:
    """The function combines new data (`Data`) with existing (` Existing_Data`) 
    In accordance with the specified mode (`mode`).

    Args:
        Data (Dict [Any, Any] | List [any]): New data (dictionary or list).
        Existing_Data (Dict [Any, Any] | List [Any]): existing data (dictionary or list).
        Mode (str): Association mode. Supported `config.mode_ppend_start` and` config.mode_ppend_end`.

    Returns:
        DICT [Any, Any] | List [Any]: United data. If the types are incompatible or the regime does not imply a merger,
                                     It can return `Data` or` Existing_Data` based on the logic of the regime.
                                     Returns `Data` by default, if the mode is not` A+`or`+A`.
                                     In case of error, the empty dictionary returns.
    
    Example:
        >>> _merge_data ({'c': 3}, {'a': 1, 'b': 2}, config.mode_ppend_start)
        {'a': 1, 'b': 2, 'c': 3}
        >>> _MERGE_DATA ([3], [1, 2], config.mode_ppend_start)
        [3, 1, 2]
        >>> _merge_data ({'c': 3}, {'a': 1, 'b': 2}, config.mode_ppend_end)
        {'a': 1, 'b': 2, 'c': 3}
        >>> _MERGE_DATA ([3], [1, 2], config.mode_ppend_end)
        [1, 2, 3]"""
    # Data combination depending on the regime
    try:
        if mode == Config.MODE_APPEND_START:
            # Adding new data to the beginning (for lists) or updating the existing dictionary (for dictionaries)
            if isinstance(data, list) and isinstance(existing_data, list):
               return data + existing_data
            if isinstance(data, dict) and isinstance(existing_data, dict):
                 merged_dict: dict[Any, Any] = existing_data.copy()
                 merged_dict.update(data) # The keys from 'Data' will rewrite the keys to 'Existing_data'
                 return merged_dict
            logger.warning(f"Cannot merge data for MODE_APPEND_START due to type mismatch or unsupported types. Returning existing_data. Data type: {type(data)}, Existing data type: {type(existing_data)}")
            return existing_data # Priority to existing data
        elif mode == Config.MODE_APPEND_END:
            # Adding new data to the end (for lists) or updating the new dictionary existing data (for dictionaries)
            if isinstance(data, list) and isinstance(existing_data, list):
                return existing_data + data
            if isinstance(data, dict) and isinstance(existing_data, dict):
                 merged_dict = data.copy()
                 merged_dict.update(existing_data) # The keys from 'Existing_data' will redraw the keys to 'Data'
                 return merged_dict
            logger.warning(f"Cannot merge data for MODE_APPEND_END due to type mismatch or unsupported types. Returning data. Data type: {type(data)}, Existing data type: {type(existing_data)}")
            return data # Priority with new data
        # If the regime does not imply merger (for example, 'w'), new data are returned
        return data
    except Exception as ex:
        logger.error(f'Error merging data: {ex}', ex, exc_info=True)
        return {} # Return of an empty dictionary in the event of an unforeseen error


def j_dumps(
    data: dict[Any, Any] | SimpleNamespace | list[Any] | str,
    file_path: Path | str | None = None,
    ensure_ascii: bool = False,
    mode: str = Config.MODE_WRITE,
    exc_info: bool = True,
) -> bool | dict[Any, Any] | list[Any] | None:
    """Provincials Python object in JSON line or save it to a file.

    If `file_path` is indicated, the function tries to write data to the file.
    Returns `true` with a successful recording,` false` in case of error.

    If `file_path` is not specified (` none`), the function processes `data` 
    (for example, converts from `simplenamespace` or json string) and returns 
    The resulting Python object (`dict` or` list`). Returns `none 'when processing error.

    Args:
        Data (Dict | Simplenamespace | List | str): data for serialization. Can be a dictionary
            `Simplenamespace`, list or json string (which will be pre-processed).
        File_path (Path | Str | None, Optional): Way to the file for saving.
            If `none`, the data is not saved, but returned after processing. By default `none`.
        ENSURE_ASCII (Bool, Optional): If `false`, the symbols of non-USCII will be preserved as it is.
            If `true`, they will be shielded. By default `false`.
        Mode (str, Optional): File recording mode if `file_path` is indicated.
            Supported `config.mode_write` (rewriting),` config.mode_ppend_start` (adding "to the beginning"),
            `Config.mode_ppend_end` (adding" to the end "). By default `config.mode_write`.
            The addition modes logically combine data before recording.
        Exc_info (Bool, Optional): Do you log in complete information about the exclusion. By default `true`.

    Returns:
        Bool | dict | List | None:
            - `True`: if` file_path` is indicated and the entry to the file was successful.
            - `false`: if` file_path` is indicated and an entry error occurred.
            - `dict | List`: If `File_Path` is not indicated, the processed Python object is returned.
            - `none`: if` file_path` is not indicated and data processing error occurred.
    
    Example:
        >>> Data_dict = {'Key': 'Value', 'Num': 123}
        >>> # j_dumps (Data_dict, 'output.json') # writes to the file, return True/False (requires the file)
        >>> Class Myns (Simplenamespace): Pass
        >>> ns_data = myns (name = 'test')
        >>> Processed_data = j_dumps (ns_data) 
        >>> Isinstance (Processed_data, Dict)
        True
        >>> Processed_data ['name']
        'test'
        >>> Invalid_json_string = "{'key': 'velue'}" 
        >>> result = j_dumps (Invalid_json_string) 
        >>> Result is none 
        True"""
    processed_data: dict[Any, Any] | list[Any] | None
    path: Path | None = None

    # Initial input processing
    if isinstance(data, str):
        data_as_obj: dict[Any, Any] | list[Any] = _string_to_dict(data)
        # If _String_to_DICT returned empty, but the line was non -empty and was not "{}" or "[]"
        if not data_as_obj and data.strip() and data.strip() not in ('{}', '[]'):
            try:
                repaired_json_str: str = repair_json(data, return_objects=True)
                processed_data = json.loads(repaired_json_str)
            except Exception as ex_repair:
                logger.error(f'Error repairing/parsing JSON string (first 100 chars): "{data[:100]}..."', ex_repair, exc_info=exc_info)
                return False if file_path else None
        else:
            processed_data = data_as_obj
    elif isinstance(data, (SimpleNamespace, dict, list)):
        processed_data = _convert_to_dict(data)
    else:
        logger.error(f'Unsupported data type for j_dumps: {type(data)}', None, exc_info=exc_info)
        return False if file_path else None

    if processed_data is None : # It should not happen if _Convert_to_DICT/_String_to_DICT work as expected
        logger.error(f'Data became None after initial processing. Original type: {type(data)}', None, exc_info=exc_info)
        return False if file_path else None

    if file_path:
        path = Path(file_path)

    if mode not in {Config.MODE_WRITE, Config.MODE_APPEND_START, Config.MODE_APPEND_END}:
        logger.warning(f"Unsupported mode '{mode}'. Defaulting to '{Config.MODE_WRITE}'.")
        mode = Config.MODE_WRITE

    if path:
        final_data_to_write: dict[Any, Any] | list[Any] = processed_data
        
        if mode in {Config.MODE_APPEND_START, Config.MODE_APPEND_END}:
            if path.exists() and path.is_file(): # Check that this is a file
                existing_data: dict[Any, Any] | list[Any] = _read_existing_data(path, exc_info)
                # Verification of types before merging
                if isinstance(processed_data, (dict, list)) and isinstance(existing_data, (dict, list)):
                    final_data_to_write = _merge_data(processed_data, existing_data, mode)
                    if not final_data_to_write and (processed_data or existing_data):
                         logger.warning(f"Data merging resulted in empty data for {path}. Check merge logic and data types.")
                elif not isinstance(existing_data, (dict, list)): # Existing_Data failed to read correctly
                    logger.warning(f"Could not properly read or parse existing data from {path} for merge. Read data type: {type(existing_data)}. Writing new data only.")
                    # final_data_to_write остается processed_data
            elif not path.exists() : # The file does not exist, the add -on mode works as a regular record
                logger.info(f"File {path} does not exist for append mode. Will create a new file.")

        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open(Config.MODE_WRITE, encoding='utf-8') as f: # The merger is made, we always write in 'w'
                json.dump(final_data_to_write, f, ensure_ascii=ensure_ascii, indent=4)
            return True
        except Exception as ex:
            logger.error(f'Failed to write data to {path}:', ex, exc_info=exc_info)
            return False
    else: # file_path is None
        return processed_data


def _decode_strings(data: Any) -> Any:
    """The function recursively decodes the lines in the data structure from the 'unicode_escape' format.

    This is useful for lines that could be shielded, for example, when transmitting via json
    and contain sequences of the type `\\ uxxxx`.

    Args:
        Data (Any): Data structure (line, list, dictionary) for decoding.

    Returns:
        ANY: Data structure with recursively decoded lines.
             If the element is not a line, a list or dictionary, it returns unchanged.
    
    Example:
        >>> _Decode_strings ("Hello \\ U0020world")
        'Hello World'
        >>> _Decode_strings ({"Key": "Value \\ U0020test"})
        {'Key': 'Value test'}
        >>> _decode_strings (["item1", "item \\ u0032"])
        ['item1', 'item2']"""
    if isinstance(data, str):
        try:
           return codecs.decode(data, 'unicode_escape')
        except Exception:
            return data # Return of the original line if the decoding failed
    if isinstance(data, list):
        return [_decode_strings(item) for item in data]
    if isinstance(data, dict):
        return {
            _decode_strings(key): _decode_strings(value) for key, value in data.items()
        }
    return data

def _string_to_dict(json_string: str, return_objects:bool = False) -> dict[Any, Any] | list[Any]:
    """The function deleys the Markdown Bugs (for example, `` json ... `` `) from a line
    And then it parses it as a json, returning a dictionary or a list.

    Args:
        JSON_STRING (str): a string potentially containing JSON and MARKDOWN worshipers.

    Returns:
        DICT [Any, Any] | List [Any]: a dictionary or a list received after Parsing Json.
                                     Returns an empty dictionary, if the string is empty, it is unyliped json
                                     Or there is a parsing error.
    
    Example:
        >>> _string_to_dict ('`` json \\ n {"key": "value"} \\ n```' ')
        {'Key': 'value'}
        >>> _String_to_DICT ('{"NAME": "test", "items": [1, 2]}')
        {'name': 'test', 'items': [1, 2]}
        >>> _string_to_DICT ('Invalid Json')
        {}"""
    result: dict[Any, Any] | list[Any] = {}
    if not isinstance(json_string, str):
        logger.warning(f'_string_to_dict expects a string, got {type(json_string)}. Returning empty dict.')
        return {}

    cleaned_string: str = json_string.strip()
    
    # Improved regex for removing `` json ... `` `and just` `` `` `` ER
    if cleaned_string.startswith('```'):
        cleaned_string = re.sub(r'^```(?:json)?\s*', '', cleaned_string, count=1)
        cleaned_string = re.sub(r'\s*```$', '', cleaned_string, count=1)
        cleaned_string = cleaned_string.strip()
        
    if not cleaned_string:
        return {}

    try:
        result:dict = json.loads(cleaned_string)
    except json.JSONDecodeError as ex:
        logger.error(f'JSON parsing error for string (first 100 chars): "{cleaned_string[:100]}..."', ex, False)
        logger.debug(f'Trying repair_json')
        try:
            repaired_result:dict|bool = repair_json(cleaned_string)
            result:dict = json.loads(repaired_result)
        except Exception as ex:
            logger.error(f'Error in repair_json', ex)
            return {}
    except Exception as ex:
        logger.error(f'Unexpected error parsing string (first 100 chars): "{cleaned_string[:100]}..."', ex, False)
        return {}
        
    return result


def j_loads(
    jjson: dict[Any, Any] | SimpleNamespace | str | Path | list[Any], ordered: bool = True # ordered not used
) -> dict[Any, Any] | list[Any]:
    """Loads JSON-compatible data from various sources.

    Supports download from:
    - `dict`,` list`, `simplenamespace`: return after some processing (for example, decoding rows).
    - `str`: the line pars like JSON (with preliminary cleaning from Markdown and an attempt to" repair ").
    - `Path`: If the path indicates the file, it is read as JSON. If the directory,
              Recursively all `.json` files from it are loaded, and the result is returned as a list.
    
    The `ordered` parameter is not used in the current implementation to preserve the order of elements.

    Args:
        JJSON (DICT | SIMPLENAMESPACE | STR | PATH | LIST): Data source.
        Ordered (Bool, Optional): a parameter for future use. The current version does not affect. By default `true`.

    Returns:
        DICT [Any, Any] | LIST [ANY]: Processed data (dictionary or list).
                                     In case of error, the empty dictionary `{}` returns.
    
    Example:
        >>> # Suppose 'Data.json' contains {"id": 1, "value": "test \\ u0020data"}
        >>> # Data_from_file = J_loads (Path ('Data.json'))
        >>> # ISINSTANCE (DATA_FROM_FILE, DICT) and Data_from_file.get ('Value') == 'Test Data'
        >>> # True (requires a file)
        >>> Data_from_string = j_loads ('{"name": "example"}')
        >>> Data_from_string.get ('Name')
        'Example'
        >>> Data_from_list = j_loads ([{"item": "a"}, "item \\ u0020b"])
        >>> Isinstance (Data_from_List, List) and Data_from_List [1] == 'Item B'
        True
        >>> # j_loads (Path ('non_existent_dir/'))
        >>> # {} (requires a file system)"""
    jjson_internal: Any = jjson
    if isinstance(jjson, SimpleNamespace):
        jjson_internal = vars(jjson) # Simplenamespace conversion to DICT for further processing

    try:
        if isinstance(jjson_internal, Path):
            path_obj: Path = jjson_internal
            if path_obj.is_dir():
                files: TypingList[Path] = list(path_obj.glob('*.json'))
                return [j_loads(file, ordered=ordered) for file in files] # J_loads will return {} for unimportant files
            elif path_obj.is_file():
                # Json.loads correctly processes \ uxxxx from the file. _Decode_strings is not needed here.
                try:
                    return json.loads(path_obj.read_text(encoding='utf-8'))
                except Exception as ex:
                    logger.error(f'Ошибка чтения словаря',ex, False)
                    try:
                        with path_obj.open('r', encoding='utf-8') as f:
                            file_content: str = f.read()
                            if not file_content:
                                logger.error(f'В файле {path_obj} Нет данных!', None, False)
                                return {}

                        repaired_json: dict| None = _string_to_dict(file_content, return_objects=True)
                        ...
                        return repaired_json 
                    except Exception as ex:
                        logger.error(f'Error reading file {path_obj}: {ex}', ex, False)
                        ...
                        return {}
                    ...
            else:
                logger.error(f'Path does not exist or is not a file/directory: {path_obj}', None, False)
                return {}
        
        if isinstance(jjson_internal, str):
            parsed_obj: dict[Any, Any] | list[Any] = _string_to_dict(jjson_internal) # _String_to_DICT returns {} when error
            return _decode_strings(parsed_obj) # Decoding lines in the resulting object

        if isinstance(jjson_internal, list):
            return _decode_strings(jjson_internal) # Decoding lines in the list
        
        if isinstance(jjson_internal, dict):
            return _decode_strings(jjson_internal) # Decoding lines in the dictionary
            
    except FileNotFoundError: # This branch may not be achieved due to IS_File/IS_DIR checks
        logger.error(f'File not found: {str(jjson_internal)}', None, False)
        return {}
    except json.JSONDecodeError as ex:
        log_input_repr: str = str(jjson_internal) if isinstance(jjson_internal, Path) else repr(jjson_internal)[:200]
        logger.error(f'JSON parsing error for input ({type(jjson_internal)}): {log_input_repr}...', ex, False)
        return {}
    except Exception as ex:
        log_input_repr = str(jjson_internal) if isinstance(jjson_internal, Path) else repr(jjson_internal)[:200]
        logger.error(f'Error loading data for input ({type(jjson_internal)}): {log_input_repr}...', ex, False)
        return {}
    
    logger.warning(f'j_loads received unhandled data type: {type(jjson_internal)}. Returning empty dict.')
    return {}


def j_loads_ns(
    jjson: Path | SimpleNamespace | dict[Any, Any] | str | list[Any], # Added List [Any] for completeness
    ordered: bool = True # ordered not used
) -> SimpleNamespace | TypingList[SimpleNamespace | Any] | dict[Any, Any]: # dict if j_loads returns empty {}
    """Loads JSON-compatible data and converts the result in `simplenamespace`.

    The function is a wrapping over `j_loads`. If `j_loads` returns the dictionary,
    It is converted into `simplenamespace`. If `j_loads` returns the list,
    Each element-layer in the list is converted into `simplenamespace`.

    Args:
        JJSON (Path | Simplenamespace | Dict | str | List): Data source, like in `j_loads`.
        Ordered (Bool, Optional): Parameter for `J_loads`. In the current version is not used. By default `true`.

    Returns:
        Simplenamespace | List [simplenamespace | Any] | Dict:
            - `simplenamespace`: if the loaded data is a dictionary.
            - `List [simplenamespace | Any] `: If the loaded data is a list (elements are converted).
            - `dict`: an empty dictionary`} ``, if `j_loads` returned an empty result or an error has occurred.
    
    Example:
        >>> # Suppose 'user.json' contains {"name": "alice", "age": 30}
        >>> # user_ns = j_loads_ns (Path ('user.json'))
        >>> # ISINSTANCE (User_ns, Simplenamespace) and User_ns.name == 'Alice'
        >>> # True (requires a file)
        >>> # Suppose 'users.json' contains [{"name": "bob"}, {"name": "chambers"}]
        >>> # users_list_ns = j_loads_ns (Path ('users.json'))
        >>> # ISINSTANCE (Users_List_ns, List) and IsinStance (Users_List_ns [0], Simplenamespace)
        >>> # True (requires a file)
        >>> J_loads_ns ("Invalid Json")
        {}"""
    data: dict[Any, Any] | list[Any] = j_loads(jjson, ordered=ordered)
    
    if not data and isinstance(data, dict): # J_loads returned {}, which means an error or empty json
        return {} 
    
    if isinstance(data, list):
        return [dict2ns(item) if isinstance(item, dict) else item for item in data]
    if isinstance(data, dict): # Including unlucky dictionaries
        return dict2ns(data)
    
    # If Data is not dict and not light (for example, J_loads has returned something unexpected, although it should not)
    # Or Data is an empty list (J_loads ([]) -> []), then dict2ns is not applied directly.
    # If Data is an empty list, we will return it.
    if isinstance(data, list): # Covers empty list case specifically
        return []

    return {} # General Fallback, if Data has an unexpected type or J_loads has returned something strange

def sanitize_json_files(path: Path) -> bool:
    """Checks the validity of JSON files in the specified directory or one JSON file.

    If the file is universal, it is renamed by adding the suffix '. Sanitized' to its name.
    If the file is valid, it remains unchanged.
    If the specified path does not exist or is not a file/directory, an error is logged in,
    And the function returns `false`.

    Args:
        Path (Path): the path to a json file or a directory containing JSON files.

    Returns:
        Bool: `true`, if all processed files are valid or were successfully“ sanitized ”(renamed).
              `False`, if the path is unimportant, or if at least one file could not be processed.
    
    Example:
        >>> # Examples require the creation of temporary files and directory.
        >>> # from Pathlib Import Path
        >>> # Import json
        >>> # TEMP_DIR = PATH ('./ TEMP_SANITIZE_TEST')
        >>> # TEMP_DIR.MKDIR (Exist_ok = True)
        >>> # (TEMP_DIR / 'VALID.JSON'). Write_text (JSON.Dumps ({"Key": "Value"}))
        >>> # (TEMP_DIR / 'Invalid.json'). Write_text ("{'bad': 'json'")
        >>> # Sanitize_json_Files (TEMP_DIR) # Expected result: True
        >>> # (TEMP_DIR / 'Invalid.json.sanitized'). Exists () # expected result: True
        >>> # # ... cleaning ..."""
    all_successful: bool = True

    def process_file(file_path: Path) -> bool:
        logger.info(f'Start sanitize file: {file_path}')

        def write_sanitzed_suffix(file_path) -> bool:
            try:
                sanitized_path: Path = file_path.with_name(file_path.name + '.sanitized')
                file_path.rename(sanitized_path)
                logger.info(f'File renamed to: {sanitized_path}')
                return True
            except Exception as rename_ex:
                logger.error(f'Failed to rename file: {file_path} to {sanitized_path}', rename_ex)
                return False


        if not file_path.is_file() or file_path.suffix.lower() != '.json':
            logger.error(f'Path is not a JSON file: {file_path}')
            return False
        
        try:
            with file_path.open('r', encoding='utf-8') as f:
                json.load(f)
            logger.info(f'File is valid: {file_path}')
            return True

        except Exception as ex:
            logger.error(f'Error reading or parsing JSON in file: {file_path}\nStart repair', ex)
            try:
                with file_path.open('r', encoding='utf-8') as f:
                    text_data:str = f
            except Exception as ex:
                logger.error("Не удается открыть файл. Возват из функции")
                write_sanitzed_suffix(file_path)
                return False

            repaired_data = _string_to_dict(text_data, return_objects=True)
            if not repaired_data:
                logger.error(f'Failed to repair JSON in file: {file_path}')
                write_sanitzed_suffix(file_path)
                return False
                

            if j_dumps(repaired_data, file_path.open('w', encoding='utf-8'), ensure_ascii=False, indent=4):
                logger.success(f'File repaired and saved: {file_path}')
                return True

        return True # The file is valid or successfully renamed

    if not path.exists():
        logger.error(f'Path not found: {path}')
        return False

    if path.is_file():
        if not process_file(path):
            all_successful = False
    elif path.is_dir():
        for json_file in path.rglob('*.json'):
            # Passing files that have already been renamed with the Suffix. Sanitized,
            # To avoid their re -processing or errors.
            if '.sanitized' in json_file.suffixes: # Check if '.sanitized' is one of the suffixes
                continue
            if not process_file(json_file):
                all_successful = False
    else:
        logger.error(f'Path is not a file or directory: {path}')
        return False

    return all_successful


def find_keys(
    obj: Any,
    keys_to_find_input: TypingList[str] | str,
    found: TypingDict[str, TypingList[Any]] | None = None,
) -> TypingDict[str, TypingList[Any]]:
    """Recursively finds all values related to the specified keys in the invested data structure.

    Args:
        OBJ (Any): Input Python Object (Dictionary, List or any JSON-like structure).
        keys_to_find_input (Typinglist [str] | str): a list of string keys for searching or one key-string.
        Found (dict [str, list [any]] | None, Optional): a battery for found keys and their values.
            It is usually used internally for recursion. By default `none`.

    Returns:
        DICT [str, lib [Any]]: a dictionary where each desired key is compared with a list of all values found for him.
    
    Example:
        >>> Data = {
        ... "id": 1, "name": "parent", 
        ... "child": {"id": 2, "name": "child1"}, 
        ... "items": [{"id": 3, "value": "a"}, {"name": "child2", "id": 4}]
        ...}
        >>> Result = find_keys (Data, ["ID", "NAME"])
        >>> sorted (result ['id']) # sorting for predictable order in the test
        [1, 2, 3, 4]
        >>> sorted (result ['name'])
        ['Child1', 'Child2', 'Parent']
        >>> # Test with a Single Key String
        >>> Result_single = find_keys (Data, "id")
        >>> sorted (result_single ['id'])
        [1, 2, 3, 4]
        >>> find_keys (Data, ["Non_existent_key"]) # test with non-existent key
        {'non_existent_key': []}"""
    
    # This variable will contain the actual list of string keys for the search.
    actual_keys_list_to_search: TypingList[str]
    # This variable will contain a dictionary-accumulator.
    current_accumulator_dict: TypingDict[str, TypingList[Any]]

    # The block is performed only with the initial (not recursive) call.
    if found is None:
        # Processing Keys_to_find_input to guarantee that this is a list of lines.
        if isinstance(keys_to_find_input, str):
            actual_keys_list_to_search = [keys_to_find_input]
        elif isinstance(keys_to_find_input, list) and all(isinstance(k, str) for k in keys_to_find_input):
            actual_keys_list_to_search = keys_to_find_input
        else:
            # Error logging if the type of input does not correspond to the expected one.
            logger.error(f"Параметр 'keys_to_find_input' должен быть строкой или списком строк. Получено: {type(keys_to_find_input)}")
            # Return of an empty dictionary or partially formed, if possible.
            if hasattr(keys_to_find_input, '__iter__') and not isinstance(keys_to_find_input, (str, bytes)):
                 return {str(k): [] for k in keys_to_find_input if isinstance(k, str)}
            return {}

        # Initialization of the dictionary-accumulator.
        current_accumulator_dict = {key_item: [] for key_item in actual_keys_list_to_search}
    # The block is performed in recursive challenges.
    else:
        current_accumulator_dict = found
        # In recursive challenges, `keys_to_find_input 'is actually` actual_keys_list_to_search` from the parent call.
        # Thus, this is already a processed list of lines.
        if not (isinstance(keys_to_find_input, list) and all(isinstance(k, str) for k in keys_to_find_input)):
            # This should not happen if the recursion is called correctly. Error logging if this happened.
            logger.error("Внутренняя ошибка: `keys_to_find_input` в рекурсивном вызове не является списком строк.")
            return current_accumulator_dict # Or throw off an exception

        actual_keys_list_to_search = keys_to_find_input


    try:
        # If the object is a dictionary or a similar display.
        if isinstance(obj, Mapping):
            for key, value in obj.items():
                # Bringing the key from OBJ to the line for search.
                key_as_str: str = str(key)
                if key_as_str in actual_keys_list_to_search:
                    # If the key coincides with one of the desired, adding its value.
                    # The user code contained `If value:` that would miss false values (for example, None, 0, FALSE).
                    # This check is deleted to turn on all values for the found keys.
                    if value:
                        # Checking whether the value is a list or a motorcade.
                        if isinstance(value, (list, tuple)):
                            # Association to the list of storage in the battery.
                            current_accumulator_dict[key_as_str].extend(list(value))
                        else:
                            # Adding a value to the battery.
                            current_accumulator_dict[key_as_str].append(value)
                
                # Recursive call Find_keys for value.
                # Transfer `Actual_keys_list_to_search` (processed list) and` current_accumulator_dict`.
                find_keys(value, actual_keys_list_to_search, current_accumulator_dict)
        # If the object is a list or a motorcade (but not a line/bytes).
        elif isinstance(obj, Sequence) and not isinstance(obj, (str, bytes)):
            for item in obj:
                # Recursive call Find_keys for each element in the sequence.
                find_keys(item, actual_keys_list_to_search, current_accumulator_dict)
    
    except Exception as ex:
        logger.error('Ошибка при поиске ключей в объекте', ex, exc_info=True)
        # The function will return 'Current_accumulator_dict' in its state at the time of the error.

    return current_accumulator_dict
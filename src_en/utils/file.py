# # \file /src/utils/file.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

""".. Module :: src.utils.file 
	: Platform: Windows, Unix
	: synopsis: read, wite, search text files

Module for working with files.
======================================================================================ward

The module contains a set of utilities to perform operations with files, such as saving, reading,
and getting lists. Supports the processing of large files using generators
to save memory.

An example of use
-------------------

`` `python

    From Pathlib Import Path
    from src.utils.file import read_text_file, save_text_file

    File_path = Path ('Example.txt')
    Content = Read_text_file (File_path)
    IF Content:
        Print (F'File Content: {Content [: 100]} ... ')

    Save_text_File (File_path, 'New Text')
`` `"""
import os
import asyncio
import json
import fnmatch
import re
from pathlib import Path
from typing import List, Dict, Optional, Union, Generator, Iterator
from src.logger.logger import logger


def save_text_file(
    data: str | list[str] | dict,
    file_path: str | Path,
    mode: str = 'w'
) -> bool:
    """Saves data to a text file.

    Args:
        File_path (str | path): the path to the file for saving.
        Data (str | list [str] | dict): data for recording. Can be a line, a list of lines or a dictionary.
        Mode (str, Optional): file recording mode ('w' for recording, 'a' to add).
    Returns:
        Bool: `true`, if the file is successfully saved,` false` otherwise.
    RAISES:
        Exception: If an error occurs when writing to a file.

    Example:
        >>> from Pathlib Import Path
        >>> file_path = Path ('Example.txt')
        >>> Data = 'Example of the text'
        >>> Result = Save_text_File (File_path, Data)
        >>> Print (Result)
        True"""
    try:
        file_path = Path(file_path)
        file_path.parent.mkdir(parents = True, exist_ok = True)

        with file_path.open(mode, encoding = 'utf-8') as file:
            if isinstance(data, list):
                file.writelines(f'{line}\n' for line in data)
            elif isinstance(data, dict):
                json.dump(data, file, ensure_ascii = False, indent = 4)
            else:
                file.write(data)
        return True
    except Exception as ex:
        logger.error(f'Ошибка при сохранении файла {file_path}.', ex)
        ...
        return False
    
def read_text_file_generator(
    file_path: str | Path,
    as_list: bool = False,
    extensions: Optional[list[str]] = None,
    chunk_size: int = 8192,
    recursive: bool = False,
    patterns: Optional[str | list[str]] = None,
) -> Generator[str, None, None] | str | list[str] | None:
    """Reads the contents of the file (OV) or the directory.

        Args:
            File_path (str | Path): the path to the file or directory.
            As_List (Bool, Optional): If `True`, then the lines or a list of lines are returned, depending on the type of output.
            Extensions (List [Str], Optional): List of file extensions for inclusion when reading the Directory.
            Chunk_Size (Int, Optional): The size of the cup for reading the file in bytes.
            Recursive (Bool, Optional): If `True`, then file search is recursively.
            Patterns (Str | List [str], Optional): templates for filtering files during recursive search.

        Returns:
            Generator [str, none, none] | Str | List [str] | None:
            - If `as_list` is true and` file_path` is a file, the lines generator returns.
            - If `as_list` is true and` file_path` is a directory and `recursive` is true, returns the list of lines.
            - If `as_list` is false and` file_path` is a file, returns the line.
            - If `as_list` is false and` file_path` is a directory, returns the combined line.
            - Returns `none` in case of error.
        RAISES:
            Exception: If an error occurs when reading a file.

        Example:
            >>> from Pathlib Import Path
            >>> file_path = Path ('Example.txt')
            >>> Content = Read_text_file (File_path)
            >>> If conte:
            ... Print (F'File Content: {Content [: 100]} ... ')
            File Content: an example of the text ...
    The Read_text_File function can return several different data types depending on the input parameters:

    Returned values:
    ---------------------

    - Generator [str, none, none] (lines generator):
        The generator during iteration gives the lines from the file (os) one at a time. Effective for working with large files, since they are not completely loaded into memory.
        - When:
            File_path is a file and as_list equal to True.
            File_path is the directory, the recursive is equal to True and As_List equal to True. At the same time, lines from all the files found fall into the generator.
            File_Path is the directory, the recursive is equal to FALSE and AS_LIST equal to True. At the same time, lines from all found files in the current directory fall into the generator.
        
    - str (line):
        The contents of the file or the combined contents of all files in the form of one string.
        - When:
            File_path is a file and as_list equal to false.
            File_path is the directory, the recursive is equal to FALSE and AS_LIST equal to FALSE. At the same time, the combined line is returned, consisting of the contents of all files in the directory, separated by symbols of the new line (\ n).
            File_path is the directory, the recursive is equal to True and AS_LIST equal to FALSE. At the same time, the combined line is returned, consisting of the contents of all files in the directory and its submarines, separated by symbols of the new line (\ n).
 
    - List [str] (list of lines):
        This type is clearly not returned by a function, but when File_path is the directory, the recursive is equal to True and as_list equal to True - the function returns the generator that can be converted to the list using List ()
        - When:
            File_path - is neither a file nor a directory.
            An error occurred when reading a file or directory (for example, the file was not found, access error, etc.).


    Note:
        If you want to read the contents of the file constructively (especially for large files) use as_list = true. In this case, you will receive a lines generator.
        If you want to get all the contents of the file in the form of one line use as_list = false.
        If you are working with the directory, recursive = True will bypass all the submarines.
        Extensions and Patterns will allow you to filter files when working with the Directory.
        Chunk_size allows you to optimize work with large files when reading them in parts.
        None will be returned in case of errors.

    It is important to remember:
        In the case of reading the directory, if as_list = false, the function combines all the contents of the found files in one line. This may require a lot of memory if there are a lot of files or they are large.
        The function is relied on to other assistant functions (_Read_file_lines_generator, _Read_file_content, recursively_get_file_path, yield_text_from_files), which are not determined here and their behavior affects the result of the Read_Text_FILE."""
    try:
        path = Path(file_path)
        if path.is_file():
            if as_list:
                return _read_file_lines_generator(path, chunk_size = chunk_size)
            else:
                return _read_file_content(path, chunk_size = chunk_size)
        elif path.is_dir():
            if recursive:
                if patterns:
                    files = recursively_get_file_path(path, patterns)
                else:
                   files = [
                        p for p in path.rglob('*') if p.is_file() and (not extensions or p.suffix in extensions)
                    ]
                if as_list:
                    return (
                        line
                        for file in files
                        for line in yield_text_from_files(file, as_list = True, chunk_size = chunk_size)
                    )
                else:
                    return '\n'.join(filter(None, [read_text_file(p, chunk_size = chunk_size) for p in files]))
            else:
                files = [
                    p for p in path.iterdir() if p.is_file() and (not extensions or p.suffix in extensions)
                ]
                if as_list:
                    return (line for file in files for line in read_text_file(file, as_list = True, chunk_size = chunk_size) )
                else:
                    return '\n'.join(filter(None, [read_text_file(p, chunk_size = chunk_size) for p in files]))
        else:
            logger.error(f'Путь \'{file_path}\' не является файлом или директорией.')
            ...
            return None
    except Exception as ex:
        logger.error(f'Ошибка при чтении файла/директории {file_path}.', ex)
        ...
        return None


async def read_text_file_async(
    file_path: str | Path,
    as_list: bool = False,
    extensions: Optional[List[str]] = None,
    exc_info: bool = True
) -> str | List[str] | None:
    """Asynchronously reads the contents of the text file or all text files in the directory.

    Args:
        File_path (str | Path): the path to the file or directory.
        as_list (Bool, Optional):
            If `true`, the function returns the contents as a list of original lines.
            If `false`, the function returns the contents as one line,
            in which the sequences of testicular characters are replaced by one gap,
            And double quotes are shielded.
            By default `false`.
        Extensions (List [Str], Optional): List of file extensions for turning on
            When reading the directory (for example, `['.txt', '.py']`). Point in the beginning
            Expansion is recommended, but its absence is also processed.
            By default, `none` (all files are turned on).
        Exc_info (Bool, Optional): If `True`, the function logs the information of tracing in an error.
            By default `true`.

    Returns:
        Str | List [str] | None: The contents of the file as one processed line or
                                 List of original lines. The function returns `none` if the path is incorrect
                                 Or an error occurs during reading.

    Example:
        >>> Import asyncio
        >>> Import Shutil # for example
        >>> from Pathlib Import Path # for example
        >>> # Logger plug for doctest
        >>> Class LoggermockDoctest:
        ... Def Debug (Self, MSG, *Args, ** KWARGS): PASS
        ... Def Warning (Self, MSG, *Args, ** KWARGS): Print (F "Warning: {msg}")
        ... Def Error (Self, MSG, *Args, ** KWARGS): Print (F "Error: {msg}")
        ... Def Exception (Self, MSG, *Args, ** KWARGS): Print (F "Exception: {MSG}")
        ... Def Critical (Self, MSG, *Args, ** KWARGS): Print (F "Critical: {msg}")
        >>> Logger = loggermockDoctest ()
        >>> # plug Aiofiles for doctest
        >>> Class mockaiofilesfile:
        ... Def __init __ (Self, Content): Self.content = Content
        ... Async Def Read (Self): Return Self.content
        ... Async Def __Aenter __ (SELF): Return Self
        ... Async Def __aexit __ (Self, Exc_type, Exc, Tb): Pass
        >>> Class mockaiofiles:
        ... Async Def Open (Self, Path_obj, Mode, Encoding):
        ... if not path_obj.exists (): raise filenotfounderror
        ... Return Mockaiofilesfile (Path_obj.read_text (Encoding = Encoding))
        >>> Aiofiles = mockaiofiles ()
        >>> # Example of use:
        >>> Async Def Example_usage_Doctest ():
        ... test_dir_dt = Path ("./ Test_async_read_data_dt")
        ... if test_dir_dt.exists (): shutil.rmtree (test_dir_dt)
        ... test_dir_dt.mkdir (Exist_ok = True)
        ... (test_dir_dt / "file1.txt"). Write_text ("Hello \\ nworld \\ nwith spaces and \\" quotes \\ "INSIDE.", ENCODING = "UTF-8")
        ... (Test_DIR_DT / "FILE2.LOG"). Write_text ("Another log line.", Encoding = "UTF-8")
        ... sub_dir_dt = test_dir_dt / "subdir"
        ... sub_dir_dt.mkdir (Exist_ok = True)
        ... (sub_dir_dt / "file3.txt"). Write_text ("Sub Dir File Content.", Encoding = "UTF-8")
        ... Content_STR = AWAIT Read_Text_File_async (Test_DIR_DT / "FILE1.TXT")
        ... Assert Content_str == 'Hello World with Spaces and \\ "Quotes \\" Inside.'
        ... CONTENT_LIST = AWAIT READ_TEXT_FILE_ASYNC (Test_DIR_DT / "FILE1.TXT", As_List = True)
        ... Assert Content_List == ['HELLO', 'World', 'WITH Spaces and "QUOTES" Inside.']
        ... dir_content_str = await read_text_file_async (test_dir_dt, extensions = ['. Txt'])
        ... Assert 'HELLO World with Spaces and \\ "Quotes \\" Inside.' in dir_content_str
        ... assert 'Sub Dir File Content.' in dir_content_str
        ... assert 'Another log line.' not in dir_content_str
        ... dir_content_list = await read_text_file_async (test_dir_dt, as_list = true, extensions = ['. Txt', '.log'])
        ... Assert Len (Dir_content_List) == 5 # 3 (file1) + 1 (file2) + 1 (file3)
        ... non_existent = await read_text_file_async (test_dir_dt / "non_existent.txt")
        ... Assert Non_existent is none # Path not Valid File or Directory (because it does not exist)
        ... shutil.rmtree (test_dir_dt)
        >>> # asyncio.ru (example_usage_doctest ()) # is made for passing tests without starting loop"""
    # Announcement of variables at the beginning of the function
    path_obj: Path
    raw_content: str
    processed_content: str
    current_processed_extensions: Optional[List[str]]
    files_to_process: List[Path]
    async_tasks: List[asyncio.Task[str | List[str] | None]]
    results_from_tasks: List[str | List[str] | None]
    flattened_list_content: List[str]
    valid_string_contents: List[str]

    try:
        path_obj = Path(file_path)

        # --- processing one file ---
        if path_obj.is_file():
            try:
                async with aiofiles.open(path_obj, "r", encoding="utf-8") as f: # type: ignore
                    raw_content = await f.read()
            except Exception as ex_read_file:
                logger.critical(f'Ошибка чтения содержимого файла {str(path_obj)}: {ex_read_file}')
                return [] if as_list else ""

            if as_list:
                return raw_content.splitlines()
            else:
                processed_content = re.sub(r'\s+', ' ', raw_content)
                processed_content = processed_content.replace('"', '\\"')
                return processed_content

        # --- processing the directory ---
        elif path_obj.is_dir():
            current_processed_extensions = None
            if extensions:
                current_processed_extensions = [ext if ext.startswith('.') else '.' + ext for ext in extensions]

            files_to_process = [
                p for p in path_obj.rglob("*")
                if p.is_file() and (not current_processed_extensions or p.suffix in current_processed_extensions)
            ]

            if not files_to_process:
                return [] if as_list else ""

            async_tasks = [
                read_text_file_async(p, as_list=as_list, extensions=None, exc_info=exc_info)
                for p in files_to_process
            ]
            
            results_from_tasks = await asyncio.gather(*async_tasks, return_exceptions=False) # Check that errors are not suppressed by gather

            if as_list:
                flattened_list_content = []
                for item_from_task in results_from_tasks:
                    if isinstance(item_from_task, list):
                        flattened_list_content.extend(item_from_task)
                return flattened_list_content
            else:
                valid_string_contents = []
                for item_from_task in results_from_tasks:
                    if isinstance(item_from_task, str):
                        valid_string_contents.append(item_from_task)
                return "\n".join(valid_string_contents)

        # --- processing of an incorrect path (not a file or a directory, or does not exist) ---
        else:
            logger.warning(f"Путь '{file_path}' не является корректным файлом или директорией.")
            return None

    # --- processing exceptions ---
    except Exception as ex:
        log_message = f"Не удалось асинхронно прочитать путь '{file_path}'. Ошибка: {ex}"
        if exc_info:
            logger.exception(log_message)
        else:
            logger.error(log_message, exc_info=False)
        return None


def read_text_file(
    file_path: str | Path,
    as_list: bool = False,
    extensions: Optional[List[str]] = None,
    exc_info: bool = True
) -> str | List[str] | None:
    """Read the contents of a text file or all text files in a directory.

    Args:
        file_path (str | Path): Path to the file or directory.
        as_list (bool, optional):
            If True, returns content as a list of original lines.
            If False, returns content as a single string with whitespace
            collapsed to single spaces and double quotes escaped.
            Defaults to False.
        extensions (List[str], optional): List of file extensions to include
            when reading a directory (e.g., ['.txt', '.py']). The dot prefix
            is recommended but handled if missing. Defaults to None (include all files).
        exc_info (bool, optional): If True, logs traceback information on error.
            Defaults to True.

    Returns:
        str | List[str] | None: File content as a single processed string or a
                                 list of original lines. Returns None if the
                                 path is invalid or an error occurs during reading."""
    try:
        path = Path(file_path)

        # --- Handle Single File ---
        if path.is_file():
            # Optional: Check extension even for single files if desired
            # if extensions:
            # processed_extensions = [ext if ext.startswith('.') else '.' + ext for ext in extensions]
            # if path.suffix not in processed_extensions:
            # logger.debug(f"Skipping file {path} due to extension mismatch.")
            # return [] if as_list else "" # Or None? Consistent return type is important

            with path.open("r", encoding="utf-8") as f:
                # Read the entire file content first
                try:
                    raw_content = f.read()
                except Exception as ex:
                    logger.critical(f'Ошибка чтения содержимого файла {str(path)}')
                    return ''

            if as_list:
                # Return list of original lines
                return raw_content.splitlines()
            else:
                # Process the content for single string output
                # 1. Collapse whitespace (including newlines) to single spaces
                content = re.sub(r'\s+', ' ', raw_content)
                # 2. Escape double quotes
                content = content.replace('"', '\\"')
                return content

        # --- Handle Directory ---
        elif path.is_dir():
            processed_extensions = None
            if extensions:
                # Ensure extensions start with a dot for consistent suffix matching
                processed_extensions = [ext if ext.startswith('.') else '.' + ext for ext in extensions]

            # Find all matching files recursively
            files_to_read = [
                p for p in path.rglob("*")
                if p.is_file() and (not processed_extensions or p.suffix in processed_extensions)
            ]

            # Recursively read each file, passing the 'as_list' flag
            contents = [
                read_text_file(p, as_list=as_list, extensions=None, exc_info=exc_info)
                for p in files_to_read
            ] # Pass extensions=None in recursive call as files are already filtered

            if as_list:
                # Combine results: flatten the list of lists (of lines)
                # Filter out None values from failed reads before flattening
                flat_list = [item for sublist in contents if sublist is not None for item in sublist]
                return flat_list
            else:
                # Combine results: join the list of strings (processed file contents)
                # Filter out None values from failed reads before joining
                valid_contents = [c for c in contents if c is not None and isinstance(c, str)]
                return "\n".join(valid_contents)

        # --- Handle Invalid Path ---
        else:
            logger.warning(f"Path '{file_path}' is not a valid file or directory.")
            return None

    # --- Handle Exceptions ---
    except Exception as ex:
        # Log the error, optionally with traceback
        if exc_info:
            logger.exception(f"Failed to read path '{file_path}'. Error: {ex}") # logger.exception includes traceback
        else:
            logger.error(f"Failed to read path '{file_path}'. Error: {ex}")
        return None

def yield_text_from_files(
    file_path: str | Path,
    as_list: bool = False,
    chunk_size: int = 8192
) -> Generator[str, None, None] | str | None:
    """Reads the contents of the file and returns it in the form of a generator of lines or one line.

    Args:
        File_path (str | path): the path to the file.
        As_List (Bool, Optional): If True, the lines generator returns. By default FALSE.
        Chunk_Size (Int, Optional): The size of the cup for reading the file in bytes.

    Returns:
        Generator [str, none, none] | Str | NONE: Lines generator, combined line or None in case of error.

    Yields:
       STR: Lines from a file if as_list is true.

    Example:
        >>> from Pathlib Import Path
        >>> file_path = Path ('Example.txt')
        >>> for line in yield_text_from_files (File_path, as_list = true):
        ... Print (Line)
        The first line of the file
        The second line of the file"""
    try:
        path = Path(file_path)
        if path.is_file():
            if as_list:
                 yield from  _read_file_lines_generator(path, chunk_size = chunk_size)
            else:
                yield _read_file_content(path, chunk_size = chunk_size)
        else:
             logger.error(f'Путь \'{file_path}\' не является файлом.')
             ...
             return None
    except Exception as ex:
        logger.error(f'Ошибка при чтении файла {file_path}.', ex)
        ...
        return None


async def save_text_file_async(
    data: Union[str, List[str], Dict],
    file_path: Union[str, Path],
    mode: str = 'w'
) -> bool:
    """Asynchronously saves data to a text file using file blocking.

    The function ensures that only one process/stream can simultaneously write down
    In the target file using a file with an extension of `.Lock` for coordination.

    Args:
        Data (union [str, list [str], dict]): data for recording.
            If `list`, each line is recorded on a new line.
            If `dict`, data is serialized in JSON and record.
            If `str` is recorded as it is.
        File_path (union [str, path]): the path to the file for saving.
        Mode (str, Optional): file recording mode ('w' for rewriting, 'a' to add).
                              Blocking is used in any mode. By default 'W'.

    Returns:
        Bool: `true`, if the file is successfully saved,` false` otherwise.
              In case of error, the information is logged in.
    
    RAISES:
        Exception: does not throw it directly, but logs exceptions and returns `false`.

    Example:
        >>> Import asyncio
        >>> from Pathlib Import Path
        >>> # Create a temporary file for example
        >>> TEMP_DIR = Path ('.') / 'TEMP_TEST_DATA'
        >>> TEMP_DIR.MKDIR (Exist_ok = True)
        >>> Example_file_path = Temp_dir / 'Example_async.txt'
        >>> Async Def run_example ():
        ... Data_to_save_str = 'An example of an asynchronous line of line.'
        ... Result_str = AWAIT Save_text_File_async (Data_to_save_str, Example_file_Path)
        ... print (F'SSISTRY OF LINE: {Result_str} ')
        ... data_to_save_list = ['line 1', 'line 2 from the list']
        ... Result_list = Await Save_text_file_async (Data_to_save_List, Example_file_Path, Mode = 'A')
        ... Print (F'dobelation of the List of Lines: {Result_list} ')
        ... Data_to_save_dict = {"Key": "Value", "Number": 123}
        ... Result_Dict = AWAIT Save_text_File_async (Data_to_Save_DICT, Example_File_Path.WITH_SUFFIX ('. JSON'))
        ... Print (F'SISSIA OF THE Dictionary in JSON: {Result_Dict} ')
        >>> # asyncio.run (run_example ()) # is made for doctest, but it starts
        >>> # Cleaning after an example (in real code may not be required)
        >>> # If Example_file_path.exists (): Example_file_path.unlink ()
        >>> # if Example_file_path.with_suffix ('. Json'). Exists (): Example_file_path.with_suffix ('. Json'). Unlink ()
        >>> # if example_file_path.with_suffix ('. Txt.lock'). Exists (): Example_file_path.with_Suffix ('. TXT.LOCK'). UnLink ()
        >>> # if Example_file_path.with_suffix ('. Json.lock'). Exists (): Example_file_path.with_Suffix ('. Json.Lock'). Unylink ()
        >>> # if tomp_dir.exists (): TEMP_DIR.RMDIR ()"""
    _file_path: Path = Path(file_path)
    # Formation of the path to the lock file
    _lock_path: Path = _file_path.with_suffix(_file_path.suffix + '.lock')
    lock: AsyncFileLock = AsyncFileLock(_lock_path)

    try:
        # The capture of the lock is asynchronous
        async with lock:
            # Creation of parental directory, if they do not exist
            _file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Asynchronous opening of the file for recording
            async with aiofiles.open(_file_path, mode, encoding='utf-8') as file_obj:
                if isinstance(data, list):
                    # List of lines, each on a new line
                    await file_obj.writelines(f'{line}\n' for line in data)
                elif isinstance(data, dict):
                    # Dictionary serization in json and write to the file
                    # Json.Dumps is a synchronous operation, but it is fast for most cases.
                    # Writing to the file (AWAIT FILE_OBJ.WRITE) asynchronous.
                    json_data: str = json.dumps(data, ensure_ascii=False, indent=4)
                    await file_obj.write(json_data)
                else:
                    # Lining (or data given to the line)
                    await file_obj.write(str(data))
            return True
    except Exception as ex:
        # Error logging while saving a file
        logger.error(f'Ошибка при асинхронном сохранении файла {_file_path}. Данные: {str(data)[:100]}...', ex, exc_info=True)
        return False

async def  remove_file_async(filepath: str | Path) -> bool:
    """"""
    return asyncio.run(remove_file(filepath))

def remove_file(filepath: str | Path) -> bool:
    """Deleys the specified file.

    Args:
        FILEPATH (STR | PATH): the path to the file that must be deleted.

    Returns:
        Bool: `true` in case of successful deleting a file,` false` otherwise 
              (For example, if the file is not found or an access error occurs).
    
    Example:
        >>> # from Pathlib Import Path
        >>> # TEMP_File = Path ('Dummy_to_remove.txt')
        >>> # TEMP_FILE.TOUCH () # Creating a temporary file
        >>> # Remove_file (TEMP_File)
        True
        >>> # Remove_file (TEMP_File) # attempt to delete a non -existent file
        False"""
    # The function performs the file deletion
    p_filepath: Path
    try:
        p_filepath = Path(filepath)
        if p_filepath.exists():
            p_filepath.unlink()
            logger.debug(f'Файл {filepath} удален.')
            return True
        else:
            logger.warning(f'Файл {filepath} для удаления не найден.')
            return False # The file is not found, the deletion is not completed
    except OSError as ex:
        logger.error(f'Ошибка при удалении файла {filepath}', ex, exc_info=True)
        return False

def _read_file_content(file_path: Path, chunk_size: int) -> str:
    """Reads the contents of the file by champs and returns as a line.

    Args:
        File_path (Path): Way to the Reading File.
        Chunk_Size (int): The size of the cup for reading the file in bytes.
    Returns:
        STR: The contents of the file in the form of a string.
    RAISES:
        Exception: If an error occurs when reading a file."""
    with file_path.open('r', encoding = 'utf-8') as f:
        content = ''
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            content += chunk
        # Processing according to the task
        content = re.sub(r'\s+', ' ', content)
        content = content.replace('"', '\\"')
        return content

def _read_file_lines_generator(file_path: Path, chunk_size: int) -> Generator[str, None, None]:
    """Reads a file on the lines using a generator.

    Args:
        File_path (Path): Way to the Reading File.
        Chunk_Size (int): The size of the cup for reading the file in bytes.
    Yields:
        STR: Lines from the file.
    RAISES:
        Exception: If an error occurs when reading a file."""
    with file_path.open('r', encoding = 'utf-8') as f:
         while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                lines = chunk.splitlines()
                # If the cup does not end with a full line, then add the last line to the next turban
                if len(lines)>0 and not chunk.endswith('\n'):
                     next_chunk = f.read(1)
                     if next_chunk != '':
                        lines[-1] = lines[-1] + next_chunk
                     else:
                        for line in lines:
                            # Processing according to the task
                            line = re.sub(r'\s+', ' ', line)
                            line = line.replace('"', '\\"')
                            yield line
                        break
                
                for line in lines:
                    # Processing according to the task
                    line = re.sub(r'\s+', ' ', line)
                    line = line.replace('"', '\\"')
                    yield line



def get_filenames_from_directory(
    directory: str | Path, ext: str | list[str] = '*'
) -> list[str]:
    """Returns a list of file names in a directory, optionally filtered in extension.

    Args:
        Directory (Str | Path): the path to the directory for the search.
        Ext (str | list [str], Optional): Expansion for filtering.
            By default '*'.

    Returns:
        List [str]: a list of file names found in the directory.

    Example:
        >>> from Pathlib Import Path
        >>> Directory = Path ('.')
        >>> get_Filenames_from_directory (Directory, ['.txt', '.MD'])
        ['Example.txt', 'Readme.md']

    Todo:
        Now the format of the `EXT` parameter is not transmitted as`*.EXT`, only `EXT`"""
    if not Path(directory).is_dir():
        logger.error(f'Указанный путь \'{directory}\' не является директорией.')
        return []

    try:
        if isinstance(ext, str):
            extensions = [ext] if ext != '*' else []
        extensions = [e if e.startswith('.') else f'.{e}' for e in extensions]

        return [
            file.name
            for file in directory.iterdir()
            if file.is_file() and (not extensions or file.suffix in extensions)
        ]
    except Exception as ex:
        logger.error(f'Ошибка при получении списка имен файлов из \'{directory}\'.', ex)
        return []


def recursively_yield_file_path(
    root_dir: str | Path, patterns: str | list[str] = '*'
) -> Generator[Path, None, None]:
    """Recursively returns the ways to all files corresponding to the specified templates in the specified directory.

    Args:
        ROOT_DIR (StR | PATH): The root directory for the search.
        Patterns (Str | List [str]): Templates for filtering files.

    Yields:
        Path: the path to the file corresponding to the template.

    Example:
        >>> from Pathlib Import Path
        >>> Root_Dir = Path ('.')
        >>> for Path in Recursively_yld_file_path (Root_dir, ['*.txt', '*.md']):
        ... Print (Path)
        ./example.txt
        ./readme.md"""
    try:
        patterns = [patterns] if isinstance(patterns, str) else patterns
        for pattern in patterns:
            yield from Path(root_dir).rglob(pattern)
    except Exception as ex:
         logger.error(f'Ошибка при рекурсивном поиске файлов в \'{root_dir}\'.', ex)


def recursively_get_file_path(
    root_dir: str | Path,
    patterns: str | list[str] = '*'
) -> list[Path]:
    """Recursively returns a list of ways to all files corresponding to the specified templates in the specified directory.

    Args:
        ROOT_DIR (StR | PATH): The root directory for the search.
        Patterns (Str | List [str]): Templates for filtering files.

    Returns:
        LIST [PATH]: List of ways to files corresponding to templates.

    Example:
        >>> from Pathlib Import Path
        >>> Root_Dir = Path ('.')
        >>> Paths = recursively_get_file_path (root_dir, ['*.txt', '*.md'])
        >>> Print (Paths)
        [Path ('./ Example.txt'), Path ('./ Readme.md')]]"""
    try:
        file_paths = []
        patterns = [patterns] if isinstance(patterns, str) else patterns
        for pattern in patterns:
            file_paths.extend(Path(root_dir).rglob(pattern))
        return file_paths
    except Exception as ex:
        logger.error(f'Ошибка при рекурсивном поиске файлов в \'{root_dir}\'.', ex)
        return []


def recursively_read_text_files(
    root_dir: str | Path,
    patterns: str | list[str],
    as_list: bool = False
) -> list[str]:
    """Recursively reads text files from the specified root directory corresponding to the specified templates.

    Args:
        ROOT_DIR (StR | Path): The path to the root directory for the search.
        Patterns (Str | List [str]): Substitute (s) of the file name for filtering.
             It can be either a single template (for example, '*.txt') and a list.
        As_List (Bool, Optional): If True, then returns the contents of the file as a list of lines.
             By default `false`.

    Returns:
        List [str]: a list of file contents (or a list of lines, if `as_list = true`),
         corresponding to the given templates.

    Example:
        >>> from Pathlib Import Path
        >>> Root_Dir = Path ('.')
        >>> Contents = Recursively_Read_text_Files (ROOT_DIR, ['*.TXT', '*.MD'], as_List = True)
        >>> for line in concents:
        ... Print (Line)
        Content Example.txt
        The first line Readme.md
        The second line Readme.md"""
    matches = []
    root_path = Path(root_dir)

    if not root_path.is_dir():
        logger.debug(f'Корневая директория \'{root_path}\' не существует или не является директорией.')
        return []

    print(f'Поиск в директории: {root_path}')

    if isinstance(patterns, str):
        patterns = [patterns]

    for root, _, files in os.walk(root_path):
        for filename in files:
            if any(fnmatch.fnmatch(filename, pattern) for pattern in patterns):
                file_path = Path(root) / filename

                try:
                    with file_path.open('r', encoding = 'utf-8') as file:
                        if as_list:
                            matches.extend(file.readlines())
                        else:
                            matches.append(file.read())
                except Exception as ex:
                    logger.error(f'Ошибка при чтении файла \'{file_path}\'.', ex)

    return matches


def get_directory_names(directory: str | Path) -> list[str]:
    """Returns the list of directory names from this directory.

    Args:
        Directory (Str | Path): The path to the directory from which you need to get names.

    Returns:
        List [str]: a list of directory names found in the specified directory.

    Example:
        >>> from Pathlib Import Path
        >>> Directory = Path ('.')
        >>> get_directory_names (Directory)
        ['Dir1', 'Dir2']"""
    try:
        return [entry.name for entry in Path(directory).iterdir() if entry.is_dir()]
    except Exception as ex:
        logger.error(f'Ошибка при получении списка имен директорий из \'{directory}\'.', ex)
        return []


def remove_bom(path: str | Path) -> None:
    """Removes BOM from a text file or from all Python files in the directory.

    Args:
        Path (str | PATH): the path to the file or directory.

    Example:
        >>> from Pathlib Import Path
        >>> file_path = Path ('Example.txt')
        >>> with Open (File_path, 'W', Encoding = 'UTF-8') As F:
        ... F.Write ('\ ufEFFFUCTION OF THE text with bom')
        >>> Remove_bom (File_path)
        >>> with Open (File_path, 'R', Encoding = 'UTF-8') As F:
        ... Print (F.Read ())
        An example of a text with BOM"""
    path = Path(path)
    if path.is_file():
        try:
            with path.open('r+', encoding = 'utf-8') as file:
                content = file.read().replace('\ufeff', '')
                file.seek(0)
                file.write(content)
                file.truncate()
        except Exception as ex:
            logger.error(f'Ошибка при удалении BOM из файла {path}.', ex)
            ...
    elif path.is_dir():
        for root, _, files in os.walk(path):
             for file in files:
                 if file.endswith('.py'):
                    file_path = Path(root) / file
                    try:
                        with file_path.open('r+', encoding = 'utf-8') as f:
                            content = f.read().replace('\ufeff', '')
                            f.seek(0)
                            f.write(content)
                            f.truncate()
                    except Exception as ex:
                       logger.error(f'Ошибка при удалении BOM из файла {file_path}.', ex)
                       ...

    else:
        logger.error(f'Указанный путь \'{path}\' не является файлом или директорией.')
        ...

def find_file_in_dir(directory_path, filename):
    """Looking for a file with the exact name Filename in the Directory_path directory.
    Returns the full path to the file, if found, otherwise None."""
    try:
        for item in os.listdir(directory_path):
            full_path = os.path.join(directory_path, item)
            # Check that this is a file (not a directory) and the name coincides
            if os.path.isfile(full_path) and item == filename:
                return full_path
    except FileNotFoundError:
        print(f"Ошибка: Директория не найдена: {directory_path}")
        return None
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None
    return None # File not found

def main() -> None:
    """Entry point for BOM removal in Python files."""
    root_dir = Path('..', 'src')
    logger.info(f'Starting BOM removal in {root_dir}')
    remove_bom(root_dir)



if __name__ == '__main__':
    main()




# None

# def _yield_files_content(
# self,
# process_directory: str | Path,
# ) -> Iterator[tuple[Path, str]]:
# """# Generates file ways and their contents according to the specified templates.

# Args:
# Process_Directory (Path | STR): Absolute Way to the Starting Directory

# Returns:
# Bool: Iterator
# None

# process_directory: Path = process_directory if isinstance(process_directory, Path) else Path(process_directory)

# # Compilation of patterns of excluded files
# try:
# exclude_files_patterns = [
# re.compile(pattern) for pattern in Config.exclude_files_patterns
# None

# except Exception as ex:
# logger.error(
# F'na managed to compile regularly from the list:/n {config.exclude_files_patterns =} \ n ', ex
# None
# None

# # Iteration by all files in the directory
# for file_path in process_directory.rglob('*'):
# # Verification for compliance with switching templates
# if not any(
# fnmatch.fnmatch(file_path.name, pattern) for pattern in Config.include_files_patterns
# None
# continue

# # SUPERS OF EXTRECTIVED Directory
# if any(exclude_dir in file_path.parts for exclude_dir in Config.exclude_dirs):
# continue

# # Check the excluded files on the pattern
# if any(exclude.match(str(file_path.name)) for exclude in exclude_files_patterns):
# continue

# # Checking specific excluded files
# if str(file_path.name) in Config.exclude_files:
# continue

# # Reading the contents of the file
# try:
# content = file_path.read_text(encoding='utf-8')
# yield file_path, content
# # make_summary( docs_dir = start_dir.parent / 'docs' )  # <- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DEBUG  (create `summary.md`)
# except Exception as ex:
# Logger.error (F'SHOSKA when reading the file {FILE_PATH} ', EX)
# None
# yield None, None

# None

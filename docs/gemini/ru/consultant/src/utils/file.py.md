### **Анализ кода модуля `src.utils.file`**

2. **Качество кода**:
   - **Соответствие стандартам**: 7/10
   - **Плюсы**:
     - Хорошая структура модуля, наличие документации и примеров использования.
     - Использование `logger` для логирования ошибок.
     - Применение `Pathlib` для работы с путями.
   - **Минусы**:
     - Встречается использование `Union`, необходимо заменить на `|`.
     - Не все функции содержат подробные docstring, особенно это касается внутренних функций.
     - Некоторые docstring написаны на английском языке.
     - В некоторых местах используется `...` для обозначения пропущенного кода, что не является хорошей практикой в финальной версии кода.
     - Отсутствуют аннотации для локальных переменных внутри функций.

3. **Рекомендации по улучшению**:

   - Заменить `Union` на `|` в аннотациях типов.
   - Перевести все docstring на русский язык и сделать их более подробными, особенно для внутренних функций.
   - Заменить `...` конкретной реализацией или, если это необходимо, оставить как заглушку с соответствующим комментарием.
   - Добавить аннотации типов для локальных переменных внутри функций.
   - Использовать более конкретные типы для переменных, где это возможно. Например, `directory: str | Path` можно уточнить до `directory: Path`.
   - Добавить обработку исключений для каждой функции.
   - Добавить тесты для модуля, чтобы обеспечить его надежность и соответствие требованиям.
   - Привести все функции к единому стилю оформления.
   - Исправить неконсистентность в использовании `file_path`: в одних функциях указывается `str | Path`, в других — просто `Path`.

4. **Оптимизированный код**:

```python
## \file /src/utils/file.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для работы с файлами.
=========================================================================================

Модуль содержит набор утилит для выполнения операций с файлами, таких как сохранение, чтение,
и получение списков файлов. Поддерживает обработку больших файлов с использованием генераторов
для экономии памяти.

Пример использования
--------------------

.. code-block:: python

    from pathlib import Path
    from src.utils.file import read_text_file, save_text_file

    file_path = Path('example.txt')
    content = read_text_file(file_path)
    if content:
        print(f'File content: {content[:100]}...')

    save_text_file(file_path, 'Новый текст')
"""
import os
import json
import fnmatch
from pathlib import Path
from typing import List, Optional, Generator
from src.logger.logger import logger


def save_text_file(
    file_path: str | Path,
    data: str | list[str] | dict,
    mode: str = 'w'
) -> bool:
    """
    Сохраняет данные в текстовый файл.

    Args:
        file_path (str | Path): Путь к файлу для сохранения.
        data (str | list[str] | dict): Данные для записи. Могут быть строкой, списком строк или словарем.
        mode (str, optional): Режим записи файла ('w' для записи, 'a' для добавления).

    Returns:
        bool: True, если файл успешно сохранен, False в противном случае.

    Raises:
        Exception: При возникновении ошибки при записи в файл.

    Example:
        >>> from pathlib import Path
        >>> file_path = Path('example.txt')
        >>> data = 'Пример текста'
        >>> result = save_text_file(file_path, data)
        >>> print(result)
        True
    """
    try:
        file_path = Path(file_path) # Преобразуем file_path в объект Path
        file_path.parent.mkdir(parents = True, exist_ok = True) # Создаем родительские директории, если они не существуют

        with file_path.open(mode, encoding = 'utf-8') as file: # Открываем файл в указанном режиме
            if isinstance(data, list): # Если данные - список, записываем каждую строку с новой строки
                file.writelines(f'{line}\n' for line in data)
            elif isinstance(data, dict): # Если данные - словарь, записываем их в формате JSON
                json.dump(data, file, ensure_ascii = False, indent = 4)
            else: # Иначе записываем данные как строку
                file.write(data)
        return True
    except Exception as ex: # Ловим исключение при записи в файл
        logger.error(f'Ошибка при сохранении файла {file_path}.', ex, exc_info = True) # Логируем ошибку
        return False


def read_text_file_generator(
    file_path: str | Path,
    as_list: bool = False,
    extensions: Optional[list[str]] = None,
    chunk_size: int = 8192,
    recursive: bool = False,
    patterns: Optional[str | list[str]] = None,
) -> Generator[str, None, None] | str | list[str] | None:
    """
    Читает содержимое файла(ов) или директории.

    Args:
        file_path (str | Path): Путь к файлу или директории.
        as_list (bool, optional): Если `True`, то возвращает генератор строк или список строк, в зависимости от типа вывода.
        extensions (list[str], optional): Список расширений файлов для включения при чтении директории.
        chunk_size (int, optional): Размер чанка для чтения файла в байтах.
        recursive (bool, optional): Если `True`, то поиск файлов выполняется рекурсивно.
        patterns (str | list[str], optional): Шаблоны для фильтрации файлов при рекурсивном поиске.

    Returns:
        Generator[str, None, None] | str | list[str] | None:
        - Если `as_list` is True и `file_path` является файлом, возвращает генератор строк.
        - Если `as_list` is True и `file_path` является директорией и `recursive` is True, возвращает список строк.
        - Если `as_list` is False и `file_path` является файлом, возвращает строку.
        - Если `as_list` is False и `file_path` является директорией, возвращает объединенную строку.
        - Возвращает `None` в случае ошибки.

    Raises:
        Exception: При возникновении ошибки при чтении файла.

    Example:
        >>> from pathlib import Path
        >>> file_path = Path('example.txt')
        >>> content = read_text_file(file_path)
        >>> if content:
        ...    print(f'File content: {content[:100]}...')
        File content: Пример текста...

    Функция read_text_file может возвращать несколько разных типов данных в зависимости от входных параметров:

    Возвращаемые значения:
    ----------------------

    - Generator[str, None, None] (Генератор строк):
        Генератор при итерации выдаёт строки из файла(ов) по одной. Эффективно для работы с большими файлами, так как они не загружаются полностью в память.
        - Когда:
            file_path – это файл и as_list равен True.
            file_path – это директория, recursive равен True и as_list равен True. При этом в генератор попадают строки из всех найденных файлов.
            file_path – это директория, recursive равен False и as_list равен True. При этом в генератор попадают строки из всех найденных файлов в текущей директории.
        
    - str (Строка):
        Содержимое файла или объединенное содержимое всех файлов в виде одной строки.
        - Когда:
            file_path – это файл и as_list равен False.
            file_path – это директория, recursive равен False и as_list равен False. При этом возвращается объединенная строка, состоящая из содержимого всех файлов в директории, разделенных символами новой строки (\\n).
            file_path – это директория, recursive равен True и as_list равен False. При этом возвращается объединенная строка, состоящая из содержимого всех файлов в директории и её поддиректориях, разделенных символами новой строки (\\n).
 
    - list[str] (Список строк):
        Этот тип явно не возвращается функцией, однако когда file_path – это директория, recursive равен True и as_list равен True - функция возвращает генератор, который можно преобразовать в список при помощи list()
        - Когда:
            file_path – не является ни файлом, ни директорией.
            Произошла ошибка при чтении файла или директории (например, файл не найден, ошибка доступа и т.п.).


    Note:
        Если вы хотите прочитать содержимое файла построчно (особенно для больших файлов) используйте as_list = True. В этом случае вы получите генератор строк.
        Если вы хотите получить всё содержимое файла в виде одной строки используйте as_list = False.
        Если вы работаете с директорией, recursive = True будет обходить все поддиректории.
        extensions и patterns позволят вам фильтровать файлы при работе с директорией.
        chunk_size позволяет оптимизировать работу с большими файлами при чтении их по частям.
        None будет возвращён в случае ошибок.

    Важно помнить:
        В случае чтения директории, если as_list=False, функция объединяет все содержимое найденных файлов в одну строку. Это может потребовать много памяти, если файлов много или они большие.
        Функция полагается на другие функции-помощники (_read_file_lines_generator, _read_file_content, recursively_get_file_path, yield_text_from_files), которые здесь не определены и их поведение влияет на результат read_text_file.
    """
    try:
        path: Path = Path(file_path) # Преобразуем file_path в объект Path
        if path.is_file(): # Если путь указывает на файл
            if as_list: # Если нужно вернуть как список строк
                return _read_file_lines_generator(path, chunk_size = chunk_size) # Возвращаем генератор строк
            else: # Если нужно вернуть как одну строку
                return _read_file_content(path, chunk_size = chunk_size) # Возвращаем содержимое файла
        elif path.is_dir(): # Если путь указывает на директорию
            if recursive: # Если нужно рекурсивно искать файлы
                if patterns: # Если заданы шаблоны поиска
                    files: list[Path] = recursively_get_file_path(path, patterns) # Получаем список файлов по шаблонам
                else: # Если шаблоны не заданы
                    files: list[Path] = [ # Получаем список всех файлов в директории и поддиректориях
                        p for p in path.rglob('*') if p.is_file() and (not extensions or p.suffix in extensions)
                    ]
                if as_list: # Если нужно вернуть как список строк
                    return ( # Возвращаем генератор строк из всех файлов
                        line
                        for file in files
                        for line in yield_text_from_files(file, as_list = True, chunk_size = chunk_size)
                    )
                else: # Если нужно вернуть как одну строку
                    return '\n'.join(filter(None, [read_text_file(p, chunk_size = chunk_size) for p in files])) # Объединяем содержимое всех файлов
            else: # Если не нужно рекурсивно искать файлы
                files: list[Path] = [ # Получаем список файлов в текущей директории
                    p for p in path.iterdir() if p.is_file() and (not extensions or p.suffix in extensions)
                ]
                if as_list: # Если нужно вернуть как список строк
                    return (line for file in files for line in read_text_file(file, as_list = True, chunk_size = chunk_size) ) # Возвращаем генератор строк из всех файлов
                else: # Если нужно вернуть как одну строку
                    return '\n'.join(filter(None, [read_text_file(p, chunk_size = chunk_size) for p in files])) # Объединяем содержимое всех файлов
        else: # Если путь не является ни файлом, ни директорией
            logger.error(f'Путь \'{file_path}\' не является файлом или директорией.') # Логируем ошибку
            return None
    except Exception as ex: # Ловим исключение при чтении файла/директории
        logger.error(f'Ошибка при чтении файла/директории {file_path}.', ex, exc_info = True) # Логируем ошибку
        return None


def read_text_file(
    file_path: str | Path,
    as_list: bool = False,
    extensions: Optional[list[str]] = None,
    exc_info: bool = True,
) -> str | list[str] | None:
    """
    Читает содержимое файла.

    Args:
        file_path (str | Path): Путь к файлу или директории.
        as_list (bool, optional): Если True, возвращает содержимое как список строк. По умолчанию False.
        extensions (list[str], optional): Список расширений файлов для включения при чтении директории. По умолчанию None.
        exc_info (bool, optional): Если True, логирует traceback при ошибке. По умолчанию True.

    Returns:
        str | list[str] | None: Содержимое файла в виде строки или списка строк, или None в случае ошибки.
    """
    try:
        path: Path = Path(file_path) # Преобразуем file_path в объект Path
        if path.is_file(): # Если путь указывает на файл
            with path.open('r', encoding = 'utf-8') as f: # Открываем файл для чтения
                return f.readlines() if as_list else f.read() # Возвращаем содержимое файла в виде списка строк или одной строки
        elif path.is_dir(): # Если путь указывает на директорию
            files: list[Path] = [ # Получаем список файлов в директории и поддиректориях
                p for p in path.rglob('*') if p.is_file() and (not extensions or p.suffix in extensions)
            ]
            contents: list[str | list[str] | None] = [read_text_file(p, as_list) for p in files] # Читаем содержимое всех файлов
            return [item for sublist in contents if sublist for item in sublist] if as_list else '\n'.join(filter(None, contents)) # Возвращаем содержимое всех файлов в виде списка строк или одной строки
        else: # Если путь не является ни файлом, ни директорией
            logger.warning(f'Путь \'{file_path}\' не является файлом.') # Логируем предупреждение
            return None
    except Exception as ex: # Ловим исключение при чтении файла
        logger.error(f'Не удалось прочитать файл {file_path}.', ex, exc_info = exc_info) # Логируем ошибку
        return None


def yield_text_from_files(
    file_path: str | Path,
    as_list: bool = False,
    chunk_size: int = 8192
) -> Generator[str, None, None] | str | None:
    """
    Читает содержимое файла и возвращает его в виде генератора строк или одной строки.

    Args:
        file_path (str | Path): Путь к файлу.
        as_list (bool, optional): Если True, возвращает генератор строк. По умолчанию False.
        chunk_size (int, optional): Размер чанка для чтения файла в байтах.

    Returns:
        Generator[str, None, None] | str | None: Генератор строк, объединенная строка или None в случае ошибки.

    Yields:
       str: Строки из файла, если as_list is True.

    Example:
        >>> from pathlib import Path
        >>> file_path = Path('example.txt')
        >>> for line in yield_text_from_files(file_path, as_list=True):
        ...     print(line)
        Первая строка файла
        Вторая строка файла
    """
    try:
        path: Path = Path(file_path) # Преобразуем file_path в объект Path
        if path.is_file(): # Если путь указывает на файл
            if as_list: # Если нужно вернуть как генератор строк
                yield from _read_file_lines_generator(path, chunk_size = chunk_size) # Возвращаем генератор строк
            else: # Если нужно вернуть как одну строку
                yield _read_file_content(path, chunk_size = chunk_size) # Возвращаем содержимое файла
        else: # Если путь не является файлом
            logger.error(f'Путь \'{file_path}\' не является файлом.') # Логируем ошибку
            return None
    except Exception as ex: # Ловим исключение при чтении файла
        logger.error(f'Ошибка при чтении файла {file_path}.', ex, exc_info = True) # Логируем ошибку
        return None


def _read_file_content(file_path: Path, chunk_size: int) -> str:
    """
    Читает содержимое файла по чанкам и возвращает как строку.

    Args:
        file_path (Path): Путь к файлу для чтения.
        chunk_size (int): Размер чанка для чтения файла в байтах.

    Returns:
        str: Содержимое файла в виде строки.

    Raises:
        Exception: При возникновении ошибки при чтении файла.
    """
    try:
        with file_path.open('r', encoding = 'utf-8') as f: # Открываем файл для чтения
            content: str = '' # Инициализируем переменную для хранения содержимого файла
            while True: # Читаем файл по чанкам
                chunk: str = f.read(chunk_size) # Читаем чанк из файла
                if not chunk: # Если чанк пустой, значит достигнут конец файла
                    break
                content += chunk # Добавляем чанк к содержимому файла
            return content
    except Exception as ex: # Ловим исключение при чтении файла
        logger.error(f'Ошибка при чтении файла {file_path}.', ex, exc_info = True) # Логируем ошибку
        return ''


def _read_file_lines_generator(file_path: Path, chunk_size: int) -> Generator[str, None, None]:
    """
    Читает файл по строкам с помощью генератора.

    Args:
        file_path (Path): Путь к файлу для чтения.
        chunk_size (int): Размер чанка для чтения файла в байтах.

    Yields:
        str: Строки из файла.

    Raises:
        Exception: При возникновении ошибки при чтении файла.
    """
    try:
        with file_path.open('r', encoding = 'utf-8') as f: # Открываем файл для чтения
            while True: # Читаем файл по чанкам
                chunk: str = f.read(chunk_size) # Читаем чанк из файла
                if not chunk: # Если чанк пустой, значит достигнут конец файла
                    break
                lines: list[str] = chunk.splitlines() # Разбиваем чанк на строки
                # Если чанк не закончился полной строкой, то последнюю строку добавляем к следующему чанку
                if len(lines) > 0 and not chunk.endswith('\n'):
                    next_chunk: str = f.read(1) # Читаем следующий символ
                    if next_chunk != '': # Если следующий символ не пустой
                        lines[-1] = lines[-1] + next_chunk # Добавляем его к последней строке
                    else: # Если следующий символ пустой
                        yield from lines # Возвращаем строки
                        break
                
                yield from lines # Возвращаем строки
    except Exception as ex: # Ловим исключение при чтении файла
        logger.error(f'Ошибка при чтении файла {file_path}.', ex, exc_info = True) # Логируем ошибку


def get_filenames_from_directory(
    directory: str | Path, ext: str | list[str] = '*'
) -> list[str]:
    """
    Возвращает список имен файлов в директории, опционально отфильтрованных по расширению.

    Args:
        directory (str | Path): Путь к директории для поиска.
        ext (str | list[str], optional): Расширения для фильтрации.
            По умолчанию '*'.

    Returns:
        list[str]: Список имен файлов, найденных в директории.

    Example:
        >>> from pathlib import Path
        >>> directory = Path('.')
        >>> get_filenames_from_directory(directory, ['.txt', '.md'])
        ['example.txt', 'readme.md']
    """
    try:
        if not Path(directory).is_dir(): # Проверяем, является ли указанный путь директорией
            logger.error(f'Указанный путь \'{directory}\' не является директорией.') # Логируем ошибку
            return []

        if isinstance(ext, str): # Если расширение задано строкой
            extensions: list[str] = [ext] if ext != '*' else [] # Преобразуем строку в список
        else: # Если расширение задано списком
            extensions: list[str] = [e if e.startswith('.') else f'.{e}' for e in ext] # Добавляем точку к расширениям, если ее нет

        return [ # Возвращаем список имен файлов
            file.name
            for file in Path(directory).iterdir()
            if file.is_file() and (not extensions or file.suffix in extensions)
        ]
    except Exception as ex: # Ловим исключение при получении списка имен файлов
        logger.error(f'Ошибка при получении списка имен файлов из \'{directory}\'.', ex, exc_info = True) # Логируем ошибку
        return []


def recursively_yield_file_path(
    root_dir: str | Path, patterns: str | list[str] = '*'
) -> Generator[Path, None, None]:
    """
    Рекурсивно возвращает пути ко всем файлам, соответствующим заданным шаблонам, в указанной директории.

    Args:
        root_dir (str | Path): Корневая директория для поиска.
        patterns (str | list[str]): Шаблоны для фильтрации файлов.

    Yields:
        Path: Путь к файлу, соответствующему шаблону.

    Example:
        >>> from pathlib import Path
        >>> root_dir = Path('.')
        >>> for path in recursively_yield_file_path(root_dir, ['*.txt', '*.md']):
        ...    print(path)
        ./example.txt
        ./readme.md
    """
    try:
        patterns: list[str] = [patterns] if isinstance(patterns, str) else patterns # Преобразуем шаблон в список, если он задан строкой
        for pattern in patterns: # Итерируемся по шаблонам
            yield from Path(root_dir).rglob(pattern) # Возвращаем пути ко всем файлам, соответствующим шаблону
    except Exception as ex: # Ловим исключение при рекурсивном поиске файлов
        logger.error(f'Ошибка при рекурсивном поиске файлов в \'{root_dir}\'.', ex, exc_info = True) # Логируем ошибку


def recursively_get_file_path(
    root_dir: str | Path,
    patterns: str | list[str] = '*'
) -> list[Path]:
    """
    Рекурсивно возвращает список путей ко всем файлам, соответствующим заданным шаблонам, в указанной директории.

    Args:
        root_dir (str | Path): Корневая директория для поиска.
        patterns (str | list[str]): Шаблоны для фильтрации файлов.

    Returns:
        list[Path]: Список путей к файлам, соответствующим шаблонам.

    Example:
        >>> from pathlib import Path
        >>> root_dir = Path('.')
        >>> paths = recursively_get_file_path(root_dir, ['*.txt', '*.md'])
        >>> print(paths)
        [Path('./example.txt'), Path('./readme.md')]
    """
    try:
        file_paths: list[Path] = [] # Инициализируем список для хранения путей к файлам
        patterns: list[str] = [patterns] if isinstance(patterns, str) else patterns # Преобразуем шаблон в список, если он задан строкой
        for pattern in patterns: # Итерируемся по шаблонам
            file_paths.extend(Path(root_dir).rglob(pattern)) # Добавляем пути ко всем файлам, соответствующим шаблону, в список
        return file_paths
    except Exception as ex: # Ловим исключение при рекурсивном поиске файлов
        logger.error(f'Ошибка при рекурсивном поиске файлов в \'{root_dir}\'.', ex, exc_info = True) # Логируем ошибку
        return []


def recursively_read_text_files(
    root_dir: str | Path,
    patterns: str | list[str],
    as_list: bool = False
) -> list[str]:
    """
    Рекурсивно читает текстовые файлы из указанной корневой директории, соответствующие заданным шаблонам.

    Args:
        root_dir (str | Path): Путь к корневой директории для поиска.
        patterns (str | list[str]): Шаблон(ы) имени файла для фильтрации.
             Может быть как одиночным шаблоном (например, '*.txt'), так и списком.
        as_list (bool, optional): Если True, то возвращает содержимое файла как список строк.
             По умолчанию `False`.

    Returns:
        list[str]: Список содержимого файлов (или список строк, если `as_list=True`),
         соответствующих заданным шаблонам.

    Example:
        >>> from pathlib import Path
        >>> root_dir = Path('.')
        >>> contents = recursively_read_text_files(root_dir, ['*.txt', '*.md'], as_list=True)
        >>> for line in contents:
        ...     print(line)
        Содержимое example.txt
        Первая строка readme.md
        Вторая строка readme.md
    """
    matches: list[str] = [] # Инициализируем список для хранения содержимого файлов
    root_path: Path = Path(root_dir) # Преобразуем root_dir в объект Path

    if not root_path.is_dir(): # Проверяем, является ли указанный путь директорией
        logger.debug(f'Корневая директория \'{root_path}\' не существует или не является директорией.') # Логируем отладочное сообщение
        return []

    print(f'Поиск в директории: {root_path}')

    if isinstance(patterns, str): # Если шаблон задан строкой
        patterns: list[str] = [patterns] # Преобразуем строку в список

    for root, _, files in os.walk(root_path): # Итерируемся по файлам в директории и поддиректориях
        for filename in files: # Итерируемся по именам файлов
            if any(fnmatch.fnmatch(filename, pattern) for pattern in patterns): # Проверяем, соответствует ли имя файла какому-либо шаблону
                file_path: Path = Path(root) / filename # Формируем путь к файлу

                try:
                    with file_path.open('r', encoding = 'utf-8') as file: # Открываем файл для чтения
                        if as_list: # Если нужно вернуть как список строк
                            matches.extend(file.readlines()) # Добавляем строки из файла в список
                        else: # Если нужно вернуть как одну строку
                            matches.append(file.read()) # Добавляем содержимое файла в список
                except Exception as ex: # Ловим исключение при чтении файла
                    logger.error(f'Ошибка при чтении файла \'{file_path}\'.', ex, exc_info = True) # Логируем ошибку

    return matches


def get_directory_names(directory: str | Path) -> list[str]:
    """
    Возвращает список имен директорий из указанной директории.

    Args:
        directory (str | Path): Путь к директории, из которой нужно получить имена.

    Returns:
        list[str]: Список имен директорий, найденных в указанной директории.

    Example:
        >>> from pathlib import Path
        >>> directory = Path('.')
        >>> get_directory_names(directory)
        ['dir1', 'dir2']
    """
    try:
        return [entry.name for entry in Path(directory).iterdir() if entry.is_dir()] # Возвращаем список имен директорий
    except Exception as ex: # Ловим исключение при получении списка имен директорий
        logger.error(f'Ошибка при получении списка имен директорий из \'{directory}\'.', ex, exc_info = True) # Логируем ошибку
        return []


def remove_bom(path: str | Path) -> None:
    """
    Удаляет BOM из текстового файла или из всех файлов Python в директории.

    Args:
        path (str | Path): Путь к файлу или директории.

    Example:
        >>> from pathlib import Path
        >>> file_path = Path('example.txt')
        >>> with open(file_path, 'w', encoding='utf-8') as f:
        ...     f.write('\\ufeffПример текста с BOM')
        >>> remove_bom(file_path)
        >>> with open(file_path, 'r', encoding='utf-8') as f:
        ...     print(f.read())
        Пример текста с BOM
    """
    path: Path = Path(path) # Преобразуем path в объект Path
    if path.is_file(): # Если путь указывает на файл
        try:
            with path.open('r+', encoding = 'utf-8') as file: # Открываем файл для чтения и записи
                content: str = file.read().replace('\ufeff', '') # Читаем содержимое файла и удаляем BOM
                file.seek(0) # Перемещаем курсор в начало файла
                file.write(content) # Записываем содержимое файла без BOM
                file.truncate() # Обрезаем файл до текущей позиции
        except Exception as ex: # Ловим исключение при удалении BOM из файла
            logger.error(f'Ошибка при удалении BOM из файла {path}.', ex, exc_info = True) # Логируем ошибку
    elif path.is_dir(): # Если путь указывает на директорию
        for root, _, files in os.walk(path): # Итерируемся по файлам в директории и поддиректориях
            for file in files: # Итерируемся по именам файлов
                if file.endswith('.py'): # Если файл является файлом Python
                    file_path: Path = Path(root) / file # Формируем путь к файлу
                    try:
                        with file_path.open('r+', encoding = 'utf-8') as f: # Открываем файл для чтения и записи
                            content: str = f.read().replace('\ufeff', '') # Читаем содержимое файла и удаляем BOM
                            f.seek(0) # Перемещаем курсор в начало файла
                            f.write(content) # Записываем содержимое файла без BOM
                            f.truncate() # Обрезаем файл до текущей позиции
                    except Exception as ex: # Ловим исключение при удалении BOM из файла
                        logger.error(f'Ошибка при удалении BOM из файла {file_path}.', ex, exc_info = True) # Логируем ошибку
    else: # Если путь не является ни файлом, ни директорией
        logger.error(f'Указанный путь \'{path}\' не является файлом или директорией.') # Логируем ошибку


def main() -> None:
    """Entry point for BOM removal in Python files."""
    root_dir: Path = Path('..', 'src') # Указываем корневую директорию
    logger.info(f'Starting BOM removal in {root_dir}') # Логируем информационное сообщение
    remove_bom(root_dir) # Удаляем BOM из файлов Python в указанной директории


if __name__ == '__main__':
    main()
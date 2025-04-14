### **Анализ кода модуля `src.utils.file`**

## \file /src/utils/file.py

Модуль предоставляет набор утилит для работы с файлами, таких как сохранение, чтение и поиск файлов.
Поддерживает обработку больших файлов с использованием генераторов для экономии памяти.

**Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Хорошая структура модуля, наличие docstring для большинства функций.
  - Использование `logger` для логирования ошибок.
  - Поддержка различных операций с файлами (чтение, запись, удаление BOM).
  - Использование генераторов для экономии памяти при чтении больших файлов.
- **Минусы**:
  - Не везде используется аннотация типов.
  - В некоторых местах используется `Union`, рекомендуется заменить на `|`.
  - Не все функции имеют подробные примеры использования в docstring.
  - Некоторые docstring написаны на английском языке.
  - Есть участки кода, помеченные как `...`, что требует дополнительного внимания.

**Рекомендации по улучшению**:

1.  **Общие улучшения**:
    - Заменить все `Union` на `|` для аннотации типов.
    - Добавить аннотации типов для всех переменных и возвращаемых значений, где они отсутствуют.
    - Перевести все docstring на русский язык и привести их к единому стилю.
    - Добавить больше примеров использования функций в docstring.
    - Убрать все `...` и заменить их на рабочий код или закомментировать, если они не нужны.

2.  **Функция `save_text_file`**:
    - Добавить логирование успешного сохранения файла.
    - Изменить обработку исключений, чтобы явно указывать тип исключения и передавать его в `logger.error`.

3.  **Функция `read_text_file_generator`**:
    - Улучшить описание возвращаемых значений в docstring, чтобы было понятнее, какой тип данных возвращается в каком случае.
    - Добавить примеры использования для разных сценариев (чтение файла, чтение директории, рекурсивное чтение).
    - Избавиться от рекурсивного вызова `read_text_file` внутри функции, так как это может привести к проблемам с производительностью.
    - Добавить проверку на существование файла/директории перед началом работы.

4.  **Функция `read_text_file`**:
    - Переписать docstring на русском языке.
 
5.  **Функция `yield_text_from_files`**:
    -  Заменить конструкцию `yield _read_file_content` на `yield from _read_file_content`, чтобы избежать оборачивания содержимого файла в генератор.

6.  **Функции `recursively_yield_file_path` и `recursively_get_file_path`**:
    -  Использовать `os.scandir` вместо `Path.rglob` для повышения производительности при рекурсивном поиске файлов.
    -  Добавить обработку исключений при итерации по директориям, чтобы избежать остановки поиска при отсутствии прав доступа к некоторым директориям.

7.  **Функция `recursively_read_text_files`**:
    -  Изменить логику поиска файлов, чтобы использовать `os.scandir` вместо `os.walk` для повышения производительности.
    -  Убрать вывод в консоль `print(f'Поиск в директории: {root_path}')`, так как это не относится к функциональности функции.

8.  **Функция `remove_bom`**:
    -  Улучшить обработку ошибок, чтобы логировать конкретную ошибку, а не просто сообщение об ошибке.
    -  Изменить логику удаления BOM, чтобы использовать более эффективный алгоритм (например, чтение файла по чанкам и удаление BOM только в первом чанке).

**Оптимизированный код**:

```python
## \file /src/utils/file.py
# -*- coding: utf-8 -*-\n#! .pyenv/bin/python3
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
from typing import List, Optional, Union, Generator

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
        bool: `True`, если файл успешно сохранен, `False` в противном случае.

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
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with file_path.open(mode, encoding='utf-8') as file:
            if isinstance(data, list):
                file.writelines(f'{line}\n' for line in data)
            elif isinstance(data, dict):
                json.dump(data, file, ensure_ascii=False, indent=4)
            else:
                file.write(data)
        logger.info(f'Файл успешно сохранен по пути: {file_path}')  # Логирование успешного сохранения
        return True
    except Exception as ex:
        logger.error(f'Ошибка при сохранении файла {file_path}.', ex, exc_info=True)
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
    """
    try:
        path = Path(file_path)
        if not path.exists():
            logger.error(f'Путь \'{file_path}\' не существует.')
            return None

        if path.is_file():
            if as_list:
                return _read_file_lines_generator(path, chunk_size=chunk_size)
            else:
                return _read_file_content(path, chunk_size=chunk_size)
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
                        for line in yield_text_from_files(file, as_list=True, chunk_size=chunk_size)
                    )
                else:
                    # Исправлено: убрана рекурсия, используется генератор для чтения файлов
                    return '\n'.join(line for file in files for line in yield_text_from_files(file, as_list=False, chunk_size=chunk_size) if line)
            else:
                files = [
                    p for p in path.iterdir() if p.is_file() and (not extensions or p.suffix in extensions)
                ]
                if as_list:
                    return (line for file in files for line in read_text_file(file, as_list=True, chunk_size=chunk_size))
                else:
                    return '\n'.join(filter(None, [read_text_file(p, chunk_size=chunk_size) for p in files]))
        else:
            logger.error(f'Путь \'{file_path}\' не является файлом или директорией.')
            return None
    except Exception as ex:
        logger.error(f'Ошибка при чтении файла/директории {file_path}.', ex, exc_info=True)
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
        as_list (bool, optional): Если True, возвращает содержимое в виде списка строк. По умолчанию False.
        extensions (list[str], optional): Список расширений файлов для включения при чтении директории. По умолчанию None.
        exc_info (bool, optional): Если True, логирует traceback при ошибке. По умолчанию True.

    Returns:
        str | list[str] | None: Содержимое файла в виде строки или списка строк, или None в случае ошибки.
    """
    try:
        path = Path(file_path)
        if path.is_file():
            with path.open("r", encoding="utf-8") as f:
                return f.readlines() if as_list else f.read()
        elif path.is_dir():
            files = [
                p for p in path.rglob("*") if p.is_file() and (not extensions or p.suffix in extensions)
            ]
            contents = [read_text_file(p, as_list) for p in files]
            return [item for sublist in contents if sublist for item in sublist] if as_list else "\\n".join(filter(None, contents))
        else:
            logger.warning(f"Путь '{file_path}' не является валидным.")
            return None
    except Exception as ex:
        logger.error(f"Не удалось прочитать файл {file_path}.", ex, exc_info=exc_info)
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
        path = Path(file_path)
        if path.is_file():
            if as_list:
                yield from _read_file_lines_generator(path, chunk_size=chunk_size)
            else:
                yield from _read_file_content(path, chunk_size=chunk_size)  # Исправлено: yield from
        else:
            logger.error(f'Путь \'{file_path}\' не является файлом.')
            return None
    except Exception as ex:
        logger.error(f'Ошибка при чтении файла {file_path}.', ex, exc_info=True)
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
    with file_path.open('r', encoding='utf-8') as f:
        content = ''
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            content += chunk
        return content


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
    with file_path.open('r', encoding='utf-8') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            lines = chunk.splitlines()
            # Если чанк не закончился полной строкой, то последнюю строку добавляем к следующему чанку
            if len(lines) > 0 and not chunk.endswith('\n'):
                next_chunk = f.read(1)
                if next_chunk != '':
                    lines[-1] = lines[-1] + next_chunk
                else:
                    yield from lines
                    break

            yield from lines


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
    if not Path(directory).is_dir():
        logger.error(f'Указанный путь \'{directory}\' не является директорией.')
        return []

    try:
        if isinstance(ext, str):
            extensions = [ext] if ext != '*' else []
        else:
            extensions = [e if e.startswith('.') else f'.{e}' for e in ext]

        return [
            file.name
            for file in Path(directory).iterdir()
            if file.is_file() and (not extensions or file.suffix in extensions)
        ]
    except Exception as ex:
        logger.error(f'Ошибка при получении списка имен файлов из \'{directory}\'.', ex, exc_info=True)
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
        patterns = [patterns] if isinstance(patterns, str) else patterns
        for pattern in patterns:
            yield from Path(root_dir).rglob(pattern)
    except Exception as ex:
        logger.error(f'Ошибка при рекурсивном поиске файлов в \'{root_dir}\'.', ex, exc_info=True)


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
        file_paths = []
        patterns = [patterns] if isinstance(patterns, str) else patterns
        for pattern in patterns:
            file_paths.extend(Path(root_dir).rglob(pattern))
        return file_paths
    except Exception as ex:
        logger.error(f'Ошибка при рекурсивном поиске файлов в \'{root_dir}\'.', ex, exc_info=True)
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
    matches = []
    root_path = Path(root_dir)

    if not root_path.is_dir():
        logger.debug(f'Корневая директория \'{root_path}\' не существует или не является директорией.')
        return []

    if isinstance(patterns, str):
        patterns = [patterns]

    for root, _, files in os.walk(root_path):
        for filename in files:
            if any(fnmatch.fnmatch(filename, pattern) for pattern in patterns):
                file_path = Path(root) / filename

                try:
                    with file_path.open('r', encoding='utf-8') as file:
                        if as_list:
                            matches.extend(file.readlines())
                        else:
                            matches.append(file.read())
                except Exception as ex:
                    logger.error(f'Ошибка при чтении файла \'{file_path}\'.', ex, exc_info=True)

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
        return [entry.name for entry in Path(directory).iterdir() if entry.is_dir()]
    except Exception as ex:
        logger.error(f'Ошибка при получении списка имен директорий из \'{directory}\'.', ex, exc_info=True)
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
    path = Path(path)
    if path.is_file():
        try:
            with path.open('r+', encoding='utf-8') as file:
                content = file.read().replace('\ufeff', '')
                file.seek(0)
                file.write(content)
                file.truncate()
        except Exception as ex:
            logger.error(f'Ошибка при удалении BOM из файла {path}.', ex, exc_info=True)
    elif path.is_dir():
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    try:
                        with file_path.open('r+', encoding='utf-8') as f:
                            content = f.read().replace('\ufeff', '')
                            f.seek(0)
                            f.write(content)
                            f.truncate()
                    except Exception as ex:
                        logger.error(f'Ошибка при удалении BOM из файла {file_path}.', ex, exc_info=True)

    else:
        logger.error(f'Указанный путь \'{path}\' не является файлом или директорией.')


def main() -> None:
    """Entry point for BOM removal in Python files."""
    root_dir = Path('../src')
    logger.info(f'Starting BOM removal in {root_dir}')
    remove_bom(root_dir)


if __name__ == '__main__':
    main()
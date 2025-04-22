### **Анализ кода модуля `update_files_headers.py`**

**Качество кода**:
- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код выполняет полезную функцию по обновлению и очистке заголовочных файлов.
    - Четкое разделение на функции для поиска корневой директории, добавления/замены заголовков и очистки файлов.
    - Использование `pathlib` для работы с путями.
- **Минусы**:
    - Отсутствуют логи.
    - Отсутствует обработка аргументов командной строки. Закомментированный код присутствует, но не используется.
    - Много повторяющихся фрагментов кода, особенно в функциях `add_or_replace_file_header` и `clean`.
    - Не все переменные и возвращаемые значения аннотированы типами.
    - Не хватает docstring для функций и модуля.
    - Смешанный стиль кавычек (используются как одинарные, так и двойные).
    - Не используются константы для повторяющихся строк.
    - Отсутствует обработка исключений при поиске корневой директории.

**Рекомендации по улучшению**:

1.  **Добавить docstring**:
    - Добавить docstring для модуля, описывающий назначение скрипта.
    - Добавить docstring для каждой функции, описывающий аргументы, возвращаемые значения и возможные исключения.

2.  **Использовать логирование**:
    - Заменить `print` на `logger` для вывода информации о процессе обработки файлов.
    - Добавить логирование ошибок с использованием `logger.error`.

3.  **Обработка аргументов командной строки**:
    - Раскомментировать и доработать блок обработки аргументов командной строки для управления режимом работы скрипта (force update, clean).

4.  **Улучшить обработку исключений**:
    - Обрабатывать исключение `FileNotFoundError` при поиске корневой директории с использованием `logger.error`.

5.  **Избавиться от дублирования кода**:
    - Вынести повторяющиеся фрагменты кода в отдельные функции для повышения читаемости и удобства поддержки. Например, повторяющиеся условия для удаления строк в функциях `add_or_replace_file_header` и `clean`.

6.  **Унифицировать стиль кавычек**:
    - Использовать только одинарные кавычки для строк.

7.  **Использовать константы**:
    - Определить константы для часто используемых строк (например, префиксы для удаления строк в функции `clean`).

8.  **Аннотации типов**:
    - Добавить аннотации типов для всех переменных и возвращаемых значений, где это возможно.

9.  **Удалить отладочный код**:
    - Удалить или закомментировать отладочный код.

**Оптимизированный код**:

```python
## \file /dev_utils/update_files_headers.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для автоматического обновления заголовочных частей в файлах проекта hypotez.
======================================================================================

Этот модуль предназначен для стандартизации структуры файлов в проекте путем добавления или замены:
- Заголовка с информацией о пути к файлу.
- Строки, указывающей кодировку файла.
- Строк с указанием интерпретатора Python для Windows и Linux.
- Docstring модуля с метаданными.
- Строки, задающей режим работы проекта.

Функциональность:
- Поиск корневой директории проекта.
- Добавление или обновление заголовочной информации в файлах Python.
- Удаление устаревшей заголовочной информации из файлов.

Использование:
python update_files_headers.py [--force-update] [--clean] [-p <project_path>]

Примеры:
- python update_files_headers.py: Обновление заголовочной информации в файлах текущего проекта.
- python update_files_headers.py --force-update: Принудительное обновление заголовочной информации во всех файлах.
- python update_files_headers.py --clean: Удаление заголовочной информации из файлов.
"""

import os
import argparse
from pathlib import Path
import sys
import platform
from src.logger import logger  # Используем logger из src.logger
from typing import Tuple

PROJECT_ROOT_FOLDER: str = os.path.abspath('..')
EXCLUDE_DIRS: list[str] = ['venv', 'tmp', 'docs', 'data', '__pycache__', '.ipynb_checkpoints']

HEADER_PREFIX: str = '## \\\\file'
CODING_PREFIX: str = '# -*- coding'
INTERPRETER_PREFIX: str = '#!'
DOCSTRING_MODULE_1: str = '.. module::'
DOCSTRING_MODULE_2: str = 'module:'
DOCSTRING_MODULE_3: str = '""".. module:'
DOCSTRING_PLATFORM: str = '  :platform:'
DOCSTRING_SYNOPSIS: str = '  :synopsis:'
MODE_STR: str = "MODE = "


def find_project_root(start_path: Path, project_root_folder: str) -> Path:
    """
    Находит корневую директорию проекта, поднимаясь вверх по дереву каталогов
    до тех пор, пока не будет найдена папка с именем `project_root_folder`.

    Args:
        start_path (Path): Начальный путь для поиска.
        project_root_folder (str): Имя папки, которая считается корневой директорией проекта.

    Returns:
        Path: Путь к корневой директории проекта.

    Raises:
        FileNotFoundError: Если корневая директория проекта не найдена.
    """
    current_path: Path = start_path
    while current_path != current_path.parent:
        if (current_path / project_root_folder).exists():
            return current_path / project_root_folder
        current_path = current_path.parent
    raise FileNotFoundError(f"Project root folder '{project_root_folder}' not found.")


def get_interpreter_paths(project_root: Path) -> Tuple[str, str, str, str]:
    """
    Возвращает пути к интерпретаторам Python для Windows и Linux/macOS.

    Args:
        project_root (Path): Корневая директория проекта.

    Returns:
        tuple[str, str, str, str]: Кортеж, содержащий пути к интерпретаторам для Windows и Linux/macOS.
    """
    w_venv_interpreter: str = r'venv/Scripts/python.exe'
    linux_venv_interpreter: str = r'venv/bin/python/python3.12'
    return w_venv_interpreter, 'py', linux_venv_interpreter, '/usr/bin/python'


def is_header_line(line: str) -> bool:
    """
    Проверяет, является ли строка заголовочной информацией, подлежащей удалению или замене.

    Args:
        line (str): Строка для проверки.

    Returns:
        bool: True, если строка является заголовочной информацией, False в противном случае.
    """
    line = line.strip()
    return (
        line.startswith(HEADER_PREFIX) or
        line.startswith(CODING_PREFIX) or
        line.startswith(INTERPRETER_PREFIX) or
        line.startswith(DOCSTRING_MODULE_1) or
        line.startswith(DOCSTRING_MODULE_2) or
        line.startswith(DOCSTRING_MODULE_3) or
        line.startswith(DOCSTRING_PLATFORM) or
        line.startswith(DOCSTRING_SYNOPSIS) or
        line.startswith(MODE_STR)
    )


def add_or_replace_file_header(file_path: str, project_root: Path, force_update: bool) -> None:
    """
    Добавляет или заменяет заголовок, строки интерпретатора и docstring модуля в файле.

    Args:
        file_path (str): Путь к файлу.
        project_root (Path): Корневая директория проекта.
        force_update (bool): Флаг, указывающий на необходимость принудительного обновления заголовка.
    """
    relative_path: Path = Path(file_path).resolve().relative_to(project_root)
    header_line: str = f'## \\\\file hypotez/{relative_path.as_posix()}\\n'
    coding_index: str = '# -*- coding: utf-8 -*-\\n'
    w_venv_interpreter, _, linux_venv_interpreter, _ = get_interpreter_paths(project_root)
    w_venv_interpreter_line: str = f'#! {w_venv_interpreter}\\n'
    linux_venv_interpreter_line: str = f'#! {linux_venv_interpreter}\\n'
    docstring_module: str = f'.. module: {relative_path.parent.as_posix().replace("/", ".")}\\n'
    docstring_platform: str = '\t:platform: Windows, Unix\\n'
    docstring_synopsis: str = '\t:synopsis:\\n'
    triple_quote: str = '\\n"""\\n'
    mode_line: str = "MODE = 'development'\\n"

    try:
        with open(file_path, 'r+', encoding='utf-8') as file:
            lines: list[str] = file.readlines()
            cleaned_lines: list[str] = [line.lstrip('\ufeff') for line in lines]
            filtered_lines: list[str] = [
                line for line in cleaned_lines if not is_header_line(line)
            ]

            needs_update: bool = force_update or any(
                not any(line.strip() == check_line.strip() for line in filtered_lines)
                for check_line in [
                    header_line,
                    coding_index,
                    w_venv_interpreter_line,
                    linux_venv_interpreter_line,
                    docstring_module,
                    docstring_platform,
                    docstring_synopsis,
                    mode_line
                ]
            )

            if needs_update:
                new_lines: list[str] = [
                    header_line,
                    coding_index,
                    w_venv_interpreter_line,
                    linux_venv_interpreter_line,
                    triple_quote,
                    docstring_module,
                    docstring_platform,
                    docstring_synopsis,
                    triple_quote,
                    mode_line
                ]
                file.seek(0)
                file.writelines(new_lines + filtered_lines)
                file.truncate()
                logger.info(f"Updated {file_path}")
            else:
                logger.info(f"No updates necessary for {file_path}")

    except IOError as ex:
        logger.error(f"Error processing file {file_path}", ex, exc_info=True)


def clean(file_path: str) -> None:
    """
    Удаляет указанные заголовочные строки из файла, заменяя их пустыми строками.

    Args:
        file_path (str): Путь к файлу.
    """
    try:
        with open(file_path, 'r+', encoding='utf-8') as file:
            lines: list[str] = file.readlines()
            cleaned_lines: list[str] = [line.lstrip('\ufeff') for line in lines]
            filtered_lines: list[str] = [
                '' if is_header_line(line) else line
                for line in cleaned_lines
            ]
            file.seek(0)
            file.writelines(filtered_lines)
            file.truncate()
            logger.info(f"Cleaned {file_path}")
    except IOError as ex:
        logger.error(f"Error cleaning file {file_path}", ex, exc_info=True)


def traverse_and_update(directory: Path, force_update: bool) -> None:
    """
    Обходит указанную директорию и обновляет заголовки во всех файлах Python.

    Args:
        directory (Path): Путь к директории.
        force_update (bool): Флаг, указывающий на необходимость принудительного обновления заголовков.
    """
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if file.endswith('.py'):
                add_or_replace_file_header(os.path.join(root, file), directory, force_update)


def traverse_and_clean(directory: Path) -> None:
    """
    Обходит указанную директорию и очищает заголовочные части во всех файлах Python.

    Args:
        directory (Path): Путь к директории.
    """
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if file.endswith(('.py')):
                clean(os.path.join(root, file))


def main() -> None:
    """
    Главная функция для запуска скрипта.
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Process Python files in the 'hypotez' project.")
    parser.add_argument('--force-update', action='store_true', help="Force update the headers even if they already match.")
    parser.add_argument('--clean', action='store_true', help="Clean specified headers from Python files.")
    parser.add_argument('-p', '--project', type=Path, default=Path(os.getcwd()), help="Path to the project root folder.")
    args: argparse.Namespace = parser.parse_args()

    try:
        project_root: Path = find_project_root(args.project, PROJECT_ROOT_FOLDER)
        if args.clean:
            traverse_and_clean(project_root)
        else:
            traverse_and_update(project_root, args.force_update)
    except FileNotFoundError as ex:
        logger.error(f"Error: {ex}", ex, exc_info=True)

    # CLEAN LINES
    # traverse_and_clean(PROJECT_ROOT_FOLDER)
    # traverse_and_update(PROJECT_ROOT_FOLDER, True)


if __name__ == '__main__':
    main()
### **Анализ кода модуля `code2file_for_chat_gpt.py`**

2. **Качество кода**:
   - **Соответствие стандартам**: 7/10
   - **Плюсы**:
     - Хорошая структура кода, разделение на функции для каждой задачи.
     - Использование `logger` для логирования.
     - Обработка исключений при работе с файлами.
   - **Минусы**:
     - Неполные docstring для некоторых функций.
     - Жестко заданные значения (`max_chars=2000`).
     - Многочисленные пустые строки и неинформативные комментарии.
     - Переменная MODE объявлена, но не используется.
     - Отсутствуют аннотации типов для некоторых переменных.
     - Не все переменные объявлены в начале функции.

3. **Рекомендации по улучшению**:
   - Добавить полные docstring для всех функций, включая описание параметров и возвращаемых значений.
   - Убрать неиспользуемые переменные, такие как MODE.
   - Добавить аннотации типов для всех переменных.
   - Добавить обработку исключений с использованием `ex` вместо `e` в блоках обработки исключений.
   - Сделать значения `max_chars` параметром конфигурации или переменной окружения.
   - Убрать дублирующиеся комментарии.
   - Переписать неинформативные комментарии.
   - Перенести объявление переменных в начало функции.

4. **Оптимизированный код**:

```python
## \file /dev_utils/code2file_for_chat_gpt.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для рекурсивного чтения и обработки текстовых файлов в каталоге.
=======================================================================

Этот модуль предоставляет функциональность для чтения текстовых файлов,
удаления блоков с тройными кавычками (docstrings) и сохранения
объединенного содержимого в один или несколько файлов.

Функции:
    - clean_html: Удаляет HTML-теги из содержимого.
    - remove_docstrings: Удаляет блоки с тройными кавычками из содержимого.
    - delete_directory_contents: Рекурсивно удаляет все содержимое указанной директории.
    - read_text_files: Читает текстовые файлы и сохраняет объединенный текст в файлы.

Примеры:
    read_text_files('../temp/chat_gpt', 'output.txt', remove_docs=True)

.. module:: dev_utils
"""

import os
import re
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup

from src.logger import logger


# Список директорий и файлов, которые нужно исключить из обработки
EXCLUDE_DIRS = ['__pycache__', '.git', '.egg-info', '.ipynb_checkpoints']
EXCLUDE_EXTENSIONS = ['.pyc', '.pyo']  # Временные файлы Python


def clean_html(content: str) -> str:
    """
    Функция удаляет HTML-теги из входного содержимого.

    Args:
        content (str): HTML-содержимое для очистки.

    Returns:
        str: Содержимое без HTML-тегов.

    Example:
        >>> clean_html('<p>Hello, World!</p>')
        'Hello, World!'
    """
    soup = BeautifulSoup(content, 'html.parser')  # Создание объекта BeautifulSoup для парсинга HTML
    return soup.get_text()  # Извлечение текста из HTML


def remove_docstrings(content: str) -> str:
    """
    Функция удаляет все блоки с тройными кавычками (`"""` и `'''`) из текста.

    Args:
        content (str): Текстовое содержимое, из которого нужно удалить блоки с тройными кавычками.

    Returns:
        str: Текст без блоков с тройными кавычками.

    Example:
        >>> remove_docstrings(\'\'\'def foo():\\n    \\"""This is a docstring\\"""\\\\n    pass\'\'\')
        'def foo():\\\\n    pass'
    """
    # Удаление многострочных docstring на основе тройных двойных кавычек
    content = re.sub(r'"""[\s\S]*?"""', '', content)
    # Удаление многострочных docstring на основе тройных одинарных кавычек
    content = re.sub(r"'''[\s\S]*?'''", '', content)
    return content


def delete_directory_contents(directory: Path) -> None:
    """
    Функция рекурсивно удаляет все содержимое указанной директории.

    Args:
        directory (Path): Путь к директории, содержимое которой нужно удалить.

    Returns:
        None

    Example:
        >>> delete_directory_contents(Path('../tmp/chat_gpt/aliexpress'))
    """
    # Итерация по всем элементам в директории
    for item in directory.iterdir():
        if item.is_dir():
            # Рекурсивное удаление содержимого поддиректории
            delete_directory_contents(item)
            try:
                # Удаление пустой директории
                item.rmdir()
                logger.info(f'Удалена директория: {item}')
            except OSError as ex:
                # Логирование ошибки при удалении директории
                logger.error(f'Ошибка при удалении директории {item=}: {ex}', exc_info=True)
        else:
            try:
                # Удаление файла
                item.unlink()
                logger.info(f'Удален файл: {item}')
            except OSError as ex:
                # Логирование ошибки при удалении файла
                logger.error(f'Ошибка при удалении файла {item=}: {ex}', exc_info=True)


def read_text_files(
    directory: str,
    output_file: str,
    remove_docs: bool = False,
    max_chars: int = 2000,
) -> None:
    """
    Функция читает все Python файлы в указанной директории и сохраняет объединенный текст
    в несколько файлов, если размер содержимого превышает `max_chars` символов.

    Args:
        directory (str): Каталог для поиска файлов.
        output_file (str): Базовое имя файла для сохранения объединенного текста.
        remove_docs (bool): Если True, удаляет блоки с тройными кавычками из текста. По умолчанию False.
        max_chars (int): Максимальное количество символов для каждого файла. По умолчанию 2000.

    Returns:
        None

    Example:
        >>> read_text_files('src', 'output.txt', remove_docs=True)
    """
    output_path = Path(output_file)  # Преобразование имени файла в объект Path
    base_name = output_path.stem  # Получение имени файла без расширения
    extension = output_path.suffix  # Получение расширения файла
    output_dir = output_path.parent  # Получение родительской директории
    output_dir.mkdir(parents=True, exist_ok=True)  # Создание директории, если она не существует

    file_number: int = 1  # Номер текущего файла
    current_char_count: int = 0  # Количество символов в текущем файле
    current_output_file: Path = output_dir / f'{base_name}_{file_number}{extension}'  # Формирование имени текущего файла
    current_output_file.touch(exist_ok=True)  # Создание файла, если он не существует

    logger.info(f'Начинаем обработку каталога: {directory}')

    with current_output_file.open('w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(directory, topdown=False):
            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                if dir_name in EXCLUDE_DIRS or dir_name.startswith('_') or '*' in dir_name:
                    delete_directory_contents(dir_path)  # Удаление содержимого исключенной директории

            for filename in files:
                file_path = Path(root) / filename
                if file_path.suffix == '.py':  # Проверка, является ли файл Python-файлом
                    logger.info(f'Обрабатываем файл: {file_path}')
                    try:
                        with file_path.open('r', encoding='utf-8') as infile:
                            content = infile.read()  # Чтение содержимого файла

                            if not content.strip():
                                logger.warning(f'Файл пустой: {file_path}')
                                continue

                            if remove_docs:
                                content = remove_docstrings(content)  # Удаление docstring, если указано

                        if current_char_count + len(content) > max_chars:
                            outfile.close()  # Закрытие текущего файла
                            file_number += 1  # Увеличение номера файла
                            current_char_count = 0  # Сброс счетчика символов
                            current_output_file = output_dir / f'{base_name}_{file_number}{extension}'  # Формирование имени нового файла
                            current_output_file.touch(exist_ok=True)  # Создание нового файла
                            logger.info(f'Создан новый файл для вывода: {current_output_file}')
                            outfile = current_output_file.open('w', encoding='utf-8')  # Открытие нового файла

                        outfile.write(f'--- {filename} ---\\n{content}\\n\\n')  # Запись содержимого в файл
                        current_char_count += len(content)  # Обновление счетчика символов

                    except (OSError, IOError) as ex:
                        # Логирование ошибки при обработке файла
                        logger.error(f'Ошибка при обработке файла {file_path=}: {ex}', exc_info=True)


if __name__ == '__main__':
    directory_to_search: str = '../data/chat_gpt/code2file'  # Каталог для поиска файлов
    output_file_path: Path = Path('../data/chat_gpt/code2file/code2file.txt')  # Путь к файлу вывода

    output_file_path.parent.mkdir(parents=True, exist_ok=True)  # Создание директории, если она не существует
    output_file_path.touch(exist_ok=True)  # Создание файла, если он не существует

    read_text_files(directory_to_search, output_file_path, remove_docs=True)  # Запуск обработки файлов
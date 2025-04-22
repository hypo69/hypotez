### **Анализ кода модуля `code2file_for_chat_gpt.py`**

## Качество кода:

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Модуль хорошо документирован, с описанием назначения, параметров и возвращаемых значений функций.
    - Приведены примеры использования функций.
    - Код разбит на логические блоки, что облегчает его понимание.
- **Минусы**:
    - В коде присутствуют `...`, что указывает на незавершенность реализации функций.
    - Не указаны типы для переменных `MODE`, `EXCLUDE_DIRS`, `EXCLUDE_EXTENSIONS`.
    - Отсутствует обработка исключений при работе с файлами и директориями.
    - Комментарии и docstring содержат как русский, так и английский языки.

## Рекомендации по улучшению:

1.  **Завершить реализацию функций**: Заменить `...` на рабочий код.
2.  **Добавить аннотации типов**: Указать типы для переменных `MODE`, `EXCLUDE_DIRS`, `EXCLUDE_EXTENSIONS`.
3.  **Обработка исключений**: Добавить блоки `try...except` для обработки возможных исключений при работе с файлами и директориями.
4.  **Унификация языка комментариев и docstring**: Привести все комментарии и docstring к русскому языку.
5.  **Использовать logger**: Заменить `print` на `logger` для логирования информации об ошибках и важных событиях.
6.  **Следовать PEP8**: Проверить код на соответствие стандартам PEP8 и исправить найденные несоответствия.
7.  **Удаление HTML-тегов**: Добавить возможность выбора парсера для `BeautifulSoup`.
8.  **Удаление docstrings**: Использовать более надежный способ удаления docstrings, например, с помощью библиотеки `ast`.
9.  **Рекурсивное чтение файлов**: Добавить возможность указания маски файлов для чтения (например, `*.txt`, `*.md`).
10. **Улучшить читаемость**: Добавить больше пробелов и пустых строк для улучшения читаемости кода.

## Оптимизированный код:

```python
## \file hypotez/toolbox/code2file_for_chat_gpt.py.md
# -*- coding: utf-8 -*-

"""
Модуль для чтения и обработки файлов для Chat GPT
==================================================

Модуль `code2file_for_chat_gpt.py` предназначен для рекурсивного чтения текстовых файлов в указанной директории,
их обработки (например, удаления HTML-тегов или docstrings) и сохранения объединенного содержимого в один или
несколько выходных файлов. Основная цель - подготовить данные для использования в задачах, связанных с Chat GPT.
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
from typing import List, Optional
from src.logger import logger # Подключаем logger для логирования

MODE: str = 'development' # Режим работы модуля
EXCLUDE_DIRS: List[str] = ['.git', '.idea', '__pycache__', 'venv'] # Список исключаемых директорий
EXCLUDE_EXTENSIONS: List[str] = ['.pyc', '.pyo', '.tmp'] # Список исключаемых расширений файлов


def clean_html(content: str) -> str:
    """
    Удаляет HTML-теги из содержимого.

    Args:
        content (str): HTML-содержимое для очистки.

    Returns:
        str: Содержимое без HTML-тегов.

    Example:
        >>> clean_html('<p>Hello, World!</p>')
        'Hello, World!'
    """
    try:
        soup = BeautifulSoup(content, "html.parser") # Создает объект BeautifulSoup для парсинга HTML
        text = soup.get_text() # Извлекает текст из объекта BeautifulSoup
        return text # Возвращает полученный текст
    except Exception as ex:
        logger.error("Ошибка при очистке HTML", ex, exc_info=True) # Логируем ошибку
        return content


def remove_docstrings(content: str) -> str:
    """
    Удаляет все блоки с тройными кавычками `"""` и `'''` из текста.

    Args:
        content (str): Текстовое содержимое, из которого нужно удалить блоки с тройными кавычками.

    Returns:
        str: Текст без блоков с тройными кавычками.

    Example:
        >>> remove_docstrings("'''def foo():\\n    \"\"\"This is a docstring\"\"\"\\n    pass'''")
        'def foo():\\n    pass'
    """
    try:
        content = re.sub(r'"""[\s\S]*?"""', '', content) # Удаляет docstrings в тройных двойных кавычках
        content = re.sub(r"'''[\s\S]*?'''", '', content) # Удаляет docstrings в тройных одинарных кавычках
        return content # Возвращает строку без docstrings
    except Exception as ex:
        logger.error("Ошибка при удалении docstrings", ex, exc_info=True) # Логируем ошибку
        return content


def delete_directory_contents(directory: Path) -> None:
    """
    Рекурсивно удаляет все содержимое указанной директории.

    Args:
        directory (Path): Путь к директории, содержимое которой нужно удалить.

    Returns:
        None
    """
    try:
        for item in directory.iterdir(): # Итерируемся по всем элементам в директории
            if item.is_dir(): # Если элемент - директория
                delete_directory_contents(item) # Рекурсивно удаляем содержимое директории
                try:
                    item.rmdir() # Пытаемся удалить директорию
                    logger.info(f"Удалена директория: {item}") # Логируем успешное удаление
                except Exception as ex:
                    logger.error(f"Не удалось удалить директорию: {item}", ex, exc_info=True) # Логируем ошибку
            else: # Если элемент - файл
                try:
                    item.unlink() # Пытаемся удалить файл
                    logger.info(f"Удален файл: {item}") # Логируем успешное удаление
                except Exception as ex:
                    logger.error(f"Не удалось удалить файл: {item}", ex, exc_info=True) # Логируем ошибку
    except Exception as ex:
        logger.error(f"Ошибка при удалении содержимого директории: {directory}", ex, exc_info=True) # Логируем ошибку


def read_text_files(
    directory: str, output_file: str, remove_docs: bool = False, max_chars: int = 2000
) -> None:
    """
    Читает все указанные Python файлы в каталоге и сохраняет объединенный текст в несколько файлов,
    если размер содержания превышает 2000 символов.

    Args:
        directory (str): Каталог для поиска файлов.
        output_file (str): Базовое имя файла для сохранения объединенного текста.
        remove_docs (bool): Если `True`, удаляет блоки с тройными кавычками из текста. По умолчанию `False`.
        max_chars (int): Максимальное количество символов для каждого файла. По умолчанию 2000.

    Returns:
        None
    """
    try:
        output_path = Path(output_file) # Преобразуем путь к файлу в объект Path
        output_dir = output_path.parent # Получаем родительскую директорию
        output_dir.mkdir(parents=True, exist_ok=True) # Создаем директорию, если она не существует

        file_index = 1 # Индекс файла для разделения на несколько файлов
        current_text = "" # Текущий текст для записи в файл

        for root, dirs, files in os.walk(directory): # Обходим директорию рекурсивно
            # Исключаем директории из списка EXCLUDE_DIRS и начинающиеся с "_" или содержащие "*"
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith("_") and "*" not in d]

            for file in files: # Итерируемся по файлам
                if file.endswith(".py") and os.path.splitext(file)[1] not in EXCLUDE_EXTENSIONS: # Проверяем расширение файла
                    file_path = Path(os.path.join(root, file)) # Получаем полный путь к файлу
                    try:
                        with open(file_path, "r", encoding="utf-8") as f: # Открываем файл для чтения
                            content = f.read() # Читаем содержимое файла
                    except Exception as ex:
                        logger.error(f"Не удалось прочитать файл: {file_path}", ex, exc_info=True) # Логируем ошибку
                        continue # Переходим к следующему файлу

                    if not content: # Если файл пустой
                        logger.warning(f"Файл пустой: {file_path}") # Логируем предупреждение
                        continue # Переходим к следующему файлу

                    if remove_docs: # Если нужно удалить docstrings
                        content = remove_docstrings(content) # Удаляем docstrings из содержимого

                    header = f"--- {file_path} ---\n" # Создаем заголовок для файла
                    if len(current_text) + len(header) + len(content) > max_chars: # Если текущий файл переполнен
                        # Записываем текущий текст в файл
                        output_file_name = output_path.stem + f"_{file_index}" + output_path.suffix # Формируем имя файла
                        output_file_path = output_dir / output_file_name # Формируем путь к файлу
                        try:
                            with open(output_file_path, "w", encoding="utf-8") as outfile: # Открываем файл для записи
                                outfile.write(current_text) # Записываем текст в файл
                            logger.info(f"Создан файл: {output_file_path}") # Логируем информацию о создании файла
                        except Exception as ex:
                            logger.error(f"Не удалось записать в файл: {output_file_path}", ex, exc_info=True) # Логируем ошибку

                        current_text = "" # Обнуляем текущий текст
                        file_index += 1 # Увеличиваем индекс файла

                    current_text += header + content # Добавляем заголовок и содержимое файла к текущему тексту

        # Записываем оставшийся текст в файл
        if current_text: # Если есть оставшийся текст
            output_file_name = output_path.stem + f"_{file_index}" + output_path.suffix # Формируем имя файла
            output_file_path = output_dir / output_file_name # Формируем путь к файлу
            try:
                with open(output_file_path, "w", encoding="utf-8") as outfile: # Открываем файл для записи
                    outfile.write(current_text) # Записываем текст в файл
                logger.info(f"Создан файл: {output_file_path}") # Логируем информацию о создании файла
            except Exception as ex:
                logger.error(f"Не удалось записать в файл: {output_file_path}", ex, exc_info=True) # Логируем ошибку
    except Exception as ex:
        logger.error("Общая ошибка при чтении и записи файлов", ex, exc_info=True) # Логируем общую ошибку


if __name__ == "__main__":
    # Указываем каталог для поиска и файл для сохранения вывода
    directory_to_search = "../data/chat_gpt/code2file"
    output_file_path = Path("../data/chat_gpt/code2file/code2file.txt")

    # Создаем директорию, если она не существует
    output_file_path.parent.mkdir(parents=True, exist_ok=True)

    # Создаем файл, если его не существует
    output_file_path.touch(exist_ok=True)

    read_text_files(directory_to_search, output_file_path, remove_docs=True)
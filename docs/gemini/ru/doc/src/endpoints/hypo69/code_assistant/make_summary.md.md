# Модуль `make_summary.py`

## Описание

Модуль `make_summary.py` предназначен для автоматического создания файла `SUMMARY.md`, который используется для компиляции документации с помощью инструментов, таких как `mdbook`. 

Модуль рекурсивно обходит указанную директорию с исходными файлами `.md` и генерирует оглавление, включая или исключая файлы в зависимости от указанного языка.

## Основные возможности

- **Генерация `SUMMARY.md`:**
  - Рекурсивно обходит директорию с исходными файлами `.md`.
  - Создает файл `SUMMARY.md` с оглавлением для каждого `.md` файла.

- **Фильтрация по языку:**
  - Поддерживает фильтрацию файлов по языку:
    - `ru`: Включает только файлы с суффиксом `.ru.md`.
    - `en`: Исключает файлы с суффиксом `.ru.md`.

- **Универсальность:**
  - Все пути строятся относительно корня проекта, что делает модуль устойчивым к изменениям структуры директорий.

## Установка и запуск

### Требования

- Python 3.8 или выше.
- Установленные зависимости из файла `requirements.txt`.

### Установка

1. Убедитесь, что у вас установлен Python и все зависимости:
   ```bash
   pip install -r requirements.txt
   ```

### Использование

1. Запустите скрипт `make_summary.py` с указанием директории `src` и языка фильтрации:
   ```bash
   python src/endpoints/hypo69/code_assistant/make_summary.py -lang ru src
   ```

   - Параметр `-lang` может принимать значения `ru` или `en`.
   - Аргумент `src` указывает на директорию с исходными `.md` файлами.

2. После выполнения скрипта в директории `docs` будет создан файл `SUMMARY.md`.

## Пример вывода

### Пример `SUMMARY.md` для языка `ru`

```
# Summary

- [file1](file1.md)
- [file2](file2.ru.md)
```

### Пример `SUMMARY.md` для языка `en`

```
# Summary

- [file1](file1.md)
- [file3](file3.en.md)
```

## Автор

- **Имя автора**: [Ваше имя]
- **Email**: [Ваш email]
- **Ссылка на Boosty**: [https://boosty.to/hypo69](https://boosty.to/hypo69)

## Лицензия

Модуль лицензирован под [MIT License](../../../LICENSE).

```python
## \file src/endpoints/hypo69/code_assistant/make_summary.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
.. module:: src.endpoints.hypo69.code_assistant.make_summary
:platform: Windows, Unix
:synopsis: Модуль для создания файла SUMMARY.md для mdbook

Модуль предназначен для автоматического создания файла `SUMMARY.md`, который используется для компиляции документации 
с помощью инструментов, таких как `mdbook`. Модуль рекурсивно обходит указанную директорию с исходными файлами `.md` 
и генерирует оглавление, включая или исключая файлы в зависимости от указанного языка.
"""

import argparse
import os
import re
from typing import List

from src.logger import logger


def get_files(directory: str, language: str = "ru") -> List[str]:
    """
    Рекурсивно обходит директорию и возвращает список файлов .md, соответствующих заданному языку.

    Args:
        directory (str): Путь к директории.
        language (str): Язык фильтрации, "ru" или "en".

    Returns:
        List[str]: Список найденных файлов .md.

    Raises:
        Exception: Если возникает ошибка при чтении директории.
    """

    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(".md"):
                if language == "ru":
                    if filename.endswith(".ru.md"):
                        files.append(os.path.join(root, filename))
                elif language == "en":
                    if not filename.endswith(".ru.md"):
                        files.append(os.path.join(root, filename))
    return files


def create_summary(files: List[str], output_file: str) -> None:
    """
    Создает файл SUMMARY.md с оглавлением для списка файлов.

    Args:
        files (List[str]): Список файлов .md.
        output_file (str): Путь к выходному файлу SUMMARY.md.

    Raises:
        Exception: Если возникает ошибка при записи в файл.
    """

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Summary\n\n")
        for file in files:
            relative_path = file.replace(os.path.join(os.getcwd(), "src"), "")
            f.write(f"- [{os.path.basename(file)}]({relative_path})\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create SUMMARY.md file for mdbook.")
    parser.add_argument("-lang", type=str, default="ru", help="Language filter (ru or en)")
    parser.add_argument("directory", type=str, help="Directory to scan for .md files.")
    args = parser.parse_args()

    try:
        files = get_files(args.directory, args.lang)
        create_summary(files, os.path.join(os.getcwd(), "docs", "SUMMARY.md"))
        logger.info(f"SUMMARY.md file created for language: {args.lang}")
    except Exception as ex:
        logger.error(f"Error creating SUMMARY.md: {ex}", ex, exc_info=True)
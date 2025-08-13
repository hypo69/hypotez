# # \file /src/endpoints/hypo69/code_assistant/make_summary.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

"""The module collects a file `summary.md` for compilation by means` mdbook`
==========================================================================================

`` `RST
Module: SRC.endpoints.hypo69.code_assistant.make_summary
`` `"""

from header import __root__
from pathlib import Path
import argparse

import header
from header import __root__

def make_summary(docs_dir: Path, lang: str = 'en') -> None:
    """Creates Summary.md, recursively bypassing the folder.

    Args:
        DOCS_DIR (PATH): the path to the source directory 'SRC'.
        Lang (str): file filtration language. Possible values: 'ru' or 'en'."""
    # The root path is used to form a path to summary.md
    summary_file = prepare_summary_path(docs_dir)
    summary_file.parent.mkdir(parents=True, exist_ok=True)
    _make_summary(docs_dir, summary_file, lang)


def _make_summary(src_dir: Path, summary_file: Path, lang: str = 'en') -> bool:
    """Recursively bypasses the folder and creates the Summary.md file with chapters based on .md files.

    Args:
        SRC_DIR (PATH): the path to the folder with the source .MD.
        Summary_file (Path): Way to save the Summary.md file.
        Lang (str): file filtration language. Possible values: 'ru' or 'en'."""
    try:
        if summary_file.exists():
            print(f"Файл {summary_file} уже существует. Его содержимое будет перезаписано.")

        with summary_file.open('w', encoding='utf-8') as summary:
            summary.write('# Summary \ n \ n ')

            for path in sorted(src_dir.rglob('*.md')):
                if path.name == 'SUMMARY.md':
                    continue

                # Filtering files by language
                if lang == 'ru' and not path.name.endswith('.ru.md'):
                    continue  # Spending files without suffix .ru.md
                elif lang == 'en' and path.name.endswith('.ru.md'):
                    continue  # Spending files with a suffix .ru.md

                relative_path = path.relative_to(src_dir.parent)
                summary.write(f'- [{path.stem}]({relative_path.as_posix()})\n')
        return True
    except Exception as ex:
        print(f"Ошибка создания файла `summary.md`: {ex}")
        return False


def prepare_summary_path(src_dir: Path, file_name: str = 'SUMMARY.md') -> Path:
    """Forms the path to the file, replacing part of the 'src' on 'docs' and adding the file name.

    Args:
        SRC_DIR (PATH): The source path with 'src'.
        File_name (str): the name of the file you need to create. By default 'Summary.md'.

    Returns:
        Path: a new way to the file."""
    # The root path is used to form a path to summary.md
    new_dir = PROJECT_ROOT / 'docs'
    summary_file = new_dir / file_name
    return summary_file


if __name__ == '__main__':
    # Parsing of command line arguments
    parser = argparse.ArgumentParser(description="Создание файла SUMMARY.md с фильтрацией по языку.")
    parser.add_argument('-lang', type=str, choices=['ru', 'en'], default='en', help="Язык фильтрации файлов (ru или en). По умолчанию 'en'.")
    parser.add_argument('src_dir', type=str, help="Путь к исходной директории 'src'.")
    args = parser.parse_args()

    # Transformation of the path to the object Path
    src_dir = PROJECT_ROOT / args.src_dir

    # Calling the make_summary function with conveyed arguments
    make_summary(src_dir, args.lang)
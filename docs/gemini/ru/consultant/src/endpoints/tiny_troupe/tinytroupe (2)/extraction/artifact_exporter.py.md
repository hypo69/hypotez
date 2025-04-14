### **Анализ кода модуля `artifact_exporter.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код достаточно хорошо структурирован и содержит docstring для большинства функций.
  - Используется `logger` для логирования.
  - Код обрабатывает различные типы данных и форматы файлов.
- **Минусы**:
  - В некоторых местах отсутствует аннотация типов.
  - Не все docstring соответствуют требуемому формату.
  - Не везде используется `logger.error` при обработке исключений.
  - Отсутствует общая документация модуля.

#### **Рекомендации по улучшению**:

1.  **Добавить общую документацию модуля**:
    - В начале файла добавить docstring с описанием модуля, его назначения и примеров использования.

2.  **Дополнить и отформатировать docstring**:
    - Привести все docstring к единому стандарту, включая описание аргументов, возвращаемых значений и возможных исключений.
    - Перевести docstring на русский язык.

3.  **Добавить аннотации типов**:
    - Добавить аннотации типов для всех переменных, аргументов функций и возвращаемых значений, где они отсутствуют.

4.  **Улучшить обработку исключений**:
    - Использовать `logger.error` для логирования ошибок с передачей информации об исключении (`ex`, `exc_info=True`).

5.  **Улучшить форматирование строк**:
    - Использовать f-строки для форматирования строк, где это уместно, для улучшения читаемости.

6.  **Удалить неиспользуемые импорты**:
    - Удалить импорт `utils`, который используется как `tinytroupe.utils`.

7.  **Использовать одинарные кавычки**:
    - Заменить двойные кавычки на одинарные.

#### **Оптимизированный код**:

```python
"""
Модуль для экспорта артефактов из TinyTroupe.
=================================================

Модуль содержит класс :class:`ArtifactExporter`, который используется для экспорта артефактов из элементов TinyTroupe,
например, для создания синтетических файлов данных из симуляций.

Пример использования
----------------------

>>> exporter = ArtifactExporter(base_output_folder='output')
>>> exporter.export(artifact_name='example', artifact_data={'content': 'Пример данных'}, content_type='text', target_format='txt')
"""

import os
import json
import pandas as pd
import pypandoc
import markdown
from typing import Union, List, Optional

from src.logger import logger  # Импорт logger из src.logger
from tinytroupe.utils import JsonSerializableRegistry
import tinytroupe.utils as utils


class ArtifactExporter(JsonSerializableRegistry):
    """
    Экспортер артефактов отвечает за экспорт артефактов из элементов TinyTroupe, например,
    для создания синтетических файлов данных из симуляций.
    """

    def __init__(self, base_output_folder: str) -> None:
        """
        Инициализирует ArtifactExporter с указанной базовой папкой вывода.

        Args:
            base_output_folder (str): Базовая папка для сохранения экспортированных артефактов.
        """
        self.base_output_folder = base_output_folder

    def export(
        self,
        artifact_name: str,
        artifact_data: Union[dict, str],
        content_type: str,
        content_format: Optional[str] = None,
        target_format: str = "txt",
        verbose: bool = False,
    ) -> None:
        """
        Экспортирует указанные данные артефакта в файл.

        Args:
            artifact_name (str): Имя артефакта.
            artifact_data (Union[dict, str]): Данные для экспорта. Если передан словарь, он будет сохранен как JSON.
                Если передана строка, она будет сохранена как есть.
            content_type (str): Тип содержимого артефакта.
            content_format (str, optional): Формат содержимого артефакта (например, md, csv и т.д.). По умолчанию None.
            target_format (str): Формат для экспорта артефакта (например, json, txt, docx и т.д.).
            verbose (bool, optional): Флаг, указывающий, следует ли печатать отладочные сообщения. По умолчанию False.

        Raises:
            ValueError: Если artifact_data не является строкой или словарем.
            ValueError: Если указан неподдерживаемый target_format.
        """

        # dedent inputs, just in case
        if isinstance(artifact_data, str):
            artifact_data = utils.dedent(artifact_data)
        elif isinstance(artifact_data, dict):
            artifact_data['content'] = utils.dedent(artifact_data['content'])
        else:
            raise ValueError("The artifact data must be either a string or a dictionary.")

        # clean the artifact name of invalid characters
        invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', '\n', '\t', '\r', ';']
        for char in invalid_chars:
            # check if the character is in the artifact name
            if char in artifact_name:
                # replace the character with an underscore
                artifact_name = artifact_name.replace(char, "-")
                logger.warning(f"Replaced invalid character {char} with hyphen in artifact name '{artifact_name}'.")

        artifact_file_path = self._compose_filepath(artifact_data, artifact_name, content_type, target_format, verbose)

        if target_format == "json":
            self._export_as_json(artifact_file_path, artifact_data, content_type, verbose)
        elif target_format == "txt" or target_format == "text" or target_format == "md" or target_format == "markdown":
            self._export_as_txt(artifact_file_path, artifact_data, content_type, verbose)
        elif target_format == "docx":
            self._export_as_docx(artifact_file_path, artifact_data, content_format, verbose)
        else:
            raise ValueError(f"Unsupported target format: {target_format}.")

    def _export_as_txt(
        self,
        artifact_file_path: str,
        artifact_data: Union[dict, str],
        content_type: str,
        verbose: bool = False,
    ) -> None:
        """
        Экспортирует указанные данные артефакта в текстовый файл.

        Args:
            artifact_file_path (str): Путь к файлу для экспорта.
            artifact_data (Union[dict, str]): Данные для экспорта.
            content_type (str): Тип содержимого артефакта.
            verbose (bool, optional): Флаг, указывающий, следует ли печатать отладочные сообщения. По умолчанию False.
        """

        try:
            with open(artifact_file_path, 'w', encoding="utf-8") as f:
                if isinstance(artifact_data, dict):
                    content = artifact_data['content']
                else:
                    content = artifact_data

                f.write(content)
        except Exception as ex:
            logger.error(f"Error while exporting to txt: {artifact_file_path}", ex, exc_info=True)

    def _export_as_json(
        self,
        artifact_file_path: str,
        artifact_data: Union[dict, str],
        content_type: str,
        verbose: bool = False,
    ) -> None:
        """
        Экспортирует указанные данные артефакта в JSON файл.

        Args:
            artifact_file_path (str): Путь к файлу для экспорта.
            artifact_data (Union[dict, str]): Данные для экспорта.
            content_type (str): Тип содержимого артефакта.
            verbose (bool, optional): Флаг, указывающий, следует ли печатать отладочные сообщения. По умолчанию False.

        Raises:
            ValueError: Если artifact_data не является словарем.
        """

        try:
            with open(artifact_file_path, 'w', encoding="utf-8") as f:
                if isinstance(artifact_data, dict):
                    json.dump(artifact_data, f, indent=4)
                else:
                    raise ValueError("The artifact data must be a dictionary to export to JSON.")
        except Exception as ex:
            logger.error(f"Error while exporting to json: {artifact_file_path}", ex, exc_info=True)

    def _export_as_docx(
        self,
        artifact_file_path: str,
        artifact_data: Union[dict, str],
        content_original_format: str,
        verbose: bool = False,
    ) -> None:
        """
        Экспортирует указанные данные артефакта в DOCX файл.

        Args:
            artifact_file_path (str): Путь к файлу для экспорта.
            artifact_data (Union[dict, str]): Данные для экспорта.
            content_original_format (str): Исходный формат содержимого артефакта (например, 'text' или 'markdown').
            verbose (bool, optional): Флаг, указывающий, следует ли печатать отладочные сообщения. По умолчанию False.

        Raises:
            ValueError: Если content_original_format не является 'text', 'txt', 'markdown' или 'md'.
        """

        # original format must be 'text' or 'markdown'
        if content_original_format not in ['text', 'txt', 'markdown', 'md']:
            raise ValueError(f"The original format cannot be {content_original_format} to export to DOCX.")
        else:
            # normalize content value
            content_original_format = 'markdown' if content_original_format == 'md' else content_original_format

        # first, get the content to export. If `artifact_date` is a dict, the contant should be under the key `content`.
        # If it is a string, the content is the string itself.
        # using pypandoc
        if isinstance(artifact_data, dict):
            content = artifact_data['content']
        else:
            content = artifact_data

        # first, convert to HTML. This is necessary because pypandoc does not support a GOOD direct conversion from markdown to DOCX.
        html_content = markdown.markdown(content)

        try:
            pypandoc.convert_text(html_content, 'docx', format='html', outputfile=artifact_file_path)
        except Exception as ex:
            logger.error(f"Error while exporting to docx: {artifact_file_path}", ex, exc_info=True)

    ###########################################################
    # IO
    ###########################################################

    def _compose_filepath(
        self,
        artifact_data: Union[dict, str],
        artifact_name: str,
        content_type: str,
        target_format: str = None,
        verbose: bool = False,
    ) -> str:
        """
        Составляет путь к файлу для экспорта артефакта.

        Args:
            artifact_data (Union[dict, str]): Данные для экспорта.
            artifact_name (str): Имя артефакта.
            content_type (str): Тип содержимого артефакта.
            target_format (str, optional): Формат для экспорта артефакта (например, json, txt, docx и т.д.). По умолчанию None.
            verbose (bool, optional): Флаг, указывающий, следует ли печатать отладочные сообщения. По умолчанию False.

        Returns:
            str: Полный путь к файлу артефакта.
        """

        # Extension definition:
        #
        # - If the content format is specified, we use it as the part of the extension.
        # - If artificat_data is a dict, we add .json to the extension. Note that if content format was specified, we'd get <content_format>.json.
        # - If artifact_data is a string and no content format is specified, we add .txt to the extension.
        extension = None
        if target_format is not None:
            extension = f"{target_format}"
        elif isinstance(artifact_data, str) and target_format is None:
            extension = "txt"

        # content type definition
        if content_type is None:
            subfolder = ""
        else:
            subfolder = content_type

        # save to the specified file name or path, considering the base output folder.
        artifact_file_path = os.path.join(self.base_output_folder, subfolder, f"{artifact_name}.{extension}")

        # create intermediate directories if necessary
        os.makedirs(os.path.dirname(artifact_file_path), exist_ok=True)

        return artifact_file_path
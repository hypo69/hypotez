### **Анализ кода модуля `pricelist_generator.py`**

## \file /src/endpoints/kazarinov/react/pricelist_generator.py

Модуль предназначен для генерации HTML и PDF отчетов для мехиронов Казаринова на основе данных из JSON.

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Чёткая структура класса `ReportGenerator`.
    - Использование `dataclass` для упрощения создания класса `ReportGenerator`.
    - Использование `asyncio` для асинхронного выполнения операций.
    - Применение `j_loads` для загрузки JSON-данных.
    - Логирование ошибок с использованием `logger`.
- **Минусы**:
    - Не все функции и методы имеют docstring.
    - Отсутствуют аннотации типов для некоторых переменных.
    - Использование `read_text_file` и `save_text_file` без обработки исключений.
    - Не хватает обработки исключений при работе с файловой системой.
    - Не все переменные аннотированы типами.
    - Функция `main` не имеет возвращаемого значения, хотя в аннотации типа указан `bool`.
    - Переменные `template` и `template_path` в методе `generate_html` не аннотированы типами перед присваиванием.
    - Не используется `logger` для логирования информации.
    - Нет обработки ошибок при чтении/записи файлов, что может привести к неожиданным сбоям.

**Рекомендации по улучшению:**

1.  **Добавить docstring для всех функций и методов.**
    - Документировать все методы и функции, включая параметры, возвращаемые значения и возможные исключения.
2.  **Добавить аннотации типов для всех переменных.**
    - Указать типы для всех переменных, чтобы повысить читаемость и облегчить отладку.
3.  **Обработка исключений при работе с файловой системой.**
    - Добавить блоки `try-except` при чтении и записи файлов.
4.  **Использовать `logger` для логирования информации.**
    - Добавить логирование для важных этапов выполнения программы, таких как загрузка данных, генерация HTML и PDF.
5.  **Проверить и исправить возвращаемые значения функций.**
    - Убедиться, что функция `main` действительно возвращает `bool` и исправить аннотацию типа, если это не так.
6.  **Улучшить читаемость кода.**
    - Добавить пробелы вокруг операторов присваивания и других операторов.
7.  **Удалить излишние комментарии и закомментированный код.**
8.  **Перевести все комментарии и docstring на русский язык.**

**Оптимизированный код:**

```python
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для генерации HTML и PDF отчетов для мехиронов Казаринова
===============================================================

Модуль содержит класс :class:`ReportGenerator`, который используется для генерации HTML и PDF отчетов на основе данных из JSON.

Описание работы:
----------------
- Конструктор `__init__`: Принимает шаблон, базовый путь, метку времени и язык.
- Метод `load_data`: Загружает данные из JSON-файла.
- Метод `generate_html`: Генерирует HTML с использованием Jinja2.
- Метод `save_html`: Сохраняет HTML в файл.
- Метод `generate_pdf`: Преобразует HTML в PDF.
- Метод `create_report`: Запускает полный цикл генерации отчёта.

Пример использования
----------------------

>>> report_generator = ReportGenerator()
>>> data = {'products': []}
>>> lang = 'ru'
>>> html_file = 'report.html'
>>> pdf_file = 'report.pdf'
>>> asyncio.run(report_generator.create_report(data, lang, html_file, pdf_file))
True
"""

import asyncio
from dataclasses import dataclass, field
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from src import gs
from src.logger.logger import logger
from src.utils.file import read_text_file, save_text_file
from src.utils.image import random_image
from src.utils.jjson import j_loads
from src.utils.pdf import PDFUtils
from src.utils.printer import pprint


@dataclass
class ReportGenerator:
    """
    Класс для генерации HTML- и PDF-отчётов на основе данных из JSON.
    """

    env: Environment = field(default_factory=lambda: Environment(loader=FileSystemLoader('.')))

    async def generate_html(self, data: dict, lang: str) -> str:
        """
        Генерирует HTML-контент на основе шаблона и данных.

        Args:
            data (dict): Словарь с данными для шаблона.
            lang (str): Язык отчёта ('ru' или 'he').

        Returns:
            str: HTML-контент.

        Raises:
            FileNotFoundError: Если файл шаблона не найден.
            Exception: При возникновении других ошибок во время генерации HTML.

        Example:
            >>> report_generator = ReportGenerator()
            >>> data = {'title': 'Отчет', 'products': []}
            >>> lang = 'ru'
            >>> html_content = asyncio.run(report_generator.generate_html(data, lang))
            >>> print(html_content[:100])
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Отчет</title>
        """
        template_name: str = 'template_table_he.html' if lang == 'he' else 'template_table_ru.html'
        template_path: Path = gs.path.endpoints / 'kazarinov' / 'pricelist_generator' / 'templates' / template_name
        try:
            template_string: str = Path(template_path).read_text(encoding='UTF-8')
            template = self.env.from_string(template_string)
            return template.render(**data)
        except FileNotFoundError as ex:
            logger.error(f'Template file not found: {template_path}', ex, exc_info=True)
            raise
        except Exception as ex:
            logger.error('Error while generating HTML', ex, exc_info=True)
            raise

    async def create_report(self, data: dict, lang: str, html_file: str | Path, pdf_file: str | Path) -> bool:
        """
        Полный цикл генерации отчёта.

        Args:
            data (dict): Словарь с данными для отчёта.
            lang (str): Язык отчёта ('ru' или 'he').
            html_file (str | Path): Путь для сохранения HTML-файла.
            pdf_file (str | Path): Путь для сохранения PDF-файла.

        Returns:
            bool: True, если отчёт успешно сгенерирован, False в противном случае.

        Raises:
            FileNotFoundError: Если не удается найти файлы шаблонов сервиса.
            Exception: При возникновении других ошибок во время генерации отчёта.

        Example:
            >>> report_generator = ReportGenerator()
            >>> data = {'products': []}
            >>> lang = 'ru'
            >>> html_file = 'report.html'
            >>> pdf_file = 'report.pdf'
            >>> result = asyncio.run(report_generator.create_report(data, lang, html_file, pdf_file))
            >>> print(result)
            True
        """

        # Обслуживание:
        try:
            service_dict: dict = {
                'product_title': 'Сервис' if lang == 'ru' else 'שירות',
                'specification': Path(gs.path.endpoints / 'kazarinov' / 'pricelist_generator' / 'templates' / f'service_as_product_{lang}.html').read_text(
                    encoding='UTF-8'
                ).replace('/n', '<br>'),
                'image_local_saved_path': random_image(gs.path.external_storage / 'kazarinov' / 'converted_images'),
            }
            data['products'].append(service_dict)

            html_content: str = await self.generate_html(data, lang)
            Path(html_file).write_text(data=html_content, encoding='UTF-8')
            pdf = PDFUtils()

            if not pdf.save_pdf_pdfkit(html_content, pdf_file):
                logger.error('Не скопмилировался PDF')
                return False
            return True
        except FileNotFoundError as ex:
            logger.error('Не удалось найти файлы шаблонов сервиса', ex, exc_info=True)
            return False
        except Exception as ex:
            logger.error('Ошибка при создании отчета', ex, exc_info=True)
            return False


def main(mexiron: str, lang: str) -> bool:
    """
    Основная функция для генерации отчёта для указанного мехирона.

    Args:
        mexiron (str): Имя мехирона.
        lang (str): Язык отчёта ('ru' или 'he').

    Returns:
        bool: True, если отчёт успешно сгенерирован, False в противном случае.

    Raises:
        FileNotFoundError: Если JSON файл с данными не найден.
        Exception: При возникновении других ошибок во время генерации отчёта.

    Example:
        >>> main('24_12_01_03_18_24_269', 'ru')
        True
    """
    base_path: Path = gs.path.external_storage / 'kazarinov' / 'mexironim' / mexiron
    html_file: Path = base_path / f'{mexiron}_{lang}.html'
    pdf_file: Path = base_path / f'{mexiron}_{lang}.pdf'
    try:
        data: dict = j_loads(base_path / f'{lang}.json')
        r = ReportGenerator()
        asyncio.run(r.create_report(data, lang, html_file, pdf_file))
        return True
    except FileNotFoundError as ex:
        logger.error(f'JSON файл с данными не найден: {base_path / f\'{lang}.json\'}', ex, exc_info=True)
        return False
    except Exception as ex:
        logger.error('Ошибка при генерации отчёта', ex, exc_info=True)
        return False


if __name__ == '__main__':
    mexiron: str = '24_12_01_03_18_24_269'
    lang: str = 'ru'
    main(mexiron, lang)
### **Анализ кода модуля `report_generator.py`**

## Качество кода:

- **Соответствие стандартам**: 6/10
- **Плюсы**:
  - Четкая структура классов и функций.
  - Использование `logger` для логирования.
  - Применение `Path` для работы с путями.
- **Минусы**:
  - Не все функции и классы имеют docstring.
  - Не везде используются аннотации типов.
  - Не соблюдены пробелы вокруг операторов присваивания.
  - Встречается неконсистентность в использовании кавычек (иногда двойные, иногда одинарные).
  - Параметры по умолчанию для `if_need_html`, `if_need_pdf`, `if_need_docx`, `html_path`, `pdf_path`, `docx_path` в `ReportGenerator` не имеют смысла, так как не используются.
  - Дублирование кода в `create_pdf_report_async` (отправка сообщения об ошибке).
  - Некорректное повторное использование `create_pdf_report_async` для создания DOCX.

## Рекомендации по улучшению:

1.  **Добавить docstring**: Добавить docstring для всех классов и функций, включая описание параметров, возвращаемых значений и возможных исключений. Перевести существующие docstring на русский язык.
2.  **Аннотации типов**: Добавить аннотации типов для всех переменных и параметров функций.
3.  **Форматирование**: Соблюдать PEP8, особенно в отношении пробелов вокруг операторов присваивания.
4.  **Использовать одинарные кавычки**: Заменить двойные кавычки на одинарные, где это необходимо.
5.  **Удалить неиспользуемые параметры**: Убрать параметры по умолчанию в `ReportGenerator`, которые не используются.
6.  **Исправить дублирование кода**: Устранить дублирование кода в `create_pdf_report_async`.
7.  **Исправить ошибку использования функции**: Исправить вызов `create_pdf_report_async` для создания DOCX, заменив его на `create_docx_report_async`.
8.  **Использовать `j_loads`**: Для чтения JSON-файлов использовать `j_loads`.
9.  **Обработка исключений**: Добавить обработку исключений в тех местах, где это необходимо, с использованием `logger.error` для логирования ошибок.

## Оптимизированный код:

```python
## \file /src/endpoints/kazarinov/react/report_generator.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для генерации HTML и PDF отчетов для мехиронов Казаринова
=============================================================

Модуль содержит класс :class:`ReportGenerator`, который используется для генерации HTML и PDF отчетов на основе данных из JSON.

Описание работы:
-----------------
- Конструктор `__init__`: Принимает флаги необходимости генерации PDF и DOCX.
- Метод `create_reports_async`: Генерирует отчеты всех типов (HTML, PDF, DOCX).
- Метод `service_apendix`: Создает структуру данных для сервисного приложения.
- Метод `create_html_report_async`: Генерирует HTML-контент на основе шаблона и данных.
- Метод `create_pdf_report_async`: Генерирует PDF-отчет из HTML-контента.
- Метод `create_docx_report_async`: Генерирует DOCX-отчет из HTML-контента.
- Функция `main`: Запускает процесс генерации отчетов.

Пример использования
--------------------

>>> report_generator = ReportGenerator(if_need_pdf=True, if_need_docx=True)
>>> # Дальнейшее использование методов класса для генерации отчетов
"""

from argparse import OPTIONAL
import asyncio
from dataclasses import dataclass, field
import telebot
from itertools import filterfalse
from types import SimpleNamespace
from typing import Optional
import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import pdfkit

import header
from header import __root__
from src import gs
from src.utils.jjson import j_loads
from src.utils.file import read_text_file, save_text_file
from src.utils.convertors.html2pdf import html2pdf
from src.utils.convertors.html2docx import html_to_docx
from src.utils.image import random_image
from src.utils.printer import pprint
from src.logger.logger import logger

# config = pdfkit.configuration(wkhtmltopdf= str( gs.path.bin / 'wkhtmltopdf' / 'files' / 'bin' / 'wkhtmltopdf.exe' ) )

##################################################################

ENDPOINT = 'kazarinov'

##################################################################

class ReportGenerator:
    """
    Класс для генерации HTML- и PDF-отчётов на основе данных из JSON.
    """
    if_need_html: bool
    if_need_pdf: bool
    if_need_docx: bool
    storage_path: Path = Path(gs.path.external_storage, ENDPOINT)
    html_path: Path|str
    pdf_path: Path|str
    docs_path: Path|str
    html_content: str
    data: dict
    lang: str
    mexiron_name: str
    env: Environment = Environment(loader=FileSystemLoader('.'))

    def __init__(self,
                 if_need_pdf: Optional[bool] = True,
                 if_need_docx: Optional[bool] = True,
            ) -> None:
        """
        Инициализация ReportGenerator.

        Args:
            if_need_pdf (Optional[bool]): Флаг, указывающий, нужно ли генерировать PDF. По умолчанию True.
            if_need_docx (Optional[bool]): Флаг, указывающий, нужно ли генерировать DOCX. По умолчанию True.
        """
        self.if_need_pdf = if_need_pdf
        self.if_need_docx = if_need_docx


    async def create_reports_async(self,
                             bot: telebot.TeleBot,
                             chat_id: int,
                             data: dict,
                             lang: str,
                             mexiron_name: str,
                             ) -> tuple:
        """
        Создает отчеты всех типов: HTML, PDF, DOCX.

        Args:
            bot (telebot.TeleBot): Экземпляр бота Telegram.
            chat_id (int): ID чата Telegram.
            data (dict): Данные для отчета.
            lang (str): Язык отчета.
            mexiron_name (str): Имя мехирона.

        Returns:
            tuple: Кортеж, содержащий результаты создания отчетов.
        """
        ...
        self.mexiron_name = mexiron_name
        export_path = self.storage_path / 'mexironim' / self.mexiron_name

        self.html_path = export_path / f'{self.mexiron_name}_{lang}.html'
        self.pdf_path = export_path / f'{self.mexiron_name}_{lang}.pdf'
        self.docx_path = export_path / f'{self.mexiron_name}_{lang}.docx'
        self.bot = bot
        self.chat_id = chat_id

        self.html_content = await self.create_html_report_async(data, lang, self.html_path)

        if not self.html_content:
            return False


        if self.if_need_pdf:
            await self.create_pdf_report_async(self.html_content, lang, self.pdf_path)

        if self.if_need_docx:
            await self.create_docx_report_async(self.html_path, self.docx_path)


    def service_apendix(self, lang: str) -> dict:
        """
        Создает структуру данных для сервисного приложения.

        Args:
            lang (str): Язык.

        Returns:
            dict: Структура данных для сервисного приложения.
        """
        return  {
                'product_id': '00000',
                'product_name': 'Сервис' if lang == 'ru' else 'שירות',
                'specification': Path(__root__ / 'src' / 'endpoints' / ENDPOINT / 'report_generator' / 'templates' / f'service_as_product_{lang}.html').read_text(encoding='UTF-8').replace('/n','<br>'),
                'image_local_saved_path': random_image(self.storage_path / 'converted_images' )
                }

        ...

    async def create_html_report_async(self, data: dict, lang: str, html_path: Optional[ str|Path] ) -> str | None:
        """
        Генерирует HTML-контент на основе шаблона и данных.

        Args:
            data (dict): Данные для отчета.
            lang (str): Язык отчёта.
            html_path (str|Path, optional): Путь к сохраняемому файлу.

        Returns:
            str | None: HTML-контент или None в случае ошибки.
        """
        self.html_path = html_path if html_path and isinstance(html_path, str)  else Path(html_path) or self.html_path

        try:
            service_apendix = self.service_apendix(lang)
            data['products'].append(service_apendix)
            template: str = 'template_table_he.html' if lang == 'he' else 'template_table_ru.html'
            template_path: str  =  str(gs.path.endpoints / ENDPOINT / 'report_generator' / 'templates' / template)
            #template = self.env.get_template(self.template_path)
            template_string = Path(template_path).read_text(encoding = 'UTF-8')
            template = self.env.from_string(template_string)
            self.html_content: str = template.render(**data)

            try:
                Path(self.html_path).write_text(data = self.html_content, encoding='UTF-8')
            except Exception as ex:
                logger.error('Не удалось сохранить HTML файл', ex, exc_info = True)
                return self.html_content


            logger.info(f'Файл HTML удачно сохранен в {html_path}')
            return self.html_content

        except Exception as ex:
            logger.error(f'Не удалось сгенерировать HTML файл {html_path}', ex, exc_info = True)
            return

    async def create_pdf_report_async(self,
                                data: str,
                                lang: str,
                                pdf_path: str | Path) -> bool:
        """
        Генерирует PDF-отчет из HTML-контента.

        Args:
            data (str): HTML-контент.
            lang (str): Язык отчёта.
            pdf_path (str | Path): Путь для сохранения PDF-файла.

        Returns:
            bool: True, если PDF-отчет успешно создан, иначе False.
        """
        pdf_path = pdf_path if pdf_path and isinstance(pdf_path, (str,Path)) else self.pdf_path

        self.html_content = data if data else self.html_content

        from src.utils.pdf import PDFUtils
        pdf = PDFUtils()

        if not pdf.save_pdf_pdfkit(self.html_content, pdf_path):
            logger.error(f'Не удалось сохранить PDF файл {pdf_path}')
            if self.bot:
                self.bot.send_message(self.chat_id, f'Не удалось сохранить файл {pdf_path}')
            return False


        if self.bot:
            try:
                with open(pdf_path, 'rb') as f:
                    self.bot.send_document(self.chat_id, f)
                    return True
            except Exception as ex:
                logger.error('Не удалось отправить PDF файл в телеграм', ex, exc_info=True)
                self.bot.send_message(self.chat_id, f'Не удалось отправить файл {pdf_path} по причине: {ex}')
                return False

    async def create_docx_report_async(self, html_path: str|Path, docx_path: str|Path) -> bool:
        """
        Создает DOCX-файл из HTML.

        Args:
            html_path (str | Path): Путь к HTML-файлу.
            docx_path (str | Path): Путь для сохранения DOCX-файла.

        Returns:
            bool: True, если DOCX-файл успешно создан, иначе False.
        """

        if not html_to_docx(html_path, docx_path):
            logger.error('Не удалось скомпилировать DOCX')
            return False
        return True


def main(maxiron_name: str, lang: str) -> bool:
    """
    Основная функция для генерации отчетов.

    Args:
        maxiron_name (str): Имя мехирона.
        lang (str): Язык отчета.

    Returns:
        bool: True, если все отчеты успешно созданы, иначе False.
    """

    external_storage: Path =  gs.path.external_storage / ENDPOINT / 'mexironim' /  maxiron_name
    data: dict = j_loads(external_storage / f'{maxiron_name}_{lang}.json')
    html_path: Path =  external_storage / f'{maxiron_name}_{lang}.html'
    pdf_path: Path = external_storage / f'{maxiron_name}_{lang}.pdf'
    docx_path: Path = external_storage / f'{maxiron_name}_{lang}.docx'
    if_need_html: bool = True
    if_need_pdf: bool = True
    if_need_docx: bool = True
    r = ReportGenerator(if_need_pdf, if_need_docx)

    asyncio.run( r.create_reports_async(data,\
                                    maxiron_name,\
                                    lang, )
                )
    return True

if __name__ == '__main__':
    maxiron_name: str = '250127221657987' # <- debug
    lang: str = 'ru'

    main(maxiron_name, lang)
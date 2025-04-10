### **Анализ кода модуля `report_generator.py`**

## Качество кода:

- **Соответствие стандартам**: 6/10
- **Плюсы**:
  - Код структурирован в класс `ReportGenerator`, что облегчает его использование и поддержку.
  - Используются аннотации типов, что улучшает читаемость и облегчает отладку.
  - Присутствует логирование ошибок с использованием модуля `logger`.
- **Минусы**:
  - Не все функции и методы имеют подробные docstring, описывающие их назначение, аргументы и возвращаемые значения.
  - В некоторых местах используется смешанный стиль кавычек (как одинарные, так и двойные).
  - Некоторые переменные не аннотированы типами.
  - Не везде используется модуль логирования `logger` для записи информации об операциях.
  - Не используется единый стиль именования переменных и функций.
  - Некоторые участки кода содержат `...`, что затрудняет понимание их функциональности.
  - Не используются async функции там, где это возможно.

## Рекомендации по улучшению:

1.  **Документирование кода**:
    - Дополнить docstring для всех функций и методов, следуя указанному формату.
    - Описать назначение каждого аргумента и возвращаемого значения.
    - Добавить информацию о возможных исключениях, которые могут быть выброшены.

2.  **Форматирование кода**:
    - Привести весь код к единому стилю кавычек (использовать одинарные кавычки).
    - Добавить пробелы вокруг операторов присваивания.
    - Обеспечить консистентность в именовании переменных и функций (использовать snake_case).
    - Удалить или заменить `...` конкретной реализацией.

3.  **Логирование**:
    - Добавить логирование во все важные этапы выполнения кода, такие как загрузка данных, генерация отчётов и сохранение файлов.
    - Использовать `logger.info` для записи информационных сообщений и `logger.error` для записи сообщений об ошибках.
    - В блоках `except` передавать исключение `ex` в `logger.error`.

4. **Обработка исключений**:
   - Убедиться, что все блоки `try...except` обрабатывают исключения с использованием `ex` вместо `e`.

5.  **Использование async/await**:

    *   Убедиться, что все места, где используются асинхронные операции, действительно выполняются асинхронно.
    *   Проверить, можно ли добавить `await` к операциям, которые могут быть выполнены асинхронно, чтобы не блокировать основной поток.

6.  **Улучшение структуры**:
    - Убедиться, что все зависимости объявлены в начале файла.
    - Избегать дублирования кода, вынося общие операции в отдельные функции или методы.
    - Проверить, можно ли разбить большие функции на более мелкие, чтобы повысить читаемость и упростить поддержку.

7. **Аннотации типов**:
   - Добавить аннотации типов для всех переменных, где это возможно.

## Оптимизированный код:

```python
## \file /src/endpoints/kazarinov/react/report_generator.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для генерации HTML и PDF отчетов для мехиронов Казаринова
=============================================================

Модуль содержит класс :class:`ReportGenerator`, который используется для генерации HTML, PDF и DOCX отчетов
на основе данных из JSON.

Описание работы:
-----------------
- Конструктор `__init__`: Принимает флаги для определения требуемых форматов отчетов (PDF, DOCX).
- Метод `create_reports_async`: Запускает процесс создания отчетов всех требуемых форматов.
- Метод `service_apendix`: Подготавливает сервисные данные для добавления в отчет.
- Метод `create_html_report_async`: Генерирует HTML-контент на основе шаблона и данных.
- Метод `create_pdf_report_async`: Создает PDF-отчет из HTML-контента.
- Метод `create_docx_report_async`: Создает DOCX-отчет из HTML-контента.
- Функция `main`: Основная функция для запуска генерации отчетов.

Пример использования
----------------------

>>> report_generator = ReportGenerator(if_need_pdf=True, if_need_docx=True)
>>> # await report_generator.create_reports_async(...)
"""

import asyncio
from pathlib import Path
from typing import Optional, Tuple

import pdfkit
import telebot
from jinja2 import Environment, FileSystemLoader

from src import gs
from src.utils.jjson import j_loads
from src.utils.file import save_text_file
from src.utils.convertors.html2pdf import html2pdf
from src.utils.convertors.html2docx import html_to_docx
from src.utils.image import random_image
from src.logger.logger import logger

# config = pdfkit.configuration(wkhtmltopdf=str(gs.path.bin / 'wkhtmltopdf' / 'files' / 'bin' / 'wkhtmltopdf.exe'))

##################################################################

ENDPOINT: str = 'kazarinov'

##################################################################


class ReportGenerator:
    """
    Класс для генерации HTML- и PDF-отчётов на основе данных из JSON.
    """

    if_need_html: bool
    if_need_pdf: bool
    if_need_docx: bool
    storage_path: Path = Path(gs.path.external_storage, ENDPOINT)
    html_path: str | Path
    pdf_path: str | Path
    docs_path: str | Path
    html_content: str
    data: dict
    lang: str
    mexiron_name: str
    env: Environment = Environment(loader=FileSystemLoader('.'))

    def __init__(
        self,
        if_need_pdf: Optional[bool] = True,
        if_need_docx: Optional[bool] = True,
    ) -> None:
        """
        Инициализирует ReportGenerator с указанием форматов отчетов, которые необходимо создать.

        Args:
            if_need_pdf (Optional[bool], optional): Флаг, указывающий, нужно ли генерировать PDF-отчет. Defaults to True.
            if_need_docx (Optional[bool], optional): Флаг, указывающий, нужно ли генерировать DOCX-отчет. Defaults to True.
        """
        self.if_need_pdf = if_need_pdf
        self.if_need_docx = if_need_docx

    async def create_reports_async(
        self,
        bot: telebot.TeleBot,
        chat_id: int,
        data: dict,
        lang: str,
        mexiron_name: str,
    ) -> Tuple[bool, bool, bool]:
        """
        Создает отчеты во всех указанных форматах (HTML, PDF, DOCX).

        Args:
            bot (telebot.TeleBot): Объект TeleBot для отправки отчетов.
            chat_id (int): ID чата для отправки отчетов.
            data (dict): Данные для генерации отчетов.
            lang (str): Язык отчетов.
            mexiron_name (str): Название мехирона.

        Returns:
            Tuple[bool, bool, bool]: Кортеж, содержащий флаги успешного создания HTML, PDF и DOCX отчетов соответственно.
        """
        self.mexiron_name = mexiron_name
        export_path: Path = self.storage_path / 'mexironim' / self.mexiron_name

        self.html_path = export_path / f'{self.mexiron_name}_{lang}.html'
        self.pdf_path = export_path / f'{self.mexiron_name}_{lang}.pdf'
        self.docx_path = export_path / f'{self.mexiron_name}_{lang}.docx'
        self.bot = bot
        self.chat_id = chat_id

        self.html_content = await self.create_html_report_async(data, lang, self.html_path)

        if not self.html_content:
            logger.error('Не удалось создать HTML-отчет.')
            return False, False, False

        pdf_success: bool = True
        docx_success: bool = True

        if self.if_need_pdf:
            pdf_success = await self.create_pdf_report_async(self.html_content, lang, self.pdf_path)

        if self.if_need_docx:
            docx_success = await self.create_docx_report_async(self.html_path, self.docx_path)

        return True, pdf_success, docx_success

    def service_apendix(self, lang: str) -> dict:
        """
        Подготавливает сервисные данные для добавления в отчет.

        Args:
            lang (str): Язык отчета.

        Returns:
            dict: Словарь с сервисными данными.
        """
        return {
            'product_id': '00000',
            'product_name': 'Сервис' if lang == 'ru' else 'שירות',
            'specification': Path(gs.path.endpoints / ENDPOINT / 'report_generator' / 'templates' / f'service_as_product_{lang}.html').read_text(encoding='UTF-8').replace(
                '/n', '<br>'
            ),
            'image_local_saved_path': random_image(self.storage_path / 'converted_images'),
        }

    async def create_html_report_async(self, data: dict, lang: str, html_path: str | Path) -> str | None:
        """
        Генерирует HTML-контент на основе шаблона и данных.

        Args:
            data (dict): Данные для отчета.
            lang (str): Язык отчета.
            html_path (str | Path): Путь для сохранения HTML-файла.

        Returns:
            str | None: HTML-контент или None в случае ошибки.
        """
        self.html_path = html_path if html_path and isinstance(html_path, str) else Path(html_path) or self.html_path

        try:
            service_apendix: dict = self.service_apendix(lang)
            data['products'].append(service_apendix)
            template: str = 'template_table_he.html' if lang == 'he' else 'template_table_ru.html'
            template_path: str = str(gs.path.endpoints / ENDPOINT / 'report_generator' / 'templates' / template)
            # template = self.env.get_template(self.template_path)
            template_string: str = Path(template_path).read_text(encoding='UTF-8')
            template = self.env.from_string(template_string)
            self.html_content: str = template.render(**data)

            try:
                await save_text_file(self.html_path, self.html_content) #Path(self.html_path).write_text(data=self.html_content, encoding='UTF-8')
            except Exception as ex:
                logger.error('Не удалось сохранить HTML файл', ex, exc_info=True)
                return self.html_content

            logger.info(f'Файл HTML удачно сохранен в {html_path}')
            return self.html_content

        except Exception as ex:
            logger.error(f'Не удалось сгенерировать HTML файл {html_path}', ex, exc_info=True)
            return None

    async def create_pdf_report_async(
        self,
        data: str,
        lang: str,
        pdf_path: str | Path,
    ) -> bool:
        """
        Генерирует PDF-отчет из HTML-контента.

        Args:
            data (str): HTML-контент для преобразования в PDF.
            lang (str): Язык отчета.
            pdf_path (str | Path): Путь для сохранения PDF-файла.

        Returns:
            bool: True в случае успешного создания PDF-отчета, False в противном случае.
        """
        pdf_path = pdf_path if pdf_path and isinstance(pdf_path, (str, Path)) else self.pdf_path

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
                    await self.bot.send_document(self.chat_id, f)
                    return True
            except Exception as ex:
                logger.error(f"Не удалось отправить файл {pdf_path} по причине: {ex}", ex, exc_info=True)
                self.bot.send_message(self.chat_id, f'Не удалось отправить файл {pdf_path} по причине: {ex}')
                return False
        return True

    async def create_docx_report_async(self, html_path: str | Path, docx_path: str | Path) -> bool:
        """
        Создает DOCX-файл из HTML-файла.

        Args:
            html_path (str | Path): Путь к HTML-файлу.
            docx_path (str | Path): Путь для сохранения DOCX-файла.

        Returns:
            bool: True в случае успешного создания DOCX-файла, False в противном случае.
        """

        if not html_to_docx(html_path, docx_path):
            logger.error('Не удалось скомпилировать DOCX.')
            return False
        return True


def main(maxiron_name: str, lang: str) -> bool:
    """
    Основная функция для запуска генерации отчетов.

    Args:
        maxiron_name (str): Название мехирона.
        lang (str): Язык отчетов.

    Returns:
        bool: True в случае успешного завершения, False в противном случае.
    """
    external_storage: Path = gs.path.external_storage / ENDPOINT / 'mexironim' / maxiron_name
    data: dict = j_loads(external_storage / f'{maxiron_name}_{lang}.json')
    html_path: Path = external_storage / f'{maxiron_name}_{lang}.html'
    pdf_path: Path = external_storage / f'{maxiron_name}_{lang}.pdf'
    docx_path: Path = external_storage / f'{maxiron_name}_{lang}.docx'
    if_need_html: bool = True
    if_need_pdf: bool = True
    if_need_docx: bool = True
    r = ReportGenerator(if_need_html, if_need_pdf, if_need_docx)

    asyncio.run(
        r.create_reports_async(
            data,
            maxiron_name,
            lang,
            html_path,
            pdf_path,
            docx_path,
        )
    )


if __name__ == '__main__':
    maxiron_name: str = '250127221657987'  # <- debug
    lang: str = 'ru'

    main(maxiron_name, lang)
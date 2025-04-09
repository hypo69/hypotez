### **Анализ кода модуля `report_generator`**

2. **Качество кода**:
   - **Соответствие стандартам**: 6/10
   - **Плюсы**:
     - Код достаточно структурирован и содержит классы и функции для генерации отчетов в различных форматах.
     - Используются аннотации типов.
     - Присутствует логирование ошибок.
   - **Минусы**:
     - Не все функции и классы имеют подробное описание в docstring.
     - Есть участки кода с `...`, что указывает на незавершенность реализации.
     - Не используется модуль `logger` для логирования во всех блоках `except`.
     - Не все переменные аннотированы типами.
     - Смешанный стиль кавычек (используются и одинарные, и двойные).
     - В некоторых местах не соблюдены пробелы вокруг оператора присваивания.
     - Использование `Union` вместо `|`.
     - Есть ошибки в наименовании переменных (например, `maxiron_name` вместо `mexiron_name`).

3. **Рекомендации по улучшению**:
   - Добавить полные и подробные docstring для всех классов, методов и функций, используя русский язык и формат UTF-8.
   - Заменить `Union` на `|` в аннотациях типов.
   - Использовать `logger.error` с передачей исключения `ex` в качестве аргумента и `exc_info=True` во всех блоках `except`.
   - Проверить и исправить опечатки в коде (например, `maxiron_name` должно быть `mexiron_name`).
   - Привести код к единому стилю кавычек (использовать только одинарные кавычки).
   - Добавить пробелы вокруг оператора присваивания.
   - Завершить реализацию участков кода, где используется `...`.
   - Изменить способ передачи путей к файлам, использовать pathlib
   - Убрать магические значения
   - Для каждой переменной необходимо добавить аннотацию типа.
   - Избавиться от дублирования кода.
   - Упростить логику там где это возможно

4. **Оптимизированный код**:

```python
                ## \file /src/endpoints/kazarinov/react/report_generator.py
# -*- coding: utf-8 -*-\n\n

"""
Модуль для генерации HTML и PDF отчетов для мехиронов Казаринова.
==================================================================

Модуль содержит класс :class:`ReportGenerator`, который используется для генерации отчетов на основе данных из JSON
в форматах HTML, PDF и DOCX.

Описание работы:
----------------
- Конструктор `__init__`: Определяет, какие форматы отчетов требуется сгенерировать.
- Метод `create_reports_async`: Асинхронно создает отчеты во всех требуемых форматах (HTML, PDF, DOCX).
- Метод `service_apendix`: Создает сервисный блок для добавления в отчет.
- Метод `create_html_report_async`: Генерирует HTML-контент на основе шаблона и данных.
- Метод `create_pdf_report_async`: Генерирует PDF-отчет из HTML-контента.
- Метод `create_docx_report_async`: Генерирует DOCX-отчет из HTML-контента.
- Функция `main`: Запускает процесс генерации отчетов.

Пример использования:
--------------------
>>> report_generator = ReportGenerator(if_need_pdf=True, if_need_docx=True)
>>> asyncio.run(report_generator.create_reports_async(bot, chat_id, data, lang, mexiron_name))
"""

import asyncio
from pathlib import Path
from typing import Optional
import telebot
from jinja2 import Environment, FileSystemLoader

from src import gs
from src.utils.jjson import j_loads
from src.utils.file import save_text_file
from src.utils.convertors.html2pdf import html2pdf
from src.utils.convertors.html2docx import html_to_docx
from src.utils.image import random_image
from src.logger.logger import logger

ENDPOINT: str = 'kazarinov'
TEMPLATE_RU: str = 'template_table_ru.html'
TEMPLATE_HE: str = 'template_table_he.html'
SERVICE_AS_PRODUCT_RU: str = 'service_as_product_ru.html'
SERVICE_AS_PRODUCT_HE: str = 'service_as_product_he.html'
CONVERTED_IMAGES: str = 'converted_images'
MEXIRONIM: str = 'mexironim'

class ReportGenerator:
    """
    Класс для генерации HTML- и PDF-отчётов на основе данных из JSON.
    """
    if_need_html: bool
    if_need_pdf: bool
    if_need_docx: bool
    storage_path: Path
    html_path: Path | str
    pdf_path: Path | str
    docs_path: Path | str
    html_content: str
    data: dict
    lang: str
    mexiron_name: str
    bot: Optional[telebot.TeleBot]
    chat_id: Optional[int]
    env: Environment

    def __init__(self,
                 if_need_pdf: Optional[bool] = True,
                 if_need_docx: Optional[bool] = True,
                 ):
        """
        Определение, какие форматы данных требуется вернуть.

        Args:
            if_need_pdf (Optional[bool], optional): Флаг необходимости генерации PDF-отчета. Defaults to True.
            if_need_docx (Optional[bool], optional): Флаг необходимости генерации DOCX-отчета. Defaults to True.
        """
        self.if_need_pdf = if_need_pdf
        self.if_need_docx = if_need_docx
        self.storage_path = Path(gs.path.external_storage, ENDPOINT)
        self.env = Environment(loader=FileSystemLoader('.'))
        self.bot = None
        self.chat_id = None

    async def create_reports_async(self,
                                 bot: telebot.TeleBot,
                                 chat_id: int,
                                 data: dict,
                                 lang: str,
                                 mexiron_name: str,
                                 ) -> tuple[bool, bool, bool]:
        """
        Асинхронно создает отчеты во всех требуемых форматах (HTML, PDF, DOCX).

        Args:
            bot (telebot.TeleBot): Telebot instance.
            chat_id (int): Chat ID for sending messages.
            data (dict): Данные для отчета.
            lang (str): Язык отчета ('ru' или 'he').
            mexiron_name (str): Имя мехирона.

        Returns:
            tuple[bool, bool, bool]: Кортеж, содержащий результаты создания HTML, PDF и DOCX отчетов.
        """
        self.mexiron_name = mexiron_name
        self.lang = lang
        self.bot = bot
        self.chat_id = chat_id
        export_path: Path = self.storage_path / MEXIRONIM / self.mexiron_name

        self.html_path = export_path / f'{self.mexiron_name}_{self.lang}.html'
        self.pdf_path = export_path / f'{self.mexiron_name}_{self.lang}.pdf'
        self.docx_path = export_path / f'{self.mexiron_name}_{self.lang}.docx'

        html_created: bool = await self.create_html_report_async(data, self.lang, self.html_path)

        if not html_created:
            logger.error('Не удалось создать HTML отчет')
            return False, False, False

        pdf_created: bool = False
        docx_created: bool = False

        if self.if_need_pdf:
            pdf_created = await self.create_pdf_report_async(self.html_content, self.lang, self.pdf_path)

        if self.if_need_docx:
            docx_created = await self.create_docx_report_async(self.html_path, self.docx_path)

        return html_created, pdf_created, docx_created

    def service_apendix(self, lang: str) -> dict:
        """
        Создает сервисный блок для добавления в отчет.

        Args:
            lang (str): Язык отчета ('ru' или 'he').

        Returns:
            dict: Словарь с данными сервисного блока.
        """
        template_file: str = SERVICE_AS_PRODUCT_RU if lang == 'ru' else SERVICE_AS_PRODUCT_HE
        specification_path: Path = Path(
            gs.path.endpoints, ENDPOINT, 'report_generator', 'templates', template_file
        )
        specification: str = specification_path.read_text(encoding='UTF-8').replace('\n', '<br>')
        image_local_saved_path: Path = random_image(self.storage_path / CONVERTED_IMAGES)

        return {
            'product_id': '00000',
            'product_name': 'Сервис' if lang == 'ru' else 'שירות',
            'specification': specification,
            'image_local_saved_path': image_local_saved_path
        }

    async def create_html_report_async(self, data: dict, lang: str, html_path: str | Path) -> bool:
        """
        Генерирует HTML-контент на основе шаблона и данных.

        Args:
            data (dict): Данные для отчета.
            lang (str): Язык отчета ('ru' или 'he').
            html_path (str | Path): Путь для сохранения HTML-файла.

        Returns:
            bool: True, если HTML-контент успешно сгенерирован и сохранен, иначе False.
        """
        self.html_path = Path(html_path) if isinstance(html_path, str) else html_path or self.html_path

        try:
            service_apendix: dict = self.service_apendix(lang)
            if 'products' in data and isinstance(data['products'], list):
                data['products'].append(service_apendix)
            else:
                data['products'] = [service_apendix]

            template_file: str = TEMPLATE_RU if lang == 'ru' else TEMPLATE_HE
            template_path: Path = Path(gs.path.endpoints, ENDPOINT, 'report_generator', 'templates', template_file)
            template_string: str = template_path.read_text(encoding='UTF-8')
            template = self.env.from_string(template_string)
            self.html_content: str = template.render(**data)

            try:
                await save_text_file(self.html_path, self.html_content, encoding='UTF-8')
                logger.info(f'Файл HTML удачно сохранен в {self.html_path}')
                return True
            except Exception as ex:
                logger.error(f'Не удалось сохранить HTML файл {self.html_path}', ex, exc_info=True)
                return False

        except Exception as ex:
            logger.error(f'Не удалось сгенерировать HTML файл {self.html_path}', ex, exc_info=True)
            return False

    async def create_pdf_report_async(self, data: str, lang: str, pdf_path: str | Path) -> bool:
        """
        Генерирует PDF-отчет из HTML-контента.

        Args:
            data (str): HTML-контент для преобразования в PDF.
            lang (str): Язык отчета ('ru' или 'he').
            pdf_path (str | Path): Путь для сохранения PDF-файла.

        Returns:
            bool: True, если PDF-отчет успешно сгенерирован и сохранен, иначе False.
        """
        pdf_path = Path(pdf_path) if isinstance(pdf_path, str) else pdf_path or self.pdf_path
        self.html_content = data or self.html_content

        from src.utils.pdf import PDFUtils
        pdf = PDFUtils()

        if not pdf.save_pdf_pdfkit(self.html_content, pdf_path):
            logger.error(f'Не удалось сохранить PDF файл {pdf_path}')
            if self.bot:
                await self.bot.send_message(self.chat_id, f'Не удалось сохранить файл {pdf_path}')
            return False

        if self.bot:
            try:
                with open(pdf_path, 'rb') as f:
                    await self.bot.send_document(self.chat_id, f)
                    return True
            except Exception as ex:
                logger.error(f'Не удалось отправить PDF файл {pdf_path} в чат {self.chat_id}', ex, exc_info=True)
                await self.bot.send_message(self.chat_id, f'Не удалось отправить файл {pdf_path} по причине: {ex}')
                return False
        return True

    async def create_docx_report_async(self, html_path: str | Path, docx_path: str | Path) -> bool:
        """
        Создает DOCX-файл из HTML-файла.

        Args:
            html_path (str | Path): Путь к HTML-файлу.
            docx_path (str | Path): Путь для сохранения DOCX-файла.

        Returns:
            bool: True, если DOCX-файл успешно создан, иначе False.
        """
        html_path = Path(html_path) if isinstance(html_path, str) else html_path or self.html_path
        docx_path = Path(docx_path) if isinstance(docx_path, str) else docx_path or self.docx_path

        if not html_to_docx(html_path, docx_path):
            logger.error(f'Не удалось скомпилировать DOCX файл из {html_path} в {docx_path}')
            return False
        logger.info(f'DOCX файл успешно создан из {html_path} в {docx_path}')
        return True

def main(mexiron_name: str, lang: str) -> bool:
    """
    Основная функция для запуска процесса генерации отчетов.

    Args:
        mexiron_name (str): Имя мехирона.
        lang (str): Язык отчета ('ru' или 'he').

    Returns:
        bool: True, если процесс завершен успешно, иначе False.
    """
    external_storage: Path = gs.path.external_storage / ENDPOINT / MEXIRONIM / mexiron_name
    data: dict = j_loads(external_storage / f'{mexiron_name}_{lang}.json')
    if not data:
        logger.error(f'Не удалось загрузить JSON файл для {mexiron_name} на языке {lang}')
        return False

    if_need_html: bool = True
    if_need_pdf: bool = True
    if_need_docx: bool = True

    report_generator: ReportGenerator = ReportGenerator(if_need_pdf, if_need_docx)
    async def run_reports():
        nonlocal report_generator
        await report_generator.create_reports_async(None, None, data, lang, mexiron_name)

    asyncio.run(run_reports())
    return True

if __name__ == '__main__':
    mexiron_name: str = '250127221657987'  # <- debug
    lang: str = 'ru'

    main(mexiron_name, lang)
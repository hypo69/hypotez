### **Анализ кода модуля `src.utils.pdf`**

2. **Качество кода**:
   - **Соответствие стандартам**: 7/10
   - **Плюсы**:
     - Модуль предоставляет функциональность для преобразования HTML в PDF с использованием различных библиотек.
     - Используется логирование для отслеживания ошибок и успешных операций.
     - Присутствуют docstring для большинства функций, что облегчает понимание их назначения и использования.
   - **Минусы**:
     - Местами отсутствует обработка исключений, что может приводить к непредсказуемому поведению программы.
     - Некоторые комментарии и сообщения об ошибках на английском языке.
     - Не везде используются аннотации типов.
     - Используются неконсистентные кавычки (и одинарные, и двойные).

3. **Рекомендации по улучшению**:
   - Дополнить docstring для всех функций и методов, включая описание параметров, возвращаемых значений и возможных исключений.
   - Перевести все комментарии и сообщения об ошибках на русский язык.
   - Унифицировать стиль кавычек, используя только одинарные кавычки.
   - Добавить аннотации типов для переменных и параметров функций.
   - Явное указание кодировки при открытии файлов.
   - Улучшить обработку исключений, чтобы предотвратить неожиданное завершение программы.
   - В методе `dict2pdf` исправить сравнение типа данных, убрать магические числа и добавить docstring в соответствии со стандартом.
   - Использовать `logger.error` с передачей исключения в качестве второго аргумента и `exc_info=True` для более подробной информации об ошибке.

4. **Оптимизированный код**:

```python
## \file /src/utils/pdf.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для преобразования HTML-контента или файлов в PDF
========================================================

Модуль предоставляет инструменты для преобразования HTML-контента или файлов в PDF с использованием различных библиотек.
Включает поддержку `pdfkit`, `FPDF`, `WeasyPrint` и `xhtml2pdf`.

Дополнительная информация:
- https://chatgpt.com/share/672266a3-0048-800d-a97b-c38f647d496b
- https://stackoverflow.com/questions/73599970/how-to-solve-wkhtmltopdf-reported-an-error-exit-with-code-1-due-to-network-err
- https://habr.com/ru/companies/bothub/articles/853490/

 .. module:: src.utils.pdf
"""

import os
import json
from pathlib import Path
from typing import Any

import pdfkit
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from src.logger.logger import logger
from src.utils.printer import pprint

class PDFUtils:
    """
    Класс для работы с PDF-файлами.
    Предоставляет методы для сохранения HTML-контента в PDF с использованием различных библиотек.
    """

    @staticmethod
    def save_pdf_pdfkit(data: str | Path, pdf_file: str | Path) -> bool:
        """
        Сохраняет HTML-контент или файл в PDF с использованием библиотеки `pdfkit`.

        Args:
            data (str | Path): HTML-контент или путь к HTML-файлу.
            pdf_file (str | Path): Путь к сохраняемому PDF-файлу.

        Returns:
            bool: `True`, если PDF успешно сохранен, иначе `False`.

        Raises:
            FileNotFoundError: Если не найден исполняемый файл `wkhtmltopdf.exe`.
            pdfkit.PDFKitError: При ошибке генерации PDF через `pdfkit`.
            OSError: При ошибке доступа к файлу.
        """
        wkhtmltopdf_exe: Path = Path(__root__) / 'bin' / 'wkhtmltopdf' / 'files' / 'bin' /  'wkhtmltopdf.exe'

        if not wkhtmltopdf_exe.exists():
            msg = f'Не найден wkhtmltopdf.exe по указанному пути: {wkhtmltopdf_exe}'
            logger.error(msg)
            raise FileNotFoundError(msg)

        try:
            configuration = pdfkit.configuration(wkhtmltopdf=str(wkhtmltopdf_exe))
            options = {'enable-local-file-access': ''}

            if isinstance(data, str):
                # Преобразование HTML-контента в PDF
                pdfkit.from_string(data, str(pdf_file), configuration=configuration, options=options)
            else:
                # Преобразование HTML-файла в PDF
                pdfkit.from_file(str(data), str(pdf_file), configuration=configuration, options=options)

            logger.info(f'PDF успешно сохранен: {pdf_file}')
            return True
        except (pdfkit.PDFKitError, OSError) as ex:
            logger.error('Ошибка генерации PDF через pdfkit', ex, exc_info=True)
            return False
        except Exception as ex:
            logger.error('Неожиданная ошибка при генерации PDF через pdfkit', ex, exc_info=True)
            return False

    @staticmethod
    def save_pdf_fpdf(data: str, pdf_file: str | Path) -> bool:
        """
        Сохраняет текст в PDF с использованием библиотеки FPDF.

        Args:
            data (str): Текст, который необходимо сохранить в PDF.
            pdf_file (str | Path): Путь к сохраняемому PDF-файлу.

        Returns:
            bool: `True`, если PDF успешно сохранен, иначе `False`.

        Raises:
            FileNotFoundError: Если не найден файл шрифтов `fonts.json` или файлы шрифтов.
            Exception: При любой другой ошибке.
        """
        try:
            from fpdf import FPDF

            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)

            # Путь к файлу fonts.json
            fonts_file_path: Path = Path(__root__) / 'assets' / 'fonts' / 'fonts.json'

            if not fonts_file_path.exists():
                msg = (
                    f'JSON файл установки шрифтов не найден: {fonts_file_path}\n'
                    'Формат файла `fonts.json`:\n'
                    '{\n'
                    '    "dejavu-sans.book": {\n'
                    '        "family": "DejaVuSans",\n'
                    '        "path": "dejavu-sans.book.ttf",\n'
                    '        "style": "book",\n'
                    '        "uni": true\n'
                    '    }\n'
                    '}'
                )
                logger.error(msg)
                raise FileNotFoundError(msg)

            with open(fonts_file_path, 'r', encoding='utf-8') as json_file:
                fonts = json.load(json_file)

            # Добавление шрифтов
            for font_name, font_info in fonts.items():
                font_path: Path = Path(__root__) / 'assets' / 'fonts' / font_info['path']
                if not font_path.exists():
                    msg = f'Файл шрифта не найден: {font_path}'
                    logger.error(msg)
                    raise FileNotFoundError(msg)

                pdf.add_font(font_info['family'], font_info['style'], str(font_path), uni=font_info['uni'])

            # Установка шрифта по умолчанию
            pdf.set_font('DejaVuSans', style='book', size=12)
            pdf.multi_cell(0, 10, data)
            pdf.output(str(pdf_file))

            logger.info(f'PDF отчет успешно сохранен: {pdf_file}')
            return True
        except Exception as ex:
            logger.error('Ошибка при сохранении PDF через FPDF: ', ex, exc_info=True)
            return False


    @staticmethod
    def save_pdf_weasyprint(data: str | Path, pdf_file: str | Path) -> bool:
        """
        Сохраняет HTML-контент или файл в PDF с использованием библиотеки `WeasyPrint`.

        Args:
            data (str | Path): HTML-контент или путь к HTML-файлу.
            pdf_file (str | Path): Путь к сохраняемому PDF-файлу.

        Returns:
            bool: `True`, если PDF успешно сохранен, иначе `False`.

        Raises:
            Exception: При ошибке сохранения PDF через `WeasyPrint`.
        """
        try:
            from weasyprint import HTML

            if isinstance(data, str):
                HTML(string=data).write_pdf(pdf_file)
            else:
                HTML(filename=str(data)).write_pdf(pdf_file)

            logger.info(f'PDF успешно сохранен: {pdf_file}')
            return True
        except Exception as ex:
            logger.error('Ошибка при сохранении PDF через WeasyPrint: ', ex, exc_info=True)
            return False

    @staticmethod
    def save_pdf_xhtml2pdf(data: str | Path, pdf_file: str | Path) -> bool:
        """
        Сохраняет HTML-контент или файл в PDF с использованием библиотеки `xhtml2pdf`.

        Args:
            data (str | Path): HTML-контент или путь к HTML-файлу.
            pdf_file (str | Path): Путь к сохраняемому PDF-файлу.

        Returns:
            bool: `True`, если PDF успешно сохранен, иначе `False`.

        Raises:
            Exception: При ошибке сохранения PDF через `xhtml2pdf`.
        """
        try:
            from xhtml2pdf import pisa

            with open(pdf_file, 'w+b') as result_file:
                if isinstance(data, str):
                    # Убедимся, что строка имеет кодировку UTF-8
                    data_utf8 = data.encode('utf-8').decode('utf-8')  # Преобразуем строку обратно в UTF-8, если нужно
                    try:
                        pisa.CreatePDF(data_utf8, dest=result_file)
                    except Exception as ex:
                        logger.error('Ошибка компиляции PDF: ', ex, exc_info=True)
                        return False
                else:
                    with open(str(data), 'r', encoding='utf-8') as source_file:
                        try:
                            # Прочитаем файл в кодировке UTF-8
                            source_data = source_file.read()
                            pisa.CreatePDF(source_data, dest=result_file, encoding='UTF-8')
                        except Exception as ex:
                            logger.error('Ошибка компиляции PDF: ', ex, exc_info=True)
                            return False

            logger.info(f'PDF успешно сохранен: {pdf_file}')
            return True
        except Exception as ex:
            logger.error('Ошибка при сохранении PDF через xhtml2pdf: ', ex, exc_info=True)
            return False

    @staticmethod
    def html2pdf(html_str: str, pdf_file: str | Path) -> bool | None:
        """Converts HTML content to a PDF file using WeasyPrint."""
        try:
            from weasyprint import HTML
            HTML(string=html_str).write_pdf(pdf_file)
            return True
        except Exception as e:
            print(f"Error during PDF generation: {e}")
            return

    @staticmethod
    def pdf_to_html(pdf_file: str | Path, html_file: str | Path) -> bool:
        """
        Конвертирует PDF-файл в HTML-файл.

        Args:
            pdf_file (str | Path): Путь к исходному PDF-файлу.
            html_file (str | Path): Путь к сохраняемому HTML-файлу.

        Returns:
            bool: `True`, если конвертация прошла успешно, иначе `False`.

        Raises:
            Exception: При ошибке конвертации PDF в HTML.
        """
        try:
            # Извлечение текста из PDF
            from pdfminer.high_level import extract_text

            text = extract_text(str(pdf_file))

            # Создание HTML-файла
            with open(html_file, 'w', encoding='utf-8') as file:
                file.write(f'<html><body>{text}</body></html>')

            print(f'HTML успешно сохранен: {html_file}')
            return True
        except Exception as ex:
            print(f'Ошибка при конвертации PDF в HTML: {ex}')
            return False

    @staticmethod
    def dict2pdf(data: Any, file_path: str | Path) -> None:
        """
        Сохраняет данные словаря в PDF-файл.

        Args:
            data (dict): Словарь для сохранения в PDF.
            file_path (str | Path): Путь к выходному PDF-файлу.

        Raises:
            TypeError: Если входные данные не являются словарем.
        """
        if not isinstance(data, dict):
            raise TypeError('Входные данные должны быть словарем.')

        pdf = canvas.Canvas(str(file_path), pagesize=A4)
        width, height = A4
        x, y = 50, height - 50

        pdf.setFont('Helvetica', 12)

        line_height = 20  # Высота строки

        for key, value in data.items():
            line = f'{key}: {value}'
            pdf.drawString(x, y, line)
            y -= line_height

            if y < 50:  # Создать новую страницу, если места недостаточно
                pdf.showPage()
                pdf.setFont('Helvetica', 12)
                y = height - 50

        pdf.save()
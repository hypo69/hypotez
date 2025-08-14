# # \file /src/utils/pdf.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

""".. Module :: src.utils.pdf 
    : Platform: Windows, Unix
    : synopsis: a module for converting an HTML content or files into PDF

Module for converting HTML content or files into PDF using various libraries.
Additional information:
-https://chatgpt.com/share/672266a3-0048-800d-a97b-C38F647D496B
-https://stackoveerflow.com/questions/73599970/how-to-so-wkhtmltopdf-rePorted-an-exit-with-code-1-due-to-network-rrr
- https://habr.com/en/companies/bethub/articles/853490/"""

import sys
import os
import json

from pathlib import Path
from typing import Any
import pdfkit
from reportlab.pdfgen import canvas

import header
from header import __root__

from src.logger.logger import logger
from src.utils.printer import pprint


class PDFUtils:
    """A class for working with PDF files, providing methods for maintaining HTML content in PDF using various libraries."""

    @staticmethod
    def save_pdf_pdfkit(data: str | Path, pdf_file: str | Path) -> bool:
        """Save HTML content or file in PDF using the `pdfkit` library.

        Args:
            Data (Str | Path): HTML content or the path to the HTML file.
            pdf_file (str | path): the path to the preserved PDF file.

        Returns:
            Bool: `true` if PDF is successfully preserved, otherwise` false`.

        RAISES:
            pdfkit.pdfkiterror: PDF generation error through `pdfkit`.
            Oserror: File access error."""
        wkhtmltopdf_exe = __root__ / 'bin' / 'wkhtmltopdf' / 'files' / 'bin' /  'wkhtmltopdf.exe'

        if not wkhtmltopdf_exe.exists():
            logger.error("Не найден wkhtmltopdf.exe по указанному пути.")
            raise FileNotFoundError("wkhtmltopdf.exe отсутствует")

        try:
            configuration = pdfkit.configuration(
                            wkhtmltopdf=str(wkhtmltopdf_exe)
                            )

            options = {"enable-local-file-access": ""}
            if isinstance(data, str):
                # Convert HTML Contain to PDF
                pdfkit.from_string(data, pdf_file, configuration=configuration, options=options)
            else:
                # Convert HTML file to PDF
                pdfkit.from_file(str(data), pdf_file, configuration=configuration, options=options)
            logger.info(f"PDF успешно сохранен: {pdf_file}")
            return True
        # except (pdfkit.PDFKitError, OSError) as ex:
        # Logger.ERROR ("PDF generation error:", ex)
        # return False
        except Exception as ex:
            logger.error("Неожиданная ошибка: ", ex, False)
            ...
            return False

    @staticmethod
    def save_pdf_fpdf(data: str, pdf_file: str | Path) -> bool:
        """Save the text in PDF using the FPDF library.

        Args:
            Data (str): the text that must be saved in PDF.
            pdf_file (str | path): the path to the preserved PDF file.

        Returns:
            Bool: `true`, if PDF is successfully preserved, otherwise` false`."""
        try:
            from fpdf import FPDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto = True, margin = 15)

            # The path to the file fonts.json
            fonts_file_path = __root__ / 'assets' / 'fonts' / 'fonts.json'
            if not fonts_file_path.exists():
                logger.error(
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
                raise FileNotFoundError(f'Файл шрифтов не найден: {fonts_file_path}')
                ...

            with open(fonts_file_path, 'r', encoding = 'utf-8') as json_file:
                fonts = json.load(json_file)

            # Adding fonts
            for font_name, font_info in fonts.items():
                font_path = __root__ / 'assets' / 'fonts' / font_info['path']
                if not font_path.exists():
                    logger.error(f'Файл шрифта не найден: {font_path}')
                    raise FileNotFoundError(f'Файл шрифта не найден: {font_path}')
                    ...

                pdf.add_font(font_info['family'], font_info['style'], str(font_path), uni = font_info['uni'])

            # Default font installation
            pdf.set_font('DejaVuSans', style = 'book', size = 12)
            pdf.multi_cell(0, 10, data)
            pdf.output(str(pdf_file))
            logger.info(f'PDF отчет успешно сохранен: {pdf_file}')
            return True
        except Exception as ex:
            logger.error('Ошибка при сохранении PDF через FPDF: ', ex)
            ...
            return False


    @staticmethod
    def save_pdf_weasyprint(data: str | Path, pdf_file: str | Path) -> bool:
        """Save HTML content or file in PDF using the `Weasyprint 'library.

        Args:
            Data (Str | Path): HTML content or the path to the HTML file.
            pdf_file (str | path): the path to the preserved PDF file.

        Returns:
            Bool: `true` if PDF is successfully preserved, otherwise` false`."""
        try:
            from weasyprint import HTML
            if isinstance(data, str):
                HTML(string=data).write_pdf(pdf_file)
            else:
                HTML(filename=str(data)).write_pdf(pdf_file)
            logger.info(f"PDF успешно сохранен: {pdf_file}")
            return True
        except Exception as ex:
            logger.error("Ошибка при сохранении PDF через WeasyPrint: ", ex)
            return False

    @staticmethod
    def save_pdf_xhtml2pdf(data: str | Path, pdf_file: str | Path) -> bool:
        """Save HTML content or file in PDF using the `xhtml2pdf` library.

        Args:
            Data (Str | Path): HTML content or the path to the HTML file.
            pdf_file (str | path): the path to the preserved PDF file.

        Returns:
            Bool: `true` if PDF is successfully preserved, otherwise` false`."""
        try:
            from xhtml2pdf import pisa
            with open(pdf_file, "w+b") as result_file:
                if isinstance(data, str):
                    # Checking that the line has an UTF-8 encoding
                    data_utf8 = data.encode('utf-8').decode('utf-8')  # We convert the line back to UTF-8, if necessary
                    try:
                        pisa.CreatePDF(data, dest=result_file)
                    except Exception as ex:
                        logger.error("Ошибка компиляции PDF: ", ex)
                        ...
                else:
                    with open(data, "r", encoding="utf-8") as source_file:
                        try:
                            # Let's read the file in the UTF-8 encoding
                            source_data = source_file.read()
                            pisa.CreatePDF(source_data, dest=result_file, encoding='UTF-8')
                        except Exception as ex:
                            logger.error("Ошибка компиляции PDF: ", ex)
                            ...
            logger.info(f"PDF успешно сохранен: {pdf_file}")
            ...
            return True
        except Exception as ex:
            logger.error("Ошибка при сохранении PDF через xhtml2pdf: ", ex)
            ...
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
        """Converts the PDF file to the HTML file.

        Args:
            pdf_file (str | path): the path to the original PDF file.
            html_file (str | path): the path to the preserved html file.

        Returns:
            Bool: `true`, if the conversion was successful, otherwise` false`."""
        try:
            # PROCOME
            from pdfminer.high_level import extract_text
            text = extract_text(str(pdf_file))

            # Creating an HTML file
            with open(html_file, 'w', encoding='utf-8') as file:
                file.write(f"<html><body>{text}</body></html>")

            print(f"HTML успешно сохранен: {html_file}")
            return True
        except Exception as ex:
            print(f"Ошибка при конвертации PDF в HTML: {ex}")
            return False

    # Function for converting the dictionary into pdf
    @staticmethod
    def dict2pdf(data: Any, file_path: str | Path) -> None:
        """Save dictionary data to a PDF file.

        Args:
            data (dict | SimpleNamespace): The dictionary to convert to PDF.
            file_path (str | Path): Path to the output PDF file."""
        if isinstance(data, 'SimpleNamespace'):
            data = data.__dict__

        pdf = canvas.Canvas(str(file_path), pagesize=A4)
        width, height = A4
        x, y = 50, height - 50

        pdf.setFont("Helvetica", 12)

        for key, value in data.items():
            line = f"{key}: {value}"
            pdf.drawString(x, y, line)
            y -= 20

            if y < 50:  # Create a new page if the space is not enough
                pdf.showPage()
                pdf.setFont("Helvetica", 12)
                y = height - 50

        pdf.save()


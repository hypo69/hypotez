# # \file /src/endpoints/kazarinov/react/pricelist_generator.py
# -*- coding: utf-8 -*-

# ! .pyenv/bin/python3

""".. Module :: src.endpoints.kazarinov.react 
	: Platform: Windows, Unix
	: synopsis: HTML and PDF generator for Kazarinov Mehrons

Work description:
- The designer `__init__`: takes a template, basic path, a mark of time and tongue.
- Method `Load_Data`: downloads data from a json file.
- Method `Generate_html`: generates html using Jinja2.
- Method `save_html`: saves html in a file.
- The method `generate_pdf`: converts html into pdf.
- Method `Create_Report`: launches a full cycle of reporting."""


# https://dev.to/kboskin/building-web-applications-with-react-and-python-2d8c


import header
import asyncio
from dataclasses import dataclass, field
from src import gs
import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import pdfkit
from src.utils.jjson import j_loads
from src.utils.file import read_text_file, save_text_file    
from src.utils.pdf import PDFUtils
from src.utils.convertors.html import html2pdf
from src.utils.image import random_image
from src.utils.printer import pprint
from src.logger.logger import logger

# config = pdfkit.configuration(wkhtmltopdf= str( gs.path.bin / 'wkhtmltopdf' / 'files' / 'bin' / 'wkhtmltopdf.exe' ) )


@dataclass
class ReportGenerator:
    """Class for generating HTML and PDF reports based on data from JSON."""

    env: Environment = field(default_factory=lambda: Environment(loader=FileSystemLoader('.')))

    async def generate_html(self, data:dict, lang:str ) -> str:
        """Generate HTML Content on the main template and data.

        Args:
            Lang (STR): Language Report.

        Returns:
            STR: HTML-Content."""
        template:str = 'template_table_he.html' if lang == 'he' else  'template_table_ru.html'
        template_path: str  =  str(gs.path.endpoints / 'kazarinov' / 'pricelist_generator' / 'templates' / template)
        # template = self.env.get_template(self.template_path)
        template_string = Path(template_path).read_text(encoding = 'UTF-8')
        template = self.env.from_string(template_string)
        return template.render(**data)


    async def create_report(self, data: dict, lang:str, html_file:str| Path, pdf_file:str |Path) -> bool:
        """A full cycle of reporting.

        Args:
            Lang (str): report language."""

        # Service:
        service_dict:dict = {
                            "product_title":"Сервис" if lang == 'ru' else "שירות",
                            "specification":Path(gs.path.endpoints / 'kazarinov' / 'pricelist_generator' / 'templates' / f'service_as_product_{lang}.html').read_text(encoding='UTF-8').replace('/n','<br>'),
                            "image_local_saved_path":random_image(gs.path.external_storage / 'kazarinov' / 'converted_images' )
                            }
        data['products'].append(service_dict)

        html_content = await self.generate_html(data,lang)
        Path(html_file).write_text(data = html_content, encoding='UTF-8')
        pdf = PDFUtils()

        if not pdf.save_pdf_pdfkit(html_content,pdf_file):
            logger.error(f"Не скопмилировался PDF")
            ...
            return False
        return True

def main(mexiron:str,lang:str) ->bool:
    base_path:Path =  gs.path.external_storage / 'kazarinov' / 'mexironim' / mexiron
    data:dict = j_loads(base_path / f'{lang}.json')
    html_file:Path =  base_path / f'{mexiron}_{lang}.html' 
    pdf_file:Path = base_path / f'{mexiron}_{lang}.pdf'
    r = ReportGenerator()
    asyncio.run( r.create_report(data, lang, html_file, pdf_file)   )

if __name__ == "__main__":
    mexiron:str = '24_12_01_03_18_24_269'
    lang:str = 'ru'
    main(mexiron,lang)


# # \file /src/endpoints/kazarinov/react/report_generator.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

"""HTML and PDF generator for Kazarinov Mehrons

Work description:
- The designer `__init__`: takes a template, basic path, a mark of time and tongue.
- Method `Load_Data`: downloads data from a json file.
- Method `Generate_html`: generates html using Jinja2.
- Method `save_html`: saves html in a file.
- The method `generate_pdf`: converts html into pdf.
- Method `Create_Report`: launches a full cycle of reporting.

rst```
.. Module :: src.endpoints.kazarinov.react.report_generator
    : Platform: Windows, Unix
    : synopsis: HTML and PDF generator for Kazarinov Mehrons
`` `"""


# https://dev.to/kboskin/building-web-applications-with-react-and-python-2d8c



import asyncio
from dataclasses import dataclass, field
import telebot
from typing import Optional
import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
# Import PDFKIT # is not used directly, PDF.Save_PDF_PDFKIT is used

import header
from header import __root__
from src import gs
from src.utils.jjson import j_loads
from src.utils.file import read_text_file, save_text_file    
from src.utils.convertors.html import html2pdf
# from src.utils.convertors.html import html_to_docx # is used only in Create_Docx_report_async, but a call is made
from src.utils.image import random_image
from src.utils.printer import pprint
from src.logger.logger import logger

@dataclass
class Config:
    ENDPOINT = 'kazarinov'


@dataclass(slots=True, kw_only=True)
class ReportGenerator:
    """Class for generating HTML and PDF reports based on data from JSON.
    (Version on DACLASSI)"""
    # --- fields determined when creating an object (arguments for __init__) ---
    generate_html: bool = True
    generate_pdf: bool = True
    generate_docx: bool = False

    # --- Fields with default values that are not the arguments of __init__ ---
    
    # storage_path: Path = field(
    # init = false,
    # default=Path(gs.path.external_storage, Config.ENDPOINT)
    # None
    
    # # IMPORTANT: For changed objects (like environment) you need to use
    # # Default_Factory, so that each copy of the class has its own unique object.
    # env: Environment = field(
    # init = false,
    # default_factory=lambda: Environment(loader=FileSystemLoader('.'))
    # None

    # --- fields that will be filled later (not in __init__) ---
    # They are assigned the default values so that their initial state is clear.
    data: dict | None = field(init=False, default=None)
    html_content: str | None = field(init=False, default=None)
    lang: str | None = field(init=False, default=None)
    mexiron_name: str | None = field(init=False, default=None)
    
    html_path: Path | str | None = field(init=False, default=None)
    pdf_path: Path | str | None = field(init=False, default=None)
    docs_path: Path | str | None = field(init=False, default=None)
    storage_path: Path | str | None = field(init=False, default=None)
        

    def service_apendix(self, lang:str) -> dict:
        """Footer"""
        return  {
                "product_id":"00000",
                "product_name":"Сервис" if lang == 'ru' else "שירות",
                "specification":Path(__root__ / 'src' / 'endpoints' / Config.ENDPOINT / 'report_generator' / 'templates' / f'service_as_product_{lang}.html').read_text(encoding='UTF-8').replace('/n','<br>'),
                "image_local_saved_path":random_image(self.storage_path / 'converted_images' )
                }

        ...

    async def create_html_report_async(self, data:dict, lang:str, html_path:Optional[ str|Path] ) -> str:
        """Generate HTML Content on the main template and data.

        Args:
            Lang (STR): Language Report.

        Returns:
            STR: HTML-Content."""
        self.html_path = html_path if html_path and isinstance(html_path, str)  else Path(html_path) or self.html_path

        try:
            service_apendix = self.service_apendix(lang)
            data['products'].append(service_apendix)
            template:str = 'template_table_he.html' if lang == 'he' else  'template_table_ru.html'
            template_path: str  =  str(gs.path.endpoints / Config.ENDPOINT / 'report_generator' / 'templates' / template)
            # template = self.env.get_template(self.template_path)
            template_string = Path(template_path).read_text(encoding = 'UTF-8')
            template = self.env.from_string(template_string)
            self.html_content:str = template.render(**data)

            # try:
            # Path(self.html_path).write_text(data = self.html_content, encoding='UTF-8')
            # except Exception as ex:
            # Logger.error (F "Failed to save the file")
            # return self.html_content
                

            logger.info(f"Файл HTML удачно сохранен в {html_path}")
            return self.html_content

        except Exception as ex:
            logger.error(f"Не удалось сгенерирпвать HTML {html_path}", ex)
            return ''

    async def create_pdf_report_async(self, 
                                data: dict, 
                                lang:str, 
                                pdf_path:str |Path) -> bool:
        """A full cycle of reporting.

        Args:
            Lang (str): report language."""
        pdf_path = pdf_path if pdf_path and isinstance(pdf_path, (str,Path)) else self.pdf_path

        self.html_content = data if data else self.html_content

        from src.utils.pdf import PDFUtils
        pdf = PDFUtils()

        if not pdf.save_pdf_pdfkit(self.html_content, pdf_path):
            logger.error(f"Не удалось сохранить PDF файл {pdf_path}")
            if self.bot: self.bot.send_message(self.chat_id, f"Не удалось сохранить файл {pdf_path}")
            ...
            return False
        

        if self.bot:
            try:
                with open(pdf_path, 'rb') as f:
                    self.bot.send_document(self.chat_id, f)
                    return True
            except Exception as ex:
                self.bot.send_message(self.chat_id, f"Не удалось отправить файл {pdf_path} по причине:\n",ex,False)
                return False

        return True


    async def create_docx_report_async(self, html_path:str|Path, docx_path:str|Path) -> bool :
        """Create a docx file"""

        if not html_to_docx(self.html_path, docx_path):
            logger.error(f"Не скопмилировался DOCX.")
            return False
        return True


    async def create_reports_async(self,

                             data:dict,
                             lang:str,
                             mexiron_name:str,
                             bot: Optional[telebot.TeleBot] = None,
                             chat_id: Optional[int] = None,
                             ) -> tuple:
        """Create ALL types: HTML, PDF, DOCX"""
        ...
        self.storage_path: Path = gs.path.external_storage / Config.ENDPOINT
        self.mexiron_name = mexiron_name 
        export_path = self.storage_path / 'mexironim' / self.mexiron_name

        self.html_path = export_path / f"{self.mexiron_name}_{lang}.html"
        self.pdf_path = export_path / f"{self.mexiron_name}_{lang}.pdf"
        self.docx_path = export_path / f"{self.mexiron_name}_{lang}.docx"
        self.bot = bot
        self.chat_id = chat_id

        self.html_content = await self.create_html_report_async(data, lang, self.html_path)

        if not self.html_content:
            return False


        if self.generate_pdf:
            await self.create_pdf_report_async(self.html_content, lang, self.pdf_path)

        if self.generate_docx:
            await self.create_pdf_report_async(self.html_content, lang, self.pdf_path)

        return True

      
         



# +++++++++++++++++++ man++++++ Mumen examples ++++++++++++ man+++++++++++++++++++++um

def main(maxiron_name:str, lang:str) ->bool:
    
    external_storage: Path =  gs.path.external_storage / Config.ENDPOINT / 'mexironim' /  maxiron_name
    
    html_path: Path =  external_storage / f'{maxiron_name}_{lang}.html' 
    pdf_path: Path = external_storage / f'{maxiron_name}_{lang}.pdf'
    docx_path: Path = external_storage / f'{maxiron_name}_{lang}.docx'
    generate_html: bool = True
    generate_pdf: bool = True
    generate_docx: bool = True 
    data: dict = j_loads(external_storage / f'{maxiron_name}_{lang}.json')
    r = ReportGenerator( generate_html = generate_html,  
                        generate_pdf = generate_pdf, 
                        generate_docx = generate_docx, 
                        html_path = html_path, 
                        pdf_path = pdf_path, 
                        docx_path = docx_path)

    asyncio.run( r.create_reports_async( data,
                                    maxiron_name,
                                    lang, )   
                )

if __name__ == "__main__":
    maxiron_name = '250127221657987' # <- debug
    lang:str = 'ru'
    
    main(maxiron_name, lang)


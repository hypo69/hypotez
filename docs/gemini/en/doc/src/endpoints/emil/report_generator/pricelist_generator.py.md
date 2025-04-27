# Генератор отчётов для мехиронов Казаринова

## Обзор

Этот модуль обеспечивает функциональность для генерации HTML- и PDF-отчётов для мехиронов Казаринова на основе данных из JSON-файлов. 

## Детали

Модуль `pricelist_generator.py`  предоставляет класс `ReportGenerator`, который используется для генерации HTML- и PDF-отчётов, основанных на данных, хранящихся в JSON-файлах.  

## Классы

### `ReportGenerator`

**Описание**: Класс для генерации HTML- и PDF-отчётов на основе данных из JSON-файла.

**Атрибуты**:

- `env` (Environment): Экземпляр класса `Environment` из библиотеки Jinja2, используемый для рендеринга шаблонов.

**Методы**:

- `generate_html(self, data:dict, lang:str ) -> str`: Генерирует HTML-контент на основе шаблона и данных.

- `create_report(self, data: dict, lang:str, html_file:str| Path, pdf_file:str |Path) -> bool`: Полный цикл генерации отчёта, включая преобразование HTML в PDF.

## Функции

### `main(mexiron:str,lang:str) ->bool`

**Описание**: Точка входа для генерации отчёта для конкретного мехирона.

**Параметры**:

- `mexiron` (str): Идентификатор мехирона.
- `lang` (str): Язык отчёта.

**Возвращает**:

- `bool`: `True` если отчет успешно сгенерирован, `False` в случае ошибки.

**Пример**:

```python
# Генерация отчета для мехирона "24_12_01_03_18_24_269" на русском языке
main(mexiron='24_12_01_03_18_24_269', lang='ru')
```


## Детали реализации

###  `ReportGenerator.generate_html`

**Описание**:  Генерирует HTML-контент на основе шаблона и данных. 

**Как работает**:

1.  Определяет путь к файлу шаблона (`template_path`) в зависимости от языка.
2.  Считывает содержимое шаблона из файла (`template_string`).
3.  Создает экземпляр шаблона Jinja2 (`template`) из строки (`template_string`).
4.  Рендерит шаблон с использованием данных из JSON-файла (`data`) и возвращает HTML-контент.

###  `ReportGenerator.create_report`

**Описание**:  Выполняет полный цикл генерации отчёта, включая преобразование HTML в PDF.

**Как работает**:

1.  Добавляет информацию о сервисе в список товаров (`data['products']`).
2.  Генерирует HTML-контент с использованием метода `generate_html`.
3.  Сохраняет HTML-контент в файл (`html_file`).
4.  Создает экземпляр класса `PDFUtils` для преобразования HTML в PDF.
5.  Преобразует HTML в PDF с использованием библиотеки pdfkit.
6.  Возвращает `True` если отчет успешно сгенерирован, `False` в случае ошибки.

## Пример работы

1.  **Загрузка данных:** Данные о мехиронах загружаются из JSON-файла, который расположен в директории `gs.path.external_storage / 'kazarinov' / 'mexironim' / mexiron`.
2.  **Генерация HTML:**  `ReportGenerator.generate_html` генерирует HTML-контент, используя шаблон Jinja2 и данные из JSON-файла.
3.  **Сохранение HTML:** HTML-контент сохраняется в файл с именем `mexiron_lang.html`.
4.  **Преобразование в PDF:** `PDFUtils.save_pdf_pdfkit`  преобразует HTML-контент в PDF-файл.
5.  **Сохранение PDF:** PDF-файл сохраняется в директории с мехироном, названный `mexiron_lang.pdf`.

## Дополнительные замечания

-  В `ReportGenerator.create_report`  в список товаров (`data['products']`) добавляется информация о сервисе.
-  Для генерации случайных изображений для отчета используется функция `random_image` из модуля `src.utils.image`.
-  Для логгирования используется модуль `src.logger.logger`.

```python
## \file /src/endpoints/kazarinov/react/pricelist_generator.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.endpoints.kazarinov.react 
	:platform: Windows, Unix
	:synopsis: Генератор HTML и PDF для мехиронов Казаринова

Описание работы:
- Конструктор `__init__`: Принимает шаблон, базовый путь, метку времени и язык.
- Метод `load_data`: Загружает данные из JSON-файла.
- Метод `generate_html`: Генерирует HTML с использованием Jinja2.
- Метод `save_html`: Сохраняет HTML в файл.
- Метод `generate_pdf`: Преобразует HTML в PDF.
- Метод `create_report`: Запускает полный цикл генерации отчёта.

"""


#https://dev.to/kboskin/building-web-applications-with-react-and-python-2d8c


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

# config = pdfkit.configuration(wkhtmltopdf= str( gs.path.bin / \'wkhtmltopdf\' / \'files\' / \'bin\' / \'wkhtmltopdf.exe\' ) )


@dataclass
class ReportGenerator:
    """
    Класс для генерации HTML- и PDF-отчётов на основе данных из JSON.
    """

    env: Environment = field(default_factory=lambda: Environment(loader=FileSystemLoader('.')))


    async def generate_html(self, data:dict, lang:str ) -> str:
        """
        Генерирует HTML-контент на основе шаблона и данных.

        Args:
            lang (str): Язык отчёта.

        Returns:
            str: HTML-контент.
        """
        template:str = 'template_table_he.html' if lang == 'he' else  'template_table_ru.html'
        template_path: str  =  str(gs.path.endpoints / 'kazarinov' / 'pricelist_generator' / 'templates' / template)
        #template = self.env.get_template(self.template_path)
        template_string = Path(template_path).read_text(encoding = 'UTF-8')
        template = self.env.from_string(template_string)
        return template.render(**data)


    async def create_report(self, data: dict, lang:str, html_file:str| Path, pdf_file:str |Path) -> bool:
        """
        Полный цикл генерации отчёта.

        Args:
            lang (str): Язык отчёта.
        """

        # Обслуживание:
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
### **Анализ кода модуля `quotation_builder.py`**

## \\file /src/endpoints/kazarinov/scenarios/quotation_builder.py

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
  - Код разбит на логические блоки и функции.
  - Используется логирование для отслеживания ошибок.
  - Присутствуют docstring для большинства функций.
- **Минусы**:
  -  Не везде есть аннотации типов.
  -  Не все docstring соответствуют требуемому формату.
  -  Есть устаревшие конструкции (например, `Union[]` вместо `|`).
  -  Не используется `logger` во всех блоках `except`.
  -  В некоторых местах отсутствуют пробелы вокруг оператора присваивания `=`.

**Рекомендации по улучшению:**

1.  **Общие улучшения**:
    - Добавь аннотации типов для всех переменных и параметров функций.
    - Перепиши docstring в соответствии с указанным форматом (Args, Returns, Raises, Example).
    - Замени `Union[]` на `|`.
    - Добавь `logger.error` во все блоки `except`, чтобы логировать ошибки.
    - Добавь пробелы вокруг операторов присваивания `=`.

2.  **Класс `QuotationBuilder`**:
    - Укажи типы для всех атрибутов класса, включая `driver`, `export_path`, `products_list`, `model`, `translations`, `required_fields`.
    - Добавь более подробное описание в docstring для класса.

3.  **Метод `__init__`**:
    - Добавь описание для всех параметров в docstring.
    - Убедись, что все переменные внутри метода аннотированы типами.

4.  **Метод `convert_product_fields`**:
    - Укажи типы для локальных переменных `product_name`, `description`, `description_short`, `specification`.
    - Добавь больше информации в docstring, описывающей процесс конвертации полей.

5.  **Методы `process_llm` и `process_llm_async`**:
    - Убедись, что все локальные переменные аннотированы типами.
    - Добавь более подробное описание в docstring о том, как именно происходит обработка данных AI моделью.
    - Исправить ошибку в `process_llm`, где не возвращается результат рекурсивного вызова функции:
     ```python
     self.process_llm(products_list, lang, attempts -1 )
     ```
     заменить на:
     ```python
     return self.process_llm(products_list, lang, attempts -1 )
     ```

6.  **Метод `save_product_data`**:
    - Добавь описание возвращаемого значения в docstring.

7.  **Метод `post_facebook_async`**:
    - Добавь описание, что делает функция.
    - Убедись, что все локальные переменные аннотированы типами.

8.  **Функция `main`**:
    - Убедись, что все локальные переменные аннотированы типами.

**Оптимизированный код:**

```python
## \file /src/endpoints/kazarinov/scenarios/quotation_builder.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для подготовки данных, обработки AI и интеграции с Facebook для публикации продуктов.
==================================================================

```rst
.. module:: src.endpoints.kazarinov.scenarios.quotation_builder
    :platform: Windows, Unix
    :synopsis: Предоставляет функциональность для извлечения, разбора и обработки данных о продуктах от различных поставщиков.
               Модуль обрабатывает подготовку данных, обработку AI и интеграцию с Facebook для публикации продуктов.
```

"""
import re
from bs4 import BeautifulSoup
from jinja2.utils import F
from pydantic.type_adapter import P
import requests
import asyncio
import random
import shutil
from pathlib import Path
from typing import Optional, List, Any, Tuple
from types import SimpleNamespace
from dataclasses import field
import telebot

import header
from header import __root__
from src import gs
from src.endpoints.prestashop.product_fields import ProductFields

from src.webdriver.driver import Driver
from src.webdriver.firefox import Firefox
from src.webdriver.playwright import Playwrid

from src.ai.gemini import GoogleGenerativeAi
from src.endpoints.advertisement.facebook.scenarios import (
    post_message_title, upload_post_media, message_publish
)
from src.suppliers.suppliers_list.morlevi.graber import Graber as MorleviGraber
from src.suppliers.suppliers_list.ksp.graber import Graber as KspGraber
from src.suppliers.suppliers_list.ivory.graber import Graber as IvoryGraber
from src.suppliers.suppliers_list.grandadvance.graber import Graber as GrandadvanceGraber
from src.endpoints.kazarinov.report_generator import ReportGenerator

from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from src.utils.file import read_text_file, save_text_file, recursively_get_file_path
from src.utils.image import save_image_from_url_async, save_image
from src.utils.printer import pprint as print
from src.logger.logger import logger

##############################################################

ENDPOINT: str = 'kazarinov'

#############################################################

class QuotationBuilder:
    """
    Обрабатывает извлечение, разбор и сохранение данных о продуктах поставщиков.

    Attributes:
        driver (Driver): Экземпляр Selenium WebDriver.
        export_path (Path): Путь для экспорта данных.
        products_list (List[dict]): Список обработанных данных о продуктах.
    """

    base_path: Path = __root__ / 'src' / 'endpoints' / ENDPOINT

    try:
        config: SimpleNamespace = j_loads_ns(base_path / f'{ENDPOINT}.json')
    except Exception as ex:
        logger.error(f"Error loading configuration", ex, exc_info=True)


    html_path: str | Path
    pdf_path: str | Path
    docx_path: str | Path

    #driver: Playwrid = Playwrid()
    driver: 'Driver'
    export_path: Path
    mexiron_name: str
    price: float
    timestamp: str
    products_list: List[dict] = field(default_factory=list)
    model: 'GoogleGenerativeAi'
    translations: 'SimpleNamespace' =  j_loads_ns(base_path / 'translations' / 'mexiron.json')

    # Не все поля товара надо заполнять. Вот кортеж необходимых полей:
    required_fields: tuple = ('id_product',
                                'name',
                                'description_short',
                                'description',
                                'specification',
                                'local_image_path')


    def __init__(self, mexiron_name: Optional[str] = gs.now, driver: Optional[Firefox | Playwrid | str] = None,  **kwards):
        """
        Инициализирует класс Mexiron с необходимыми компонентами.

        Args:
            driver (Optional[Firefox | Playwrid | str]): Инстанс Selenium WebDriver.
            mexiron_name (Optional[str]): Пользовательское имя для процесса Mexiron. По умолчанию gs.now.
            webdriver_name (Optional[str]): Имя используемого веб-драйвера. По умолчанию 'firefox'. Вызов Firefox или Playwrid.
            window_mode (Optional[str]): Оконный режим веб-драйвера. Может быть 'maximized', 'headless', 'minimized', 'fullscreen', 'normal', 'hidden', 'kiosk'.

        """
        self.mexiron_name: str = mexiron_name
        try:
            self.export_path: Path = gs.path.external_storage / ENDPOINT / 'mexironim' / self.mexiron_name
        except Exception as ex:
            logger.error(f"Error constructing export path:", ex, exc_info=True)
            ...
            return

        # 1. Initialize webdriver

        if driver:

           if isinstance(driver, Driver):
                self.driver: Driver = driver

           elif isinstance(driver, (Firefox, Playwrid, )):  # Chrome, Edge
                self.driver: Driver = Driver(driver, **kwards)

           elif isinstance(driver, str):
               if driver.lower() == 'firefox':
                    self.driver: Driver = Driver(Firefox, **kwards)

               elif driver.lower() == 'playwright':
                    self.driver: Driver = Driver(Playwrid, **kwards)

        else:
            self.driver: Driver = Driver(Firefox, **kwards)



        # 2. Initialize Gemini model

        try:
            system_instruction: str = (gs.path.endpoints / ENDPOINT / 'instructions' / 'system_instruction_mexiron.md').read_text(encoding='UTF-8')
            api_key: str = gs.credentials.gemini.kazarinov
            self.model: GoogleGenerativeAi = GoogleGenerativeAi(
                api_key=api_key,
                system_instruction=system_instruction,
                generation_config={'response_mime_type': 'application/json'}
            )
        except Exception as ex:
            logger.error(f"Error loading model, or instructions or API key:", ex, exc_info=True)
            ...


    def convert_product_fields(self, f: ProductFields) -> dict:
        """
        Конвертирует поля продукта из объекта `ProductFields` в словарь.

        Функция конвертирует поля из объекта `ProductFields` в простой словарь для модели ии.
        Она извлекает данные из полей `name`, `description`, `description_short` и `specification`,
        а также путь к локальному изображению продукта.

        Args:
            f (ProductFields): Объект, содержащий распарсенные данные о продукте.

        Returns:
            dict: Форматированный словарь с данными продукта.

        .. note:: Правила построения полей определяются в `ProductFields`
        """
        if not f.id_product:
            logger.error(f"Сбой при получении полей товара. ")
            return {} # <- сбой при получении полей товара. Такое может произойти если вместо страницы товара попалась страница категории, при невнимательном составлении мехирона из комплектующих
        ...



        product_name: str = f.name['language']['value'] if f.name else ''
        description: str = f.description['language']['value'] if f.description else ''
        description_short: str = f.description_short['language']['value'] if f.description_short else ''
        specification: str = f.specification['language']['value']  if f.specification else ''

        if not product_name:
            return {}
        return {
            'product_name':product_name,
            'product_id': f.id_product,
            'description_short':description_short,
            'description': description,
            'specification': specification,
            'local_image_path': str(f.local_image_path),
        }

    def process_llm(self, products_list: List[str], lang: str,  attempts: int = 3) -> dict | bool:
        """
        Обрабатывает список продуктов с использованием AI модели.

        Функция отправляет список продуктов в AI модель для обработки и возвращает результат.
        Если возникает ошибка при получении или обработке ответа, функция повторяет попытку указанное количество раз.

        Args:
            products_list (List[str]): Список словарей с данными о продуктах в виде строки.
            lang (str): Язык, на котором нужно получить ответ от модели.
            attempts (int, optional): Количество попыток повтора в случае неудачи. По умолчанию 3.

        Returns:
            dict | bool: Обработанный ответ в формате словаря.
                         Возвращает `False`, если не удалось получить валидный ответ после всех попыток.

        .. note::
            Модель может возвращать невалидный результат.
            В таком случае я переспрашиваю модель разумное количество раз.
        """
        if attempts < 1:
            ...
            return {}  # return early if no attempts are left

        model_command: str = Path(gs.path.endpoints / ENDPOINT / 'instructions' / f'command_instruction_mexiron_{lang}.md').read_text(encoding='UTF-8')
        # Request response from the AI model
        q: str = model_command + '\n' + str(products_list)
        response: str = self.model.ask(q)
        if not response:
            logger.error(f"Нет ответа от модели", exc_info=True)
            ...
            return {}


        response_dict: dict = j_loads(response) # <- если будет ошибка , то вернется пустой словарь

        if not response_dict:
            logger.error(f"Ошибка парсинга ответа модели", exc_info=True)
            if attempts > 1:
                ...
                return self.process_llm(products_list, lang, attempts -1 )
            return {}
        return  response_dict

    async def process_llm_async(self, products_list: List[str], lang: str,  attempts: int = 3) -> dict | bool:
        """
        Асинхронно обрабатывает список продуктов с использованием AI модели.

        Функция отправляет список продуктов в AI модель для обработки и возвращает результат.
        Если возникает ошибка при получении или обработке ответа, функция повторяет попытку указанное количество раз.

        Args:
            products_list (List[str]): Список словарей с данными о продуктах в виде строки.
            lang (str): Язык, на котором нужно получить ответ от модели.
            attempts (int, optional): Количество попыток повтора в случае неудачи. По умолчанию 3.

        Returns:
            dict | bool: Обработанный ответ в формате словаря.
                         Возвращает `False`, если не удалось получить валидный ответ после всех попыток.

        .. note::
            Модель может возвращать невалидный результат.
            В таком случае я переспрашиваю модель разумное количество раз.
        """
        if attempts < 1:
            ...
            return {}  # return early if no attempts are left

        model_command: str = Path(gs.path.endpoints / ENDPOINT / 'instructions' / f'command_instruction_mexiron_{lang}.md').read_text(encoding='UTF-8')
        # Request response from the AI model
        q: str = model_command + '\n' + str(products_list)

        response: str = await self.model.ask_async(q) # CORRECT

        if not response:
            logger.error(f"Нет ответа от модели", exc_info=True)
            ...
            return {}

        response_dict: dict = j_loads(response) # <- если будет ошибка , то вернется пустой словарь

        if not response_dict:
            logger.error(f'Ошибка {attempts} парсинга ответа модели', exc_info=True)
            if attempts > 1:
                ...
                return await self.process_llm_async(products_list, lang, attempts - 1)
            return {}
        return  response_dict

    async def save_product_data(self, product_data: dict) -> bool:
        """
        Сохраняет данные отдельного продукта в файл.

        Args:
            product_data (dict): Форматированные данные продукта.

        Returns:
            bool: True если сохранено успешно
        """
        file_path: Path = self.export_path / 'products' / f"{product_data['product_id']}.json"
        if not j_dumps(product_data, file_path, ensure_ascii=False):\
            logger.error(f'Ошибка сохранения словаря {print(product_data)}\n Путь: {file_path}', exc_info=True)
            ...
            return
        return True


    async def post_facebook_async(self, mexiron: SimpleNamespace) -> bool:
        """Функция исполняет сценарий рекламного модуля `facvebook`."""
        ...
        self.driver.get_url(r'https://www.facebook.com/profile.php?id=61566067514123')
        currency: str = "ש''ח"
        title: str = f'{mexiron.title}\n{mexiron.description}\n{mexiron.price} {currency}'
        if not post_message_title(self.d, title):
            logger.warning(f'Не получилось отправить название мехирона')
            ...
            return

        if not upload_post_media(self.d, media = mexiron.products):
            logger.warning(f'Не получилось отправить media')
            ...
            return
        if not message_publish(self.d):
            logger.warning(f'Не получилось отправить media')
            ...
            return

        return True

def main():
    """"""
    ...
    lang: str = 'he'

    mexiron_name: str = '250203025325520'
    base_path: Path = Path(gs.path.external_storage)
    export_path: Path = base_path / ENDPOINT / 'mexironim' / mexiron_name
    html_path: Path = export_path / f'{mexiron_name}_{lang}.html'
    pdf_path: Path = export_path / f'{mexiron_name}_{lang}.pdf'
    docx_path: Path = export_path / f'{mexiron_name}_{lang}.doc'
    data: dict = j_loads(export_path / f'{mexiron_name}_{lang}.json')

    quotation: QuotationBuilder = QuotationBuilder(mexiron_name)
    asyncio.run(quotation.create_reports(data[lang], mexiron_name, lang, html_path, pdf_path, docx_path))


if __name__ == '__main__':
    main()
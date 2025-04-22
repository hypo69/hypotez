### **Анализ кода модуля `from_supplier_to_prestashop`**

## \file /src/endpoints/emil/scenarios/from_supplier_to_prestashop.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль исполнения сценария `emil-design.com`
==================================================================

```rst
.. module:: src.endpoints.emil.scenarios.from_supplier_to_prestashop
	:platform: Windows, Unix
	:synopsis: Provides functionality for extracting, parsing, and processing product data from 
various suppliers. The module handles data preparation, AI processing, 
and integration with Prestashop for product posting.
```

"""

import os

import asyncio
import random
import shutil
from pathlib import Path
from tkinter import SEL
from typing import Optional, List
from types import SimpleNamespace

import header
from header import __root__
from src import gs, USE_ENV

from src.endpoints.prestashop.product_fields import ProductFields
from src.endpoints.prestashop.product import PrestaProduct

from src.webdriver.driver import Driver
from src.webdriver.firefox import Firefox
from src.llm.gemini import GoogleGenerativeAi
from src.endpoints.emil.report_generator import ReportGenerator
from src.endpoints.advertisement.facebook.scenarios import post_message_title, upload_post_media, message_publish
from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_url

from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from src.utils.file import read_text_file, save_text_file, recursively_get_file_path
from src.utils.image import save_image_from_url_async, save_image
from src.utils.convertors.unicode import decode_unicode_escape
from src.utils.printer import pprint as print
from src.logger.logger import logger

from dataclasses import dataclass

@dataclass
class Config:
    ENDPOINT = 'emil'

    if USE_ENV:
        from dotenv import load_dotenv
        load_dotenv()


class SupplierToPrestashopProvider:
    """Обрабатывает извлечение, разбор и сохранение данных о товарах поставщиков.
    Данные могут быть получены как с посторонних сайтов, так и из файла JSON.

    Attributes:
        driver (Driver): Экземпляр Selenium WebDriver.
        export_path (Path): Путь для экспорта данных.
        products_list (List[dict]): Список обработанных данных о товарах.
    """
    base_dir: Path = __root__ / 'src' / 'suppliers' / 'supppliers_list' / Config.ENDPOINT
    driver: Driver
    export_path: Path
    mexiron_name: str
    price: float
    timestamp: str
    products_list: list
    model: GoogleGenerativeAi
    config: SimpleNamespace
    local_images_path: Path = gs.path.external_storage / Config.ENDPOINT / 'images' / 'furniture_images'
    lang: str
    gemini_api: str
    presta_api: str
    presta_url: str


    def __init__(self,
                 lang: str,
                 gemini_api: str,
                 presta_api: str,
                 presta_url: str,
                 driver: Optional[Driver] = None,
                 ):
        """
        Инициализирует класс SupplierToPrestashopProvider с необходимыми компонентами.

        Args:
            lang (str): Язык.
            gemini_api (str): API ключ Gemini.
            presta_api (str): API ключ Prestashop.
            presta_url (str): URL Prestashop.
            driver (Optional[Driver], optional): Экземпляр Selenium WebDriver. Defaults to None.
        """
        self.gemini_api = gemini_api
        self.presta_api = presta_api
        self.presta_url = presta_url
        self.lang = lang
        try:
            self.config = j_loads_ns(gs.path.endpoints / Config.ENDPOINT / f'{Config.ENDPOINT}.json')
        except Exception as ex:
            logger.error(f"Ошибка загрузки конфигурации: {ex}", ex, exc_info=True)
            return  # или raise an exception, в зависимости от вашей стратегии обработки ошибок

        self.timestamp = gs.now
        self.driver = driver if driver else Driver(Firefox)
        self.model = self.initialise_ai_model(self.lang)


    def initialise_ai_model(self) -> GoogleGenerativeAi | None:
        """Инициализация модели Gemini.

        Функция загружает системные инструкции для модели Gemini и инициализирует модель с этими инструкциями.

        Returns:
            GoogleGenerativeAi | None: Объект GoogleGenerativeAi или None в случае ошибки.
        """
        try:
            system_instruction = (gs.path.endpoints / 'emil' / 'instructions' / f'system_instruction_mexiron.{self.lang}.md').read_text(encoding='UTF-8')
            return GoogleGenerativeAi(
                api_key=gs.credentials.gemini.kazarinov,
                system_instruction=system_instruction,
                generation_config={'response_mime_type': 'application/json'}
            )
        except Exception as ex:
            logger.error("Ошибка загрузки инструкций", ex, exc_info=True)
            return None

    async def process_graber(
        self,
        urls: list[str],
        price: Optional[str] = '',
        mexiron_name: Optional[str] = '',
        scenarios: dict | list[dict, dict] = None,

    ) -> bool:
        """
        Выполняет сценарий: разбирает товары, обрабатывает их через AI и сохраняет данные.

        Args:
            urls (list[str]): URL страниц товаров.
            price (Optional[str], optional): Цена для обработки. Defaults to ''.
            mexiron_name (Optional[str], optional): Пользовательское имя Mexiron. Defaults to ''.
            scenarios (dict | list[dict, dict], optional): Сценарий исполнения, который находится в директории `src.suppliers.suppliers_list.<supplier>.sceanarios`. Defaults to None.

        Returns:
            bool: True, если сценарий выполнен успешно, иначе False.

        .. todo:
            сделать логер перед отрицательным выходом из функции.
            Важно! модель ошибается.
        """

        # Не все поля товара надо заполнять. Вот кортеж необходимых полей:
        required_fields: tuple = (
            'id_product',
            'name',
            'description_short',
            'description',
            'specification',
            'local_image_path'
        )
        products_list = []

        # 1. Сбор товаров
        for url in urls:

            graber = get_graber_by_supplier_url(url)

            if not graber:
                logger.debug(f"Нет грабера для: {url}", None, False)
                ...
                continue

            try:
                # scenarios_files_list:list =  recursively_get_file_path(__root__ / 'src' / 'suppliers' / 'suppliers_list' / graber.supplier_prefix / 'scenarios', '.json')
                # f = await graber.grab_page(*required_fields)

                graber.process_graber('hb')
                ...

            except Exception as ex:
                logger.error("Ошибка получения полей товара", ex, exc_info=True)
                ...
                continue

            if not f:
                logger.debug(f'Не удалось разобрать поля товара для URL: {url}')
                ...
                continue

            product_data = await self.convert_product_fields(f)
            if not product_data:
                logger.debug(f'Не удалось преобразовать поля товара: {product_data}')
                ...
                continue

            if not await self.save_product_data(product_data):
                logger.error(f"Данные не сохранены! {print(product_data)}")
                ...
                continue
            products_list.append(product_data)

    async def process_scenarios(self, suppliers_prefixes: Optional[str] = '') -> bool:
        """Обрабатывает сценарии для заданных префиксов поставщиков.

        Args:
            suppliers_prefixes (Optional[str], optional): Префиксы поставщиков. Defaults to ''.

        Returns:
            bool: Результат обработки сценариев.
        """
        ...
        suppliers_prefixes = suppliers_prefixes if isinstance(suppliers_prefixes, list) else [suppliers_prefixes] if isinstance(suppliers_prefixes, str) else []


    async def save_product_data(self, product_data: dict) -> bool:
        """
        Сохраняет данные об отдельном товаре в файл.

        Args:
            product_data (dict): Отформатированные данные о товаре.

        Returns:
            bool: True, если данные успешно сохранены, иначе False.
        """
        file_path = self.export_path / 'products' / f"{product_data['product_id']}.json"
        if not j_dumps(product_data, file_path, ensure_ascii=False):
            logger.error(f'Ошибка сохранения словаря {print(product_data)}\n Путь: {file_path}')
            ...
            return False
        return True

    async def process_llm(self, products_list: List[str], lang: str, attempts: int = 3) -> dict | bool:
        """
        Обрабатывает список товаров через AI модель.

        Args:
            products_list (List[str]): Список словарей с данными товаров в виде строки.
            lang (str): Язык обработки.
            attempts (int, optional): Количество попыток повтора в случае неудачи. Defaults to 3.

        Returns:
            dict: Обработанный ответ в формате `ru` и `he`.
            bool: False, если не удалось получить допустимый ответ после повторных попыток.

        .. note::
            Модель может возвращать невалидный результат.
            В таком случае я переспрашиваю модель разумное количество раз.
        """
        if attempts < 1:
            ...
            return {}  # return early if no attempts are left
        model_command = Path(gs.path.endpoints / 'emil' / 'instructions' / f'command_instruction_mexiron_{lang}.md').read_text(encoding='UTF-8')
        # Request response from the AI model
        q = model_command + '\n' + str(products_list)
        response = await self.model.ask(q)
        if not response:
            logger.error("Нет ответа от модели")
            ...
            return {}

        response_dict: dict = j_loads(response)

        if not response_dict:
            logger.error("Ошибка парсинга ответа модели", None, False)
            if attempts > 1:
                ...
                await self.process_llm(products_list, lang, attempts - 1)
            return {}
        return response_dict


    async def save_in_prestashop(self, products_list: ProductFields | list[ProductFields]) -> bool:
        """Функция, которая сохраняет товары в Prestashop emil-design.com.

        Args:
            products_list (ProductFields | list[ProductFields]): Список товаров для сохранения.

        Returns:
            bool: True, если товары успешно сохранены, иначе False.
        """

        products_list: list = products_list if isinstance(products_list, list) else [products_list]

        p = PrestaProduct(api_key=self.presta_api, api_domain=self.presta_url)

        for f in products_list:
            p.add_new_product(f)

    async def post_facebook(self, mexiron: SimpleNamespace) -> bool:
        """Функция исполняет сценарий рекламного модуля `facebook`.

        Args:
            mexiron (SimpleNamespace): Данные для публикации в Facebook.

        Returns:
            bool: True, если публикация прошла успешно, иначе False.
        """
        ...
        self.driver.get_url('https://www.facebook.com/profile.php?id=61566067514123')
        currency = "ש''ח"
        title = f'{mexiron.title}\n{mexiron.description}\n{mexiron.price} {currency}'
        if not post_message_title(self.driver, title):
            logger.warning('Не получилось отправить название мехирона')
            ...
            return False

        if not upload_post_media(self.driver, media=mexiron.products):
            logger.warning('Не получилось отправить media')
            ...
            return False
        if not message_publish(self.driver):
            logger.warning('Не получилось отправить media')
            ...
            return False

        return True

    async def create_report(self, data: dict, lang: str, html_file: Path, pdf_file: Path) -> bool:
        """Функция отправляет задание на создание отчета в формате `html` и `pdf`.
        Если отчет в формате pdf создался (`generator.create_report()` вернул True) -
        отправить его боту.

        Args:
            data (dict): Данные для отчета.
            lang (str): Язык отчета.
            html_file (Path): Путь для сохранения HTML файла.
            pdf_file (Path): Путь для сохранения PDF файла.

        Returns:
            bool: True, если отчет создан и отправлен успешно, иначе False.
        """

        report_generator = ReportGenerator()

        if await report_generator.create_report(data, lang, html_file, pdf_file):
            # Проверка, существует ли файл и является ли он файлом
            if pdf_file.exists() and pdf_file.is_file():
                # Отправка боту PDF-файл через reply_document()
                await self.update.message.reply_document(document=pdf_file)
                return True
            else:
                logger.error(f"PDF файл не найден или не является файлом: {pdf_file}")
                return False


async def upload_redacted_images_from_emil():
    """
    На данный момент функция читает JSON со списком фотографий, которые были получены от Эмиля.
    """
    lang = 'he'
    ENDPOINT = 'emil'
    products_ns = j_loads_ns(gs.path.external_storage / ENDPOINT / 'out_250108230345305_he.json')
    suppier_to_presta = SupplierToPrestashopProvider(lang=lang, gemini_api = gs.credentials.gemini.kazarinov, presta_api = gs.credentials.prestashop.emil.api_key, presta_url = gs.credentials.prestashop.emil.api_url)
    products_list: list = [f for f in products_ns]
    await suppier_to_presta.save_in_prestashop(products_list)


async def main():
    """
    """
    await upload_redacted_images_from_emil()




if __name__ == '__main__':
    asyncio.run(main())
```

## **Анализ кода модуля `from_supplier_to_prestashop`**

**Качество кода:**
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код хорошо структурирован и содержит docstring для большинства функций и классов.
  - Используется логирование с помощью `logger`.
  - Применение `j_loads`, `j_loads_ns`, `j_dumps` для работы с JSON.
  - Использование `dataclass` для класса `Config`.
- **Минусы**:
  - Некоторые docstring отсутствуют или неполные.
  - В коде встречаются закомментированные участки кода.
  - Не везде используется аннотация типов.
  - Встречаются `...` в коде, что указывает на незавершенную реализацию.
  - Использование `USE_ENV` и `load_dotenv` внутри класса `Config` может привести к проблемам с конфигурацией.
  - В методе `post_facebook` хардкодится URL.
  - Не везде в блоках `except` передается `exc_info=True` в `logger.error`.

**Рекомендации по улучшению:**

1.  **Документация**:
    *   Заполнить отсутствующие docstring для функций и классов.
    *   Улучшить существующие docstring, сделав их более подробными и информативными.
    *   Перевести docstring на русский язык, если они написаны на английском.

2.  **Аннотация типов**:
    *   Добавить аннотации типов для всех переменных, аргументов функций и возвращаемых значений, где они отсутствуют.

3.  **Обработка ошибок**:
    *   Убедиться, что во всех блоках `except` передается `exc_info=True` в `logger.error` для получения полной информации об ошибке.
    *   Рассмотреть возможность обработки исключений более конкретно, чтобы избежать перехвата всех исключений подряд.

4.  **Конфигурация**:
    *   Вынести логику `USE_ENV` и `load_dotenv` из класса `Config` в более подходящее место, например, в начале модуля или в отдельную функцию конфигурации.

5.  **Удаление неиспользуемого кода**:
    *   Удалить закомментированные участки кода, если они не несут полезной информации.

6.  **Завершение реализации**:
    *   Заменить все `...` реальным кодом или, если это не планируется, удалить их и добавить соответствующий комментарий.

7.  **Метод `post_facebook`**:
    *   Убрать хардкод URL и вынести его в конфигурацию.
    *   Использовать `cls` вместо `self` там, где это уместно.

8.  **Именование**:
    *   Использовать более описательные имена переменных и функций, чтобы повысить читаемость кода.

**Оптимизированный код:**

```python
## \file /src/endpoints/emil/scenarios/from_supplier_to_prestashop.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль исполнения сценария `emil-design.com`
==================================================================

```rst
.. module:: src.endpoints.emil.scenarios.from_supplier_to_prestashop
	:platform: Windows, Unix
	:synopsis: Обеспечивает функциональность для извлечения, разбора и обработки данных о товарах
различных поставщиков. Модуль обрабатывает подготовку данных, обработку с помощью AI и
интеграцию с Prestashop для размещения товаров.
```

"""

import os
import asyncio
import random
import shutil
from pathlib import Path
from typing import Optional, List
from types import SimpleNamespace

import header
from header import __root__
from src import gs, USE_ENV

from src.endpoints.prestashop.product_fields import ProductFields
from src.endpoints.prestashop.product import PrestaProduct

from src.webdriver.driver import Driver
from src.webdriver.firefox import Firefox
from src.llm.gemini import GoogleGenerativeAi
from src.endpoints.emil.report_generator import ReportGenerator
from src.endpoints.advertisement.facebook.scenarios import post_message_title, upload_post_media, message_publish
from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_url

from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from src.utils.file import read_text_file, save_text_file, recursively_get_file_path
from src.utils.image import save_image_from_url_async, save_image
from src.utils.convertors.unicode import decode_unicode_escape
from src.utils.printer import pprint as print
from src.logger.logger import logger

from dataclasses import dataclass

if USE_ENV:
    from dotenv import load_dotenv
    load_dotenv()


@dataclass
class Config:
    """
    Конфигурация для модуля emil.
    """
    ENDPOINT: str = 'emil'
    FACEBOOK_PROFILE_URL: str = "https://www.facebook.com/profile.php?id=61566067514123"


class SupplierToPrestashopProvider:
    """Обрабатывает извлечение, разбор и сохранение данных о товарах поставщиков.
    Данные могут быть получены как с посторонних сайтов, так и из файла JSON.

    Attributes:
        driver (Driver): Экземпляр Selenium WebDriver.
        export_path (Path): Путь для экспорта данных.
        products_list (List[dict]): Список обработанных данных о товарах.
    """
    base_dir: Path = __root__ / 'src' / 'suppliers' / 'supppliers_list' / Config.ENDPOINT
    driver: Driver
    export_path: Path
    mexiron_name: str
    price: float
    timestamp: str
    products_list: list
    model: GoogleGenerativeAi
    config: SimpleNamespace
    local_images_path: Path = gs.path.external_storage / Config.ENDPOINT / 'images' / 'furniture_images'
    lang: str
    gemini_api: str
    presta_api: str
    presta_url: str


    def __init__(self,
                 lang: str,
                 gemini_api: str,
                 presta_api: str,
                 presta_url: str,
                 driver: Optional[Driver] = None,
                 ):
        """
        Инициализирует класс SupplierToPrestashopProvider с необходимыми компонентами.

        Args:
            lang (str): Язык.
            gemini_api (str): API ключ Gemini.
            presta_api (str): API ключ Prestashop.
            presta_url (str): URL Prestashop.
            driver (Optional[Driver], optional): Экземпляр Selenium WebDriver. Defaults to None.
        """
        self.gemini_api = gemini_api
        self.presta_api = presta_api
        self.presta_url = presta_url
        self.lang = lang
        try:
            self.config = j_loads_ns(gs.path.endpoints / Config.ENDPOINT / f'{Config.ENDPOINT}.json')
        except Exception as ex:
            logger.error(f"Ошибка загрузки конфигурации: {ex}", ex, exc_info=True)
            return  # или raise an exception, в зависимости от вашей стратегии обработки ошибок

        self.timestamp = gs.now
        self.driver = driver if driver else Driver(Firefox)
        self.model = self.initialise_ai_model(self.lang)


    def initialise_ai_model(self) -> GoogleGenerativeAi | None:
        """Инициализация модели Gemini.

        Функция загружает системные инструкции для модели Gemini и инициализирует модель с этими инструкциями.

        Returns:
            GoogleGenerativeAi | None: Объект GoogleGenerativeAi или None в случае ошибки.
        """
        try:
            system_instruction = (gs.path.endpoints / 'emil' / 'instructions' / f'system_instruction_mexiron.{self.lang}.md').read_text(encoding='UTF-8')
            return GoogleGenerativeAi(
                api_key=gs.credentials.gemini.kazarinov,
                system_instruction=system_instruction,
                generation_config={'response_mime_type': 'application/json'}
            )
        except Exception as ex:
            logger.error("Ошибка загрузки инструкций", ex, exc_info=True)
            return None

    async def process_graber(
        self,
        urls: list[str],
        price: Optional[str] = '',
        mexiron_name: Optional[str] = '',
        scenarios: dict | list[dict, dict] = None,

    ) -> bool:
        """
        Выполняет сценарий: разбирает товары, обрабатывает их через AI и сохраняет данные.

        Args:
            urls (list[str]): URL страниц товаров.
            price (Optional[str], optional): Цена для обработки. Defaults to ''.
            mexiron_name (Optional[str], optional): Пользовательское имя Mexiron. Defaults to ''.
            scenarios (dict | list[dict, dict], optional): Сценарий исполнения, который находится в директории `src.suppliers.suppliers_list.<supplier>.sceanarios`. Defaults to None.

        Returns:
            bool: True, если сценарий выполнен успешно, иначе False.
        """

        # Не все поля товара надо заполнять. Вот кортеж необходимых полей:
        required_fields: tuple = (
            'id_product',
            'name',
            'description_short',
            'description',
            'specification',
            'local_image_path'
        )
        products_list = []

        # 1. Сбор товаров
        for url in urls:

            graber = get_graber_by_supplier_url(url)

            if not graber:
                logger.debug(f"Нет грабера для: {url}")
                continue

            try:
                # scenarios_files_list:list =  recursively_get_file_path(__root__ / 'src' / 'suppliers' / 'suppliers_list' / graber.supplier_prefix / 'scenarios', '.json')
                # f = await graber.grab_page(*required_fields)

                graber.process_graber('hb')
                ...

            except Exception as ex:
                logger.error("Ошибка получения полей товара", ex, exc_info=True)
                continue

            if not f:
                logger.debug(f'Не удалось разобрать поля товара для URL: {url}')
                continue

            product_data = await self.convert_product_fields(f)
            if not product_data:
                logger.debug(f'Не удалось преобразовать поля товара: {product_data}')
                continue

            if not await self.save_product_data(product_data):
                logger.error(f"Данные не сохранены! {print(product_data)}")
                continue
            products_list.append(product_data)

    async def process_scenarios(self, suppliers_prefixes: Optional[str] = '') -> bool:
        """Обрабатывает сценарии для заданных префиксов поставщиков.

        Args:
            suppliers_prefixes (Optional[str], optional): Префиксы поставщиков. Defaults to ''.

        Returns:
            bool: Результат обработки сценариев.
        """
        suppliers_prefixes = suppliers_prefixes if isinstance(suppliers_prefixes, list) else [suppliers_prefixes] if isinstance(suppliers_prefixes, str) else []
        ...


    async def save_product_data(self, product_data: dict) -> bool:
        """
        Сохраняет данные об отдельном товаре в файл.

        Args:
            product_data (dict): Отформатированные данные о товаре.

        Returns:
            bool: True, если данные успешно сохранены, иначе False.
        """
        file_path = self.export_path / 'products' / f"{product_data['product_id']}.json"
        if not j_dumps(product_data, file_path, ensure_ascii=False):
            logger.error(f'Ошибка сохранения словаря {print(product_data)}\n Путь: {file_path}', exc_info=True)
            return False
        return True

    async def process_llm(self, products_list: List[str], lang: str, attempts: int = 3) -> dict | bool:
        """
        Обрабатывает список товаров через AI модель.

        Args:
            products_list (List[str]): Список словарей с данными товаров в виде строки.
            lang (str): Язык обработки.
            attempts (int, optional): Количество попыток повтора в случае неудачи. Defaults to 3.

        Returns:
            dict: Обработанный ответ в формате `ru` и `he`.
            bool: False, если не удалось получить допустимый ответ после повторных попыток.
        """
        if attempts < 1:
            return {}  # return early if no attempts are left
        model_command = Path(gs.path.endpoints / 'emil' / 'instructions' / f'command_instruction_mexiron_{lang}.md').read_text(encoding='UTF-8')
        # Request response from the AI model
        q = model_command + '\n' + str(products_list)
        response = await self.model.ask(q)
        if not response:
            logger.error("Нет ответа от модели", exc_info=True)
            return {}

        response_dict: dict = j_loads(response)

        if not response_dict:
            logger.error("Ошибка парсинга ответа модели", exc_info=True)
            if attempts > 1:
                await self.process_llm(products_list, lang, attempts - 1)
            return {}
        return response_dict


    async def save_in_prestashop(self, products_list: ProductFields | list[ProductFields]) -> bool:
        """Сохраняет товары в Prestashop emil-design.com.

        Args:
            products_list (ProductFields | list[ProductFields]): Список товаров для сохранения.

        Returns:
            bool: True, если товары успешно сохранены, иначе False.
        """

        products_list: list = products_list if isinstance(products_list, list) else [products_list]

        p = PrestaProduct(api_key=self.presta_api, api_domain=self.presta_url)

        for f in products_list:
            p.add_new_product(f)

    async def post_facebook(self, mexiron: SimpleNamespace) -> bool:
        """Исполняет сценарий рекламного модуля `facebook`.

        Args:
            mexiron (SimpleNamespace): Данные для публикации в Facebook.

        Returns:
            bool: True, если публикация прошла успешно, иначе False.
        """
        self.driver.get_url(Config.FACEBOOK_PROFILE_URL)
        currency = "ש''ח"
        title = f'{mexiron.title}\n{mexiron.description}\n{mexiron.price} {currency}'
        if not post_message_title(self.driver, title):
            logger.warning('Не получилось отправить название мехирона')
            return False

        if not upload_post_media(self.driver, media=mexiron.products):
            logger.warning('Не получилось отправить media')
            return False
        if not message_publish(self.driver):
            logger.warning('Не получилось отправить media')
            return False

        return True

    async def create_report(self, data: dict, lang: str, html_file: Path, pdf_file: Path) -> bool:
        """Отправляет задание на создание отчета в формате `html` и `pdf`.
        Если отчет в формате pdf создался (`generator.create_report()` вернул True) -
        отправить его боту.

        Args:
            data (dict): Данные для отчета.
            lang (str): Язык отчета.
            html_file (Path): Путь для сохранения HTML файла.
            pdf_file (Path): Путь для сохранения PDF файла.

        Returns:
            bool: True, если отчет создан и отправлен успешно, иначе False.
        """

        report_generator = ReportGenerator()

        if await report_generator.create_report(data, lang, html_file, pdf_file):
            # Проверка, существует ли файл и является ли он файлом
            if pdf_file.exists() and pdf_file.is_file():
                # Отправка боту PDF-файл через reply_document()
                await self.update.message.reply_document(document=pdf_file)
                return True
            else:
                logger.error(f"PDF файл не найден или не является файлом: {pdf_file}")
                return False


async def upload_redacted_images_from_emil():
    """
    Читает JSON со списком фотографий, которые были получены от Эмиля и загружает их.
    """
    lang: str = 'he'
    ENDPOINT: str = 'emil'
    products_ns = j_loads_ns(gs.path.external_storage / ENDPOINT / 'out_250108230345305_he.json')
    suppier_to_presta = SupplierToPrestashopProvider(lang=lang, gemini_api = gs.credentials.gemini.kazarinov, presta_api = gs.credentials.prestashop.emil.api_key, presta_url = gs.credentials.prestashop.emil.api_url)
    products_list: list = [f for f in products_ns]
    await suppier_to_presta.save_in_prestashop(products_list)


async def main():
    """
    Основная функция для запуска процесса загрузки отредактированных изображений от Эмиля в Prestashop.
    """
    await upload_redacted_images_from_emil()




if __name__ == '__main__':
    asyncio.run(main())
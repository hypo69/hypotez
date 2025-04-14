### **Анализ кода модуля `from_supplier_to_prestashop.py`**

2. **Качество кода**:
   - **Соответствие стандартам**: 7/10
   - **Плюсы**:
     - Код разбит на логические блоки, упрощающие понимание.
     - Используются аннотации типов, что улучшает читаемость и поддержку кода.
     - Присутствует обработка исключений с логированием ошибок.
     - Активно используется модуль `logger` для записи информации об ошибках и отладочных сообщений.
   - **Минусы**:
     - Не все функции и методы имеют docstring, что затрудняет понимание их назначения.
     - В некоторых местах используется `...` вместо конкретной реализации, что снижает понимание логики работы.
     - Отсутствует единообразие в стиле форматирования (например, использование `print` вместо `logger.info` для отладочной информации).
     - Не все переменные аннотированы типами.

3. **Рекомендации по улучшению**:
   - Добавить docstring для всех функций, методов и классов, чтобы улучшить понимание кода.
   - Заменить `...` конкретной реализацией или объяснить их назначение в комментариях.
   - Использовать `logger` вместо `print` для отладочной информации, чтобы обеспечить единообразие в логировании.
   - Добавить аннотации типов для всех переменных.
   - В `__init__`  добавить аннотацию типа для driver.
   - Перевести все комментарии и docstring на русский язык.
   - В `run_scenario` добавить логирование перед отрицательным выходом из функции, как указано в `todo`.
   - Исправить опечатку в слове `suppier_to_presta` на `supplier_to_presta` в функции `main`.
   - Использовать константы для путей к файлам вместо жестко заданных строк.
   - Явное указание типа для products_list в методе __init__.
   - В `save_in_prestashop` типизировать p: PrestaProduct

4. **Оптимизированный код**:

```python
                ## \file /src/endpoints/emil/scenarios/from_supplier_to_prestashop.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль исполнения сценария создания мехирона для Сергея Казаринова
==================================================================

```rst
.. module:: src.endpoints.emil.scenarios.from_supplier_to_prestashop
    :platform: Windows, Unix
    :synopsis: Provides functionality for extracting, parsing, and processing product data from 
various suppliers. The module handles data preparation, AI processing, 
and integration with Prestashop for product posting.
```

"""

import asyncio
import os
import random
import shutil
from pathlib import Path
from tkinter import SEL
from types import SimpleNamespace
from typing import List, Optional

import header
from src import gs
from src.ai.gemini import GoogleGenerativeAI
from src.endpoints.advertisement.facebook.scenarios import (
    message_publish,
    post_message_title,
    upload_post_media,
)
from src.endpoints.emil.report_generator import ReportGenerator
from src.endpoints.prestashop.product import PrestaProduct
from src.endpoints.prestashop.product_fields import ProductFields
from src.logger.logger import logger
from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_url
from src.utils.convertors.unicode import decode_unicode_escape
from src.utils.file import (
    read_text_file,
    recursively_get_file_path,
    save_text_file,
)
from src.utils.image import save_image, save_image_from_url
from src.utils.jjson import j_dumps, j_loads, j_loads_ns
from src.utils.printer import pprint as print
from src.webdriver.driver import Driver
from src.webdriver.firefox import Firefox

##############################################################

ENDPOINT: str = 'emil'
USE_ENV: bool = True  # <- Определает откуда брать ключи. Если False - то из базы данных с паролями, иначе из .env

if USE_ENV:
    from dotenv import load_dotenv

    load_dotenv()

#############################################################


class SupplierToPrestashopProvider:
    """Обрабатывает извлечение, разбор и сохранение данных о продуктах поставщиков.
    Данные могут быть получены как из посторнних сайтов, так и из файла JSON

    Attributes:
        driver (Driver): Экземпляр Selenium WebDriver.
        export_path (Path): Путь для экспорта данных.
        products_list (List[dict]): Список обработанных данных о продуктах.
    """

    driver: Driver
    export_path: Path
    mexiron_name: str
    price: float
    timestamp: str
    products_list: list
    model: GoogleGenerativeAI
    config: SimpleNamespace
    local_images_path: Path = gs.path.external_storage / ENDPOINT / 'images' / 'furniture_images'
    lang: str
    gemini_api: str
    presta_api: str
    presta_url: str

    def __init__(
        self,
        lang: str,
        gemini_api: str,
        presta_api: str,
        presta_url: str,
        driver: Optional[Driver] = None,
    ):
        """
        Инициализирует класс SupplierToPrestashopProvider необходимыми компонентами.

        Args:
            lang (str): Язык.
            gemini_api (str): API ключ Gemini.
            presta_api (str): API ключ Prestashop.
            presta_url (str): URL Prestashop.
            driver (Optional[Driver], optional): Экземпляр Selenium WebDriver. По умолчанию None.

        """
        self.gemini_api: str = gemini_api
        self.presta_api: str = presta_api
        self.presta_url: str = presta_url
        self.lang: str = lang
        try:
            self.config: SimpleNamespace = j_loads_ns(gs.path.endpoints / ENDPOINT / f'{ENDPOINT}.json')
        except Exception as ex:
            logger.error(f"Error loading configuration: {ex}", ex, exc_info=True)
            return  # or raise an exception, depending on your error handling strategy

        self.timestamp: str = gs.now
        self.driver: Driver = driver if driver else Driver(Firefox)
        self.model: GoogleGenerativeAI = self.initialise_ai_model()

    def initialise_ai_model(self) -> GoogleGenerativeAI | None:
        """Инициализация модели Gemini"""
        try:
            system_instruction: str = (
                gs.path.endpoints / 'emil' / 'instructions' / f'system_instruction_mexiron.{self.lang}.md'
            ).read_text(encoding='UTF-8')
            return GoogleGenerativeAI(
                api_key=gs.credentials.gemini.emil,
                system_instruction=system_instruction,
                generation_config={'response_mime_type': 'application/json'},
            )
        except Exception as ex:
            logger.error(f"Error loading instructions", ex, exc_info=True)
            return None

    async def run_scenario(
        self,
        urls: list[str],
        price: Optional[str] = '',
        mexiron_name: Optional[str] = '',
    ) -> bool:
        """
        Выполняет сценарий: разбирает продукты, обрабатывает их через AI и сохраняет данные.

        Args:
            urls (list[str]): Список URL-адресов продуктов.
            price (Optional[str], optional): Цена для обработки. По умолчанию пустая строка.
            mexiron_name (Optional[str], optional): Пользовательское имя Mexiron. По умолчанию пустая строка.

        Returns:
            bool: True, если сценарий выполнен успешно, False в противном случае.

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
            'local_image_path',
        )
        products_list: list = []

        # 1. Сбор товаров
        for url in urls:
            graber = get_graber_by_supplier_url(url)

            if not graber:
                logger.debug(f"Нет грабера для: {url}", None, False)
                logger.info(f"Нет грабера для: {url}")
                continue

            try:
                f = await graber.grab_page(*required_fields)

                if gs.host_name == 'Vostro-3888':
                    pass
                    # self.driver.wait(5)   # <- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Замедлитель
            except Exception as ex:
                logger.error(f"Ошибка получения полей товара", ex, False)
                logger.error(f"Ошибка получения полей товара: {ex}", ex, exc_info=True)
                continue

            if not f:
                logger.debug(f'Failed to parse product fields for URL: {url}')
                logger.info(f'Не удалось разобрать поля продукта для URL: {url}')
                continue

            product_data = await self.convert_product_fields(f)
            if not product_data:
                logger.debug(f'Failed to convert product fields: {product_data}')
                logger.info(f'Не удалось преобразовать поля продукта: {product_data}')
                continue

            if not await self.save_product_data(product_data):
                logger.error(f"Data not saved! {pprint(product_data)}")
                logger.error(f"Данные не сохранены! {pprint(product_data)}", exc_info=True)
                continue
            products_list.append(product_data)

    async def save_product_data(self, product_data: dict) -> bool:
        """
        Сохраняет данные об отдельном продукте в файл.

        Args:
            product_data (dict): Отформатированные данные продукта.
        """
        file_path: Path = self.export_path / 'products' / f"{product_data['product_id']}.json"
        if not j_dumps(product_data, file_path, ensure_ascii=False):
            logger.error(f'Ошибка сохранения словаря {print(product_data)}\n Путь: {file_path}')
            logger.error(
                f'Ошибка сохранения словаря {print(product_data)}\n Путь: {file_path}', exc_info=True
            )
            return False
        return True

    async def process_ai(self, products_list: List[str], lang: str, attempts: int = 3) -> dict | bool:
        """
        Обрабатывает список продуктов через AI модель.

        Args:
            products_list (str): Список словарей данных о продуктах в виде строки.
            lang (str): Язык.
            attempts (int, optional): Количество попыток повтора в случае сбоя. По умолчанию 3.

        Returns:
            dict: Обработанный ответ в форматах `ru` и `he`.
            bool: False, если не удалось получить допустимый ответ после повторных попыток.

        .. note::
            Модель может возвращать невалидный результат.
            В таком случае я переспрашиваю модель разумное количество раз.
        """
        if attempts < 1:
            logger.error("Нет доступных попыток")
            return {}  # return early if no attempts are left
        model_command: str = (
            Path(gs.path.endpoints / 'emil' / 'instructions' / f'command_instruction_mexiron_{lang}.md').read_text(
                encoding='UTF-8'
            )
        )
        # Request response from the AI model
        q: str = model_command + '\n' + str(products_list)
        response: str = await self.model.ask(q)
        if not response:
            logger.error(f"Нет ответа от модели")
            return {}

        response_dict: dict = j_loads(response)

        if not response_dict:
            logger.error("Ошибка парсинга ответа модели", None, False)
            logger.error("Ошибка парсинга ответа модели", exc_info=True)
            if attempts > 1:
                await self.process_ai(products_list, lang, attempts - 1)
            return {}
        return response_dict

    async def read_data_from_json(self):
        """Загружаю JSON файлы и фотки, которые я сделал через телеграм"""

        # 1. Get from JSON
        raw_data: SimpleNamespace = j_loads_ns(self.local_images_path)
        print(raw_data)

    async def save_in_prestashop(self, products_list: ProductFields | list[ProductFields]) -> bool:
        """Функция, которая сохраняет товары в Prestashop emil-design.com"""

        products_list: list = products_list if isinstance(products_list, list) else [products_list]

        p: PrestaProduct = PrestaProduct(api_key=self.presta_api, api_domain=self.presta_url)

        for f in products_list:
            p.add_new_product(f)

    async def post_facebook(self, mexiron: SimpleNamespace) -> bool:
        """Функция исполняет сценарий рекламного модуля `facvebook`."""

        self.driver.get_url(r'https://www.facebook.com/profile.php?id=61566067514123')
        currency: str = "ש''ח"
        title: str = f'{mexiron.title}\n{mexiron.description}\n{mexiron.price} {currency}'
        if not post_message_title(self.driver, title):
            logger.warning(f'Не получилось отправить название мехирона')
            return False

        if not upload_post_media(self.driver, media=mexiron.products):
            logger.warning(f'Не получилось отправить media')
            return False
        if not message_publish(self.driver):
            logger.warning(f'Не получилось отправить media')
            return False

        return True

    async def create_report(self, data: dict, lang: str, html_file: Path, pdf_file: Path) -> bool:
        """Функция отправляет задание на создание мехирона в формате `html` и `pdf`.
        Если мехорон в pdf создался (`generator.create_report()` вернул True) -
        отправить его боту
        """

        report_generator: ReportGenerator = ReportGenerator()

        if await report_generator.create_report(data, lang, html_file, pdf_file):
            # Проверка, существует ли файл и является ли он файлом
            if pdf_file.exists() and pdf_file.is_file():
                # Отправка боту PDF-файл через reply_document()
                await self.update.message.reply_document(document=pdf_file)
                return True
            else:
                logger.error(f"PDF файл не найден или не является файлом: {pdf_file}")
                return None


async def main():
    """На данный момент функция читает JSON со списком фотографий, которые были получены от Эмиля"""
    lang: str = 'he'
    products_ns: SimpleNamespace = j_loads_ns(
        gs.path.external_storage / ENDPOINT / 'out_250108230345305_he.json'
    )

    supplier_to_presta: SupplierToPrestashopProvider = SupplierToPrestashopProvider(lang)
    products_list: list = [f for f in products_ns]
    await supplier_to_presta.save_in_prestashop(products_list)


if __name__ == '__main__':
    asyncio.run(main())
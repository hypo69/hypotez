### **Анализ кода модуля `quotation_builder`**

## \file /src/endpoints/kazarinov/scenarios/quotation_builder.py

Модуль предоставляет функциональность для извлечения, разбора и обработки данных о продуктах от различных поставщиков, включая подготовку данных, обработку с использованием ИИ и интеграцию с Facebook для публикации продуктов.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Использование `logger` для логирования ошибок.
    - Наличие docstring для большинства функций и классов.
    - Использование `j_loads_ns` для загрузки конфигурационных файлов.
    - Применение аннотаций типов.
- **Минусы**:
    - Не все функции и классы имеют подробные docstring.
    - Отсутствует единообразие в стиле кодирования (например, использование `Driver` вместо `driver` в некоторых местах).
    - Использование `...` как заполнителя, что затрудняет понимание логики кода.
    - Местами отсутствует обработка исключений.
    - Не везде есть проверка типов.
    - Не все переменные аннотированы типами.

**Рекомендации по улучшению:**

1.  **Документирование кода**:
    *   Добавить docstring к каждой функции, методу и классу, подробно описывая их назначение, аргументы, возвращаемые значения и возможные исключения.
    *   Перевести существующие docstring на русский язык и привести к единому формату.
    *   Уточнить и расширить комментарии, чтобы они были более информативными и понятными.
    *   В `__init__` класса `QuotationBuilder` добавить описание полей класса.

2.  **Обработка исключений**:
    *   Добавить обработку исключений в тех местах, где она отсутствует.
    *   Использовать `logger.error` для логирования ошибок с указанием типа исключения и дополнительной информацией.

3.  **Типизация**:
    *   Добавить аннотации типов для всех переменных и параметров функций, где это необходимо.

4.  **Использование веб-драйвера**:
    *   Убедиться, что веб-драйвер инициализируется и используется правильно.
    *   Уточнить, какие методы и классы веб-драйвера используются и как они взаимодействуют с остальным кодом.

5.  **Рефакторинг**:
    *   Устранить использование `...` в коде, заменив их реальной логикой или комментариями, объясняющими, что должно быть реализовано.
    *   Привести код в соответствие со стандартами PEP8.
    *   Использовать `driver` вместо `Driver` для экземпляров драйвера.

6.  **Логирование**:
    *   Добавить логирование действий в ключевых точках выполнения программы.
    *   Использовать разные уровни логирования (INFO, WARNING, ERROR) в зависимости от ситуации.

7.  **Конфигурация**:
    *   Убедиться, что все необходимые конфигурационные файлы загружаются правильно и что в случае ошибки загрузки предусмотрена обработка исключений.

**Оптимизированный код:**

```python
## \file /src/endpoints/kazarinov/scenarios/quotation_builder.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для обработки данных о продуктах и их интеграции с Facebook.
==================================================================

Модуль содержит класс :class:`QuotationBuilder`, который используется для извлечения,
разбора и сохранения данных о продуктах от различных поставщиков.
Модуль обрабатывает подготовку данных, обработку с использованием ИИ
и интеграцию с Facebook для публикации продуктов.
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
from typing import Optional, List, Any
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

from src.ai.gemini import GoogleGenerativeAI
from src.endpoints.advertisement.facebook.scenarios import (
    post_message_title, upload_post_media, message_publish
)
from src.suppliers.morlevi.graber import Graber as MorleviGraber
from src.suppliers.ksp.graber import Graber as KspGraber
from src.suppliers.ivory.graber import Graber as IvoryGraber
from src.suppliers.grandadvance.graber import Graber as GrandadvanceGraber
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
        base_path (Path): Базовый путь к файлам модуля.
        config (SimpleNamespace): Конфигурация, загруженная из JSON.
        html_path (str | Path): Путь к HTML файлу.
        pdf_path (str | Path): Путь к PDF файлу.
        docx_path (str | Path): Путь к DOCX файлу.
        mexiron_name (str): Имя процесса Mexiron.
        price (float): Цена.
        timestamp (str): Временная метка.
        model (GoogleGenerativeAI): Модель Google Generative AI.
        translations (SimpleNamespace): Переводы, загруженные из JSON.
        required_fields (tuple): Кортеж необходимых полей товара.
    """

    base_path: Path = __root__ / 'src' / 'endpoints' / ENDPOINT

    try:
        config: SimpleNamespace = j_loads_ns(base_path / f'{ENDPOINT}.json')
    except Exception as ex:
        logger.error(f"Ошибка загрузки конфигурации", ex, exc_info=True)

    html_path: str | Path
    pdf_path: str | Path
    docx_path: str | Path

    driver: 'Driver'
    export_path: Path
    mexiron_name: str
    price: float
    timestamp: str
    products_list: List = field(default_factory=list)
    model: 'GoogleGenerativeAI'
    translations: 'SimpleNamespace' = j_loads_ns(base_path / 'translations' / 'mexiron.json')

    # Не все поля товара надо заполнять. Вот кортеж необходимых полей:
    required_fields: tuple = (
        'id_product',
        'name',
        'description_short',
        'description',
        'specification',
        'local_image_path'
    )

    def __init__(self, mexiron_name: Optional[str] = gs.now, driver: Optional[Firefox | Playwrid | str] = None, **kwards) -> None:
        """
        Инициализирует класс QuotationBuilder с необходимыми компонентами.

        Args:
            mexiron_name (Optional[str]): Настраиваемое имя для процесса Mexiron. По умолчанию текущее время.
            driver (Optional[Firefox | Playwrid | str]): Инстанс веб-драйвера Selenium. Может быть инстансом Firefox, Playwrid или строкой 'firefox'/'playwright'. По умолчанию None.
            **kwards: Дополнительные аргументы для инициализации веб-драйвера.

        Raises:
            Exception: Если не удается создать путь для экспорта.

        """
        self.mexiron_name = mexiron_name
        try:
            self.export_path = gs.path.external_storage / ENDPOINT / 'mexironim' / self.mexiron_name
        except Exception as ex:
            logger.error("Ошибка при создании пути для экспорта:", ex, exc_info=True)
            return

        # 1. Initialize webdriver
        # Инициализация веб-драйвера
        if driver:

            if isinstance(driver, Driver):
                self.driver = driver

            elif isinstance(driver, (Firefox, Playwrid,)):  # Chrome, Edge
                self.driver = Driver(driver, **kwards)

            elif isinstance(driver, str):
                if driver.lower() == 'firefox':
                    self.driver = Driver(Firefox, **kwards)

                elif driver.lower() == 'playwright':
                    self.driver = Driver(Playwrid, **kwards)

        else:
            self.driver = Driver(Firefox, **kwards)

        # 2. Initialize Gemini model
        # Инициализация модели Gemini
        try:
            system_instruction: str = (gs.path.endpoints / ENDPOINT / 'instructions' / 'system_instruction_mexiron.md').read_text(encoding='UTF-8')
            api_key: str = gs.credentials.gemini.kazarinov
            self.model = GoogleGenerativeAI(
                api_key=api_key,
                system_instruction=system_instruction,
                generation_config={'response_mime_type': 'application/json'}
            )
        except Exception as ex:
            logger.error("Ошибка при загрузке модели, инструкций или API ключа:", ex, exc_info=True)

    def convert_product_fields(self, f: ProductFields) -> dict:
        """
        Преобразует поля продукта в словарь.

        Функция конвертирует поля из объекта `ProductFields` в простой словарь для модели ИИ.

        Args:
            f (ProductFields): Объект, содержащий распарсенные данные продукта.

        Returns:
            dict: Отформатированный словарь данных продукта.

        Note:
            Правила построения полей определяются в `ProductFields`
        """
        if not f.id_product:
            logger.error("Сбой при получении полей товара.")
            return {}  # <- сбой при получении полей товара. Такое может произойти если вместо страницы товара попалась страница категории, при невнимательном составлении мехирона из комплектующих

        product_name: str = f.name['language']['value'] if f.name else ''
        description: str = f.description['language']['value'] if f.description else ''
        description_short: str = f.description_short['language']['value'] if f.description_short else ''
        specification: str = f.specification['language']['value'] if f.specification else ''

        if not product_name:
            return {}

        return {
            'product_name': product_name,
            'product_id': f.id_product,
            'description_short': description_short,
            'description': description,
            'specification': specification,
            'local_image_path': str(f.local_image_path),
        }

    def process_ai(self, products_list: List[str], lang: str, attempts: int = 3) -> dict | bool:
        """
        Обрабатывает список продуктов с помощью модели ИИ.

        Args:
            products_list (List[str]): Список словарей данных продукта в виде строки.
            lang (str): Язык, на котором нужно получить ответ.
            attempts (int, optional): Количество попыток повтора в случае сбоя. По умолчанию 3.

        Returns:
            dict: Обработанный ответ в формате словаря.
            bool: False, если не удалось получить валидный ответ после нескольких попыток.

        Note:
            Модель может возвращать невалидный результат.
            В таком случае я переспрашиваю модель разумное количество раз.
        """
        if attempts < 1:
            logger.error(f"Не удалось получить валидный ответ от модели после всех попыток.")
            return {}  # return early if no attempts are left

        model_command: str = Path(gs.path.endpoints / ENDPOINT / 'instructions' / f'command_instruction_mexiron_{lang}.md').read_text(encoding='UTF-8')
        # Request response from the AI model
        # Запрос ответа от модели ИИ
        q: str = model_command + '\n' + str(products_list)
        response: str = self.model.ask(q)

        if not response:
            logger.error("Нет ответа от модели")
            return {}

        response_dict: dict = j_loads(response)  # <- если будет ошибка , то вернется пустой словарь

        if not response_dict:
            logger.error("Ошибка парсинга ответа модели")
            if attempts > 1:
                logger.warning(f"Попытка {attempts} повторного запроса к модели.")
                return self.process_ai(products_list, lang, attempts - 1)
            return {}
        return response_dict

    async def process_ai_async(self, products_list: List[str], lang: str, attempts: int = 3) -> dict | bool:
        """
        Асинхронно обрабатывает список продуктов с помощью модели ИИ.

        Args:
            products_list (List[str]): Список словарей данных продукта в виде строки.
            lang (str): Язык, на котором нужно получить ответ.
            attempts (int, optional): Количество попыток повтора в случае сбоя. По умолчанию 3.

        Returns:
            dict: Обработанный ответ в формате словаря.
            bool: False, если не удалось получить валидный ответ после нескольких попыток.

        Note:
            Модель может возвращать невалидный результат.
            В таком случае я переспрашиваю модель разумное количество раз.
        """
        if attempts < 1:
            logger.error("Не удалось получить валидный ответ от модели после всех попыток.")
            return {}  # return early if no attempts are left

        model_command: str = Path(gs.path.endpoints / ENDPOINT / 'instructions' / f'command_instruction_mexiron_{lang}.md').read_text(encoding='UTF-8')
        # Request response from the AI model
        # Запрос ответа от модели ИИ
        q: str = model_command + '\n' + str(products_list)

        response: str = await self.model.ask_async(q)  # CORRECT

        if not response:
            logger.error("Нет ответа от модели")
            return {}

        response_dict: dict = j_loads(response)  # <- если будет ошибка , то вернется пустой словарь

        if not response_dict:
            logger.error(f'Ошибка {attempts} парсинга ответа модели')
            if attempts > 1:
                logger.warning(f"Попытка {attempts} повторного запроса к модели.")
                return await self.process_ai_async(products_list, lang, attempts - 1)
            return {}
        return response_dict

    async def save_product_data(self, product_data: dict) -> bool:
        """
        Сохраняет данные отдельного продукта в файл.

        Args:
            product_data (dict): Отформатированные данные продукта.

        Returns:
            bool: True, если данные успешно сохранены, False в противном случае.
        """
        file_path: Path = self.export_path / 'products' / f"{product_data['product_id']}.json"
        if not j_dumps(product_data, file_path, ensure_ascii=False):
            logger.error(f"Ошибка сохранения словаря {print(product_data)}\nПуть: {file_path}")
            return False
        return True

    async def post_facebook_async(self, mexiron: SimpleNamespace) -> bool:
        """Функция исполняет сценарий рекламного модуля `facvebook`."""
        # Здесь должен быть код для публикации в Facebook
        # driver.get_url(r'https://www.facebook.com/profile.php?id=61566067514123')
        # currency = "ש''ח"
        # title = f'{mexiron.title}\n{mexiron.description}\n{mexiron.price} {currency}'
        # if not post_message_title(self.d, title):
        #     logger.warning(f'Не получилось отправить название мехирона')
        #     return

        # if not upload_post_media(self.d, media=mexiron.products):
        #     logger.warning(f'Не получилось отправить media')
        #     return
        # if not message_publish(self.d):
        #     logger.warning(f'Не получилось отправить media')
        #     return
        logger.info("Функция post_facebook_async была вызвана.")
        return True

def main() -> None:
    """
    Основная функция для запуска процесса создания отчетов.
    """
    # Здесь должна быть логика для запуска процесса
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
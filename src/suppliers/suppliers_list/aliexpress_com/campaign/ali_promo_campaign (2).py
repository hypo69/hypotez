## \file /src/suppliers/aliexpress/campaign/ali_promo_campaign (2).py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.campaign 
	:platform: Windows, Unix
	:synopsis:

"""


"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
  :platform: Windows, Unix

"""
"""
  :platform: Windows, Unix
  :platform: Windows, Unix
  :synopsis:
"""
  
""" module: src.suppliers.suppliers_list.aliexpress_com.campaign """



"""
@dotfile suppliers/aliexpress/campaigns/_dot/aliexpress_campaign.dot

## AliPromoCampaign

### Назначение:
Модуль предназначен для управления рекламными кампаниями на платформе AliExpress, включая обработку данных о категориях и товарах, создание и редактирование JSON-файлов с информацией о кампаниях, а также использование AI для генерации данных о кампаниях.

### Описание:
Класс `AliPromoCampaign` позволяет загружать и обрабатывать данные рекламных кампаний, управлять категориями и товарами, а также использовать ИИ для генерации описаний и других данных. Модуль поддерживает различные языки и валюты, обеспечивая гибкость в настройке кампаний.

### Примеры:
Пример инициализации рекламной кампании:

    >>> campaign = AliPromoCampaign("new_campaign", "EN", "USD")
    >>> print(campaign.campaign_name)

Пример обработки всей кампании:

    >>> campaign = AliPromoCampaign("new_campaign", "EN", "USD")
    >>> campaign.process_campaign()

Пример обработки данных о товарах в категории:

    >>> campaign = AliPromoCampaign("new_campaign", "EN", "USD")
    >>> products = campaign.process_category_products("electronics")

Пример заполнения данных категорий с использованием AI:

    >>> campaign = AliPromoCampaign("new_campaign", "EN", "USD")
    >>> campaign.fill_cat_json()
"""

import header
import time
import json
import copy
from pathlib import Path
from types import SimpleNamespace
from typing import List, Optional, Dict, Union
from src.suppliers.suppliers_list.aliexpress import campaign

from src.suppliers.suppliers_list.apiexpress.affiliated_products_generator import AliAffiliatedProducts
from src.goog.gemini import GoolgeGenerativeAI
from src.logger.logger import logger
from src import gs
from src.utils.file import get_filenames, read_text_file
from src.utils.file.file import get_directory_names
from src.utils.jjson import j_dumps, j_loads_ns, j_loads
from src.utils.convertors import csv2dict
from src.utils.printer import pprint
from src.suppliers.suppliers_list.aliexpress_com.campaign.html_generators import (
    ProductHTMLGenerator,
    CategoryHTMLGenerator,
    CampaignHTMLGenerator,
)
from src.suppliers.suppliers_list.aliexpress_com.utils.extract_product_id import extract_prod_ids
from src.logger.logger import logger

class AliPromoCampaign:
    """Управление рекламной кампанией."""

    # Class attributes declaration
    language: str
    currency: str
    base_path: Path
    campaign_name: str
    campaign: SimpleNamespace
    campaign_ai: SimpleNamespace
    campaign_ai_file_name: str
    locale: str  # <- EN_USD

    def __init__(
        self,
        campaign_name: str,
        language: Optional[str] = None,
        currency: Optional[str] = None,
        campaign_file: Optional[str | Path] = None,
    ):
        """Инициализация и возвращение объекта SimpleNamespace для кампании.

        Args:
            campaign_file (Optional[str | Path]): Путь к файлу кампании или ссылка для загрузки кампании.
            campaign_name (Optional[str]): Название кампании.
            language (Optional[str | dict]): Язык, Используетсяый в кампании.
            currency (Optional[str]): Валюта, Используетсяая в кампании.

        Returns:
            SimpleNamespace: Объект, представляющий кампанию.



        Example:
        # Есть два способа инициализации класса

        # 1. через имя, язык и валюту рекламной кампании
            >>> campaign = AliPromoCampaign(campaign_name="SummerSale", language="EN", currency="USD")
            >>> print(campaign.campaign_name)
            SummerSale
        # 2. через файл рекламной кампании:
            >>> campaign = AliPromoCampaign(campaign_name="SummerSale", campaign_file="EN_USD.JSON")
            >>> print(campaign.campaign_name)
            SummerSale
        """
        ...
        self.base_path = gs.path.google_drive / "aliexpress" / "campaigns" / campaign_name
        campaign_file_path = (
            self.base_path / f"{language}_{currency}.json"
            if not campaign_file
            else self.base_path / campaign_file
        )
        self.campaign = j_loads_ns(campaign_file_path, exc_info=False)
        if not self.campaign:
            logger.critical(f"Campaign file not found at {campaign_file_path=}")
            return

        self.language, self.currency = self.campaign.language, self.campaign.currency

        self.campaign_ai = copy.copy(self.campaign)
        # self.campaign.category = {}
        self.campaign_ai_file_name = f"{language}_{currency}_AI_{gs.now}.json"
        """ 
        Тodo:
            Загружать объект `campaign_ai` из файла.
            Сейчас я каждый запуск создаю новый файл. Это неплохо - модель каждый раз генерирует новы ответы
        """

    def process_camapign(self):
        """Функция итерируется по категориям рекламной кампании и обрабатывает товары категории через генератор партнерских ссылок.

        Example:
            >>> campaign.process_camapign()
        """
        ...
        for category_ns in self.campaign.category:
            self.process_category_products(category_ns.category_name)
            self.process_llm_category(category_ns.category_name)

    def process_llm_campaign_properties(self):
        """ Установка значений `title`, `description` для заголовка реклмной кампании """
        ...

    def process_llm_category(self, category_name: Optional[str] = None):
        """Обработка AI кампании для указанной категории или всех категорий.

        Args:
            category_name (Optional[str]): Имя категории для обработки. Если не указано, будут обработаны все категории.

        Example:
            >>> campaign.process_llm_campaign("Electronics")
            >>> campaign.process_llm_campaign()
        """
        ...
        _base_path = gs.path.src / "suppliers" / "aliexpress" / "campaign" / "prompts"
        prompt_path = _base_path / "fill_and_translate_aliexpress_campaign.json"
        prompt: SimpleNamespace = j_loads_ns(prompt_path)

        system_instruction_path = (
            _base_path / prompt.generate_campaign_details.system_instruction
        )
        system_instruction: str = read_text_file(system_instruction_path)

        model = GoolgeGenerativeAI(system_instruction=system_instruction)


        def _process_category(category_name: str, attempts:int = 5):
            """Process AI-generated category data and update campaign category.

            Args:
                category_name (str): The name of the category to process.

            This function reads product titles for the given category, generates a prompt
            for the AI model, and updates the corresponding category in the campaign.

            Example:
                >>> process_llm_category('Electronics')
            """
            titles_path:Path = self.base_path / 'category' / category_name / f"{self.language}_{self.currency}" / 'product_titles.txt'
            product_titles = read_text_file(titles_path, get_list=True)
            prompt = f"language={self.language}\ncategory_name={category_name}\nproduct_titles={product_titles}"

            def get_response(_attempts:int=5):
                try:
                    response = model.ask(
                        prompt
                    )  # Ожидается, что модель вернет словарь в формате JSON
                    return response
                except Exception as ex:
                    logger.error("Google GoolgeGenerativeAI error:", ex, exc_info= False)
                    time.sleep(15) # GoolgeGenerativeAI позволяет max 5 запросов в минуту
                    if _attempts > 0:
                        get_response(_attempts - 1)
                    return

            response = get_response()
            if not response:
                return
            try:
                res: dict = j_loads(response)
                # Проверка, существует ли уже такая категория
                if hasattr(self.campaign.category, category_name):
                    # Обновление существующей категории
                    current_category = getattr(self.campaign.category, category_name)
                    for key, value in res.items():
                        setattr(current_category, key, value)
                else:
                    # Добавление новой категории
                    setattr(self.campaign.category, category_name, SimpleNamespace(**res))
            except Exception as ex:
                logger.error(f"Error updating campaign for {category_name=}:", ex, exc_info=False)

        if category_name:
            _process_category(category_name)
        else:
            for category_name, _ in vars(self.campaign.category).items():
                _process_category(category_name)

        j_dumps(self.campaign_ai, self.base_path / "ai" / self.campaign_ai_file_name)

    def process_new_campaign(
        self,
        campaign_name: Optional[str] = None,
        language: Optional[str] = None,
        currency: Optional[str] = None,
    ):
        """Обработка всей кампании для всех категорий.

        Args:
            campaign_name (Optional[str]): Название рекламной кампании.
            language (Optional[str]): Язык для кампании (необязательно).
            currency (Optional[str]): Валюта для кампании (необязательно).

        Returns:
            List[Tuple[str, Any]]: Список кортежей с именами категорий и их обработанными результатами.

        Example:
            >>> campaign.process_new_campaign(campaign_name="HolidaySale", language="RU", currency="ILS")
        """
        campaign_name = campaign_name if campaign_name else "default_campaign"
        _base_dir = Path(gs.path.google_drive / "aliexpress" / "campaigns" / campaign_name)
        aliexpress_campaign_categories_dirs = get_directory_names(
            _base_dir / "category"
        )

        # Define default language and currency mappings
        language_files = {"EN": "USD", "RU": "ILS", "HE": "ILS"}

        # If specific language and currency are provided, update the mapping
        if language and currency:
            language_files = {language: currency}

        # Create JSON files for each language and currency
        for lang, curr in language_files.items():
            file_path = _base_dir / f"{self.locale}.json"

            campaign_data = {
                "campaign_name": campaign_name,
                "title": "",
                "language": self.locale,
                "currency": self.currency,
                "description": "",
                "category": {},
            }

            j_dumps(campaign_data, file_path)

        results = []
        categories = self.set_categories_from_directories()

        # Process each category for each language and currency
        for category_name in categories:
            for lang, curr in language_files.items():
                self.process_category_products(campaign_name, category_name, lang, curr)

    def process_category_products(
        self, category_name: str
    ) -> Optional[List[SimpleNamespace]]:
        """Обработка товаров в конкретной категории.

        Args:
            category_name (str): Имя категории.

        Returns:
            Optional[List[SimpleNamespace]]: Список объектов SimpleNamespace, представляющих товары.

        Example:
            >>> products:list[SimpleNamspace] = campaign.process_category_products("Electronics")
            >>> print(len(products))
            20
            >>> for product in products[0]:
            >>> pprint(product)  # pprint function from src.utils.pprint
            Todo:
                Сделать распечатку ключей товара
        """
        ...

        def read_sources(category_name: str) -> Optional[List[str]]:
            product_ids = []
            html_files = get_filenames(
                self.base_path / "category" / category_name / "sources",
                extensions=".html",
                exc_info=False,
            )
            if html_files:
                product_ids.extend(extract_prod_ids(html_files))
            product_urls = read_text_file(
                self.base_path / "category" / category_name / "sources.txt",
                get_list=True,
                exc_info=False,
            )

            if product_urls:
                _ = extract_prod_ids(product_urls)
                product_ids.extend(_)
            if not product_ids:
                return
            return product_ids

        ...

        prod_ids = read_sources(category_name)

        if not prod_ids:
            logger.error(
                f"No products found in category {category_name}/{self.language}_{self.currency}."
            )
            ...
            return
        promo_generator = AliAffiliatedProducts(
            language=self.language, currency=self.currency
        )
        affiliated_products = promo_generator.process_affiliate_products(
            campaign=self.campaign, category_name=category_name, prod_ids=prod_ids
        )

        if not affiliated_products:
            logger.error(f"No affiliated products found.")
            return

        self.process_llm_campaign(category_name)
        return affiliated_products

    def get_category_products(
        self, category_name: str
    ) -> Optional[List[SimpleNamespace]]:
        """Чтение данных о товарах из JSON файлов для конкретной категории.

        Args:
            category_name (str): Имя категории.

        Returns:
            Optional[List[SimpleNamespace]]: Список объектов SimpleNamespace, представляющих товары.

        Example:
            >>> products = campaign.get_category_products("Electronics")
            >>> print(len(products))
            15
        """
        category_path = (
            self.base_path
            / "category"
            / category_name
            / f"{self.language}_{self.currency}"
        )
        json_filenames = get_filenames(category_path, extensions="json")
        products = []

        if json_filenames:
            for json_filename in json_filenames:
                product_data = j_loads_ns(category_path / json_filename)
                product = SimpleNamespace(**vars(product_data))
                products.append(product)
            return products
        else:
            logger.error(
                f"No JSON files found for {category_name=} at {category_path=}.\nStart prepare category"
            )
            self.process_category_products(category_name)
            return

    def dump_category_products_files(
        self, category_name: str, products: List[SimpleNamespace]
    ):
        """Сохранение данных о товарах в JSON файлы.

        Args:
            category_name (str): Имя категории.
            products (List[SimpleNamespace]): Список объектов SimpleNamespace, представляющих товары.

        Example:
            >>> campaign.dump_category_products_files("Electronics", products)
        """
        if not products:
            logger.warning("No products to save.")
            return

        category_path = Path(self.base_path / "category" / category_name)
        for product in products:
            product_id = getattr(product, "product_id", None)
            if not product_id:
                logger.warning(f"Skipping product without product_id: {product}")
                continue
            j_dumps(product, category_path / f"{product_id}.json")

    def set_categories_from_directories(self):
        """Устанавливает категории рекламной кампании из названий директорий в `category`.

        Преобразует каждый элемент списка категорий в объект `SimpleNamespace` с атрибутами
        `category_name`, `title`, и `description`.

        Example:
            >>> self.set_categories()
            >>> print(self.campaign.category[0].category_name)
        """
        ...
        category_dirs = self.base_path / "category"
        categories = get_directory_names(category_dirs)

        # Преобразуем каждый элемент списка категорий в объект SimpleNamespace
        self.campaign.category = [
            SimpleNamespace(category_name=category, title="", description="")
            for category in categories
        ]

    def generate_html_for_campaign(self, campaign_name: str):
        """Генерирует HTML-страницы для рекламной кампании.

        Args:
            campaign_name (str): Имя рекламной кампании.

        Example:
            >>> campaign.generate_html_for_campaign("HolidaySale")
        """
        campaign_root = Path(gs.path.google_drive / "aliexpress" / "campaigns" / campaign_name)
        categories = get_filenames(campaign_root / "category", extensions="")

        # Генерация HTML страниц для каждой категории
        for category_name in categories:
            category_path = campaign_root / "category" / category_name
            products = self.get_category_products(category_name=category_name)

            if products:
                # Генерация страниц для каждого товара
                for product in products:
                    ProductHTMLGenerator.set_product_html(product, category_path)

                # Генерация страницы категории
                CategoryHTMLGenerator.set_category_html(products, category_path)
            else:
                logger.warning(f"No products found for category {category_name}.")

        # Генерация страницы рекламной кампании
        CampaignHTMLGenerator.set_campaign_html(categories, campaign_root)

### **Анализ кода модуля `ali_promo_campaign.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Хорошая структурированность кода с разделением на методы для выполнения различных задач.
    - Наличие docstring для большинства функций и методов.
    - Использование `logger` для логирования.
- **Минусы**:
    - Не везде есть аннотации типов.
    - Отсутствуют примеры использования в некоторых docstring.
    - Местами docstring на английском языке.
    - Не все docstring соответствуют требуемому формату.
    - Местами отсутствует логирование ошибок.

#### **Рекомендации по улучшению**:
1. **Документация**:
    - Перевести все docstring на русский язык и привести к требуемому формату.
    - Добавить примеры использования для всех функций и методов, где это возможно.
    - Уточнить и дополнить описания параметров и возвращаемых значений.
2. **Типизация**:
    - Добавить аннотации типов для всех переменных и параметров функций, где это отсутствует.
3. **Логирование**:
    - Добавить обработку исключений и логирование ошибок в тех местах, где это отсутствует.
    - Использовать `logger.error(f"Описание ошибки: ", ex, exc_info=True)` для более подробного логирования.
4. **Комментарии**:
    - Уточнить и дополнить комментарии, чтобы они более точно описывали назначение кода.
    - Избегать расплывчатых формулировок, таких как "получаем" или "делаем".
5. **Использование констант**:
    - Вынести часто используемые пути к файлам и идентификаторы ассистентов в константы для удобства изменения и поддержки.
6. **Рефакторинг**:
    - Упростить логику обработки категорий в методе `process_llm_category`.
    - Разбить большие методы на более мелкие и переиспользовать их.
7. **Обработка ошибок**:
    - Добавить обработку ошибок при чтении файлов и директорий.
8. **Прочее**:
   - Избавиться от `Union` заменив их на `|`.
   - Использовать `ex` вместо `e` в блоках обработки исключений.
   - Использовать одинарные кавычки (`\'`) в Python-коде.

#### **Оптимизированный код**:

```python
## \file /src/suppliers/aliexpress/campaign/ali_promo_campaign.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для управления рекламными кампаниями на платформе AliExpress
==================================================================

Модуль предназначен для управления рекламными кампаниями на платформе AliExpress, включая обработку данных о категориях и товарах,
создание и редактирование JSON-файлов с информацией о кампаниях, а также использование AI для генерации данных о кампаниях.

Класс `AliPromoCampaign` позволяет загружать и обрабатывать данные рекламных кампаний, управлять категориями и товарами,
а также использовать ИИ для генерации описаний и других данных. Модуль поддерживает различные языки и валюты,
обеспечивая гибкость в настройке кампаний.

Пример использования:
----------------------

>>> campaign = AliPromoCampaign("new_campaign", "EN", "USD")
>>> print(campaign.campaign_name)

>>> campaign.process_campaign()

>>> products = campaign.process_category_products("electronics")

>>> campaign.process_llm_category("Electronics")
"""

import asyncio
import copy
import html
import time
from pathlib import Path
from types import SimpleNamespace
from typing import List, Optional, Dict

from src import gs
from src.suppliers.suppliers_list.aliexpress import campaign
from src.suppliers.suppliers_list.aliexpress.affiliated_products_generator import AliAffiliatedProducts
from src.suppliers.suppliers_list.aliexpress.utils import locales
from src.ai.gemini import GoogleGenerativeAi
from src.ai.openai import OpenAIModel
from src.suppliers.suppliers_list.aliexpress.campaign.html_generators import (
    ProductHTMLGenerator,
    CategoryHTMLGenerator,
    CampaignHTMLGenerator,
)
from src.logger.logger import logger

from src.utils.file import (read_text_file,
                        get_filenames_from_directory,
                        get_directory_names,
                        )
from src.utils.jjson import j_dumps, j_loads_ns, j_loads
from src.utils.convertors.csv import csv2dict
from src.utils.file import save_text_file
from src.utils.printer import pprint

from src.suppliers.suppliers_list.aliexpress.utils.extract_product_id import extract_prod_ids
from src.logger.logger import logger

class AliPromoCampaign:
    """Управление рекламной кампанией."""

    # Class attributes declaration
    language: str = None
    currency: str = None
    base_path: Path = None
    campaign_name: str = None
    campaign: SimpleNamespace = None
    campaign_ai: SimpleNamespace = None
    gemini: GoogleGenerativeAi = None
    openai: OpenAIModel = None

    def __init__(
        self,
        campaign_name: str,
        language: Optional[str] = None,
        currency: Optional[str] = None,
        model:str = 'openai'
    ):
        """Инициализация объекта AliPromoCampaign для рекламной кампании.

        Args:
            campaign_name (str): Название кампании.
            language (Optional[str]): Язык, используемый в кампании.
            currency (Optional[str]): Валюта, используемая в кампании.
            model (str): Модель ИИ для использования. По умолчанию 'openai'.

        Returns:
            None

        Example:
            >>> campaign = AliPromoCampaign(campaign_name="SummerSale", language="EN", currency="USD")
            >>> print(campaign.campaign_name)

        """
        self.campaign_name = campaign_name
        self.language = language
        self.currency = currency
        self.model = model

        self.base_path = gs.path.google_drive / "aliexpress" / "campaigns" / campaign_name
        campaign_file_path = self.base_path / f"{language}_{currency}.json"

        self.campaign = j_loads_ns(campaign_file_path, exc_info=False)
        # Если файла кампании нет, запускается процесс создания новой кампании
        if not self.campaign:
            logger.warning(
                f"Campaign file not found at {campaign_file_path=}\\nStart as new \\n (Start build JSON file, categories, products etc.)"
            )
            # Если в корне рекламной кампании нет файла JSON -> запускается процесс создания новой реклмной кампании
            # создадутся категории из названий директорий ц директории `catergorry`,
            # соберутся affiliated товары в файлы <product_id>.JSON
            # сгенеририуется ai параметры
            self.process_new_campaign(
                campaign_name=campaign_name, language=language, currency=currency
            )  # <- создание новой рекламной кампании
            return

        if self.campaign.language and self.campaign.currency:
            self.language, self.currency = (
                self.campaign.language,
                self.campaign.currency,
            )
        else:
            self.language, self.currency = language, currency

        #self.campaign_ai = copy.copy(self.campaign)
        self._models_payload()


    def _models_payload(self) -> None:
        """Инициализация моделей ИИ (Gemini, OpenAI) с системными инструкциями."""
        #self.campaign_ai_file_name = f"{self.language}_{self.currency}_{model}_{gs.now}.json"
        system_instruction_path: Path = gs.path.src / 'ai' / 'prompts' / 'aliexpress_campaign' / 'system_instruction.txt'
        system_instruction: str = read_text_file(system_instruction_path)
        #self.model = OpenAIModel(system_instruction=system_instruction,
        #                         assistant_id = gs.credentials.openai.assistant.category_descriptions)
        self.gemini = GoogleGenerativeAi(system_instruction = system_instruction)
        assistant_id: str = "asst_dr5AgQnhhhnef5OSMzQ9zdk9" # <-  задача asst_dr5AgQnhhhnef5OSMzQ9zdk9 создание категорий и описаний на основе списка названий товаров
        #self.openai = OpenAIModel(system_instruction = system_instruction, assistant_id = assistant_id)

    def process_campaign(self) -> None:
        """Итерируется по категориям рекламной кампании и обрабатывает товары категории через генератор партнерских ссылок.

        Example:
            >>> campaign.process_campaign()
        """
        categories_names_list: list[str] = get_directory_names(self.base_path / 'category') # читаю название папок категорий
        for category_name in categories_names_list:
            logger.info(f"Starting {category_name=}")
            self.process_category_products(category_name)
            logger.info(f"Starting AI category")
            self.process_llm_category(category_name)
            ...


    def process_campaign_category(
        self, category_name: str
    ) -> list[SimpleNamespace] | None:
        """Обрабатывает конкретную категорию кампании для всех языков и валют.

        Args:
            category_name (str): Категория для кампании.

        Returns:
            List[SimpleNamespace] | None: Список наименований товаров в категории.
        """
        # Process category products and get the list of products
        self.process_category_products(category_name=category_name)
        self.process_llm_category(category_name=category_name)

    def process_new_campaign(
        self,
        campaign_name: str,
        language: Optional[str] = None,
        currency: Optional[str] = None,
    ) -> None:
        """Создает новую рекламную кампанию.

        Условия для создания кампании:
        - директория кампании с питоник названием
        - вложенная директория `campaign`, в ней директории с питоник названиями категорий
        - файл sources.txt и/или директория `sources` с файлами `<product)id>.html`

        Args:
            campaign_name (str): Название рекламной кампании.
            language (Optional[str]): Язык для кампании (необязательно).
            currency (Optional[str]): Валюта для кампании (необязательно).

        Returns:
            None

        Example:
            >>> campaign.process_new_campaign(campaign_name="HolidaySale", language="RU", currency="ILS")

        Flowchart:
        ┌──────────────────────────────────────────────┐
        │ Start                                        │
        └──────────────────────────────────────────────┘
                          │
                          ▼
        ┌───────────────────────────────────────────────┐
        │ Check if `self.language` and `self.currency`  │
        │ are set                                       │
        └───────────────────────────────────────────────┘
                          │
                ┌─────────┴──────────────────────────┐
                │                                    │
                ▼                                    ▼
        ┌─────────────────────────────┐   ┌──────────────────────────────────────┐
        │Yes: `locale` = `{language:  │   │No: `locale` = {                      │
        │currency}`                   │   │     "EN": "USD",                     │
        │                             │   │     "HE": "ILS",                     │
        │                             │   │     "RU": "ILS"                      │
        │                             │   │    }                                 │
        └─────────────────────────────┘   └──────────────────────────────────────┘
                         │                         │
                         ▼                         ▼
        ┌───────────────────────────────────────────────┐
        │ For each `language`, `currency` in `locale`:  │
        │ - Set `self.language`, `self.currency`        │
        │ - Initialize `self.campaign`                  │
        └───────────────────────────────────────────────┘
                         │
                         ▼
        ┌───────────────────────────────────────────────┐
        │ Call `self.set_categories_from_directories()` │
        │ to populate categories                        │
        └───────────────────────────────────────────────┘
                         │
                         ▼
        ┌───────────────────────────────────────────────┐
        │ Copy `self.campaign` to `self.campaign_ai`    │
        │ and set `self.campaign_ai_file_name`          │
        └───────────────────────────────────────────────┘
                         │
                         ▼
        ┌───────────────────────────────────────────────┐
        │ For each `category_name` in campaign:         │
        │ - Call `self.process_category_products`       │
        │ - Call `self.process_llm_category`             │
        └───────────────────────────────────────────────┘
                         │
                         ▼
        ┌──────────────────────────────────────────────┐
        │ End                                          │
        └──────────────────────────────────────────────┘

        """
        if not language and not currency:
            # Process all locales if language or currency is not provided
            _l: list[tuple[str, str]] = [(lang, curr) for locale in locales for lang, curr in locale.items()]
        else:
            _l: list[tuple[str, str]] = [(language, currency)]

        for language, currency in _l:
            self.language, self.currency = language, currency
            self.campaign = SimpleNamespace(
                **{\
                    "campaign_name": campaign_name,\
                    "title": "",\
                    "language": language,\
                    "currency": currency,\
                    "description": "",\
                    "category": SimpleNamespace(),\
                }\
            )

            self.set_categories_from_directories()
            self.campaign_ai = copy.copy(
                self.campaign
            )  # <- паралельно создаю ai кампанию
            self.campaign_ai_file_name = f"{language}_{currency}_AI_{gs.now}.json"
            for category_name in self.campaign.category.__dict__:
                self.process_category_products(category_name)

                self.process_llm_category(category_name)
                j_dumps(
                    self.campaign_ai,
                    self.base_path / f"{self.language}_{self.currency}.json",
                )  # <- в вновь созданный файл категорий

    def process_llm_category(self, category_name: Optional[str] = None) -> None:
        """Обрабатывает AI-данные для указанной категории или для всех категорий кампании.

        Args:
            category_name (Optional[str]): Название категории для обработки. Если не указано, обрабатываются все категории.

        Returns:
            None

        Example:
            >>> campaign.process_llm_category("Electronics")
            >>> campaign.process_llm_category()

        Flowchart:
        ┌──────────────────────────────────────────────┐
        │ Start                                        │
        └──────────────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────────────┐
        │ Load system instructions from JSON file       │
        └───────────────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────────────┐
        │ Initialize AI model with system instructions  │
        └───────────────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────────────┐
        │ Check if `category_name` is provided          │
        └───────────────────────────────────────────────┘
                            │
            ┌─────────────────┴───────────────────┐
            │                                     │
            ▼                                     ▼
        ┌─────────────────────────────────────┐   ┌────────────────────────────────────┐
        │ Process specified category          │   │ Iterate over all categories        │
        │ - Load product titles               │   │ - Call `_process_category`         │
        │ - Generate prompt                   │   │   for each category                │
        │ - Get response from AI model        │   └────────────────────────────────────┘
        │ - Update or add category            │
        └─────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────────────┐
        │ Save updated campaign data to file            │
        └───────────────────────────────────────────────┘
                            │
                            ▼
        ┌──────────────────────────────────────────────┐
        │ End                                          │
        └──────────────────────────────────────────────┘

        """
        campaign_ai: SimpleNamespace = copy.copy(self.campaign)


        def _process_category(category_name: str) -> None:
            """Обрабатывает AI-сгенерированные данные категории и обновляет категорию кампании."""

            titles_path: Path = (
                self.base_path
                / "category"
                / category_name
                / f"{campaign_ai.language}_{campaign_ai.currency}"
                / "product_titles.txt"
            )
            product_titles: list[str] = read_text_file(titles_path, as_list=True)
            prompt: str = f"language={campaign_ai.language}\\n{category_name=}\\n{product_titles=}"

            if not self.gemini or not self.openai:
                self._models_payload()

            def get_response(_attempts: int = 5) -> str | None:
                """Получает ответ от AI модели."""
                #return [self.gemini.ask(prompt), self.openai.ask(prompt)]
                #gemini_response, openai_response = self.gemini.ask(prompt), self.openai.ask(prompt)
                return self.gemini.ask(prompt)
                ...

            response: str | None = get_response()
            if not response:
                return

            try:
                res_ns: SimpleNamespace = j_loads_ns(response)  # <- превращаю ответ машины в объект SimpleNamespace
                if hasattr(campaign_ai.category, category_name):
                    current_category: SimpleNamespace = getattr(campaign_ai.category, category_name)
                    nested_category_ns: SimpleNamespace = getattr(res_ns, category_name)
                    for key, value in vars(nested_category_ns).items():
                        setattr(current_category, key, fix_json_string(value))
                    logger.debug(f"Category {category_name=} updated", None, False)
                else:
                    setattr(campaign_ai.category, category_name, res_ns)
                    logger.debug(f"Category {category_name=} created")
            except Exception as ex:
                logger.error(f"Error updating campaign for {category_name=}: ", ex, exc_info=True)
                ...

        # if category_name:
        #     if not _process_category(category_name):
        #         return
        # else:
        #     for category_name in vars(campaign_ai.category).keys():
        #         _process_category(category_name)

        for category_name in vars(campaign_ai.category).keys():
            _process_category(category_name)

        j_dumps(campaign_ai, self.base_path / "ai" / f"gemini_{gs.now}_{self.language}_{self.currency}.json")
        return

    def process_category_products(
        self, category_name: str
    ) -> Optional[List[SimpleNamespace]]:
        """Обрабатывает товары в указанной категории.

        Args:
            category_name (str): Название категории.

        Returns:
            Optional[List[SimpleNamespace]]: Список объектов SimpleNamespace, представляющих товары.
            Возвращает `None`, если товары не найдены.

        Example:
            >>> products: List[SimpleNamespace] = campaign.process_category_products("Electronics")
            >>> print(len(products))
            20
            >>> for product in products:
            >>>     pprint(product)  # Use pprint from `src.utils.pprint`

        Notes:
            Функция пытается считать идентификаторы товаров из HTML-файлов и текстовых файлов
            в директории `sources` указанной категории. Если идентификаторы товаров не найдены,
            регистрируется ошибка и функция возвращает `None`.
            Если партнерские товары найдены, они возвращаются; в противном случае регистрируется ошибка
            и функция возвращает `None`.

        Flowchart:
        ┌───────────────────────────────────────────────────────────┐
        │ Start                                                     │
        └───────────────────────────────────────────────────────────┘
                      │
                      ▼
        ┌───────────────────────────────────────────────────────────┐
        │ Call `read_sources(category_name)` to get product IDs     │
        │ - Searches for product IDs in HTML files and sources.txt  │
        └───────────────────────────────────────────────────────────┘
                      │
                      ▼
        ┌───────────────────────────────────────────────────────────┐
        │ Check if `prod_ids` is empty                              │
        │ - If empty, log an error and return `None`                │
        └───────────────────────────────────────────────────────────┘
                      │
                      ▼
        ┌───────────────────────────────────────────────────────────┐
        │ Initialize `AliAffiliatedProducts` with `language`        │
        │ and `currency`                                            │
        └───────────────────────────────────────────────────────────┘
                      │
                      ▼
        ┌───────────────────────────────────────────────────────────┐
        │ Call `process_affiliate_products`                         │
        │ - Pass `campaign`, `category_name`, and `prod_ids`        │
        └───────────────────────────────────────────────────────────┘
                      │
                      ▼
        ┌───────────────────────────────────────────────────────────┐
        │ Check if `affiliated_products` is empty                   │
        │ - If empty, log an error and return `None`                │
        └───────────────────────────────────────────────────────────┘
                      │
                      ▼
        ┌───────────────────────────────────────────────────────────┐
        │ Return `affiliated_products`                              │
        └───────────────────────────────────────────────────────────┘
                      │
                      ▼
        ┌───────────────────────────────────────────────────────────┐
        │ End                                                       │
        └───────────────────────────────────────────────────────────┘

        """

        def read_sources(category_name: str) -> Optional[List[str]]:
            """Считывает источники товаров и извлекает идентификаторы товаров.

            Args:
                category_name (str): Название категории.

            Returns:
                Optional[List[str]]: Список идентификаторов товаров, если найдены; иначе `None`.

            Example:
                >>> product_ids: Optional[List[str]] = read_sources("Electronics")
                >>> print(product_ids)
                ['12345', '67890', ...]

            Notes:
                Эта функция ищет идентификаторы товаров как в HTML-файлах, так и в файле `sources.txt`, расположенном
                в директории `sources` категории. Если идентификаторы товаров не найдены, она возвращает `None`.
            """
            product_ids: list[str] = []
            html_files: list[str] = get_filenames_from_directory(
                self.base_path / "category" / category_name / "sources",
                extensions=".html",
                exc_info=False,
            )
            if html_files:
                product_ids.extend(extract_prod_ids(html_files))
            product_urls: str | None = read_text_file(
                self.base_path / "category" / category_name / "sources.txt",
                as_list = True,
                exc_info = False,
            )

            if product_urls:
                _: list[str] = extract_prod_ids(product_urls)
                product_ids.extend(_)
            if not product_ids:
                return

            return product_ids

        prod_ids: list[str] | None = read_sources(category_name)

        if not prod_ids:
            logger.error(
                f"No products found in category {category_name}/{self.language}_{self.currency}.",
                exc_info=False,
            )
            ...
            return

        promo_generator: AliAffiliatedProducts = AliAffiliatedProducts(
            language = self.language, currency = self.currency
        )

        return asyncio.run(promo_generator.process_affiliate_products(
            prod_ids = prod_ids,\
            category_root = self.base_path
            / "category"
            / category_name,\
        ))\

    def dump_category_products_files(
        self, category_name: str, products: List[SimpleNamespace]
    ) -> None:
        """Сохраняет данные о товарах в JSON файлы.

        Args:
            category_name (str): Имя категории.
            products (List[SimpleNamespace]): Список объектов SimpleNamespace, представляющих товары.

        Example:
            >>> campaign.dump_category_products_files("Electronics", products)
        """
        if not products:
            logger.warning("No products to save.")
            return

        category_path: Path = Path(self.base_path / "category" / category_name)
        for product in products:
            product_id: str | None = getattr(product, "product_id", None)
            if not product_id:
                logger.warning(f"Skipping product without product_id: {product}")
                continue
            j_dumps(product, category_path / f"{product_id}.json")

    def set_categories_from_directories(self) -> None:
        """Устанавливает категории рекламной кампании из названий директорий в `category`.

        Преобразует каждый элемент списка категорий в объект `SimpleNamespace` с атрибутами
        `category_name`, `title`, и `description`.

        Example:
            >>> self.set_categories_from_directories()
            >>> print(self.campaign.category.category1.category_name)
        """
        category_dirs: Path = self.base_path / "category"
        categories: list[str] = get_directory_names(category_dirs)

        # Ensure that self.campaign.category is an object of SimpleNamespace
        if not hasattr(self.campaign, "category"):
            self.campaign.category = SimpleNamespace()

        # Add each category as an attribute to the campaign's category SimpleNamespace
        for category_name in categories:
            setattr(
                self.campaign.category,
                category_name,
                SimpleNamespace(category_name=category_name, title="", description=""),
            )

    async def generate_output(self, campaign_name: str, category_path: str | Path, products_list: list[SimpleNamespace] | SimpleNamespace) -> None:
        """Сохраняет данные о товарах в различных форматах:

        - `<product_id>.json`: Содержит все параметры товара, один файл на товар.
        - `ai_{timestamp}.json`: Общий файл для всех товаров с определенными ключами.
        - `promotion_links.txt`: Список ссылок на товары, создается в функции `save_promotion_links()`.
        - `category_products_titles.json`: Файл, содержащий title, `product_id`, `first_category_name` и `second_category_name`
          для каждого товара в категории.

        Args:
            campaign_name (str): Название кампании для выходных файлов.
            category_path (str | Path): Путь для сохранения выходных файлов.
            products_list (list[SimpleNamespace] | SimpleNamespace): Список товаров или один товар для сохранения.

        Returns:
            None

        Example:
            >>> products_list: list[SimpleNamespace] = [
            ...     SimpleNamespace(product_id="123", product_title="Product A", promotion_link="http://example.com/product_a",
            ...                     first_level_category_id=1, first_level_category_name="Category1",
            ...                     second_level_category_id=2, second_level_category_name="Subcategory1",
            ...                     product_main_image_url="http://example.com/image.png", product_video_url="http://example.com/video.mp4"),
            ...     SimpleNamespace(product_id="124", product_title="Product B", promotion_link="http://example.com/product_b",
            ...                     first_level_category_id=1, first_level_category_name="Category1",
            ...                     second_level_category_id=3, second_level_category_name="Subcategory2",
            ...                     product_main_image_url="http://example.com/image2.png", product_video_url="http://example.com/video2.mp4")
            ... ]
            >>> category_path: Path = Path("/path/to/category")
            >>> await generate_output("CampaignName", category_path, products_list)

        Flowchart:
            ┌───────────────────────────────┐
            │  Start `generate_output`      │
            └───────────────────────────────┘
                        │
                        ▼
            ┌───────────────────────────────┐
            │ Format `timestamp` for file   │
            │ names.                        │
            └───────────────────────────────┘
                        │
                        ▼
            ┌───────────────────────────────┐
            │ Check if `products_list` is   │
            │ a list; if not, convert it to │
            │ a list.                       │
            └───────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │ Initialize `_data_for_openai`,│
        │ `_promotion_links_list`, and  │
        │ `_product_titles` lists.      │
        └───────────────────────────────┘
                        │
                        ▼
    ┌─────────────────────────────────────────┐
    │ For each `product` in `products_list`:  │
    └─────────────────────────────────────────┘
                        │
                        ▼
    ┌───────────────────────────────────────────────┐
    │ 1. Create `categories_convertor` dictionary   │
    │ for `product`.                                │
    └───────────────────────────────────────────────┘
                        │
                        ▼
    ┌───────────────────────────────────────────────┐
    │ 2. Add `categories_convertor` to `product`.   │
    └───────────────────────────────────────────────┘
                        │
                        ▼
    ┌───────────────────────────────────────────────┐
    │ 3. Save `product` as `<product_id>.json`.     │
    └───────────────────────────────────────────────┘
                        │
                        ▼
    ┌───────────────────────────────────────────────┐
    │ 4. Append `product_title` and                 │
    │ `promotion_link` to their respective lists.   │
    └───────────────────────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │ Call `save_product_titles`    │
        │ with `_product_titles` and    │
        │ `category_path`.              │
        └───────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │ Call `save_promotion_links`   │
        │ with `_promotion_links_list`  │
        │ and `category_path`.          │
        └───────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────────┐
        │ Call `generate_html` with         │
        │ `campaign_name`, `category_path`, │
        │ and `products_list`.              │
        └───────────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │  End `generate_output`        │
        └───────────────────────────────┘

        ### Flowchart Description

        1. **Start `generate_output`**: The function begins execution.
        2. **Format `timestamp` for file names**: Generate a timestamp to use in filenames.
        3. **Check if `products_list` is a list**: Ensure that `products_list` is in list format.
        4. **Initialize `_data_for_openai`, `_promotion_links_list`, and `_product_titles` lists**: Prepare empty lists to collect data.
        5. **For each `product` in `products_list`**: Process each product in the list.
        - **Create `categories_convertor` dictionary for `product`**: Create a dictionary for category conversion.
        - **Add `categories_convertor` to `product`**: Attach this dictionary to the product.
        - **Save `product` as `<product_id>.json`**: Save product details in a JSON file.
        - **Append `product_title` and `promotion_link` to their respective lists**: Collect titles and links.
        6. **Call `save_product_titles` with `_product_titles` and `category_path`**: Save titles data to a file.
        7. **Call `save_promotion_links` with `_promotion_links_list` and `category_path`**: Save promotion links to a file.
        8. **Call `generate_html` with `campaign_name`, `category_path`, and `products_list`**: Generate HTML output for products.
        9. **End `generate_output`**: The function completes execution.

        This flowchart captures the key steps and processes involved in the `generate_output` function.

        """
        timestamp: str = datetime.now().strftime("%Y-%m-%d %H%M%S")
        products_list: list[SimpleNamespace] = products_list if isinstance(products_list, list) else [products_list]
        _data_for_openai: dict = {}
        _promotion_links_list: list = []
        _product_titles: list = []

        for product in products_list:
            # Adding the categories_convertor dictionary
            categories_convertor: dict = {
                str(product.first_level_category_id): {
                    "ali_category_name": product.first_level_category_name,
                    "ali_parent": "",
                    "PrestaShop_categories": [],
                    "PrestaShop_main_category": ""
                },\
                str(product.second_level_category_id): {\
                    "ali_category_name": product.second_level_category_name,
                    "ali_parent": str(product.first_level_category_id),
                    "PrestaShop_categories": [],
                    "PrestaShop_main_category": ""
                }\
            }
            product.categories_convertor = categories_convertor

            # Save individual product JSON
            j_dumps(product, Path(category_path / f"{self.language}_{self.currency}" / f"{product.product_id}.json"), exc_info=False)
            _product_titles.append(product.product_title)
            _promotion_links_list.append(product.promotion_link)

        await self.save_product_titles(product_titles=_product_titles, category_path=category_path)
        await self.save_promotion_links(promotion_links=_promotion_links_list, category_path=category_path)
        await self.generate_html(campaign_name=campaign_name, category_path=category_path, products
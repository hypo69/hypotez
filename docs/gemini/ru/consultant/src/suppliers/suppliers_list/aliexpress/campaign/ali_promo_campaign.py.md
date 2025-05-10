### Анализ кода модуля `ali_promo_campaign.py`

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Хорошая структурированность кода, разделение на методы.
  - Наличие документации для большинства функций и классов.
  - Использование логгирования.
  - Попытка следовать принципам DRY (Don't Repeat Yourself).
- **Минусы**:
  - Использование английского языка в docstring и комментариях.
  - Не везде есть подробные описания в docstring.
  - Некоторые функции не имеют аннотации типов.
  - Смешение ответственности в некоторых функциях.
  - Отсутствие обработки исключений в некоторых местах.
  - Не везде используется `logger.error` с передачей исключения.
  - Есть закомментированный код.

**Рекомендации по улучшению:**

1.  **Перевод документации и комментариев на русский язык**:
    - Необходимо перевести все docstring и комментарии на русский язык в формате UTF-8.

2.  **Доработка docstring**:
    - Добавить подробные описания для всех параметров и возвращаемых значений в docstring.
    - Описать возможные исключения (`Raises`).
    - Привести примеры использования (`Example`).

3.  **Аннотация типов**:
    - Добавить аннотации типов для всех аргументов функций и возвращаемых значений, а также для переменных.

4.  **Улучшение обработки исключений**:
    - Использовать `logger.error` с передачей исключения `ex` и `exc_info=True` для более полного логгирования ошибок.
    - Добавить обработку исключений там, где это необходимо.

5.  **Удаление закомментированного кода**:
    - Удалить все закомментированные участки кода, которые не несут полезной информации.

6.  **Использовать одинарные кавычки**:
    - Заменить двойные кавычки на одинарные, где это необходимо.

7.  **Улучшение структуры `process_llm_category`**:

    -   Убрать лишнее копирование `campaign_ai` в начале функции, т.к. это делается внутри `_process_category`.

    -   Устранить дублирование вызова `_process_category` и заменить условной конструкцией, которая была закомментирована.

8.  **Пересмотреть логику `process_new_campaign`**:

    -   Улучшить читаемость кода за счет устранения дублирования логики.

    -   Избавиться от множественного присваивания `self.language, self.currency = ...`.

9.  **Устранить дублирование кода**:

    -   В функции `process_llm_category` код `if not self.gemini or not self.openai: self._models_payload()` можно вынести за пределы функции `_process_category`, чтобы избежать повторного вызова `self._models_payload()` для каждой категории.

**Оптимизированный код:**

```python
## \file /src/suppliers/aliexpress/campaign/ali_promo_campaign.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для управления рекламными кампаниями на платформе AliExpress.
====================================================================

Модуль предназначен для управления рекламными кампаниями на платформе AliExpress,
включая обработку данных о категориях и товарах, создание и редактирование
JSON-файлов с информацией о кампаниях, а также использование AI для генерации
данных о кампаниях.

Модуль содержит класс :class:`AliPromoCampaign`, который позволяет загружать и
обрабатывать данные рекламных кампаний, управлять категориями и товарами, а
также использовать ИИ для генерации описаний и других данных. Модуль
поддерживает различные языки и валюты, обеспечивая гибкость в настройке кампаний.

Пример использования
----------------------

>>> campaign = AliPromoCampaign(campaign_name="new_campaign", language="EN", currency="USD")
>>> print(campaign.campaign_name)

>>> campaign = AliPromoCampaign(campaign_name="new_campaign", language="EN", currency="USD")
>>> campaign.process_campaign()

>>> campaign = AliPromoCampaign(campaign_name="new_campaign", language="EN", currency="USD")
>>> products = campaign.process_category_products("electronics")

>>> campaign = AliPromoCampaign(campaign_name="new_campaign", language="EN", currency="USD")
>>> campaign.process_llm_category("Electronics")

 .. module:: src.suppliers.suppliers_list.aliexpress.campaign
"""

import asyncio
import copy
import html
import time
from pathlib import Path
from types import SimpleNamespace
from typing import List, Optional, Dict, Any, Tuple

from src import gs
from src.suppliers.suppliers_list.aliexpress import campaign
from src.suppliers.suppliers_list.aliexpress.affiliated_products_generator import AliAffiliatedProducts
from src.suppliers.suppliers_list.aliexpress.utils import locales
from src.llm.gemini import GoogleGenerativeAi
from src.llm.openai import OpenAIModel
from src.suppliers.suppliers_list.aliexpress.campaign.html_generators import (
    ProductHTMLGenerator,
    CategoryHTMLGenerator,
    CampaignHTMLGenerator,
)
from src.logger.logger import logger

from src.utils.file import (
    read_text_file,
    get_filenames_from_directory,
    get_directory_names,
)
from src.utils.jjson import j_dumps, j_loads_ns, j_loads
from src.utils.convertors.csv import csv2dict
from src.utils.file import save_text_file
from src.utils.printer import pprint

from src.suppliers.suppliers_list.aliexpress.utils.extract_product_id import extract_prod_ids


class AliPromoCampaign:
    """Класс для управления рекламной кампанией."""

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
        model: str = 'openai'
    ) -> None:
        """
        Инициализация объекта AliPromoCampaign для рекламной кампании.

        Args:
            campaign_name (str): Название кампании.
            language (Optional[str]): Язык, используемый в кампании. По умолчанию None.
            currency (Optional[str]): Валюта, используемая в кампании. По умолчанию None.
            model (str): Модель ИИ для использования. По умолчанию 'openai'.

        Returns:
            None

        Example:
            >>> campaign = AliPromoCampaign(campaign_name="SummerSale", language="EN", currency="USD")
            >>> print(campaign.campaign_name)
        """
        self.base_path = gs.path.google_drive / 'aliexpress' / 'campaigns' / campaign_name
        campaign_file_path = self.base_path / f'{language}_{currency}.json'
        self.campaign = j_loads_ns(
            campaign_file_path, exc_info=False
        )  # Файл может отсутствовать при создании новой рекламной кампании
        if not self.campaign:
            logger.warning(
                f'Файл кампании не найден по пути {campaign_file_path=}\\nНачинаем как новую кампанию \\n(Создание JSON файла, категорий, товаров и т.д.)'
            )
            # Если в корне рекламной кампании нет файла JSON, запускается процесс создания новой рекламной кампании
            # Создаются категории из названий директорий в директории `category`,
            # Собираются affiliated товары в файлы <product_id>.JSON,
            # Генерируются ai параметры
            self.process_new_campaign(
                campaign_name=campaign_name, language=language, currency=currency
            )  # Создание новой рекламной кампании
            return
        if self.campaign.language and self.campaign.currency:
            self.language = self.campaign.language
            self.currency = self.campaign.currency
        else:
            self.language = language
            self.currency = currency

        self._models_payload()

    def _models_payload(self) -> None:
        """
        Загружает параметры для моделей ИИ.

        Инициализирует модели Google Gemini и OpenAI с системными инструкциями.
        """
        system_instruction_path = gs.path.src / 'ai' / 'prompts' / 'aliexpress_campaign' / 'system_instruction.txt'
        system_instruction: str = read_text_file(system_instruction_path)

        self.gemini = GoogleGenerativeAi(system_instruction=system_instruction)
        assistant_id = 'asst_dr5AgQnhhhnef5OSMzQ9zdk9'  # Задача - создание категорий и описаний на основе списка названий товаров
        # self.openai = OpenAIModel(system_instruction = system_instruction, assistant_id = assistant_id)

    def process_campaign(self) -> None:
        """
        Итерируется по категориям рекламной кампании и обрабатывает товары категории.

        Обходит все категории в рекламной кампании и для каждой категории вызывает
        методы `process_category_products` и `process_llm_category`.

        Example:
            >>> campaign.process_campaign()
        """
        categories_names_list = get_directory_names(self.base_path / 'category')  # Читаю название папок категорий
        for category_name in categories_names_list:
            logger.info(f'Начинаем {category_name=}')
            self.process_category_products(category_name)
            logger.info('Начинаем AI category')
            self.process_llm_category(category_name)

    def process_campaign_category(
        self, category_name: str
    ) -> Optional[List[SimpleNamespace]]:
        """
        Обрабатывает указанную категорию в кампании для всех языков и валют.

        Args:
            category_name (str): Категория для кампании.

        Returns:
            Optional[List[SimpleNamespace]]: Список наименований товаров в категории.
        """
        # Обработка товаров категории и получение списка товаров
        self.process_category_products(category_name=category_name)
        self.process_llm_category(category_name=category_name)
        return None

    def process_new_campaign(
        self,
        campaign_name: str,
        language: Optional[str] = None,
        currency: Optional[str] = None,
    ) -> None:
        """
        Создает новую рекламную кампанию.

        Создает структуру директорий и файлов для новой рекламной кампании на основе
        существующих директорий категорий и данных о товарах.

        Условия для создания кампании:
        - директория кампании с понятным названием
        - вложенная директория `campaign`, в ней директории с названиями категорий
        - файл sources.txt и/или директория `sources` с файлами `<product_id>.html`

        Args:
            campaign_name (str): Название рекламной кампании.
            language (Optional[str]): Язык для кампании (необязательно).
            currency (Optional[str]): Валюта для кампании (необязательно).

        Returns:
            None

        Example:
            >>> campaign.process_new_campaign(campaign_name="HolidaySale", language="RU", currency="ILS")
        """
        if language is None and currency is None:
            _l: List[Tuple[str, str]] = [(lang, curr) for locale in locales for lang, curr in locale.items()]
        else:
            _l: List[Tuple[str, str]] = [(language, currency)]

        for language, currency in _l:
            self.language = language
            self.currency = currency
            self.campaign = SimpleNamespace(
                **{
                    'campaign_name': campaign_name,
                    'title': '',
                    'language': language,
                    'currency': currency,
                    'description': '',
                    'category': SimpleNamespace(),
                }
            )

            self.set_categories_from_directories()
            self.campaign_ai = copy.copy(
                self.campaign
            )  # Параллельно создаю ai кампанию
            self.campaign_ai_file_name = f'{language}_{currency}_AI_{gs.now}.json'
            for category_name in self.campaign.category.__dict__:
                self.process_category_products(category_name)

                self.process_llm_category(category_name)
                j_dumps(
                    self.campaign_ai,
                    self.base_path / f'{self.language}_{self.currency}.json',
                )  # В вновь созданный файл категорий

    def process_llm_category(self, category_name: Optional[str] = None) -> None:
        """
        Обрабатывает AI-сгенерированные данные для указанной категории или всех категорий.

        Args:
            category_name (Optional[str]): Название категории для обработки.
                Если не указано, обрабатываются все категории.
        """

        def _process_category(category_name: str) -> None:
            """Обрабатывает AI-сгенерированные данные категории и обновляет категорию кампании."""
            titles_path: Path = (
                self.base_path
                / 'category'
                / category_name
                / f'{self.campaign_ai.language}_{self.campaign_ai.currency}'
                / 'product_titles.txt'
            )
            product_titles: Optional[List[str]] = read_text_file(titles_path, as_list=True)
            if product_titles is None:
                logger.warning(f'Не удалось прочитать названия товаров из файла: {titles_path}')
                return

            prompt: str = f'language={self.campaign_ai.language}\\n{category_name=}\\n{product_titles=}'

            def get_response(_attempts: int = 5) -> Any:
                """Получает ответ от AI модели."""
                # return [self.gemini.ask(prompt), self.openai.ask(prompt)]
                # gemini_response, openai_response = self.gemini.ask(prompt), self.openai.ask(prompt)
                return self.gemini.ask(prompt)

            response: Any = get_response()
            if not response:
                logger.warning(f'Не получен ответ от AI модели для категории: {category_name}')
                return

            try:
                res_ns: SimpleNamespace = j_loads_ns(response)  # Превращаю ответ машины в объект SimpleNamespace
                if hasattr(self.campaign_ai.category, category_name):
                    current_category: SimpleNamespace = getattr(self.campaign_ai.category, category_name)
                    nested_category_ns: SimpleNamespace = getattr(res_ns, category_name)
                    for key, value in vars(nested_category_ns).items():
                        setattr(current_category, key, fix_json_string(value))
                    logger.debug(f'Категория {category_name=} обновлена')
                else:
                    setattr(self.campaign_ai.category, category_name, res_ns)
                    logger.debug(f'Категория {category_name=} создана')
            except Exception as ex:
                logger.error(f'Ошибка при обновлении кампании для {category_name=}: ', ex, exc_info=False)

        # Инициализируем модели, если они еще не инициализированы
        if not self.gemini or not self.openai:
            self._models_payload()

        campaign_ai: SimpleNamespace = copy.copy(self.campaign)

        for category_name in vars(campaign_ai.category).keys():
            _process_category(category_name)

        j_dumps(campaign_ai, self.base_path / 'ai' / f'gemini_{gs.now}_{self.language}_{self.currency}.json')
        return

    def process_category_products(
        self, category_name: str
    ) -> Optional[List[SimpleNamespace]]:
        """
        Обрабатывает товары в указанной категории.

        Args:
            category_name (str): Название категории.

        Returns:
            Optional[List[SimpleNamespace]]: Список объектов SimpleNamespace, представляющих товары.
            Возвращает None, если товары не найдены.

        Example:
            >>> products: List[SimpleNamespace] = campaign.process_category_products("Electronics")
            >>> print(len(products))
            20
            >>> for product in products:
            >>>     pprint(product)  # Используйте pprint из `src.utils.pprint`
        """

        def read_sources(category_name: str) -> Optional[List[str]]:
            """
            Читает источники товаров и извлекает идентификаторы товаров.

            Args:
                category_name (str): Название категории.

            Returns:
                Optional[List[str]]: Список идентификаторов товаров, если найдены; иначе None.

            Example:
                >>> product_ids: Optional[List[str]] = read_sources("Electronics")
                >>> print(product_ids)
                ['12345', '67890', ...]
            """
            product_ids: List[str] = []
            html_files: List[str] | None = get_filenames_from_directory(
                self.base_path / 'category' / category_name / 'sources',
                extensions='.html',
                exc_info=False,
            )
            if html_files:
                product_ids.extend(extract_prod_ids(html_files))
            product_urls: Optional[List[str]] = read_text_file(
                self.base_path / 'category' / category_name / 'sources.txt',
                as_list=True,
                exc_info=False,
            )

            if product_urls:
                _: List[str] = extract_prod_ids(product_urls)
                product_ids.extend(_)
            if not product_ids:
                return None
            return product_ids

        prod_ids: Optional[List[str]] = read_sources(category_name)

        if not prod_ids:
            logger.error(
                f'Товары не найдены в категории {category_name}/{self.language}_{self.currency}.',
                exc_info=False,
            )
            return

        promo_generator: AliAffiliatedProducts = AliAffiliatedProducts(
            language=self.language, currency=self.currency
        )

        return asyncio.run(promo_generator.process_affiliate_products(
            prod_ids=prod_ids,
            category_root=self.base_path
            / 'category'
            / category_name,
        ))

    def dump_category_products_files(
        self, category_name: str, products: List[SimpleNamespace]
    ) -> None:
        """
        Сохраняет данные о товарах в JSON файлы.

        Args:
            category_name (str): Имя категории.
            products (List[SimpleNamespace]): Список объектов SimpleNamespace, представляющих товары.

        Example:
            >>> campaign.dump_category_products_files("Electronics", products)
        """
        if not products:
            logger.warning('Нет товаров для сохранения.')
            return

        category_path: Path = Path(self.base_path / 'category' / category_name)
        for product in products:
            product_id: Any = getattr(product, 'product_id', None)
            if not product_id:
                logger.warning(f'Пропускаем товар без product_id: {product}')
                continue
            j_dumps(product, category_path / f'{product_id}.json')

    def set_categories_from_directories(self) -> None:
        """
        Устанавливает категории рекламной кампании из названий директорий в `category`.

        Преобразует каждый элемент списка категорий в объект `SimpleNamespace` с атрибутами
        `category_name`, `title` и `description`.

        Example:
            >>> self.set_categories_from_directories()
            >>> print(self.campaign.category.category1.category_name)
        """
        category_dirs: Path = self.base_path / 'category'
        categories: List[str] = get_directory_names(category_dirs)

        # Убедитесь, что self.campaign.category является объектом SimpleNamespace
        if not hasattr(self.campaign, 'category'):
            self.campaign.category = SimpleNamespace()

        # Добавьте каждую категорию как атрибут в SimpleNamespace категории кампании
        for category_name in categories:
            setattr(
                self.campaign.category,
                category_name,
                SimpleNamespace(category_name=category_name, title='', description=''),
            )

    async def generate_output(self, campaign_name: str, category_path: str | Path, products_list: list[SimpleNamespace] | SimpleNamespace) -> None:
        """
        Сохраняет данные о товарах в различных форматах:

        - `<product_id>.json`: Содержит все параметры товара, один файл на товар.
        - `ai_{timestamp}.json`: Общий файл для всех товаров с определенными ключами.
        - `promotion_links.txt`: Список ссылок на товары, созданный в функции `save_promotion_links()`.
        - `category_products_titles.json`: Файл, содержащий заголовок, `product_id`, `first_category_name` и `second_category_name` каждого товара в категории.

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
        """
        from datetime import datetime

        timestamp: str = datetime.now().strftime('%Y-%m-%d %H%M%S')
        products_list = products_list if isinstance(products_list, list) else [products_list]
        _data_for_openai: dict = {}
        _promotion_links_list: list = []
        _product_titles: list = []

        for product in products_list:
            # Добавление словаря categories_convertor
            categories_convertor: dict = {
                str(product.first_level_category_id): {
                    'ali_category_name': product.first_level_category_name,
                    'ali_parent': '',
                    'PrestaShop_categories': [],
                    'PrestaShop_main_category': ''
                },
                str(product.second_level_category_id): {
                    'ali_category_name': product.second_level_category_name,
                    'ali_parent': str(product.first_level_category_id),
                    'PrestaShop_categories': [],
                    'PrestaShop_main_category': ''
                }
            }
            product.categories_convertor = categories_convertor

            # Сохранение отдельного JSON файла товара
            j_dumps(product, Path(category_path / f'{self.language}_{self.currency}' / f'{product.product_id}.json'), exc_info=False)
            _product_titles.append(product.product_title)
            _promotion_links_list.append(product.promotion_link)

        await self.save_product_titles(product_titles=_product_titles, category_path=category_path)
        await self.save_promotion_links(promotion_links=_promotion_links_list, category_path=category_path)
        await self.generate_html(campaign_name=campaign_name, category_path=category_path, products_list=products_list)

    async def generate_html(self, campaign_name: str, category_path: str | Path, products_list: list[SimpleNamespace] | SimpleNamespace) -> None:
        """Создает HTML файл для категории и корневой индексный файл.

        Args:
            products_list (list[SimpleNamespace] | SimpleNamespace): Список товаров для включения в HTML.
            category_path (str | Path): Путь для сохранения HTML файла.
        """
        products_list = products_list if isinstance(products_list, list) else [products_list]

        category_name: str = Path(category_path).name
        category_html_path: Path = Path(category_path) / f'{self.language}_{self.currency}' / f'{category_name}.html'

        # Инициализируем словарь категории для хранения названий товаров
        category: dict = {
            'products_titles': []
        }

        html_content: str = f"""<!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{category_name} Products</title>
        <link rel="stylesheet" href="styles.css">
        </head>
        <body>
        <h1>{category_name} Products</h1>
        <div class="product-grid">
        """

        for product in products_list:
            # Добавляем детали товара в products_titles категории
            category['products_titles'].append({
                'title': product.product_title,
                'product_id': product.product_id,
                'first_category_name': product.first_level_category_name,
                'second_category_name': product.second_level_category_name
            })

            html_content += f"""
            <div class="product-card">
            <img src="{product.local_image_path}" alt="{html.escape(product.product_title)}" class="product-image">
            <div class="product-info">
            <h2 class="product-title">{html.escape(product.product_title)}</h2>
            <p class="product-price">{product.target_sale_price} {product.target_sale_price_currency}</p>
            <p class="product-original-price">{product.target_original_price} {product.target_original_price_currency}</p>
            <p class="product-category">Category: {product.second_level_category_name}</p>
            <a href="{product.promotion_link}" class="product-link">Buy Now</a>
            </div>
            </div>
            """

        html_content += """
        </div>
        </body>
        </html>
        """

        # Сохраняем HTML контент
        save_text_file(html_content, category_html_path)

        # Генерируем основной index.html файл
        campaign_path: Path = gs.path.google_drive / 'aliexpress' / 'campaigns' / campaign_name
        campaign_path.mkdir(parents=True, exist_ok=True)
        index_html_path: Path = campaign_path / 'index.html'

        # Собираем все ссылки на категории
        category_links: list = []
        categories: List[str] = get_directory_names(campaign_path / 'category')
        for _category_path in categories:
            category_name = Path(_category_path).name
            category_link = f'{category_name}/{category_name}.html'
            category_links.append(f'<li><a href="{category_link}">{html.escape(category_name)}</a></li>')

        index_html_content: str = f"""<!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Categories</title>
        <link rel="stylesheet" href="styles.css">
        </head>
        <body>
        <h1>Product Categories</h1>
        <ul>
        {"".join(category_links)}
        </ul>
        </body>
        </html>
        """

        save_text_file(index_html_content, index_html_path)

    def generate_html_for_campaign(self, campaign_name: str) -> None:
        """
        Генерирует HTML-страницы для рекламной кампании.

        Args:
            campaign_name (str): Имя рекламной кампании.

        Example:
            >>> campaign.generate_html_for_campaign("HolidaySale")
        """
        campaign_root: Path = Path(gs.path.google_drive / 'aliexpress' / 'campaigns' / campaign_name)
        categories: List[str] = get_filenames_from_directory(campaign_root / 'category', extensions='')

        # Генерация HTML страниц для каждой категории
        for category_name in categories:
            category_path: Path = campaign_root / 'category' / category_name
            products: Optional[List[SimpleNamespace]] = self.get_category_products(category_name=category_name)

            if products:
                # Генерация страниц для каждого товара
                for product in products:
                    ProductHTMLGenerator.set_product_html(product, category_path)

                # Генерация страницы категории
                CategoryHTMLGenerator.set_category_html(products, category_path)
            else:
                logger.warning(f'Товары не найдены для категории {category_name}.')

        # Генерация страницы рекламной кампании
        CampaignHTMLGenerator.set_campaign_html(categories, campaign_root)
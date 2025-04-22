### **Анализ кода модуля `affiliated_products_generator.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Четкая структура класса `AliAffiliatedProducts`.
  - Использование аннотаций типов.
  - Наличие базовой обработки ошибок.
  - Логирование основных этапов работы.
- **Минусы**:
  - Отсутствие единого стиля в оформлении документации и комментариев.
  - Docstring класса `AliAffiliatedProducts` содержит элементы кода (`@code`, `@endcode`), что не соответствует стандарту Markdown.
  - Неполное документирование некоторых методов и атрибутов.
  - Использование `Union` вместо `|` в аннотациях типов.

#### **Рекомендации по улучшению**:
1. **Документация**:
   - Привести docstring и комментарии к единому стилю оформления, следуя рекомендациям, описанным в инструкции.
   - Перевести docstring на русский язык, сохраняя формат UTF-8.
   - Заменить `@code` и `@endcode` в docstring на стандартные блоки кода Markdown.
   - Добавить более подробное описание для параметров и возвращаемых значений методов, включая возможные исключения.

2. **Типизация**:
   - Использовать `|` вместо `Union` в аннотациях типов для большей современности и соответствия стандартам.

3. **Обработка ошибок**:
   - Улучшить обработку ошибок, чтобы более конкретно реагировать на различные исключительные ситуации.

4. **Логирование**:
   - Унифицировать стиль логирования, используя `logger.error` для ошибок и `logger.info` для информационных сообщений.

5. **Общее**:
   - Проверить и обновить все устаревшие комментарии, привести их в соответствие с текущим кодом.

#### **Оптимизированный код**:

```python
## \file src/suppliers/suppliers_list/aliexpress/affiliated_products_generator.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для генерации аффилированных товаров AliExpress.
========================================================

Этот модуль содержит класс `AliAffiliatedProducts`, который отвечает за генерацию полных данных о товарах
из AliExpress Affiliate API. Он расширяет класс `AliApi` для обработки URL-адресов или идентификаторов товаров
и получения подробной информации об аффилированных товарах, включая сохранение изображений, видео и JSON-данных.

Пример использования:
----------------------
    prod_urls = ['123','456',...]
    prod_urls = ['https://www.aliexpress.com/item/123.html','456',...]

    parser = AliAffiliatedProducts(
                                campaign_name,
                                campaign_category,
                                language,
                                currency)

    products = parser.process_affiliate_products(prod_urls)
"""

import asyncio
from itertools import count
from math import log
from pathlib import Path
from typing import List, Union, Optional
from types import SimpleNamespace
from urllib.parse import urlparse, parse_qs

from src import gs
from src.suppliers.suppliers_list.aliexpress import AliApi
from src.suppliers.suppliers_list.aliexpress import Aliexpress
from src.suppliers.suppliers_list.aliexpress.affiliate_links_shortener_via_webdriver import AffiliateLinksShortener
from src.suppliers.suppliers_list.aliexpress.utils.extract_product_id import extract_prod_ids
from src.suppliers.suppliers_list.aliexpress.utils.set_full_https import ensure_https
from src.utils.convertor.csv2json import csv2dict
from src.utils.jjson import j_dumps
from src.utils import save_png_from_url, save_video_from_url
from src.utils.printer import pprint
from src.utils.file import read_text_file, save_text_file

from src.logger.logger import logger


class AliAffiliatedProducts(AliApi):
    """
    Класс для сбора полных данных о товарах из URL-адресов или идентификаторов товаров.
    Предназначен для создания шаблонов рекламных кампаний.

    Args:
        campaign_name (str): Название рекламной кампании.
        campaign_category (Optional[str], optional): Категория кампании (по умолчанию None).
        language (str, optional): Язык кампании (по умолчанию 'EN').
        currency (str, optional): Валюта кампании (по умолчанию 'USD').

    Example:
        prod_urls = ['123','456',...]
        prod_urls = ['https://www.aliexpress.com/item/123.html','456',...]

        parser = AliAffiliatedProducts(
                                    campaign_name,
                                    campaign_category,
                                    language,
                                    currency)

        products = parser.process_affiliate_products(prod_urls)
    """

    campaign_name: str
    campaign_category: Optional[str]
    campaign_path: Path
    language: str
    currency: str

    def __init__(
        self,
        campaign_name: str,
        campaign_category: Optional[str] = None,
        language: str = 'EN',
        currency: str = 'USD',
        *args,
        **kwargs,
    ) -> None:
        """
        Инициализирует класс AliAffiliatedProducts.

        Args:
            campaign_name (str): Название рекламной кампании. Директория с подготовленным материалом берется по имени.
            campaign_category (Optional[str], optional): Категория кампании (default None).
            language (str, optional): Язык кампании (default 'EN').
            currency (str, optional): Валюта кампании (default 'USD').
        """
        super().__init__(language, currency)

        self.campaign_name = campaign_name
        self.campaign_category = campaign_category
        self.language = language
        self.currency = currency
        self.locale = f"{self.language}_{self.currency}"
        self.campaign_path = gs.path.google_drive / 'aliexpress' / 'campaigns' / self.campaign_name / 'categories' / self.campaign_category

    def process_affiliate_products(self, prod_urls: List[str]) -> List[SimpleNamespace] | None:
        """
        Обрабатывает список URL-адресов и возвращает список товаров с партнерскими ссылками и сохраненными изображениями.

        Args:
            prod_urls (List[str]): Список URL-адресов или идентификаторов товаров.

        Returns:
            List[SimpleNamespace] | None: Список обработанных товаров или None в случае ошибки.
        """
        _promotion_links: list = []
        _prod_urls: list = []
        promotional_prod_urls = ensure_https(prod_urls)
        print_flag = 'new_line'

        for prod_url in promotional_prod_urls:
            _link = super().get_affiliate_links(prod_url)
            if _link:
                _link = _link[0]

            if hasattr(_link, 'promotion_link'):
                _promotion_links.append(_link.promotion_link)
                _prod_urls.append(prod_url)

                pprint(f'found affiliate for: {_link.promotion_link}', end=print_flag)
                print_flag = 'inline'
            else:
                logger.info(f'Not found affiliate for {prod_url}')

        if not _promotion_links:
            logger.error('No affiliate products returned')
            return None

        logger.info('Start receiving product details...')
        _affiliate_products: SimpleNamespace = self.retrieve_product_details(_prod_urls)
        if not _affiliate_products:
            return None

        print_flag = 'new_line'
        for product, promotion_link in zip(_affiliate_products, _promotion_links):

            if not promotion_link:
                parsed_url = urlparse(product.promotion_link)
                query_params = parse_qs(parsed_url.query)
                aff_short_key = query_params.get('aff_short_key', [None])[0]
                if aff_short_key:
                    product.promotion_link = fr'https://s.click.aliexpress.com/e/{aff_short_key}'
                else:
                    # Этот товар не является партнерским
                    self.delete_product(product.product_id)
                    continue
            else:
                product.promotion_link = promotion_link

            image_path = self.campaign_path / 'images' / f"{product.product_id}.png"
            save_png_from_url(product.product_main_image_url, image_path, exc_info=False)
            product.local_image_path = str(image_path)
            if len(product.product_video_url) > 1:
                parsed_url = urlparse(product.product_video_url)
                suffix = Path(parsed_url.path).suffix

                video_path = self.campaign_path / 'videos' / f'{product.product_id}.{suffix}'
                save_video_from_url(product.product_video_url, video_path, exc_info=False)
                product.local_video_path = str(video_path)

            pprint(f'caught product - {product.product_id}', end=print_flag)
            print_flag = 'inline'

            if not j_dumps(product, self.campaign_path / self.locale / f"{product.product_id}.json", exc_info=False):
                logger.warning(
                    f"""Failed to write dictionary: \n {pprint(product)} \n path: {self.campaign_path / self.locale / product.product_id}.json""",
                    exc_info=False,
                )
                continue

        pprint(f'caught {len(_affiliate_products)}', end='new_line')
        return _affiliate_products

    def delete_product(self, product_id: str, exc_info: bool = False) -> None:
        """
        Удаляет товар, у которого нет партнерской ссылки.

        Args:
            product_id (str): Идентификатор товара.
            exc_info (bool, optional): Флаг для вывода подробной информации об исключении. По умолчанию False.
        """
        _product_id = extract_prod_ids(product_id)

        product_path = self.campaign_path / 'sources.txt'
        prepared_product_path = self.campaign_path / '_sources.txt'
        products_list = read_text_file(product_path)
        if products_list:
            products_list = convert_list_to_homogeneous_list(products_list)
            for record in products_list:
                if _product_id:
                    record_id = extract_prod_ids(record)
                    if record_id == str(product_id):
                        products_list.remove(record)
                        save_text_file(list2string(products_list, '\n'), prepared_product_path)
                        break
                else:
                    if record == str(product_id):
                        products_list.remove(record)
                        save_text_file(list2string(products_list, '\n'), product_path)

        else:
            product_path = self.campaign_path / 'sources' / f'{product_id}.html'
            try:
                product_path.rename(self.campaign_path / 'sources' / f'{product_id}_.html')
                # product_path.unlink()
                logger.info(f"Product file {product_path} renamed successfully.")
            except FileNotFoundError as ex:
                logger.error(f"Product file {product_path} not found.", ex, exc_info=exc_info)
            except Exception as ex:
                logger.critical(f"An error occurred while deleting the product file {product_path}.", ex)
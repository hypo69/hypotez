### **Анализ кода модуля `affiliated_products_generator.py`**

## \file /src/suppliers/suppliers_list/aliexpress/affiliated_products_generator.py

Модуль предназначен для получения данных о партнерских продуктах с AliExpress. Он содержит класс `AliAffiliatedProducts`, который позволяет собирать полную информацию о продуктах по URL или ID, сохранять изображения и видео, а также генерировать данные для рекламных кампаний.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Использование аннотаций типов.
    - Наличие документации для классов и методов.
    - Использование `logger` для логирования.
    - Разбиение кода на логические блоки.
    - Использование `j_loads_ns` и `j_dumps` для работы с JSON.
- **Минусы**:
    - Отсутствие docstring для модуля.
    - Использование как `str | dict` (Лучше использовать `|` вместо `Union`).
    - Не везде используется `logger.error` для логирования ошибок.
    - Не все переменные аннотированы типами.

**Рекомендации по улучшению:**

1.  **Добавить docstring для модуля**:

    ```python
    """
    Модуль для получения данных о партнерских продуктах с AliExpress.
    ==============================================================

    Модуль содержит класс :class:`AliAffiliatedProducts`, который позволяет собирать полную информацию о продуктах по URL или ID,
    сохранять изображения и видео, а также генерировать данные для рекламных кампаний.

    Пример использования
    ----------------------

    >>> products = AliAffiliatedProducts()
    >>> asyncio.run(products.process_affiliate_products(["http://example.com/product1"], "electronics"))
    """
    ```

2.  **Использовать `|` вместо `Union`**:

    Вместо `str | dict` использовать `str | dict`.

3.  **Улучшить обработку ошибок**:

    Добавить `logger.error` с информацией об исключении в блоках `except`.

4.  **Добавить аннотации типов для переменных**:

    Добавить аннотации типов для всех переменных, где это возможно.

5.  **Улучшить комментарии**:

    Сделать комментарии более конкретными и понятными.

6.  **Удалить закомментированный код**:

    Удалить или объяснить необходимость закомментированного кода.

7.  **Использовать константы для строк**:

    Вместо повторения строковых литералов использовать константы.

8.  **Использовать f-строки для форматирования строк**:

    Использовать f-строки вместо конкатенации строк.

9.  **Использовать асинхронные функции для файловых операций**:

    Убедиться, что все файловые операции выполняются асинхронно.

**Оптимизированный код:**

```python
                ## \file /src/suppliers/suppliers_list/aliexpress/affiliated_products_generator.py
# -*- coding: utf-8 -*-\n\n#! .pyenv/bin/python3
"""
Модуль для получения данных о партнерских продуктах с AliExpress.
==============================================================

Модуль содержит класс :class:`AliAffiliatedProducts`, который позволяет собирать полную информацию о продуктах по URL или ID,
сохранять изображения и видео, а также генерировать данные для рекламных кампаний.

Пример использования
----------------------

>>> products = AliAffiliatedProducts()
>>> asyncio.run(products.process_affiliate_products(["http://example.com/product1"], "electronics"))
"""

import asyncio
from datetime import datetime
import html
from pathlib import Path
from urllib.parse import urlparse
from types import SimpleNamespace
from typing import List, Optional

from src.logger.logger import logger
from src import gs
from src.suppliers.suppliers_list.aliexpress import AliApi
from src.suppliers.suppliers_list.aliexpress.campaign.html_generators import ProductHTMLGenerator, CategoryHTMLGenerator, CampaignHTMLGenerator
from src.suppliers.suppliers_list.aliexpress.utils.ensure_https import ensure_https
from src.endpoints.prestashop.product_fields import ProductFields as f
from src.utils.image import save_image_from_url_async
from src.utils.video import save_video_from_url
from src.utils.file import (read_text_file,
                        get_filenames_from_directory,
                        get_directory_names,
                        save_text_file
                        )
from src.utils.jjson import j_loads_ns, j_dumps
from src.utils.printer import pprint
from src.logger.logger import logger


class AliAffiliatedProducts(AliApi):
    """ Class to collect full product data from URLs or product IDs.
    For more details on how to create templates for ad campaigns, see the section `Managing Aliexpress Ad Campaigns`.
    """
    language: str = None
    currency: str = None

    def __init__(self,
                 language: str = 'EN',
                 currency: str = 'USD',
                 *args, **kwargs):
        """
        Инициализирует класс AliAffiliatedProducts.

        Args:
            language (str): Язык для рекламной кампании (по умолчанию 'EN').
            currency (str): Валюта для рекламной кампании (по умолчанию 'USD').
        """
        if not language or not currency:
            logger.critical('No language or currency provided!')
            return
        super().__init__(language, currency)
        self.language: str = language
        self.currency: str = currency

    async def process_affiliate_products(self, prod_ids: list[str], category_root: Path | str) -> list[SimpleNamespace]:
        """
        Обрабатывает список ID или URL продуктов, возвращает список продуктов с партнерскими ссылками и сохраненными изображениями.

        Args:
            prod_ids (list[str]): Список URL или ID продуктов.
            category_root (Path | str): Путь к корневой директории категории.

        Returns:
            list[SimpleNamespace]: Список обработанных продуктов с партнерскими ссылками и сохраненными изображениями.

        Raises:
            Exception: Если не найдено имя категории в кампании.
        """

        _promotion_links: list[str] = []
        _prod_urls: list[str] = []
        normilized_prod_urls: list[str] = ensure_https(prod_ids)  # <- привожу к виду `https://aliexpress.com/item/<product_id>.html`
        print_flag: str = ''  # <- флаг переключения печати в одну строку

        for prod_url in normilized_prod_urls:
            _links = super().get_affiliate_links(prod_url)
            if _links:
                _links = _links[0]
            if hasattr(_links, 'promotion_link'):
                _promotion_links.append(_links.promotion_link)
                _prod_urls.append(prod_url)
                logger.info(f'found affiliate for {_links.promotion_link}')
                # pprint(              # <- печать в одну строку
                #     f'found affiliate for: {_links.promotion_link}\', end=print_flag)
                # print_flag = \'\\r\'
            else:
                continue

        if not _promotion_links:
            logger.warning(f'No affiliate products returned {prod_ids=}')
            return []

        _affiliated_products: List[SimpleNamespace] = self.retrieve_product_details(_prod_urls)
        if not _affiliated_products:
            return []

        affiliated_products_list: list[SimpleNamespace] = []
        product_titles: list[str] = []
        for product, promotion_link in zip(_affiliated_products, _promotion_links):
            product_titles.append(product.product_title)
            product.language = self.language
            product.promotion_link = promotion_link
            image_path: Path = Path(category_root) / 'images' / f'{product.product_id}.png'
            await save_image_from_url(product.product_main_image_url, image_path)
            logger.info(f'Saved image for {product.product_id=}')

            product.local_image_path = str(image_path)
            if len(product.product_video_url) > 1:
                parsed_url: Path = urlparse(product.product_video_url)
                suffix: str = Path(parsed_url.path).suffix

                video_path: Path = Path(category_root) / 'videos' / f'{product.product_id}{suffix}'
                await save_video_from_url(product.product_video_url, video_path)
                product.local_video_path = str(video_path)
                logger.info(f'Saved video for {product.product_id=}')

            logger.info(f'{product.product_title}')
            j_dumps(product, Path(category_root) / f'{self.language}_{self.currency}' / f'{product.product_id}.json')

            affiliated_products_list.append(product)

        product_titles_path: Path = Path(category_root) / f'{self.language}_{self.currency}' / 'product_titles.txt'
        await save_text_file(product_titles, product_titles_path)
        return affiliated_products_list
### **Анализ кода модуля `affiliated_products_generator.py`**

## Качество кода:

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код хорошо структурирован и организован в классы и функции.
  - Используется логгирование для отслеживания хода выполнения и ошибок.
  - Применены асинхронные операции для улучшения производительности.
  - Обработка исключений присутствует.
  - Использованы аннотации типов.

- **Минусы**:
  - Не все функции и методы имеют подробные docstring.
  - Встречаются смешанные стили форматирования (например, использование print вместо logger).
  - Некоторые переменные не имеют аннотации типов.
  - Не хватает обработки ошибок при сохранении изображений и видео.
  - Не все логи записываются с уровнем `error` при возникновении исключений.

## Рекомендации по улучшению:

1.  **Документация**:

    *   Добавить docstring к классам и функциям, описывающие их назначение, аргументы, возвращаемые значения и возможные исключения.
    *   В docstring необходимо добавить примеры использования.

2.  **Логгирование**:

    *   Заменить `print` на `logger.info` или `logger.debug` для отладочной информации.
    *   Убедиться, что все исключения логируются с использованием `logger.error` с передачей информации об ошибке (`ex, exc_info=True`).

3.  **Обработка ошибок**:

    *   Добавить обработку ошибок при сохранении изображений и видео, чтобы избежать неожиданных сбоев.
    *   Рассмотреть возможность добавления проверок на существование директорий перед сохранением файлов.

4.  **Аннотации типов**:

    *   Добавить аннотации типов для всех переменных, где это возможно.
    *   Убедиться, что все аргументы функций и возвращаемые значения аннотированы типами.

5.  **Форматирование**:

    *   Привести код в соответствие со стандартами PEP8.
    *   Использовать только одинарные кавычки (`'`) для строк.

6.  **Безопасность**:

    *   Убедиться, что все URL проходят валидацию перед использованием, чтобы избежать potential security issues.

7.  **Улучшение обработки данных**:

    *   Более надежная обработка данных, возвращаемых из API, с проверкой на `None` или пустые значения.
    *   Использовать `j_loads` или `j_loads_ns` для чтения JSON или конфигурационных файлов.

## Оптимизированный код:

```python
## \file /src/suppliers/suppliers_list/aliexpress/affiliated_products_generator.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для получения партнерских продуктов с AliExpress
========================================================

Модуль содержит класс :class:`AliAffiliatedProducts`, который используется для сбора данных о продуктах с AliExpress
и создания партнерских ссылок.

Пример использования
----------------------

>>> affiliated_products = AliAffiliatedProducts(language='RU', currency='RUB')
>>> product_ids = ['1234567890', '0987654321']
>>> category_root = '/path/to/category'
>>> products = await affiliated_products.process_affiliate_products(product_ids, category_root)
>>> for product in products:
...     print(product.product_title)
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
    """
    Класс для сбора полных данных о продуктах по URL или ID продуктов.
    Для получения более подробной информации о создании шаблонов для рекламных кампаний см. раздел "Управление рекламными кампаниями Aliexpress".
    """
    language: str = None
    currency: str = None

    def __init__(self,
                 language: str = 'EN',
                 currency: str = 'USD',
                 *args, **kwargs) -> None:
        """
        Инициализирует класс AliAffiliatedProducts.

        Args:
            language (str): Язык для кампании (по умолчанию 'EN').
            currency (str): Валюта для кампании (по умолчанию 'USD').
        """
        if not language or not currency:
            logger.critical('No language or currency provided!')
            return
        super().__init__(language, currency)
        self.language: str = language
        self.currency: str = currency

    async def process_affiliate_products(self, prod_ids: list[str], category_root: Path | str) -> list[SimpleNamespace]:
        """
        Обрабатывает список ID продуктов или URL и возвращает список продуктов с партнерскими ссылками и сохраненными изображениями.

        Args:
            prod_ids (list[str]): Список URL или ID продуктов.
            category_root (Path | str): Корневой каталог категории.

        Returns:
            list[SimpleNamespace]: Список обработанных продуктов с партнерскими ссылками и сохраненными изображениями.

        Example:
            >>> affiliated_products = AliAffiliatedProducts(language='RU', currency='RUB')
            >>> product_ids = ['1234567890', '0987654321']
            >>> category_root = '/path/to/category'
            >>> products = await affiliated_products.process_affiliate_products(product_ids, category_root)
            >>> for product in products:
            ...     print(product.product_title)

        Raises:
            Exception: Если возникает ошибка при обработке продуктов.
        """

        _promotion_links: list = []
        _prod_urls: list = []
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
                # print_flag = '\\r'
            else:
                continue

        if not _promotion_links:
            logger.warning(
                f'No affiliate products returned {prod_ids=}/n', None, None)
            return None

        _affiliated_products: List[SimpleNamespace] = self.retrieve_product_details(
            _prod_urls)
        if not _affiliated_products:
            return None

        affiliated_products_list: list[SimpleNamespace] = []
        product_titles: list[str] = []
        for product, promotion_link in zip(_affiliated_products, _promotion_links):
            product_titles.append(product.product_title)
            product.language: str = self.language
            product.promotion_link: str = promotion_link
            image_path: Path = Path(category_root) / 'images' / \
                f'{product.product_id}.png'
            await save_image_from_url(product.product_main_image_url, image_path)
            # pprint(f"Saved image for {product.product_id=}", end=print_flag)
            logger.info(f'Saved image for {product.product_id=}')

            product.local_image_path: str = str(image_path)
            if len(product.product_video_url) > 1:
                parsed_url: Path = urlparse(product.product_video_url)
                suffix: str = Path(parsed_url.path).suffix

                video_path: Path = Path(category_root) / 'videos' / \
                    f'{product.product_id}{suffix}'
                await save_video_from_url(product.product_video_url, video_path)
                product.local_video_path: str = str(video_path)
                logger.info(f'Saved video for {product.product_id=}')

            # product.tags = f"#{f_normalizer.simplify_string(product.first_level_category_name)}, #{f_normalizer.simplify_string(product.second_level_category_name)}"\
            logger.info(f'{product.product_title}')
            j_dumps(product, Path(category_root) / f'{self.language}_{self.currency}' / f'{product.product_id}.json')
            # pprint(f"Dumped in {Path(category_root) / f'{self.language}_{self.currency}' / f'{product.product_id}.json'} ")

            affiliated_products_list.append(product)
        # print_flag = 'newline'
        product_titles_path: Path = Path(category_root) / f'{self.language}_{self.currency}' / 'product_titles.txt'
        await save_text_file(product_titles, product_titles_path)
        return affiliated_products_list
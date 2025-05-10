### **Анализ кода модуля `affiliated_products_generator.py`**

**Расположение файла:** `src/suppliers/suppliers_list/aliexpress/affiliated_products_generator.py`

**Описание:** Модуль предназначен для получения данных о партнерских товарах с AliExpress, включая получение партнерских ссылок, сохранение изображений и видео, и сохранение полученных данных в формате JSON.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код хорошо структурирован и логически разделен на функции.
  - Используется асинхронность для выполнения операций, что повышает производительность.
  - Присутствует логирование важных этапов работы.
  - Используются аннотации типов.
- **Минусы**:
  - Не все функции и методы имеют подробные docstring.
  - Встречаются закомментированные строки кода.
  - Некоторые переменные объявлены без явного указания типа.

**Рекомендации по улучшению:**

1.  **Документирование кода**:
    - Добавить подробные docstring для всех функций и методов, описывающие их назначение, входные параметры, возвращаемые значения и возможные исключения.
    - Включить примеры использования в docstring.
2.  **Удаление закомментированного кода**:
    - Удалить все закомментированные строки кода, если они не несут полезной информации.
3.  **Явное указание типов переменных**:
    - Указывать типы для всех переменных, чтобы повысить читаемость и облегчить отладку.
4.  **Улучшение логирования**:
    - Добавить больше контекстной информации в сообщения логирования, чтобы облегчить отладку и мониторинг работы модуля.
5. **Использовать `j_dumps` или `j_loads_ns`**:
    - Для чтения JSON или конфигурационных файлов замените стандартное использование `open` и `json.load` на `j_loads` или `j_loads_ns`.
6. **Не используй `Union[]` в коде. Вместо него используй `|`

**Оптимизированный код:**

```python
## \file /src/suppliers/suppliers_list/aliexpress/affiliated_products_generator.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для получения данных о партнерских товарах с AliExpress.
=================================================================
Модуль содержит класс :class:`AliAffiliatedProducts`, который используется для получения
полных данных о товарах с AliExpress, включая партнерские ссылки,
сохранение изображений и видео, и сохранение полученных данных в формате JSON.

"""

import asyncio
from datetime import datetime
import html
from pathlib import Path
from urllib.parse import urlparse
from types import SimpleNamespace
from typing import List

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
    Класс для сбора полных данных о товарах с AliExpress, включая партнерские ссылки.
    Подробнее о создании шаблонов для рекламных кампаний смотрите в разделе "Управление рекламными кампаниями Aliexpress".
    """
    language: str = None
    currency: str = None

    def __init__(self,
                 language: str | dict = 'EN',
                 currency: str = 'USD',
                 *args, **kwargs):
        """
        Инициализирует класс AliAffiliatedProducts.

        Args:
            language (str | dict): Язык для кампании (по умолчанию 'EN').
            currency (str): Валюта для кампании (по умолчанию 'USD').
        """
        if not language or not currency:
            logger.critical(f"Нет языка или валюты!")
            return
        super().__init__(language, currency)
        self.language: str = language
        self.currency: str = currency

    async def process_affiliate_products(self, prod_ids: list[str], category_root: Path | str) -> list[SimpleNamespace]:
        """
        Обрабатывает список ID товаров или URL и возвращает список товаров с партнерскими ссылками и сохраненными изображениями.

        Args:
            prod_ids (list[str]): Список URL или ID товаров.
            category_root (Path | str): Корневой путь к категории.

        Returns:
            list[SimpleNamespace]: Список обработанных товаров с партнерскими ссылками и сохраненными изображениями.

        Example:
            >>> campaign = SimpleNamespace(category={})
            >>> category_name = "electronics"
            >>> prod_ids = ["http://example.com/product1", "http://example.com/product2"]
            >>> products = campaign.process_affiliate_products(category_name, prod_ids)
            >>> for product in products:
            ...     print(product.product_title)
            "Product 1 Title"
            "Product 2 Title"

        Raises:
            Exception: Если имя категории не найдено в кампании.

        """

        _promotion_links: list = []
        _prod_urls: list = []
        normilized_prod_urls: list[str] = ensure_https(prod_ids)  # приведение к виду `https://aliexpress.com/item/<product_id>.html`
        print_flag: str = ''  # флаг переключения печати в одну строку

        for prod_url in normilized_prod_urls:
            _links = super().get_affiliate_links(prod_url)
            if _links:
                _links = _links[0]
            if hasattr(_links, 'promotion_link'):
                _promotion_links.append(_links.promotion_link)
                _prod_urls.append(prod_url)
                logger.info(f"Найдена партнерская ссылка для {_links.promotion_link}")
            else:
                continue

        if not _promotion_links:
            logger.warning(
                f'Партнерские товары не возвращены {prod_ids=}/n', None, None)
            return None

        _affiliated_products: List[SimpleNamespace] = self.retrieve_product_details(
            _prod_urls)
        if not _affiliated_products:
            return None

        affiliated_products_list: list[SimpleNamespace] = []
        product_titles: list = []
        for product, promotion_link in zip(_affiliated_products, _promotion_links):
            product_titles.append(product.product_title)
            product.language = self.language
            product.promotion_link = promotion_link
            image_path: Path = Path(category_root) / 'images' / \
                f"{product.product_id}.png"
            await save_image_from_url(product.product_main_image_url, image_path)
            logger.info(f"Сохранено изображение для {product.product_id=}")

            product.local_image_path = str(image_path)
            if len(product.product_video_url) > 1:
                parsed_url: Path = urlparse(product.product_video_url)
                suffix: str = Path(parsed_url.path).suffix

                video_path: Path = Path(category_root) / 'videos' / \
                    f'{product.product_id}{suffix}'
                await save_video_from_url(product.product_video_url, video_path)
                product.local_video_path = str(video_path)
                logger.info(f"Сохранено видео для {product.product_id=}")

            logger.info(f"{product.product_title}")
            j_dumps(product, Path(category_root) / f'{self.language}_{self.currency}' / f'{product.product_id}.json')

            affiliated_products_list.append(product)
        product_titles_path: Path = category_root / \
            f"{self.language}_{self.currency}" / 'product_titles.txt'
        await save_text_file(product_titles, product_titles_path)
        return affiliated_products_list
### **Анализ кода модуля `affiliated_products_generator.py`**

## \file /hypotez/src/suppliers/suppliers_list/aliexpress/_docs/affiliated_products_generator.md

### **Анализ кода модуля `affiliated_products_generator.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код содержит подробное описание класса `AliAffiliatedProducts` и его методов.
  - Присутствуют примеры использования и объяснения основных функциональностей.
  - Есть упоминания о юнит-тестах и обработке ошибок.
- **Минусы**:
  - Отсутствует docstring в соответствии с заданным форматом.
  - Не все параметры функций аннотированы типами.
  - Отсутствует логирование с использованием `logger` из модуля `src.logger`.
  - Не все комментарии переведены на русский язык.
  - Не везде используется одинарные кавычки.

#### **Рекомендации по улучшению**:
1. **Формат документации**:
   - Добавить docstring в соответствии с заданным форматом для класса `AliAffiliatedProducts` и всех его методов, включая внутренние функции.
   - Перевести все комментарии и docstring на русский язык в формате UTF-8.
   - В docstring добавить подробное описание того, что именно делает каждая функция, аргументы, возвращаемые значения и возможные исключения.

2. **Аннотации типов**:
   - Убедиться, что все параметры функций и переменные аннотированы типами.
   - Использовать `|` вместо `Union[]`.

3. **Логирование**:
   - Заменить `print` на `logger.info` или `logger.debug` для информационных сообщений.
   - Использовать `logger.error` для логирования ошибок и исключений, передавая ошибку вторым аргументом и устанавливая `exc_info=True`.

4. **Использование кавычек**:
   - Привести все строки к использованию одинарных кавычек.

5. **Обработка исключений**:
   - Использовать `ex` вместо `e` в блоках обработки исключений.

6. **Дополнительные улучшения**:
   - Рассмотреть возможность использования асинхронных запросов для повышения производительности.
   - Добавить больше юнит-тестов для покрытия краевых случаев и обеспечения надежности кода.

#### **Оптимизированный код**:
```python
"""
Модуль для работы с Aliexpress Affiliate API
=================================================

Модуль содержит класс :class:`AliAffiliatedProducts`, который используется для получения полной информации о продуктах
из Aliexpress Affiliate API. Класс расширяет :class:`AliApi` для обработки URL-адресов продуктов или идентификаторов,
извлечения деталей об аффилированных продуктах, включая сохранение изображений, видео и JSON-данных.

Пример использования
----------------------

>>> parser = AliAffiliatedProducts(campaign_name='test_campaign', campaign_category='test_category', language='RU', currency='RUB')
>>> products = parser.process_affiliate_products(['https://www.aliexpress.com/item/123.html'])
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
    Класс для сбора полных данных о продуктах из URL-адресов или идентификаторов продуктов, используя Aliexpress Affiliate API.

    Args:
        campaign_name (str): Название рекламной кампании.
        campaign_category (Optional[str]): Категория кампании (по умолчанию None).
        language (str): Язык кампании (по умолчанию 'EN').
        currency (str): Валюта кампании (по умолчанию 'USD').

    Example:
        >>> prod_urls = ['123','456',...]
        >>> prod_urls = ['https://www.aliexpress.com/item/123.html','456',...]
        >>> parser = AliAffiliatedProducts(
        ...     campaign_name='test_campaign',
        ...     campaign_category='test_category',
        ...     language='RU',
        ...     currency='RUB'
        ... )
        >>> products = parser.process_affiliate_products(prod_urls)
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
        Инициализация экземпляра класса AliAffiliatedProducts.

        Args:
            campaign_name (str): Название рекламной кампании.
            campaign_category (Optional[str]): Категория кампании (по умолчанию None).
            language (str): Язык кампании (по умолчанию 'EN').
            currency (str): Валюта кампании (по умолчанию 'USD').
        """
        super().__init__(language, currency)

        self.campaign_name = campaign_name
        self.campaign_category = campaign_category
        self.language = language
        self.currency = currency
        self.locale = f'{self.language}_{self.currency}'
        self.campaign_path = gs.path.google_drive / 'aliexpress' / 'campaigns' / self.campaign_name / 'categories' / self.campaign_category

    def process_affiliate_products(self, prod_urls: List[str]) -> List[SimpleNamespace] | None:
        """
        Обрабатывает список URL-адресов и возвращает список продуктов с партнерскими ссылками и сохраненными изображениями.

        Args:
            prod_urls (List[str]): Список URL-адресов или идентификаторов продуктов.

        Returns:
            List[SimpleNamespace] | None: Список обработанных продуктов.
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

                logger.info(f'Найдена партнерская ссылка для: {_link.promotion_link}')
                pprint(f'found affiliate for: {_link.promotion_link}', end=print_flag)  # TODO: remove pprint
                print_flag = 'inline'
            else:
                logger.info(f'Не найдена партнерская ссылка для {prod_url}')
                # logger.info_red(f'Not found affiliate for {prod_url}') # TODO: remove info_red

        if not _promotion_links:
            logger.error('Не найдено партнерских продуктов')
            return None
            # logger.error('No affiliate products returned') # TODO: remove error
            # return

        logger.info('Начинаем получение деталей продукта...')
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
                    """ Этот продукт не является партнерским """
                    self.delete_product(product.product_id)
                    continue
            else:
                product.promotion_link = promotion_link

            image_path = self.campaign_path / 'images' / f'{product.product_id}.png'
            save_png_from_url(product.product_main_image_url, image_path, exc_info=False)
            product.local_image_path = str(image_path)
            if len(product.product_video_url) > 1:
                parsed_url = urlparse(product.product_video_url)
                suffix = Path(parsed_url.path).suffix

                video_path = self.campaign_path / 'videos' / f'{product.product_id}.{suffix}'
                save_video_from_url(product.product_video_url, video_path, exc_info=False)
                product.local_video_path = str(video_path)

            logger.info(f'Получен продукт - {product.product_id}')
            pprint(f'caught product - {product.product_id}', end=print_flag)  # TODO: remove pprint
            print_flag = 'inline'

            if not j_dumps(product, self.campaign_path / self.locale / f'{product.product_id}.json', exc_info=False):
                logger.warning(
                    f'Не удалось записать словарь: \n {pprint(product)} \n path: {self.campaign_path / self.locale / product.product_id}.json',
                    exc_info=False,
                )
                continue

        logger.info(f'Получено {len(_affiliate_products)} продуктов')
        pprint(f'caught {len(_affiliate_products)}', end='new_line')  # TODO: remove pprint
        return _affiliate_products

    def delete_product(self, product_id: str, exc_info: bool = False) -> None:
        """
        Удаляет продукт, у которого нет партнерской ссылки.

        Args:
            product_id (str): Идентификатор продукта.
            exc_info (bool, optional): Определяет, нужно ли выводить служебную информацию об исключении. По умолчанию False.
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
                logger.info(f'Файл продукта {product_path} успешно переименован.')
                # logger.success(f"Product file {product_path} renamed successfully.") # TODO: remove success
            except FileNotFoundError as ex:
                logger.error(f'Файл продукта {product_path} не найден.', ex, exc_info=exc_info)
                # logger.error(f"Product file {product_path} not found.", exc_info=exc_info) # TODO: remove error
            except Exception as ex:
                logger.critical(f'Произошла ошибка при удалении файла продукта {product_path}.', ex, exc_info=True)
                # logger.critical(f"An error occurred while deleting the product file {product_path}.", ex) # TODO: remove critical
### **Анализ кода модуля `affiliated_products_generator.py`**

## \file /hypotez/src/suppliers/suppliers_list/aliexpress/_docs/affiliated_products_generator.md

#### **Качество кода**:

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код хорошо структурирован и разбит на логические блоки.
  - Присутствуют docstring для классов и методов, что облегчает понимание кода.
  - Используются аннотации типов.
- **Минусы**:
  - Docstring написаны на английском языке.
  - Не все функции и методы имеют подробные docstring, описывающие их функциональность, аргументы и возвращаемые значения.
  - Встречаются неинформативные комментарии, например, "Purpose".
  - Не все логические блоки кода подробно прокомментированы.

#### **Рекомендации по улучшению**:

1.  **Перевод Docstring на русский язык**:
    *   Все docstring должны быть переведены на русский язык для соответствия стандартам проекта.

2.  **Доработка Docstring**:
    *   Дополнить docstring для всех функций и методов, указав подробное описание их работы, аргументов, возвращаемых значений и возможных исключений.
    *   Включить примеры использования для основных функций.

3.  **Детализация комментариев**:
    *   Заменить общие комментарии, такие как "Purpose", на более конкретные описания, объясняющие назначение каждого блока кода.
    *   Добавить комментарии для каждого логического блока кода, объясняющие его функциональность.

4.  **Использование `logger`**:
    *   Убедиться, что все ошибки и исключения логируются с использованием `logger.error` с передачей `exc_info=True` для получения подробной информации об ошибке.
    *   Логировать важные этапы выполнения кода с использованием `logger.info`.

5.  **Форматирование кода**:
    *   Привести код в соответствие со стандартами PEP8, включая пробелы вокруг операторов и использование одинарных кавычек.

6.  **Обработка исключений**:
    *   Использовать `ex` вместо `e` в блоках обработки исключений.

7.  **Аннотации типов**:
    *   Убедиться, что все переменные и параметры функций аннотированы типами.

8. **Использовать webdriver, если надо**
    *   Если в коде используется webdriver, знай как его использовать, наследуй Driver, Chrome, Firexox, Playwright. Далее определи так:
    ```python
    # Создание инстанса драйвера (пример с Chrome)
    driver = Drivewr(Chrome)
    ```
    *   В модулях Driver И Chrome, Firexox, Playwright уже содержатся все настройки selenium.
    *   Основная комада, которая используется в коде: `driver.execute_locator(l:dict)`. Она возвращает аначение вебэелемента по локатору.

#### **Оптимизированный код**:

```python
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
    Класс для сбора полных данных о продукте по URL или идентификатору продукта
    locator_description Подробнее о создании шаблонов для рекламных кампаний см. в разделе `Управление рекламными кампаниями Aliexpress`

    Пример использования:
    ----------------------
    >>> prod_urls = ['123','456',...]
    >>> prod_urls = ['https://www.aliexpress.com/item/123.html','456',...]

    >>> parser = AliAffiliatedProducts(
    >>>                                 campaign_name,
    >>>                                 campaign_category,
    >>>                                 language,
    >>>                                 currency)

    >>> products = parser._affiliate_product(prod_urls)
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
        Инициализация класса AliAffiliatedProducts.

        Args:
            campaign_name (str): Название рекламной кампании. Директория с подготовленным материалом берется по названию.
            campaign_category (Optional[str], optional): Категория для кампании (по умолчанию None).
            language (str, optional): Язык для кампании (по умолчанию 'EN').
            currency (str, optional): Валюта для кампании (по умолчанию 'USD').
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
            List[SimpleNamespace] | None: Список обработанных продуктов или None, если не найдено партнерских продуктов.
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
                    """ This product is not an affiliate"""
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

            pprint(f'caught product - {product.product_id}', end=print_flag)
            print_flag = 'inline'

            if not j_dumps(product, self.campaign_path / self.locale / f'{product.product_id}.json', exc_info=False):
                logger.warning(
                    f"""Failed to write dictionary: \n {pprint(product)} \n path: {self.campaign_path / self.locale / product.product_id}.json""",
                    exc_info=False,
                )
                continue

        pprint(f'caught {len(_affiliate_products)}', end='new_line')
        return _affiliate_products

    def delete_product(self, product_id: str, exc_info: bool = False) -> None:
        """
        Удаляет продукт, у которого нет партнерской ссылки.

        Args:
            product_id (str): Идентификатор продукта.
            exc_info (bool, optional): Флаг для отображения информации об исключении. По умолчанию False.

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
                logger.info(f'Product file {product_path} renamed successfully.')
            except FileNotFoundError as ex:
                logger.error(f'Product file {product_path} not found.', ex, exc_info=exc_info)
            except Exception as ex:
                logger.critical(f'An error occurred while deleting the product file {product_path}.', ex, exc_info=exc_info)
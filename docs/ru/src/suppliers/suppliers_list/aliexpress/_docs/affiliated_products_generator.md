# Документация модуля `affiliated_products_generator.py`

## Обзор

Файл `affiliated_products_generator.py` содержит класс `AliAffiliatedProducts`, предназначенный для получения полных данных о товарах из Aliexpress Affiliate API. Этот класс расширяет класс `AliApi` для обработки URL-адресов или идентификаторов товаров, а также для извлечения подробной информации о партнерских продуктах, включая сохранение изображений, видео и данных JSON.

## Подробнее

Данный модуль является частью проекта `hypotez` и предназначен для работы с партнерской программой Aliexpress. Он позволяет автоматизировать процесс сбора информации о товарах, получения партнерских ссылок и сохранения необходимых медиафайлов для дальнейшего использования в рекламных кампаниях или других целях.

## Содержание

1.  [Импорты и зависимости](#Импорты-и-зависимости)
2.  [Класс `AliAffiliatedProducts`](#Класс-AliAffiliatedProducts)
    *   [Описание класса](#Описание-класса)
    *   [Атрибуты класса](#Атрибуты-класса)
    *   [Метод `__init__`](#Метод---init--)
    *   [Метод `process_affiliate_products`](#Метод-process_affiliate_products)
    *   [Метод `delete_product`](#Метод-delete_product)

## Импорты и зависимости

В данном файле используются следующие модули и библиотеки:

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
```

*   **Стандартные библиотеки:** `asyncio`, `itertools`, `math`, `pathlib`, `typing`, `types`, `urllib.parse`.
*   **Внешние библиотеки:** `src.settings`, `src.suppliers.suppliers_list.aliexpress`, `src.utils.convertor`, `src.utils`, `src.logger`.

## Класс `AliAffiliatedProducts`

### Описание класса

```python
class AliAffiliatedProducts(AliApi):
    """ Class to collect full product data from URLs or product IDs
    locator_description For more details on how to create templates for ad campaigns, see the section `Managing Aliexpress Ad Campaigns`
    @code
    # Example usage:
    prod_urls = ['123','456',...]
    prod_urls = ['https://www.aliexpress.com/item/123.html','456',...]

    parser = AliAffiliatedProducts(
                                campaign_name,
                                campaign_category,
                                language,
                                currency)

    products = parser._affiliate_product(prod_urls)
    @endcode
    """
```

**Назначение:** Класс для сбора полных данных о товарах из URL-адресов или идентификаторов товаров, используя Aliexpress Affiliate API.

**Наследует:** `AliApi`.

### Атрибуты класса

```python
campaign_name: str
campaign_category: Optional[str]
campaign_path: Path
language: str
currency: str
```

*   `campaign_name` (str): Имя рекламной кампании.
*   `campaign_category` (Optional[str]): Категория кампании (по умолчанию `None`).
*   `campaign_path` (Path): Путь к каталогу, где хранятся материалы кампании.
*   `language` (str): Язык для кампании (по умолчанию `'EN'`).
*   `currency` (str): Валюта для кампании (по умолчанию `'USD'`).

### Метод `__init__`

```python
def __init__(self,
             campaign_name: str,
             campaign_category: Optional[str] = None,
             language: str = 'EN',
             currency: str = 'USD',
             *args, **kwargs):
    """
    @param campaign_name `str`: Name of the advertising campaign. The directory with the prepared material is taken by name.
    @param campaign_category `Optional[str]`: Category for the campaign (default None).
    @param language `str`: Language for the campaign (default 'EN').
    @param currency `str`: Currency for the campaign (default 'USD').
    @param tracking_id `str`: Tracking ID for Aliexpress API.
    """
    super().__init__(language, currency)

    self.campaign_name = campaign_name
    self.campaign_category = campaign_category
    self.language = language
    self.currency = currency
    self.locale = f"{self.language}_{self.currency}"
    self.campaign_path = gs.path.google_drive / 'aliexpress' / 'campaigns' / self.campaign_name / 'categories' / self.campaign_category
```

**Назначение:** Инициализирует экземпляр класса `AliAffiliatedProducts`.

**Параметры:**

*   `campaign_name` (str): Имя рекламной кампании.
*   `campaign_category` (Optional[str], optional): Категория кампании. По умолчанию `None`.
*   `language` (str, optional): Язык для кампании. По умолчанию `'EN'`.
*   `currency` (str, optional): Валюта для кампании. По умолчанию `'USD'`.

**Как работает метод:**

1.  Вызывает конструктор родительского класса `AliApi` с параметрами `language` и `currency`.
2.  Устанавливает атрибуты экземпляра класса, такие как `campaign_name`, `campaign_category`, `language`, `currency` и `locale`.
3.  Формирует путь к каталогу кампании (`campaign_path`) на основе имени кампании и категории, используя настройки Google Drive (`gs.path.google_drive`).

### Метод `process_affiliate_products`

```python
def process_affiliate_products(self, prod_urls: List[str]) -> List[SimpleNamespace]:
    """
    Processes a list of URLs and returns a list of products with affiliate links and saved images.

    :param prod_urls: List of product URLs or IDs.
    :return: List of processed products.
    """
    ...
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
            logger.info_red(f'Not found affiliate for {prod_url}')
    
    if not _promotion_links:
        logger.error('No affiliate products returned')
        return

    logger.info_red('Start receiving product details...')
    _affiliate_products: SimpleNamespace = self.retrieve_product_details(_prod_urls)
    if not _affiliate_products:
        return 
    
    print_flag = 'new_line'
    for product, promotion_link in zip(_affiliate_products, _promotion_links):
        ...

        if not promotion_link:
            parsed_url = urlparse(product.promotion_link)
            query_params = parse_qs(parsed_url.query)
            aff_short_key = query_params.get('aff_short_key', [None])[0]
            if aff_short_key:
                product.promotion_link = fr'https://s.click.aliexpress.com/e/{aff_short_key}'
            else:
                """ This product is not an affiliate"""
                self.delete_product(product.product_id)
                ...
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
            logger.warning(f"""Failed to write dictionary: \n {pprint(product)} \n path: {self.campaign_path / self.locale / product.product_id}.json""", exc_info=False)
            ...
            continue
            
    pprint(f'caught {len(_affiliate_products)}', end='new_line')
    return _affiliate_products
```

**Назначение:** Обрабатывает список URL-адресов товаров или их идентификаторов для получения партнерских ссылок, сохранения изображений и видео, а также сохранения подробной информации о товарах.

**Параметры:**

*   `prod_urls` (List[str]): Список URL-адресов товаров или их идентификаторов.

**Возвращает:**

*   List[SimpleNamespace]: Список объектов `SimpleNamespace`, представляющих обработанные товары.

**Как работает метод:**

1.  Инициализирует два пустых списка: `_promotion_links` для хранения партнерских ссылок и `_prod_urls` для хранения URL-адресов товаров.
2.  Вызывает функцию `ensure_https` для преобразования всех URL-адресов товаров в HTTPS.
3.  Перебирает URL-адреса товаров:
    *   Вызывает метод `get_affiliate_links` родительского класса `AliApi` для получения партнерской ссылки для каждого URL-адреса товара.
    *   Если партнерская ссылка найдена, добавляет её в список `_promotion_links`, а URL-адрес товара — в список `_prod_urls`.
    *   Выводит информацию о найденной партнерской ссылке с помощью `pprint`.
    *   Если партнерская ссылка не найдена, регистрирует это событие с помощью `logger.info_red`.
4.  Если список `_promotion_links` пуст, регистрирует ошибку с помощью `logger.error` и возвращает `None`.
5.  Вызывает метод `retrieve_product_details` для получения подробной информации о товарах.
6.  Перебирает товары и соответствующие партнерские ссылки:
    *   Если партнерская ссылка отсутствует, пытается извлечь короткий ключ партнерской ссылки из URL-адреса товара.
    *   Если короткий ключ найден, формирует партнерскую ссылку на его основе.
    *   Если короткий ключ не найден, вызывает метод `delete_product` для удаления товара и переходит к следующему товару.
    *   Сохраняет изображение товара с помощью функции `save_png_from_url` и устанавливает атрибут `local_image_path` объекта товара.
    *   Если у товара есть видео, сохраняет его с помощью функции `save_video_from_url` и устанавливает атрибут `local_video_path` объекта товара.
    *   Сохраняет информацию о товаре в формате JSON с помощью функции `j_dumps`.
    *   В случае ошибки при сохранении JSON, регистрирует предупреждение с помощью `logger.warning` и переходит к следующему товару.
7.  Возвращает список обработанных товаров `_affiliate_products`.

### Метод `delete_product`

```python
def delete_product(self, product_id: str, exc_info: bool = False):
    """ Delete a product that does not have an affiliate link"""
    ...
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
            logger.success(f"Product file {product_path} renamed successfully.")
        except FileNotFoundError as ex:
            logger.error(f"Product file {product_path} not found.", exc_info=exc_info)
        except Exception as ex:
            logger.critical(f"An error occurred while deleting the product file {product_path}.", ex)                
    ...
```

**Назначение:** Удаляет информацию о товаре, для которого не найдена партнерская ссылка.

**Параметры:**

*   `product_id` (str): Идентификатор товара.
*   `exc_info` (bool, optional): Флаг, указывающий, нужно ли выводить расширенную информацию об исключении в лог. По умолчанию `False`.

**Как работает метод:**

1.  Извлекает идентификатор товара с помощью функции `extract_prod_ids`.
2.  Определяет пути к файлам `sources.txt` и `_sources.txt` в каталоге кампании.
3.  Читает содержимое файла `sources.txt` с помощью функции `read_text_file`.
4.  Если файл `sources.txt` существует:
    *   Преобразует список товаров в однородный список с помощью функции `convert_list_to_homogeneous_list`.
    *   Перебирает записи в списке товаров:
        *   Если идентификатор товара найден, извлекает идентификатор записи и сравнивает его с идентификатором товара.
        *   Если идентификаторы совпадают, удаляет запись из списка товаров и сохраняет обновленный список в файл `_sources.txt` с помощью функции `save_text_file`.
        *   Если запись не содержит идентификатора товара, сравнивает запись с идентификатором товара.
        *   Если запись и идентификатор совпадают, удаляет запись из списка товаров и сохраняет обновленный список в файл `sources.txt`.
5.  Если файл `sources.txt` не существует:
    *   Определяет путь к файлу товара в каталоге `sources`.
    *   Пытается переименовать файл товара, добавив к имени файла символ `_`.
    *   В случае успеха регистрирует сообщение об успехе с помощью `logger.success`.
    *   В случае ошибки `FileNotFoundError` регистрирует ошибку с помощью `logger.error`.
    *   В случае другой ошибки регистрирует критическую ошибку с помощью `logger.critical`.

```
`
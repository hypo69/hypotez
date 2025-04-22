# `affiliated_products_generator.py`: Генерация данных об аффилированных товарах

## Обзор

Файл `affiliated_products_generator.py` содержит класс `AliAffiliatedProducts`, который отвечает за генерацию полных данных о товарах из Aliexpress Affiliate API. Он основан на классе `AliApi` и предназначен для обработки URL-адресов или идентификаторов товаров, извлечения подробной информации об аффилированных товарах, включая сохранение изображений, видео и данных в формате JSON.

## Подробней

Этот файл является частью проекта `hypotez` и расположен в `src/suppliers/suppliers_list/aliexpress`. Он используется для получения информации о товарах с AliExpress через Affiliate API и сохранения этой информации локально для дальнейшего использования в рекламных кампаниях.

## Импорты и зависимости

В начале файла импортируются необходимые библиотеки и модули:

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

- **Стандартные библиотеки:** `asyncio`, `itertools`, `math`, `pathlib`, `typing`, `types`, `urllib.parse`.
- **Внешние библиотеки:** `src.settings`, `src.suppliers.suppliers_list.aliexpress`, `src.utils.convertor`, `src.utils`, `src.logger`.

## Классы

### `AliAffiliatedProducts`

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

**Описание**: Класс для сбора полных данных о товарах из URL-адресов или идентификаторов товаров.

**Наследует**:
- `AliApi`: Предоставляет базовую функциональность для взаимодействия с API Aliexpress.

**Атрибуты**:
- `campaign_name` (str): Название рекламной кампании.
- `campaign_category` (Optional[str]): Категория для кампании (по умолчанию `None`).
- `campaign_path` (Path): Путь к директории, где хранятся материалы кампании.
- `language` (str): Язык для кампании (по умолчанию `'EN'`).
- `currency` (str): Валюта для кампании (по умолчанию `'USD'`).

**Принцип работы**:
Класс `AliAffiliatedProducts` предназначен для получения данных о товарах из AliExpress, используя их URL-адреса или идентификаторы. Он использует API AliExpress для получения информации о товарах, включая аффилированные ссылки, изображения и видео. Полученные данные сохраняются локально для дальнейшего использования в рекламных кампаниях. Класс наследуется от `AliApi`, что позволяет повторно использовать общую логику для взаимодействия с API AliExpress.

## Методы класса

### `__init__`

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

**Назначение**: Инициализация экземпляра класса `AliAffiliatedProducts`.

**Параметры**:
- `campaign_name` (str): Название рекламной кампании.
- `campaign_category` (Optional[str], optional): Категория для кампании. По умолчанию `None`.
- `language` (str, optional): Язык для кампании. По умолчанию `'EN'`.
- `currency` (str, optional): Валюта для кампании. По умолчанию `'USD'`.
- `*args`: Произвольные позиционные аргументы, передаваемые в конструктор родительского класса.
- `**kwargs`: Произвольные именованные аргументы, передаваемые в конструктор родительского класса.

**Как работает функция**:
- Вызывает конструктор родительского класса `AliApi` с параметрами `language` и `currency`.
- Устанавливает атрибуты экземпляра класса: `campaign_name`, `campaign_category`, `language`, `currency`.
- Формирует атрибут `locale` на основе `language` и `currency`.
- Формирует путь к директории кампании `campaign_path` на основе названия кампании и категории, используя настройки из `gs.path.google_drive`.

### `process_affiliate_products`

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
        
        if not j_dumps(product, self.campaign_path / self.locale / f"{product.product_id}.json", exc_info=False):\
            logger.warning(f"""Failed to write dictionary: \n {pprint(product)} \n path: {self.campaign_path / self.locale / product.product_id}.json""", exc_info=False)
            ...
            continue
            
    pprint(f'caught {len(_affiliate_products)}', end='new_line')
    return _affiliate_products
```

**Назначение**: Обрабатывает список URL-адресов товаров, получает аффилированные ссылки, сохраняет изображения и видео, а также сохраняет детали товаров.

**Параметры**:
- `prod_urls` (List[str]): Список URL-адресов или идентификаторов товаров.

**Возвращает**:
- List[SimpleNamespace]: Список объектов `SimpleNamespace`, представляющих обработанные товары.

**Как работает функция**:
1. Инициализирует пустые списки `_promotion_links` и `_prod_urls`.
2. Преобразует URL-адреса товаров в HTTPS, используя функцию `ensure_https`.
3. Перебирает URL-адреса товаров:
   - Получает аффилированную ссылку для каждого URL-адреса, используя метод `get_affiliate_links` родительского класса `AliApi`.
   - Если аффилированная ссылка найдена, добавляет её в список `_promotion_links` и URL-адрес товара в список `_prod_urls`.
   - Выводит информацию об аффилированной ссылке с помощью функции `pprint`.
   - Если аффилированная ссылка не найдена, логирует информацию об этом с помощью `logger.info_red`.
4. Если список `_promotion_links` пуст, логирует ошибку и возвращает `None`.
5. Получает детали товаров, используя метод `retrieve_product_details` с списком `_prod_urls`.
6. Перебирает товары и их аффилированные ссылки:
   - Если аффилированная ссылка отсутствует, пытается получить её из параметров URL-адреса товара.
   - Если аффилированная ссылка все равно не найдена, удаляет товар с помощью метода `delete_product`.
   - Сохраняет изображение товара, используя функцию `save_png_from_url`, и устанавливает локальный путь к изображению в атрибуте `local_image_path` товара.
   - Если у товара есть видео, сохраняет его, используя функцию `save_video_from_url`, и устанавливает локальный путь к видео в атрибуте `local_video_path` товара.
   - Выводит информацию о полученном товаре с помощью функции `pprint`.
   - Сохраняет данные о товаре в формате JSON, используя функцию `j_dumps`. Если сохранение не удалось, логирует предупреждение.
7. Выводит общее количество обработанных товаров и возвращает список `_affiliate_products`.

### `delete_product`

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

**Назначение**: Удаляет товар, у которого нет аффилированной ссылки.

**Параметры**:
- `product_id` (str): Идентификатор товара, который нужно удалить.
- `exc_info` (bool, optional): Флаг, указывающий, нужно ли логировать информацию об исключении. По умолчанию `False`.

**Как работает функция**:
1. Извлекает идентификатор товара с помощью функции `extract_prod_ids`.
2. Определяет пути к файлам, содержащим список товаров.
3. Читает список товаров из файла `sources.txt`.
4. Если список товаров существует:
   - Преобразует список товаров в однородный список.
   - Перебирает записи в списке товаров:
     - Если удалось извлечь идентификатор товара:
       - Извлекает идентификатор записи.
       - Если идентификатор записи совпадает с идентификатором товара, удаляет запись из списка товаров и сохраняет обновленный список в файл `_sources.txt`.
     - Если не удалось извлечь идентификатор товара, сравнивает запись с идентификатором товара и, если они совпадают, удаляет запись из списка и сохраняет обновленный список в файл `sources.txt`.
5. Если список товаров не существует:
   - Формирует путь к HTML-файлу товара.
   - Переименовывает HTML-файл товара, добавляя к нему суффикс `_`.
   - Логирует успешное переименование файла.
   - В случае возникновения исключений `FileNotFoundError` или `Exception`, логирует ошибку или критическую ошибку соответственно.

## Параметры класса

- `campaign_name` (str): Название рекламной кампании. Используется для организации файлов и данных, связанных с конкретной кампанией.
- `campaign_category` (Optional[str]): Категория кампании. Позволяет дополнительно структурировать данные внутри кампании.
- `campaign_path` (Path): Путь к каталогу кампании, где хранятся все ресурсы и данные, связанные с кампанией.
- `language` (str): Язык, используемый в кампании. Влияет на локализацию контента и сообщений.
- `currency` (str): Валюта, используемая в кампании. Определяет валюту цен и других финансовых показателей.

## Примеры

Пример использования класса `AliAffiliatedProducts`:

```python
from src.suppliers.suppliers_list.aliexpress.affiliated_products_generator import AliAffiliatedProducts

# Пример использования:
prod_urls = ['123','456',...]
prod_urls = ['https://www.aliexpress.com/item/123.html','456',...]

parser = AliAffiliatedProducts(
                            campaign_name='test_campaign',
                            campaign_category='test_category',
                            language='RU',
                            currency='RUB')

products = parser.process_affiliate_products(prod_urls)

if products:
    for product in products:
        print(f"Product ID: {product.product_id}")
        print(f"Promotion Link: {product.promotion_link}")
        print(f"Local Image Path: {product.local_image_path}")
        print(f"Local Video Path: {product.local_video_path}")
```

В этом примере создается экземпляр класса `AliAffiliatedProducts` с указанием названия кампании, категории, языка и валюты. Затем вызывается метод `process_affiliate_products` с списком URL-адресов товаров. Если товары успешно обработаны, выводится информация о каждом товаре, включая его идентификатор, аффилированную ссылку, локальный путь к изображению и локальный путь к видео.
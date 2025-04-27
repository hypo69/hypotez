# `affiliated_products_generator.py` 

## Обзор

Файл `affiliated_products_generator.py` содержит класс `AliAffiliatedProducts`. Этот класс отвечает за получение полных данных о товарах из API AliExpress Affiliate. Он опирается на класс `AliApi` для обработки URL или ID товаров и получения информации о партнерских товарах, включая сохранение изображений, видео и данных JSON.

## Детали

### Импорты и зависимости

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

- **Стандартные библиотеки:** `asyncio`, `itertools`, `math`, `pathlib`, `typing`, `types`, `urllib.parse`
- **Внешние библиотеки:** `src.settings`, `src.suppliers.suppliers_list.aliexpress`, `src.utils.convertor`, `src.utils`, `src.logger`


### Класс `AliAffiliatedProducts`

#### Документация класса

```python
class AliAffiliatedProducts(AliApi):
    """ Класс для сбора полных данных о товарах из URL или ID товаров
    locator_description Для более подробной информации о том, как создавать шаблоны для рекламных кампаний, см. раздел `Управление рекламными кампаниями AliExpress`
    @code
    # Пример использования:
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

- **Цель:** Сбор полных данных о товарах из URL или ID товаров с использованием API AliExpress Affiliate.
- **Пример использования:** Показывает, как инициализировать класс и вызвать метод `_affiliate_product` для обработки URL товаров.

#### Атрибуты

```python
campaign_name: str
campaign_category: Optional[str]
campaign_path: Path
language: str
currency: str
```

- **`campaign_name`**: Название рекламной кампании.
- **`campaign_category`**: Категория для кампании (по умолчанию `None`).
- **`campaign_path`**: Путь к каталогу, где хранятся материалы кампании.
- **`language`**: Язык для кампании (по умолчанию `'EN'`).
- **`currency`**: Валюта для кампании (по умолчанию `'USD'`).

#### Инициализация

```python
def __init__(self,
             campaign_name: str,
             campaign_category: Optional[str] = None,
             language: str = 'EN',
             currency: str = 'USD',
             *args, **kwargs):
    """
    @param campaign_name `str`: Название рекламной кампании. Каталог с подготовленным материалом берется по имени.
    @param campaign_category `Optional[str]`: Категория для кампании (по умолчанию None).
    @param language `str`: Язык для кампании (по умолчанию 'EN').
    @param currency `str`: Валюта для кампании (по умолчанию 'USD').
    @param tracking_id `str`: Tracking ID для AliExpress API.
    """
    super().__init__(language, currency)

    self.campaign_name = campaign_name
    self.campaign_category = campaign_category
    self.language = language
    self.currency = currency
    self.locale = f"{self.language}_{self.currency}"
    self.campaign_path = gs.path.google_drive / 'aliexpress' / 'campaigns' / self.campaign_name / 'categories' / self.campaign_category
```

- **`super().__init__(language, currency)`**: Вызывает конструктор родительского класса `AliApi`.
- **`self.campaign_path`**: Строит путь к каталогу кампании на основе `campaign_name` и `campaign_category`.

#### Методы

##### `process_affiliate_products`

```python
def process_affiliate_products(self, prod_urls: List[str]) -> List[SimpleNamespace]:
    """
    Обрабатывает список URL и возвращает список товаров с партнерскими ссылками и сохраненными изображениями.

    :param prod_urls: Список URL или ID товаров.
    :return: Список обработанных товаров.
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

- **Цель:** Обработать список URL или ID товаров, чтобы получить партнерские ссылки, сохранить изображения и видео, а также сохранить сведения о товарах.
- **Параметры:**
  - **`prod_urls`**: Список URL или ID товаров.
- **Возвращает:** Список объектов `SimpleNamespace`, представляющих обработанные товары.

##### `delete_product`

```python
def delete_product(self, product_id: str, exc_info: bool = False):
    """ Удаляет товар, у которого нет партнерской ссылки"""
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

- **Цель:** Удалить товар, у которого нет партнерской ссылки. 

## Ключевые функциональности

1. **Получение содержимого страницы**: Функция `get_page_content` получает HTML-содержимое заданного URL с использованием библиотеки `requests`, обрабатывая любые возможные HTTP-ошибки.

2. **Получение партнерской ссылки**: Метод вызывает `get_affiliate_links` для получения партнерских ссылок для каждого URL товара.

3. **Получение информации о товаре**: Метод получает сведения о товаре с помощью `retrieve_product_details`.

4. **Сохранение мультимедиа**: Он сохраняет изображения и видео товаров с использованием вспомогательных функций, таких как `save_png_from_url` и `save_video_from_url`.

5. **Ведение журнала**: Метод записывает в журнал различные этапы обработки, включая ошибки и успешные извлечения.

## Единые тесты

Единые тесты предназначены для проверки поведения метода `process_affiliate_products` в различных сценариях:

1. **Успешная обработка**: Проверяет, что метод правильно обрабатывает ID товаров и получает партнерские ссылки и сведения о товарах.

2. **Отсутствие партнерских ссылок**: Проверяет поведение метода, когда партнерские ссылки не найдены, ожидая пустого возврата.

3. **Отсутствие возвращенных товаров**: Проверяет поведение метода, когда сведения о товаре не возвращаются, также ожидая пустого возврата.

## Пример использования

Пример использования в документации класса показывает, как создать экземпляр класса `AliAffiliatedProducts` и вызвать метод `process_affiliate_products` со списком URL или ID товаров.

## Улучшения и соображения

- **Обработка ошибок**: Хотя есть определенная обработка ошибок, можно было бы внести дальнейшие улучшения, чтобы более изящно обрабатывать определенные случаи.
- **Покрытие тестами**: Можно добавить дополнительные тесты для покрытия граничных случаев, таких как неверные URL или сетевые сбои.
- **Производительность**: В зависимости от количества обрабатываемых товаров следует рассмотреть возможность реализации асинхронных запросов для повышения производительности.
- **Документация**: Убедитесь, что код хорошо задокументирован, особенно для публичных методов, чтобы облегчить понимание и использование другими разработчиками.
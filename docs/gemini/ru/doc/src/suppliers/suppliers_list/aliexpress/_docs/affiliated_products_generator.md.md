# Генератор аффилированных продуктов AliExpress

## Обзор

Этот модуль содержит класс `AliAffiliatedProducts`, который используется для сбора полной информации о продуктах с AliExpress Affiliate API. Он основан на классе `AliApi` и позволяет обрабатывать ссылки на продукты или идентификаторы продуктов, чтобы получить подробные сведения об аффилированных продуктах, включая сохранение изображений, видео и данных в формате JSON. 

## Подробней

Модуль `affiliated_products_generator.py`  расположен по адресу `hypotez/src/suppliers/suppliers_list/aliexpress/_docs/affiliated_products_generator.md`. Он предоставляет класс `AliAffiliatedProducts`, который: 

* **Получает аффилированные ссылки для продуктов:** `AliAffiliatedProducts`  использует методы родительского класса `AliApi` для получения аффилированных ссылок для продуктов, используя идентификаторы продуктов или ссылки. 
* **Собирает полную информацию о продуктах:** Извлекает данные о продуктах с AliExpress Affiliate API. 
* **Сохраняет информацию о продуктах:** Сохраняет изображения, видео и данные в формате JSON в соответствующие директории. 

### Пример использования:

```python
# Пример использования
prod_urls = ['123','456',...]
prod_urls = ['https://www.aliexpress.com/item/123.html','456',...]

parser = AliAffiliatedProducts(
    campaign_name, 
    campaign_category, 
    language, 
    currency
)
products = parser._affiliate_product(prod_urls)
```

## Классы

### `AliAffiliatedProducts`

**Описание**: Класс для сбора полной информации о продуктах с использованием AliExpress Affiliate API. 
**Наследует**: `AliApi`
**Атрибуты**:

* `campaign_name` (str): Название рекламной кампании.
* `campaign_category` (Optional[str]): Категория для кампании (по умолчанию `None`).
* `campaign_path` (Path): Путь к каталогу, где хранятся материалы кампании.
* `language` (str): Язык для кампании (по умолчанию `'EN'`).
* `currency` (str): Валюта для кампании (по умолчанию `'USD'`).

**Методы**:

#### `process_affiliate_products`

**Назначение**: Обрабатывает список ссылок на продукты и возвращает список продуктов с аффилированными ссылками и сохраненными изображениями.

**Параметры**:

* `prod_urls` (List[str]): Список ссылок на продукты или идентификаторов продуктов.

**Возвращает**:

* List[SimpleNamespace]: Список обработанных продуктов.

**Пример**:

```python
# Пример использования
prod_urls = ['123','456',...]
prod_urls = ['https://www.aliexpress.com/item/123.html','456',...]

parser = AliAffiliatedProducts(
    campaign_name, 
    campaign_category, 
    language, 
    currency
)
products = parser.process_affiliate_products(prod_urls)
```

**Как работает функция**: 

1. Получает аффилированные ссылки для каждого продукта из списка `prod_urls` с помощью метода `get_affiliate_links` родительского класса `AliApi`.
2. Проверяет,  существуют ли аффилированные ссылки для каждого продукта.
3. Собирает полную информацию о продуктах с AliExpress Affiliate API, используя метод `retrieve_product_details`.
4. Сохраняет изображения и видео с помощью функций `save_png_from_url` и `save_video_from_url`.
5. Сохраняет информацию о продуктах в формате JSON в соответствующие директории.
6. Возвращает список обработанных продуктов.

#### `delete_product`

**Назначение**: Удаляет продукт, у которого нет аффилированной ссылки.

**Параметры**:

* `product_id` (str): Идентификатор продукта.
* `exc_info` (bool, optional): Флаг, указывающий, нужно ли выводить информацию об исключении. По умолчанию `False`.

**Пример**:

```python
# Пример использования
product_id = '123'
parser.delete_product(product_id)
```

**Как работает функция**: 

1. Извлекает идентификатор продукта с помощью функции `extract_prod_ids`.
2. Проверяет, существует ли файл с информацией о продукте в директории `sources.txt`.
3. Если файл существует, удаляет информацию о продукте из файла и сохраняет обновленный файл.
4. Если файл не существует, переименовывает файл с информацией о продукте в директории `sources` в файл с суффиксом `_`.
5. Логирует успешное удаление или ошибку удаления.

## Параметры класса

* `campaign_name` (str): Название рекламной кампании.
* `campaign_category` (Optional[str]): Категория для кампании (по умолчанию `None`).
* `campaign_path` (Path): Путь к каталогу, где хранятся материалы кампании.
* `language` (str): Язык для кампании (по умолчанию `'EN'`).
* `currency` (str): Валюта для кампании (по умолчанию `'USD'`).

## Примеры

```python
# Создание экземпляра класса AliAffiliatedProducts
parser = AliAffiliatedProducts(
    campaign_name='MyCampaign',
    campaign_category='Electronics',
    language='EN',
    currency='USD'
)

# Обработка списка ссылок на продукты
prod_urls = ['https://www.aliexpress.com/item/123.html', 'https://www.aliexpress.com/item/456.html']
products = parser.process_affiliate_products(prod_urls)

# Вывод информации о продуктах
for product in products:
    print(f"Product ID: {product.product_id}")
    print(f"Product Title: {product.product_title}")
    print(f"Product URL: {product.product_url}")
    print(f"Affiliate Link: {product.promotion_link}")
    print(f"Image Path: {product.local_image_path}")
    print(f"Video Path: {product.local_video_path}")
```

##  Логгирование

В модуле используется `logger` из `src.logger.logger` для записи информации о ходе выполнения. 

##  Дополнительно

* **Обработка ошибок:** В коде присутствует базовая обработка ошибок, однако ее можно расширить для более корректной обработки исключительных ситуаций.
* **Тестовое покрытие:**  Модуль содержит модульные тесты для метода `process_affiliate_products`, но можно добавить больше тестов для покрытия всех сценариев.
* **Производительность:** При обработке большого количества продуктов стоит рассмотреть использование асинхронных запросов для повышения производительности.
* **Документация:** Необходимо убедиться, что код хорошо задокументирован, особенно для публичных методов, чтобы другие разработчики могли легко понять, как его использовать. 

```python
# Пример использования logger
logger.info('Some information message')
try:
    # ...
except SomeError as ex:
    logger.error('Some error message', ex, exc_info=True)
# Модуль тестирования генератора аффилированных товаров AliExpress

## Обзор

Данный модуль содержит набор тестов для проверки функциональности генератора аффилированных товаров AliExpress, реализованного в классе `AliAffiliatedProducts`. Модуль обеспечивает тестирование основных методов класса, включая `check_and_process_affiliate_products` и `process_affiliate_products`.

## Детали

Модуль использует библиотеку `pytest` для запуска тестов и `unittest.mock` для имитации внешних зависимостей. 

## Классы

### `AliAffiliatedProducts`

**Описание**: Класс `AliAffiliatedProducts` используется для генерации аффилированных товаров AliExpress.

**Атрибуты**:
- `campaign_name` (str): Название кампании.
- `category_name` (str): Название категории.
- `language` (str): Язык.
- `currency` (str): Валюта.

**Методы**:
- `check_and_process_affiliate_products(prod_urls: list) -> None`: Проверяет URL-адреса товаров и вызывает метод `process_affiliate_products` для обработки.
- `process_affiliate_products(prod_urls: list) -> list`: Обрабатывает URL-адреса товаров, извлекает информацию о товарах и возвращает список обработанных товаров.

## Тесты

### `test_check_and_process_affiliate_products(ali_affiliated_products)`

**Цель**: Проверить, что метод `check_and_process_affiliate_products` правильно вызывает метод `process_affiliate_products`.

**Параметры**:
- `ali_affiliated_products`: Экземпляр класса `AliAffiliatedProducts`.

**Функциональность**:
- Использует `patch.object` для имитации метода `process_affiliate_products`.
- Вызывает метод `check_and_process_affiliate_products` с тестовыми URL-адресами.
- Проверяет, что метод `process_affiliate_products` был вызван один раз.

### `test_process_affiliate_products(ali_affiliated_products)`

**Цель**: Проверить, что метод `process_affiliate_products` правильно обрабатывает товары.

**Параметры**:
- `ali_affiliated_products`: Экземпляр класса `AliAffiliatedProducts`.

**Функциональность**:
- Использует `patch.object` для имитации метода `retrieve_product_details`, а также для имитации функций `ensure_https`, `save_image_from_url`, `save_video_from_url` и `j_dumps`.
- Вызывает метод `process_affiliate_products` с тестовыми URL-адресами.
- Проверяет, что количество обработанных товаров соответствует ожидаемому значению.
- Проверяет, что атрибуты обработанных товаров соответствуют ожидаемым значениям.


## Функции

### `ali_affiliated_products`

**Описание**: Фикстура pytest, возвращающая экземпляр класса `AliAffiliatedProducts`.

**Параметры**:
- Нет.

**Возвращает**:
- Экземпляр класса `AliAffiliatedProducts`.

**Функциональность**:
- Создает экземпляр класса `AliAffiliatedProducts` с тестовыми данными.

## Примеры

```python
# Тестирование метода check_and_process_affiliate_products
def test_check_and_process_affiliate_products(ali_affiliated_products):
    with patch.object(ali_affiliated_products, 'process_affiliate_products') as mock_process:
        ali_affiliated_products.check_and_process_affiliate_products(prod_urls)
        mock_process.assert_called_once_with(prod_urls)

# Тестирование метода process_affiliate_products
def test_process_affiliate_products(ali_affiliated_products):
    mock_product_details = [SimpleNamespace(product_id="123", promotion_link="promo_link", product_main_image_url="image_url", product_video_url="video_url")]

    with patch.object(ali_affiliated_products, 'retrieve_product_details', return_value=mock_product_details) as mock_retrieve, \
         patch("src.suppliers.suppliers_list.aliexpress.affiliated_products_generator.ensure_https", return_value=prod_urls), \
         patch("src.suppliers.suppliers_list.aliexpress.affiliated_products_generator.save_image_from_url"), \
         patch("src.suppliers.suppliers_list.aliexpress.affiliated_products_generator.save_video_from_url"), \
         patch("src.suppliers.suppliers_list.aliexpress.affiliated_products_generator.j_dumps", return_value=True):

        processed_products = ali_affiliated_products.process_affiliate_products(prod_urls)

        assert len(processed_products) == 1
        assert processed_products[0].product_id == "123"
```

## Примечания

- Модуль использует тестовые данные, которые определены в начале файла.
- Тесты используют патчи для имитации внешних зависимостей, таких как `retrieve_product_details`, `ensure_https`, `save_image_from_url`, `save_video_from_url` и `j_dumps`.
- Тесты проверяют, что методы класса `AliAffiliatedProducts` работают правильно.
- Модуль содержит фикстуру pytest `ali_affiliated_products`, которая возвращает экземпляр класса `AliAffiliatedProducts`.
- Тесты содержат примеры вызовов функций и методов.
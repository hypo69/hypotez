# Модуль для тестирования генератора аффилированных товаров AliExpress

## Обзор

Этот модуль содержит набор тестов для генератора аффилированных товаров AliExpress, реализованного в модуле `src.suppliers.suppliers_list.aliexpress.affiliated_products_generator`. Тесты покрывают функции `check_and_process_affiliate_products` и `process_affiliate_products`.

## Подробней

Модуль использует `pytest` для запуска тестов и `unittest.mock` для имитации внешних зависимостей, таких как `retrieve_product_details` и `ensure_https`. 

## Классы

### `AliAffiliatedProducts`

**Описание**: Класс для работы с аффилированными товарами AliExpress.

**Атрибуты**:

- `campaign_name` (str): Имя кампании.
- `category_name` (str): Название категории.
- `language` (str): Язык.
- `currency` (str): Валюта.

**Методы**:

- `check_and_process_affiliate_products(prod_urls)`: Проверяет ссылки на товары и запускает обработку, если они валидны.
- `process_affiliate_products(prod_urls)`: Обрабатывает список URL товаров, извлекая информацию о каждом товаре.

## Функции

### `ali_affiliated_products`

**Назначение**: Фикстура pytest, которая возвращает экземпляр класса `AliAffiliatedProducts`.

**Параметры**:

- `None`

**Возвращает**:

- `AliAffiliatedProducts`: Экземпляр класса `AliAffiliatedProducts`.

**Примеры**:

```python
def test_check_and_process_affiliate_products(ali_affiliated_products):
    # ...
```

### `test_check_and_process_affiliate_products`

**Назначение**: Тестирует метод `check_and_process_affiliate_products`, проверяя, что он правильно вызывает метод `process_affiliate_products`.

**Параметры**:

- `ali_affiliated_products`: Фикстура pytest, возвращающая экземпляр класса `AliAffiliatedProducts`.

**Возвращает**:

- `None`

**Вызывает исключения**:

- `None`

**Примеры**:

```python
def test_check_and_process_affiliate_products(ali_affiliated_products):
    with patch.object(ali_affiliated_products, 'process_affiliate_products') as mock_process:
        ali_affiliated_products.check_and_process_affiliate_products(prod_urls)
        mock_process.assert_called_once_with(prod_urls)
```

**Как работает функция**:

- Имитирует метод `process_affiliate_products` с помощью `patch.object`.
- Вызывает метод `check_and_process_affiliate_products` с тестовыми данными.
- Проверяет, что `process_affiliate_products` был вызван один раз с правильным аргументом.

### `test_process_affiliate_products`

**Назначение**: Тестирует метод `process_affiliate_products`, проверяя, что он правильно обрабатывает список URL товаров.

**Параметры**:

- `ali_affiliated_products`: Фикстура pytest, возвращающая экземпляр класса `AliAffiliatedProducts`.

**Возвращает**:

- `None`

**Вызывает исключения**:

- `None`

**Примеры**:

```python
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

**Как работает функция**:

- Имитирует методы `retrieve_product_details`, `ensure_https`, `save_image_from_url`, `save_video_from_url` и `j_dumps` с помощью `patch`.
- Вызывает метод `process_affiliate_products` с тестовыми данными.
- Проверяет, что количество обработанных товаров соответствует ожидаемому, и что атрибуты обработанного товара соответствуют тестовым данным.

## Параметры

- `campaign_name` (str): Имя кампании.
- `category_name` (str): Название категории.
- `language` (str): Язык.
- `currency` (str): Валюта.
- `prod_urls` (list): Список URL товаров.

## Примеры

```python
# Создание экземпляра класса AliAffiliatedProducts
ali_affiliated_products = AliAffiliatedProducts(campaign_name, category_name, language, currency)

# Запуск проверки и обработки URL товаров
ali_affiliated_products.check_and_process_affiliate_products(prod_urls)

# Обработка URL товаров
processed_products = ali_affiliated_products.process_affiliate_products(prod_urls)
```
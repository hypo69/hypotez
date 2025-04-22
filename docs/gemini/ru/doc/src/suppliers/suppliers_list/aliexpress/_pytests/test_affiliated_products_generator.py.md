# Модуль `test_affiliated_products_generator.py`

## Обзор

Модуль содержит набор тестов для проверки функциональности класса `AliAffiliatedProducts`, который отвечает за генерацию информации о партнерских товарах из AliExpress. Тесты проверяют правильность обработки ссылок на товары, извлечение деталей о товарах и сохранение полученной информации.

## Подробней

Этот модуль использует библиотеку `pytest` для организации и запуска тестов. Он также использует `unittest.mock` для создания мок-объектов, которые заменяют внешние зависимости и позволяют изолировать тестируемый код. Модуль содержит фикстуру `ali_affiliated_products`, которая создает экземпляр класса `AliAffiliatedProducts` с предопределенными параметрами, а также два тестовых случая: `test_check_and_process_affiliate_products` и `test_process_affiliate_products`.
Тесты имитируют вызовы внешних функций и проверяют, что методы класса `AliAffiliatedProducts` вызываются с правильными аргументами и возвращают ожидаемые результаты.

## Фикстуры

### `ali_affiliated_products`

```python
@pytest.fixture
def ali_affiliated_products():
    """
    Создает и возвращает экземпляр класса `AliAffiliatedProducts` с заданными параметрами.

    Returns:
        AliAffiliatedProducts: Экземпляр класса `AliAffiliatedProducts`.
    """
    return AliAffiliatedProducts(campaign_name, category_name, language, currency)
```

**Назначение**: Фикстура создает экземпляр класса `AliAffiliatedProducts`, который используется в тестах.

**Параметры**:

-   `campaign_name` (str): Имя рекламной кампании.
-   `category_name` (str): Имя категории товара.
-   `language` (str): Язык.
-   `currency` (str): Валюта.

**Возвращает**:

-   `AliAffiliatedProducts`: Экземпляр класса `AliAffiliatedProducts`.

**Пример**:

```python
@pytest.fixture
def ali_affiliated_products():
    return AliAffiliatedProducts("sample_campaign", "sample_category", "EN", "USD")
```

## Функции

### `test_check_and_process_affiliate_products`

```python
def test_check_and_process_affiliate_products(ali_affiliated_products):
    """
    Тестирует метод `check_and_process_affiliate_products` класса `AliAffiliatedProducts`.

    Args:
        ali_affiliated_products: Фикстура, предоставляющая экземпляр класса `AliAffiliatedProducts`.
    """
    with patch.object(ali_affiliated_products, 'process_affiliate_products') as mock_process:
        ali_affiliated_products.check_and_process_affiliate_products(prod_urls)
        mock_process.assert_called_once_with(prod_urls)
```

**Назначение**: Проверяет, что метод `check_and_process_affiliate_products` вызывает метод `process_affiliate_products` с правильными аргументами.

**Параметры**:

-   `ali_affiliated_products`: Фикстура, предоставляющая экземпляр класса `AliAffiliatedProducts`.

**Как работает функция**:

1.  Используется `patch.object` для замены метода `process_affiliate_products` мок-объектом `mock_process`.
2.  Вызывается метод `check_and_process_affiliate_products` с тестовыми URL-ами товаров (`prod_urls`).
3.  Проверяется, что метод `process_affiliate_products` был вызван один раз с аргументом `prod_urls` с помощью `mock_process.assert_called_once_with(prod_urls)`.

**Пример**:

```python
def test_check_and_process_affiliate_products(ali_affiliated_products):
    with patch.object(ali_affiliated_products, 'process_affiliate_products') as mock_process:
        ali_affiliated_products.check_and_process_affiliate_products(["https://www.aliexpress.com/item/123.html", "456"])
        mock_process.assert_called_once_with(["https://www.aliexpress.com/item/123.html", "456"])
```

### `test_process_affiliate_products`

```python
def test_process_affiliate_products(ali_affiliated_products):
    """
    Тестирует метод `process_affiliate_products` класса `AliAffiliatedProducts`.

    Args:
        ali_affiliated_products: Фикстура, предоставляющая экземпляр класса `AliAffiliatedProducts`.
    """
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

**Назначение**: Проверяет, что метод `process_affiliate_products` правильно обрабатывает данные о товарах и возвращает ожидаемый результат.

**Параметры**:

-   `ali_affiliated_products`: Фикстура, предоставляющая экземпляр класса `AliAffiliatedProducts`.

**Как работает функция**:

1.  Создается список `mock_product_details`, содержащий мок-объекты с деталями о товаре.
2.  Используется `patch.object` для замены метода `retrieve_product_details` мок-объектом `mock_retrieve`, который возвращает `mock_product_details`.
3.  Используются `patch` для замены функций `ensure_https`, `save_image_from_url`, `save_video_from_url` и `j_dumps` мок-объектами, возвращающими предопределенные значения.
4.  Вызывается метод `process_affiliate_products` с тестовыми URL-ами товаров (`prod_urls`).
5.  Проверяется, что длина возвращаемого списка `processed_products` равна 1 и что `product_id` первого элемента равен "123".

**Пример**:

```python
def test_process_affiliate_products(ali_affiliated_products):
    mock_product_details = [SimpleNamespace(product_id="123", promotion_link="promo_link", product_main_image_url="image_url", product_video_url="video_url")]

    with patch.object(ali_affiliated_products, 'retrieve_product_details', return_value=mock_product_details) as mock_retrieve, \
         patch("src.suppliers.suppliers_list.aliexpress.affiliated_products_generator.ensure_https", return_value=["https://www.aliexpress.com/item/123.html", "456"]), \
         patch("src.suppliers.suppliers_list.aliexpress.affiliated_products_generator.save_image_from_url"), \
         patch("src.suppliers.suppliers_list.aliexpress.affiliated_products_generator.save_video_from_url"), \
         patch("src.suppliers.suppliers_list.aliexpress.affiliated_products_generator.j_dumps", return_value=True):

        processed_products = ali_affiliated_products.process_affiliate_products(["https://www.aliexpress.com/item/123.html", "456"])

        assert len(processed_products) == 1
        assert processed_products[0].product_id == "123"
```
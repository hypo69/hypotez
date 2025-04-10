# Модуль для тестирования генерации партнерских товаров AliExpress

## Обзор

Модуль содержит тесты для проверки функциональности класса `AliAffiliatedProducts`, который используется для генерации партнерских товаров AliExpress. Тесты проверяют корректность обработки и преобразования данных о товарах, а также взаимодействие с внешними зависимостями.

## Подробней

Этот файл содержит тесты, проверяющие правильность работы методов `check_and_process_affiliate_products` и `process_affiliate_products` класса `AliAffiliatedProducts`. Для изоляции тестов используются моки внешних зависимостей. Расположение файла в директории `src/suppliers/aliexpress/_pytests` указывает на то, что это набор тестов для модуля, отвечающего за работу с AliExpress в контексте поставщиков товаров.

## Fixtures

### `ali_affiliated_products`

```python
@pytest.fixture
def ali_affiliated_products():
    return AliAffiliatedProducts(campaign_name, category_name, language, currency)
```

Фикстура создает экземпляр класса `AliAffiliatedProducts` с предопределенными параметрами.

**Назначение**: Предоставляет тестовый экземпляр класса `AliAffiliatedProducts` для использования в тестах.

**Параметры**:
-   `campaign_name` (str): Имя кампании.
-   `category_name` (str): Имя категории.
-   `language` (str): Язык.
-   `currency` (str): Валюта.

**Возвращает**:
-   `AliAffiliatedProducts`: Экземпляр класса `AliAffiliatedProducts`.

**Как работает фикстура**:
Фикстура создает и возвращает экземпляр класса `AliAffiliatedProducts`, используя предопределенные значения для имени кампании, имени категории, языка и валюты. Это позволяет избежать повторения кода инициализации в каждом тесте и обеспечивает консистентность тестовой среды.

## Функции

### `test_check_and_process_affiliate_products`

```python
def test_check_and_process_affiliate_products(ali_affiliated_products):
    with patch.object(ali_affiliated_products, 'process_affiliate_products') as mock_process:
        ali_affiliated_products.check_and_process_affiliate_products(prod_urls)
        mock_process.assert_called_once_with(prod_urls)
```

Тест проверяет, что метод `check_and_process_affiliate_products` вызывает метод `process_affiliate_products` с правильными аргументами.

**Назначение**: Проверка вызова метода `process_affiliate_products` методом `check_and_process_affiliate_products`.

**Параметры**:
-   `ali_affiliated_products` (AliAffiliatedProducts): Фикстура, предоставляющая экземпляр класса `AliAffiliatedProducts`.

**Как работает функция**:
1.  Используется `patch.object` для мокирования метода `process_affiliate_products` экземпляра `ali_affiliated_products`.
2.  Вызывается метод `check_and_process_affiliate_products` с предопределенным списком URL-адресов товаров (`prod_urls`).
3.  С помощью `mock_process.assert_called_once_with(prod_urls)` проверяется, что мокированный метод `process_affiliate_products` был вызван ровно один раз и с правильным аргументом (`prod_urls`).

**Примеры**:

```python
def test_check_and_process_affiliate_products(ali_affiliated_products):
    with patch.object(ali_affiliated_products, 'process_affiliate_products') as mock_process:
        ali_affiliated_products.check_and_process_affiliate_products(prod_urls)
        mock_process.assert_called_once_with(prod_urls)
```

### `test_process_affiliate_products`

```python
def test_process_affiliate_products(ali_affiliated_products):
    mock_product_details = [SimpleNamespace(product_id="123", promotion_link="promo_link", product_main_image_url="image_url", product_video_url="video_url")]
    
    with patch.object(ali_affiliated_products, 'retrieve_product_details', return_value=mock_product_details) as mock_retrieve, \
         patch("src.suppliers.aliexpress.affiliated_products_generator.ensure_https", return_value=prod_urls), \
         patch("src.suppliers.aliexpress.affiliated_products_generator.save_image_from_url"), \
         patch("src.suppliers.aliexpress.affiliated_products_generator.save_video_from_url"), \
         patch("src.suppliers.aliexpress.affiliated_products_generator.j_dumps", return_value=True):
        
        processed_products = ali_affiliated_products.process_affiliate_products(prod_urls)
        
        assert len(processed_products) == 1
        assert processed_products[0].product_id == "123"
```

Тест проверяет, что метод `process_affiliate_products` правильно обрабатывает данные о товарах и возвращает ожидаемый результат.

**Назначение**: Проверка обработки данных о товарах в методе `process_affiliate_products`.

**Параметры**:
-   `ali_affiliated_products` (AliAffiliatedProducts): Фикстура, предоставляющая экземпляр класса `AliAffiliatedProducts`.

**Как работает функция**:

1.  Создается `mock_product_details` - список объектов `SimpleNamespace`, имитирующих детали товара, возвращаемые методом `retrieve_product_details`.
2.  Используется `patch.object` для мокирования метода `retrieve_product_details` экземпляра `ali_affiliated_products`, возвращающего `mock_product_details`.
3.  Также мокируются функции `ensure_https`, `save_image_from_url`, `save_video_from_url` и `j_dumps` из модуля `src.suppliers.aliexpress.affiliated_products_generator`.
4.  Вызывается метод `process_affiliate_products` с предопределенным списком URL-адресов товаров (`prod_urls`).
5.  Проверяется, что длина списка обработанных товаров равна 1 и что `product_id` первого элемента равен "123".

**Примеры**:

```python
def test_process_affiliate_products(ali_affiliated_products):
    mock_product_details = [SimpleNamespace(product_id="123", promotion_link="promo_link", product_main_image_url="image_url", product_video_url="video_url")]
    
    with patch.object(ali_affiliated_products, 'retrieve_product_details', return_value=mock_product_details) as mock_retrieve, \
         patch("src.suppliers.aliexpress.affiliated_products_generator.ensure_https", return_value=prod_urls), \
         patch("src.suppliers.aliexpress.affiliated_products_generator.save_image_from_url"), \
         patch("src.suppliers.aliexpress.affiliated_products_generator.save_video_from_url"), \
         patch("src.suppliers.aliexpress.affiliated_products_generator.j_dumps", return_value=True):
        
        processed_products = ali_affiliated_products.process_affiliate_products(prod_urls)
        
        assert len(processed_products) == 1
        assert processed_products[0].product_id == "123"
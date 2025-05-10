# Модуль тестирования партнерских товаров Aliexpress

## Обзор

Этот модуль содержит тесты для проверки функциональности класса `AliAffiliatedProducts`, который генерирует партнерские товары из Aliexpress. Он включает фикстуру для создания экземпляра класса `AliAffiliatedProducts` и тесты для проверки методов `check_and_process_affiliate_products` и `process_affiliate_products`. Тесты имитируют внешние зависимости и проверяют правильность обработки товаров.

## Подробнее

Модуль содержит тесты, проверяющие корректность работы класса `AliAffiliatedProducts`.
В частности, проверяется вызов метода `process_affiliate_products` из метода `check_and_process_affiliate_products`,
а также логика обработки товаров в методе `process_affiliate_products`.

## Фикстуры

### `ali_affiliated_products`

**Описание**: Фикстура создает и возвращает экземпляр класса `AliAffiliatedProducts`.

**Параметры**:

-   `campaign_name` (str): Название кампании.
-   `category_name` (str): Название категории.
-   `language` (str): Язык.
-   `currency` (str): Валюта.

**Принцип работы**:

Фикстура создает экземпляр класса `AliAffiliatedProducts` с заданными параметрами и возвращает его.
Это позволяет использовать один и тот же экземпляр класса в нескольких тестах.

```python
@pytest.fixture
def ali_affiliated_products():
    return AliAffiliatedProducts(campaign_name, category_name, language, currency)
```

## Тесты

### `test_check_and_process_affiliate_products`

**Назначение**: Проверяет, что метод `check_and_process_affiliate_products` вызывает метод `process_affiliate_products` с правильными аргументами.

**Параметры**:

-   `ali_affiliated_products` (AliAffiliatedProducts): Экземпляр класса `AliAffiliatedProducts`, предоставленный фикстурой.

**Как работает функция**:

-   Имитирует метод `process_affiliate_products` с помощью `patch.object`.
-   Вызывает метод `check_and_process_affiliate_products` с заданными URL-адресами товаров.
-   Проверяет, что метод `process_affiliate_products` был вызван один раз с правильными аргументами.

```python
def test_check_and_process_affiliate_products(ali_affiliated_products):
    with patch.object(ali_affiliated_products, 'process_affiliate_products') as mock_process:
        ali_affiliated_products.check_and_process_affiliate_products(prod_urls)
        mock_process.assert_called_once_with(prod_urls)
```

### `test_process_affiliate_products`

**Назначение**: Проверяет, что метод `process_affiliate_products` правильно обрабатывает товары и возвращает ожидаемый результат.

**Параметры**:

-   `ali_affiliated_products` (AliAffiliatedProducts): Экземпляр класса `AliAffiliatedProducts`, предоставленный фикстурой.

**Как работает функция**:

1.  Определяет `mock_product_details` - имитированный список с деталями товара, содержащий объекты `SimpleNamespace` с данными о товаре, такими как `product_id`, `promotion_link`, `product_main_image_url` и `product_video_url`.

2.  Имитирует несколько внешних зависимостей:
    -   `retrieve_product_details`: имитируется метод, возвращающий `mock_product_details`.
    -   `ensure_https`: имитируется функция, возвращающая список `prod_urls`.
    -   `save_image_from_url`: имитируется функция сохранения изображения.
    -   `save_video_from_url`: имитируется функция сохранения видео.
    -   `j_dumps`: имитируется функция, возвращающая `True`.

3.  Вызывает метод `process_affiliate_products` с заданными URL-адресами товаров (`prod_urls`).

4.  Проверяет, что возвращенный список содержит один элемент и что `product_id` этого элемента равен "123".

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
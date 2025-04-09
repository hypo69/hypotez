# Модуль `test_affiliated_products_generator.py`

## Обзор

Этот модуль содержит набор тестов для класса `AliAffiliatedProducts`, который отвечает за генерацию партнерских продуктов AliExpress. Тесты проверяют правильность обработки и преобразования данных о продуктах, а также взаимодействие с внешними зависимостями.

## Подробней

Модуль использует библиотеку `pytest` для организации и запуска тестов. В частности, определена фикстура `ali_affiliated_products`, которая создает экземпляр класса `AliAffiliatedProducts` с предопределенными параметрами. Тесты используют моки для имитации поведения внешних функций и методов, что позволяет изолированно проверять логику класса `AliAffiliatedProducts`.

## Функции

### `ali_affiliated_products`

```python
@pytest.fixture
def ali_affiliated_products():
    return AliAffiliatedProducts(campaign_name, category_name, language, currency)
```

**Назначение**: Фикстура `pytest`, создающая экземпляр класса `AliAffiliatedProducts` с заданными параметрами.

**Параметры**:
- Отсутствуют, но фикстура использует глобальные переменные `campaign_name`, `category_name`, `language` и `currency` для инициализации объекта `AliAffiliatedProducts`.

**Возвращает**:
- `AliAffiliatedProducts`: Экземпляр класса `AliAffiliatedProducts`.

**Как работает фикстура**:

1.  Создается экземпляр класса `AliAffiliatedProducts` с использованием предопределенных значений `campaign_name`, `category_name`, `language` и `currency`.
2.  Возвращается созданный экземпляр.

```
Создание экземпляра AliAffiliatedProducts
↓
Возврат экземпляра
```

### `test_check_and_process_affiliate_products`

```python
def test_check_and_process_affiliate_products(ali_affiliated_products):
    with patch.object(ali_affiliated_products, 'process_affiliate_products') as mock_process:
        ali_affiliated_products.check_and_process_affiliate_products(prod_urls)
        mock_process.assert_called_once_with(prod_urls)
```

**Назначение**: Тест проверяет, что метод `check_and_process_affiliate_products` вызывает метод `process_affiliate_products` с правильными аргументами.

**Параметры**:
- `ali_affiliated_products`: Фикстура `pytest`, предоставляющая экземпляр класса `AliAffiliatedProducts`.

**Возвращает**:
- Ничего. Тест проверяет, что метод `process_affiliate_products` был вызван с ожидаемыми аргументами.

**Как работает тест**:

1.  Используется `patch.object` для мокирования метода `process_affiliate_products` экземпляра `ali_affiliated_products`.
2.  Вызывается метод `check_and_process_affiliate_products` с предопределенными URL (`prod_urls`).
3.  Проверяется, что мокированный метод `process_affiliate_products` был вызван ровно один раз с аргументом `prod_urls`.

```
Мокирование process_affiliate_products
↓
Вызов check_and_process_affiliate_products с prod_urls
↓
Проверка вызова mock_process с prod_urls
```

**Примеры**:

```python
# Пример вызова функции в тестовом контексте
def test_example(ali_affiliated_products):
    ali_affiliated_products.check_and_process_affiliate_products(["http://example.com/item/123.html"])
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

**Назначение**: Тест проверяет, что метод `process_affiliate_products` правильно обрабатывает продукты, возвращает корректные результаты и взаимодействует с мокированными внешними функциями.

**Параметры**:
- `ali_affiliated_products`: Фикстура `pytest`, предоставляющая экземпляр класса `AliAffiliatedProducts`.

**Возвращает**:
- Ничего. Тест проверяет длину и содержимое списка обработанных продуктов.

**Как работает тест**:

1.  Создается `mock_product_details` - имитация деталей продукта, возвращаемая методом `retrieve_product_details`.
2.  Используется `patch.object` для мокирования метода `retrieve_product_details` экземпляра `ali_affiliated_products`, а также функций `ensure_https`, `save_image_from_url`, `save_video_from_url` и `j_dumps`.
3.  Вызывается метод `process_affiliate_products` с предопределенными URL (`prod_urls`).
4.  Проверяется, что длина возвращенного списка `processed_products` равна 1, и что `product_id` первого элемента равен "123".

```
Создание mock_product_details
↓
Мокирование retrieve_product_details, ensure_https, save_image_from_url, save_video_from_url, j_dumps
↓
Вызов process_affiliate_products с prod_urls
↓
Проверка длины processed_products и product_id
```

**Примеры**:

```python
# Пример вызова функции в тестовом контексте
def test_example(ali_affiliated_products):
    result = ali_affiliated_products.process_affiliate_products(["http://example.com/item/123.html"])
    if result:
        print(f"Обработанные продукты: {result}")
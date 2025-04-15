# Модуль `test_affiliated_products_generator.py`

## Обзор

Этот модуль содержит тесты для класса `AliAffiliatedProducts`, который отвечает за генерацию партнерских продуктов AliExpress. Он включает в себя фикстуру `ali_affiliated_products` и два теста: `test_check_and_process_affiliate_products` и `test_process_affiliate_products`. Тесты проверяют правильность обработки и подготовки данных о партнерских продуктах.

## Подробней

Модуль содержит тесты, проверяющие логику обработки аффилированных продуктов AliExpress. Тесты используют `unittest.mock` для изоляции тестируемого кода от внешних зависимостей и проверки правильности вызовов методов и обработки данных. Расположение модуля в структуре проекта указывает на то, что он относится к тестам для функциональности, связанной с AliExpress.

## Классы

В этом модуле нет классов, но используется класс `AliAffiliatedProducts` из модуля `affiliated_products_generator`.

## Фикстуры

### `ali_affiliated_products`

```python
@pytest.fixture
def ali_affiliated_products():
    return AliAffiliatedProducts(campaign_name, category_name, language, currency)
```

**Назначение**:
Фикстура создает экземпляр класса `AliAffiliatedProducts` с предопределенными параметрами.

**Параметры**:
- `campaign_name` (str): Имя кампании.
- `category_name` (str): Имя категории.
- `language` (str): Язык.
- `currency` (str): Валюта.

**Возвращает**:
- `AliAffiliatedProducts`: Объект класса `AliAffiliatedProducts`.

**Принцип работы**:
Фикстура инициализирует класс `AliAffiliatedProducts` с заранее заданными параметрами, чтобы использовать его в тестах.

**Примеры**:
```python
def test_something(ali_affiliated_products):
    # Используем ali_affiliated_products в тесте
    pass
```

## Функции

### `test_check_and_process_affiliate_products`

```python
def test_check_and_process_affiliate_products(ali_affiliated_products):
    with patch.object(ali_affiliated_products, 'process_affiliate_products') as mock_process:
        ali_affiliated_products.check_and_process_affiliate_products(prod_urls)
        mock_process.assert_called_once_with(prod_urls)
```

**Назначение**:
Тест проверяет, что метод `check_and_process_affiliate_products` вызывает метод `process_affiliate_products` с правильными аргументами.

**Параметры**:
- `ali_affiliated_products`: Фикстура, предоставляющая экземпляр класса `AliAffiliatedProducts`.

**Как работает функция**:
- Используется `patch.object` для замены метода `process_affiliate_products` мок-объектом (`mock_process`).
- Вызывается метод `check_and_process_affiliate_products` с параметром `prod_urls`.
- Проверяется, что `mock_process` был вызван ровно один раз с аргументом `prod_urls` с помощью `mock_process.assert_called_once_with(prod_urls)`.

**Примеры**:
```python
def test_check_and_process_affiliate_products(ali_affiliated_products):
    # Пример вызова теста
    pass
```

### `test_process_affiliate_products`

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

**Назначение**:
Тест проверяет, что метод `process_affiliate_products` правильно обрабатывает продукты и возвращает ожидаемый результат.

**Параметры**:
- `ali_affiliated_products`: Фикстура, предоставляющая экземпляр класса `AliAffiliatedProducts`.

**Как работает функция**:
- Создается моковый объект `mock_product_details`, имитирующий детали продукта.
- Используется контекстный менеджер `with patch.object` для замены метода `retrieve_product_details` мок-объектом `mock_retrieve`, который возвращает `mock_product_details`.
- Используются `patch` для замены функций `ensure_https`, `save_image_from_url`, `save_video_from_url` и `j_dumps` мок-объектами.
- Вызывается метод `process_affiliate_products` с параметром `prod_urls`.
- Проверяется, что длина списка `processed_products` равна 1, и что `product_id` первого элемента равен "123".

**Примеры**:
```python
def test_process_affiliate_products(ali_affiliated_products):
    # Пример вызова теста
    pass
```

## Main

```python
if __name__ == "__main__":
    pytest.main()
```

**Назначение**:
Этот блок кода запускает тесты, если скрипт запускается напрямую.

**Как работает функция**:
- Вызывается функция `pytest.main()`, которая запускает все тесты в текущем модуле.
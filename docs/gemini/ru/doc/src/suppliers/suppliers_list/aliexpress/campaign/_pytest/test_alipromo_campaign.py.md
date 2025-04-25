# Модуль тестирования AliPromoCampaign

## Обзор

Этот модуль содержит юнит-тесты для класса `AliPromoCampaign`, который отвечает за обработку кампаний на AliExpress. 

## Подробности

Тесты охватывают различные аспекты функциональности `AliPromoCampaign`, включая:

- Инициализацию кампании: `test_initialize_campaign`.
- Извлечение продуктов из категорий: `test_get_category_products_no_json_files`, `test_get_category_products_with_json_files`.
- Создание пространств имен для продуктов, категорий и кампаний: `test_create_product_namespace`, `test_create_category_namespace`, `test_create_campaign_namespace`.
- Подготовку продуктов: `test_prepare_products`.
- Извлечение данных о продуктах: `test_fetch_product_data`.
- Сохранение данных о продуктах: `test_save_product`.
- Вывод списка продуктов кампании: `test_list_campaign_products`.

## Тесты

### `test_initialize_campaign`

**Назначение**: Проверяет, что метод `initialize_campaign` правильно инициализирует данные кампании.

**Параметры**:

- `mocker`: Мокинг фреймворк для создания тестовых зависимостей.
- `campaign`: Экземпляр `AliPromoCampaign`.

**Возвращает**: 
- `None`.

**Пример**:

```python
# Тестовые данные для инициализации кампании
mock_json_data = {
    "name": "test_campaign",
    "title": "Test Campaign",
    "language": "EN",
    "currency": "USD",
    "category": {
        "test_category": {
            "name": "test_category",
            "tags": "tag1, tag2",
            "products": [],
            "products_count": 0
        }
    }
}

# Мокинг функции j_loads_ns для возврата тестовых данных
mocker.patch("src.utils.jjson.j_loads_ns", return_value=SimpleNamespace(**mock_json_data))

# Инициализация кампании
campaign.initialize_campaign()

# Проверка инициализированных данных
assert campaign.campaign.name == "test_campaign"
assert campaign.campaign.category.test_category.name == "test_category"
```


### `test_get_category_products_no_json_files`

**Назначение**: Проверяет, что метод `get_category_products` возвращает пустой список, если отсутствуют JSON-файлы с данными о продуктах.

**Параметры**:

- `mocker`: Мокинг фреймворк для создания тестовых зависимостей.
- `campaign`: Экземпляр `AliPromoCampaign`.

**Возвращает**: 
- `None`.

**Пример**:

```python
# Мокинг функции get_filenames для возврата пустого списка
mocker.patch("src.utils.file.get_filenames", return_value=[])

# Мокинг функции fetch_product_data для возврата пустого списка
mocker.patch("src.suppliers.suppliers_list.aliexpress.campaign.ali_promo_campaign.AliPromoCampaign.fetch_product_data", return_value=[])

# Получение продуктов
products = campaign.get_category_products(force=True)

# Проверка результатов
assert products == []
```


### `test_get_category_products_with_json_files`

**Назначение**: Проверяет, что метод `get_category_products` корректно считывает данные о продуктах из JSON-файлов.

**Параметры**:

- `mocker`: Мокинг фреймворк для создания тестовых зависимостей.
- `campaign`: Экземпляр `AliPromoCampaign`.

**Возвращает**: 
- `None`.

**Пример**:

```python
# Тестовые данные о продукте
mock_product_data = SimpleNamespace(product_id="123", product_title="Test Product")

# Мокинг функции get_filenames для возврата списка JSON-файлов
mocker.patch("src.utils.file.get_filenames", return_value=["product_123.json"])

# Мокинг функции j_loads_ns для возврата тестовых данных о продукте
mocker.patch("src.utils.jjson.j_loads_ns", return_value=mock_product_data)

# Получение продуктов
products = campaign.get_category_products()

# Проверка результатов
assert len(products) == 1
assert products[0].product_id == "123"
assert products[0].product_title == "Test Product"
```


### `test_create_product_namespace`

**Назначение**: Проверяет, что метод `create_product_namespace` правильно создает пространство имен для продукта.

**Параметры**:

- `campaign`: Экземпляр `AliPromoCampaign`.

**Возвращает**: 
- `None`.

**Пример**:

```python
# Тестовые данные о продукте
product_data = {
    "product_id": "123",
    "product_title": "Test Product"
}

# Создание пространства имен для продукта
product = campaign.create_product_namespace(**product_data)

# Проверка результатов
assert product.product_id == "123"
assert product.product_title == "Test Product"
```


### `test_create_category_namespace`

**Назначение**: Проверяет, что метод `create_category_namespace` правильно создает пространство имен для категории.

**Параметры**:

- `campaign`: Экземпляр `AliPromoCampaign`.

**Возвращает**: 
- `None`.

**Пример**:

```python
# Тестовые данные о категории
category_data = {
    "name": "test_category",
    "tags": "tag1, tag2",
    "products": [],
    "products_count": 0
}

# Создание пространства имен для категории
category = campaign.create_category_namespace(**category_data)

# Проверка результатов
assert category.name == "test_category"
assert category.tags == "tag1, tag2"
```


### `test_create_campaign_namespace`

**Назначение**: Проверяет, что метод `create_campaign_namespace` правильно создает пространство имен для кампании.

**Параметры**:

- `campaign`: Экземпляр `AliPromoCampaign`.

**Возвращает**: 
- `None`.

**Пример**:

```python
# Тестовые данные о кампании
campaign_data = {
    "name": "test_campaign",
    "title": "Test Campaign",
    "language": "EN",
    "currency": "USD",
    "category": SimpleNamespace()
}

# Создание пространства имен для кампании
camp = campaign.create_campaign_namespace(**campaign_data)

# Проверка результатов
assert camp.name == "test_campaign"
assert camp.title == "Test Campaign"
```


### `test_prepare_products`

**Назначение**: Проверяет, что метод `prepare_products` вызывает метод `process_affiliate_products`.

**Параметры**:

- `mocker`: Мокинг фреймворк для создания тестовых зависимостей.
- `campaign`: Экземпляр `AliPromoCampaign`.

**Возвращает**: 
- `None`.

**Пример**:

```python
# Мокинг метода get_prepared_products
mocker.patch("src.suppliers.suppliers_list.aliexpress.campaign.ali_promo_campaign.AliPromoCampaign.get_prepared_products", return_value=[])

# Мокинг функции read_text_file
mocker.patch("src.utils.file.read_text_file", return_value="source_data")

# Мокинг функции get_filenames
mocker.patch("src.utils.file.get_filenames", return_value=["source.html"])

# Мокинг метода process_affiliate_products
mocker.patch("src.suppliers.suppliers_list.aliexpress.campaign.ali_promo_campaign.AliPromoCampaign.process_affiliate_products")

# Вызов метода prepare_products
campaign.prepare_products()

# Проверка, что метод process_affiliate_products был вызван
campaign.process_affiliate_products.assert_called_once()
```


### `test_fetch_product_data`

**Назначение**: Проверяет, что метод `fetch_product_data` корректно извлекает данные о продуктах.

**Параметры**:

- `mocker`: Мокинг фреймворк для создания тестовых зависимостей.
- `campaign`: Экземпляр `AliPromoCampaign`.

**Возвращает**: 
- `None`.

**Пример**:

```python
# Список идентификаторов продуктов
product_ids = ["123", "456"]

# Тестовые данные о продуктах
mock_products = [SimpleNamespace(product_id="123"), SimpleNamespace(product_id="456")]

# Мокинг метода process_affiliate_products
mocker.patch("src.suppliers.suppliers_list.aliexpress.campaign.ali_promo_campaign.AliPromoCampaign.process_affiliate_products", return_value=mock_products)

# Извлечение данных о продуктах
products = campaign.fetch_product_data(product_ids)

# Проверка результатов
assert len(products) == 2
assert products[0].product_id == "123"
assert products[1].product_id == "456"
```


### `test_save_product`

**Назначение**: Проверяет, что метод `save_product` корректно сохраняет данные о продукте в JSON-файл.

**Параметры**:

- `mocker`: Мокинг фреймворк для создания тестовых зависимостей.
- `campaign`: Экземпляр `AliPromoCampaign`.

**Возвращает**: 
- `None`.

**Пример**:

```python
# Тестовые данные о продукте
product = SimpleNamespace(product_id="123", product_title="Test Product")

# Мокинг функции j_dumps
mocker.patch("src.utils.jjson.j_dumps", return_value="{}")

# Мокинг функции write_text
mocker.patch("pathlib.Path.write_text")

# Сохранение данных о продукте
campaign.save_product(product)

# Проверка, что функция write_text была вызвана
Path.write_text.assert_called_once_with("{}", encoding='utf-8')
```


### `test_list_campaign_products`

**Назначение**: Проверяет, что метод `list_campaign_products` правильно выводит список названий продуктов кампании.

**Параметры**:

- `campaign`: Экземпляр `AliPromoCampaign`.

**Возвращает**: 
- `None`.

**Пример**:

```python
# Тестовые данные о продуктах
product1 = SimpleNamespace(product_title="Product 1")
product2 = SimpleNamespace(product_title="Product 2")

# Добавление тестовых продуктов в список продуктов категории
campaign.category.products = [product1, product2]

# Получение списка названий продуктов
product_titles = campaign.list_campaign_products()

# Проверка результатов
assert product_titles == ["Product 1", "Product 2"]
```


## Параметры

- `campaign_name`: Имя кампании.
- `category_name`: Имя категории.
- `language`: Язык кампании.
- `currency`: Валюта кампании.

## Примеры

```python
# Создание экземпляра AliPromoCampaign
campaign = AliPromoCampaign("test_campaign", "test_category", "EN", "USD")

# Инициализация кампании
campaign.initialize_campaign()

# Получение продуктов из категории
products = campaign.get_category_products()

# Подготовка продуктов
campaign.prepare_products()

# Сохранение данных о продукте
campaign.save_product(product)
```

## Дополнительные сведения

- Тесты выполняются с использованием фреймворка `pytest`.
- Для мокинг зависимостей используется `mocker`.
- Для работы с JSON-файлами используется модуль `jjson`.
- Для работы с файлами используется модуль `file`.

## Принцип работы

Этот модуль используется для проверки корректности работы класса `AliPromoCampaign`. Тесты проверяют, что все методы класса работают как ожидается, и что данные обрабатываются правильно.

## Заметки

- Мокинг зависимостей позволяет изолировать тестируемый код и избежать зависимости от внешних факторов.
- Тесты должны охватывать как положительные, так и отрицательные сценарии.
- Тесты должны быть легко читаемыми и понятными.
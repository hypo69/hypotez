# Модуль тестирования alipromo_campaign

## Обзор

Модуль `test_alipromo_campaign.py` содержит набор тестов для проверки функциональности класса `AliPromoCampaign`, который предназначен для работы с рекламными кампаниями AliExpress. Модуль использует библиотеку `pytest` для организации и запуска тестов, а также включает фикстуры и моки для изоляции тестов и упрощения проверки различных сценариев.

## Подробней

Этот модуль содержит тесты, проверяющие корректность инициализации кампании, обработки данных о продуктах, создания пространства имен для продуктов и категорий, а также сохранения и извлечения данных о продуктах. Он охватывает различные аспекты работы с классом `AliPromoCampaign` и обеспечивает надежную проверку его функциональности.

## Классы

### `AliPromoCampaign`

**Описание**: Класс для управления рекламными кампаниями AliExpress.

**Наследует**: Нет наследования.

**Атрибуты**:

-   `campaign_name` (str): Имя кампании.
-   `category_name` (str): Имя категории.
-   `language` (str): Язык кампании.
-   `currency` (str): Валюта кампании.

**Методы**:

-   `initialize_campaign()`: Инициализирует данные кампании.
-   `get_category_products()`: Получает продукты для категории.
-   `create_product_namespace()`: Создает пространство имен для продукта.
-   `create_category_namespace()`: Создает пространство имен для категории.
-   `create_campaign_namespace()`: Создает пространство имен для кампании.
-   `prepare_products()`: Подготавливает продукты для кампании.
-   `fetch_product_data()`: Извлекает данные о продуктах.
-   `save_product()`: Сохраняет данные о продукте.
-   `list_campaign_products()`: Выводит список названий продуктов кампании.

## Фикстуры

### `campaign`

```python
@pytest.fixture
def campaign():
    """Fixture for creating a campaign instance."""
    return AliPromoCampaign(campaign_name, category_name, language, currency)
```

**Описание**: Фикстура `campaign` создает экземпляр класса `AliPromoCampaign` с предопределенными значениями для имени кампании, имени категории, языка и валюты.

**Параметры**: Нет параметров.

**Возвращает**: Экземпляр класса `AliPromoCampaign`.

**Принцип работы**: Фикстура просто создает и возвращает экземпляр класса `AliPromoCampaign` с заданными параметрами.

**Примеры**:

```python
def test_some_function(campaign):
    # Используем фикстуру campaign для тестирования
    assert campaign.campaign_name == "test_campaign"
```

## Функции

### `test_initialize_campaign`

```python
def test_initialize_campaign(mocker, campaign):
    """Test the initialize_campaign method."""
    mock_json_data = {
        "name": campaign_name,
        "title": "Test Campaign",
        "language": language,
        "currency": currency,
        "category": {
            category_name: {
                "name": category_name,
                "tags": "tag1, tag2",
                "products": [],
                "products_count": 0
            }
        }
    }
    mocker.patch("src.utils.jjson.j_loads_ns", return_value=SimpleNamespace(**mock_json_data))

    campaign.initialize_campaign()
    assert campaign.campaign.name == campaign_name
    assert campaign.campaign.category.test_category.name == category_name
```

**Назначение**: Тестирует метод `initialize_campaign` класса `AliPromoCampaign`.

**Параметры**:

-   `mocker`: Фикстура `pytest-mock` для создания мок-объектов.
-   `campaign`: Фикстура `campaign`, предоставляющая экземпляр класса `AliPromoCampaign`.

**Возвращает**: None.

**Вызывает исключения**: Нет.

**Как работает функция**:

1.  Создает мок-данные в формате JSON, представляющие данные кампании.
2.  Использует `mocker.patch` для замены функции `j_loads_ns` мок-объектом, возвращающим созданные мок-данные.
3.  Вызывает метод `initialize_campaign` для экземпляра `campaign`.
4.  Проверяет, что данные кампании были правильно инициализированы, сравнивая значения атрибутов `campaign.campaign.name` и `campaign.campaign.category.test_category.name` с ожидаемыми значениями.

**Примеры**:

```python
def test_initialize_campaign(mocker, campaign):
    # Тестирование метода initialize_campaign
    ...
```

### `test_get_category_products_no_json_files`

```python
def test_get_category_products_no_json_files(mocker, campaign):
    """Test get_category_products method when no JSON files are present."""
    mocker.patch("src.utils.file.get_filenames", return_value=[])
    mocker.patch("src.suppliers.aliexpress.campaign.ali_promo_campaign.AliPromoCampaign.fetch_product_data", return_value=[])

    products = campaign.get_category_products(force=True)
    assert products == []
```

**Назначение**: Тестирует метод `get_category_products` класса `AliPromoCampaign` в случае, когда отсутствуют JSON-файлы с данными о продуктах.

**Параметры**:

-   `mocker`: Фикстура `pytest-mock` для создания мок-объектов.
-   `campaign`: Фикстура `campaign`, предоставляющая экземпляр класса `AliPromoCampaign`.

**Возвращает**: None.

**Вызывает исключения**: Нет.

**Как работает функция**:

1.  Использует `mocker.patch` для замены функции `get_filenames` мок-объектом, возвращающим пустой список (имитация отсутствия файлов).
2.  Использует `mocker.patch` для замены метода `fetch_product_data` мок-объектом, возвращающим пустой список.
3.  Вызывает метод `get_category_products` для экземпляра `campaign` с параметром `force=True`.
4.  Проверяет, что метод возвращает пустой список, что соответствует ожидаемому результату при отсутствии файлов.

**Примеры**:

```python
def test_get_category_products_no_json_files(mocker, campaign):
    # Тестирование метода get_category_products при отсутствии JSON-файлов
    ...
```

### `test_get_category_products_with_json_files`

```python
def test_get_category_products_with_json_files(mocker, campaign):
    """Test get_category_products method when JSON files are present."""
    mock_product_data = SimpleNamespace(product_id="123", product_title="Test Product")
    mocker.patch("src.utils.file.get_filenames", return_value=["product_123.json"])
    mocker.patch("src.utils.jjson.j_loads_ns", return_value=mock_product_data)

    products = campaign.get_category_products()
    assert len(products) == 1
    assert products[0].product_id == "123"
    assert products[0].product_title == "Test Product"
```

**Назначение**: Тестирует метод `get_category_products` класса `AliPromoCampaign` в случае, когда присутствуют JSON-файлы с данными о продуктах.

**Параметры**:

-   `mocker`: Фикстура `pytest-mock` для создания мок-объектов.
-   `campaign`: Фикстура `campaign`, предоставляющая экземпляр класса `AliPromoCampaign`.

**Возвращает**: None.

**Вызывает исключения**: Нет.

**Как работает функция**:

1.  Создает мок-данные продукта в виде `SimpleNamespace`.
2.  Использует `mocker.patch` для замены функции `get_filenames` мок-объектом, возвращающим список с именем файла продукта.
3.  Использует `mocker.patch` для замены функции `j_loads_ns` мок-объектом, возвращающим созданные мок-данные продукта.
4.  Вызывает метод `get_category_products` для экземпляра `campaign`.
5.  Проверяет, что метод возвращает список с одним продуктом, и что атрибуты продукта соответствуют ожидаемым значениям.

**Примеры**:

```python
def test_get_category_products_with_json_files(mocker, campaign):
    # Тестирование метода get_category_products при наличии JSON-файлов
    ...
```

### `test_create_product_namespace`

```python
def test_create_product_namespace(campaign):
    """Test create_product_namespace method."""
    product_data = {
        "product_id": "123",
        "product_title": "Test Product"
    }
    product = campaign.create_product_namespace(**product_data)
    assert product.product_id == "123"
    assert product.product_title == "Test Product"
```

**Назначение**: Тестирует метод `create_product_namespace` класса `AliPromoCampaign`.

**Параметры**:

-   `campaign`: Фикстура `campaign`, предоставляющая экземпляр класса `AliPromoCampaign`.

**Возвращает**: None.

**Вызывает исключения**: Нет.

**Как работает функция**:

1.  Создает словарь с данными продукта.
2.  Вызывает метод `create_product_namespace` для экземпляра `campaign`, передавая данные продукта в качестве аргументов.
3.  Проверяет, что атрибуты созданного пространства имен продукта соответствуют ожидаемым значениям.

**Примеры**:

```python
def test_create_product_namespace(campaign):
    # Тестирование метода create_product_namespace
    ...
```

### `test_create_category_namespace`

```python
def test_create_category_namespace(campaign):
    """Test create_category_namespace method."""
    category_data = {
        "name": category_name,
        "tags": "tag1, tag2",
        "products": [],
        "products_count": 0
    }
    category = campaign.create_category_namespace(**category_data)
    assert category.name == category_name
    assert category.tags == "tag1, tag2"
```

**Назначение**: Тестирует метод `create_category_namespace` класса `AliPromoCampaign`.

**Параметры**:

-   `campaign`: Фикстура `campaign`, предоставляющая экземпляр класса `AliPromoCampaign`.

**Возвращает**: None.

**Вызывает исключения**: Нет.

**Как работает функция**:

1.  Создает словарь с данными категории.
2.  Вызывает метод `create_category_namespace` для экземпляра `campaign`, передавая данные категории в качестве аргументов.
3.  Проверяет, что атрибуты созданного пространства имен категории соответствуют ожидаемым значениям.

**Примеры**:

```python
def test_create_category_namespace(campaign):
    # Тестирование метода create_category_namespace
    ...
```

### `test_create_campaign_namespace`

```python
def test_create_campaign_namespace(campaign):
    """Test create_campaign_namespace method."""
    campaign_data = {
        "name": campaign_name,
        "title": "Test Campaign",
        "language": language,
        "currency": currency,
        "category": SimpleNamespace()
    }
    camp = campaign.create_campaign_namespace(**campaign_data)
    assert camp.name == campaign_name
    assert camp.title == "Test Campaign"
```

**Назначение**: Тестирует метод `create_campaign_namespace` класса `AliPromoCampaign`.

**Параметры**:

-   `campaign`: Фикстура `campaign`, предоставляющая экземпляр класса `AliPromoCampaign`.

**Возвращает**: None.

**Вызывает исключения**: Нет.

**Как работает функция**:

1.  Создает словарь с данными кампании.
2.  Вызывает метод `create_campaign_namespace` для экземпляра `campaign`, передавая данные кампании в качестве аргументов.
3.  Проверяет, что атрибуты созданного пространства имен кампании соответствуют ожидаемым значениям.

**Примеры**:

```python
def test_create_campaign_namespace(campaign):
    # Тестирование метода create_campaign_namespace
    ...
```

### `test_prepare_products`

```python
def test_prepare_products(mocker, campaign):
    """Test prepare_products method."""
    mocker.patch("src.suppliers.aliexpress.campaign.ali_promo_campaign.AliPromoCampaign.get_prepared_products", return_value=[])
    mocker.patch("src.utils.file.read_text_file", return_value="source_data")
    mocker.patch("src.utils.file.get_filenames", return_value=["source.html"])
    mocker.patch("src.suppliers.aliexpress.campaign.ali_promo_campaign.AliPromoCampaign.process_affiliate_products")

    campaign.prepare_products()
    campaign.process_affiliate_products.assert_called_once()
```

**Назначение**: Тестирует метод `prepare_products` класса `AliPromoCampaign`.

**Параметры**:

-   `mocker`: Фикстура `pytest-mock` для создания мок-объектов.
-   `campaign`: Фикстура `campaign`, предоставляющая экземпляр класса `AliPromoCampaign`.

**Возвращает**: None.

**Вызывает исключения**: Нет.

**Как работает функция**:

1.  Использует `mocker.patch` для замены метода `get_prepared_products` мок-объектом, возвращающим пустой список.
2.  Использует `mocker.patch` для замены функции `read_text_file` мок-объектом, возвращающим строку "source_data".
3.  Использует `mocker.patch` для замены функции `get_filenames` мок-объектом, возвращающим список с именем файла "source.html".
4.  Использует `mocker.patch` для замены метода `process_affiliate_products` мок-объектом.
5.  Вызывает метод `prepare_products` для экземпляра `campaign`.
6.  Проверяет, что метод `process_affiliate_products` был вызван один раз.

**Примеры**:

```python
def test_prepare_products(mocker, campaign):
    # Тестирование метода prepare_products
    ...
```

### `test_fetch_product_data`

```python
def test_fetch_product_data(mocker, campaign):
    """Test fetch_product_data method."""
    product_ids = ["123", "456"]
    mock_products = [SimpleNamespace(product_id="123"), SimpleNamespace(product_id="456")]
    mocker.patch("src.suppliers.aliexpress.campaign.ali_promo_campaign.AliPromoCampaign.process_affiliate_products", return_value=mock_products)

    products = campaign.fetch_product_data(product_ids)
    assert len(products) == 2
    assert products[0].product_id == "123"
    assert products[1].product_id == "456"
```

**Назначение**: Тестирует метод `fetch_product_data` класса `AliPromoCampaign`.

**Параметры**:

-   `mocker`: Фикстура `pytest-mock` для создания мок-объектов.
-   `campaign`: Фикстура `campaign`, предоставляющая экземпляр класса `AliPromoCampaign`.

**Возвращает**: None.

**Вызывает исключения**: Нет.

**Как работает функция**:

1.  Создает список идентификаторов продуктов.
2.  Создает список мок-объектов продуктов.
3.  Использует `mocker.patch` для замены метода `process_affiliate_products` мок-объектом, возвращающим список мок-объектов продуктов.
4.  Вызывает метод `fetch_product_data` для экземпляра `campaign`, передавая список идентификаторов продуктов.
5.  Проверяет, что метод возвращает список с двумя продуктами, и что атрибуты продуктов соответствуют ожидаемым значениям.

**Примеры**:

```python
def test_fetch_product_data(mocker, campaign):
    # Тестирование метода fetch_product_data
    ...
```

### `test_save_product`

```python
def test_save_product(mocker, campaign):
    """Test save_product method."""
    product = SimpleNamespace(product_id="123", product_title="Test Product")
    mocker.patch("src.utils.jjson.j_dumps", return_value="{}")
    mocker.patch("pathlib.Path.write_text")

    campaign.save_product(product)
    Path.write_text.assert_called_once_with("{}", encoding='utf-8')
```

**Назначение**: Тестирует метод `save_product` класса `AliPromoCampaign`.

**Параметры**:

-   `mocker`: Фикстура `pytest-mock` для создания мок-объектов.
-   `campaign`: Фикстура `campaign`, предоставляющая экземпляр класса `AliPromoCampaign`.

**Возвращает**: None.

**Вызывает исключения**: Нет.

**Как работает функция**:

1.  Создает мок-объект продукта.
2.  Использует `mocker.patch` для замены функции `j_dumps` мок-объектом, возвращающим пустую строку "{}".
3.  Использует `mocker.patch` для замены метода `write_text` класса `Path` мок-объектом.
4.  Вызывает метод `save_product` для экземпляра `campaign`, передавая мок-объект продукта.
5.  Проверяет, что метод `write_text` был вызван один раз с ожидаемыми аргументами.

**Примеры**:

```python
def test_save_product(mocker, campaign):
    # Тестирование метода save_product
    ...
```

### `test_list_campaign_products`

```python
def test_list_campaign_products(campaign):
    """Test list_campaign_products method."""
    product1 = SimpleNamespace(product_title="Product 1")
    product2 = SimpleNamespace(product_title="Product 2")
    campaign.category.products = [product1, product2]

    product_titles = campaign.list_campaign_products()
    assert product_titles == ["Product 1", "Product 2"]
```

**Назначение**: Тестирует метод `list_campaign_products` класса `AliPromoCampaign`.

**Параметры**:

-   `campaign`: Фикстура `campaign`, предоставляющая экземпляр класса `AliPromoCampaign`.

**Возвращает**: None.

**Вызывает исключения**: Нет.

**Как работает функция**:

1.  Создает два мок-объекта продукта с разными названиями.
2.  Присваивает список этих продуктов атрибуту `products` объекта категории кампании.
3.  Вызывает метод `list_campaign_products` для экземпляра `campaign`.
4.  Проверяет, что метод возвращает список названий продуктов, соответствующих ожидаемым значениям.

**Примеры**:

```python
def test_list_campaign_products(campaign):
    # Тестирование метода list_campaign_products
    ...
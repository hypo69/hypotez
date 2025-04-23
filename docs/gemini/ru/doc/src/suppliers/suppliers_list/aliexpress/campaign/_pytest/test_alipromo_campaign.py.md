# Модуль тестирования alipromo_campaign

## Обзор

Этот модуль содержит набор тестов для проверки функциональности класса `AliPromoCampaign`, который используется для управления рекламными кампаниями AliExpress. Модуль использует библиотеку `pytest` для организации и выполнения тестов, а также `mocker` для создания мок-объектов и изоляции тестируемого кода.

## Подробней

Модуль включает тесты для различных методов класса `AliPromoCampaign`, таких как инициализация кампании, получение продуктов категории, создание пространств имен продуктов, категорий и кампаний, подготовка продуктов, получение данных о продуктах, сохранение продуктов и листинг продуктов кампании. Каждый тест проверяет определенный аспект функциональности класса и использует мок-объекты для имитации внешних зависимостей и упрощения тестирования.

## Классы

### `campaign`

**Описание**: Fixture для создания экземпляра `AliPromoCampaign` для использования в тестах.

**Возвращает**:
- Экземпляр класса `AliPromoCampaign`.

## Функции

### `test_initialize_campaign`

**Назначение**: Тестирует метод `initialize_campaign`, чтобы убедиться, что он правильно инициализирует данные кампании.

**Параметры**:
- `mocker`: Объект `mocker` из библиотеки `pytest-mock` для создания мок-объектов.
- `campaign`: Fixture `campaign`, предоставляющая экземпляр `AliPromoCampaign`.

**Как работает функция**:
- Создается мок-объект `mock_json_data`, представляющий данные JSON кампании.
- `src.utils.jjson.j_loads_ns` патчится, чтобы возвращать `mock_json_data`.
- Вызывается метод `initialize_campaign` у экземпляра `campaign`.
- Проверяется, что атрибуты `name` и `category.test_category.name` у экземпляра `campaign.campaign` соответствуют ожидаемым значениям.

**Примеры**:
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

### `test_get_category_products_no_json_files`

**Назначение**: Тестирует метод `get_category_products`, когда отсутствуют JSON-файлы.

**Параметры**:
- `mocker`: Объект `mocker` из библиотеки `pytest-mock` для создания мок-объектов.
- `campaign`: Fixture `campaign`, предоставляющая экземпляр `AliPromoCampaign`.

**Как работает функция**:
- `src.utils.file.get_filenames` патчится, чтобы возвращать пустой список, имитируя отсутствие JSON-файлов.
- `src.suppliers.suppliers_list.aliexpress.campaign.ali_promo_campaign.AliPromoCampaign.fetch_product_data` патчится, чтобы возвращать пустой список.
- Вызывается метод `get_category_products` у экземпляра `campaign` с параметром `force=True`.
- Проверяется, что возвращаемый список продуктов пуст.

**Примеры**:
```python
def test_get_category_products_no_json_files(mocker, campaign):
    """Test get_category_products method when no JSON files are present."""
    mocker.patch("src.utils.file.get_filenames", return_value=[])
    mocker.patch("src.suppliers.suppliers_list.aliexpress.campaign.ali_promo_campaign.AliPromoCampaign.fetch_product_data", return_value=[])

    products = campaign.get_category_products(force=True)
    assert products == []
```

### `test_get_category_products_with_json_files`

**Назначение**: Тестирует метод `get_category_products`, когда JSON-файлы присутствуют.

**Параметры**:
- `mocker`: Объект `mocker` из библиотеки `pytest-mock` для создания мок-объектов.
- `campaign`: Fixture `campaign`, предоставляющая экземпляр `AliPromoCampaign`.

**Как работает функция**:
- Создается мок-объект `mock_product_data`, представляющий данные продукта.
- `src.utils.file.get_filenames` патчится, чтобы возвращать список с именем JSON-файла.
- `src.utils.jjson.j_loads_ns` патчится, чтобы возвращать `mock_product_data`.
- Вызывается метод `get_category_products` у экземпляра `campaign`.
- Проверяется, что возвращаемый список продуктов содержит один элемент и что атрибуты `product_id` и `product_title` соответствуют ожидаемым значениям.

**Примеры**:
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

### `test_create_product_namespace`

**Назначение**: Тестирует метод `create_product_namespace`.

**Параметры**:
- `campaign`: Fixture `campaign`, предоставляющая экземпляр `AliPromoCampaign`.

**Как работает функция**:
- Создается словарь `product_data` с данными продукта.
- Вызывается метод `create_product_namespace` у экземпляра `campaign` с данными продукта.
- Проверяется, что атрибуты `product_id` и `product_title` у возвращаемого объекта соответствуют ожидаемым значениям.

**Примеры**:
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

### `test_create_category_namespace`

**Назначение**: Тестирует метод `create_category_namespace`.

**Параметры**:
- `campaign`: Fixture `campaign`, предоставляющая экземпляр `AliPromoCampaign`.

**Как работает функция**:
- Создается словарь `category_data` с данными категории.
- Вызывается метод `create_category_namespace` у экземпляра `campaign` с данными категории.
- Проверяется, что атрибуты `name` и `tags` у возвращаемого объекта соответствуют ожидаемым значениям.

**Примеры**:
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

### `test_create_campaign_namespace`

**Назначение**: Тестирует метод `create_campaign_namespace`.

**Параметры**:
- `campaign`: Fixture `campaign`, предоставляющая экземпляр `AliPromoCampaign`.

**Как работает функция**:
- Создается словарь `campaign_data` с данными кампании.
- Вызывается метод `create_campaign_namespace` у экземпляра `campaign` с данными кампании.
- Проверяется, что атрибуты `name` и `title` у возвращаемого объекта соответствуют ожидаемым значениям.

**Примеры**:
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

### `test_prepare_products`

**Назначение**: Тестирует метод `prepare_products`.

**Параметры**:
- `mocker`: Объект `mocker` из библиотеки `pytest-mock` для создания мок-объектов.
- `campaign`: Fixture `campaign`, предоставляющая экземпляр `AliPromoCampaign`.

**Как работает функция**:
- `src.suppliers.suppliers_list.aliexpress.campaign.ali_promo_campaign.AliPromoCampaign.get_prepared_products` патчится, чтобы возвращать пустой список.
- `src.utils.file.read_text_file` патчится, чтобы возвращать "source_data".
- `src.utils.file.get_filenames` патчится, чтобы возвращать список с именем HTML-файла.
- `src.suppliers.suppliers_list.aliexpress.campaign.ali_promo_campaign.AliPromoCampaign.process_affiliate_products` патчится.
- Вызывается метод `prepare_products` у экземпляра `campaign`.
- Проверяется, что метод `process_affiliate_products` был вызван один раз.

**Примеры**:
```python
def test_prepare_products(mocker, campaign):
    """Test prepare_products method."""
    mocker.patch("src.suppliers.suppliers_list.aliexpress.campaign.ali_promo_campaign.AliPromoCampaign.get_prepared_products", return_value=[])
    mocker.patch("src.utils.file.read_text_file", return_value="source_data")
    mocker.patch("src.utils.file.get_filenames", return_value=["source.html"])
    mocker.patch("src.suppliers.suppliers_list.aliexpress.campaign.ali_promo_campaign.AliPromoCampaign.process_affiliate_products")

    campaign.prepare_products()
    campaign.process_affiliate_products.assert_called_once()
```

### `test_fetch_product_data`

**Назначение**: Тестирует метод `fetch_product_data`.

**Параметры**:
- `mocker`: Объект `mocker` из библиотеки `pytest-mock` для создания мок-объектов.
- `campaign`: Fixture `campaign`, предоставляющая экземпляр `AliPromoCampaign`.

**Как работает функция**:
- Создается список `product_ids` с идентификаторами продуктов.
- Создается список `mock_products` с мок-объектами продуктов.
- `src.suppliers.suppliers_list.aliexpress.campaign.ali_promo_campaign.AliPromoCampaign.process_affiliate_products` патчится, чтобы возвращать `mock_products`.
- Вызывается метод `fetch_product_data` у экземпляра `campaign` с `product_ids`.
- Проверяется, что возвращаемый список продуктов содержит два элемента и что атрибуты `product_id` соответствуют ожидаемым значениям.

**Примеры**:
```python
def test_fetch_product_data(mocker, campaign):
    """Test fetch_product_data method."""
    product_ids = ["123", "456"]
    mock_products = [SimpleNamespace(product_id="123"), SimpleNamespace(product_id="456")]
    mocker.patch("src.suppliers.suppliers_list.aliexpress.campaign.ali_promo_campaign.AliPromoCampaign.process_affiliate_products", return_value=mock_products)

    products = campaign.fetch_product_data(product_ids)
    assert len(products) == 2
    assert products[0].product_id == "123"
    assert products[1].product_id == "456"
```

### `test_save_product`

**Назначение**: Тестирует метод `save_product`.

**Параметры**:
- `mocker`: Объект `mocker` из библиотеки `pytest-mock` для создания мок-объектов.
- `campaign`: Fixture `campaign`, предоставляющая экземпляр `AliPromoCampaign`.

**Как работает функция**:
- Создается мок-объект `product`, представляющий продукт.
- `src.utils.jjson.j_dumps` патчится, чтобы возвращать "{}".
- `pathlib.Path.write_text` патчится.
- Вызывается метод `save_product` у экземпляра `campaign` с `product`.
- Проверяется, что метод `Path.write_text` был вызван один раз с ожидаемыми аргументами.

**Примеры**:
```python
def test_save_product(mocker, campaign):
    """Test save_product method."""
    product = SimpleNamespace(product_id="123", product_title="Test Product")
    mocker.patch("src.utils.jjson.j_dumps", return_value="{}")
    mocker.patch("pathlib.Path.write_text")

    campaign.save_product(product)
    Path.write_text.assert_called_once_with("{}", encoding='utf-8')
```

### `test_list_campaign_products`

**Назначение**: Тестирует метод `list_campaign_products`.

**Параметры**:
- `campaign`: Fixture `campaign`, предоставляющая экземпляр `AliPromoCampaign`.

**Как работает функция**:
- Создаются мок-объекты `product1` и `product2`, представляющие продукты.
- Атрибуту `category.products` экземпляра `campaign` присваивается список с `product1` и `product2`.
- Вызывается метод `list_campaign_products` у экземпляра `campaign`.
- Проверяется, что возвращаемый список заголовков продуктов соответствует ожидаемым значениям.

**Примеры**:
```python
def test_list_campaign_products(campaign):
    """Test list_campaign_products method."""
    product1 = SimpleNamespace(product_title="Product 1")
    product2 = SimpleNamespace(product_title="Product 2")
    campaign.category.products = [product1, product2]

    product_titles = campaign.list_campaign_products()
    assert product_titles == ["Product 1", "Product 2"]
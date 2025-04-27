# Модуль `test_alipromo_campaign.py`

## Обзор

Данный модуль содержит юнит-тесты для класса `AliPromoCampaign` из модуля `src.suppliers.suppliers_list.aliexpress.campaign.ali_promo_campaign`. 

## Детали

Модуль тестирует функциональность класса `AliPromoCampaign`, который отвечает за обработку данных рекламных кампаний AliExpress. 
Тесты охватывают основные функции класса, такие как:
- Инициализация кампании;
- Извлечение списка продуктов категории;
- Создание пространств имен для продуктов, категорий и кампаний;
- Подготовка продуктов к обработке;
- Получение данных о продуктах;
- Сохранение данных о продуктах;
- Получение списка названий продуктов в кампании.

## Тесты

### `test_initialize_campaign`

**Цель**: Проверка правильной инициализации данных кампании методом `initialize_campaign`.

**Параметры**:
- `mocker`: Фикстура для мокирования функций.
- `campaign`: Фикстура для создания экземпляра `AliPromoCampaign`.

**Возвращаемое значение**: `None`.

**Исключения**: `None`.

**Пример**:

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

**Цель**: Проверка метода `get_category_products` в случае отсутствия JSON-файлов с данными о продуктах.

**Параметры**:
- `mocker`: Фикстура для мокирования функций.
- `campaign`: Фикстура для создания экземпляра `AliPromoCampaign`.

**Возвращаемое значение**: `None`.

**Исключения**: `None`.

**Пример**:

```python
def test_get_category_products_no_json_files(mocker, campaign):
    """Test get_category_products method when no JSON files are present."""
    mocker.patch("src.utils.file.get_filenames", return_value=[])
    mocker.patch("src.suppliers.suppliers_list.aliexpress.campaign.ali_promo_campaign.AliPromoCampaign.fetch_product_data", return_value=[])

    products = campaign.get_category_products(force=True)
    assert products == []
```

### `test_get_category_products_with_json_files`

**Цель**: Проверка метода `get_category_products` в случае наличия JSON-файлов с данными о продуктах.

**Параметры**:
- `mocker`: Фикстура для мокирования функций.
- `campaign`: Фикстура для создания экземпляра `AliPromoCampaign`.

**Возвращаемое значение**: `None`.

**Исключения**: `None`.

**Пример**:

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

**Цель**: Проверка метода `create_product_namespace`, который создает пространство имен для продукта.

**Параметры**:
- `campaign`: Фикстура для создания экземпляра `AliPromoCampaign`.

**Возвращаемое значение**: `None`.

**Исключения**: `None`.

**Пример**:

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

**Цель**: Проверка метода `create_category_namespace`, который создает пространство имен для категории.

**Параметры**:
- `campaign`: Фикстура для создания экземпляра `AliPromoCampaign`.

**Возвращаемое значение**: `None`.

**Исключения**: `None`.

**Пример**:

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

**Цель**: Проверка метода `create_campaign_namespace`, который создает пространство имен для кампании.

**Параметры**:
- `campaign`: Фикстура для создания экземпляра `AliPromoCampaign`.

**Возвращаемое значение**: `None`.

**Исключения**: `None`.

**Пример**:

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

**Цель**: Проверка метода `prepare_products`, который подготавливает продукты к обработке.

**Параметры**:
- `mocker`: Фикстура для мокирования функций.
- `campaign`: Фикстура для создания экземпляра `AliPromoCampaign`.

**Возвращаемое значение**: `None`.

**Исключения**: `None`.

**Пример**:

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

**Цель**: Проверка метода `fetch_product_data`, который получает данные о продуктах.

**Параметры**:
- `mocker`: Фикстура для мокирования функций.
- `campaign`: Фикстура для создания экземпляра `AliPromoCampaign`.

**Возвращаемое значение**: `None`.

**Исключения**: `None`.

**Пример**:

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

**Цель**: Проверка метода `save_product`, который сохраняет данные о продукте.

**Параметры**:
- `mocker`: Фикстура для мокирования функций.
- `campaign`: Фикстура для создания экземпляра `AliPromoCampaign`.

**Возвращаемое значение**: `None`.

**Исключения**: `None`.

**Пример**:

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

**Цель**: Проверка метода `list_campaign_products`, который возвращает список названий продуктов в кампании.

**Параметры**:
- `campaign`: Фикстура для создания экземпляра `AliPromoCampaign`.

**Возвращаемое значение**: `None`.

**Исключения**: `None`.

**Пример**:

```python
def test_list_campaign_products(campaign):
    """Test list_campaign_products method."""
    product1 = SimpleNamespace(product_title="Product 1")
    product2 = SimpleNamespace(product_title="Product 2")
    campaign.category.products = [product1, product2]

    product_titles = campaign.list_campaign_products()
    assert product_titles == ["Product 1", "Product 2"]
```

## Параметры

### `campaign_name`

**Описание**: Название тестовой кампании.

**Тип**: `str`.

### `category_name`

**Описание**: Название тестовой категории.

**Тип**: `str`.

### `language`

**Описание**: Язык кампании.

**Тип**: `str`.

### `currency`

**Описание**: Валюта кампании.

**Тип**: `str`.

## Фикстуры

### `campaign`

**Описание**: Фикстура для создания экземпляра класса `AliPromoCampaign`.

**Возвращаемое значение**: `AliPromoCampaign`.

**Пример**:

```python
@pytest.fixture
def campaign():
    """Fixture for creating a campaign instance."""
    return AliPromoCampaign(campaign_name, category_name, language, currency)
```

## Примечания

- В тестах используются мокированные функции для имитации поведения реальных функций.
- Тестовые данные для кампании, категории и продуктов определены в начале модуля.
- Модуль использует библиотеку `pytest` для запуска тестов.
- Для сериализации и десериализации JSON-данных используется модуль `src.utils.jjson`.
- Для работы с файлами используется модуль `src.utils.file`.
- Модуль импортирует класс `AliPromoCampaign` из модуля `src.suppliers.suppliers_list.aliexpress.campaign.ali_promo_campaign`.
# Модуль тестирования alipromo_campaign

## Обзор

Этот модуль содержит набор тестов для класса `AliPromoCampaign`, который отвечает за управление рекламными кампаниями AliExpress. Модуль использует библиотеку `pytest` для организации и выполнения тестов.

## Подробнее

Модуль содержит тесты для различных методов класса `AliPromoCampaign`, включая инициализацию кампании, получение продуктов категории, создание пространств имен для продуктов, категорий и кампаний, подготовку продуктов, получение данных о продуктах и сохранение продуктов.

## Классы

### `AliPromoCampaign`

**Описание**: Класс для управления рекламными кампаниями AliExpress.

**Методы**:

- `initialize_campaign`: Инициализирует данные кампании.
- `get_category_products`: Получает продукты из категории.
- `create_product_namespace`: Создает пространство имен для продукта.
- `create_category_namespace`: Создает пространство имен для категории.
- `create_campaign_namespace`: Создает пространство имен для кампании.
- `prepare_products`: Подготавливает продукты для кампании.
- `fetch_product_data`: Получает данные о продуктах.
- `save_product`: Сохраняет данные о продукте.
- `list_campaign_products`: Выводит список названий продуктов кампании.

## Фикстуры

### `campaign`

```python
@pytest.fixture
def campaign():
    """Fixture for creating a campaign instance."""
    return AliPromoCampaign(campaign_name, category_name, language, currency)
```

**Назначение**: Создает экземпляр класса `AliPromoCampaign` для использования в тестах.

**Возвращает**:
- `AliPromoCampaign`: Экземпляр класса `AliPromoCampaign`.

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

**Назначение**: Проверяет, правильно ли метод `initialize_campaign` инициализирует данные кампании.

**Параметры**:
- `mocker`: Объект `pytest-mock` для подмены зависимостей.
- `campaign`: Фикстура `campaign`, предоставляющая экземпляр класса `AliPromoCampaign`.

**Как работает функция**:
- Создается моковый JSON с данными кампании.
- Используется `mocker.patch` для замены функции `j_loads_ns` моковым объектом, возвращающим данные кампании.
- Вызывается метод `initialize_campaign` объекта `campaign`.
- Проверяется, что атрибуты объекта `campaign.campaign` и `campaign.campaign.category.test_category` установлены правильно.

### `test_get_category_products_no_json_files`

```python
def test_get_category_products_no_json_files(mocker, campaign):
    """Test get_category_products method when no JSON files are present."""
    mocker.patch("src.utils.file.get_filenames", return_value=[])
    mocker.patch("src.suppliers.suppliers_list.aliexpress.campaign.ali_promo_campaign.AliPromoCampaign.fetch_product_data", return_value=[])

    products = campaign.get_category_products(force=True)
    assert products == []
```

**Назначение**: Проверяет метод `get_category_products`, когда нет JSON-файлов.

**Параметры**:
- `mocker`: Объект `pytest-mock` для подмены зависимостей.
- `campaign`: Фикстура `campaign`, предоставляющая экземпляр класса `AliPromoCampaign`.

**Как работает функция**:
- Используется `mocker.patch` для замены функций `get_filenames` и `fetch_product_data` моковыми объектами.
- Вызывается метод `get_category_products` объекта `campaign` с параметром `force=True`.
- Проверяется, что возвращаемый список продуктов пуст.

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

**Назначение**: Проверяет метод `get_category_products`, когда JSON-файлы присутствуют.

**Параметры**:
- `mocker`: Объект `pytest-mock` для подмены зависимостей.
- `campaign`: Фикстура `campaign`, предоставляющая экземпляр класса `AliPromoCampaign`.

**Как работает функция**:
- Создается моковый объект продукта `SimpleNamespace`.
- Используется `mocker.patch` для замены функций `get_filenames` и `j_loads_ns` моковыми объектами.
- Вызывается метод `get_category_products` объекта `campaign`.
- Проверяется, что возвращаемый список содержит один продукт с правильными атрибутами.

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

**Назначение**: Проверяет метод `create_product_namespace`.

**Параметры**:
- `campaign`: Фикстура `campaign`, предоставляющая экземпляр класса `AliPromoCampaign`.

**Как работает функция**:
- Создаются данные продукта в виде словаря.
- Вызывается метод `create_product_namespace` объекта `campaign` с данными продукта.
- Проверяется, что атрибуты возвращаемого объекта установлены правильно.

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

**Назначение**: Проверяет метод `create_category_namespace`.

**Параметры**:
- `campaign`: Фикстура `campaign`, предоставляющая экземпляр класса `AliPromoCampaign`.

**Как работает функция**:
- Создаются данные категории в виде словаря.
- Вызывается метод `create_category_namespace` объекта `campaign` с данными категории.
- Проверяется, что атрибуты возвращаемого объекта установлены правильно.

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

**Назначение**: Проверяет метод `create_campaign_namespace`.

**Параметры**:
- `campaign`: Фикстура `campaign`, предоставляющая экземпляр класса `AliPromoCampaign`.

**Как работает функция**:
- Создаются данные кампании в виде словаря.
- Вызывается метод `create_campaign_namespace` объекта `campaign` с данными кампании.
- Проверяется, что атрибуты возвращаемого объекта установлены правильно.

### `test_prepare_products`

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

**Назначение**: Проверяет метод `prepare_products`.

**Параметры**:
- `mocker`: Объект `pytest-mock` для подмены зависимостей.
- `campaign`: Фикстура `campaign`, предоставляющая экземпляр класса `AliPromoCampaign`.

**Как работает функция**:
- Используется `mocker.patch` для замены функций `get_prepared_products`, `read_text_file`, `get_filenames` и `process_affiliate_products` моковыми объектами.
- Вызывается метод `prepare_products` объекта `campaign`.
- Проверяется, что метод `process_affiliate_products` был вызван один раз.

### `test_fetch_product_data`

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

**Назначение**: Проверяет метод `fetch_product_data`.

**Параметры**:
- `mocker`: Объект `pytest-mock` для подмены зависимостей.
- `campaign`: Фикстура `campaign`, предоставляющая экземпляр класса `AliPromoCampaign`.

**Как работает функция**:
- Создается список идентификаторов продуктов.
- Создается список моковых объектов продуктов `SimpleNamespace`.
- Используется `mocker.patch` для замены функции `process_affiliate_products` моковым объектом, возвращающим список моковых продуктов.
- Вызывается метод `fetch_product_data` объекта `campaign` со списком идентификаторов продуктов.
- Проверяется, что возвращаемый список содержит два продукта с правильными идентификаторами.

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

**Назначение**: Проверяет метод `save_product`.

**Параметры**:
- `mocker`: Объект `pytest-mock` для подмены зависимостей.
- `campaign`: Фикстура `campaign`, предоставляющая экземпляр класса `AliPromoCampaign`.

**Как работает функция**:
- Создается моковый объект продукта `SimpleNamespace`.
- Используется `mocker.patch` для замены функций `j_dumps` и `Path.write_text` моковыми объектами.
- Вызывается метод `save_product` объекта `campaign` с моковым объектом продукта.
- Проверяется, что метод `Path.write_text` был вызван один раз с правильными аргументами.

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

**Назначение**: Проверяет метод `list_campaign_products`.

**Параметры**:
- `campaign`: Фикстура `campaign`, предоставляющая экземпляр класса `AliPromoCampaign`.

**Как работает функция**:
- Создаются два моковых объекта продукта `SimpleNamespace`.
- Устанавливается атрибут `products` объекта `campaign.category` равным списку моковых продуктов.
- Вызывается метод `list_campaign_products` объекта `campaign`.
- Проверяется, что возвращаемый список названий продуктов содержит правильные названия.
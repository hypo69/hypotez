# Модуль `test_alipromo_campaign.py`

## Обзор

Модуль содержит набор тестов для проверки функциональности класса `AliPromoCampaign`, используемого для управления рекламными кампаниями на платформе AliExpress. В тестах проверяются различные аспекты работы класса, такие как инициализация кампании, получение информации о продуктах, создание пространства имен для продуктов и категорий, подготовка продуктов к обработке, сохранение данных о продуктах и формирование списка продуктов кампании.

## Подробней

Этот модуль использует библиотеку `pytest` для организации и запуска тестов. `pytest` позволяет определять фикстуры (fixtures) для предварительной настройки тестовой среды и упрощения написания тестов. В данном модуле определена фикстура `campaign`, которая создает экземпляр класса `AliPromoCampaign` с тестовыми данными.

Модуль содержит тесты для следующих методов класса `AliPromoCampaign`:

- `initialize_campaign`: проверяет корректность инициализации данных кампании.
- `get_category_products`: проверяет получение списка продуктов из категории как при наличии, так и при отсутствии JSON-файлов с данными о продуктах.
- `create_product_namespace`: проверяет создание пространства имен для продукта.
- `create_category_namespace`: проверяет создание пространства имен для категории.
- `create_campaign_namespace`: проверяет создание пространства имен для кампании.
- `prepare_products`: проверяет подготовку продуктов к обработке.
- `fetch_product_data`: проверяет получение данных о продуктах.
- `save_product`: проверяет сохранение данных о продукте.
- `list_campaign_products`: проверяет формирование списка продуктов кампании.

## Классы

В данном модуле нет классов, но используется фикстура `campaign`, которая создает экземпляр класса `AliPromoCampaign` для использования в тестах.

## Фикстуры

### `campaign`

**Описание**: Фикстура для создания экземпляра класса `AliPromoCampaign`.

**Параметры**:
- Нет параметров.

**Принцип работы**:
Фикстура создает экземпляр класса `AliPromoCampaign` с тестовыми данными: `campaign_name`, `category_name`, `language` и `currency`.

**Примеры**:
```python
@pytest.fixture
def campaign():
    """Fixture for creating a campaign instance."""
    return AliPromoCampaign(campaign_name, category_name, language, currency)
```

## Функции

### `test_initialize_campaign`

**Назначение**: Проверяет метод `initialize_campaign` класса `AliPromoCampaign`.

**Параметры**:
- `mocker`: Объект для создания мок-объектов и подмены зависимостей.
- `campaign`: Фикстура, предоставляющая экземпляр класса `AliPromoCampaign`.

**Возвращает**:
- Ничего. Функция проверяет утверждения (`assert`) и не возвращает значений.

**Как работает функция**:
1. Определяет мок-данные для JSON-файла.
2. Использует `mocker.patch` для замены функции `src.utils.jjson.j_loads_ns` мок-объектом, который возвращает `SimpleNamespace` с мок-данными.
3. Вызывает метод `initialize_campaign` у экземпляра класса `AliPromoCampaign`.
4. Проверяет, что атрибуты `name` и `category.test_category.name` экземпляра `campaign.campaign` соответствуют ожидаемым значениям.

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

**Назначение**: Проверяет метод `get_category_products` класса `AliPromoCampaign` в случае отсутствия JSON-файлов с данными о продуктах.

**Параметры**:
- `mocker`: Объект для создания мок-объектов и подмены зависимостей.
- `campaign`: Фикстура, предоставляющая экземпляр класса `AliPromoCampaign`.

**Возвращает**:
- Ничего. Функция проверяет утверждения (`assert`) и не возвращает значений.

**Как работает функция**:
1. Использует `mocker.patch` для замены функций `src.utils.file.get_filenames` и `src.suppliers.suppliers_list.aliexpress.campaign.ali_promo_campaign.AliPromoCampaign.fetch_product_data` мок-объектами, которые возвращают пустой список.
2. Вызывает метод `get_category_products` у экземпляра класса `AliPromoCampaign` с параметром `force=True`.
3. Проверяет, что возвращаемый список продуктов пуст.

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

**Назначение**: Проверяет метод `get_category_products` класса `AliPromoCampaign` в случае наличия JSON-файлов с данными о продуктах.

**Параметры**:
- `mocker`: Объект для создания мок-объектов и подмены зависимостей.
- `campaign`: Фикстура, предоставляющая экземпляр класса `AliPromoCampaign`.

**Возвращает**:
- Ничего. Функция проверяет утверждения (`assert`) и не возвращает значений.

**Как работает функция**:
1. Создает экземпляр `SimpleNamespace` с мок-данными о продукте.
2. Использует `mocker.patch` для замены функций `src.utils.file.get_filenames` и `src.utils.jjson.j_loads_ns` мок-объектами, которые возвращают список с именем JSON-файла и `SimpleNamespace` с данными о продукте соответственно.
3. Вызывает метод `get_category_products` у экземпляра класса `AliPromoCampaign`.
4. Проверяет, что возвращаемый список продуктов содержит один элемент, и что атрибуты `product_id` и `product_title` этого элемента соответствуют ожидаемым значениям.

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

**Назначение**: Проверяет метод `create_product_namespace` класса `AliPromoCampaign`.

**Параметры**:
- `campaign`: Фикстура, предоставляющая экземпляр класса `AliPromoCampaign`.

**Возвращает**:
- Ничего. Функция проверяет утверждения (`assert`) и не возвращает значений.

**Как работает функция**:
1. Определяет словарь с данными о продукте.
2. Вызывает метод `create_product_namespace` у экземпляра класса `AliPromoCampaign` с данными о продукте.
3. Проверяет, что атрибуты `product_id` и `product_title` возвращаемого объекта соответствуют ожидаемым значениям.

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

**Назначение**: Проверяет метод `create_category_namespace` класса `AliPromoCampaign`.

**Параметры**:
- `campaign`: Фикстура, предоставляющая экземпляр класса `AliPromoCampaign`.

**Возвращает**:
- Ничего. Функция проверяет утверждения (`assert`) и не возвращает значений.

**Как работает функция**:
1. Определяет словарь с данными о категории.
2. Вызывает метод `create_category_namespace` у экземпляра класса `AliPromoCampaign` с данными о категории.
3. Проверяет, что атрибуты `name` и `tags` возвращаемого объекта соответствуют ожидаемым значениям.

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

**Назначение**: Проверяет метод `create_campaign_namespace` класса `AliPromoCampaign`.

**Параметры**:
- `campaign`: Фикстура, предоставляющая экземпляр класса `AliPromoCampaign`.

**Возвращает**:
- Ничего. Функция проверяет утверждения (`assert`) и не возвращает значений.

**Как работает функция**:
1. Определяет словарь с данными о кампании.
2. Вызывает метод `create_campaign_namespace` у экземпляра класса `AliPromoCampaign` с данными о кампании.
3. Проверяет, что атрибуты `name` и `title` возвращаемого объекта соответствуют ожидаемым значениям.

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

**Назначение**: Проверяет метод `prepare_products` класса `AliPromoCampaign`.

**Параметры**:
- `mocker`: Объект для создания мок-объектов и подмены зависимостей.
- `campaign`: Фикстура, предоставляющая экземпляр класса `AliPromoCampaign`.

**Возвращает**:
- Ничего. Функция проверяет утверждения (`assert`) и не возвращает значений.

**Как работает функция**:
1. Использует `mocker.patch` для замены функций `src.suppliers.suppliers_list.aliexpress.campaign.ali_promo_campaign.AliPromoCampaign.get_prepared_products`, `src.utils.file.read_text_file`, `src.utils.file.get_filenames` и `src.suppliers.suppliers_list.aliexpress.campaign.ali_promo_campaign.AliPromoCampaign.process_affiliate_products` мок-объектами.
2. Вызывает метод `prepare_products` у экземпляра класса `AliPromoCampaign`.
3. Проверяет, что метод `process_affiliate_products` был вызван один раз.

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

**Назначение**: Проверяет метод `fetch_product_data` класса `AliPromoCampaign`.

**Параметры**:
- `mocker`: Объект для создания мок-объектов и подмены зависимостей.
- `campaign`: Фикстура, предоставляющая экземпляр класса `AliPromoCampaign`.

**Возвращает**:
- Ничего. Функция проверяет утверждения (`assert`) и не возвращает значений.

**Как работает функция**:
1. Определяет список идентификаторов продуктов.
2. Создает список `SimpleNamespace` с мок-данными о продуктах.
3. Использует `mocker.patch` для замены функции `src.suppliers.suppliers_list.aliexpress.campaign.ali_promo_campaign.AliPromoCampaign.process_affiliate_products` мок-объектом, который возвращает список `mock_products`.
4. Вызывает метод `fetch_product_data` у экземпляра класса `AliPromoCampaign` с идентификаторами продуктов.
5. Проверяет, что возвращаемый список продуктов содержит два элемента, и что атрибуты `product_id` этих элементов соответствуют ожидаемым значениям.

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

**Назначение**: Проверяет метод `save_product` класса `AliPromoCampaign`.

**Параметры**:
- `mocker`: Объект для создания мок-объектов и подмены зависимостей.
- `campaign`: Фикстура, предоставляющая экземпляр класса `AliPromoCampaign`.

**Возвращает**:
- Ничего. Функция проверяет утверждения (`assert`) и не возвращает значений.

**Как работает функция**:
1. Создает экземпляр `SimpleNamespace` с мок-данными о продукте.
2. Использует `mocker.patch` для замены функций `src.utils.jjson.j_dumps` и `pathlib.Path.write_text` мок-объектами.
3. Вызывает метод `save_product` у экземпляра класса `AliPromoCampaign` с данными о продукте.
4. Проверяет, что метод `Path.write_text` был вызван один раз с ожидаемыми аргументами.

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

**Назначение**: Проверяет метод `list_campaign_products` класса `AliPromoCampaign`.

**Параметры**:
- `campaign`: Фикстура, предоставляющая экземпляр класса `AliPromoCampaign`.

**Возвращает**:
- Ничего. Функция проверяет утверждения (`assert`) и не возвращает значений.

**Как работает функция**:
1. Создает экземпляры `SimpleNamespace` с мок-данными о продуктах.
2. Присваивает список продуктов атрибуту `category.products` экземпляра класса `AliPromoCampaign`.
3. Вызывает метод `list_campaign_products` у экземпляра класса `AliPromoCampaign`.
4. Проверяет, что возвращаемый список заголовков продуктов соответствует ожидаемым значениям.

**Примеры**:
```python
def test_list_campaign_products(campaign):
    """Test list_campaign_products method."""
    product1 = SimpleNamespace(product_title="Product 1")
    product2 = SimpleNamespace(product_title="Product 2")
    campaign.category.products = [product1, product2]

    product_titles = campaign.list_campaign_products()
    assert product_titles == ["Product 1", "Product 2"]
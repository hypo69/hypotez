# Модуль для тестирования AliPromoCampaign

## Обзор

Модуль содержит набор тестов для класса `AliPromoCampaign`, который используется для управления рекламными кампаниями на платформе AliExpress. Тесты охватывают различные аспекты работы класса, включая инициализацию кампании, получение продуктов из категорий, создание пространств имен продуктов, категорий и кампаний, подготовку продуктов, получение данных о продуктах, сохранение продуктов и листинг продуктов кампании.

## Подробнее

Этот модуль использует библиотеку `pytest` для организации и запуска тестов. Он также использует библиотеку `mocker` для имитации поведения внешних зависимостей, таких как файловая система и API AliExpress. Это позволяет тестировать класс `AliPromoCampaign` в изолированной среде, не зависящей от внешних факторов.

## Классы

### `AliPromoCampaign`

**Описание**: Класс для управления рекламными кампаниями на платформе AliExpress.

**Принцип работы**:

Класс `AliPromoCampaign` предоставляет методы для инициализации кампании, получения продуктов из категорий, создания пространств имен продуктов, категорий и кампаний, подготовки продуктов, получения данных о продуктах, сохранение продуктов и листинг продуктов кампании.

## Функции

### `campaign`

```python
@pytest.fixture
def campaign():
    """Fixture for creating a campaign instance."""
    return AliPromoCampaign(campaign_name, category_name, language, currency)
```

**Назначение**: Создает экземпляр класса `AliPromoCampaign` для использования в тестах.

**Параметры**:

-   Отсутствуют.

**Возвращает**:

-   `AliPromoCampaign`: Экземпляр класса `AliPromoCampaign`.

**Как работает функция**:

1.  Функция `campaign` является фикстурой `pytest`, что означает, что она выполняется перед каждым тестом, который ее использует.
2.  Она создает экземпляр класса `AliPromoCampaign` с использованием предопределенных значений `campaign_name`, `category_name`, `language` и `currency`.
3.  Возвращает созданный экземпляр класса `AliPromoCampaign`.

**Примеры**:

```python
def test_some_test(campaign):
    assert isinstance(campaign, AliPromoCampaign)
```

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

-   `mocker`: Объект `mocker` из библиотеки `pytest-mock`, используемый для имитации поведения внешних зависимостей.
-   `campaign`: Экземпляр класса `AliPromoCampaign`, созданный с помощью фикстуры `campaign`.

**Возвращает**:

-   `None`

**Как работает функция**:

1.  Создается словарь `mock_json_data`, представляющий собой имитацию данных, которые метод `initialize_campaign` должен загрузить из JSON-файла.
2.  Используется `mocker.patch` для имитации функции `src.utils.jjson.j_loads_ns`, которая обычно загружает данные из JSON-файла. Вместо этого она возвращает объект `SimpleNamespace`, созданный на основе `mock_json_data`.
3.  Вызывается метод `campaign.initialize_campaign()`.
4.  Выполняются утверждения (`assert`), чтобы убедиться, что метод `initialize_campaign` правильно инициализировал данные кампании.

**Примеры**:

```python
def test_initialize_campaign(mocker, campaign):
    # ... (код функции)
    assert campaign.campaign.name == campaign_name
    assert campaign.campaign.category.test_category.name == category_name
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

**Назначение**: Тестирует метод `get_category_products` класса `AliPromoCampaign`, когда нет JSON-файлов с данными о продуктах.

**Параметры**:

-   `mocker`: Объект `mocker` из библиотеки `pytest-mock`, используемый для имитации поведения внешних зависимостей.
-   `campaign`: Экземпляр класса `AliPromoCampaign`, созданный с помощью фикстуры `campaign`.

**Возвращает**:

-   `None`

**Как работает функция**:

1.  Используется `mocker.patch` для имитации функции `src.utils.file.get_filenames`, которая обычно возвращает список имен файлов в каталоге. В данном случае она возвращает пустой список, имитируя отсутствие JSON-файлов.
2.  Используется `mocker.patch` для имитации метода `fetch_product_data`, который отвечает за получение данных о продуктах. В данном случае он возвращает пустой список.
3.  Вызывается метод `campaign.get_category_products(force=True)`.
4.  Выполняется утверждение (`assert`), чтобы убедиться, что метод `get_category_products` возвращает пустой список, что ожидаемо, когда нет JSON-файлов с данными о продуктах.

**Примеры**:

```python
def test_get_category_products_no_json_files(mocker, campaign):
    # ... (код функции)
    assert products == []
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

**Назначение**: Тестирует метод `get_category_products` класса `AliPromoCampaign`, когда есть JSON-файлы с данными о продуктах.

**Параметры**:

-   `mocker`: Объект `mocker` из библиотеки `pytest-mock`, используемый для имитации поведения внешних зависимостей.
-   `campaign`: Экземпляр класса `AliPromoCampaign`, созданный с помощью фикстуры `campaign`.

**Возвращает**:

-   `None`

**Как работает функция**:

1.  Создается объект `mock_product_data`, представляющий собой имитацию данных продукта, загруженных из JSON-файла.
2.  Используется `mocker.patch` для имитации функции `src.utils.file.get_filenames`, которая обычно возвращает список имен файлов в каталоге. В данном случае она возвращает список, содержащий имя файла "product\_123.json", имитируя наличие JSON-файла.
3.  Используется `mocker.patch` для имитации функции `src.utils.jjson.j_loads_ns`, которая обычно загружает данные из JSON-файла. Вместо этого она возвращает объект `mock_product_data`.
4.  Вызывается метод `campaign.get_category_products()`.
5.  Выполняются утверждения (`assert`), чтобы убедиться, что метод `get_category_products` возвращает список, содержащий один продукт, и что данные этого продукта соответствуют данным, имитированным в `mock_product_data`.

**Примеры**:

```python
def test_get_category_products_with_json_files(mocker, campaign):
    # ... (код функции)
    assert len(products) == 1
    assert products[0].product_id == "123"
    assert products[0].product_title == "Test Product"
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

-   `campaign`: Экземпляр класса `AliPromoCampaign`, созданный с помощью фикстуры `campaign`.

**Возвращает**:

-   `None`

**Как работает функция**:

1.  Создается словарь `product_data`, содержащий данные о продукте.
2.  Вызывается метод `campaign.create_product_namespace(**product_data)`.
3.  Выполняются утверждения (`assert`), чтобы убедиться, что метод `create_product_namespace` правильно создал пространство имен продукта и что данные в этом пространстве имен соответствуют данным в словаре `product_data`.

**Примеры**:

```python
def test_create_product_namespace(campaign):
    # ... (код функции)
    assert product.product_id == "123"
    assert product.product_title == "Test Product"
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

-   `campaign`: Экземпляр класса `AliPromoCampaign`, созданный с помощью фикстуры `campaign`.

**Возвращает**:

-   `None`

**Как работает функция**:

1.  Создается словарь `category_data`, содержащий данные о категории.
2.  Вызывается метод `campaign.create_category_namespace(**category_data)`.
3.  Выполняются утверждения (`assert`), чтобы убедиться, что метод `create_category_namespace` правильно создал пространство имен категории и что данные в этом пространстве имен соответствуют данным в словаре `category_data`.

**Примеры**:

```python
def test_create_category_namespace(campaign):
    # ... (код функции)
    assert category.name == category_name
    assert category.tags == "tag1, tag2"
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

-   `campaign`: Экземпляр класса `AliPromoCampaign`, созданный с помощью фикстуры `campaign`.

**Возвращает**:

-   `None`

**Как работает функция**:

1.  Создается словарь `campaign_data`, содержащий данные о кампании.
2.  Вызывается метод `campaign.create_campaign_namespace(**campaign_data)`.
3.  Выполняются утверждения (`assert`), чтобы убедиться, что метод `create_campaign_namespace` правильно создал пространство имен кампании и что данные в этом пространстве имен соответствуют данным в словаре `campaign_data`.

**Примеры**:

```python
def test_create_campaign_namespace(campaign):
    # ... (код функции)
    assert camp.name == campaign_name
    assert camp.title == "Test Campaign"
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

-   `mocker`: Объект `mocker` из библиотеки `pytest-mock`, используемый для имитации поведения внешних зависимостей.
-   `campaign`: Экземпляр класса `AliPromoCampaign`, созданный с помощью фикстуры `campaign`.

**Возвращает**:

-   `None`

**Как работает функция**:

1.  Используется `mocker.patch` для имитации метода `get_prepared_products`, который возвращает список подготовленных продуктов. В данном случае он возвращает пустой список.
2.  Используется `mocker.patch` для имитации функции `read_text_file`, которая читает содержимое текстового файла. В данном случае она возвращает строку "source\_data".
3.  Используется `mocker.patch` для имитации функции `get_filenames`, которая возвращает список имен файлов в каталоге. В данном случае она возвращает список, содержащий имя файла "source.html".
4.  Используется `mocker.patch` для имитации метода `process_affiliate_products`, который обрабатывает продукты партнерской программы.
5.  Вызывается метод `campaign.prepare_products()`.
6.  Выполняется утверждение (`assert`), чтобы убедиться, что метод `process_affiliate_products` был вызван один раз.

**Примеры**:

```python
def test_prepare_products(mocker, campaign):
    # ... (код функции)
    campaign.process_affiliate_products.assert_called_once()
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

-   `mocker`: Объект `mocker` из библиотеки `pytest-mock`, используемый для имитации поведения внешних зависимостей.
-   `campaign`: Экземпляр класса `AliPromoCampaign`, созданный с помощью фикстуры `campaign`.

**Возвращает**:

-   `None`

**Как работает функция**:

1.  Создается список `product_ids`, содержащий идентификаторы продуктов.
2.  Создается список `mock_products`, содержащий имитацию данных о продуктах.
3.  Используется `mocker.patch` для имитации метода `process_affiliate_products`, который обрабатывает продукты партнерской программы. В данном случае он возвращает список `mock_products`.
4.  Вызывается метод `campaign.fetch_product_data(product_ids)`.
5.  Выполняются утверждения (`assert`), чтобы убедиться, что метод `fetch_product_data` возвращает список, содержащий данные о продуктах, и что данные этих продуктов соответствуют данным, имитированным в `mock_products`.

**Примеры**:

```python
def test_fetch_product_data(mocker, campaign):
    # ... (код функции)
    assert len(products) == 2
    assert products[0].product_id == "123"
    assert products[1].product_id == "456"
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

-   `mocker`: Объект `mocker` из библиотеки `pytest-mock`, используемый для имитации поведения внешних зависимостей.
-   `campaign`: Экземпляр класса `AliPromoCampaign`, созданный с помощью фикстуры `campaign`.

**Возвращает**:

-   `None`

**Как работает функция**:

1.  Создается объект `product`, представляющий собой имитацию данных продукта.
2.  Используется `mocker.patch` для имитации функции `j_dumps`, которая преобразует данные в формат JSON. В данном случае она возвращает пустую строку "{}".
3.  Используется `mocker.patch` для имитации метода `write_text` класса `Path`, который записывает данные в текстовый файл.
4.  Вызывается метод `campaign.save_product(product)`.
5.  Выполняется утверждение (`assert`), чтобы убедиться, что метод `write_text` был вызван один раз с правильными аргументами.

**Примеры**:

```python
def test_save_product(mocker, campaign):
    # ... (код функции)
    Path.write_text.assert_called_once_with("{}", encoding='utf-8')
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

-   `campaign`: Экземпляр класса `AliPromoCampaign`, созданный с помощью фикстуры `campaign`.

**Возвращает**:

-   `None`

**Как работает функция**:

1.  Создаются два объекта `product1` и `product2`, представляющие собой имитацию данных о продуктах.
2.  Список `campaign.category.products` заполняется этими объектами.
3.  Вызывается метод `campaign.list_campaign_products()`.
4.  Выполняются утверждения (`assert`), чтобы убедиться, что метод `list_campaign_products` возвращает список, содержащий заголовки продуктов, и что заголовки продуктов соответствуют заголовкам, имитированным в `product1` и `product2`.

**Примеры**:

```python
def test_list_campaign_products(campaign):
    # ... (код функции)
    assert product_titles == ["Product 1", "Product 2"]
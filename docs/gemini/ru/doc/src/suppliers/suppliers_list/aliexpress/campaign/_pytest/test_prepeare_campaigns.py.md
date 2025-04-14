# Модуль тестирования подготовки кампаний (test_prepeare_campaigns.py)

## Обзор

Модуль `test_prepeare_campaigns.py` содержит набор тестов pytest для проверки функциональности модуля `prepare_campaigns.py`, который отвечает за подготовку и обработку рекламных кампаний AliExpress. В частности, модуль тестирует функции обновления категорий, обработки категорий кампаний и обработки самих кампаний.

## Подробней

Этот файл предоставляет модульные тесты для различных функций, связанных с подготовкой кампаний AliExpress. Он использует библиотеку `pytest` для организации тестов, `unittest.mock` для создания мок-объектов и `asyncio` для асинхронных тестов.

## Фикстуры

### `mock_j_loads`

```python
@pytest.fixture
def mock_j_loads():
    with patch("src.utils.jjson.j_loads") as mock:
        yield mock
```

Фикстура `mock_j_loads` предоставляет мок-объект для функции `j_loads` из модуля `src.utils.jjson`. Функция `j_loads` используется для загрузки данных из JSON-файлов. Мок-объект позволяет изолировать тестируемый код от реальной файловой системы и контролировать возвращаемые значения.

### `mock_j_dumps`

```python
@pytest.fixture
def mock_j_dumps():
    with patch("src.utils.jjson.j_dumps") as mock:
        yield mock
```

Фикстура `mock_j_dumps` предоставляет мок-объект для функции `j_dumps` из модуля `src.utils.jjson`. Функция `j_dumps` используется для сохранения данных в JSON-файлы. Мок-объект позволяет проверить, что тестируемый код вызывает эту функцию с правильными аргументами.

### `mock_logger`

```python
@pytest.fixture
def mock_logger():
    with patch("src.logger.logger") as mock:
        yield mock
```

Фикстура `mock_logger` предоставляет мок-объект для модуля `logger` из `src.logger.logger`. Это позволяет перехватывать вызовы функций логирования (`logger.error`, `logger.warning`, `logger.info` и т. д.) и проверять, что тестируемый код правильно регистрирует события.

### `mock_get_directory_names`

```python
@pytest.fixture
def mock_get_directory_names():
    with patch("src.utils.get_directory_names") as mock:
        yield mock
```

Фикстура `mock_get_directory_names` предоставляет мок-объект для функции `get_directory_names` из модуля `src.utils`. Эта функция, вероятно, используется для получения списка имен подкаталогов в указанном каталоге.

### `mock_ali_promo_campaign`

```python
@pytest.fixture
def mock_ali_promo_campaign():
    with patch("src.suppliers.suppliers_list.aliexpress.campaign.AliPromoCampaign") as mock:
        yield mock
```

Фикстура `mock_ali_promo_campaign` предоставляет мок-объект для класса `AliPromoCampaign` из модуля `src.suppliers.suppliers_list.aliexpress.campaign`. Этот класс, вероятно, отвечает за обработку рекламных кампаний AliExpress. Мок-объект позволяет изолировать тестируемый код от реальной логики обработки кампаний.

## Функции

### `test_update_category_success`

```python
def test_update_category_success(mock_j_loads, mock_j_dumps, mock_logger):
    mock_json_path = Path("mock/path/to/category.json")
    mock_category = SimpleNamespace(name="test_category")

    mock_j_loads.return_value = {"category": {}}
    
    result = update_category(mock_json_path, mock_category)
    
    assert result is True
    mock_j_dumps.assert_called_once_with({"category": {"name": "test_category"}}, mock_json_path)
    mock_logger.error.assert_not_called()
```

Функция `test_update_category_success` тестирует успешное обновление категории.

**Параметры:**

-   `mock_j_loads`: Мок-объект для функции `j_loads`.
-   `mock_j_dumps`: Мок-объект для функции `j_dumps`.
-   `mock_logger`: Мок-объект для модуля `logger`.

**Как работает функция:**

1.  Определяет фиктивный путь к JSON-файлу (`mock_json_path`) и создает фиктивный объект категории (`mock_category`).
2.  Настраивает мок-объект `mock_j_loads` так, чтобы он возвращал пустой словарь `{"category": {}}`.
3.  Вызывает функцию `update_category` с фиктивными данными.
4.  Проверяет, что функция `update_category` вернула `True` (успех).
5.  Проверяет, что функция `j_dumps` была вызвана один раз с ожидаемыми аргументами (обновленные данные и путь к файлу).
6.  Проверяет, что функция `logger.error` не была вызвана (отсутствие ошибок).

**Примеры:**

Пример успешного обновления категории:

```python
test_update_category_success(mock_j_loads, mock_j_dumps, mock_logger)
```

### `test_update_category_failure`

```python
def test_update_category_failure(mock_j_loads, mock_j_dumps, mock_logger):
    mock_json_path = Path("mock/path/to/category.json")
    mock_category = SimpleNamespace(name="test_category")

    mock_j_loads.side_effect = Exception("Error")
    
    result = update_category(mock_json_path, mock_category)
    
    assert result is False
    mock_j_dumps.assert_not_called()
    mock_logger.error.assert_called_once()
```

Функция `test_update_category_failure` тестирует ситуацию, когда обновление категории завершается неудачно (например, при ошибке чтения файла).

**Параметры:**

-   `mock_j_loads`: Мок-объект для функции `j_loads`.
-   `mock_j_dumps`: Мок-объект для функции `j_dumps`.
-   `mock_logger`: Мок-объект для модуля `logger`.

**Как работает функция:**

1.  Определяет фиктивный путь к JSON-файлу (`mock_json_path`) и создает фиктивный объект категории (`mock_category`).
2.  Настраивает мок-объект `mock_j_loads` так, чтобы он вызывал исключение `Exception("Error")` при вызове.
3.  Вызывает функцию `update_category` с фиктивными данными.
4.  Проверяет, что функция `update_category` вернула `False` (неудача).
5.  Проверяет, что функция `j_dumps` не была вызвана.
6.  Проверяет, что функция `logger.error` была вызвана один раз (зарегистрирована ошибка).

**Примеры:**

Пример неудачного обновления категории:

```python
test_update_category_failure(mock_j_loads, mock_j_dumps, mock_logger)
```

### `test_process_campaign_category_success`

```python
@pytest.mark.asyncio
async def test_process_campaign_category_success(mock_ali_promo_campaign, mock_logger):
    mock_campaign_name = "test_campaign"
    mock_category_name = "test_category"
    mock_language = "EN"
    mock_currency = "USD"

    mock_ali_promo = mock_ali_promo_campaign.return_value
    mock_ali_promo.process_affiliate_products = MagicMock()

    result = await process_campaign_category(mock_campaign_name, mock_category_name, mock_language, mock_currency)

    assert result is not None
    mock_logger.error.assert_not_called()
```

Функция `test_process_campaign_category_success` тестирует успешную обработку категории кампании.

**Параметры:**

-   `mock_ali_promo_campaign`: Мок-объект для класса `AliPromoCampaign`.
-   `mock_logger`: Мок-объект для модуля `logger`.

**Как работает функция:**

1.  Определяет фиктивные значения для имени кампании (`mock_campaign_name`), имени категории (`mock_category_name`), языка (`mock_language`) и валюты (`mock_currency`).
2.  Создает мок-объект `mock_ali_promo` на основе `mock_ali_promo_campaign` и заменяет метод `process_affiliate_products` на `MagicMock`.
3.  Вызывает асинхронную функцию `process_campaign_category` с фиктивными данными.
4.  Проверяет, что функция `process_campaign_category` вернула не `None`.
5.  Проверяет, что функция `logger.error` не была вызвана (отсутствие ошибок).

**Примеры:**

Пример успешной обработки категории кампании:

```python
await test_process_campaign_category_success(mock_ali_promo_campaign, mock_logger)
```

### `test_process_campaign_category_failure`

```python
@pytest.mark.asyncio
async def test_process_campaign_category_failure(mock_ali_promo_campaign, mock_logger):
    mock_campaign_name = "test_campaign"
    mock_category_name = "test_category"
    mock_language = "EN"
    mock_currency = "USD"

    mock_ali_promo = mock_ali_promo_campaign.return_value
    mock_ali_promo.process_affiliate_products.side_effect = Exception("Error")

    result = await process_campaign_category(mock_campaign_name, mock_category_name, mock_language, mock_currency)

    assert result is None
    mock_logger.error.assert_called_once()
```

Функция `test_process_campaign_category_failure` тестирует ситуацию, когда обработка категории кампании завершается неудачно.

**Параметры:**

-   `mock_ali_promo_campaign`: Мок-объект для класса `AliPromoCampaign`.
-   `mock_logger`: Мок-объект для модуля `logger`.

**Как работает функция:**

1.  Определяет фиктивные значения для имени кампании (`mock_campaign_name`), имени категории (`mock_category_name`), языка (`mock_language`) и валюты (`mock_currency`).
2.  Создает мок-объект `mock_ali_promo` на основе `mock_ali_promo_campaign` и настраивает метод `process_affiliate_products` так, чтобы он вызывал исключение `Exception("Error")`.
3.  Вызывает асинхронную функцию `process_campaign_category` с фиктивными данными.
4.  Проверяет, что функция `process_campaign_category` вернула `None`.
5.  Проверяет, что функция `logger.error` была вызвана один раз (зарегистрирована ошибка).

**Примеры:**

Пример неудачной обработки категории кампании:

```python
await test_process_campaign_category_failure(mock_ali_promo_campaign, mock_logger)
```

### `test_process_campaign`

```python
def test_process_campaign(mock_get_directory_names, mock_logger):
    mock_campaign_name = "test_campaign"
    mock_categories = ["category1", "category2"]
    mock_language = "EN"
    mock_currency = "USD"
    mock_force = False

    mock_get_directory_names.return_value = mock_categories

    results = process_campaign(mock_campaign_name, mock_categories, mock_language, mock_currency, mock_force)

    assert len(results) == 2
    for category_name, result in results:
        assert category_name in mock_categories
        assert result is not None
    mock_logger.warning.assert_not_called()
```

Функция `test_process_campaign` тестирует обработку кампании.

**Параметры:**

-   `mock_get_directory_names`: Мок-объект для функции `get_directory_names`.
-   `mock_logger`: Мок-объект для модуля `logger`.

**Как работает функция:**

1.  Определяет фиктивные значения для имени кампании (`mock_campaign_name`), списка категорий (`mock_categories`), языка (`mock_language`), валюты (`mock_currency`) и флага `force` (`mock_force`).
2.  Настраивает мок-объект `mock_get_directory_names` так, чтобы он возвращал список категорий (`mock_categories`).
3.  Вызывает функцию `process_campaign` с фиктивными данными.
4.  Проверяет, что длина списка результатов равна 2 (количество категорий).
5.  Проверяет, что каждая категория из списка результатов присутствует в списке `mock_categories` и что результат для каждой категории не `None`.
6.  Проверяет, что функция `logger.warning` не была вызвана (отсутствие предупреждений).

**Примеры:**

Пример обработки кампании:

```python
test_process_campaign(mock_get_directory_names, mock_logger)
```

### `test_main`

```python
@pytest.mark.asyncio
async def test_main(mock_get_directory_names):
    mock_campaign_name = "test_campaign"
    mock_categories = ["category1", "category2"]
    mock_language = "EN"
    mock_currency = "USD"
    mock_force = False

    mock_get_directory_names.return_value = mock_categories

    await main(mock_campaign_name, mock_categories, mock_language, mock_currency, mock_force)

    mock_get_directory_names.assert_called_once()
```

Функция `test_main` тестирует главную функцию `main`.

**Параметры:**

-   `mock_get_directory_names`: Мок-объект для функции `get_directory_names`.

**Как работает функция:**

1.  Определяет фиктивные значения для имени кампании (`mock_campaign_name`), списка категорий (`mock_categories`), языка (`mock_language`), валюты (`mock_currency`) и флага `force` (`mock_force`).
2.  Настраивает мок-объект `mock_get_directory_names` так, чтобы он возвращал список категорий (`mock_categories`).
3.  Вызывает асинхронную функцию `main` с фиктивными данными.
4.  Проверяет, что функция `get_directory_names` была вызвана один раз.

**Примеры:**

Пример вызова главной функции:

```python
await test_main(mock_get_directory_names)
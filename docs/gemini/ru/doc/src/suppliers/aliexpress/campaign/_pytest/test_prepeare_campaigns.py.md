# Модуль для тестирования подготовки кампаний AliExpress

## Обзор

Модуль содержит набор тестов для проверки функциональности подготовки кампаний в AliExpress.
Он использует `pytest` для организации тестов и `unittest.mock` для имитации различных зависимостей и компонентов системы.
Модуль включает тесты для функций `update_category`, `process_campaign_category`, `process_campaign` и `main`,
обеспечивая проверку различных сценариев, включая успешное выполнение и обработку ошибок.

## Подробней

Этот модуль предназначен для автоматизированного тестирования процесса подготовки рекламных кампаний AliExpress.
Он использует моки для изоляции тестируемых функций и проверки их взаимодействия с другими компонентами,
такими как чтение и запись JSON-файлов, логирование и обработка данных о партнерских продуктах.
Тесты охватывают различные аспекты подготовки кампаний, включая обновление категорий, обработку кампаний по категориям
и общую координацию процесса подготовки кампаний.

## Фикстуры

### `mock_j_loads`

```python
@pytest.fixture
def mock_j_loads():
    with patch("src.utils.jjson.j_loads") as mock:
        yield mock
```

**Описание**: Фикстура `mock_j_loads` используется для имитации функции `j_loads` из модуля `src.utils.jjson`.
Она позволяет перехватывать вызовы `j_loads` и контролировать возвращаемые значения,
что полезно для изоляции тестируемого кода от реального чтения JSON-файлов.

### `mock_j_dumps`

```python
@pytest.fixture
def mock_j_dumps():
    with patch("src.utils.jjson.j_dumps") as mock:
        yield mock
```

**Описание**: Фикстура `mock_j_dumps` используется для имитации функции `j_dumps` из модуля `src.utils.jjson`.
Она позволяет перехватывать вызовы `j_dumps` и проверять, какие данные были переданы для записи в JSON-файл.

### `mock_logger`

```python
@pytest.fixture
def mock_logger():
    with patch("src.logger.logger") as mock:
        yield mock
```

**Описание**: Фикстура `mock_logger` используется для имитации объекта `logger` из модуля `src.logger`.
Она позволяет перехватывать вызовы методов логирования (`error`, `warning`, `info` и т.д.) и проверять,
какие сообщения были зарегистрированы в процессе выполнения теста.

### `mock_get_directory_names`

```python
@pytest.fixture
def mock_get_directory_names():
    with patch("src.utils.get_directory_names") as mock:
        yield mock
```

**Описание**: Фикстура `mock_get_directory_names` используется для имитации функции `get_directory_names`
из модуля `src.utils`. Она позволяет контролировать список категорий, возвращаемый функцией,
что полезно для тестирования логики обработки кампаний по категориям.

### `mock_ali_promo_campaign`

```python
@pytest.fixture
def mock_ali_promo_campaign():
    with patch("src.suppliers.aliexpress.campaign.AliPromoCampaign") as mock:
        yield mock
```

**Описание**: Фикстура `mock_ali_promo_campaign` используется для имитации класса `AliPromoCampaign`
из модуля `src.suppliers.aliexpress.campaign`. Она позволяет перехватывать создание экземпляров класса
и контролировать поведение имитированного объекта, что полезно для тестирования взаимодействия
с логикой обработки партнерских продуктов AliExpress.

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

**Назначение**: Тест проверяет успешное обновление категории.

**Параметры**:
- `mock_j_loads`: Мок функции `j_loads`.
- `mock_j_dumps`: Мок функции `j_dumps`.
- `mock_logger`: Мок объекта `logger`.

**Как работает функция**:
1. Определяет путь к JSON-файлу и создает объект `SimpleNamespace` с именем категории.
2. Настраивает мок `mock_j_loads` так, чтобы он возвращал пустой словарь для категории.
3. Вызывает функцию `update_category` с мокированным путем и объектом категории.
4. Проверяет, что функция вернула `True` (успешное обновление).
5. Проверяет, что функция `mock_j_dumps` была вызвана один раз с ожидаемыми данными и путем.
6. Проверяет, что функция `mock_logger.error` не была вызвана (отсутствие ошибок).

**Примеры**:

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

**Назначение**: Тест проверяет ситуацию, когда обновление категории завершается с ошибкой.

**Параметры**:
- `mock_j_loads`: Мок функции `j_loads`.
- `mock_j_dumps`: Мок функции `j_dumps`.
- `mock_logger`: Мок объекта `logger`.

**Как работает функция**:
1. Определяет путь к JSON-файлу и создает объект `SimpleNamespace` с именем категории.
2. Настраивает мок `mock_j_loads` так, чтобы он вызывал исключение при вызове.
3. Вызывает функцию `update_category` с мокированным путем и объектом категории.
4. Проверяет, что функция вернула `False` (обновление не удалось).
5. Проверяет, что функция `mock_j_dumps` не была вызвана (запись не производилась из-за ошибки).
6. Проверяет, что функция `mock_logger.error` была вызвана один раз (ошибка была залогирована).

**Примеры**:

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

**Назначение**: Тест проверяет успешную обработку категории кампании.

**Параметры**:
- `mock_ali_promo_campaign`: Мок класса `AliPromoCampaign`.
- `mock_logger`: Мок объекта `logger`.

**Как работает функция**:
1. Определяет параметры кампании (имя, категория, язык, валюта).
2. Настраивает мок `mock_ali_promo_campaign` так, чтобы он возвращал имитированный объект `AliPromoCampaign`.
3. Настраивает мок метода `process_affiliate_products` так, чтобы он ничего не делал.
4. Вызывает функцию `process_campaign_category` с мокированными параметрами.
5. Проверяет, что функция вернула не `None` (обработка выполнена успешно).
6. Проверяет, что функция `mock_logger.error` не была вызвана (отсутствие ошибок).

**Примеры**:

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

**Назначение**: Тест проверяет ситуацию, когда обработка категории кампании завершается с ошибкой.

**Параметры**:
- `mock_ali_promo_campaign`: Мок класса `AliPromoCampaign`.
- `mock_logger`: Мок объекта `logger`.

**Как работает функция**:
1. Определяет параметры кампании (имя, категория, язык, валюта).
2. Настраивает мок `mock_ali_promo_campaign` так, чтобы он возвращал имитированный объект `AliPromoCampaign`.
3. Настраивает мок метода `process_affiliate_products` так, чтобы он вызывал исключение при вызове.
4. Вызывает функцию `process_campaign_category` с мокированными параметрами.
5. Проверяет, что функция вернула `None` (обработка не удалась).
6. Проверяет, что функция `mock_logger.error` была вызвана один раз (ошибка была залогирована).

**Примеры**:

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

**Назначение**: Тест проверяет общую логику обработки кампании.

**Параметры**:
- `mock_get_directory_names`: Мок функции `get_directory_names`.
- `mock_logger`: Мок объекта `logger`.

**Как работает функция**:
1. Определяет параметры кампании (имя, список категорий, язык, валюта, флаг принудительного обновления).
2. Настраивает мок `mock_get_directory_names` так, чтобы он возвращал список категорий.
3. Вызывает функцию `process_campaign` с мокированными параметрами.
4. Проверяет, что функция вернула список результатов, содержащий результаты для каждой категории.
5. Проверяет, что функция `mock_logger.warning` не была вызвана (отсутствие предупреждений).

**Примеры**:

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

**Назначение**: Тест проверяет функцию `main`.

**Параметры**:
- `mock_get_directory_names`: Мок функции `get_directory_names`.

**Как работает функция**:
1. Определяет параметры кампании (имя, список категорий, язык, валюта, флаг принудительного обновления).
2. Настраивает мок `mock_get_directory_names` так, чтобы он возвращал список категорий.
3. Вызывает асинхронную функцию `main` с мокированными параметрами.
4. Проверяет, что функция `mock_get_directory_names` была вызвана один раз.

**Примеры**:

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
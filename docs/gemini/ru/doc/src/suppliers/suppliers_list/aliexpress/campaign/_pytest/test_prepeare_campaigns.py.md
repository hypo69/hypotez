# Модуль тестирования для обработки кампаний AliExpress

## Обзор

Этот модуль содержит набор юнит-тестов для функций, отвечающих за подготовку кампаний AliExpress. Тесты проверяют правильность работы функций, таких как `update_category`, `process_campaign_category`, `process_campaign` и `main`. Тесты используют моки для имитации взаимодействия с внешними сервисами и файловой системой.

## Подробнее

Тесты используют моки для имитации работы следующих функций:

- `j_loads` - для загрузки JSON-данных из файла
- `j_dumps` - для сохранения JSON-данных в файл
- `logger` - для логирования ошибок и сообщений
- `get_directory_names` - для получения списка имен категорий
- `AliPromoCampaign` - для имитации работы класса, отвечающего за обработку кампаний

## Классы

### `test_prepeare_campaigns`

**Описание**: Класс содержит набор юнит-тестов для функций, отвечающих за подготовку кампаний AliExpress.

**Атрибуты**:

- `mock_j_loads` (мокинг): Мокинг для имитации работы функции `j_loads`
- `mock_j_dumps` (мокинг): Мокинг для имитации работы функции `j_dumps`
- `mock_logger` (мокинг): Мокинг для имитации работы логгера
- `mock_get_directory_names` (мокинг): Мокинг для имитации работы функции `get_directory_names`
- `mock_ali_promo_campaign` (мокинг): Мокинг для имитации работы класса `AliPromoCampaign`

## Функции

### `test_update_category_success`

**Назначение**: Тест для проверки успешного обновления категории.

**Параметры**:

- `mock_j_loads` (мокинг): Мокинг для имитации работы функции `j_loads`
- `mock_j_dumps` (мокинг): Мокинг для имитации работы функции `j_dumps`
- `mock_logger` (мокинг): Мокинг для имитации работы логгера

**Возвращает**:

- `None`: Тест не возвращает значение.

**Как работает функция**:

- Тест проверяет, что функция `update_category` возвращает `True` в случае успеха.
- Тест проверяет, что функция `j_dumps` вызывается один раз для сохранения обновленной информации о категории.
- Тест проверяет, что функция `logger.error` не вызывается, так как ошибок не возникло.

**Примеры**:

```python
# Тест для проверки успешного обновления категории
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

**Назначение**: Тест для проверки неудачного обновления категории.

**Параметры**:

- `mock_j_loads` (мокинг): Мокинг для имитации работы функции `j_loads`
- `mock_j_dumps` (мокинг): Мокинг для имитации работы функции `j_dumps`
- `mock_logger` (мокинг): Мокинг для имитации работы логгера

**Возвращает**:

- `None`: Тест не возвращает значение.

**Как работает функция**:

- Тест проверяет, что функция `update_category` возвращает `False` в случае ошибки.
- Тест проверяет, что функция `j_dumps` не вызывается, так как ошибка произошла до сохранения данных.
- Тест проверяет, что функция `logger.error` вызывается один раз для записи сообщения об ошибке.

**Примеры**:

```python
# Тест для проверки неудачного обновления категории
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

**Назначение**: Тест для проверки успешной обработки категории кампании.

**Параметры**:

- `mock_ali_promo_campaign` (мокинг): Мокинг для имитации работы класса `AliPromoCampaign`
- `mock_logger` (мокинг): Мокинг для имитации работы логгера

**Возвращает**:

- `None`: Тест не возвращает значение.

**Как работает функция**:

- Тест проверяет, что функция `process_campaign_category` возвращает не `None` в случае успеха.
- Тест проверяет, что функция `logger.error` не вызывается, так как ошибок не возникло.

**Примеры**:

```python
# Тест для проверки успешной обработки категории кампании
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

**Назначение**: Тест для проверки неудачной обработки категории кампании.

**Параметры**:

- `mock_ali_promo_campaign` (мокинг): Мокинг для имитации работы класса `AliPromoCampaign`
- `mock_logger` (мокинг): Мокинг для имитации работы логгера

**Возвращает**:

- `None`: Тест не возвращает значение.

**Как работает функция**:

- Тест проверяет, что функция `process_campaign_category` возвращает `None` в случае ошибки.
- Тест проверяет, что функция `logger.error` вызывается один раз для записи сообщения об ошибке.

**Примеры**:

```python
# Тест для проверки неудачной обработки категории кампании
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

**Назначение**: Тест для проверки обработки кампании.

**Параметры**:

- `mock_get_directory_names` (мокинг): Мокинг для имитации работы функции `get_directory_names`
- `mock_logger` (мокинг): Мокинг для имитации работы логгера

**Возвращает**:

- `None`: Тест не возвращает значение.

**Как работает функция**:

- Тест проверяет, что функция `process_campaign` возвращает список результатов для каждой категории.
- Тест проверяет, что количество результатов соответствует количеству категорий.
- Тест проверяет, что для каждой категории результат не равен `None`.
- Тест проверяет, что функция `logger.warning` не вызывается, так как ошибок не возникло.

**Примеры**:

```python
# Тест для проверки обработки кампании
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

**Назначение**: Тест для проверки главной функции.

**Параметры**:

- `mock_get_directory_names` (мокинг): Мокинг для имитации работы функции `get_directory_names`

**Возвращает**:

- `None`: Тест не возвращает значение.

**Как работает функция**:

- Тест проверяет, что функция `main` вызывается один раз.
- Тест проверяет, что функция `get_directory_names` вызывается один раз для получения списка категорий.

**Примеры**:

```python
# Тест для проверки главной функции
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
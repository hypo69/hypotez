# Модуль для тестирования подготовки кампаний AliExpress

## Обзор

Модуль `test_prepeare_campaigns.py` содержит набор тестов для функций, связанных с подготовкой кампаний AliExpress, включая обновление категорий, обработку кампаний по категориям и общую обработку кампаний. В тестах используются фикстуры pytest для имитации внешних зависимостей, таких как загрузка и сохранение JSON, логирование и асинхронные операции.

## Подробней

Этот модуль предназначен для автоматизированного тестирования функций подготовки кампаний AliExpress. Он использует библиотеку `pytest` для организации тестов и `unittest.mock` для имитации зависимостей, таких как файловый ввод-вывод, API AliExpress и логирование. Модуль гарантирует, что функции подготовки кампаний работают правильно, обрабатывают ошибки и корректно взаимодействуют с внешними сервисами.

## Фикстуры

### `mock_j_loads`

```python
@pytest.fixture
def mock_j_loads():
    with patch("src.utils.jjson.j_loads") as mock:
        yield mock
```

**Описание**: Фикстура `mock_j_loads` имитирует функцию `j_loads` из модуля `src.utils.jjson`.

### `mock_j_dumps`

```python
@pytest.fixture
def mock_j_dumps():
    with patch("src.utils.jjson.j_dumps") as mock:
        yield mock
```

**Описание**: Фикстура `mock_j_dumps` имитирует функцию `j_dumps` из модуля `src.utils.jjson`.

### `mock_logger`

```python
@pytest.fixture
def mock_logger():
    with patch("src.logger.logger") as mock:
        yield mock
```

**Описание**: Фикстура `mock_logger` имитирует модуль `logger` из `src.logger`.

### `mock_get_directory_names`

```python
@pytest.fixture
def mock_get_directory_names():
    with patch("src.utils.get_directory_names") as mock:
        yield mock
```

**Описание**: Фикстура `mock_get_directory_names` имитирует функцию `get_directory_names` из модуля `src.utils`.

### `mock_ali_promo_campaign`

```python
@pytest.fixture
def mock_ali_promo_campaign():
    with patch("src.suppliers.aliexpress.campaign.AliPromoCampaign") as mock:
        yield mock
```

**Описание**: Фикстура `mock_ali_promo_campaign` имитирует класс `AliPromoCampaign` из модуля `src.suppliers.aliexpress.campaign`.

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

**Назначение**: Проверяет успешное обновление категории.

**Параметры**:
- `mock_j_loads`: Имитация функции `j_loads`.
- `mock_j_dumps`: Имитация функции `j_dumps`.
- `mock_logger`: Имитация модуля `logger`.

**Как работает функция**:
1. **Инициализация**: Создаются моковые объекты `mock_json_path` (путь к файлу) и `mock_category` (категория).
2. **Настройка имитации**: Устанавливается возвращаемое значение для `mock_j_loads` в виде пустого словаря `{"category": {}}`.
3. **Вызов функции**: Вызывается функция `update_category` с моковыми объектами.
4. **Проверки**:
   - Проверяется, что функция вернула `True`.
   - Проверяется, что функция `mock_j_dumps` была вызвана один раз с ожидаемыми аргументами.
   - Проверяется, что функция `mock_logger.error` не вызывалась.

```
Инициализация → Настройка имитации → Вызов update_category → Проверки
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

**Назначение**: Проверяет обработку ошибки при обновлении категории.

**Параметры**:
- `mock_j_loads`: Имитация функции `j_loads`.
- `mock_j_dumps`: Имитация функции `j_dumps`.
- `mock_logger`: Имитация модуля `logger`.

**Как работает функция**:
1. **Инициализация**: Создаются моковые объекты `mock_json_path` и `mock_category`.
2. **Настройка имитации**: Устанавливается имитация исключения при вызове `mock_j_loads`.
3. **Вызов функции**: Вызывается функция `update_category` с моковыми объектами.
4. **Проверки**:
   - Проверяется, что функция вернула `False`.
   - Проверяется, что функция `mock_j_dumps` не вызывалась.
   - Проверяется, что функция `mock_logger.error` была вызвана один раз.

```
Инициализация → Настройка имитации → Вызов update_category → Проверки
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

**Назначение**: Проверяет успешную обработку категории кампании.

**Параметры**:
- `mock_ali_promo_campaign`: Имитация класса `AliPromoCampaign`.
- `mock_logger`: Имитация модуля `logger`.

**Как работает функция**:
1. **Инициализация**: Определяются моковые значения для имени кампании, имени категории, языка и валюты.
2. **Настройка имитации**: Создается имитация метода `process_affiliate_products` класса `AliPromoCampaign`.
3. **Вызов функции**: Вызывается асинхронная функция `process_campaign_category` с моковыми значениями.
4. **Проверки**:
   - Проверяется, что функция вернула не `None`.
   - Проверяется, что функция `mock_logger.error` не вызывалась.

```
Инициализация → Настройка имитации → Вызов process_campaign_category → Проверки
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

**Назначение**: Проверяет обработку ошибки при обработке категории кампании.

**Параметры**:
- `mock_ali_promo_campaign`: Имитация класса `AliPromoCampaign`.
- `mock_logger`: Имитация модуля `logger`.

**Как работает функция**:
1. **Инициализация**: Определяются моковые значения для имени кампании, имени категории, языка и валюты.
2. **Настройка имитации**: Устанавливается имитация исключения при вызове метода `process_affiliate_products`.
3. **Вызов функции**: Вызывается асинхронная функция `process_campaign_category` с моковыми значениями.
4. **Проверки**:
   - Проверяется, что функция вернула `None`.
   - Проверяется, что функция `mock_logger.error` была вызвана один раз.

```
Инициализация → Настройка имитации → Вызов process_campaign_category → Проверки
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

**Назначение**: Проверяет обработку кампании.

**Параметры**:
- `mock_get_directory_names`: Имитация функции `get_directory_names`.
- `mock_logger`: Имитация модуля `logger`.

**Как работает функция**:
1. **Инициализация**: Определяются моковые значения для имени кампании, списка категорий, языка, валюты и флага `force`.
2. **Настройка имитации**: Устанавливается возвращаемое значение для `mock_get_directory_names` в виде списка категорий.
3. **Вызов функции**: Вызывается функция `process_campaign` с моковыми значениями.
4. **Проверки**:
   - Проверяется, что длина списка результатов равна 2.
   - Проверяется, что каждая категория присутствует в списке моковых категорий и результат не равен `None`.
   - Проверяется, что функция `mock_logger.warning` не вызывалась.

```
Инициализация → Настройка имитации → Вызов process_campaign → Проверки
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

**Назначение**: Проверяет основную функцию `main`.

**Параметры**:
- `mock_get_directory_names`: Имитация функции `get_directory_names`.

**Как работает функция**:
1. **Инициализация**: Определяются моковые значения для имени кампании, списка категорий, языка, валюты и флага `force`.
2. **Настройка имитации**: Устанавливается возвращаемое значение для `mock_get_directory_names` в виде списка категорий.
3. **Вызов функции**: Вызывается асинхронная функция `main` с моковыми значениями.
4. **Проверки**:
   - Проверяется, что функция `mock_get_directory_names` была вызвана один раз.

```
Инициализация → Настройка имитации → Вызов main → Проверки
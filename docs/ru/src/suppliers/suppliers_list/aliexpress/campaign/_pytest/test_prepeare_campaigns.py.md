# Модуль тестирования подготовки кампаний AliExpress

## Обзор

Модуль содержит набор тестов для проверки функциональности подготовки кампаний AliExpress, включая обновление категорий, обработку кампаний по категориям и обработку кампаний в целом. Он использует `pytest` для организации тестов и `unittest.mock` для создания мок-объектов, чтобы изолировать тестируемые функции от внешних зависимостей.

## Подробней

Этот модуль предназначен для автоматизированного тестирования процесса подготовки рекламных кампаний на AliExpress. Он проверяет корректность обновления информации о категориях, обработки кампаний для каждой категории и общей обработки кампаний. Модуль использует моки для имитации работы внешних зависимостей, таких как файловая система, API AliExpress и система логирования, что позволяет проводить тесты в изолированной среде.

## Классы

В данном модуле классы отсутствуют.

## Фикстуры

### `mock_j_loads`

```python
@pytest.fixture
def mock_j_loads():
    """
    Фикстура для мокирования функции `j_loads` из модуля `src.utils.jjson`.

    Yields:
        mock: Мок-объект функции `j_loads`.
    """
    ...
```

**Назначение**: Мокирует функцию `j_loads`, используемую для загрузки JSON-данных из файла.

**Как работает фикстура**:
- Использует `patch` из модуля `unittest.mock` для замены функции `j_loads` мок-объектом.
- Предоставляет мок-объект для использования в тестах.

### `mock_j_dumps`

```python
@pytest.fixture
def mock_j_dumps():
    """
    Фикстура для мокирования функции `j_dumps` из модуля `src.utils.jjson`.

    Yields:
        mock: Мок-объект функции `j_dumps`.
    """
    ...
```

**Назначение**: Мокирует функцию `j_dumps`, используемую для сохранения JSON-данных в файл.

**Как работает фикстура**:
- Использует `patch` из модуля `unittest.mock` для замены функции `j_dumps` мок-объектом.
- Предоставляет мок-объект для использования в тестах.

### `mock_logger`

```python
@pytest.fixture
def mock_logger():
    """
    Фикстура для мокирования объекта `logger` из модуля `src.logger`.

    Yields:
        mock: Мок-объект объекта `logger`.
    """
    ...
```

**Назначение**: Мокирует объект `logger`, используемый для логирования информации.

**Как работает фикстура**:
- Использует `patch` из модуля `unittest.mock` для замены объекта `logger` мок-объектом.
- Предоставляет мок-объект для использования в тестах.

### `mock_get_directory_names`

```python
@pytest.fixture
def mock_get_directory_names():
    """
    Фикстура для мокирования функции `get_directory_names` из модуля `src.utils`.

    Yields:
        mock: Мок-объект функции `get_directory_names`.
    """
    ...
```

**Назначение**: Мокирует функцию `get_directory_names`, используемую для получения списка имен подкаталогов.

**Как работает фикстура**:
- Использует `patch` из модуля `unittest.mock` для замены функции `get_directory_names` мок-объектом.
- Предоставляет мок-объект для использования в тестах.

### `mock_ali_promo_campaign`

```python
@pytest.fixture
def mock_ali_promo_campaign():
    """
    Фикстура для мокирования класса `AliPromoCampaign` из модуля `src.suppliers.suppliers_list.aliexpress.campaign`.

    Yields:
        mock: Мок-объект класса `AliPromoCampaign`.
    """
    ...
```

**Назначение**: Мокирует класс `AliPromoCampaign`, представляющий кампанию AliExpress.

**Как работает фикстура**:
- Использует `patch` из модуля `unittest.mock` для замены класса `AliPromoCampaign` мок-объектом.
- Предоставляет мок-объект для использования в тестах.

## Функции

### `test_update_category_success`

```python
def test_update_category_success(mock_j_loads, mock_j_dumps, mock_logger):
    """
    Тест успешного обновления категории.

    Args:
        mock_j_loads: Мок-объект функции `j_loads`.
        mock_j_dumps: Мок-объект функции `j_dumps`.
        mock_logger: Мок-объект объекта `logger`.
    """
    ...
```

**Назначение**: Проверяет успешное обновление категории с использованием мокированных функций `j_loads`, `j_dumps` и `logger`.

**Параметры**:
- `mock_j_loads`: Мок-объект функции `j_loads`.
- `mock_j_dumps`: Мок-объект функции `j_dumps`.
- `mock_logger`: Мок-объект объекта `logger`.

**Как работает функция**:
- Определяет путь к мок-файлу JSON и создает мок-объект категории.
- Устанавливает возвращаемое значение для `mock_j_loads` в виде словаря с категорией.
- Вызывает функцию `update_category` с мокированными параметрами.
- Проверяет, что функция вернула `True`.
- Проверяет, что функция `mock_j_dumps` была вызвана с ожидаемыми аргументами.
- Проверяет, что функция `mock_logger.error` не была вызвана.

### `test_update_category_failure`

```python
def test_update_category_failure(mock_j_loads, mock_j_dumps, mock_logger):
    """
    Тест неудачного обновления категории.

    Args:
        mock_j_loads: Мок-объект функции `j_loads`.
        mock_j_dumps: Мок-объект функции `j_dumps`.
        mock_logger: Мок-объект объекта `logger`.
    """
    ...
```

**Назначение**: Проверяет неудачное обновление категории при возникновении исключения в функции `j_loads`.

**Параметры**:
- `mock_j_loads`: Мок-объект функции `j_loads`.
- `mock_j_dumps`: Мок-объект функции `j_dumps`.
- `mock_logger`: Мок-объект объекта `logger`.

**Как работает функция**:
- Определяет путь к мок-файлу JSON и создает мок-объект категории.
- Устанавливает побочный эффект для `mock_j_loads`, вызывающий исключение.
- Вызывает функцию `update_category` с мокированными параметрами.
- Проверяет, что функция вернула `False`.
- Проверяет, что функция `mock_j_dumps` не была вызвана.
- Проверяет, что функция `mock_logger.error` была вызвана.

### `test_process_campaign_category_success`

```python
@pytest.mark.asyncio
async def test_process_campaign_category_success(mock_ali_promo_campaign, mock_logger):
    """
    Тест успешной обработки категории кампании.

    Args:
        mock_ali_promo_campaign: Мок-объект класса `AliPromoCampaign`.
        mock_logger: Мок-объект объекта `logger`.
    """
    ...
```

**Назначение**: Проверяет успешную обработку категории кампании с использованием мокированного класса `AliPromoCampaign` и объекта `logger`.

**Параметры**:
- `mock_ali_promo_campaign`: Мок-объект класса `AliPromoCampaign`.
- `mock_logger`: Мок-объект объекта `logger`.

**Как работает функция**:
- Определяет мокированные имя кампании, имя категории, язык и валюту.
- Устанавливает возвращаемое значение для `mock_ali_promo_campaign.return_value` как экземпляр `MagicMock`.
- Устанавливает функцию `process_affiliate_products` мок-объекта `mock_ali_promo` как `MagicMock`.
- Вызывает асинхронную функцию `process_campaign_category` с мокированными параметрами.
- Проверяет, что функция вернула не `None`.
- Проверяет, что функция `mock_logger.error` не была вызвана.

### `test_process_campaign_category_failure`

```python
@pytest.mark.asyncio
async def test_process_campaign_category_failure(mock_ali_promo_campaign, mock_logger):
    """
    Тест неудачной обработки категории кампании.

    Args:
        mock_ali_promo_campaign: Мок-объект класса `AliPromoCampaign`.
        mock_logger: Мок-объект объекта `logger`.
    """
    ...
```

**Назначение**: Проверяет неудачную обработку категории кампании при возникновении исключения в методе `process_affiliate_products`.

**Параметры**:
- `mock_ali_promo_campaign`: Мок-объект класса `AliPromoCampaign`.
- `mock_logger`: Мок-объект объекта `logger`.

**Как работает функция**:
- Определяет мокированные имя кампании, имя категории, язык и валюту.
- Устанавливает побочный эффект для `mock_ali_promo_campaign.return_value.process_affiliate_products`, вызывающий исключение.
- Вызывает асинхронную функцию `process_campaign_category` с мокированными параметрами.
- Проверяет, что функция вернула `None`.
- Проверяет, что функция `mock_logger.error` была вызвана.

### `test_process_campaign`

```python
def test_process_campaign(mock_get_directory_names, mock_logger):
    """
    Тест обработки кампании.

    Args:
        mock_get_directory_names: Мок-объект функции `get_directory_names`.
        mock_logger: Мок-объект объекта `logger`.
    """
    ...
```

**Назначение**: Проверяет обработку кампании с использованием мокированной функции `get_directory_names` и объекта `logger`.

**Параметры**:
- `mock_get_directory_names`: Мок-объект функции `get_directory_names`.
- `mock_logger`: Мок-объект объекта `logger`.

**Как работает функция**:
- Определяет мокированные имя кампании, список категорий, язык, валюту и флаг `force`.
- Устанавливает возвращаемое значение для `mock_get_directory_names` как список категорий.
- Вызывает функцию `process_campaign` с мокированными параметрами.
- Проверяет, что длина возвращаемого списка результатов равна 2.
- Проверяет, что имя каждой категории в результатах находится в списке мокированных категорий.
- Проверяет, что результат для каждой категории не `None`.
- Проверяет, что функция `mock_logger.warning` не была вызвана.

### `test_main`

```python
@pytest.mark.asyncio
async def test_main(mock_get_directory_names):
    """
    Тест функции `main`.

    Args:
        mock_get_directory_names: Мок-объект функции `get_directory_names`.
    """
    ...
```

**Назначение**: Проверяет функцию `main` с использованием мокированной функции `get_directory_names`.

**Параметры**:
- `mock_get_directory_names`: Мок-объект функции `get_directory_names`.

**Как работает функция**:
- Определяет мокированные имя кампании, список категорий, язык, валюту и флаг `force`.
- Устанавливает возвращаемое значение для `mock_get_directory_names` как список категорий.
- Вызывает асинхронную функцию `main` с мокированными параметрами.
- Проверяет, что функция `mock_get_directory_names` была вызвана один раз.
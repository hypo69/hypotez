### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код содержит набор тестов pytest для проверки функциональности подготовки кампаний AliExpress, включая обновление категорий, обработку категорий кампаний, обработку кампаний в целом и запуск основной функции. Используются моки для изоляции тестируемых компонентов и проверки их взаимодействия.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей и функций**:
   - Импортируются модули `pytest`, `asyncio`, `Path`, `patch`, `MagicMock`, `SimpleNamespace`.
   - Импортируются функции из модуля `prepare_campaigns`: `update_category`, `process_campaign_category`, `process_campaign`, `main`.

2. **Определение фикстур pytest**:
   - `mock_j_loads`: Мокирует функцию `j_loads` из модуля `src.utils.jjson`.
   - `mock_j_dumps`: Мокирует функцию `j_dumps` из модуля `src.utils.jjson`.
   - `mock_logger`: Мокирует модуль `logger` из модуля `src.logger.logger`.
   - `mock_get_directory_names`: Мокирует функцию `get_directory_names` из модуля `src.utils`.
   - `mock_ali_promo_campaign`: Мокирует класс `AliPromoCampaign` из модуля `src.suppliers.suppliers_list.aliexpress.campaign`.

3. **Тест функции `update_category`**:
   - `test_update_category_success`: Проверяет успешное обновление категории.
     - Мокирует путь к JSON-файлу и объект категории.
     - Устанавливает возвращаемое значение для `mock_j_loads` как пустой словарь.
     - Вызывает функцию `update_category`.
     - Проверяет, что функция возвращает `True`, `mock_j_dumps` вызывается с ожидаемыми аргументами, и `mock_logger.error` не вызывается.
   - `test_update_category_failure`: Проверяет неудачное обновление категории.
     - Мокирует путь к JSON-файлу и объект категории.
     - Устанавливает вызов исключения для `mock_j_loads`.
     - Вызывает функцию `update_category`.
     - Проверяет, что функция возвращает `False`, `mock_j_dumps` не вызывается, и `mock_logger.error` вызывается один раз.

4. **Тест асинхронной функции `process_campaign_category`**:
   - `test_process_campaign_category_success`: Проверяет успешную обработку категории кампании.
     - Мокирует имя кампании, имя категории, язык и валюту.
     - Устанавливает возвращаемое значение для `mock_ali_promo_campaign.return_value.process_affiliate_products` как `MagicMock`.
     - Вызывает функцию `process_campaign_category`.
     - Проверяет, что функция возвращает не `None`, и `mock_logger.error` не вызывается.
   - `test_process_campaign_category_failure`: Проверяет неудачную обработку категории кампании.
     - Мокирует имя кампании, имя категории, язык и валюту.
     - Устанавливает вызов исключения для `mock_ali_promo_campaign.return_value.process_affiliate_products`.
     - Вызывает функцию `process_campaign_category`.
     - Проверяет, что функция возвращает `None`, и `mock_logger.error` вызывается один раз.

5. **Тест функции `process_campaign`**:
   - Мокирует имя кампании, список категорий, язык, валюту и флаг `force`.
   - Устанавливает возвращаемое значение для `mock_get_directory_names` как список категорий.
   - Вызывает функцию `process_campaign`.
   - Проверяет, что длина возвращаемого списка равна 2, каждая категория присутствует в списке мокированных категорий, результат не `None`, и `mock_logger.warning` не вызывается.

6. **Тест асинхронной функции `main`**:
   - Мокирует имя кампании, список категорий, язык, валюту и флаг `force`.
   - Устанавливает возвращаемое значение для `mock_get_directory_names` как список категорий.
   - Вызывает функцию `main`.
   - Проверяет, что функция `mock_get_directory_names` вызывается один раз.

Пример использования
-------------------------

```python
import pytest
from unittest.mock import patch, MagicMock
from types import SimpleNamespace
from pathlib import Path
from src.suppliers.suppliers_list.aliexpress.campaign.prepare_campaigns import (
    update_category,
    process_campaign_category,
    process_campaign,
    main,
)

@pytest.fixture
def mock_j_loads():
    with patch("src.utils.jjson.j_loads") as mock:
        yield mock

@pytest.fixture
def mock_j_dumps():
    with patch("src.utils.jjson.j_dumps") as mock:
        yield mock

@pytest.fixture
def mock_logger():
    with patch("src.logger.logger") as mock:
        yield mock

@pytest.fixture
def mock_get_directory_names():
    with patch("src.utils.get_directory_names") as mock:
        yield mock

@pytest.fixture
def mock_ali_promo_campaign():
    with patch("src.suppliers.suppliers_list.aliexpress.campaign.AliPromoCampaign") as mock:
        yield mock

# Пример теста для update_category
def test_update_category_success(mock_j_loads, mock_j_dumps, mock_logger):
    mock_json_path = Path("mock/path/to/category.json")
    mock_category = SimpleNamespace(name="test_category")

    mock_j_loads.return_value = {"category": {}}
    
    result = update_category(mock_json_path, mock_category)
    
    assert result is True
    mock_j_dumps.assert_called_once_with({"category": {"name": "test_category"}}, mock_json_path)
    mock_logger.error.assert_not_called()
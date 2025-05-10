# Модуль для обработки аргументов API AliExpress
## Обзор

Модуль `arguments.py` содержит функции для обработки и валидации аргументов, используемых в API AliExpress. Он предоставляет инструменты для преобразования входных данных в нужный формат, а также для проверки их корректности.

## Подробней

Этот модуль предназначен для облегчения работы с аргументами API, такими как идентификаторы товаров. Он включает функции для преобразования списков в строки и извлечения идентификаторов товаров из различных форматов входных данных.

## Функции

### `get_list_as_string`

**Назначение**: Преобразует переданное значение в строку, если это возможно.

**Параметры**:
- `value` (Any): Значение для преобразования.

**Возвращает**:
- `str | None`: Значение в виде строки, если `value` является строкой или списком. Возвращает `None`, если `value` равно `None`.

**Вызывает исключения**:
- `InvalidArgumentException`: Если `value` не является строкой, списком или `None`.

**Как работает функция**:
- Функция проверяет, является ли входное значение `None`. Если да, возвращает `None`.
- Если входное значение является строкой, функция возвращает его без изменений.
- Если входное значение является списком, функция объединяет элементы списка в строку, разделяя их запятыми.
- Если входное значение не является ни строкой, ни списком, функция вызывает исключение `InvalidArgumentException` с сообщением об ошибке.

**Примеры**:

```python
from src.suppliers.aliexpress.api.helpers.arguments import get_list_as_string
from src.suppliers.aliexpress.api.errors.exceptions import InvalidArgumentException

# Пример 1: Преобразование списка в строку
result1 = get_list_as_string(['item1', 'item2', 'item3'])
print(result1)  # Вывод: item1,item2,item3

# Пример 2: Возвращение строки без изменений
result2 = get_list_as_string('single_item')
print(result2)  # Вывод: single_item

# Пример 3: Обработка значения None
result3 = get_list_as_string(None)
print(result3)  # Вывод: None

# Пример 4: Вызов исключения при некорректном типе данных
try:
    result4 = get_list_as_string(123)
except InvalidArgumentException as ex:
    print(ex)  # Вывод: Argument should be a list or string: 123
```

### `get_product_ids`

**Назначение**: Извлекает и возвращает список идентификаторов товаров из входных значений.

**Параметры**:
- `values` (str | list): Строка с разделенными запятыми идентификаторами или список идентификаторов товаров.

**Возвращает**:
- `list`: Список идентификаторов товаров.

**Вызывает исключения**:
- `InvalidArgumentException`: Если `values` не является строкой или списком.

**Как работает функция**:
- Функция проверяет, является ли входное значение строкой или списком. Если нет, вызывает исключение `InvalidArgumentException`.
- Если входное значение является строкой, она разделяется на список идентификаторов, используя запятую в качестве разделителя.
- Затем функция итерируется по списку значений и для каждого значения вызывает функцию `get_product_id` для извлечения идентификатора товара.
- Собранные идентификаторы товаров добавляются в список `product_ids`, который затем возвращается.

**Примеры**:

```python
from src.suppliers.aliexpress.api.helpers.arguments import get_product_ids
from src.suppliers.aliexpress.api.tools.get_product_id import get_product_id
from unittest.mock import patch
from src.suppliers.aliexpress.api.errors.exceptions import InvalidArgumentException


# Пример 1: Извлечение идентификаторов из строки
@patch('src.suppliers.aliexpress.api.helpers.arguments.get_product_id')
def test_get_product_ids_from_string(mock_get_product_id):
    mock_get_product_id.side_effect = lambda x: f'ID_{x}'
    result = get_product_ids('123,456,789')
    print(result)  # Вывод: ['ID_123', 'ID_456', 'ID_789']

# Пример 2: Извлечение идентификаторов из списка
@patch('src.suppliers.aliexpress.api.helpers.arguments.get_product_id')
def test_get_product_ids_from_list(mock_get_product_id):
    mock_get_product_id.side_effect = lambda x: f'ID_{x}'
    result = get_product_ids(['123', '456', '789'])
    print(result)  # Вывод: ['ID_123', 'ID_456', 'ID_789']

# Пример 3: Вызов исключения при некорректном типе данных
def test_get_product_ids_invalid_argument():
    try:
        result = get_product_ids(123)
    except InvalidArgumentException as ex:
        print(ex)  # Вывод: Argument product_ids should be a list or string
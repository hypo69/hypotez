# Модуль для экспериментов со сценариями

## Обзор

Модуль `test_scenario.py` предназначен для тестирования и экспериментов со сценариями, связанными с различными поставщиками (suppliers). Он включает в себя инициализацию поставщика и запуск сценариев для этого поставщика.

## Подробнее

Этот модуль позволяет быстро переключаться между разными поставщиками, такими как `'aliexpress'`, `'amazon'`, `'kualastyle'` и `'ebay'`, чтобы тестировать сценарии для каждого из них. Он использует классы `Scenario` и `Supplier` из других модулей проекта `hypotez`.

## Классы

### `Supplier`

**Описание**: Класс для представления поставщика.

**Атрибуты**:
- `supplier_prefix` (str): Префикс поставщика (например, 'aliexpress').

**Методы**:
- Нет явных методов, так как это представление класса.

### `Scenario`

**Описание**: Класс для управления сценариями.

**Атрибуты**:
- `s` (Supplier): Объект класса `Supplier`, представляющий поставщика.

**Методы**:
- `run_scenarios()`: Запускает сценарии для данного поставщика.

## Функции

### `start_supplier`

```python
def start_supplier(supplier_prefix: str) -> Supplier:
    """
    Создает и инициализирует объект поставщика (`Supplier`).

    Args:
        supplier_prefix (str): Префикс поставщика (например, 'aliexpress').

    Returns:
        Supplier: Объект класса `Supplier`, инициализированный с указанным префиксом.

    Example:
        >>> supplier = start_supplier('aliexpress')
        >>> print(supplier.supplier_prefix)
        aliexpress
    """
    params: dict = {
        'supplier_prefix': supplier_prefix
    }

    return Supplier(**params)
```

**Назначение**: Создает экземпляр класса `Supplier` с заданным префиксом.

**Параметры**:
- `supplier_prefix` (str): Префикс поставщика.

**Возвращает**:
- `Supplier`: Объект класса `Supplier`.

**Как работает функция**:
- Функция принимает префикс поставщика в качестве аргумента.
- Создает словарь `params`, содержащий префикс поставщика.
- Возвращает экземпляр класса `Supplier`, инициализированный с использованием переданных параметров.

**Примеры**:

```python
supplier = start_supplier('aliexpress')
print(supplier.supplier_prefix)
# Вывод: aliexpress
```

## Переменные модуля

- `supplier_prefix` (str): Префикс поставщика, который можно менять для тестирования разных поставщиков.
- `s` (Supplier): Экземпляр класса `Supplier`, созданный на основе `supplier_prefix`.
- `scenario` (Scenario): Экземпляр класса `Scenario`, использующий экземпляр класса `Supplier` `s`.

## Примеры

```python
from src.scenario import Scenario
from src.suppliers import Supplier

def start_supplier(supplier_prefix: str) -> Supplier:
    params: dict = {
        'supplier_prefix': supplier_prefix
    }

    return Supplier(**params)

supplier_prefix = 'aliexpress'
s = start_supplier(supplier_prefix)
scenario = Scenario(s)
scenario.run_scenarios()
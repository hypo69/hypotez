# Module `src.suppliers.supplier`

## Overview

This module describes the base class for suppliers, `Supplier`. It is a key component of the system, providing abstraction and unification of interaction with various suppliers. The module includes functionality for loading related supplier modules and managing scenarios.

The `Supplier` class is designed for:
 - Running data collection scenarios.
 - Managing page element locators.
 - Interacting with the web driver.

[Module Documentation](https://github.com/hypo69/hypotez/blob/master/docs/ru/src/suppliers/supplier.py.md)

[Locator Documentation](https://github.com/hypo69/hypotez/blob/master/docs/ru/src/webdriver/locator.ru.md)

Next: Class [Graber](https://github.com/hypo69/hypotez/blob/master/docs/ru/src/suppliers/graber.py.md)

Flowchart:

```
                   supplier_prefix
                         |
web <-> webdriver <-> SUPPLIER -> product
                         ^
                         |
                      scenario
```

## Classes

### `Supplier`

**Description**: Класс `Supplier`. Выполняет сценарии для различных поставщиков.

**Attributes**:
    - `supplier_id` (Optional[int]): Идентификатор поставщика.
    - `supplier_prefix` (str): Префикс поставщика.
    - `locale` (str): Код локали в формате ISO 639-1.
    - `price_rule` (Optional[str]): Правило расчета цен.
    - `related_modules` (Optional[ModuleType]): Функции, относящиеся к каждому поставщику.
    - `scenario_files` (List[str]): Список файлов сценариев для выполнения.
    - `current_scenario` (Dict[str, Any]): Текущий исполняемый сценарий.
    - `locators` (Dict[str, Any]): Локаторы для элементов страницы.
    - `driver` (Optional['Driver']): Веб-драйвер.

**Working principle**:

1.  Инициализирует объект `Supplier` с заданными параметрами.
2.  Загружает связанные модули и конфигурации для конкретного поставщика.
3.  Позволяет выполнять сценарии сбора данных, управлять локаторами и взаимодействовать с веб-драйвером для автоматизации задач.

### `Supplier.Config`

**Description**: Вспомогательный класс `Config` для конфигурации модели `Supplier`.

**Attributes**:
    - `arbitrary_types_allowed` (bool): Разрешает произвольные типы данных.

## Class Methods

### `check_supplier_prefix`

```python
def check_supplier_prefix(cls, value: str) -> str:
    """Проверка префикса поставщика на пустое значение.

    Args:
        value (str): Префикс поставщика.

    Returns:
        str: Префикс поставщика, если он не пустой.

    Raises:
        ValueError: Если префикс поставщика пустой.
    """
    ...
```

**Purpose**: Проверяет, что префикс поставщика не является пустым. Если префикс пустой, вызывается исключение `ValueError`.

**Parameters**:
    - `value` (str): Префикс поставщика для проверки.

**Returns**:
    - `str`: Возвращает префикс поставщика, если проверка пройдена.

**How the function works**:

1.  Проверяет, является ли переданное значение пустым.
2.  Если значение пустое, выбрасывается исключение `ValueError` с сообщением об ошибке.
3.  Если значение не пустое, функция возвращает его.

**Examples**:

```python
Supplier.check_supplier_prefix("prefix")  # Returns "prefix"
```

### `__init__`

```python
def __init__(self, **data):
    """Инициализация поставщика, загрузка конфигурации.

    Args:
        **data: Произвольные аргументы для инициализации поставщика.

    Raises:
        DefaultSettingsException: Если не удалось запустить поставщика.
    """
    ...
```

**Purpose**: Инициализирует экземпляр класса `Supplier`, загружает конфигурацию и проверяет основные параметры.

**Parameters**:
    - `**data`: Произвольные аргументы для инициализации поставщика.

**Raises**:
    - `DefaultSettingsException`: Если при загрузке параметров поставщика возникают ошибки.

**How the function works**:

1.  Вызывает конструктор базового класса `BaseModel` для инициализации атрибутов модели данными, переданными в `**data`.
2.  Вызывает метод `_payload()` для загрузки параметров поставщика.
3.  Если метод `_payload()` возвращает `False`, выбрасывается исключение `DefaultSettingsException` с сообщением об ошибке.

**Examples**:

```python
supplier = Supplier(supplier_prefix="test_supplier", locale="ru")
```

### `_payload`

```python
def _payload(self) -> bool:
    """Загрузка параметров поставщика с использованием `j_loads_ns`.

    Returns:
        bool: `True`, если загрузка успешна, иначе `False`.
    """
    ...
```

**Purpose**: Загружает параметры поставщика, используя `j_loads_ns`, и импортирует связанные модули.

**Returns**:
    - `bool`: `True`, если загрузка и импорт прошли успешно, `False` в противном случае.

**How the function works**:

1.  Логирует начало загрузки настроек для поставщика.
2.  Пытается импортировать модуль, связанный с поставщиком, используя `importlib.import_module()`.
3.  В случае успеха присваивает импортированный модуль атрибуту `related_modules` объекта `Supplier`.
4.  Если модуль не найден, логирует ошибку и возвращает `False`.
5.  В случае успеха возвращает `True`.

**Examples**:

```python
supplier = Supplier(supplier_prefix="test_supplier", locale="ru")
result = supplier._payload()
```

### `login`

```python
def login(self) -> bool:
    """Выполняет вход на сайт поставщика.

    Returns:
        bool: `True`, если вход выполнен успешно, иначе `False`.
    """
    ...
```

**Purpose**: Выполняет вход на сайт поставщика, используя функцию `login` из связанного модуля.

**Returns**:
    - `bool`: `True`, если вход выполнен успешно, `False` в противном случае.

**How the function works**:

1.  Вызывает функцию `login` из модуля `related_modules`, передавая ей текущий объект `Supplier`.
2.  Возвращает результат выполнения функции `login`.

**Examples**:

```python
supplier = Supplier(supplier_prefix="test_supplier", locale="ru")
supplier._payload()  #  Вызов _payload необходим для загрузки related_modules
result = supplier.login()
```

### `run_scenario_files`

```python
def run_scenario_files(self, scenario_files: Optional[str | List[str]] = None) -> bool:
    """Выполнение одного или нескольких файлов сценариев.

    Args:
        scenario_files (Optional[str | List[str]]): Список файлов сценариев.
            Если не указан, берется из `self.scenario_files`.

    Returns:
        bool: `True`, если все сценарии успешно выполнены, иначе `False`.
    """
    ...
```

**Purpose**: Выполняет один или несколько файлов сценариев, используя функцию `run_scenario_files`.

**Parameters**:
    - `scenario_files` (Optional[str | List[str]]): Список файлов сценариев для выполнения. Если не указан, используются файлы из атрибута `self.scenario_files`.

**Returns**:
    - `bool`: `True`, если все сценарии успешно выполнены, `False` в противном случае.

**How the function works**:

1.  Определяет, какие файлы сценариев использовать: если `scenario_files` переданы в аргументе, использует их, иначе использует `self.scenario_files`.
2.  Вызывает функцию `run_scenario_files` из модуля `src.suppliers.scenario.scenario_executor`, передавая ей текущий объект `Supplier` и список файлов сценариев.
3.  Возвращает результат выполнения функции `run_scenario_files`.

**Examples**:

```python
supplier = Supplier(supplier_prefix="test_supplier", locale="ru", scenario_files=["scenario1.json", "scenario2.json"])
result = supplier.run_scenario_files()
```

### `run_scenarios`

```python
def run_scenarios(self, scenarios: dict | List[dict]) -> bool:
    """Выполнение списка или одного сценария.

    Args:
        scenarios (dict | List[dict]): Сценарий или список сценариев для выполнения.

    Returns:
        bool: `True`, если сценарий успешно выполнен, иначе `False`.
    """
    ...
```

**Purpose**: Выполняет один или несколько сценариев, используя функцию `run_scenarios`.

**Parameters**:
    - `scenarios` (dict | List[dict]): Сценарий или список сценариев для выполнения.

**Returns**:
    - `bool`: `True`, если сценарий успешно выполнен, `False` в противном случае.

**How the function works**:

1.  Вызывает функцию `run_scenarios` из модуля `src.suppliers.scenario.scenario_executor`, передавая ей текущий объект `Supplier` и сценарии.
2.  Возвращает результат выполнения функции `run_scenarios`.

**Examples**:

```python
supplier = Supplier(supplier_prefix="test_supplier", locale="ru")
scenario = {"name": "test_scenario", "steps": []}
result = supplier.run_scenarios(scenario)
```
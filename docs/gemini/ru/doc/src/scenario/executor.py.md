# Модуль для выполнения сценариев
## Обзор

Модуль `executor.py` предназначен для выполнения сценариев, загрузки их из файлов и обработки процесса извлечения информации о продуктах и вставки их в PrestaShop.

## Подробнее

Этот модуль содержит функции для выполнения сценариев, включая загрузку из файлов и обработку данных для PrestaShop. Он использует другие модули проекта, такие как `gs`, `jjson`, `prestashop.product_async`, `db`, `logger` и `exceptions`.
Модуль предоставляет функциональность для загрузки, выполнения и обработки результатов сценариев, а также для записи журналов выполнения.

## Функции

### `dump_journal`

```python
def dump_journal(s, journal: dict) -> None:
    """
    Сохраняет данные журнала в файл JSON.

    Args:
        s (object): Объект поставщика (Supplier instance).
        journal (dict): Словарь, содержащий данные журнала.

    Returns:
        None
    """
```

**Назначение**: Функция сохраняет данные журнала выполнения сценария в файл JSON. Файл сохраняется в директории `_journal` внутри директории поставщика.

**Параметры**:
- `s`: Объект поставщика, содержащий информацию о поставщике и путях к файлам.
- `journal`: Словарь с данными журнала, которые нужно сохранить.

**Возвращает**:
- `None`

**Как работает функция**:

1.  Формирует путь к файлу журнала, используя информацию о поставщике и имени журнала.
2.  Использует функцию `j_dumps` для записи данных журнала в файл JSON.

**Примеры**:

```python
# Пример вызова функции dump_journal
# Предположим, что s - это объект Supplier, а journal - словарь с данными журнала
# s = Supplier(...)
# journal = {'name': 'test_scenario', 'start_time': '2024-01-01 10:00:00', 'end_time': '2024-01-01 10:05:00'}
# dump_journal(s, journal)
```

### `run_scenario_files`

```python
def run_scenario_files(s, scenario_files_list: List[Path] | Path) -> bool:
    """
    Выполняет список файлов сценариев.

    Args:
        s (object): Объект поставщика (Supplier instance).
        scenario_files_list (List[Path] | Path): Список путей к файлам сценариев или одиночный путь к файлу.

    Returns:
        bool: True, если все сценарии были выполнены успешно, False в противном случае.

    Raises:
        TypeError: Если scenario_files_list не является списком или объектом Path.
    """
```

**Назначение**: Функция выполняет сценарии, содержащиеся в указанных файлах. Она принимает список файлов или один файл и выполняет каждый сценарий в них.

**Параметры**:
- `s`: Объект поставщика, содержащий информацию о поставщике и путях к файлам.
- `scenario_files_list`: Список объектов `Path`, указывающих на файлы сценариев, или один объект `Path`.

**Возвращает**:
- `bool`: `True`, если все сценарии успешно выполнены, `False` в противном случае.

**Вызывает исключения**:
- `TypeError`: Если `scenario_files_list` не является списком или объектом `Path`.

**Как работает функция**:

1.  Проверяет тип аргумента `scenario_files_list`. Если это `Path`, преобразует в список с одним элементом. Если это не список и не `Path`, вызывает `TypeError`.
2.  Итерируется по списку файлов сценариев.
3.  Для каждого файла вызывает функцию `run_scenario_file`.
4.  Логирует результаты выполнения каждого сценария в `_journal` и с помощью `logger`.

**Примеры**:

```python
# Пример вызова функции run_scenario_files со списком файлов
# s = Supplier(...)
# scenario_files_list = [Path('scenario1.json'), Path('scenario2.json')]
# run_scenario_files(s, scenario_files_list)

# Пример вызова функции run_scenario_files с одним файлом
# s = Supplier(...)
# scenario_file = Path('scenario1.json')
# run_scenario_files(s, scenario_file)
```

### `run_scenario_file`

```python
def run_scenario_file(s, scenario_file: Path) -> bool:
    """
    Загружает и выполняет сценарии из файла.

    Args:
        s (object): Объект поставщика (Supplier instance).
        scenario_file (Path): Путь к файлу сценария.

    Returns:
        bool: True, если сценарий был выполнен успешно, False в противном случае.
    """
```

**Назначение**: Функция загружает сценарии из указанного файла и выполняет их.

**Параметры**:
- `s`: Объект поставщика.
- `scenario_file`: Объект `Path`, указывающий на файл сценария.

**Возвращает**:
- `bool`: `True`, если сценарий выполнен успешно, `False` в противном случае.

**Вызывает исключения**:
- `FileNotFoundError`: Если файл сценария не найден.
- `json.JSONDecodeError`: Если файл сценария содержит некорректный JSON.

**Как работает функция**:

1.  Загружает содержимое файла сценария с помощью `j_loads`.
2.  Итерируется по сценариям в файле.
3.  Для каждого сценария вызывает функцию `run_scenario`.
4.  Логирует результаты выполнения каждого сценария с помощью `logger`.

**Примеры**:

```python
# Пример вызова функции run_scenario_file
# s = Supplier(...)
# scenario_file = Path('scenario.json')
# run_scenario_file(s, scenario_file)
```

### `run_scenarios`

```python
def run_scenarios(s, scenarios: Optional[List[dict] | dict] = None, _journal=None) -> List | dict | bool:
    """
    Выполняет список сценариев (НЕ ФАЙЛОВ).

    Args:
        s (object): Объект поставщика (Supplier instance).
        scenarios (Optional[List[dict] | dict], optional): Список сценариев или один сценарий в виде словаря. По умолчанию None.
        _journal: Журнал.

    Returns:
        List | dict | bool: Результат выполнения сценариев или False в случае ошибки.

    Todo:
        Check the option when no scenarios are specified from all sides. For example, when s.current_scenario is not specified and scenarios are not specified.
    """
```

**Назначение**: Функция выполняет список сценариев, представленных в виде словарей.

**Параметры**:
- `s`: Объект поставщика.
- `scenarios`: Список словарей, представляющих сценарии, или один словарь. Если `None`, используется `s.current_scenario`.
- `_journal`: Журнал.

**Возвращает**:
- `List | dict | bool`: Результат выполнения сценариев.

**Как работает функция**:

1.  Если `scenarios` не указаны, использует `s.current_scenario`.
2.  Преобразует `scenarios` в список, если это один сценарий.
3.  Итерируется по списку сценариев и вызывает `run_scenario` для каждого.
4.  Логирует результаты выполнения каждого сценария в `_journal` и с помощью `dump_journal`.

**Примеры**:

```python
# Пример вызова функции run_scenarios со списком сценариев
# s = Supplier(...)
# scenarios = [{'name': 'scenario1', 'url': 'http://example.com/1'}, {'name': 'scenario2', 'url': 'http://example.com/2'}]
# run_scenarios(s, scenarios)

# Пример вызова функции run_scenarios с одним сценарием
# s = Supplier(...)
# scenario = {'name': 'scenario1', 'url': 'http://example.com/1'}
# run_scenarios(s, scenario)
```

### `run_scenario`

```python
def run_scenario(supplier, scenario: dict, scenario_name: str, _journal=None) -> List | dict | bool:
    """
    Выполняет полученный сценарий.

    Args:
        supplier (object): Объект поставщика (Supplier instance).
        scenario (dict): Словарь, содержащий детали сценария.
        scenario_name (str): Имя сценария.
        _journal: Журнал.

    Returns:
        List | dict | bool: Результат выполнения сценария.

    Todo:
        Check the need for the scenario_name parameter.
    """
```

**Назначение**: Функция выполняет один сценарий, получая данные о продуктах и вставляя их в PrestaShop.

**Параметры**:
- `supplier`: Объект поставщика.
- `scenario`: Словарь с деталями сценария, такими как URL.
- `scenario_name`: Имя сценария.

**Возвращает**:
- `List | dict | bool`: Результат выполнения сценария.

**Как работает функция**:

1.  Устанавливает текущий сценарий в объект поставщика.
2.  Получает URL из сценария и открывает его в браузере с помощью `driver.get_url`.
3.  Получает список продуктов в категории с помощью `s.related_modules.get_list_products_in_category(s)`.
4.  Если список продуктов пуст, логирует предупреждение и возвращает `False`.
5.  Итерируется по URL-ам продуктов в списке.
6.  Для каждого URL открывает страницу продукта в браузере.
7.  Извлекает поля продукта с помощью `s.related_modules.grab_product_page(s)` и `s.related_modules.grab_page(s)`.
8.  Если не удалось извлечь поля продукта, логирует ошибку и переходит к следующему продукту.
9.  Создает объект `Product` и вставляет данные с помощью функции `insert_grabbed_data`.

**Примеры**:

```python
# Пример вызова функции run_scenario
# s = Supplier(...)
# scenario = {'name': 'scenario1', 'url': 'http://example.com/1'}
# scenario_name = 'test_scenario'
# run_scenario(s, scenario, scenario_name)
```

### `insert_grabbed_data_to_prestashop`

```python
async def insert_grabbed_data_to_prestashop(
    f: ProductFields, coupon_code: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None
) -> bool:
    """
    Вставляет продукт в PrestaShop.

    Args:
        f (ProductFields): Экземпляр ProductFields, содержащий информацию о продукте.
        coupon_code (Optional[str], optional): Код купона (необязательно). По умолчанию None.
        start_date (Optional[str], optional): Дата начала акции (необязательно). По умолчанию None.
        end_date (Optional[str], optional): Дата окончания акции (необязательно). По умолчанию None.

    Returns:
        bool: True, если вставка прошла успешно, False в противном случае.
    """
```

**Назначение**: Асинхронная функция для вставки данных о продукте в PrestaShop.

**Параметры**:
- `f`: Объект `ProductFields`, содержащий информацию о продукте.
- `coupon_code`: Код купона для продукта (опционально).
- `start_date`: Дата начала действия купона (опционально).
- `end_date`: Дата окончания действия купона (опционально).

**Возвращает**:
- `bool`: `True`, если вставка прошла успешно, `False` в противном случае.

**Как работает функция**:

1.  Создает экземпляр класса `PrestaShop`.
2.  Вызывает метод `post_product_data` для вставки данных продукта в PrestaShop.
3.  Обрабатывает возможные исключения и логирует ошибки.

**Примеры**:

```python
# Пример вызова функции insert_grabbed_data_to_prestashop
# f = ProductFields(...)
# await insert_grabbed_data_to_prestashop(f, coupon_code='DISCOUNT10', start_date='2024-01-01', end_date='2024-01-31')
```
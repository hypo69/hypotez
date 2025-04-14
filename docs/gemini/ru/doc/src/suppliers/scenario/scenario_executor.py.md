# Модуль `scenario_executor`

## Обзор

Модуль `scenario_executor` предназначен для исполнения сценариев, связанных с поставщиками, в проекте `hypotez`. Он позволяет выполнять различные задачи, такие как сбор данных о товарах в определенной категории, с учетом заданных фильтров или производителей. Модуль предоставляет функциональность для загрузки, обработки и выполнения сценариев из файлов, а также логирование результатов выполнения.

## Подробнее

Модуль содержит функции для выполнения сценариев из файлов (`run_scenario_files`, `run_scenario_file`) и для непосредственного выполнения сценариев, представленных в виде словарей (`run_scenarios`, `run_scenario`). Он также включает функции для сохранения журналов выполнения сценариев (`dump_journal`) и вставки собранных данных в PrestaShop (`insert_grabbed_data_to_prestashop`).

## Функции

### `dump_journal`

```python
def dump_journal(s, journal: dict) -> None:
    """
    Сохраняет данные журнала в JSON-файл.

    Args:
        s (object): Экземпляр поставщика.
        journal (dict): Словарь, содержащий данные журнала.

    Returns:
        None

    """
    ...
```

**Назначение**: Сохраняет данные журнала выполнения сценария в файл JSON. Файл сохраняется в поддиректории `_journal` директории поставщика.

**Параметры**:
- `s` (object): Объект, представляющий поставщика, содержащий информацию о пути к директории поставщика.
- `journal` (dict): Словарь с данными журнала, которые необходимо сохранить.

**Как работает функция**:
- Формирует путь к файлу журнала, используя имя сценария (`journal['name']`) и путь к директории поставщика.
- Использует функцию `j_dumps` из модуля `src.utils.jjson` для записи словаря `journal` в файл JSON.

**Примеры**:
```python
# Пример использования функции dump_journal
supplier = ... # некий объект поставщика
journal_data = {'name': 'test_scenario', 'status': 'completed'}
dump_journal(supplier, journal_data)
```

### `run_scenario_files`

```python
def run_scenario_files(s, scenario_files_list: List[Path] | Path) -> bool:
    """
    Выполняет список файлов сценариев.

    Args:
        s (object): Экземпляр поставщика.
        scenario_files_list (List[Path] | Path): Список путей к файлам сценариев или путь к одному файлу.

    Returns:
        bool: True, если все сценарии выполнены успешно, False в противном случае.

    Raises:
        TypeError: Если scenario_files_list не является списком или объектом Path.
    """
    ...
```

**Назначение**: Выполняет сценарии, указанные в переданном списке файлов.

**Параметры**:
- `s` (object): Объект, представляющий поставщика.
- `scenario_files_list` (List[Path] | Path): Список объектов `Path`, указывающих на файлы сценариев, или один объект `Path`, указывающий на файл сценария.

**Возвращает**:
- `bool`: `True`, если все сценарии в файлах выполнены успешно, `False` в противном случае.

**Как работает функция**:
- Проверяет тип входного параметра `scenario_files_list`. Если это один файл (`Path`), преобразует его в список, содержащий только этот файл.
- Итерируется по списку файлов сценариев.
- Для каждого файла сценария вызывает функцию `run_scenario_file`.
- Логирует результаты выполнения каждого сценария в `_journal` и с использованием `logger`.
- Возвращает `True`, если все сценарии выполнены успешно, `False`, если хотя бы один сценарий завершился с ошибкой.

**Примеры**:

```python
from pathlib import Path

# Пример использования с одним файлом сценария
supplier = ... # некий объект поставщика
scenario_file = Path('/path/to/scenario.json')
result = run_scenario_files(supplier, scenario_file)

# Пример использования со списком файлов сценариев
scenario_files = [Path('/path/to/scenario1.json'), Path('/path/to/scenario2.json')]
result = run_scenario_files(supplier, scenario_files)
```

### `run_scenario_file`

```python
def run_scenario_file(s, scenario_file: Path) -> bool:
    """
    Загружает и выполняет сценарии из файла.

    Args:
        s (object): Экземпляр поставщика.
        scenario_file (Path): Путь к файлу сценария.

    Returns:
        bool: True, если сценарий выполнен успешно, False в противном случае.
    """
    ...
```

**Назначение**: Загружает сценарии из указанного файла и выполняет их.

**Параметры**:
- `s` (object): Объект, представляющий поставщика.
- `scenario_file` (Path): Объект `Path`, указывающий на файл, содержащий сценарии.

**Возвращает**:
- `bool`: `True`, если все сценарии в файле выполнены успешно, `False` в противном случае.

**Как работает функция**:
- Пытается загрузить сценарии из файла, используя функцию `j_loads`. Ожидается, что файл содержит JSON-структуру со списком сценариев под ключом `'scenarios'`.
- Итерируется по словарю сценариев.
- Для каждого сценария вызывает функцию `run_scenario`.
- Логирует результаты выполнения каждого сценария с использованием `logger`.
- Возвращает `True`, если все сценарии выполнены успешно, `False`, если произошла ошибка при загрузке файла или выполнении сценариев.

**Примеры**:

```python
from pathlib import Path

# Пример использования
supplier = ... # некий объект поставщика
scenario_file = Path('/path/to/scenario.json')
result = run_scenario_file(supplier, scenario_file)
```

### `run_scenarios`

```python
def run_scenarios(s, scenarios: Optional[List[dict] | dict] = None, _journal=None) -> List | dict | bool:
    """
    Выполняет список сценариев (НЕ ФАЙЛОВ).

    Args:
        s (object): Экземпляр поставщика.
        scenarios (Optional[List[dict] | dict], optional): Список сценариев или один сценарий в виде словаря. По умолчанию None.

    Returns:
        List | dict | bool: Результат выполнения сценариев или False в случае ошибки.

    Todo:
        Check the option when no scenarios are specified from all sides. For example, when s.current_scenario is not specified and scenarios are not specified.
    """
    ...
```

**Назначение**: Выполняет переданный список сценариев.

**Параметры**:
- `s` (object): Объект, представляющий поставщика.
- `scenarios` (Optional[List[dict] | dict], optional): Список словарей, представляющих сценарии, или один словарь, представляющий сценарий. Если не указан, используется `s.current_scenario`.

**Возвращает**:
- `List | dict | bool`: Список результатов выполнения сценариев, результат выполнения одного сценария или `False` в случае ошибки.

**Как работает функция**:
- Если `scenarios` не указаны, использует `s.current_scenario`.
- Преобразует входные сценарии в список, если это не список.
- Итерируется по списку сценариев и вызывает функцию `run_scenario` для каждого сценария.
- Логирует результаты выполнения каждого сценария в `_journal` и с использованием `logger`.
- Возвращает результаты выполнения сценариев.

**Примеры**:

```python
# Пример использования со списком сценариев
supplier = ... # некий объект поставщика
scenarios = [{'url': 'http://example.com/category1'}, {'url': 'http://example.com/category2'}]
results = run_scenarios(supplier, scenarios)

# Пример использования с одним сценарием
scenario = {'url': 'http://example.com/category1'}
result = run_scenarios(supplier, scenario)
```

### `run_scenario`

```python
def run_scenario(supplier, scenario: dict, scenario_name: str, _journal=None) -> List | dict | bool:
    """
    Выполняет полученный сценарий.

    Args:
        supplier (object): Экземпляр поставщика.
        scenario (dict): Словарь, содержащий детали сценария.
        scenario_name (str): Имя сценария.

    Returns:
        List | dict | bool: Результат выполнения сценария.

    Todo:
        Check the need for the scenario_name parameter.
    """
    ...
```

**Назначение**: Выполняет один сценарий, определенный в виде словаря.

**Параметры**:
- `supplier` (object): Объект, представляющий поставщика.
- `scenario` (dict): Словарь, содержащий детали сценария, такие как URL для посещения и другие параметры.
- `scenario_name` (str): Имя сценария.

**Возвращает**:
- `List | dict | bool`: Результат выполнения сценария. В данном случае, возвращает список URL товаров, собранных в категории.

**Как работает функция**:
1. Инициализирует драйвер и переходит по URL, указанному в сценарии.
2. Получает список товаров в категории, используя `s.related_modules.get_list_products_in_category(s)`.
3. Если список товаров пуст, логирует предупреждение и возвращает `False`.
4. Итерируется по списку URL товаров.
5. Для каждого URL переходит на страницу товара.
6. Собирает информацию о товаре, используя `s.related_modules.grab_product_page(s)` и `s.related_modules.grab_page(s)`.
7. Создает объект `Product` и пытается сохранить данные о товаре, используя функцию `insert_grabbed_data(f)`.
8. В случае ошибки при навигации по страницам или сборе данных, логирует ошибку и переходит к следующему товару.
9. Возвращает список URL товаров, собранных в категории.

**Примеры**:

```python
# Пример использования
supplier = ... # некий объект поставщика
scenario = {'url': 'http://example.com/category1'}
scenario_name = 'Category 1 Scenario'
result = run_scenario(supplier, scenario, scenario_name)
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
        bool: True, если вставка выполнена успешно, False в противном случае.
    """
    ...
```

**Назначение**: Вставляет данные о продукте в PrestaShop.

**Параметры**:
- `f` (ProductFields): Объект `ProductFields`, содержащий информацию о продукте для вставки.
- `coupon_code` (Optional[str], optional): Код купона для продукта. По умолчанию `None`.
- `start_date` (Optional[str], optional): Дата начала действия купона. По умолчанию `None`.
- `end_date` (Optional[str], optional): Дата окончания действия купона. По умолчанию `None`.

**Возвращает**:
- `bool`: `True`, если данные успешно вставлены в PrestaShop, `False` в противном случае.

**Как работает функция**:
- Создает экземпляр класса `PrestaShop`.
- Вызывает асинхронный метод `post_product_data` для вставки данных о продукте в PrestaShop.
- Передает информацию о продукте, включая идентификатор, название, категорию, цену и описание.
- Также передает информацию о купоне, если она предоставлена.
- В случае успеха возвращает `True`, в противном случае логирует ошибку и возвращает `False`.

**Примеры**:

```python
# Пример использования
product_fields = ...  # некий объект ProductFields
coupon_code = 'SUMMER20'
start_date = '2024-06-01'
end_date = '2024-08-31'
result = asyncio.run(insert_grabbed_data_to_prestashop(product_fields, coupon_code, start_date, end_date))
# Исполнитель сценариев поставщиков

## Обзор

Модуль `scenario_executor` предназначен для автоматического исполнения сценариев, определяющих алгоритмы сбора и обработки данных о товарах с различных поставщиков. 

## Детали

Модуль `scenario_executor` предоставляет набор функций и классов для выполнения заданных сценариев. Сценарии представляют собой набор инструкций для сбора данных о товарах, таких как:

- Сбор товаров в определенной категории
- Сбор товаров по определенному фильтру
- Сбор товаров по определенному производителю
- И т.д.

Сценарии хранятся в JSON-файлах, которые загружаются и интерпретируются `scenario_executor`. 

## Классы

### `class _journal`

**Описание**: Глобальный журнал для отслеживания выполнения сценариев.

**Атрибуты**:

- `scenario_files` (dict): Словарь, хранящий информацию о файлах сценариев, используемых в процессе выполнения.

**Методы**:

- `dump_journal(s, journal: dict) -> None`: Сохраняет данные журнала в JSON-файл.

### `class Product`

**Описание**: Класс, представляющий товар.

**Атрибуты**:

- `supplier_prefix` (str): Префикс поставщика.
- `presta_fields_dict` (dict): Словарь с данными о товаре для PrestaShop.

**Методы**:

- `insert_grabbed_data_to_prestashop(f: ProductFields, coupon_code: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> bool`: Вставляет данные о товаре в PrestaShop.

## Функции

### `dump_journal(s, journal: dict) -> None`

**Описание**: Функция сохраняет данные журнала в JSON-файл. 

**Параметры**:

- `s` (object): Экземпляр поставщика.
- `journal` (dict): Словарь, содержащий данные журнала.

**Возвращает**:

- `None`: Не возвращает значение.

**Как работает функция**:

- Функция формирует путь к файлу журнала, используя путь к каталогу поставщика и текущую метку времени.
- Затем функция сериализует данные журнала в JSON-формат и записывает их в файл.

**Примеры**:

```python
>>> from src.suppliers.scenario.scenario_executor import dump_journal
>>> s = Supplier() # предположим, что s - это экземпляр класса Supplier
>>> journal = {'name': 'test_journal', 'data': 'some data'}
>>> dump_journal(s, journal)
# Сохраняет данные журнала в файл 'journal.json'
```

### `run_scenario_files(s, scenario_files_list: List[Path] | Path) -> bool`

**Описание**: Функция запускает сценарии из списка файлов.

**Параметры**:

- `s` (object): Экземпляр поставщика.
- `scenario_files_list` (List[Path] | Path): Список путей к файлам сценариев или путь к единственному файлу.

**Возвращает**:

- `bool`: `True`, если все сценарии были выполнены успешно, `False` в противном случае.

**Исключения**:

- `TypeError`: Если `scenario_files_list` не является списком или объектом `Path`.

**Как работает функция**:

- Если `scenario_files_list` - это `Path`, то функция преобразует его в список, содержащий только этот `Path`.
- Если `scenario_files_list` - это не список, то функция вызывает `TypeError`.
- Функция перебирает все файлы сценариев в списке и запускает `run_scenario_file` для каждого из них.
- Если `run_scenario_file` возвращает `False`, то функция записывает информацию об ошибке в журнал и возвращает `False`.
- Если все сценарии были выполнены успешно, то функция возвращает `True`.

**Примеры**:

```python
>>> from src.suppliers.scenario.scenario_executor import run_scenario_files
>>> s = Supplier() # предположим, что s - это экземпляр класса Supplier
>>> scenario_files = [Path('./scenario_1.json'), Path('./scenario_2.json')]
>>> run_scenario_files(s, scenario_files)
# Выполняет сценарии из файлов 'scenario_1.json' и 'scenario_2.json'
```

### `run_scenario_file(s, scenario_file: Path) -> bool`

**Описание**: Функция загружает и запускает сценарии из файла.

**Параметры**:

- `s` (object): Экземпляр поставщика.
- `scenario_file` (Path): Путь к файлу сценария.

**Возвращает**:

- `bool`: `True`, если сценарий был выполнен успешно, `False` в противном случае.

**Как работает функция**:

- Функция загружает JSON-данные из файла сценария.
- Затем функция перебирает все сценарии в файле и запускает `run_scenario` для каждого из них.
- Если `run_scenario` возвращает `False`, то функция записывает информацию об ошибке в журнал и возвращает `False`.
- Если все сценарии были выполнены успешно, то функция возвращает `True`.

**Примеры**:

```python
>>> from src.suppliers.scenario.scenario_executor import run_scenario_file
>>> s = Supplier() # предположим, что s - это экземпляр класса Supplier
>>> scenario_file = Path('./scenario.json')
>>> run_scenario_file(s, scenario_file)
# Выполняет сценарий из файла 'scenario.json'
```

### `run_scenarios(s, scenarios: Optional[List[dict] | dict] = None, _journal=None) -> List | dict | bool`

**Описание**: Функция запускает список сценариев.

**Параметры**:

- `s` (object): Экземпляр поставщика.
- `scenarios` (Optional[List[dict] | dict], optional): Принимает список сценариев или один сценарий в виде словаря. По умолчанию None.

**Возвращает**:

- `List | dict | bool`: Результат выполнения сценариев или `False` в случае ошибки.

**Как работает функция**:

- Если `scenarios` не задано, то функция использует `s.current_scenario`.
- Если `scenarios` - это словарь, то функция преобразует его в список, содержащий только этот словарь.
- Функция перебирает все сценарии в списке и запускает `run_scenario` для каждого из них.
- Функция возвращает результат выполнения сценариев.

**Примеры**:

```python
>>> from src.suppliers.scenario.scenario_executor import run_scenarios
>>> s = Supplier() # предположим, что s - это экземпляр класса Supplier
>>> scenarios = [{'name': 'scenario_1', 'url': 'https://example.com/1'}, {'name': 'scenario_2', 'url': 'https://example.com/2'}]
>>> run_scenarios(s, scenarios)
# Выполняет сценарии из списка 'scenarios'
```

### `run_scenario(supplier, scenario: dict, scenario_name: str, _journal=None) -> List | dict | bool`

**Описание**: Функция запускает полученный сценарий.

**Параметры**:

- `supplier` (object): Экземпляр поставщика.
- `scenario` (dict): Словарь, содержащий детали сценария.
- `scenario_name` (str): Название сценария.

**Возвращает**:

- `List | dict | bool`: Результат выполнения сценария.

**Как работает функция**:

- Функция записывает в журнал информацию о начале выполнения сценария.
- Функция открывает страницу, указанную в сценарии.
- Функция собирает список товаров в категории, используя `s.related_modules.get_list_products_in_category(s)`.
- Если список товаров пуст, то функция записывает предупреждение в журнал и возвращает `False`.
- Функция перебирает все ссылки на товары в списке и запускает следующие действия для каждой ссылки:
    - Открывает страницу товара.
    - Собирает информацию о товаре с использованием `s.related_modules.grab_product_page(s)`.
    - Запускает асинхронную функцию `s.related_modules.grab_page(s)` для сбора дополнительных данных.
    - Сохраняет данные о товаре в базе данных.
- Функция возвращает список товаров, собранных в процессе выполнения сценария.

**Примеры**:

```python
>>> from src.suppliers.scenario.scenario_executor import run_scenario
>>> s = Supplier() # предположим, что s - это экземпляр класса Supplier
>>> scenario = {'name': 'scenario_1', 'url': 'https://example.com/1'}
>>> run_scenario(s, scenario, 'scenario_1')
# Выполняет сценарий 'scenario_1'
```

### `insert_grabbed_data_to_prestashop(f: ProductFields, coupon_code: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> bool`

**Описание**: Функция вставляет данные о товаре в PrestaShop.

**Параметры**:

- `f` (ProductFields): Экземпляр `ProductFields`, содержащий информацию о товаре.
- `coupon_code` (Optional[str], optional): Необязательный купон. По умолчанию None.
- `start_date` (Optional[str], optional): Необязательная дата начала акции. По умолчанию None.
- `end_date` (Optional[str], optional): Необязательная дата окончания акции. По умолчанию None.

**Возвращает**:

- `bool`: `True`, если вставка прошла успешно, `False` в противном случае.

**Как работает функция**:

- Функция создает экземпляр класса `PrestaShop`.
- Функция вызывает метод `post_product_data` для вставки данных о товаре в PrestaShop.
- Если вставка прошла успешно, то функция возвращает `True`, иначе - `False`.

**Примеры**:

```python
>>> from src.suppliers.scenario.scenario_executor import insert_grabbed_data_to_prestashop
>>> f = ProductFields() # предположим, что f - это экземпляр класса ProductFields
>>> insert_grabbed_data_to_prestashop(f, coupon_code='SUMMER10', start_date='2023-06-01', end_date='2023-09-30')
# Вставляет данные о товаре в PrestaShop с купоном 'SUMMER10' и датой начала акции '2023-06-01'
```
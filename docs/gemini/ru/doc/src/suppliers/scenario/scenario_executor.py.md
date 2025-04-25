# Исполнитель сценариев поставщиков

## Обзор

Модуль `scenario_executor.py` реализует функциональность для запуска и выполнения различных сценариев, используемых для сбора и обработки данных о товарах от поставщиков. 

## Подробности

Модуль предоставляет набор функций для выполнения сценариев, которые могут включать в себя:

- Сбор товаров в определенной категории
- Сбор товаров по определенному фильтру
- Сбор товаров по определенному производителю
- ...
- и т.д.

## Функции

### `dump_journal`

**Назначение**: Сохраняет данные журнала в JSON-файл.

**Параметры**:

- `s` (object): Экземпляр класса `Supplier`.
- `journal` (dict): Словарь, содержащий данные журнала.

**Возвращает**:

- `None`

**Пример**:

```python
from pathlib import Path

s = Supplier()
journal = {'scenario_files': ''}
dump_journal(s, journal)
```

### `run_scenario_files`

**Назначение**: Выполняет список сценариев, указанных в файлах.

**Параметры**:

- `s` (object): Экземпляр класса `Supplier`.
- `scenario_files_list` (List[Path] | Path): Список путей к файлам сценариев или один путь к файлу.

**Возвращает**:

- `bool`: `True`, если все сценарии были успешно выполнены, `False` в противном случае.

**Вызывает исключения**:

- `TypeError`: Если `scenario_files_list` не является списком или объектом `Path`.

**Пример**:

```python
from pathlib import Path

s = Supplier()
scenario_files_list = [Path('scenario1.json'), Path('scenario2.json')]
run_scenario_files(s, scenario_files_list)
```

### `run_scenario_file`

**Назначение**: Загружает и выполняет сценарии из файла.

**Параметры**:

- `s` (object): Экземпляр класса `Supplier`.
- `scenario_file` (Path): Путь к файлу сценария.

**Возвращает**:

- `bool`: `True`, если сценарий был успешно выполнен, `False` в противном случае.

**Пример**:

```python
from pathlib import Path

s = Supplier()
scenario_file = Path('scenario.json')
run_scenario_file(s, scenario_file)
```

### `run_scenarios`

**Назначение**: Выполняет список сценариев (НЕ ФАЙЛОВ).

**Параметры**:

- `s` (object): Экземпляр класса `Supplier`.
- `scenarios` (Optional[List[dict] | dict], optional): Принимает список сценариев или один сценарий в виде словаря. По умолчанию `None`.

**Возвращает**:

- `List | dict | bool`: Результат выполнения сценариев или `False` в случае ошибки.

**Пример**:

```python
from pathlib import Path

s = Supplier()
scenarios = [{'url': 'https://example.com'}, {'url': 'https://example2.com'}]
run_scenarios(s, scenarios)
```

### `run_scenario`

**Назначение**: Выполняет полученный сценарий.

**Параметры**:

- `supplier` (object): Экземпляр класса `Supplier`.
- `scenario` (dict): Словарь, содержащий детали сценария.
- `scenario_name` (str): Название сценария.

**Возвращает**:

- `List | dict | bool`: Результат выполнения сценария.

**Пример**:

```python
from pathlib import Path

s = Supplier()
scenario = {'url': 'https://example.com'}
scenario_name = 'test_scenario'
run_scenario(s, scenario, scenario_name)
```

### `insert_grabbed_data_to_prestashop`

**Назначение**: Вставляет полученный продукт в PrestaShop.

**Параметры**:

- `f` (ProductFields): Экземпляр `ProductFields`, содержащий информацию о продукте.
- `coupon_code` (Optional[str], optional): Необязательный промокод. По умолчанию `None`.
- `start_date` (Optional[str], optional): Необязательная дата начала акции. По умолчанию `None`.
- `end_date` (Optional[str], optional): Необязательная дата окончания акции. По умолчанию `None`.

**Возвращает**:

- `bool`: `True`, если вставка прошла успешно, `False` в противном случае.

**Пример**:

```python
from pathlib import Path

f = ProductFields()
insert_grabbed_data_to_prestashop(f)
```

## Переменные

### `_journal`

**Описание**: Глобальный журнал для отслеживания выполнения сценариев.

**Тип**: `dict`

**Пример**:

```python
_journal = {'scenario_files': ''}
```

## Принцип работы

Модуль `scenario_executor.py` организован следующим образом:

1. `run_scenario_files`: Вызывает функцию `run_scenario_file` для каждого файла сценария в списке.
2. `run_scenario_file`: Загружает сценарии из файла и вызывает функцию `run_scenario` для каждого сценария.
3. `run_scenario`: Выполняет сценарий, загружая URL, собирая список товаров, обрабатывая каждый товар и вставляя его в PrestaShop.
4. `insert_grabbed_data_to_prestashop`: Вставляет полученный товар в PrestaShop, включая информацию о товаре, промокоде, дате начала и дате окончания акции.

## Примеры

### Выполнение сценария из файла

```python
from pathlib import Path

s = Supplier()
scenario_file = Path('scenario.json')
run_scenario_file(s, scenario_file)
```

### Выполнение списка сценариев

```python
from pathlib import Path

s = Supplier()
scenarios = [{'url': 'https://example.com'}, {'url': 'https://example2.com'}]
run_scenarios(s, scenarios)
```

### Вставка товара в PrestaShop

```python
from pathlib import Path

f = ProductFields()
insert_grabbed_data_to_prestashop(f)
```
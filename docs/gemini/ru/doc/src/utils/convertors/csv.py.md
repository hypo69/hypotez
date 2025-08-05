# Модуль для работы с CSV данными

## Обзор

Модуль `src.utils.convertors.csv` предоставляет набор функций для работы с CSV-файлами. Основные функции включают в себя конвертацию данных из CSV в словарь или объект SimpleNamespace, а также конвертацию данных из CSV в JSON и сохранение в JSON-файл.

## Функции

### `csv2dict`

**Назначение**: Преобразует данные из CSV-файла в словарь.

**Параметры**:
- `csv_file` (str | Path): Путь к CSV-файлу для чтения.

**Возвращает**:
- `dict | None`: Словарь, содержащий данные из CSV, преобразованные в JSON-формат, или `None`, если преобразование не удалось.

**Вызывает исключения**:
- `Exception`: Если не удается прочитать CSV-файл.

**Пример**:
```python
>>> csv2dict('data.csv')
{'column1': ['value1', 'value2', 'value3'], 'column2': [1, 2, 3]}
```

### `csv2ns`

**Назначение**: Преобразует данные из CSV-файла в объекты SimpleNamespace.

**Параметры**:
- `csv_file` (str | Path): Путь к CSV-файлу для чтения.

**Возвращает**:
- `SimpleNamespace | None`: Объект SimpleNamespace, содержащий данные из CSV, или `None`, если преобразование не удалось.

**Вызывает исключения**:
- `Exception`: Если не удается прочитать CSV-файл.

**Пример**:
```python
>>> csv2ns('data.csv')
Namespace(column1=['value1', 'value2', 'value3'], column2=[1, 2, 3])
```

### `csv_to_json`

**Назначение**: Преобразует CSV-файл в JSON-формат и сохраняет его в JSON-файл.

**Параметры**:
- `csv_file_path` (str | Path): Путь к CSV-файлу для чтения.
- `json_file_path` (str | Path): Путь к JSON-файлу для сохранения.
- `exc_info` (bool, optional): Если True, включает информацию о трассировке в лог. По умолчанию True.

**Возвращает**:
- `List[Dict[str, str]] | None`: Данные JSON в виде списка словарей, или None, если преобразование не удалось.

**Пример**:
```python
>>> json_data = csv_to_json('dialogue_log.csv', 'dialogue_log.json')
>>> print(json_data)
[{'role': 'user', 'content': 'Hello'}, {'role': 'assistant', 'content': 'Hi there!'}]
```

## Внутренние функции

### `read_csv_as_dict`

**Назначение**: Читает CSV-файл и возвращает данные в виде словаря.

**Параметры**:
- `csv_file` (str | Path): Путь к CSV-файлу.
- `*args`: Дополнительные аргументы для `csv.DictReader`.
- `**kwargs`: Дополнительные аргументы для `csv.DictReader`.

**Возвращает**:
- `Dict[str, List[Any]] | None`: Словарь, где ключи - названия столбцов, значения - списки значений для каждого столбца, или `None` если произошла ошибка.

**Пример**:
```python
>>> read_csv_as_dict('data.csv')
{'column1': ['value1', 'value2', 'value3'], 'column2': [1, 2, 3]}
```

### `read_csv_as_ns`

**Назначение**: Читает CSV-файл и возвращает данные в виде объекта SimpleNamespace.

**Параметры**:
- `csv_file` (str | Path): Путь к CSV-файлу.
- `*args`: Дополнительные аргументы для `csv.DictReader`.
- `**kwargs`: Дополнительные аргументы для `csv.DictReader`.

**Возвращает**:
- `SimpleNamespace | None`: Объект SimpleNamespace, содержащий данные из CSV, или `None` если произошла ошибка.

**Пример**:
```python
>>> read_csv_as_ns('data.csv')
Namespace(column1=['value1', 'value2', 'value3'], column2=[1, 2, 3])
```

### `save_csv_file`

**Назначение**: Сохраняет данные в CSV-файл.

**Параметры**:
- `csv_file_path` (str | Path): Путь к CSV-файлу.
- `data` (List[Dict[str, Any]] | List[Any] | Dict[str, Any]): Данные для сохранения.
- `delimiter` (str, optional): Разделитель между столбцами. По умолчанию ',' (запятая).
- `quotechar` (str, optional): Символ кавычек. По умолчанию '"'.
- `quoting` (int, optional): Флаг для кавычек. По умолчанию csv.QUOTE_MINIMAL.
- `line_terminator` (str, optional): Символ конца строки. По умолчанию '\n'.
- `exc_info` (bool, optional): Если True, включает информацию о трассировке в лог. По умолчанию True.

**Возвращает**:
- `bool`: True, если файл был успешно сохранен, иначе False.

**Пример**:
```python
>>> save_csv_file('data.csv', [{'column1': 'value1', 'column2': 1}, {'column1': 'value2', 'column2': 2}])
True
```

### `read_csv_file`

**Назначение**: Читает CSV-файл и возвращает данные в виде списка словарей.

**Параметры**:
- `csv_file_path` (str | Path): Путь к CSV-файлу.
- `*args`: Дополнительные аргументы для `csv.DictReader`.
- `**kwargs`: Дополнительные аргументы для `csv.DictReader`.

**Возвращает**:
- `List[Dict[str, str]] | None`: Список словарей, содержащий данные из CSV, или `None` если произошла ошибка.

**Пример**:
```python
>>> read_csv_file('data.csv')
[{'column1': 'value1', 'column2': '1'}, {'column1': 'value2', 'column2': '2'}]
# Модуль для работы с Excel-файлами (XLS)

## Обзор

Модуль `src.utils.xls` предоставляет функции для преобразования файлов Excel в формат JSON и обратно. 

## Подробности

Модуль позволяет читать данные из Excel-файлов и сохранять их в JSON, а также  создавать новые Excel-файлы из JSON-данных. Он поддерживает обработку нескольких листов в файле и предоставляет механизм обработки ошибок.

## Функции

### `read_xls_as_dict`

**Назначение**: Функция считывает данные из Excel-файла и конвертирует их в формат JSON. Она может считывать данные из конкретного листа или из всех листов файла. 

**Параметры**:
- `xls_file` (str): Путь к Excel-файлу.
- `json_file` (str, optional): Путь к файлу для сохранения полученных JSON-данных. По умолчанию `None` (данные не сохраняются).
- `sheet_name` (Union[str, int], optional): Имя или индекс листа для чтения. По умолчанию `None` (считываются данные со всех листов).

**Возвращает**:
- `Dict`: Словарь, где ключи - имена листов, а значения - списки словарей, представляющих строки в каждом листе.
- `List[Dict]`: Список словарей, представляющих строки, если считывался один лист.
- `bool`: `False`, если произошла ошибка.

**Вызывает исключения**:
- `FileNotFoundError`: Если файл не найден.
- `Exception`: Если возникла ошибка при чтении или обработке файла.

**Как работает**:
- Функция проверяет наличие Excel-файла по указанному пути.
- Использует библиотеку `pandas` для чтения данных из файла Excel.
- Если указан `sheet_name`, читаются данные из одного листа. В противном случае, читаются данные из всех листов.
- Конвертирует данные из каждого листа в формат `records` с помощью метода `df.to_dict(orient='records')`.
- Сохраняет данные в JSON-файл, если указан `json_file`.

**Примеры**:

```python
# Чтение данных из листа 'Sheet1' и сохранение в JSON
data = read_xls_as_dict('input.xlsx', 'output.json', 'Sheet1')
if data:
    print(data)  # Выведет {'Sheet1': [{...}]}

# Чтение данных из всех листов
data = read_xls_as_dict('input.xlsx')
if data:
    print(data)  # Выведет {'Sheet1': [{...}], 'Sheet2': [{...}]}
```


### `save_xls_file`

**Назначение**: Функция сохраняет JSON-данные в Excel-файл.

**Параметры**:
- `data` (Dict[str, List[Dict]]): Словарь, где ключи - имена листов, а значения - списки словарей, представляющих строки в каждом листе.
- `file_path` (str): Путь к Excel-файлу для сохранения.

**Возвращает**:
- `bool`: `True`, если сохранение прошло успешно, `False` в случае ошибки.

**Вызывает исключения**:
- `Exception`: Если возникла ошибка при сохранении данных в файл.

**Как работает**:
- Функция использует библиотеку `pandas` для создания Excel-файла.
- Перебирает каждый лист в `data` и создает отдельный лист в Excel-файле.
- Сохраняет данные каждого листа в Excel-файл.

**Пример**:

```python
data_to_save = {'Sheet1': [{'column1': 'value1', 'column2': 'value2'}]}
success = save_xls_file(data_to_save, 'output.xlsx')
if success:
    print("Successfully saved to output.xlsx")
```

## Примеры использования

### Пример 1: Считывание Excel-файла и сохранение в JSON

```python
from src.utils.xls import read_xls_as_dict

# Чтение данных из Excel-файла и сохранение в JSON
data = read_xls_as_dict('input.xlsx', 'output.json', 'Sheet1')
if data:
    print(data)  # Выведет {'Sheet1': [{...}]}
```

### Пример 2: Создание Excel-файла из JSON-данных

```python
from src.utils.xls import save_xls_file

data_to_save = {'Sheet1': [{'column1': 'value1', 'column2': 'value2'}]}
success = save_xls_file(data_to_save, 'output.xlsx')
if success:
    print("Successfully saved to output.xlsx")
```

### Пример 3: Чтение данных из всех листов

```python
from src.utils.xls import read_xls_as_dict

# Чтение данных из всех листов
data = read_xls_as_dict('input.xlsx')
if data:
    print(data)  # Выведет {'Sheet1': [{...}], 'Sheet2': [{...}]}
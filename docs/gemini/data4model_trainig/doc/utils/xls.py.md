### Анализ кода модуля `hypotez/src/utils/xls.py`

## Обзор

Модуль предоставляет функции для преобразования файлов Excel (`xls`) в JSON и обратно, а также для работы с отдельными листами Excel.

## Подробнее

Модуль содержит функции для чтения Excel-файлов и преобразования их в JSON-формат, обработки нескольких листов и сохранения JSON-данных обратно в файлы Excel.

## Функции

### `read_xls_as_dict`

```python
def read_xls_as_dict(
    xls_file: str,
    json_file: str = None,
    sheet_name: Union[str, int] = None
) -> Union[Dict, List[Dict], bool]:
    """
    Reads an Excel file and converts it to JSON.  Optionally, converts a specific sheet and saves the result to a JSON file.
    Handles errors gracefully.
    """
    ...
```

**Назначение**:
Читает Excel-файл и преобразует его в JSON. При необходимости преобразует конкретный лист и сохраняет результат в JSON-файл. Корректно обрабатывает ошибки.

**Параметры**:
- `xls_file` (str): Путь к Excel-файлу.
- `json_file` (str, optional): Путь к JSON-файлу для сохранения результата. Если `None`, результат не сохраняется в файл. По умолчанию `None`.
- `sheet_name` (Union[str, int], optional): Имя или индекс листа Excel для преобразования. Если `None`, преобразуются все листы. По умолчанию `None`.

**Возвращает**:
- `Union[Dict, List[Dict], bool]`:
    - Если `sheet_name` не указан, возвращает словарь, где ключи - имена листов Excel, а значения - списки словарей, представляющих данные каждого листа.
    - Если `sheet_name` указан, возвращает список словарей, представляющих данные указанного листа.
    - Возвращает `False` в случае ошибки.

**Как работает функция**:

1. Проверяет существование Excel-файла.
2. Открывает Excel-файл с использованием `pandas.ExcelFile`.
3. Если `sheet_name` не указан:
    - Перебирает все листы Excel-файла.
    - Для каждого листа преобразует данные в список словарей с помощью `pandas.read_excel` и `to_dict(orient='records')`.
    - Сохраняет данные в словарь, где ключ - имя листа, а значение - список словарей.
4. Если `sheet_name` указан:
    - Преобразует данные указанного листа в список словарей.
5. Если указан `json_file`, сохраняет данные в JSON-файл с использованием `json.dump`.

**Вызывает исключения**:
- Нет

**Примеры**:

```python
# Чтение всего Excel-файла в словарь
data = read_xls_as_dict('input.xlsx')
if data:
    print(data)
    # Вывод: {'Sheet1': [{'column1': 'value1', 'column2': 'value2'}], 'Sheet2': [...]}

# Чтение конкретного листа Excel-файла в список словарей
data = read_xls_as_dict('input.xlsx', sheet_name='Sheet1')
if data:
    print(data)
    # Вывод: [{'column1': 'value1', 'column2': 'value2'}, ...]

# Чтение Excel-файла и сохранение в JSON-файл
data = read_xls_as_dict('input.xlsx', 'output.json', 'Sheet1')
if data:
    print("Данные успешно сохранены в файл output.json")
```

### `save_xls_file`

```python
def save_xls_file(data: Dict[str, List[Dict]], file_path: str) -> bool:
    """Saves JSON data to an Excel file. Handles errors gracefully."""
    ...
```

**Назначение**:
Сохраняет JSON-данные в Excel-файл. Корректно обрабатывает ошибки.

**Параметры**:
- `data` (Dict[str, List[Dict]]): Данные для сохранения. Должны быть словарем, где ключи - имена листов, а значения - списки словарей, представляющих строки.
- `file_path` (str): Путь к Excel-файлу для сохранения.

**Возвращает**:
- `bool`: True, если данные успешно сохранены, False в противном случае.

**Как работает функция**:
1. Открывает Excel-файл для записи с использованием `pandas.ExcelWriter`.
2. Перебирает все листы и строки в данных.
3. Для каждого листа создает DataFrame Pandas и записывает его в Excel-файл.
4. Логирует информацию об успешном сохранении каждого листа.
5. В случае возникновения ошибок логирует информацию об ошибке и возвращает False.

**Вызывает исключения**:
- Нет

**Примеры**:

```python
data_to_save = {'Sheet1': [{'column1': 'value1', 'column2': 'value2'}]}
success = save_xls_file(data_to_save, 'output.xlsx')
if success:
    print("Successfully saved to output.xlsx")
```

## Переменные

Отсутствуют

## Запуск

Для использования этого модуля необходимо установить библиотеки `pandas`, `xlsxwriter` и `json_repair`.

```bash
pip install pandas xlsxwriter json_repair
```

Пример использования функций:

```python
from src.utils import xls

# Чтение и преобразование в JSON
data = xls.read_xls_as_dict('input.xlsx', 'output.json', 'Sheet1')

# Сохранение JSON в Excel
data_to_save = {'Sheet1': [{'column1': 'value1', 'column2': 'value2'}]}
success = xls.save_xls_file(data_to_save, 'output.xlsx')
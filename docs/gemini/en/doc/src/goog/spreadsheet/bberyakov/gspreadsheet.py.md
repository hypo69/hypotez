# Модуль GSpreadsheet
## Обзор

Этот модуль предоставляет функциональность для работы с Google Sheets. В нем реализована работа с книгами, листами и ячейками. 

## Подробности

Модуль `gspreadsheet.py` предоставляет классы и функции для взаимодействия с Google Spreadsheets. Он использует библиотеку `gspread` для работы с API Google Sheets.

## Классы

### `GSpreadsheet`

**Описание**: Класс `GSpreadsheet` предоставляет функциональность для работы с Google Sheets.

**Наследование**: 
- Наследуется от `Spreadsheet`, предоставляя функциональность работы с книгами.

**Атрибуты**:

- `gsh`: Объект `Spreadsheet`, представляющий собой текущую Google Sheet.
- `gclient`: Объект `gspread.client`, предоставляющий методы для взаимодействия с API Google Sheets.

**Методы**:

#### `__init__`

**Описание**:  Инициализирует объект `GSpreadsheet`. 

**Параметры**:

- `self`: Ссылка на текущий объект.
- `s_id`: (str, optional) ID Google Sheets. Defaults to None.
- `s_title`: (str, optional) Название Google Sheets. Defaults to None.
- `*args`: Дополнительные аргументы.
- `**kwargs`: Дополнительные именованные аргументы.


#### `get_project_spreadsheets_dict`

**Описание**:  Возвращает список всех Google Sheets, доступных для проекта, в виде словаря.

**Параметры**:

- `self`: Ссылка на текущий объект.

**Возвращаемое значение**:

- `dict`: Словарь, содержащий информацию обо всех Google Sheets проекта.

#### `get_by_title`

**Описание**:  Открывает Google Sheet по названию. Если Google Sheet с заданным названием не существует, то создает новую Google Sheet.

**Параметры**:

- `self`: Ссылка на текущий объект.
- `sh_title`: (str, optional) Название Google Sheets. Defaults to 'New Spreadsheet'.

#### `get_by_id`

**Описание**:  Открывает Google Sheet по ID.

**Параметры**:

- `self`: Ссылка на текущий объект.
- `sh_id`: (str) ID Google Sheets.

**Возвращаемое значение**:

- `Spreadsheet`: Объект `Spreadsheet`, представляющий собой Google Sheet.

#### `get_all_spreadsheets_for_current_account`

**Описание**: Возвращает список всех Google Sheets, доступных для текущего аккаунта.

**Параметры**:

- `self`: Ссылка на текущий объект.

**Возвращаемое значение**:

- `list`: Список `Spreadsheet` объектов, представляющих все доступные Google Sheets.

## Примеры
```python
# Создание объекта GSpreadsheet
spreadsheet = GSpreadsheet(s_id='1ZcK74BCgWKVr4kODjPmSvjp5IyO0OxhXdbeHKWzLQiM')

# Получение списка всех Google Sheets проекта
spreadsheets = spreadsheet.get_project_spreadsheets_dict()

# Открытие Google Sheet по названию
spreadsheet.get_by_title('My Spreadsheet')

# Открытие Google Sheet по ID
spreadsheet.get_by_id('1ZcK74BCgWKVr4kODjPmSvjp5IyO0OxhXdbeHKWzLQiM')

# Получение списка всех Google Sheets для текущего аккаунта
all_spreadsheets = spreadsheet.get_all_spreadsheets_for_current_account()
```
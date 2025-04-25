# Модуль `gspreadsheet`

## Обзор

Модуль `gspreadsheet` предоставляет функции для работы с таблицами Google Sheets. Он позволяет создавать, открывать, изменять и получать доступ к таблицам Google Sheets.

## Подробнее

Модуль  `gspreadsheet` предоставляет класс `GSpreadsheet`, который позволяет работать с Google Sheets. 
В этом модуле используются функции и классы из модуля `gspread`, а также настройки из `global_settings.py`. 
Этот модуль предоставляет функции для создания новых таблиц, доступа к существующим таблицам по названию или идентификатору. 

## Классы

### `GSpreadsheet`

**Описание**: Класс `GSpreadsheet` представляет собой оболочку для работы с таблицами Google Sheets. Он предоставляет методы для создания, открытия, получения доступа к таблицам и управления доступом к ним.

**Наследует**:
    - `Spreadsheet`: класс `Spreadsheet` предоставляет базовые функциональные возможности для работы с Google Sheets.

**Атрибуты**:
    - `gsh`:  `Spreadsheet` — экземпляр объекта `Spreadsheet`, представляющий собой текущую открытую книгу Google Sheets.
    - `gclient`:  `gspread.client` — объект клиента для доступа к Google Sheets.

**Методы**:
    - `__init__(self, s_id: str = None, s_title: str = None, *args, **kwargs)`: Инициализирует экземпляр класса `GSpreadsheet`. Принимает параметры `s_id` (идентификатор таблицы) и `s_title` (название таблицы).
    - `get_project_spreadsheets_dict(self) -> dict`: Возвращает словарь с описанием таблиц Google Sheets, используемых в проекте.
    - `get_by_title(self, sh_title: str = 'New Spreadsheet')`: Открывает таблицу Google Sheets по названию `sh_title`. Создаёт новую таблицу, если такой нет.
    - `get_by_id(self, sh_id: str) -> Spreadsheet`: Открывает таблицу Google Sheets по идентификатору `sh_id`. 
    - `get_all_spreadsheets_for_current_account(self)`: Возвращает список всех таблиц, доступных для текущего аккаунта.

**Пример**:
```python
from src.goog.spreadsheet.bberyakov.gspreadsheet import GSpreadsheet

# Создаём объект GSpreadsheet с использованием идентификатора таблицы
spreadsheet = GSpreadsheet(s_id='1ZcK74BCgWKVr4kODjPmSvjp5IyO0OxhXdbeHKWzLQiM')

# Получаем список всех таблиц для текущего аккаунта
spreadsheets = spreadsheet.get_all_spreadsheets_for_current_account()

# Открываем таблицу по названию
spreadsheet.get_by_title('My Spreadsheet')

# Получаем словарь с описанием таблиц проекта
project_spreadsheets = spreadsheet.get_project_spreadsheets_dict()

```

## Функции

### `service_account(filename: str) -> gspread.client`

**Назначение**: Функция `service_account` создаёт объект клиента для доступа к Google Sheets, используя файл с секретным ключом.

**Параметры**:
    - `filename: str`: Путь к файлу с секретным ключом.

**Возвращает**:
    - `gspread.client`: Объект клиента для доступа к Google Sheets.

**Вызывает исключения**:
    - `Exception`: В случае ошибки при чтении файла с секретным ключом.

**Пример**:
```python
from src.goog.spreadsheet.bberyakov.gspreadsheet import service_account

# Создаём объект клиента для доступа к Google Sheets
client = service_account('goog\\onela-hypotez-1aafa5e5d1b5.json')

# Используем объект клиента для работы с таблицами Google Sheets
# ...

```

## Параметры класса

- `s_id`: Идентификатор таблицы Google Sheets. 
- `s_title`: Название таблицы Google Sheets.

## Примеры

```python
# Импортируем класс GSpreadsheet
from src.goog.spreadsheet.bberyakov.gspreadsheet import GSpreadsheet

# Создаём объект GSpreadsheet с использованием идентификатора таблицы
spreadsheet = GSpreadsheet(s_id='1ZcK74BCgWKVr4kODjPmSvjp5IyO0OxhXdbeHKWzLQiM')

# Открываем таблицу по названию
spreadsheet.get_by_title('My Spreadsheet')

# Открываем таблицу по идентификатору
spreadsheet = spreadsheet.get_by_id('1ZcK74BCgWKVr4kODjPmSvjp5IyO0OxhXdbeHKWzLQiM')

# Получаем словарь с описанием таблиц проекта
project_spreadsheets = spreadsheet.get_project_spreadsheets_dict()

# Выводим список всех таблиц для текущего аккаунта
spreadsheets = spreadsheet.get_all_spreadsheets_for_current_account()
print(spreadsheets)
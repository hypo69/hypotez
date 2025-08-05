# Модуль `gspreadsheet`

## Обзор

Модуль предназначен для работы с Google Sheets API через библиотеку `gspread`. Он предоставляет класс `GSpreadsheet`, который наследует функциональность класса `Spreadsheet` и расширяет её для упрощения взаимодействия с Google Sheets. Модуль позволяет открывать, создавать и делиться таблицами, а также получать доступ к таблицам по ID или заголовку.

## Подробнее

Модуль `gspreadsheet` является частью пакета `src.goog.spreadsheet.bberyakov` и предназначен для интеграции с Google Sheets. Он использует библиотеку `gspread` для аутентификации и взаимодействия с Google Sheets API. Класс `GSpreadsheet` предоставляет методы для работы с таблицами, такие как открытие по ID или заголовку, создание новых таблиц и предоставление доступа к ним другим пользователям.

## Классы

### `GSpreadsheet`

**Описание**: Класс для работы с Google Sheets.

**Наследует**:
- `Spreadsheet`: Расширяет базовый класс `Spreadsheet` для работы с Google Sheets.

**Атрибуты**:
- `gsh` (Spreadsheet): Объект таблицы Google Sheets.
- `gclient` (gspread.client): Клиент для взаимодействия с Google Sheets API.

**Принцип работы**:
Класс `GSpreadsheet` инициализируется с использованием учетных данных Google Service Account, хранящихся в файле `goog/onela-hypotez-1aafa5e5d1b5.json`. Он предоставляет методы для открытия таблиц по ID или заголовку, создания новых таблиц и обмена ими с другими пользователями.

**Методы**:
- `__init__(s_id: str = None, s_title: str = None, *args, **kwargs)`: Инициализирует экземпляр класса `GSpreadsheet`.
- `get_project_spreadsheets_dict() -> dict`: Возвращает словарь с информацией о таблицах проекта.
- `get_by_title(sh_title: str = 'New Spreadsheet')`: Открывает таблицу по заголовку. Если таблица с таким заголовком не существует, она будет создана.
- `get_by_id(sh_id: str) -> Spreadsheet`: Открывает таблицу по ID.
- `get_all_spreadsheets_for_current_account()`: Возвращает все таблицы, доступные для текущего аккаунта.

## Методы класса

### `__init__`

```python
def __init__(self, s_id: str = None, s_title: str = None, *args, **kwargs):
    """
    Книга google spreadsheet
    """
    secret_file = f'goog\\\\onela-hypotez-1aafa5e5d1b5.json'
    self.gclient = service_account(filename = secret_file)
    if s_id:
        self.gsh = self.get_by_id('1ZcK74BCgWKVr4kODjPmSvjp5IyO0OxhXdbeHKWzLQiM')
    if s_title:
        self.gsh = self.get_by_title(s_title)
```

**Назначение**: Инициализирует экземпляр класса `GSpreadsheet`.

**Параметры**:
- `s_id` (str, optional): ID таблицы Google Sheets. По умолчанию `None`.
- `s_title` (str, optional): Заголовок таблицы Google Sheets. По умолчанию `None`.
- `*args`: Произвольные позиционные аргументы.
- `**kwargs`: Произвольные именованные аргументы.

**Как работает функция**:
- Функция инициализирует клиент Google Sheets API, используя учетные данные из файла `goog/onela-hypotez-1aafa5e5d1b5.json`.
- Если передан `s_id`, пытается открыть таблицу по ID.
- Если передан `s_title`, пытается открыть таблицу по заголовку.

### `get_project_spreadsheets_dict`

```python
def get_project_spreadsheets_dict(self) -> dict:
    """
    """
    return json.loads('goog\\\\spreadsheets.json')
```

**Назначение**: Возвращает словарь с информацией о таблицах проекта.

**Параметры**:
- `self`: Ссылка на экземпляр класса.

**Возвращает**:
- `dict`: Словарь с информацией о таблицах проекта, загруженный из файла `goog/spreadsheets.json`.

**Как работает функция**:
- Функция загружает JSON-файл `goog/spreadsheets.json` и преобразует его содержимое в словарь Python.
- Возвращает полученный словарь.

### `get_by_title`

```python
def get_by_title (self, sh_title: str = 'New Spreadsheet'):
    """
    Создаю книгу, если такой нет
    """
    if sh_title not in [sh.title for sh in self.gsh.openall()]:
        self.gsh.create(sh_title)
        self.gsh.share('d07708766@gmail.com', perm_type='user', role='writer')

        # _gsh = self.create(sh_title)
        # self.set_spreadsheet_direction(_gsh, 'rtl')
        # _gsh.share('d07708766@gmail.com', perm_type='user', role='writer')
        # self = _gsh
    else:
        print(f'Spreadsheet {sh_title} already exist')
        self.gsh.open_by_title(sh_title)
```

**Назначение**: Открывает таблицу Google Sheets по её заголовку. Если таблица с указанным заголовком не существует, она создается.

**Параметры**:
- `self`: Ссылка на экземпляр класса.
- `sh_title` (str, optional): Заголовок таблицы, которую нужно открыть. По умолчанию 'New Spreadsheet'.

**Как работает функция**:
- Проверяет, существует ли таблица с указанным заголовком среди всех таблиц текущего аккаунта.
- Если таблица не существует, создает новую таблицу с указанным заголовком и предоставляет доступ пользователю `d07708766@gmail.com` с правами записи.
- Если таблица существует, открывает её.

### `get_by_id`

```python
def get_by_id (self, sh_id: str) -> Spreadsheet:
    """
    Открываю таблицу
    """
    #self = self.gclient.open_by_key (sh_id)
    return self.gclient.open_by_key (sh_id)
```

**Назначение**: Открывает таблицу Google Sheets по её ID.

**Параметры**:
- `self`: Ссылка на экземпляр класса.
- `sh_id` (str): ID таблицы, которую нужно открыть.

**Возвращает**:
- `Spreadsheet`: Объект таблицы Google Sheets.

**Как работает функция**:
- Открывает таблицу с указанным ID, используя метод `open_by_key` клиента `gspread`.
- Возвращает объект открытой таблицы.

### `get_all_spreadsheets_for_current_account`

```python
def get_all_spreadsheets_for_current_account (self):
    """
    открываю все книги (spreadsheets) аккаунта
    """
    return self.openall()
```

**Назначение**: Возвращает все таблицы Google Sheets, доступные для текущего аккаунта.

**Параметры**:
- `self`: Ссылка на экземпляр класса.

**Возвращает**:
- Результат вызова метода `openall`.

**Как работает функция**:
- Вызывает метод `openall` для получения списка всех таблиц, доступных для текущего аккаунта.
- Возвращает полученный список.
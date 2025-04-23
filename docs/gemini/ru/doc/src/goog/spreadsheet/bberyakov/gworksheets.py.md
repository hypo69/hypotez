# Модуль `gworksheets`

## Обзор

Модуль `gworksheets` предназначен для работы с Google Sheets, предоставляя функциональность для создания, получения и управления листами (worksheets) в таблицах Google Spreadsheet. Он включает классы для абстракции работы с таблицами и листами, а также для рендеринга данных в листах.

## Подробней

Модуль `gworksheets` является частью проекта `hypotez` и предназначен для упрощения взаимодействия с Google Sheets API. Он предоставляет удобный интерфейс для выполнения таких операций, как создание новых листов, открытие существующих листов, очистка данных в листах и установка направления текста (например, справа налево для языков с арабским письмом).

## Классы

### `GWorksheet`

**Описание**: Класс `GWorksheet` представляет собой обертку для работы с листами Google Sheets. Он наследует функциональность от класса `Worksheet` и предоставляет методы для управления листом, такие как получение листа, установка заголовка и установка направления текста.

**Наследует**:

- `Worksheet`: Класс, предоставляющий базовый функционал для работы с листами.

**Атрибуты**:

- `sh`: Объект, представляющий таблицу Google Spreadsheet.
- `ws`: Объект `Worksheet`, представляющий текущий лист.
- `render`: Объект `GSRender`, используемый для рендеринга данных в листе.

**Методы**:

- `__init__(self, sh, ws_title: str = 'new', rows = None, cols = None, direcion = 'rtl', wipe_if_exist: bool = True, *args, **kwargs)`: Конструктор класса.
- `get(self, sh, ws_title: str = 'new', rows: int = 100, cols: int = 100, direction: str = 'rtl', wipe_if_exist: bool = True)`: Получает или создает лист в таблице.
- `header(self, world_title: str, range: str = 'A1:Z1', merge_type: str('MERGE_ALL') | str('MERGE_COLUMNS') | str('MERGE_ROWS') = 'MERGE_ALL')`: Устанавливает заголовок листа.
- `category(self, ws_category_title)`: Записывает заголовок категории в лист.
- `direction(self, direction: str = 'rtl')`: Устанавливает направление текста в листе.

### `__init__(self, sh, ws_title: str = 'new', rows = None, cols = None, direcion = 'rtl', wipe_if_exist: bool = True, *args, **kwargs) -> None`

```python
def __init__(self, sh, ws_title: str = 'new', rows = None, cols = None, direcion = 'rtl', wipe_if_exist: bool = True, *args, **kwargs) -> None
```

**Назначение**: Инициализирует объект `GWorksheet`.

**Параметры**:

- `sh`: Объект, представляющий таблицу Google Spreadsheet.
- `ws_title` (str, optional): Название листа. По умолчанию 'new'.
- `rows` (int, optional): Количество строк в листе. По умолчанию None.
- `cols` (int, optional): Количество столбцов в листе. По умолчанию None.
- `direcion` (str, optional): Направление текста в листе. По умолчанию 'rtl' (right-to-left).
- `wipe_if_exist` (bool, optional): Если True, очищает лист, если он существует. По умолчанию True.
- `*args`: Произвольные позиционные аргументы.
- `**kwargs`: Произвольные именованные аргументы.

**Как работает функция**:
- Функция инициализирует объект `GWorksheet`, устанавливая значения атрибутов `sh` (таблица Google Spreadsheet), `ws` (текущий лист) и `render` (объект для рендеринга данных).
- Вызывает метод `get` для получения или создания листа с указанным названием и параметрами.

**Примеры**:

```python
# Пример создания объекта GWorksheet
gws = GWorksheet(sh=spreadsheet_object, ws_title='MySheet', rows=150, cols=50, direcion='ltr', wipe_if_exist=False)
```

### `get(self, sh, ws_title: str = 'new', rows: int = 100, cols: int = 100, direction: str = 'rtl', wipe_if_exist: bool = True)`

```python
def get(self, sh, ws_title: str = 'new', rows: int = 100, cols: int = 100, direction: str = 'rtl', wipe_if_exist: bool = True)
```

**Назначение**: Получает или создает лист в таблице Google Spreadsheet.

**Параметры**:

- `sh`: Объект, представляющий таблицу Google Spreadsheet.
- `ws_title` (str, optional): Название листа. Если 'new', создает новый лист. По умолчанию 'new'.
- `rows` (int, optional): Количество строк в новом листе. По умолчанию 100.
- `cols` (int, optional): Количество столбцов в новом листе. По умолчанию 100.
- `direction` (str, optional): Направление текста в листе. По умолчанию 'rtl' (right-to-left).
- `wipe_if_exist` (bool, optional): Если True, очищает лист, если он существует. По умолчанию True.

**Как работает функция**:
- Функция проверяет, существует ли лист с указанным названием (`ws_title`) в таблице (`sh`).
- Если `ws_title` равно 'new', создает новый лист.
- Если лист с указанным названием существует, открывает его и, если `wipe_if_exist` равно True, очищает его от старых данных.
- Если лист с указанным названием не существует, создает новый лист с указанным названием, количеством строк и столбцов.
- Устанавливает направление текста в листе с помощью метода `set_worksheet_direction` объекта `render`.

**Примеры**:

```python
# Пример получения существующего листа
gws.get(sh=spreadsheet_object, ws_title='ExistingSheet', wipe_if_exist=True)

# Пример создания нового листа
gws.get(sh=spreadsheet_object, ws_title='NewSheet', rows=200, cols=50, direction='ltr')
```

### `header(self, world_title: str, range: str = 'A1:Z1', merge_type: str('MERGE_ALL') | str('MERGE_COLUMNS') | str('MERGE_ROWS') = 'MERGE_ALL') -> None`

```python
def header(self, world_title: str, range: str = 'A1:Z1', merge_type: str('MERGE_ALL') | str('MERGE_COLUMNS') | str('MERGE_ROWS') = 'MERGE_ALL') -> None
```

**Назначение**: Устанавливает заголовок листа.

**Параметры**:

- `world_title` (str): Текст заголовка.
- `range` (str, optional): Диапазон ячеек для заголовка. По умолчанию 'A1:Z1'.
- `merge_type` (str, optional): Тип объединения ячеек для заголовка. Может быть 'MERGE_ALL', 'MERGE_COLUMNS' или 'MERGE_ROWS'. По умолчанию 'MERGE_ALL'.

**Как работает функция**:
- Функция вызывает метод `header` объекта `render` для установки заголовка листа с указанным текстом, диапазоном ячеек и типом объединения.

**Примеры**:

```python
# Пример установки заголовка листа
gws.header(world_title='My Spreadsheet Title', range='A1:H1', merge_type='MERGE_ALL')
```

### `category(self, ws_category_title)`

```python
def category(self, ws_category_title)
```

**Назначение**: Записывает заголовок категории в лист.

**Параметры**:

- `ws_category_title` (str): Текст заголовка категории.

**Как работает функция**:
- Функция вызывает метод `write_category_title` объекта `render` для записи заголовка категории в лист.

**Примеры**:

```python
# Пример записи заголовка категории
gws.category(ws_category_title='Category Title')
```

### `direction(self, direction: str = 'rtl')`

```python
def direction(self, direction: str = 'rtl')
```

**Назначение**: Устанавливает направление текста в листе.

**Параметры**:

- `direction` (str, optional): Направление текста. По умолчанию 'rtl' (right-to-left).

**Как работает функция**:
- Функция вызывает метод `set_worksheet_direction` объекта `render` для установки направления текста в листе.

**Примеры**:

```python
# Пример установки направления текста в листе
gws.direction(direction='ltr')
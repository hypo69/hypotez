# Модуль `grender`

## Обзор

Модуль `grender` предназначен для стилизации и форматирования таблиц Google Sheets, используя библиотеки `gspread`, `gspread_formatting` и другие инструменты для работы с Google Sheets API. Он позволяет настраивать внешний вид таблиц, добавлять заголовки, объединять ячейки и устанавливать направление текста.

## Подробнее

Модуль содержит класс `GSRender`, который инкапсулирует методы для рендеринга таблиц. Он предоставляет функциональность для создания заголовков с определенным форматированием, объединения ячеек, установки направления текста и записи данных в таблицу. Модуль использует вспомогательные функции из других модулей проекта, таких как `goog.helpers` и `spread.utils`.

## Классы

### `GSRender`

**Описание**: Класс `GSRender` предназначен для управления внешним видом и форматированием таблиц Google Sheets.

**Атрибуты**:

- `render_schemas` (dict): Словарь, содержащий схемы рендеринга.

**Методы**:

- `__init__(*args, **kwargs)`: Конструктор класса `GSRender`.
- `render_header(ws: Worksheet, world_title: str, range: str = 'A1:Z1', merge_type: str('MERGE_ALL') | str('MERGE_COLUMNS') | str('MERGE_ROWS') = 'MERGE_ALL')`: Отрисовывает заголовок таблицы в первой строке.
- `merge_range(ws: Worksheet, range: str, merge_type: str('MERGE_ALL') | str('MERGE_COLUMNS') | str('MERGE_ROWS') = 'MERGE_ALL')`: Объединяет ячейки в указанном диапазоне.
- `set_worksheet_direction(sh: Spreadsheet, ws: Worksheet, direction: str('ltr') | str('rtl') = 'rtl')`: Устанавливает направление текста на листе Google Sheets.
- `header(ws: Worksheet, ws_header: str | list, row: int = None)`: Добавляет заголовок таблицы на указанный лист.
- `write_category_title(ws: Worksheet, ws_category_title: str | list, row: int = None)`: Записывает заголовок категории на лист Google Sheets.
- `get_first_empty_row(ws: Worksheet, by_col: int = None) -> int`: Возвращает номер первой пустой строки на листе.

## Методы класса

### `__init__`

```python
def __init__(self, *args, **kwargs) -> None
```

**Назначение**: Инициализирует экземпляр класса `GSRender`. В текущей версии функциональность инициализации не реализована (`...`).

**Параметры**:
- `*args`: Произвольный список позиционных аргументов.
- `**kwargs`: Произвольный словарь именованных аргументов.

**Возвращает**:
- `None`

### `render_header`

```python
def render_header (self, ws: Worksheet, world_title: str, range: str = 'A1:Z1', merge_type: str('MERGE_ALL') | str('MERGE_COLUMNS') | str('MERGE_ROWS') = 'MERGE_ALL' ) -> None
```

**Назначение**: Отрисовывает заголовок таблицы в первой строке.

**Параметры**:
- `ws` (Worksheet): Объект `Worksheet`, представляющий таблицу в Google Sheets.
- `world_title` (str): Заголовок таблицы.
- `range` (str): Диапазон ячеек для заголовка (по умолчанию `'A1:Z1'`).
- `merge_type` (str): Тип объединения ячеек (`'MERGE_ALL'`, `'MERGE_COLUMNS'` или `'MERGE_ROWS'`, по умолчанию `'MERGE_ALL'`).

**Возвращает**:
- `None`

**Как работает функция**:
1. Определяет цвета фона и текста.
2. Создает объект `CellFormat` с заданными параметрами форматирования, такими как цвет фона, выравнивание и формат текста.
3. Создает правило условного форматирования для применения заданного формата к диапазону ячеек.
4. Устанавливает высоту строки.
5. Применяет форматирование к указанному диапазону ячеек.
6. Объединяет ячейки в указанном диапазоне.

**Примеры**:

```python
# Пример использования:
# Создание объекта GSRender (предполагается, что sh и ws уже определены)
# gs_render = GSRender()
# gs_render.render_header(ws, "Заголовок таблицы", "A1:C1")
```

### `merge_range`

```python
def merge_range (self, ws: Worksheet, range: str, merge_type: str('MERGE_ALL') | str('MERGE_COLUMNS') | str('MERGE_ROWS') =  'MERGE_ALL') -> None
```

**Назначение**: Объединяет ячейки в указанном диапазоне.

**Параметры**:
- `ws` (Worksheet): Объект `Worksheet`, представляющий таблицу в Google Sheets.
- `range` (str): Диапазон ячеек для объединения.
- `merge_type` (str): Тип объединения ячеек (`'MERGE_ALL'`, `'MERGE_COLUMNS'` или `'MERGE_ROWS'`, по умолчанию `'MERGE_ALL'`).

**Возвращает**:
- `None`

**Как работает функция**:
1. Вызывает метод `merge_cells` объекта `ws` для объединения ячеек в указанном диапазоне с заданным типом объединения.

**Примеры**:

```python
# Пример использования:
# Создание объекта GSRender (предполагается, что sh и ws уже определены)
# gs_render = GSRender()
# gs_render.merge_range(ws, "A1:C1", "MERGE_ALL")
```

### `set_worksheet_direction`

```python
def set_worksheet_direction (self, sh: Spreadsheet, ws: Worksheet, direction: str ('ltr') | str ('rtl') = 'rtl' ):
```

**Назначение**: Устанавливает направление текста на листе Google Sheets (слева направо или справа налево).

**Параметры**:
- `sh` (Spreadsheet): Объект `Spreadsheet`, представляющий всю таблицу Google Sheets.
- `ws` (Worksheet): Объект `Worksheet`, представляющий конкретный лист в таблице.
- `direction` (str): Направление текста (`'ltr'` для слева направо или `'rtl'` для справа налево`, по умолчанию `'rtl'`).

**Как работает функция**:
1. Формирует словарь `data` с запросом на обновление свойств листа.
2. Устанавливает свойство `rightToLeft` в значение `True`, если `direction` равно `'rtl'`, что указывает на направление текста справа налево.
3. Вызывает метод `batch_update` объекта `sh` для применения изменений к листу.

**Примеры**:

```python
# Пример использования:
# Создание объекта GSRender (предполагается, что sh и ws уже определены)
# gs_render = GSRender()
# gs_render.set_worksheet_direction(sh, ws, "rtl")
```

### `header`

```python
def header(self, ws: Worksheet, ws_header: str | list, row: int = None):
```

**Назначение**: Добавляет заголовок таблицы на указанный лист.

**Параметры**:
- `ws` (Worksheet): Объект `Worksheet`, представляющий таблицу в Google Sheets.
- `ws_header` (str | list): Заголовок таблицы (строка или список строк).
- `row` (int): Номер строки для заголовка (если не указан, используется первая пустая строка).

**Как работает функция**:
1. Определяет номер строки для заголовка (использует `get_first_empty_row`, если `row` не указан).
2. Преобразует `ws_header` в список, если это строка.
3. Добавляет строку с заголовком на лист.
4. Форматирует добавленный заголовок с использованием `render_header`.

**Примеры**:

```python
# Пример использования:
# Создание объекта GSRender (предполагается, что sh и ws уже определены)
# gs_render = GSRender()
# gs_render.header(ws, "Заголовок таблицы")
```

### `write_category_title`

```python
def write_category_title (self, ws: Worksheet, ws_category_title: str | list, row: int = None):
```

**Назначение**: Записывает заголовок категории на лист Google Sheets.

**Параметры**:
- `ws` (Worksheet): Объект `Worksheet`, представляющий таблицу в Google Sheets.
- `ws_category_title` (str | list): Заголовок категории (строка или список строк).
- `row` (int): Номер строки для заголовка категории (если не указан, используется первая пустая строка).

**Как работает функция**:
1. Определяет номер строки для заголовка категории (если `row` не указан).
2. Преобразует `ws_category_title` в список, если это строка.
3. Добавляет строку с заголовком категории на лист.
4. Объединяет ячейки для заголовка категории.

**Примеры**:

```python
# Пример использования:
# Создание объекта GSRender (предполагается, что sh и ws уже определены)
# gs_render = GSRender()
# gs_render.write_category_title(ws, "Заголовок категории", row=2)
```

### `get_first_empty_row`

```python
def get_first_empty_row (self, ws: Worksheet, by_col: int = None) -> int:
```

**Назначение**: Возвращает номер первой пустой строки на листе.

**Параметры**:
- `ws` (Worksheet): Объект `Worksheet`, представляющий таблицу в Google Sheets.
- `by_col` (int): Номер колонки для проверки (если не указан, проверяется вся таблица).

**Возвращает**:
- `int`: Номер первой пустой строки.

**Как работает функция**:
1. Получает список всех значений в указанной колонке (или во всей таблице, если `by_col` не указан).
2. Фильтрует список, удаляя пустые значения.
3. Возвращает длину отфильтрованного списка + 1, что соответствует номеру первой пустой строки.

**Примеры**:

```python
# Пример использования:
# Создание объекта GSRender (предполагается, что sh и ws уже определены)
# gs_render = GSRender()
# first_empty_row = gs_render.get_first_empty_row(ws)
# print(first_empty_row)
```
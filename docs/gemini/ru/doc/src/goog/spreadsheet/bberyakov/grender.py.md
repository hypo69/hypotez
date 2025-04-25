# Модуль для рендеринга таблиц Google Spreadsheets

## Обзор

Модуль `src.goog.spreadsheet.bberyakov.grender` предоставляет классы и функции для рендеринга таблиц Google Spreadsheets. Он используется для оформления, форматирования и обновления содержимого таблиц с помощью библиотеки `gspread`.

## Подробнее

Модуль содержит класс `GSRender`, который предоставляет функциональность для рендеринга таблиц Google Spreadsheets. 

## Классы

### `GSRender`

**Описание**: Класс для рендеринга таблиц Google Spreadsheets.

**Атрибуты**:

- `render_schemas`: Словарь с схемами рендеринга.

**Методы**:

- `__init__(self, *args, **kwargs) -> None`: Конструктор класса.

- `render_header(self, ws: Worksheet, world_title: str, range: str = 'A1:Z1', merge_type: str('MERGE_ALL') | str('MERGE_COLUMNS') | str('MERGE_ROWS') = 'MERGE_ALL') -> None`: Рисует заголовок таблицы в первой строке.

- `merge_range(self, ws: Worksheet, range: str, merge_type: str('MERGE_ALL') | str('MERGE_COLUMNS') | str('MERGE_ROWS') = 'MERGE_ALL') -> None`: Объединяет ячейки в таблице.

- `set_worksheet_direction(self, sh: Spreadsheet, ws: Worksheet, direction: str ('ltr') | str ('rtl') = 'rtl')`: Задает направление текста в таблице.

- `header(self, ws: Worksheet, ws_header: str | list, row: int = None)`: Добавляет заголовок в таблицу.

- `write_category_title(self, ws: Worksheet, ws_category_title: str | list, row: int = None)`: Добавляет заголовок категории в таблицу.

- `get_first_empty_row(self, ws: Worksheet, by_col: int = None) -> int`: Возвращает номер первой пустой строки в таблице.



## Функции

### `render_header`

**Назначение**: Рисует заголовок таблицы в первой строке.

**Параметры**:

- `ws` (Worksheet): Таблица в книге.
- `world_title` (str): Заголовок гугл таблицы.
- `range` (str): Диапазон ячеек.
- `merge_type` (str('MERGE_ALL') | str('MERGE_COLUMNS') | str('MERGE_ROWS') = 'MERGE_ALL'): Тип объединения ячеек.

**Возвращает**:

- `None`: Не возвращает значения.

**Как работает функция**:

- Функция `render_header` принимает в качестве входных данных таблицу Google Spreadsheets (`ws`), заголовок таблицы (`world_title`), диапазон ячеек для заголовка (`range`) и тип объединения ячеек (`merge_type`). 
- Она устанавливает цвет фона и текста для ячеек в заданном диапазоне. 
- Затем функция применяет условное форматирование, чтобы установить цвет фона для ячеек, значения которых больше 50. 
- Наконец, функция объединяет ячейки в заданном диапазоне в соответствии с указанным типом объединения.

**Примеры**:

```python
# Пример вызова функции render_header:
ws = Spreadsheet('id_таблицы').worksheet('Лист1')
grender.render_header(ws, 'Заголовок таблицы')
```

### `merge_range`

**Назначение**: Объединяет ячейки в таблице.

**Параметры**:

- `ws` (Worksheet): Таблица в книге.
- `range` (str): Диапазон ячеек.
- `merge_type` (str('MERGE_ALL') | str('MERGE_COLUMNS') | str('MERGE_ROWS') = 'MERGE_ALL'): Тип объединения ячеек.

**Возвращает**:

- `None`: Не возвращает значения.

**Как работает функция**:

- Функция `merge_range` объединяет ячейки в заданном диапазоне в соответствии с указанным типом объединения. 

**Примеры**:

```python
# Пример вызова функции merge_range:
ws = Spreadsheet('id_таблицы').worksheet('Лист1')
grender.merge_range(ws, 'A1:C1', 'MERGE_COLUMNS')
```

### `set_worksheet_direction`

**Назначение**: Задает направление текста в таблице.

**Параметры**:

- `sh` (Spreadsheet): Книга Google Spreadsheets.
- `ws` (Worksheet): Таблица в книге.
- `direction` (str ('ltr') | str ('rtl') = 'rtl'): Направление текста.

**Возвращает**:

- `None`: Не возвращает значения.

**Как работает функция**:

- Функция `set_worksheet_direction` устанавливает направление текста в таблице Google Spreadsheets. Она использует метод `batch_update` для обновления свойств таблицы.

**Примеры**:

```python
# Пример вызова функции set_worksheet_direction:
sh = Spreadsheet('id_таблицы')
ws = sh.worksheet('Лист1')
grender.set_worksheet_direction(sh, ws, 'rtl')
```

### `header`

**Назначение**: Добавляет заголовок в таблицу.

**Параметры**:

- `ws` (Worksheet): Таблица в книге.
- `ws_header` (str | list): Заголовок таблицы.
- `row` (int = None): Номер строки, в которую добавляется заголовок.

**Возвращает**:

- `None`: Не возвращает значения.

**Как работает функция**:

- Функция `header` добавляет заголовок в таблицу Google Spreadsheets. Она определяет диапазон ячеек для заголовка и объединяет ячейки в соответствии с указанным типом объединения.

**Примеры**:

```python
# Пример вызова функции header:
ws = Spreadsheet('id_таблицы').worksheet('Лист1')
grender.header(ws, 'Заголовок таблицы')
```

### `write_category_title`

**Назначение**: Добавляет заголовок категории в таблицу.

**Параметры**:

- `ws` (Worksheet): Таблица в книге.
- `ws_category_title` (str | list): Заголовок категории.
- `row` (int = None): Номер строки, в которую добавляется заголовок.

**Возвращает**:

- `None`: Не возвращает значения.

**Как работает функция**:

- Функция `write_category_title` добавляет заголовок категории в таблицу Google Spreadsheets. Она определяет диапазон ячеек для заголовка и объединяет ячейки.

**Примеры**:

```python
# Пример вызова функции write_category_title:
ws = Spreadsheet('id_таблицы').worksheet('Лист1')
grender.write_category_title(ws, 'Категория')
```

### `get_first_empty_row`

**Назначение**: Возвращает номер первой пустой строки в таблице.

**Параметры**:

- `ws` (Worksheet): Таблица в книге.
- `by_col` (int = None): Номер столбца, по которому считать (если `by_col` равно `None`, то по последнему заполненному столбцу).

**Возвращает**:

- `int`: Номер первой пустой строки.

**Как работает функция**:

- Функция `get_first_empty_row` определяет номер первой пустой строки в таблице Google Spreadsheets. Она использует методы `col_values` и `get_all_values` для определения заполненных ячеек в таблице.

**Примеры**:

```python
# Пример вызова функции get_first_empty_row:
ws = Spreadsheet('id_таблицы').worksheet('Лист1')
row_number = grender.get_first_empty_row(ws)
```

## Параметры класса

- `render_schemas`: Словарь с схемами рендеринга.

## Примеры

```python
# Создание инстанса класса GSRender:
grender = GSRender()

# Получение таблицы Google Spreadsheets:
ws = Spreadsheet('id_таблицы').worksheet('Лист1')

# Добавление заголовка в таблицу:
grender.header(ws, 'Заголовок таблицы')

# Объединение ячеек в диапазоне A1:C1:
grender.merge_range(ws, 'A1:C1', 'MERGE_COLUMNS')

# Установка направления текста в таблице на RTL:
grender.set_worksheet_direction(Spreadsheet('id_таблицы'), ws, 'rtl')
```
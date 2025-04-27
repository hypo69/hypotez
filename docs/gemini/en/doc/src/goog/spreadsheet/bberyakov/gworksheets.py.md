# Модуль GWorksheet

## Обзор

Модуль `src.goog.spreadsheet.bberyakov.gworksheets`  предназначен для работы с Google Таблицами (Google Sheets) через API Google Sheets. Модуль использует библиотеки `gspread` и `oauth2client` для взаимодействия с Google Sheets.

## Подробности

Модуль  `src.goog.spreadsheet.bberyakov.gworksheets`  предоставляет класс `GWorksheet`, который позволяет выполнять следующие операции:

- Создание новых таблиц (worksheet) в Google Таблицах
- Открытие существующих таблиц
- Очистка данных в таблице
- Установка направления текста в ячейках
- Запись заголовка таблицы (header) 
- Запись заголовка категории 


## Классы

### `GWorksheet`

**Описание**: Класс `GWorksheet` - это обертка над классом `Worksheet` из библиотеки `gspread`. Он  позволяет создавать, открывать, очищать и управлять таблицами Google Sheets.

**Inherits**:
- `Worksheet`

**Attributes**:
- `sh` (`None`):  Ссылка на объект Google Sheets.
- `ws` (`Worksheet`):  Объект, представляющий таблицу (worksheet).
- `render` (`GSRender`):  Объект `GSRender`, который используется для форматирования и записи данных в таблицу.

**Methods**:

#### `__init__(self, sh, ws_title: str = 'new', rows = None, cols = None, direcion = 'rtl', wipe_if_exist: bool = True, *args, **kwargs) -> None`

**Описание**:  Инициализирует объект `GWorksheet`.  

**Parameters**:
- `self`:  Ссылка на текущий объект `GWorksheet`.
- `sh`:  Объект Google Sheets.
- `ws_title` (`str`, optional):  Название таблицы (worksheet). По умолчанию `'new'`.
- `rows` (`int`, optional):  Количество строк. По умолчанию `None`.
- `cols` (`int`, optional):  Количество столбцов. По умолчанию `None`.
- `direcion` (`str`, optional):  Направление текста. По умолчанию `'rtl'`.
- `wipe_if_exist` (`bool`, optional):  Удалить старые данные, если таблица с таким названием уже существует. По умолчанию `True`.
- `*args`:  Дополнительные аргументы.
- `**kwargs`:  Дополнительные ключевые слова.

**Returns**: 
- `None`

**Examples**:
```python
from src.goog.spreadsheet.bberyakov.gworksheets import GWorksheet
from src.goog.spreadsheet.bberyakov.gspreadsheet import GSpreadsheet
from src.goog.spreadsheet.bberyakov.gsheet import GSheet
from src.logger import logger

gspreadsheet = GSpreadsheet()
gsheet = GSheet(gspreadsheet)
sh = gsheet.get_spreadsheet()
gworksheet = GWorksheet(sh, ws_title='New_Worksheet')
```

#### `get(self, sh, ws_title: str = 'new', rows: int = 100, cols: int = 100, direction: str = 'rtl', wipe_if_exist: bool = True)`

**Описание**:  Создает новую таблицу или открывает существующую. 

**Parameters**:
- `self`:  Ссылка на текущий объект `GWorksheet`.
- `sh`:  Объект Google Sheets.
- `ws_title` (`str`, optional):  Название таблицы (worksheet). По умолчанию `'new'`.
- `rows` (`int`, optional):  Количество строк. По умолчанию `100`.
- `cols` (`int`, optional):  Количество столбцов. По умолчанию `100`.
- `direction` (`str`, optional):  Направление текста. По умолчанию `'rtl'`.
- `wipe_if_exist` (`bool`, optional):  Удалить старые данные, если таблица с таким названием уже существует. По умолчанию `True`.

**Returns**:
- `None`

**How the Function Works**:
- Если `ws_title` равен `'new'`,  функция добавляет новую таблицу в Google Sheets.
- Если `ws_title` не равен `'new'`,  функция пытается открыть существующую таблицу с данным названием.
- Если таблица с указанным именем уже существует и `wipe_if_exist` равно `True`,  функция очищает таблицу от старых данных.
- Если таблица с указанным именем не существует, функция создает новую таблицу с указанным названием.
- Функция устанавливает направление текста в таблице с помощью `self.render.set_worksheet_direction`.

**Examples**:
```python
from src.goog.spreadsheet.bberyakov.gworksheets import GWorksheet
from src.goog.spreadsheet.bberyakov.gspreadsheet import GSpreadsheet
from src.goog.spreadsheet.bberyakov.gsheet import GSheet
from src.logger import logger

gspreadsheet = GSpreadsheet()
gsheet = GSheet(gspreadsheet)
sh = gsheet.get_spreadsheet()
gworksheet = GWorksheet(sh, ws_title='New_Worksheet')
gworksheet.get(sh, ws_title='Existing_Worksheet')
```

#### `header(self, world_title: str, range: str = 'A1:Z1', merge_type: str('MERGE_ALL') | str('MERGE_COLUMNS') | str('MERGE_ROWS') = 'MERGE_ALL') -> None`

**Описание**:  Записывает заголовок таблицы.

**Parameters**:
- `self`:  Ссылка на текущий объект `GWorksheet`.
- `world_title` (`str`):  Заголовок таблицы.
- `range` (`str`, optional):  Диапазон ячеек для заголовка. По умолчанию `'A1:Z1'`.
- `merge_type` (`str('MERGE_ALL') | str('MERGE_COLUMNS') | str('MERGE_ROWS')`, optional):  Тип слияния ячеек для заголовка. По умолчанию `'MERGE_ALL'`.

**Returns**: 
- `None`

**How the Function Works**:
- Функция использует `self.render.header` для записи заголовка таблицы.
- Параметры `world_title`, `range` и `merge_type` передаются в `self.render.header` для форматирования заголовка.

**Examples**:
```python
from src.goog.spreadsheet.bberyakov.gworksheets import GWorksheet
from src.goog.spreadsheet.bberyakov.gspreadsheet import GSpreadsheet
from src.goog.spreadsheet.bberyakov.gsheet import GSheet
from src.logger import logger

gspreadsheet = GSpreadsheet()
gsheet = GSheet(gspreadsheet)
sh = gsheet.get_spreadsheet()
gworksheet = GWorksheet(sh, ws_title='New_Worksheet')
gworksheet.header(world_title='Заголовок таблицы')
```

#### `category(self, ws_category_title)`

**Описание**:  Записывает заголовок категории.

**Parameters**:
- `self`:  Ссылка на текущий объект `GWorksheet`.
- `ws_category_title` (`str`):  Заголовок категории.

**Returns**: 
- `None`

**How the Function Works**:
- Функция использует `self.render.write_category_title` для записи заголовка категории.
- Параметр `ws_category_title` передается в `self.render.write_category_title` для форматирования заголовка категории.

**Examples**:
```python
from src.goog.spreadsheet.bberyakov.gworksheets import GWorksheet
from src.goog.spreadsheet.bberyakov.gspreadsheet import GSpreadsheet
from src.goog.spreadsheet.bberyakov.gsheet import GSheet
from src.logger import logger

gspreadsheet = GSpreadsheet()
gsheet = GSheet(gspreadsheet)
sh = gsheet.get_spreadsheet()
gworksheet = GWorksheet(sh, ws_title='New_Worksheet')
gworksheet.category(ws_category_title='Категория')
```

#### `direction(self, direction: str = 'rtl')`

**Описание**:  Устанавливает направление текста в таблице.

**Parameters**:
- `self`:  Ссылка на текущий объект `GWorksheet`.
- `direction` (`str`, optional):  Направление текста. По умолчанию `'rtl'`.

**Returns**: 
- `None`

**How the Function Works**:
- Функция использует `self.render.set_worksheet_direction` для установки направления текста в таблице.
- Параметр `direction` передается в `self.render.set_worksheet_direction` для определения направления текста.

**Examples**:
```python
from src.goog.spreadsheet.bberyakov.gworksheets import GWorksheet
from src.goog.spreadsheet.bberyakov.gspreadsheet import GSpreadsheet
from src.goog.spreadsheet.bberyakov.gsheet import GSheet
from src.logger import logger

gspreadsheet = GSpreadsheet()
gsheet = GSheet(gspreadsheet)
sh = gsheet.get_spreadsheet()
gworksheet = GWorksheet(sh, ws_title='New_Worksheet')
gworksheet.direction(direction='ltr')
```
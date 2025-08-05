# Модуль `src.goog.spreadsheet.spreadsheet`

## Обзор

Модуль `src.goog.spreadsheet.spreadsheet` предоставляет базовые функции для работы с Google Sheets. Модуль содержит класс `SpreadSheet`, который позволяет выполнять операции по доступу к Google Sheets API, создавать и управлять электронными таблицами, а также загружать данные из CSV-файла в Google Sheets.

## Подробнее

Модуль использует библиотеку `gspread` для взаимодействия с Google Sheets API. Библиотека `gspread` предоставляет удобный способ для чтения, записи и обновления данных в электронных таблицах Google Sheets.

Модуль предназначен для упрощения процесса работы с Google Sheets. Он позволяет разработчикам легко создавать и управлять электронными таблицами, а также загружать данные из различных источников.

## Классы

### `SpreadSheet`

**Описание**: Класс для работы с Google Sheets.

**Наследует**:

**Атрибуты**:

- `spreadsheet_id` (str | None): Идентификатор электронных таблиц Google Sheets. Укажите None для создания новой электронной таблицы.
- `spreadsheet_name` (str | None): Имя новой электронной таблицы, если `spreadsheet_id` не указан.
- `spreadsheet` (Spreadsheet): Объект, представляющий электронную таблицу Google Sheets.
- `data_file` (Path): Путь к CSV-файлу.
- `sheet_name` (str): Имя листа в Google Sheets.
- `credentials` (ServiceAccountCredentials): Объект, представляющий учетные данные для доступа к Google Sheets.
- `client` (gspread.Client): Объект, представляющий клиента для Google Sheets API.
- `worksheet` (Worksheet): Объект, представляющий лист в Google Sheets.
- `create_sheet` (bool): Флаг, определяющий, нужно ли создавать новый лист, если его нет.

**Методы**:

- `__init__(self, spreadsheet_id: str, *args, **kwargs)`: Инициализация GoogleSheetHandler с указанными учетными данными и файлом данных.
- `_create_credentials(self)`: Создание учетных данных из JSON-файла.
- `_authorize_client(self)`: Авторизация клиента для доступа к Google Sheets API.
- `get_worksheet(self, worksheet_name: str | Worksheet) -> Worksheet | None`: Получение листа по имени.
- `create_worksheet(self, title: str, dim: dict = {'rows': 100, 'cols': 10}) -> Worksheet | None`: Функция создает новую страницу с именем `title` и размерностью `dim`.
- `copy_worksheet(self, from_worksheet: str, to_worksheet: str)`: Копирование листа по имени.
- `upload_data_to_sheet(self)`: Загрузка данных из CSV-файла в Google Sheets.

**Принцип работы**:

Класс `SpreadSheet` обеспечивает интерфейс для работы с Google Sheets. Он позволяет создавать новые электронные таблицы, получать существующие электронные таблицы по идентификатору, получать листы по имени, создавать новые листы, копировать существующие листы и загружать данные из CSV-файла.

### `_create_credentials(self)`

**Назначение**: Создание учетных данных из JSON-файла.

**Параметры**:

**Возвращает**:

- `credentials`: Объект, представляющий учетные данные для доступа к Google Sheets.

**Вызывает исключения**:

**Как работает функция**:

Функция `_create_credentials` создает учетные данные для доступа к Google Sheets API на основе файла ключа. Она считывает файл ключа, содержащий необходимые данные для авторизации, и возвращает объект `credentials`.

### `_authorize_client(self)`

**Назначение**: Авторизация клиента для доступа к Google Sheets API.

**Параметры**:

**Возвращает**:

- `client`: Объект, представляющий клиента для Google Sheets API.

**Вызывает исключения**:

**Как работает функция**:

Функция `_authorize_client` создает и авторизует клиента для Google Sheets API на основе предоставленных учетных данных. Она использует полученные учетные данные для получения разрешения от Google Sheets API и возвращает объект `client`, который можно использовать для работы с электронными таблицами.

### `get_worksheet(self, worksheet_name: str | Worksheet) -> Worksheet | None`

**Назначение**: Получение листа по имени.

**Параметры**:

- `worksheet_name`: Имя листа в Google Sheets.

**Возвращает**:

- `Worksheet`: Объект, представляющий лист.

**Вызывает исключения**:

- `gspread.exceptions.WorksheetNotFound`: Если лист с указанным именем не найден.

**Как работает функция**:

Функция `get_worksheet` получает лист по имени. Она пытается найти лист с указанным именем в электронной таблице. Если лист не найден, функция вызывает исключение `gspread.exceptions.WorksheetNotFound`.

### `create_worksheet(self, title: str, dim: dict = {'rows': 100, 'cols': 10}) -> Worksheet | None`

**Назначение**: Создание нового листа с именем `title` и размерностью `dim`.

**Параметры**:

- `title`: Имя нового листа.
- `dim`: Словарь, определяющий размерность нового листа.

**Возвращает**:

- `Worksheet`: Объект, представляющий новый лист.

**Вызывает исключения**:

**Как работает функция**:

Функция `create_worksheet` создает новый лист с указанным именем и размерностью. Она использует метод `add_worksheet` класса `Spreadsheet` для создания нового листа и возвращает объект `Worksheet`.

### `copy_worksheet(self, from_worksheet: str, to_worksheet: str)`

**Назначение**: Копирование листа по имени.

**Параметры**:

- `from_worksheet`: Имя листа, который нужно скопировать.
- `to_worksheet`: Имя нового листа.

**Возвращает**:

- `Worksheet`: Объект, представляющий новый лист.

**Вызывает исключения**:

**Как работает функция**:

Функция `copy_worksheet` копирует лист по имени. Она использует метод `duplicate` класса `Worksheet` для создания копии листа и возвращает объект `Worksheet`, представляющий новый лист.

### `upload_data_to_sheet(self)`

**Назначение**: Загрузка данных из CSV-файла в Google Sheets.

**Параметры**:

**Возвращает**:

**Вызывает исключения**:

- `ValueError`: Если путь к файлу данных не задан или файл не существует.

**Как работает функция**:

Функция `upload_data_to_sheet` загружает данные из CSV-файла в Google Sheets. Она считывает данные из CSV-файла, используя библиотеку `pandas`, преобразует данные в формат, подходящий для записи в Google Sheets, и записывает данные в лист.

## Параметры класса

- `spreadsheet_id` (str | None): Идентификатор электронных таблиц Google Sheets. Укажите None для создания новой электронной таблицы.
- `spreadsheet_name` (str | None): Имя новой электронной таблицы, если `spreadsheet_id` не указан.
- `data_file` (Path): Путь к CSV-файлу.
- `sheet_name` (str): Имя листа в Google Sheets.

## Примеры

**Пример 1: Создание новой электронной таблицы и загрузка данных в нее**:

```python
from pathlib import Path

data_file = Path('/mnt/data/google_extracted/your_data_file.csv')  # Replace with actual data file
sheet_name = 'Sheet1'  # Replace with actual sheet name in Google Sheets

# Create a new Spreadsheet
google_sheet_handler = SpreadSheet(
    spreadsheet_id=None,  # Specify None to create a new Spreadsheet
    sheet_name=sheet_name,
    spreadsheet_name='My New Spreadsheet'  # Name of the new Spreadsheet if spreadsheet_id is not specified
)
google_sheet_handler.upload_data_to_sheet()
```

**Пример 2: Загрузка данных в существующую электронную таблицу**:

```python
from pathlib import Path

spreadsheet_id = 'your_spreadsheet_id'  # Replace with actual spreadsheet ID
sheet_name = 'Sheet1'  # Replace with actual sheet name in Google Sheets
data_file = Path('/mnt/data/google_extracted/your_data_file.csv')  # Replace with actual data file

google_sheet_handler = SpreadSheet(
    spreadsheet_id=spreadsheet_id,
    sheet_name=sheet_name
)
google_sheet_handler.upload_data_to_sheet()
```

**Пример 3: Получение и обновление данных на листе**:

```python
from pathlib import Path

spreadsheet_id = 'your_spreadsheet_id'  # Replace with actual spreadsheet ID
sheet_name = 'Sheet1'  # Replace with actual sheet name in Google Sheets

google_sheet_handler = SpreadSheet(
    spreadsheet_id=spreadsheet_id,
    sheet_name=sheet_name
)

worksheet = google_sheet_handler.get_worksheet(sheet_name)

# Read data from the worksheet
data = worksheet.get_all_values()

# Update data on the worksheet
worksheet.update('A1', [
    ['Name', 'Age'],
    ['John Doe', 30],
    ['Jane Doe', 25]
])
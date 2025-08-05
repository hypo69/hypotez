# Модуль для работы с Google Sheets
## Обзор

Модуль предоставляет класс `SpreadSheet` для работы с Google Sheets. Он обеспечивает базовые методы для доступа к API Google Sheets, создания и управления таблицами, а также загрузки данных из CSV-файлов в Google Sheets.

## Подробнее

Модуль `src.goog.spreadsheet` предназначен для упрощения взаимодействия с Google Sheets. Он предоставляет класс `SpreadSheet`, который инкапсулирует основные операции, такие как создание, открытие, копирование и загрузка данных в таблицы Google Sheets. Модуль использует библиотеки `gspread`, `oauth2client` и `pandas` для аутентификации, доступа к API и обработки данных.

## Классы

### `SpreadSheet`

**Описание**: Класс для работы с Google Sheets.

**Атрибуты**:
- `spreadsheet_id` (str | None): ID таблицы Google Sheets. Если указан `None`, создается новая таблица.
- `spreadsheet_name` (str | None): Имя новой таблицы Google Sheets, если `spreadsheet_id` не указан.
- `spreadsheet` (Spreadsheet): Объект таблицы Google Sheets.
- `data_file` (Path): Путь к файлу с данными.
- `sheet_name` (str): Имя листа в таблице Google Sheets.
- `credentials` (ServiceAccountCredentials): Учетные данные для доступа к Google Sheets.
- `client` (gspread.Client): Клиент для взаимодействия с API Google Sheets.
- `worksheet` (Worksheet): Объект листа в таблице Google Sheets.
- `create_sheet` (bool): Флаг, указывающий, нужно ли создавать новый лист, если он не существует.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `SpreadSheet`.
- `_create_credentials()`: Создает учетные данные для доступа к Google Sheets API.
- `_authorize_client()`: Авторизует клиента для доступа к Google Sheets API.
- `get_worksheet()`: Получает лист из таблицы по имени.
- `create_worksheet()`: Создает новый лист в таблице.
- `copy_worksheet()`: Копирует лист в таблице.
- `upload_data_to_sheet()`: Загружает данные из CSV-файла в Google Sheets.

### `__init__`
```python
    def __init__(self, 
                 spreadsheet_id: str, *args, **kwargs):
        """ Инициализирует GoogleSheetHandler с указанными учетными данными и файлом данных.
        
        Args:
            spreadsheet_id (str): ID таблицы Google Sheets. Укажите None, чтобы создать новую таблицу.
        """
```
- **Назначение**: Инициализирует класс `SpreadSheet` с указанным ID таблицы, учетными данными и файлом данных.
- **Параметры**:
    - `spreadsheet_id` (str): ID таблицы Google Sheets. Если указан `None`, создается новая таблица.
- **Как работает функция**:
    1. Сохраняет `spreadsheet_id` в атрибуте экземпляра класса.
    2. Вызывает `_create_credentials` для создания учетных данных.
    3. Вызывает `_authorize_client` для авторизации клиента.
    4. Пытается открыть существующую таблицу по ID.
    5. Если таблица не найдена, регистрирует ошибку и вызывает исключение `gspread.exceptions.SpreadsheetNotFound`.

### `_create_credentials`
```python
    def _create_credentials(self):
        """ Создает учетные данные из JSON файла.

        Создает учетные данные для доступа к Google Sheets API на основе файла ключа.
        Returns:
            Credentials: Учетные данные для доступа к Google Sheets.
        """
```
- **Назначение**: Создает учетные данные для доступа к Google Sheets API на основе файла ключа.
- **Возвращает**:
    - `ServiceAccountCredentials`: Учетные данные для доступа к Google Sheets.
- **Как работает функция**:
    1. Определяет путь к файлу учетных данных. Файл `e-cat-346312-137284f4419e.json` расположен в директории `gs.path.secrets`.
    2. Определяет область доступа (SCOPES) для Google Sheets API и Google Drive API.
    3. Создает учетные данные с использованием `ServiceAccountCredentials.from_json_keyfile_name`.
    4. Логирует успешное создание учетных данных.
    5. Возвращает созданные учетные данные.
    6. В случае ошибки логирует ошибку и вызывает исключение.

### `_authorize_client`
```python
    def _authorize_client(self):
        """ Авторизует клиента для доступа к Google Sheets API.

        Создает и авторизует клиента для Google Sheets API на основе предоставленных учетных данных.
        Returns:
            Client: Авторизованный клиент для работы с Google Sheets.
        """
```
- **Назначение**: Авторизует клиента для доступа к Google Sheets API.
- **Возвращает**:
    - `gspread.Client`: Авторизованный клиент для работы с Google Sheets.
- **Как работает функция**:
    1. Авторизует клиента с использованием `gspread.authorize`.
    2. Логирует успешную авторизацию клиента.
    3. Возвращает авторизованного клиента.
    4. В случае ошибки логирует ошибку и вызывает исключение.

### `get_worksheet`
```python
    def get_worksheet(self, worksheet_name: str | Worksheet) -> Worksheet | None:
        """ Получает страницу по имени.

        Если страница с указанным именем не существует и флаг `create_if_not_present` установлен в True, создается новая страница.

        Args:
            worksheet (str | Worksheet): Имя листа в Google Sheets.
        Returns:
            Worksheet | None: Рабочий лист для работы с данными.
        """
```
- **Назначение**: Получает лист из таблицы по имени. Если лист не существует, он будет создан.
- **Параметры**:
    - `worksheet_name` (str | Worksheet): Имя листа в Google Sheets.
- **Возвращает**:
    - `Worksheet | None`: Объект листа для работы с данными.
- **Как работает функция**:
    1. Пытается получить лист из таблицы по имени.
    2. Если лист не найден, создает новый лист с указанным именем.
    3. Возвращает объект листа.

### `create_worksheet`
```python
    def create_worksheet(self, title:str, dim:dict = {'rows':100,'cols':10}) -> Worksheet | None:
        """ функция создает новую страницу с именем `title` и размерностью `dim`"""
```
- **Назначение**: Создает новую страницу с указанным именем и размерностью.
- **Параметры**:
    - `title` (str): Имя создаваемой страницы.
    - `dim` (dict): Размеры создаваемой страницы (количество строк и столбцов). По умолчанию `{'rows': 100, 'cols': 10}`.
- **Возвращает**:
    - `Worksheet | None`: Объект созданной страницы или `None` в случае ошибки.
- **Как работает функция**:
    1. Пытается создать новую страницу с указанным именем и размерами.
    2. Возвращает объект созданной страницы.
    3. В случае ошибки логирует ошибку.

### `copy_worksheet`
```python
    def copy_worksheet(self, from_worksheet: str, to_worksheet: str):
        """ Копирует страницу по имени."""
```
- **Назначение**: Копирует страницу из одной таблицы в другую.
- **Параметры**:
    - `from_worksheet` (str): Имя копируемой страницы.
    - `to_worksheet` (str): Имя новой страницы.
- **Как работает функция**:
    1. Получает страницу с именем `from_worksheet`.
    2. Создает копию страницы с именем `to_worksheet`.
    3. Возвращает объект созданной страницы.

### `upload_data_to_sheet`
```python
    def upload_data_to_sheet(self):
        """ Загружает данные из CSV файла в Google Sheets.

        Загружает данные из CSV файла, указанного в `self.data_file`, на указанный лист в Google Sheets.
        """
```
- **Назначение**: Загружает данные из CSV-файла в Google Sheets.
- **Как работает функция**:
    1. Проверяет, установлен ли путь к файлу данных и существует ли файл.
    2. Читает данные из CSV-файла с использованием `pandas.read_csv`.
    3. Подготавливает данные для записи в Google Sheets.
    4. Записывает данные в Google Sheets.
    5. Логирует успешную загрузку данных.
    6. В случае ошибки логирует ошибку и вызывает исключение.

## Примеры

### Использование класса
```python
if __name__ == "__main__":
    from pathlib import Path

    data_file = Path('/mnt/data/google_extracted/your_data_file.csv')  # Замените на фактический файл данных
    sheet_name = 'Sheet1'  # Замените на фактическое имя листа в Google Sheets

    # Создание новой таблицы, если spreadsheet_id не указан
    google_sheet_handler = SpreadSheet(
        spreadsheet_id=None,  # Укажите None, чтобы создать новую таблицу
        sheet_name=sheet_name,
        spreadsheet_name='My New Spreadsheet'  # Имя новой таблицы, если spreadsheet_id не указан
    )
    google_sheet_handler.upload_data_to_sheet()
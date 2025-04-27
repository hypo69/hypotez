## Как использовать этот блок кода
=========================================================================================

### Описание
-------------------------
Этот блок кода представляет собой класс `SpreadSheet`, который предоставляет функциональность для работы с Google Sheets. Он позволяет создавать новые таблицы, открывать существующие, загружать данные из CSV-файла, создавать новые листы и т. д. 

### Шаги выполнения
-------------------------
1. **Инициализация класса `SpreadSheet`**: Создайте объект класса `SpreadSheet`, передав в конструктор ID Google Sheets таблицы. Если ID не задан, будет создана новая таблица.
2. **Авторизация**: Класс использует `gspread` и `oauth2client` для авторизации доступа к API Google Sheets. Credentials для авторизации хранятся в файле `secrets/e-cat-346312-137284f4419e.json`.
3. **Работа с таблицей**:  Класс предоставляет различные методы для работы с таблицей:
    - `get_worksheet(worksheet_name: str | Worksheet) -> Worksheet | None` - получить лист по имени
    - `create_worksheet(title:str, dim:dict = {\'rows\':100,\'cols\':10}) -> Worksheet | None` - создать новый лист
    - `copy_worksheet(from_worksheet: str, to_worksheet: str)` - скопировать лист
    - `upload_data_to_sheet()` - загрузить данные из CSV-файла на Google Sheets
4. **Загрузка данных**:  Метод `upload_data_to_sheet()` считывает данные из заданного CSV-файла (`self.data_file`) и загружает их в Google Sheets.

### Пример использования
-------------------------

```python
    from pathlib import Path

    data_file = Path('/mnt/data/google_extracted/your_data_file.csv')  # Replace with actual data file
    sheet_name = 'Sheet1'  # Replace with actual sheet name in Google Sheets

    # Create a new Spreadsheet if spreadsheet_id is not specified
    google_sheet_handler = SpreadSheet(
        spreadsheet_id=None,  # Specify None to create a new Spreadsheet
        sheet_name=sheet_name,
        spreadsheet_name='My New Spreadsheet'  # Name of the new Spreadsheet if spreadsheet_id is not specified
    )
    google_sheet_handler.upload_data_to_sheet()
```

В этом примере создается новый Google Sheets документ с именем "My New Spreadsheet" и в него загружаются данные из CSV-файла.

### Дополнительные пояснения
-------------------------
- Класс использует `logger` для записи ошибок и событий.
- Файл с credentials должен быть доступен.
- Для использования этого кода необходимо установить библиотеки `gspread` и `oauth2client`.
- `gs.path` - это объект, который предоставляет доступ к файлам и директориям проекта.
- `pprint` - это функция для форматирования вывода.
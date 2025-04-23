### **Как использовать этот блок кода**
=========================================================================================

Описание
-------------------------
Этот код предназначен для работы с Google Sheets. Он предоставляет класс `SpreadSheet`, который позволяет подключаться к Google Sheets API, создавать новые таблицы, управлять листами и загружать данные из CSV-файлов в Google Sheets.

Шаги выполнения
-------------------------
1. **Инициализация класса `SpreadSheet`**:
   - Создание экземпляра класса `SpreadSheet` с указанием `spreadsheet_id`. Если `spreadsheet_id` указан как `None`, будет создана новая таблица.
   - Создание учетных данных для доступа к Google Sheets API.
   - Авторизация клиента с использованием учетных данных.

2. **Получение доступа к листу**:
   - Использование метода `get_worksheet` для получения доступа к конкретному листу в Google Sheets по его имени.
   - Если лист не существует, он будет создан с использованием метода `create_worksheet`.

3. **Загрузка данных из CSV в Google Sheets**:
   - Использование метода `upload_data_to_sheet` для загрузки данных из CSV-файла в Google Sheets.
   - Чтение данных из CSV-файла с использованием `pandas`.
   - Подготовка данных для записи в Google Sheets.
   - Запись данных в Google Sheets с использованием метода `update`.

Пример использования
-------------------------

```python
from pathlib import Path
from src.goog.spreadsheet.spreadsheet import SpreadSheet

# Путь к CSV-файлу с данными
data_file = Path('/mnt/data/google_extracted/your_data_file.csv')  # Замените на актуальный путь к вашему файлу

# ID существующей Google Sheets таблицы (или None для создания новой)
spreadsheet_id = 'your_spreadsheet_id'  # Замените на ID вашей таблицы или укажите None

# Название листа в Google Sheets
sheet_name = 'Sheet1'

# Создание экземпляра класса SpreadSheet
google_sheet_handler = SpreadSheet(
    spreadsheet_id=spreadsheet_id
)

# Получение доступа к листу
worksheet = google_sheet_handler.get_worksheet(sheet_name)

# Загрузка данных из CSV-файла в Google Sheets
google_sheet_handler.data_file = data_file  # Установка пути к файлу с данными
google_sheet_handler.worksheet = worksheet  # Установка объекта worksheet
google_sheet_handler.upload_data_to_sheet()
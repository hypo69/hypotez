## Как использовать класс ReachSpreadsheet
=========================================================================================

Описание
-------------------------
Класс `ReachSpreadsheet` предоставляет интерфейс для работы с Google Sheets API v4 и Google Drive API v3. С помощью этого класса вы можете создавать новые таблицы, делиться ими, добавлять новые листы, устанавливать размеры столбцов и строк, а также добавлять данные и форматировать ячейки.

Шаги выполнения
-------------------------
1. **Создание экземпляра класса ReachSpreadsheet.**
   - Инициализируйте объект `ReachSpreadsheet` с необязательным параметром `debugMode`.
   - Параметр `debugMode`  включает режим отладки, который печатает дополнительные данные о запросах и ответах API в консоль.
2. **Создание новой таблицы.**
   - Используйте метод `create()` для создания новой таблицы.
   - Укажите название таблицы (`title`), название листа (`sheetTitle`), количество строк (`rows`), количество столбцов (`cols`), региональные настройки (`locale`) и часовой пояс (`timeZone`).
3. **Делитесь таблицей.**
   - Используйте методы `shareWithEmailForReading()`, `shareWithEmailForWriting()`, `shareWithAnybodyForReading()` или `shareWithAnybodyForWriting()` для предоставления доступа к таблице другим пользователям.
   - Для методов `shareWithEmailForReading()` и `shareWithEmailForWriting()` укажите адрес электронной почты пользователя.
4. **Добавляйте новые листы.**
   - Используйте метод `addSheet()` для добавления нового листа к существующей таблице.
   - Укажите название листа (`sheetTitle`), количество строк (`rows`) и количество столбцов (`cols`).
5. **Устанавливайте размеры столбцов и строк.**
   - Используйте методы `prepare_setColumnWidth()`, `prepare_setColumnsWidth()`, `prepare_setRowHeight()` и `prepare_setRowsHeight()` для настройки ширины столбцов и высоты строк.
6. **Добавляйте данные и форматируйте ячейки.**
   - Используйте метод `prepare_setValues()` для добавления данных в таблицу.
   - Используйте методы `prepare_mergeCells()`, `prepare_setCellStringFormatterormat()` и `prepare_setCellStringFormatterormats()` для форматирования ячеек.
7. **Выполнение запросов к API.**
   - После выполнения всех необходимых операций вызовите метод `runPrepared()` для отправки запросов к API и получения результатов.

Пример использования
-------------------------

```python
from src.goog.spreadsheet.reach_spreadsheet import ReachSpreadsheet
from src.utils.printer import pprint

# Создание экземпляра класса ReachSpreadsheet
ss = ReachSpreadsheet(debugMode=True)

# Создание новой таблицы
ss.create("Моя таблица", "Лист 1", rows=10, cols=5)

# Делитесь таблицей с пользователем по электронной почте
ss.shareWithEmailForWriting("volkov.ioann@gmail.com")

# Добавление нового листа
ss.addSheet("Лист 2", rows=5, cols=3)

# Установка ширины столбца
ss.prepare_setColumnWidth(0, 200)  # Устанавливает ширину первого столбца на 200 пикселей

# Добавление данных в таблицу
ss.prepare_setValues("A1:B2", [["Имя", "Возраст"], ["Иван", 30]])

# Выполнение запросов к API
results = ss.runPrepared()

# Получение URL таблицы
sheet_url = ss.getSheetURL()

pprint(sheet_url)
```

Дополнительные сведения
-------------------------

- Для работы с классом `ReachSpreadsheet` необходимо иметь учетные данные Google Cloud Platform (GCP) и разрешения на доступ к Google Sheets API v4.
- Класс `ReachSpreadsheet` обеспечивает только базовые функции для работы с Google Sheets.
- Для получения более подробной информации о Google Sheets API v4 обратитесь к [официальной документации](https://developers.google.com/sheets/api/reference/rest).
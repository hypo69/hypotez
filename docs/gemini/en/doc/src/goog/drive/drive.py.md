# Модуль `src.goog.drive.drive.py`

## Обзор

Модуль `src.goog.drive.drive.py` предоставляет функциональность для работы с Google Drive. В нем реализован класс `GoogleDriveHandler`, который позволяет загружать файлы на Google Drive.

## Детали

Модуль использует Google Drive API v3 для взаимодействия с Google Drive.  Он использует авторизацию OAuth 2.0 для доступа к аккаунту пользователя.  Класс `GoogleDriveHandler` предоставляет методы для создания учетных данных, загрузки файлов и других операций с Google Drive.

## Классы

### `class GoogleDriveHandler`

**Описание**: Класс `GoogleDriveHandler` предоставляет функциональность для работы с Google Drive.

**Атрибуты**:

- `folder_name` (str): Имя папки на Google Drive, куда будут загружаться файлы.
- `creds` (google.oauth2.credentials.Credentials): Объект учетных данных Google Drive.

**Методы**:

- `__init__(self, folder_name: str)`: Инициализирует экземпляр класса `GoogleDriveHandler` с указанным именем папки.
- `_create_credentials(self)`: Создает или обновляет учетные данные пользователя Google Drive.
- `upload_file(self, file_path: Path)`: Загружает указанный файл на Google Drive в папку `folder_name`.

## Функции

### `main()`: 

**Цель**:  Демонстрирует основное использование API Google Drive v3.

**Параметры**:  Нет

**Возвращаемое значение**:  Нет

**Примеры**: 
```python
if __name__ == '__main__':
    main()
```
**Как работает функция**: 
- Функция `main()` создает объект `GoogleDriveHandler` и вызывает метод `_create_credentials()` для получения учетных данных.
- Затем создается объект `service` с помощью `build('drive', 'v3', credentials=creds)`, который представляет собой объект сервиса Google Drive v3 API.
- Метод `files().list()` используется для получения списка файлов в корневой папке Google Drive.
- В цикле `for` выводятся имена и идентификаторы найденных файлов.

## Подробности о параметрах

- `file_path` (Path): Путь к файлу, который нужно загрузить на Google Drive.
- `folder_name` (str): Имя папки на Google Drive, куда будут загружаться файлы.

## Примеры 

```python
from pathlib import Path

file_path = Path('/mnt/data/google_extracted/sample_file.txt')  # Замените на фактический путь к файлу
folder_name = 'My Drive Folder'  # Замените на имя целевой папки в Google Drive

google_drive_handler = GoogleDriveHandler(
    folder_name=folder_name,
)
google_drive_handler.upload_file(file_path)
```

**Описание примера**: 
- В этом примере файл `/mnt/data/google_extracted/sample_file.txt` загружается в папку "My Drive Folder" на Google Drive.

## Дополнительные замечания

- `gs.path.secrets`: эта переменная используется для доступа к секретным данным проекта.  Она должна быть определена в `src/gs/gs.py`.

- `_create_credentials(self)`:  метод получает учетные данные пользователя из файла `token.pickle`. Если файл не существует или учетные данные устарели, метод запускает процесс авторизации OAuth 2.0, чтобы получить новые учетные данные.

- `upload_file(self, file_path: Path)`: метод загружает файл на Google Drive в папку `folder_name`.  Логика загрузки файла не реализована в этом фрагменте кода. Она должна быть добавлена в соответствии с требованиями Google Drive API v3.

## Важные моменты

- `logger.info(...)` и `logger.error(...)`:  для вывода сообщений в консоль используется модуль `logger` из `src.logger.logger`.

- `pprint(...)`:  для вывода отладочной информации используется функция `pprint()` из `src.utils.printer`.

- `Driver, Chrome, Firefox, Playwright`: эти модули предоставляют функциональность для работы с WebDriver.  Они используются для автоматизации браузера и взаимодействия с веб-страницами.
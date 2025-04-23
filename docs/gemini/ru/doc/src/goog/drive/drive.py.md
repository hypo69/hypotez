# Модуль для работы с Google Drive
## Обзор

Модуль `src.goog.drive` предоставляет минимальную библиотеку для взаимодействия с Google Drive. Он позволяет загружать файлы в указанную папку Google Drive, используя API Google Drive v3. Модуль использует аутентификацию OAuth 2.0 для получения доступа к Google Drive пользователя.

## Подробнее

Модуль содержит класс `GoogleDriveHandler`, который инкапсулирует логику аутентификации и загрузки файлов.  Для успешной работы требуется файл с учетными данными (`hypo69-c32c8736ca62.json`) и токен доступа (`token.pickle`).
## Классы

### `GoogleDriveHandler`

**Описание**: Класс `GoogleDriveHandler` предназначен для управления взаимодействием с Google Drive, включая аутентификацию и загрузку файлов.

**Атрибуты**:

- `folder_name` (str): Имя папки в Google Drive, в которую будут загружаться файлы.
- `creds`: Учетные данные для доступа к Google Drive.

**Методы**:

- `__init__(self, folder_name: str)`: Конструктор класса, инициализирует имя папки и создает учетные данные.
- `_create_credentials(self)`: Получает или создает учетные данные пользователя для доступа к Google Drive.
- `upload_file(self, file_path: Path)`: Загружает файл в указанную папку Google Drive.

### `__init__(self, folder_name: str)`

**Назначение**: Инициализирует экземпляр класса `GoogleDriveHandler`.

**Параметры**:

- `folder_name` (str): Имя папки в Google Drive, в которую будут загружаться файлы.

**Как работает функция**:

Конструктор инициализирует атрибут `folder_name` и вызывает метод `_create_credentials()` для получения учетных данных.

### `_create_credentials(self)`

**Назначение**: Получает или создает учетные данные пользователя для доступа к Google Drive.

**Возвращает**:

- `creds`: Учетные данные для доступа к Google Drive.

**Как работает функция**:

1.  Определяет путь к файлу с учетными данными (`hypo69-c32c8736ca62.json`) и область доступа (`SCOPES`).
2.  Проверяет наличие файла `token.pickle` с сохраненными учетными данными.
3.  Если файл существует, загружает учетные данные из файла.
4.  Если учетные данные отсутствуют или недействительны, пытается обновить их или получить новые, используя файл с учетными данными.
5.  Сохраняет полученные учетные данные в файл `token.pickle`.

### `upload_file(self, file_path: Path)`

**Назначение**: Загружает файл в указанную папку Google Drive.

**Параметры**:

- `file_path` (Path): Путь к файлу, который необходимо загрузить.

**Как работает функция**:

Метод `upload_file` предназначен для загрузки указанного файла в папку Google Drive, имя которой было задано при инициализации объекта `GoogleDriveHandler`. В предоставленном коде реализация отсутствует (стоит `...`).

## Функции

### `main()`

**Назначение**: Показывает базовое использование API Drive v3.

**Как работает функция**:

1.  Создает учетные данные, используя метод `_create_credentials()` класса `GoogleDriveHandler`.
2.  Создает объект `service` для взаимодействия с API Drive v3.
3.  Вызывает API Drive v3 для получения списка файлов.
4.  Выводит список файлов в консоль.

```python
def main():
    """
    Демонстрирует базовое использование Drive v3 API.
    """
    creds = GoogleDriveHandler()._create_credentials()  # Функция получает учетные данные
    service = build('drive', 'v3', credentials=creds) # Функция создает объект service для взаимодействия с Drive API

    # Вызов Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute() # Функция вызывает метод list для получения списка файлов
    items = results.get('files', []) # Функция извлекает список файлов из результата

    if not items: # Функция проверяет, есть ли файлы в списке
        print('No files found.') # Функция выводит сообщение, если файлы не найдены
    else:
        print('Files:') # Функция выводит заголовок списка файлов
        for item in items: # Функция перебирает файлы в списке
            print('{0} ({1})'.format(item['name'], item['id'])) # Функция выводит имя и ID файла
```

**Примеры**:

```python
if __name__ == '__main__':
    main()
```
```
## Параметры класса
- `folder_name` (str): Имя папки в Google Drive, в которую будут загружаться файлы.
- `creds`: Учетные данные для доступа к Google Drive.
```
```python
# Пример использования класса
if __name__ == "__main__":
    from pathlib import Path

    file_path = Path('/mnt/data/google_extracted/sample_file.txt')  # Replace with your actual file path
    folder_name = 'My Drive Folder'  # Replace with the target folder name in Google Drive

    google_drive_handler = GoogleDriveHandler(
        folder_name=folder_name,
    )
    google_drive_handler.upload_file(file_path)
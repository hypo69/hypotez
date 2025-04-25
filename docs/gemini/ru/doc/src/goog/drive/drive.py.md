# Модуль для работы с Google Drive
=================================================

Модуль предоставляет класс `GoogleDriveHandler` для работы с Google Drive API. 
Класс позволяет загружать файлы в Google Drive.

## Оглавление

- [Обзор](#обзор)
- [Класс GoogleDriveHandler](#класс-googledrivehandler)
    - [Инициализация](#инициализация)
    - [Создание учетных данных](#создание-учетных-данных)
    - [Загрузка файла](#загрузка-файла)
- [Пример использования](#пример-использования)

## Обзор

Модуль `drive.py` предоставляет инструменты для взаимодействия с Google Drive API. 
Ключевой компонент - это класс `GoogleDriveHandler`, который упрощает процесс работы с Google Drive. 
В основном модуль предназначен для загрузки файлов в Google Drive.

## Класс GoogleDriveHandler

### Инициализация

```python
class GoogleDriveHandler:
    """Handles interaction with Google Drive."""

    def __init__(self, folder_name: str):
        """
        Инициализирует экземпляр класса `GoogleDriveHandler`.

        Args:
            folder_name (str): Имя папки в Google Drive, в которую будут загружаться файлы.
        """
        self.folder_name = folder_name
        self.creds = self._create_credentials()
```

### Создание учетных данных

```python
    def _create_credentials(self):
        """Gets valid user credentials from storage."""
        creds_file: Path = gs.path.secrets / 'hypo69-c32c8736ca62.json'
        SCOPES: list = ['https://www.googleapis.com/auth/drive']
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.creds_file, self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return creds
```

### Загрузка файла

```python
    def upload_file(self, file_path: Path):
        """
        Загружает файл в указанную папку в Google Drive.

        Args:
            file_path (Path): Путь к файлу, который нужно загрузить.
        """
        # Implement logic to upload the file to the specified folder using the service object
        # ...
```

## Пример использования

```python
# Example usage of the class
if __name__ == "__main__":
    from pathlib import Path

    file_path = Path('/mnt/data/google_extracted/sample_file.txt')  # Replace with your actual file path
    folder_name = 'My Drive Folder'  # Replace with the target folder name in Google Drive

    google_drive_handler = GoogleDriveHandler(
        folder_name=folder_name,
    )
    google_drive_handler.upload_file(file_path)
```

## Дополнительные комментарии

- В коде используется вебдрайвер. 
- Наследуй `Driver`, `Chrome`, `Firefox`, `Playwright`.
- Создай инстанс драйвера:
    ```python
    driver = Driver(Chrome)
    ```
- Модули `Driver`, `Chrome`, `Firefox`, `Playwright` уже содержат все настройки Selenium.
- Основная команда, которая используется в коде: `driver.execute_locator(l:dict)`. 
- Она возвращает значение вебэлемента по локатору.

##  Дополнительная информация

- Документация для `gs.path.secrets` отсутствует. 
- Документация для `logger` из `src.logger.logger` отсутствует.
- Необходимо реализовать логику загрузки файла в функции `upload_file`.
- В коде используются закомментированные строки, которые нужно пересмотреть.
- В коде есть дублирование импорта `pickle`, `Path`, `build`, `AuthorizedHttpTransport`, `Request`, `Credentials` и `InstalledAppFlow`.
- В коде используется закомментированный код, который нужно пересмотреть.
- В коде используется `print` вместо `logger`.
- Необходимо добавить документацию для функции `main`.
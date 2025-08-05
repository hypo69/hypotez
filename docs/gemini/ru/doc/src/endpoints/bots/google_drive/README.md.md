# Модуль для загрузки файлов в Google Drive

## Обзор

Этот модуль представляет собой бот для Telegram, написанный на Python, который позволяет загружать файлы в Google Drive. 

**Он поддерживает следующие функции:**

- **Загрузка файлов по прямым ссылкам:**  Поддерживаются прямые ссылки на файлы, а также ссылки на популярные сервисы файлообмена, такие как Mega.nz, Dropbox и т. д.
- **Аутентификация пользователя:** Пользователи могут авторизоваться в боте через команду `/auth` и получить уникальный ключ для доступа к своим файлам.
- **Поддержка Team Drive:** Bозможность подключения Team Drive, хотя она требует ручной настройки.
- **Разнообразие команд:**  Bот предоставляет команды `/start`, `/auth`, `/revoke` и `/help` для взаимодействия с пользователем.

**Этот модуль является  начальным проектом, который больше не развивается активно.  Он не предоставляет  возможности настройки Team Drive для каждого пользователя, которая  будет реализована в будущих версиях.**

## Классы

### `class DriveUploader`
**Описание**:  Основной класс бота для загрузки файлов в Google Drive.

**Атрибуты**:
- `telegram_token`: Токен бота Telegram (required).
- `google_drive_api_credentials_path`:  Путь к файлу с API-ключами Google Drive (required).
- `teamdrive_folder_id`: ID Team Drive папки, в которую загружаются файлы (optional).
- `teamdrive_id`: ID Team Drive (optional).

**Методы**:
- `start`: Инициализация бота.
- `handle_message`:  Обработка сообщений от пользователей Telegram.
- `auth`:  Процесс аутентификации пользователя в Google Drive API.
- `revoke`:  Удаление сохраненных учетных данных пользователя.
- `upload_file`:  Загрузка файла в Google Drive.
- `get_file_info`:  Получение информации о файле.
- `get_file_url`:  Получение публичной ссылки на файл в Google Drive.
- `get_file_size`:  Получение размера файла.
- `get_file_mime_type`:  Получение MIME-типа файла.
- `get_file_id`:  Получение ID файла.
- `check_link`:  Проверка ссылки на доступность и тип файла.
- `check_drive_folder`:  Проверка Team Drive папки на наличие.
- `create_drive_folder`:  Создание новой Team Drive папки.
- `handle_commands`:  Обработка команд пользователя.
- `process_message`:  Обработка текстовых сообщений пользователя.

### `class Plugin`
**Описание**:  Базовый класс для плагинов.

**Атрибуты**:
- `name`: Название плагина.
- `supported_links`:  Список поддерживаемых типов ссылок.
- `options`:  Список доступных опций для плагина.

**Методы**:
- `download_file`:  Загрузка файла по ссылке.
- `get_file_info`:  Получение информации о файле.
- `get_file_size`:  Получение размера файла.
- `get_file_mime_type`:  Получение MIME-типа файла.
- `get_file_id`:  Получение ID файла.

### `class DropboxPlugin`
**Описание**:  Плагин для загрузки файлов с Dropbox.

**Наследует**:  `Plugin`

**Атрибуты**:
- `supported_links`:  Список поддерживаемых типов ссылок, включает `'dropbox.com'`
- `options`:  Список доступных опций для плагина.

**Методы**:
- `download_file`:  Загрузка файла с Dropbox.
- `get_file_info`:  Получение информации о файле.
- `get_file_size`:  Получение размера файла.
- `get_file_mime_type`:  Получение MIME-типа файла.
- `get_file_id`:  Получение ID файла.

### `class MegaPlugin`
**Описание**:  Плагин для загрузки файлов с Mega.nz.

**Наследует**:  `Plugin`

**Атрибуты**:
- `supported_links`:  Список поддерживаемых типов ссылок, включает `'mega.nz'`
- `options`:  Список доступных опций для плагина.

**Методы**:
- `download_file`:  Загрузка файла с Mega.nz.
- `get_file_info`:  Получение информации о файле.
- `get_file_size`:  Получение размера файла.
- `get_file_mime_type`:  Получение MIME-типа файла.
- `get_file_id`:  Получение ID файла.

### `class OpenloadPlugin`
**Описание**:  Плагин для загрузки файлов с Openload.

**Наследует**:  `Plugin`

**Атрибуты**:
- `supported_links`:  Список поддерживаемых типов ссылок, включает `'openload.co'`
- `options`:  Список доступных опций для плагина.

**Методы**:
- `download_file`:  Загрузка файла с Openload.
- `get_file_info`:  Получение информации о файле.
- `get_file_size`:  Получение размера файла.
- `get_file_mime_type`:  Получение MIME-типа файла.
- `get_file_id`:  Получение ID файла.

### `class DirectLinkPlugin`
**Описание**:  Плагин для загрузки файлов по прямым ссылкам.

**Наследует**:  `Plugin`

**Атрибуты**:
- `supported_links`:  Список поддерживаемых типов ссылок, включает `'direct_link'`
- `options`:  Список доступных опций для плагина.

**Методы**:
- `download_file`:  Загрузка файла по прямой ссылке.
- `get_file_info`:  Получение информации о файле.
- `get_file_size`:  Получение размера файла.
- `get_file_mime_type`:  Получение MIME-типа файла.
- `get_file_id`:  Получение ID файла.

## Функции

### `get_file_info_from_link(link: str) -> Dict[str, Any] | None`
**Назначение**:  Получение информации о файле по ссылке. 

**Параметры**:
- `link` (str): Ссылка на файл.

**Возвращает**:
- `Dict[str, Any] | None`:  Словарь с информацией о файле или `None` в случае ошибки.

**Как работает функция**:
- Функция анализирует ссылку и определяет ее тип.
- В зависимости от типа ссылки она вызывает соответствующий плагин.
- Плагин выполняет запрос к сервису файлообмена и получает информацию о файле.
- Информация возвращается в виде словаря.

**Примеры**:
```python
link = 'https://www.dropbox.com/s/abcdefg12345/file.txt'
file_info = get_file_info_from_link(link)
print(file_info)
```

### `upload_file_to_google_drive(file_path: str, file_name: str, mime_type: str, parent_folder_id: str | None = None, teamdrive_id: str | None = None) -> str | None`
**Назначение**:  Загрузка файла в Google Drive. 

**Параметры**:
- `file_path` (str):  Путь к файлу.
- `file_name` (str):  Имя файла.
- `mime_type` (str):  MIME-тип файла.
- `parent_folder_id` (str | None, optional): ID папки в Google Drive, в которую загружается файл. По умолчанию `None`.
- `teamdrive_id` (str | None, optional): ID Team Drive, в которую загружается файл. По умолчанию `None`.

**Возвращает**:
- `str | None`: ID загруженного файла в Google Drive или `None` в случае ошибки.

**Как работает функция**:
- Функция использует Google Drive API для загрузки файла.
- Она предоставляет все необходимые параметры, включая путь к файлу, имя, MIME-тип и ID папки, в которую загружать файл.
-  В случае успеха функция возвращает ID загруженного файла.

**Примеры**:
```python
file_path = 'path/to/file.txt'
file_name = 'file.txt'
mime_type = 'text/plain'
parent_folder_id = '1234567890abcdefg'
teamdrive_id = '01234567890abcdefg'

file_id = upload_file_to_google_drive(file_path, file_name, mime_type, parent_folder_id, teamdrive_id)
print(file_id)
```

## Параметры

- `telegram_token` (str):  Токен бота Telegram.
- `google_drive_api_credentials_path` (str):  Путь к файлу с API-ключами Google Drive.
- `teamdrive_folder_id` (str): ID Team Drive папки, в которую загружаются файлы.
- `teamdrive_id` (str): ID Team Drive.
- `mega_email` (str):  Email-адрес для Mega.nz.
- `mega_password` (str):  Пароль для Mega.nz.
- `openload_ftp_login` (str):  Логин FTP для Openload.
- `openload_ftp_key` (str):  Ключ FTP для Openload.


## Примеры

**Использование бота:**

1. Зарегистрируйте бота в Telegram с помощью @BotFather.
2. Получите API-ключи Google Drive,  создав проект в Google Cloud Console.
3. Создайте файл `creds.py` и добавьте в него следующие параметры:
   ```python
   telegram_token = 'YOUR_TELEGRAM_BOT_TOKEN'
   google_drive_api_credentials_path = 'path/to/client_secrets.json'
   teamdrive_folder_id = 'YOUR_TEAMDRIVE_FOLDER_ID' # Optional
   teamdrive_id = 'YOUR_TEAMDRIVE_ID' # Optional
   ```
4. Запустите бот:
   ```python
   python3 bot.py
   ```
5. В Telegram отправьте команду `/auth` боту, чтобы получить уникальный ключ.
6. Отправьте ссылку на файл боту, чтобы загрузить его в Google Drive.
7. Вы можете использовать команды `/start`, `/revoke` и `/help` для взаимодействия с ботом.

**Пример использования  загрузки файла с Dropbox:**

```python
from src.endpoints.bots.google_drive.upload_file import DriveUploader

telegram_token = 'YOUR_TELEGRAM_BOT_TOKEN'
google_drive_api_credentials_path = 'path/to/client_secrets.json'

drive_uploader = DriveUploader(
    telegram_token=telegram_token,
    google_drive_api_credentials_path=google_drive_api_credentials_path,
)

link = 'https://www.dropbox.com/s/abcdefg12345/file.txt'
file_info = drive_uploader.get_file_info_from_link(link)

file_path = file_info['file_path']
file_name = file_info['file_name']
mime_type = file_info['mime_type']

file_id = drive_uploader.upload_file_to_google_drive(
    file_path=file_path, 
    file_name=file_name, 
    mime_type=mime_type,
)

print(f'File uploaded successfully! File ID: {file_id}')
```

**Пример использования  загрузки файла с Mega.nz:**

```python
from src.endpoints.bots.google_drive.upload_file import DriveUploader

telegram_token = 'YOUR_TELEGRAM_BOT_TOKEN'
google_drive_api_credentials_path = 'path/to/client_secrets.json'

drive_uploader = DriveUploader(
    telegram_token=telegram_token,
    google_drive_api_credentials_path=google_drive_api_credentials_path,
)

link = 'https://mega.nz/#!abcdefg12345'
file_info = drive_uploader.get_file_info_from_link(link)

file_path = file_info['file_path']
file_name = file_info['file_name']
mime_type = file_info['mime_type']

file_id = drive_uploader.upload_file_to_google_drive(
    file_path=file_path, 
    file_name=file_name, 
    mime_type=mime_type,
)

print(f'File uploaded successfully! File ID: {file_id}')
```

## TODO

- Добавить возможность переименования файлов при загрузке.
- Добавить поддержку загрузки файлов из Telegram (с ограничением по скорости загрузки).
- Добавить поддержку Youtube-dl.
- Исправить поддержку Openload.
- Добавить поддержку zippyshare, Mediafire, cloud mail, Yandex disk, Sourceforge.
- Добавить возможность генерировать прямую ссылку на файл в Google Drive.
- Добавить возможность настройки Team Drive для каждого пользователя.

## Лицензия

GPLv3
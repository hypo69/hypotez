# Модуль для хранения учетных данных

## Обзор

Модуль содержит класс `Creds`, который используется для хранения учетных данных, таких как токен Telegram-бота и идентификаторы TeamDrive для загрузки файлов.

## Подробнее

Этот модуль предназначен для централизованного хранения и управления учетными данными, необходимыми для работы бота Telegram и взаимодействия с Google Drive API. Он предоставляет простой способ определения и доступа к этим учетным данным в других частях проекта.

## Классы

### `Creds`

**Описание**: Класс для хранения учетных данных, таких как токен Telegram-бота и идентификаторы TeamDrive.

**Атрибуты**:
- `TG_TOKEN` (str): Токен Telegram-бота. По умолчанию пустая строка.
- `TEAMDRIVE_FOLDER_ID` (str): ID папки TeamDrive. По умолчанию пустая строка.
- `TEAMDRIVE_ID` (str): ID TeamDrive. По умолчанию пустая строка.

**Принцип работы**:
Класс `Creds` предназначен для хранения учетных данных, необходимых для работы с Telegram Bot и Google Drive. Он содержит статические переменные, которые можно задать для хранения токена Telegram-бота (`TG_TOKEN`), идентификатора папки TeamDrive (`TEAMDRIVE_FOLDER_ID`) и идентификатора самого TeamDrive (`TEAMDRIVE_ID`). Эти переменные используются другими модулями для аутентификации и авторизации при взаимодействии с Telegram API и Google Drive API.

## Параметры класса

- `TG_TOKEN` (str): Токен Telegram-бота, используемый для аутентификации бота в Telegram API.
- `TEAMDRIVE_FOLDER_ID` (str): Идентификатор папки в TeamDrive, куда будут загружаться файлы.
- `TEAMDRIVE_ID` (str): Идентификатор TeamDrive, используемый для доступа к TeamDrive API.

**Примеры**:

```python
from src.endpoints.bots.google_drive.creds import Creds

# Установка значений учетных данных
Creds.TG_TOKEN = "your_telegram_bot_token"
Creds.TEAMDRIVE_FOLDER_ID = "your_teamdrive_folder_id"
Creds.TEAMDRIVE_ID = "your_teamdrive_id"

# Получение значений учетных данных
token = Creds.TG_TOKEN
folder_id = Creds.TEAMDRIVE_FOLDER_ID
teamdrive_id = Creds.TEAMDRIVE_ID

print(f"Token: {token}")
print(f"Folder ID: {folder_id}")
print(f"TeamDrive ID: {teamdrive_id}")
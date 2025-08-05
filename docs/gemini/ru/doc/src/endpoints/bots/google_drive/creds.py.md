# Модуль `creds`

## Обзор

Этот модуль содержит класс `Creds`, который используется для хранения учетных данных для ботов Google Drive. 

## Подробней

Модуль предоставляет конфигурацию для интеграции с Google Drive. В нем определяются переменные, которые должны быть заполнены пользователем для корректной работы ботов.

## Классы

### `Creds`

**Описание**: Класс `Creds` хранит конфигурацию для ботов Google Drive. 

**Атрибуты**:

- `TG_TOKEN` (str): Токен для Telegram-бота.
- `TEAMDRIVE_FOLDER_ID` (str): ID папки в Team Drive.
- `TEAMDRIVE_ID` (str): ID Team Drive.

**Примеры**:

```python
from hypotez.src.endpoints.bots.google_drive.creds import Creds

# Инициализация класса с конфигурационными данными
creds = Creds()

# Доступ к атрибутам класса
print(creds.TG_TOKEN)
print(creds.TEAMDRIVE_FOLDER_ID)
print(creds.TEAMDRIVE_ID)
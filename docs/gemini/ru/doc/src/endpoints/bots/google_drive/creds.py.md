# Модуль для хранения учетных данных `Creds`

## Обзор

Модуль содержит класс `Creds`, предназначенный для хранения учетных данных, таких как токен Telegram-бота и идентификаторы TeamDrive для загрузки файлов.

## Подробней

Этот модуль предназначен для централизованного хранения и управления учетными данными, необходимыми для работы с Telegram API и Google Drive API. Он обеспечивает удобный способ определения параметров аутентификации и идентификации, используемых в других частях проекта.

## Классы

### `Creds`

**Описание**: Класс `Creds` предназначен для хранения статических значений, таких как токен Telegram-бота и идентификаторы TeamDrive.

**Атрибуты**:
- `TG_TOKEN` (str): Токен Telegram-бота.
- `TEAMDRIVE_FOLDER_ID` (str): Идентификатор папки TeamDrive.
- `TEAMDRIVE_ID` (str): Идентификатор TeamDrive.

**Принцип работы**:
Класс `Creds` содержит статические атрибуты, которые могут быть изменены для настройки доступа к Telegram API и Google Drive API.  Для использования необходимо задать значения атрибутам, соответствующие вашим учетным данным.

**Примеры**:
```python
from src.endpoints.bots.google_drive.creds import Creds

# Пример использования класса Creds
Creds.TG_TOKEN = "your_telegram_bot_token"
Creds.TEAMDRIVE_FOLDER_ID = "your_teamdrive_folder_id"
Creds.TEAMDRIVE_ID = "your_teamdrive_id"

# Теперь можно использовать эти значения в других частях кода
print(Creds.TG_TOKEN)
print(Creds.TEAMDRIVE_FOLDER_ID)
print(Creds.TEAMDRIVE_ID)
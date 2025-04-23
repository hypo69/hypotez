# Модуль `creds.py`

## Обзор

Модуль `creds.py` содержит класс `Creds`, предназначенный для хранения учетных данных, таких как токен Telegram-бота, идентификатор папки TeamDrive и идентификатор TeamDrive. Это необходимо для настройки доступа и работы с Google Drive через Telegram-бота.

## Более подробная информация

Этот файл определяет класс `Creds`, который используется для хранения параметров аутентификации и идентификации, необходимых для взаимодействия с Telegram API и Google Drive API. Эти параметры используются для настройки бота и разрешения загрузки файлов в определенную папку TeamDrive.

## Классы

### `Creds`

**Описание**: Класс `Creds` предназначен для хранения учетных данных, необходимых для работы с Telegram-ботом и Google Drive.
**Наследует**: Отсутствует.
**Атрибуты**:
- `TG_TOKEN` (str): Токен Telegram-бота.
- `TEAMDRIVE_FOLDER_ID` (str): Идентификатор папки TeamDrive.
- `TEAMDRIVE_ID` (str): Идентификатор TeamDrive.

**Принцип работы**:
Класс `Creds` служит контейнером для хранения учетных данных, необходимых для аутентификации и авторизации при работе с Telegram API и Google Drive API. Он позволяет централизованно хранить и использовать эти параметры в различных частях приложения.

**Примеры**:

```python
# Пример инициализации класса Creds и присвоения значений
creds = Creds()
creds.TG_TOKEN = "your_telegram_bot_token"
creds.TEAMDRIVE_FOLDER_ID = "your_teamdrive_folder_id"
creds.TEAMDRIVE_ID = "your_teamdrive_id"
```

## Параметры класса

- `TG_TOKEN` (str): Токен Telegram-бота, используемый для аутентификации бота в Telegram API.
- `TEAMDRIVE_FOLDER_ID` (str): Идентификатор папки в TeamDrive, в которую будут загружаться файлы.
- `TEAMDRIVE_ID` (str): Идентификатор TeamDrive, используемый для доступа к TeamDrive через Google Drive API.

**Примеры**:

```python
# Пример заполнения параметров класса
Creds.TG_TOKEN = "your_telegram_bot_token"
Creds.TEAMDRIVE_FOLDER_ID = "your_teamdrive_folder_id"
Creds.TEAMDRIVE_ID = "your_teamdrive_id"
# Модуль для хранения учетных данных бота Google Drive

## Обзор

Модуль `src.endpoints.bots.google_drive.creds` предназначен для хранения учетных данных, необходимых для работы с Google Drive API.

## Подробней

Модуль содержит класс `Creds`, который определяет статические переменные для хранения токена Telegram-бота, ID папки Team Drive и ID самого Team Drive.

## Классы

### `Creds`

**Описание**: Класс для хранения учетных данных.

**Атрибуты**:

*   `TG_TOKEN` (str): Токен Telegram-бота.
*   `TEAMDRIVE_FOLDER_ID` (str): ID папки Team Drive.
*   `TEAMDRIVE_ID` (str): ID Team Drive.

**Как работает класс**:

Класс `Creds` предназначен для хранения учетных данных, необходимых для работы с Telegram-ботом и Google Drive API. Значения этих переменных должны быть заданы пользователем в соответствии с его учетными данными.

**Пример использования:**

```python
class Creds():
    # ENTER Your bot Token Here
    TG_TOKEN = ""
    
    
    
    #  Make Sure You Are Providing both value if you need Teamdrive upload
    # Because of pydrive And pydrive v2 Api
    
    #Folder Id Of Teamdrive
    TEAMDRIVE_FOLDER_ID = ""
    
    # Id of Team drive 
    TEAMDRIVE_ID = ""
    
    
    
    #Example 
    #TG_TOKEN = "dkjfksdkffdkfdkfdj"
    #TEAMDRIVE_FOLDER_ID = "13v4MaZnBz-iEHlZ0gFXk7rh"
    #TEAMDRIVE_ID = "0APh6R4WVvguEUk9PV"
```

**Примечания:**

*   Этот модуль не содержит функций или методов, кроме инициализации статических переменных.
*   Значения `TG_TOKEN`, `TEAMDRIVE_FOLDER_ID` и `TEAMDRIVE_ID` должны быть заполнены пользователем.
*   Если требуется загрузка файлов на Team Drive, необходимо указать как `TEAMDRIVE_FOLDER_ID`, так и `TEAMDRIVE_ID`.
*    Важно хранить эти учетные данные в безопасности и не передавать их третьим лицам.
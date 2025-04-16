# Модуль текстовых констант и учетных данных для бота Google Drive

## Обзор

Модуль `src.endpoints.bots.google_drive.plugins.TEXT` предназначен для хранения текстовых констант, используемых в Telegram-боте для взаимодействия с пользователями, а также для хранения учетных данных для работы с сервисом Mega.

## Подробней

Модуль содержит переменные с текстовыми сообщениями, которые отправляет бот, а также учетные данные для доступа к Mega.

## Переменные

*   `drive_folder_name` (str): Имя папки на Google Drive, куда будут загружаться файлы (значение: `"GDriveUploaderBot"`).
*   `MEGA_EMAIL` (str): Email для аккаунта Mega (значение: `"bearyan8@yandex.com"`).
*   `MEGA_PASSWORD` (str): Пароль для аккаунта Mega (значение: `"bearyan8@yandex.com"`).
*   `START` (str): Текст стартового сообщения бота.
*   `HELP` (str): Текст справки, содержащий описание команд и поддерживаемых ссылок.
*   `DP_DOWNLOAD` (str): Текст сообщения о начале загрузки с Dropbox.
*   `OL_DOWNLOAD` (str): Текст сообщения о начале загрузки с Openload.
*   `PROCESSING` (str): Текст сообщения об обработке запроса.
*   `DOWN_TWO` (bool): Флаг для активации второго загрузчика (значение: `True`).
*   `DOWNLOAD` (str): Текст сообщения о начале загрузки.
*   `DOWN_MEGA` (str): Текст сообщения о загрузке с Mega.
*   `DOWN_COMPLETE` (str): Текст сообщения об успешном завершении загрузки.
*   `NOT_AUTH` (str): Текст сообщения об отсутствии авторизации.
*   `REVOKE_FAIL` (str): Текст сообщения о неудачной попытке отмены авторизации.
*   `AUTH_SUCC` (str): Текст сообщения об успешной авторизации.
*   `ALREADY_AUTH` (str): Текст сообщения об уже выполненной авторизации.
*   `AUTH_URL` (str): Текст сообщения с URL для авторизации в Google Drive.
*   `UPLOADING` (str): Текст сообщения о начале загрузки файла на Google Drive.
*   `REVOKE_TOK` (str): Текст сообщения об успешной отмене авторизации.
*   `DOWN_PATH` (str): Путь к папке для сохранения загруженных файлов (значение: `"Downloads/"`).
*   `DOWNLOAD_URL` (str): Текст сообщения со ссылкой на загруженный файл на Google Drive.
*   `AUTH_ERROR` (str): Текст сообщения об ошибке авторизации.
*   `OPENLOAD` (bool): Флаг для включения/выключения поддержки Openload (значение: `True`).
*   `DROPBOX` (bool): Флаг для включения/выключения поддержки Dropbox (значение: `True`).
*   `MEGA` (bool): Флаг для включения/выключения поддержки Mega (значение: `True`).
*   `UPDATE` (str): Текст сообщения об обновлениях бота.

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

*   Этот модуль содержит важные учетные данные и текстовые константы, используемые в Telegram-боте.
*   Значения `MEGA_EMAIL` и `MEGA_PASSWORD` должны быть заполнены пользователем для работы с Mega.
*   Текстовые константы используются для формирования сообщений, отправляемых ботом пользователям.
*  Важно хранить учетные данные в безопасности и не передавать их третьим лицам.
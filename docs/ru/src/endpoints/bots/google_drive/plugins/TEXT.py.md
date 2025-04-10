# Модуль с текстовыми константами для Google Drive бота

## Обзор

Этот модуль содержит набор текстовых констант, используемых в Google Drive Uploader Bot. Он определяет различные сообщения и параметры, необходимые для работы бота, такие как имена папок, учетные данные, сообщения для пользователя и настройки поддержки различных типов ссылок.

## Подробней

Этот модуль содержит предопределенные текстовые сообщения, параметры конфигурации и настройки, которые позволяют боту правильно функционировать и взаимодействовать с пользователем. Он также определяет, какие типы ссылок поддерживаются ботом и предоставляет сообщения об ошибках и обновлениях.

## Переменные

### `drive_folder_name`

```python
drive_folder_name = "GDriveUploaderBot"
```

**Описание**: Имя папки на Google Диске, куда будут загружаться файлы.
**Назначение**: Определяет имя папки, используемой ботом для хранения загруженных файлов на Google Диске. Пользователь может изменить это имя по своему желанию.

### `MEGA_EMAIL`

```python
MEGA_EMAIL = "bearyan8@yandex.com"
```

**Описание**: Электронная почта для аккаунта Mega.
**Назначение**: Используется для входа в аккаунт Mega при загрузке файлов с Mega.

### `MEGA_PASSWORD`

```python
MEGA_PASSWORD = "bearyan8@yandex.com"
```

**Описание**: Пароль для аккаунта Mega.
**Назначение**: Используется для входа в аккаунт Mega при загрузке файлов с Mega.

### `START`

```python
START = " Hi {}  \\nI am Drive Uploader Bot . Please Authorise To use me .By using /auth \\n\\n For more info /help \\n\\n Third-Party Website \\n Support Added /update \\n\\n For Bot Updates  \\n <a href =\'https://t.me/aryan_bots\'>Join Channel</a>\\nPlease Report Bugs  @aryanvikash"
```

**Описание**: Стартовое сообщение бота.
**Назначение**: Сообщение, которое бот отправляет пользователю при первом взаимодействии. Содержит приветствие, инструкции по авторизации и ссылки на дополнительную информацию.

### `HELP`

```python
HELP = """   <b>AUTHORISE BOT</b> \n       Use  /auth Command Generate\n       Your Google Drive Token And \n       Send It To Bot  \n<b> You Wanna Change Your Login \n        Account ?</b> \\n\n        You Can Use /revoke \n        command            \n<b>What I Can Do With This Bot? </b>\n            You Can Upload Any Internet\n            Files On Your google\n            Drive Account.\n<b> Links Supported By Bot</b>\n            * Direct Links \n            * Openload links [Max Speed \n              500 KBps :(   ]\n            * Dropbox links \n            *  Mega links\n            \n            + More On Its way:)\n                \nBug Report @aryanvikash\n        """
```

**Описание**: Справочное сообщение бота.
**Назначение**: Сообщение, которое бот отправляет пользователю в ответ на команду `/help`. Содержит инструкции по авторизации, информацию о возможностях бота и поддерживаемых типах ссылок.

### `DP_DOWNLOAD`

```python
DP_DOWNLOAD = "Dropbox Link !! Downloading Started ..."
```

**Описание**: Сообщение о начале загрузки с Dropbox.
**Назначение**: Уведомляет пользователя о начале загрузки файла по ссылке Dropbox.

### `OL_DOWNLOAD`

```python
OL_DOWNLOAD = "Openload Link !! Downloading Started ... \\n Openload Links Are Extremely Slow"
```

**Описание**: Сообщение о начале загрузки с Openload.
**Назначение**: Уведомляет пользователя о начале загрузки файла по ссылке Openload и предупреждает о низкой скорости загрузки.

### `PROCESSING`

```python
PROCESSING = "Processing Your Request ...!!"
```

**Описание**: Сообщение о начале обработки запроса.
**Назначение**: Информирует пользователя о том, что бот начал обработку его запроса.

### `DOWN_TWO`

```python
DOWN_TWO = True
```

**Описание**: Флаг для параллельной загрузки.
**Назначение**: Определяет, разрешена ли параллельная загрузка файлов.

### `DOWNLOAD`

```python
DOWNLOAD = "Downloading Started ..."
```

**Описание**: Сообщение о начале загрузки.
**Назначение**: Уведомляет пользователя о начале загрузки файла.

### `DOWN_MEGA`

```python
DOWN_MEGA = "Downloading Started... \\n  Mega Links are \\n Extremely Slow :("
```

**Описание**: Сообщение о начале загрузки с Mega.
**Назначение**: Уведомляет пользователя о начале загрузки файла по ссылке Mega и предупреждает о низкой скорости загрузки.

### `DOWN_COMPLETE`

```python
DOWN_COMPLETE = "Downloading complete !!"
```

**Описание**: Сообщение об успешном завершении загрузки.
**Назначение**: Уведомляет пользователя об успешном завершении загрузки файла.

### `NOT_AUTH`

```python
NOT_AUTH = "You Are Not Authorised To Using this Bot \\n\\n Please Authorise Me Using /auth  \\n\\n @aryanvikash"
```

**Описание**: Сообщение об отсутствии авторизации.
**Назначение**: Сообщение, которое бот отправляет пользователю, если он не авторизован для использования бота.

### `REVOKE_FAIL`

```python
REVOKE_FAIL = "You Are Already UnAuthorised \\n. Please Use /auth To Authorise \\n\\n report At @aryanvikash "
```

**Описание**: Сообщение о неудачной попытке отзыва авторизации.
**Назначение**: Сообщение, которое бот отправляет пользователю, если он пытается отозвать авторизацию, когда она уже отозвана.

### `AUTH_SUCC`

```python
AUTH_SUCC = "Authorised Successfully  !! \\n\\n Now Send me A direct Link :)"
```

**Описание**: Сообщение об успешной авторизации.
**Назначение**: Сообщение, которое бот отправляет пользователю после успешной авторизации.

### `ALREADY_AUTH`

```python
ALREADY_AUTH = "You Are Already Authorised ! \\n\\n Wanna Change Drive Account? \\n\\n Use /revoke \\n\\n report At @aryanvikash "
```

**Описание**: Сообщение о повторной авторизации.
**Назначение**: Сообщение, которое бот отправляет пользователю, если он пытается авторизоваться повторно, когда уже авторизован.

### `AUTH_URL`

```python
AUTH_URL = '<a href ="{}">Vist This Url</a> \\n Generate And Copy Your Google Drive Token And Send It To Me'
```

**Описание**: URL для авторизации.
**Назначение**: Содержит URL, который бот отправляет пользователю для получения токена авторизации Google Drive.

### `UPLOADING`

```python
UPLOADING = "Download Complete !! \\n Uploading Your file"
```

**Описание**: Сообщение о начале загрузки на Google Drive.
**Назначение**: Уведомляет пользователя о начале загрузки файла на Google Drive.

### `REVOKE_TOK`

```python
REVOKE_TOK = " Your Token is Revoked Successfully !! \\n\\n Use /auth To Re-Authorise Your Drive Acc. "
```

**Описание**: Сообщение об успешном отзыве токена.
**Назначение**: Сообщение, которое бот отправляет пользователю после успешного отзыва токена авторизации.

### `DOWN_PATH`

```python
DOWN_PATH = "Downloads/"  # Linux path
```

**Описание**: Путь для сохранения загруженных файлов.
**Назначение**: Определяет путь, по которому будут сохраняться загруженные файлы на сервере.

### `DOWNLOAD_URL`

```python
DOWNLOAD_URL = "Your File Uploaded Successfully \\n\\n <b>Filename</b> : {} \\n\\n <b> Size</b> : {} MB \\n\\n <b>Download</b> {}"
```

**Описание**: Сообщение об успешной загрузке с информацией о файле.
**Назначение**: Уведомляет пользователя об успешной загрузке файла на Google Drive и предоставляет информацию о файле, такую как имя, размер и ссылку для скачивания.

### `AUTH_ERROR`

```python
AUTH_ERROR = "AUTH Error !! Please  Send Me a  valid Token or Re - Authorise Me  \\n\\n report At @aryanvikash"
```

**Описание**: Сообщение об ошибке авторизации.
**Назначение**: Сообщение, которое бот отправляет пользователю в случае ошибки авторизации.

### `OPENLOAD`

```python
OPENLOAD = True
```

**Описание**: Флаг поддержки Openload ссылок.
**Назначение**: Определяет, поддерживает ли бот загрузку файлов по ссылкам Openload.

### `DROPBOX`

```python
DROPBOX = True
```

**Описание**: Флаг поддержки Dropbox ссылок.
**Назначение**: Определяет, поддерживает ли бот загрузку файлов по ссылкам Dropbox.

### `MEGA`

```python
MEGA = True
```

**Описание**: Флаг поддержки Mega ссылок.
**Назначение**: Определяет, поддерживает ли бот загрузку файлов по ссылкам Mega.

### `UPDATE`

```python
UPDATE = """ <b> Update  on  27.07.2019</b>\n            * MEGA LINK added\n            * Error Handling Improved\n
<b> Links Supported By Bot</b>\n            * Direct Links \n            * Openload links [Max Speed \n              500 KBps :(   ]\n            * Dropbox links \n            *  Mega links (only files)\n            
+ More are in way:) """
```

**Описание**: Сообщение об обновлении бота.
**Назначение**: Сообщение, которое бот отправляет пользователю для информирования об обновлениях и новых функциях.
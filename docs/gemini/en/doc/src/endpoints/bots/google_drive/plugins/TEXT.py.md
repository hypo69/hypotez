# Модуль TEXT

## Обзор

Этот модуль содержит строковые константы и переменные, используемые в боте для загрузки файлов на Google Диск. Он определяет сообщения, URL-адреса и параметры, необходимые для взаимодействия с пользователем и обработки различных типов ссылок.

## Подробнее

Этот код содержит переменные и константы, определяющие поведение бота, сообщения для пользователей и параметры для работы с различными сервисами (Google Drive, Mega, Dropbox, Openload). Он используется для упрощения настройки и изменения текста сообщений, а также для управления функциональностью бота.
## Переменные

### `drive_folder_name`

```python
drive_folder_name: str = "GDriveUploaderBot"
```

**Описание**: Имя папки на Google Диске, куда будут загружаться файлы.
**Принцип работы**: Определяет имя папки, которая будет использоваться для хранения загруженных файлов.

### `MEGA_EMAIL`

```python
MEGA_EMAIL: str = "bearyan8@yandex.com"
```

**Описание**: Email для доступа к аккаунту Mega.
**Принцип работы**: Используется для авторизации при скачивании файлов с Mega.

### `MEGA_PASSWORD`

```python
MEGA_PASSWORD: str = "bearyan8@yandex.com"
```

**Описание**: Пароль для доступа к аккаунту Mega.
**Принцип работы**: Используется вместе с email для авторизации при скачивании файлов с Mega.

### `START`

```python
START: str = " Hi {}  \\nI am Drive Uploader Bot . Please Authorise To use me .By using /auth \\n\\n For more info /help \\n\\n Third-Party Website \\n Support Added /update \\n\\n For Bot Updates  \\n <a href =\'https://t.me/aryan_bots\'>Join Channel</a>\\nPlease Report Bugs  @aryanvikash"
```

**Описание**: Приветственное сообщение для пользователя.
**Принцип работы**: Отображается при первом взаимодействии пользователя с ботом.

### `HELP`

```python
HELP: str = """   <b>AUTHORISE BOT</b> \n       Use  /auth Command Generate\n       Your Google Drive Token And \n       Send It To Bot  \n<b> You Wanna Change Your Login \n        Account ?</b> \\n\n        You Can Use /revoke \n        command            \n<b>What I Can Do With This Bot? </b>\n            You Can Upload Any Internet\n            Files On Your google\n            Drive Account.\n<b> Links Supported By Bot</b>\n            * Direct Links \n            * Openload links [Max Speed \n              500 KBps :(   ]\n            * Dropbox links \n            *  Mega links\n            \n            + More On Its way:)\n                \nBug Report @aryanvikash\n        """
```

**Описание**: Справочное сообщение с информацией о командах и возможностях бота.
**Принцип работы**: Отображается в ответ на команду `/help`.

### `DP_DOWNLOAD`

```python
DP_DOWNLOAD: str = "Dropbox Link !! Downloading Started ..."
```

**Описание**: Сообщение о начале скачивания файла с Dropbox.
**Принцип работы**: Отображается при обнаружении ссылки на Dropbox.

### `OL_DOWNLOAD`

```python
OL_DOWNLOAD: str = "Openload Link !! Downloading Started ... \\n Openload Links Are Extremely Slow"
```

**Описание**: Сообщение о начале скачивания файла с Openload.
**Принцип работы**: Отображается при обнаружении ссылки на Openload.

### `PROCESSING`

```python
PROCESSING: str = "Processing Your Request ...!!"
```

**Описание**: Сообщение об обработке запроса пользователя.
**Принцип работы**: Отображается во время обработки запроса.

### `DOWN_TWO`

```python
DOWN_TWO: bool = True
```

**Описание**: Флаг, определяющий необходимость двойной загрузки (возможно, устаревший).
**Принцип работы**: Контролирует логику загрузки, но его назначение неясно из контекста.

### `DOWNLOAD`

```python
DOWNLOAD: str = "Downloading Started ..."
```

**Описание**: Сообщение о начале скачивания файла.
**Принцип работы**: Отображается при начале загрузки файла.

### `DOWN_MEGA`

```python
DOWN_MEGA: str = "Downloading Started... \\n  Mega Links are \\n Extremely Slow :("
```

**Описание**: Сообщение о начале скачивания файла с Mega.
**Принцип работы**: Отображается при обнаружении ссылки на Mega.

### `DOWN_COMPLETE`

```python
DOWN_COMPLETE: str = "Downloading complete !!"
```

**Описание**: Сообщение об успешном завершении скачивания файла.
**Принцип работы**: Отображается после завершения загрузки файла.

### `NOT_AUTH`

```python
NOT_AUTH: str = "You Are Not Authorised To Using this Bot \\n\\n Please Authorise Me Using /auth  \\n\\n @aryanvikash"
```

**Описание**: Сообщение об отсутствии авторизации у пользователя.
**Принцип работы**: Отображается, если пользователь не авторизован для использования бота.

### `REVOKE_FAIL`

```python
REVOKE_FAIL: str = "You Are Already UnAuthorised \\n. Please Use /auth To Authorise \\n\\n report At @aryanvikash "
```

**Описание**: Сообщение о неудачной попытке отмены авторизации.
**Принцип работы**: Отображается, если пользователь уже не авторизован.

### `AUTH_SUCC`

```python
AUTH_SUCC: str = "Authorised Successfully  !! \\n\\n Now Send me A direct Link :)"
```

**Описание**: Сообщение об успешной авторизации пользователя.
**Принцип работы**: Отображается после успешной авторизации.

### `ALREADY_AUTH`

```python
ALREADY_AUTH: str = "You Are Already Authorised ! \\n\\n Wanna Change Drive Account? \\n\\n Use /revoke \\n\\n report At @aryanvikash "
```

**Описание**: Сообщение о том, что пользователь уже авторизован.
**Принцип работы**: Отображается, если пользователь пытается авторизоваться повторно.

### `AUTH_URL`

```python
AUTH_URL: str = \'<a href ="{}">Vist This Url</a> \\n Generate And Copy Your Google Drive Token And Send It To Me\'
```

**Описание**: URL-адрес для авторизации через Google Drive.
**Принцип работы**: Предоставляет ссылку для получения токена авторизации.

### `UPLOADING`

```python
UPLOADING: str = "Download Complete !! \\n Uploading Your file"
```

**Описание**: Сообщение о начале загрузки файла на Google Диск.
**Принцип работы**: Отображается после завершения скачивания и перед началом загрузки на диск.

### `REVOKE_TOK`

```python
REVOKE_TOK: str = " Your Token is Revoked Successfully !! \\n\\n Use /auth To Re-Authorise Your Drive Acc. "
```

**Описание**: Сообщение об успешной отмене авторизации.
**Принцип работы**: Отображается после успешной отмены авторизации.

### `DOWN_PATH`

```python
DOWN_PATH: str = "Downloads/"  # Linux path
```

**Описание**: Путь к папке для сохранения скачиваемых файлов.
**Принцип работы**: Определяет, куда будут сохраняться скачиваемые файлы.

### `DOWNLOAD_URL`

```python
DOWNLOAD_URL: str = "Your File Uploaded Successfully \\n\\n <b>Filename</b> : {} \\n\\n <b> Size</b> : {} MB \\n\\n <b>Download</b> {}"
```

**Описание**: Сообщение об успешной загрузке файла на Google Диск.
**Принцип работы**: Отображается после успешной загрузки файла.

### `AUTH_ERROR`

```python
AUTH_ERROR: str = "AUTH Error !! Please  Send Me a  valid Token or Re - Authorise Me  \\n\\n report At @aryanvikash"
```

**Описание**: Сообщение об ошибке авторизации.
**Принцип работы**: Отображается, если произошла ошибка во время авторизации.

### `OPENLOAD`

```python
OPENLOAD: bool = True
```

**Описание**: Флаг, определяющий поддержку ссылок Openload.
**Принцип работы**: Включает или отключает поддержку загрузки с Openload.

### `DROPBOX`

```python
DROPBOX: bool = True
```

**Описание**: Флаг, определяющий поддержку ссылок Dropbox.
**Принцип работы**: Включает или отключает поддержку загрузки с Dropbox.

### `MEGA`

```python
MEGA: bool = True
```

**Описание**: Флаг, определяющий поддержку ссылок Mega.
**Принцип работы**: Включает или отключает поддержку загрузки с Mega.

### `UPDATE`

```python
UPDATE: str = """ <b> Update  on  27.07.2019</b>\n            * MEGA LINK added\n            * Error Handling Improved\n
<b> Links Supported By Bot</b>\n            * Direct Links \n            * Openload links [Max Speed \n              500 KBps :(   ]\n            * Dropbox links \n            *  Mega links (only files)\n            
            + More are in way:) """
```

**Описание**: Информация об обновлении бота.
**Принцип работы**: Содержит информацию о последних изменениях и поддерживаемых типах ссылок.
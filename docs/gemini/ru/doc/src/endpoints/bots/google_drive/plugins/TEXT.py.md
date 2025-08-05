# Модуль TEXT

## Обзор

Этот файл содержит константы, которые используются в боте Google Drive Uploader Bot. Эти константы содержат текст, который используется для взаимодействия с пользователем, например, приветствия, инструкции, сообщения об ошибках, а также статусы загрузки.

## Константы

### `drive_folder_name`

**Описание**:  Название папки в Google Drive, куда будут загружаться файлы.
**Тип**: `str`
**Пример**: `"GDriveUploaderBot"`

### `MEGA_EMAIL`

**Описание**:  Email от аккаунта MEGA.
**Тип**: `str`
**Пример**: `"bearyan8@yandex.com"`

### `MEGA_PASSWORD`

**Описание**:  Пароль от аккаунта MEGA.
**Тип**: `str`
**Пример**: `"bearyan8@yandex.com"`

### `START`

**Описание**:  Текст приветствия при запуске бота. 
**Тип**: `str`
**Пример**: `" Hi {}  \\nI am Drive Uploader Bot . Please Authorise To use me .By using /auth \\n\\n For more info /help \\n\\n Third-Party Website \\n Support Added /update \\n\\n For Bot Updates  \\n <a href =\'https://t.me/aryan_bots\'>Join Channel</a>\\nPlease Report Bugs  @aryanvikash"`

### `HELP`

**Описание**:  Текст справки, который отображается при использовании команды `/help`.
**Тип**: `str`
**Пример**:  """   <b>AUTHORISE BOT</b> \n       Use  /auth Command Generate\n       Your Google Drive Token And \n       Send It To Bot  \n<b> You Wanna Change Your Login \n        Account ?</b> \\n\\n        You Can Use /revoke \n        command            \n<b>What I Can Do With This Bot? </b>\n            You Can Upload Any Internet\n            Files On Your google\n            Drive Account.\n<b> Links Supported By Bot</b>\n            * Direct Links \n            * Openload links [Max Speed \n              500 KBps :(   ]\n            * Dropbox links \n            *  Mega links\n            \n            + More On Its way:)\n                \nBug Report @aryanvikash\n        """

### `DP_DOWNLOAD`

**Описание**:  Сообщение о начале загрузки файла с Dropbox.
**Тип**: `str`
**Пример**: `"Dropbox Link !! Downloading Started ..."`

### `OL_DOWNLOAD`

**Описание**:  Сообщение о начале загрузки файла с Openload.
**Тип**: `str`
**Пример**: `"Openload Link !! Downloading Started ... \\n Openload Links Are Extremely Slow"`

### `PROCESSING`

**Описание**:  Сообщение о том, что бот обрабатывает запрос.
**Тип**: `str`
**Пример**: `"Processing Your Request ...!!"`

### `DOWN_TWO`

**Описание**:  Флаг, определяющий, нужно ли использовать два разных сообщения о начале загрузки.
**Тип**: `bool`
**Пример**: `True`

### `DOWNLOAD`

**Описание**:  Сообщение о начале загрузки файла.
**Тип**: `str`
**Пример**: `"Downloading Started ..."`

### `DOWN_MEGA`

**Описание**:  Сообщение о начале загрузки файла с Mega.
**Тип**: `str`
**Пример**: `"Downloading Started... \\n  Mega Links are \\n Extremely Slow :("`

### `DOWN_COMPLETE`

**Описание**:  Сообщение о завершении загрузки файла.
**Тип**: `str`
**Пример**: `"Downloading complete !!"`

### `NOT_AUTH`

**Описание**:  Сообщение об отсутствии авторизации бота.
**Тип**: `str`
**Пример**: `"You Are Not Authorised To Using this Bot \\n\\n Please Authorise Me Using /auth  \\n\\n @aryanvikash"`

### `REVOKE_FAIL`

**Описание**:  Сообщение об ошибке при отмене авторизации.
**Тип**: `str`
**Пример**: `"You Are Already UnAuthorised \\n. Please Use /auth To Authorise \\n\\n report At @aryanvikash "`

### `AUTH_SUCC`

**Описание**:  Сообщение об успешной авторизации бота.
**Тип**: `str`
**Пример**: `"Authorised Successfully  !! \\n\\n Now Send me A direct Link :)"`

### `ALREADY_AUTH`

**Описание**:  Сообщение о том, что бот уже авторизован.
**Тип**: `str`
**Пример**: `"You Are Already Authorised ! \\n\\n Wanna Change Drive Account? \\n\\n Use /revoke \\n\\n report At @aryanvikash "`

### `AUTH_URL`

**Описание**:  Текст ссылки для авторизации бота.
**Тип**: `str`
**Пример**: `'<a href ="{}">Vist This Url</a> \\n Generate And Copy Your Google Drive Token And Send It To Me'`.

### `UPLOADING`

**Описание**:  Сообщение о начале загрузки файла в Google Drive.
**Тип**: `str`
**Пример**: `"Download Complete !! \\n Uploading Your file"`

### `REVOKE_TOK`

**Описание**:  Сообщение об успешной отмене авторизации.
**Тип**: `str`
**Пример**: `" Your Token is Revoked Successfully !! \\n\\n Use /auth To Re-Authorise Your Drive Acc. "`

### `DOWN_PATH`

**Описание**:  Путь к папке загрузки.
**Тип**: `str`
**Пример**: `"Downloads/"`

### `DOWNLOAD_URL`

**Описание**:  Текст сообщения о завершении загрузки. 
**Тип**: `str`
**Пример**: `"Your File Uploaded Successfully \\n\\n <b>Filename</b> : {} \\n\\n <b> Size</b> : {} MB \\n\\n <b>Download</b> {}"`

### `AUTH_ERROR`

**Описание**:  Сообщение об ошибке авторизации.
**Тип**: `str`
**Пример**: `"AUTH Error !! Please  Send Me a  valid Token or Re - Authorise Me  \\n\\n report At @aryanvikash"`

### `OPENLOAD`

**Описание**:  Флаг, определяющий, поддерживаются ли Openload ссылки.
**Тип**: `bool`
**Пример**: `True`

### `DROPBOX`

**Описание**:  Флаг, определяющий, поддерживаются ли Dropbox ссылки.
**Тип**: `bool`
**Пример**: `True`

### `MEGA`

**Описание**:  Флаг, определяющий, поддерживаются ли Mega ссылки.
**Тип**: `bool`
**Пример**: `True`

### `UPDATE`

**Описание**:  Текст сообщения об обновлении бота.
**Тип**: `str`
**Пример**: """ <b> Update  on  27.07.2019</b>\n            * MEGA LINK added\n            * Error Handling Improved\n\n<b> Links Supported By Bot</b>\n            * Direct Links \n            * Openload links [Max Speed \n              500 KBps :(   ]\n            * Dropbox links \n            *  Mega links (only files)\n            \n            + More are in way:) """
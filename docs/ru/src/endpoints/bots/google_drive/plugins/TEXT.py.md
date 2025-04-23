# Модуль TEXT

## Обзор

Модуль содержит текстовые константы и настройки, используемые в боте для загрузки файлов на Google Drive. Он определяет имена папок, учетные данные для Mega, приветственные сообщения, справку, сообщения о статусе загрузки и другие параметры, необходимые для работы бота.

## Подробней

Этот модуль содержит настройки для бота, включая:

- Имя папки на Google Drive (`drive_folder_name`).
- Учетные данные для доступа к Mega (`MEGA_EMAIL`, `MEGA_PASSWORD`).
- Текстовые сообщения для различных этапов работы бота (приветствие, помощь, статусы загрузки и авторизации).
- Флаги для включения/выключения поддержки определенных сервисов (`OPENLOAD`, `DROPBOX`, `MEGA`).
- Путь для сохранения загруженных файлов (`DOWN_PATH`).

## Переменные

### `drive_folder_name`

```python
drive_folder_name: str = "GDriveUploaderBot"
```

Имя папки на Google Drive, в которую будут загружаться файлы. Может быть изменено по желанию.

### `MEGA_EMAIL`

```python
MEGA_EMAIL: str = "bearyan8@yandex.com"
```

Email для доступа к аккаунту Mega, используется для загрузки файлов с Mega.

### `MEGA_PASSWORD`

```python
MEGA_PASSWORD: str = "bearyan8@yandex.com"
```

Пароль для доступа к аккаунту Mega, используется для загрузки файлов с Mega.

### `START`

```python
START: str
```

Приветственное сообщение для пользователя, отображается при первом взаимодействии с ботом.

### `HELP`

```python
HELP: str
```

Текст справки, который предоставляет информацию о командах и возможностях бота.

### `DP_DOWNLOAD`

```python
DP_DOWNLOAD: str = "Dropbox Link !! Downloading Started ..."
```

Сообщение, отображаемое при начале загрузки файла с Dropbox.

### `OL_DOWNLOAD`

```python
OL_DOWNLOAD: str = "Openload Link !! Downloading Started ... \\n Openload Links Are Extremely Slow"
```

Сообщение, отображаемое при начале загрузки файла с Openload.

### `PROCESSING`

```python
PROCESSING: str = "Processing Your Request ...!!"
```

Сообщение, отображаемое при обработке запроса пользователя.

### `DOWN_TWO`

```python
DOWN_TWO: bool = True
```

Флаг, определяющий возможность одновременной загрузки нескольких файлов.

### `DOWNLOAD`

```python
DOWNLOAD: str = "Downloading Started ..."
```

Сообщение, отображаемое при начале загрузки файла.

### `DOWN_MEGA`

```python
DOWN_MEGA: str = "Downloading Started... \\n  Mega Links are \\n Extremely Slow :("
```

Сообщение, отображаемое при начале загрузки файла с Mega.

### `DOWN_COMPLETE`

```python
DOWN_COMPLETE: str = "Downloading complete !!"
```

Сообщение, отображаемое после завершения загрузки файла.

### `NOT_AUTH`

```python
NOT_AUTH: str = "You Are Not Authorised To Using this Bot \\n\\n Please Authorise Me Using /auth  \\n\\n @aryanvikash"
```

Сообщение, отображаемое, если пользователь не авторизован.

### `REVOKE_FAIL`

```python
REVOKE_FAIL: str = "You Are Already UnAuthorised \\n. Please Use /auth To Authorise \\n\\n report At @aryanvikash "
```

Сообщение, отображаемое, если не удалось отозвать авторизацию.

### `AUTH_SUCC`

```python
AUTH_SUCC: str = "Authorised Successfully  !! \\n\\n Now Send me A direct Link :)"
```

Сообщение, отображаемое после успешной авторизации.

### `ALREADY_AUTH`

```python
ALREADY_AUTH: str = "You Are Already Authorised ! \\n\\n Wanna Change Drive Account? \\n\\n Use /revoke \\n\\n report At @aryanvikash "
```

Сообщение, отображаемое, если пользователь уже авторизован.

### `AUTH_URL`

```python
AUTH_URL: str
```

URL для авторизации пользователя в Google Drive.

### `UPLOADING`

```python
UPLOADING: str = "Download Complete !! \\n Uploading Your file"
```

Сообщение, отображаемое при начале загрузки файла на Google Drive.

### `REVOKE_TOK`

```python
REVOKE_TOK: str = " Your Token is Revoked Successfully !! \\n\\n Use /auth To Re-Authorise Your Drive Acc. "
```

Сообщение, отображаемое после успешного отзыва токена авторизации.

### `DOWN_PATH`

```python
DOWN_PATH: str = "Downloads/"
```

Путь к папке, в которую временно сохраняются загруженные файлы.

### `DOWNLOAD_URL`

```python
DOWNLOAD_URL: str = "Your File Uploaded Successfully \\n\\n <b>Filename</b> : {} \\n\\n <b> Size</b> : {} MB \\n\\n <b>Download</b> {}"
```

Сообщение, отображаемое после успешной загрузки файла на Google Drive, содержит информацию о файле и ссылку для скачивания.

### `AUTH_ERROR`

```python
AUTH_ERROR: str = "AUTH Error !! Please  Send Me a  valid Token or Re - Authorise Me  \\n\\n report At @aryanvikash"
```

Сообщение, отображаемое при ошибке авторизации.

### `OPENLOAD`

```python
OPENLOAD: bool = True
```

Флаг, определяющий поддержку загрузки файлов с Openload.

### `DROPBOX`

```python
DROPBOX: bool = True
```

Флаг, определяющий поддержку загрузки файлов с Dropbox.

### `MEGA`

```python
MEGA: bool = True
```

Флаг, определяющий поддержку загрузки файлов с Mega.

### `UPDATE`

```python
UPDATE: str
```

Сообщение с информацией об обновлениях бота.
# Название модуля: Конфигурационные параметры и текстовые сообщения для бота Google Drive

## Обзор

Модуль содержит глобальные переменные, используемые для конфигурации и текстовых сообщений бота Google Drive. Он включает в себя параметры для авторизации, путей загрузки, текстовых сообщений для различных этапов работы бота и настроек поддержки различных платформ, таких как Mega, Dropbox и Openload.

## Подробней

Этот модуль определяет основные параметры, необходимые для функционирования бота, такие как имя папки на Google Диске, учетные данные для Mega, текстовые сообщения для приветствия, помощи, уведомлений об авторизации, загрузке и завершении операций. Он также определяет, какие платформы поддерживаются ботом (Openload, Dropbox, Mega).

## Переменные

### `drive_folder_name`

**Описание**: Имя папки на Google Диске, куда бот будет загружать файлы.

### `MEGA_EMAIL`

**Описание**: Email для авторизации в Mega.

### `MEGA_PASSWORD`

**Описание**: Пароль для авторизации в Mega.

### `START`

**Описание**: Приветственное сообщение для пользователя.

### `HELP`

**Описание**: Справочное сообщение с информацией о командах и возможностях бота.

### `DP_DOWNLOAD`

**Описание**: Сообщение о начале загрузки файла с Dropbox.

### `OL_DOWNLOAD`

**Описание**: Сообщение о начале загрузки файла с Openload.

### `PROCESSING`

**Описание**: Сообщение об обработке запроса.

### `DOWN_TWO`

**Описание**: Флаг, определяющий возможность одновременной загрузки двух файлов (не используется в коде).

### `DOWNLOAD`

**Описание**: Сообщение о начале загрузки файла.

### `DOWN_MEGA`

**Описание**: Сообщение о начале загрузки файла с Mega.

### `DOWN_COMPLETE`

**Описание**: Сообщение о завершении загрузки файла.

### `NOT_AUTH`

**Описание**: Сообщение об отсутствии авторизации.

### `REVOKE_FAIL`

**Описание**: Сообщение об ошибке при попытке отмены авторизации.

### `AUTH_SUCC`

**Описание**: Сообщение об успешной авторизации.

### `ALREADY_AUTH`

**Описание**: Сообщение о том, что пользователь уже авторизован.

### `AUTH_URL`

**Описание**: URL для авторизации в Google Drive.

### `UPLOADING`

**Описание**: Сообщение о начале загрузки файла на Google Drive.

### `REVOKE_TOK`

**Описание**: Сообщение об успешной отмене авторизации.

### `DOWN_PATH`

**Описание**: Путь для сохранения загруженных файлов.

### `DOWNLOAD_URL`

**Описание**: Сообщение с информацией об успешной загрузке файла на Google Drive.

### `AUTH_ERROR`

**Описание**: Сообщение об ошибке авторизации.

### `OPENLOAD`

**Описание**: Флаг, определяющий поддержку Openload.

### `DROPBOX`

**Описание**: Флаг, определяющий поддержку Dropbox.

### `MEGA`

**Описание**: Флаг, определяющий поддержку Mega.

### `UPDATE`

**Описание**: Сообщение с информацией об обновлении бота.
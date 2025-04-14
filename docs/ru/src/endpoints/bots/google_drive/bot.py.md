# Модуль для Telegram бота, работающего с Google Drive

## Обзор

Этот модуль содержит код для Telegram-бота, который позволяет пользователям загружать файлы на Google Drive через Telegram. Бот поддерживает авторизацию через Google Auth, загрузку файлов по URL, а также обработку различных типов ссылок, включая Dropbox и Mega.

## Подробней

Модуль использует библиотеку `telegram.ext` для создания и управления Telegram-ботом. Он обрабатывает команды, такие как `/start`, `/help`, `/auth`, `/revoke`, а также сообщения с URL для загрузки файлов. Авторизация пользователя выполняется через Google Auth, с сохранением учетных данных для дальнейшего использования. Для загрузки файлов используются различные методы, включая `wget` и `SmartDL`, а также специфические обработчики для Dropbox и Mega ссылок.

## Классы

### `Creds`

**Описание**: Этот класс содержит учетные данные, такие как токен Telegram бота, email и пароль для Mega.

**Атрибуты**:
- `TG_TOKEN` (str): Токен Telegram бота.
- `MEGA_EMAIL` (str): Email для аккаунта Mega.
- `MEGA_PASSWORD` (str): Пароль для аккаунта Mega.

### `GoogleAuth`

**Описание**: Этот класс используется для управления авторизацией в Google Drive.

**Методы**:
- `LoadCredentialsFile(ID: str)`: Загружает учетные данные из файла.
- `GetAuthUrl() -> str`: Возвращает URL для авторизации.
- `Refresh()`: Обновляет токен доступа, если он истек.
- `Authorize()`: Авторизует с использованием сохраненных учетных данных.
- `Auth(token: str)`: Авторизует с использованием предоставленного токена.
- `SaveCredentialsFile(ID: str)`: Сохраняет учетные данные в файл.

## Функции

### `help`

```python
@run_async
def help(update, context):
    """
    Отправляет пользователю справочное сообщение с описанием доступных команд.

    Args:
        update (telegram.Update): Объект обновления Telegram.
        context (telegram.ext.CallbackContext): Объект контекста Telegram.

    Returns:
        None

    Raises:
        Exception: Если происходит ошибка при отправке сообщения.
    """
    ...
```

**Назначение**: Отправляет пользователю справочное сообщение с описанием доступных команд.

**Параметры**:
- `update` (telegram.Update): Объект обновления Telegram.
- `context` (telegram.ext.CallbackContext): Объект контекста Telegram.

**Как работает функция**:
Функция `help` отправляет пользователю сообщение, содержащее справочную информацию о доступных командах и их использовании. Текст сообщения берется из `TEXT.HELP`.

### `auth`

```python
@run_async
def auth(update, context):
    """
    Обрабатывает команду `/auth`, выполняет авторизацию пользователя в Google Drive.

    Args:
        update (telegram.Update): Объект обновления Telegram.
        context (telegram.ext.CallbackContext): Объект контекста Telegram.

    Returns:
        None
    """
    ...
```

**Назначение**: Обрабатывает команду `/auth`, выполняет авторизацию пользователя в Google Drive.

**Параметры**:
- `update` (telegram.Update): Объект обновления Telegram.
- `context` (telegram.ext.CallbackContext): Объект контекста Telegram.

**Как работает функция**:
Функция `auth` сначала пытается загрузить учетные данные пользователя из файла. Если учетные данные отсутствуют или устарели, функция генерирует URL для авторизации и отправляет его пользователю. Если учетные данные действительны, функция авторизует пользователя и отправляет подтверждающее сообщение.

### `token`

```python
@run_async
def token(update, context):
    """
    Обрабатывает полученный от пользователя токен авторизации и сохраняет его.

    Args:
        update (telegram.Update): Объект обновления Telegram.
        context (telegram.ext.CallbackContext): Объект контекста Telegram.

    Returns:
        None
    """
    ...
```

**Назначение**: Обрабатывает полученный от пользователя токен авторизации и сохраняет его.

**Параметры**:
- `update` (telegram.Update): Объект обновления Telegram.
- `context` (telegram.ext.CallbackContext): Объект контекста Telegram.

**Как работает функция**:
Функция `token` извлекает токен из сообщения пользователя, проверяет его валидность, авторизует пользователя с использованием токена и сохраняет учетные данные в файл.

### `start`

```python
@run_async
def start(update, context):
    """
    Отправляет приветственное сообщение пользователю при запуске бота.

    Args:
        update (telegram.Update): Объект обновления Telegram.
        context (telegram.ext.CallbackContext): Объект контекста Telegram.

    Returns:
        None
    """
    ...
```

**Назначение**: Отправляет приветственное сообщение пользователю при запуске бота.

**Параметры**:
- `update` (telegram.Update): Объект обновления Telegram.
- `context` (telegram.ext.CallbackContext): Объект контекста Telegram.

**Как работает функция**:
Функция `start` отправляет пользователю приветственное сообщение, используя имя пользователя из объекта `update.message.from_user.first_name`. Текст сообщения берется из `TEXT.START`.

### `revoke_tok`

```python
@run_async
def revoke_tok(update, context):
    """
    Удаляет файл с учетными данными пользователя, тем самым отменяя авторизацию.

    Args:
        update (telegram.Update): Объект обновления Telegram.
        context (telegram.ext.CallbackContext): Объект контекста Telegram.

    Returns:
        None
    """
    ...
```

**Назначение**: Удаляет файл с учетными данными пользователя, тем самым отменяя авторизацию.

**Параметры**:
- `update` (telegram.Update): Объект обновления Telegram.
- `context` (telegram.ext.CallbackContext): Объект контекста Telegram.

**Как работает функция**:
Функция `revoke_tok` удаляет файл с учетными данными пользователя, тем самым отменяя авторизацию.

### `UPLOAD`

```python
@run_async
def UPLOAD(update, context):
    """
    Обрабатывает URL, полученный от пользователя, и загружает файл на Google Drive.

    Args:
        update (telegram.Update): Объект обновления Telegram.
        context (telegram.ext.CallbackContext): Объект контекста Telegram.

    Returns:
        None
    """
    ...
```

**Назначение**: Обрабатывает URL, полученный от пользователя, и загружает файл на Google Drive.

**Параметры**:
- `update` (telegram.Update): Объект обновления Telegram.
- `context` (telegram.ext.CallbackContext): Объект контекста Telegram.

**Как работает функция**:
Функция `UPLOAD` извлекает URL из сообщения пользователя, проверяет наличие учетных данных пользователя. Затем, в зависимости от типа ссылки (Dropbox, Mega или обычный URL), использует соответствующий метод для загрузки файла. После успешной загрузки файл отправляется на Google Drive с использованием функции `upload`.

#### Внутренние функции:
Внутри функции `UPLOAD` используются функции `DPBOX` и `wget_dl`, а также методы библиотеки `Mega`.

### `status`

```python
def status(update, context):
    """
    Отправляет сообщение со статусом бота.

    Args:
        update (telegram.Update): Объект обновления Telegram.
        context (telegram.ext.CallbackContext): Объект контекста Telegram.

    Returns:
        None
    """
    ...
```

**Назначение**: Отправляет сообщение со статусом бота.

**Параметры**:
- `update` (telegram.Update): Объект обновления Telegram.
- `context` (telegram.ext.CallbackContext): Объект контекста Telegram.

**Как работает функция**:
Функция `status` отправляет пользователю сообщение, содержащее информацию о статусе бота. Текст сообщения берется из `TEXT.UPDATE`.

## Обработчики

- `start_handler`: Обработчик команды `/start`.
- `downloader_handler`: Обработчик сообщений, содержащих URL.
- `help_handler`: Обработчик команды `/help`.
- `auth_handler`: Обработчик команды `/auth`.
- `token_handler`: Обработчик текстовых сообщений (для получения токена авторизации).
- `revoke_handler`: Обработчик команды `/revoke`.
- `update_status`:  Обработчик команды `/update`.

## Использование

Для запуска бота необходимо установить необходимые библиотеки (`telegram`, `pySmartDL`, `pydrive`, `mega`) и указать токен Telegram бота в классе `Creds`. После этого можно запустить скрипт, и бот будет готов к приему команд и загрузке файлов.
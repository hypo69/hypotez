# Модуль CopilotAccount

## Обзор

Модуль `CopilotAccount` предоставляет класс `CopilotAccount`, который является асинхронным аутентифицированным провайдером для взаимодействия с Copilot. Этот модуль предназначен для работы с аккаунтом Copilot, требующим аутентификации, и использует HAR (HTTP Archive) файлы для получения токена доступа и cookies.

## Подробнее

Модуль является частью проекта `hypotez` и предназначен для интеграции с провайдером Copilot в асинхронном режиме. Он позволяет получать доступ к API Copilot, используя аутентификацию через HAR файлы или через интерактивный логин, если HAR файл недействителен или отсутствует.

## Классы

### `CopilotAccount`

**Описание**: Класс `CopilotAccount` предоставляет функциональность для аутентифицированного доступа к Copilot.

**Наследует**:
- `AsyncAuthedProvider`: Предоставляет базовую структуру для асинхронных аутентифицированных провайдеров.
- `Copilot`: Содержит методы для взаимодействия с API Copilot.

**Атрибуты**:
- `needs_auth` (bool): Указывает, требуется ли аутентификация для использования провайдера (всегда `True`).
- `use_nodriver` (bool): Указывает, использовать ли бездрайверный режим для аутентификации (всегда `True`).
- `parent` (str): Указывает родительский класс ("Copilot").
- `default_model` (str): Модель по умолчанию для Copilot ("Copilot").
- `default_vision_model` (str): Модель по умолчанию для обработки изображений ("Copilot").

**Методы**:
- `on_auth_async`: Асинхронно обрабатывает аутентификацию пользователя.
- `create_authed`: Асинхронно создает аутентифицированный запрос к Copilot.

## Функции

### `cookies_to_dict`

```python
def cookies_to_dict() -> dict:
    """Преобразует cookies в словарь.

    Если `Copilot._cookies` является списком, преобразует его в словарь, где ключами являются имена cookie, а значениями - их значения.
    Если `Copilot._cookies` уже является словарем, возвращает его без изменений.

    Returns:
        dict: Словарь, содержащий cookies.
    """
```

**Назначение**: Преобразует cookies в словарь.

**Возвращает**:
- `dict`: Словарь, содержащий cookies.

**Как работает функция**:
- Проверяет, является ли `Copilot._cookies` экземпляром словаря. Если да, возвращает его.
- Если `Copilot._cookies` является списком, преобразует его в словарь, где ключами являются имена cookie, а значениями - их значения.

**Примеры**:

```python
Copilot._cookies = [{'name': 'cookie1', 'value': 'value1'}, {'name': 'cookie2', 'value': 'value2'}]
cookies = cookies_to_dict()
print(cookies)  # {'cookie1': 'value1', 'cookie2': 'value2'}
```

```python
Copilot._cookies = {'cookie1': 'value1', 'cookie2': 'value2'}
cookies = cookies_to_dict()
print(cookies)  # {'cookie1': 'value1', 'cookie2': 'value2'}
```

### `on_auth_async`

```python
@classmethod
async def on_auth_async(cls, proxy: str = None, **kwargs) -> AsyncIterator:
    """Асинхронно обрабатывает аутентификацию пользователя.

    Пытается прочитать токен доступа и cookies из HAR файла. Если HAR файл недействителен или отсутствует,
    пытается получить их через интерактивный логин, используя `get_access_token_and_cookies`.

    Args:
        proxy (str, optional): Прокси для использования при подключении. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Yields:
        AuthResult: Объект, содержащий токен доступа и cookies.

    Raises:
        NoValidHarFileError: Если не удалось прочитать HAR файл и `has_nodriver` равен `False`.
    """
```

**Назначение**: Асинхронно обрабатывает аутентификацию пользователя.

**Параметры**:
- `proxy` (str, optional): Прокси для использования при подключении. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Yields**:
- `AuthResult`: Объект, содержащий токен доступа и cookies.

**Вызывает исключения**:
- `NoValidHarFileError`: Если не удалось прочитать HAR файл и `has_nodriver` равен `False`.

**Как работает функция**:
1. Пытается прочитать токен доступа и cookies из HAR файла, используя `readHAR(cls.url)`.
2. Если возникает исключение `NoValidHarFileError`:
   - Логирует ошибку.
   - Если `has_nodriver` равен `True`, пытается получить токен доступа и cookies через интерактивный логин, используя `get_access_token_and_cookies(cls.url, proxy)`.
   - Если `has_nodriver` равен `False`, вызывает исключение `NoValidHarFileError`.
3. Возвращает объект `AuthResult`, содержащий токен доступа и cookies.

**Примеры**:

```python
async for result in CopilotAccount.on_auth_async(proxy='http://proxy.example.com'):
    print(result.api_key)
    print(result.cookies)
```

### `create_authed`

```python
@classmethod
async def create_authed(
    cls,
    model: str,
    messages: Messages,
    auth_result: AuthResult,
    **kwargs
) -> AsyncResult:
    """Асинхронно создает аутентифицированный запрос к Copilot.

    Использует предоставленный токен доступа и cookies для создания запроса к API Copilot.

    Args:
        model (str): Модель для использования.
        messages (Messages): Список сообщений для отправки.
        auth_result (AuthResult): Объект, содержащий токен доступа и cookies.
        **kwargs: Дополнительные аргументы.

    Yields:
        str: Части ответа от API Copilot.
    """
```

**Назначение**: Асинхронно создает аутентифицированный запрос к Copilot.

**Параметры**:
- `model` (str): Модель для использования.
- `messages` (Messages): Список сообщений для отправки.
- `auth_result` (AuthResult): Объект, содержащий токен доступа и cookies.
- `**kwargs`: Дополнительные аргументы.

**Yields**:
- `str`: Части ответа от API Copilot.

**Как работает функция**:
1. Устанавливает `Copilot._access_token` и `Copilot._cookies` из объекта `auth_result`.
2. Устанавливает `Copilot.needs_auth` в `cls.needs_auth`.
3. Итерирует по частям ответа от API Copilot, используя `Copilot.create_completion(model, messages, **kwargs)`, и возвращает каждую часть.
4. Обновляет cookies в объекте `auth_result`.

**Примеры**:

```python
auth_result = AuthResult(api_key='test_token', cookies={'cookie1': 'value1'})
async for chunk in CopilotAccount.create_authed(model='test_model', messages=[{'role': 'user', 'content': 'test_message'}], auth_result=auth_result):
    print(chunk)
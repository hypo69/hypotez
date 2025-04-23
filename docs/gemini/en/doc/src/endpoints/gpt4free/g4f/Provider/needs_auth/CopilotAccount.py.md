# Модуль для работы с аккаунтом Copilot
## Обзор

Модуль `CopilotAccount` предназначен для аутентификации и взаимодействия с сервисом Copilot. Он использует HAR-файлы для получения токена доступа и cookie, а также предоставляет асинхронные методы для аутентификации и создания запросов.
Модуль входит в состав проекта `hypotez` и обеспечивает интеграцию с Copilot через асинхронные запросы и аутентификацию.

## Более подробно

Модуль `CopilotAccount` расширяет функциональность `AsyncAuthedProvider` и `Copilot`, предоставляя механизм для автоматической аутентификации и получения токена доступа. Он использует HAR-файлы для получения необходимой информации и поддерживает ручной ввод URL для логина через `RequestLogin`.

## Классы

### `CopilotAccount`

**Описание**: Класс для аутентификации и работы с аккаунтом Copilot.
**Наследует**:
- `AsyncAuthedProvider`: Предоставляет базовую структуру для асинхронных провайдеров с аутентификацией.
- `Copilot`: Содержит методы для взаимодействия с Copilot API.

**Атрибуты**:
- `needs_auth` (bool): Указывает, требуется ли аутентификация. Всегда `True`.
- `use_nodriver` (bool): Указывает, использовать ли бездрайверный режим. Всегда `True`.
- `parent` (str): Имя родительского провайдера. Всегда `"Copilot"`.
- `default_model` (str): Модель, используемая по умолчанию. Всегда `"Copilot"`.
- `default_vision_model` (str): Модель для обработки изображений, используемая по умолчанию. Всегда `"Copilot"`.

**Принцип работы**:
1. Класс использует HAR-файлы для получения токена доступа и cookie.
2. Если HAR-файл недействителен или отсутствует, класс пытается получить токен и cookie через `get_access_token_and_cookies`.
3. После успешной аутентификации класс может создавать запросы к Copilot API.

### Методы

- `on_auth_async`
- `create_authed`
- `cookies_to_dict`

## Функции

### `cookies_to_dict`

```python
def cookies_to_dict() -> dict:
    """Преобразует cookies в словарь.

    Функция преобразует cookies, хранящиеся в `Copilot._cookies`, в словарь.

    Returns:
        dict: Словарь, содержащий имена cookies в качестве ключей и их значения в качестве значений.
    """
    return Copilot._cookies if isinstance(Copilot._cookies, dict) else {c.name: c.value for c in Copilot._cookies}
```

### `on_auth_async`

```python
@classmethod
async def on_auth_async(cls, proxy: str = None, **kwargs) -> AsyncIterator:
    """Асинхронно аутентифицирует пользователя и получает токен доступа.

    Функция пытается прочитать токен доступа и cookies из HAR-файла. Если HAR-файл не найден или недействителен,
    она запрашивает URL для логина и пытается получить токен и cookies с использованием `get_access_token_and_cookies`.

    Args:
        proxy (str, optional): Прокси-сервер для использования при запросе. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Yields:
        AuthResult: Объект, содержащий токен доступа и cookies.
        RequestLogin: Объект, содержащий URL для логина, если требуется ручной ввод данных.

    Raises:
        NoValidHarFileError: Если не удалось прочитать HAR-файл и `has_nodriver` равно `False`.
    """
    try:
        Copilot._access_token, Copilot._cookies = readHAR(cls.url)
    except NoValidHarFileError as h:
        debug.log(f"Copilot: {h}")
        if has_nodriver:
            yield RequestLogin(cls.label, os.environ.get("G4F_LOGIN_URL", ""))
            Copilot._access_token, Copilot._cookies = await get_access_token_and_cookies(cls.url, proxy)
        else:
            raise h
    yield AuthResult(
        api_key=Copilot._access_token,
        cookies=cookies_to_dict()
    )
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
    """Создает аутентифицированный запрос к Copilot API.

    Функция устанавливает токен доступа и cookies из объекта `auth_result` и создает запрос к Copilot API с использованием `Copilot.create_completion`.

    Args:
        model (str): Имя модели для использования.
        messages (Messages): Список сообщений для отправки в запросе.
        auth_result (AuthResult): Объект, содержащий токен доступа и cookies.
        **kwargs: Дополнительные аргументы для `Copilot.create_completion`.

    Yields:
        str: Части ответа от Copilot API.
    """
    Copilot._access_token = getattr(auth_result, "api_key")
    Copilot._cookies = getattr(auth_result, "cookies")
    Copilot.needs_auth = cls.needs_auth
    for chunk in Copilot.create_completion(model, messages, **kwargs):
        yield chunk
    auth_result.cookies = cookies_to_dict()
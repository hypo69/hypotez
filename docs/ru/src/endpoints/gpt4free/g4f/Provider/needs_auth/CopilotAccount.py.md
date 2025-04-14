# Модуль CopilotAccount

## Обзор

Модуль `CopilotAccount` предоставляет асинхронный способ аутентификации и взаимодействия с Copilot API. Он использует файлы HAR для получения токенов доступа и cookie, а также поддерживает автоматическую аутентификацию через веб-драйвер, если файл HAR недействителен или отсутствует.

## Подробней

Этот модуль является частью проекта `hypotez` и предназначен для обеспечения интеграции с API Copilot, требующим аутентификации. Он предоставляет функциональность для автоматической аутентификации и выполнения запросов к API Copilot.

## Классы

### `CopilotAccount`

**Описание**: Класс `CopilotAccount` является асинхронным провайдером аутентификации для Copilot. Он наследуется от `AsyncAuthedProvider` и `Copilot`.

**Наследует**:
- `AsyncAuthedProvider`: Предоставляет базовую функциональность для асинхронных провайдеров, требующих аутентификации.
- `Copilot`: Содержит методы для взаимодействия с API Copilot.

**Атрибуты**:
- `needs_auth` (bool): Указывает, требуется ли аутентификация для использования провайдера (всегда `True`).
- `use_nodriver` (bool): Указывает, следует ли использовать безголовый веб-драйвер для автоматической аутентификации (всегда `True`).
- `parent` (str): Указывает родительский класс (`"Copilot"`).
- `default_model` (str): Модель, используемая по умолчанию (`"Copilot"`).
- `default_vision_model` (str): Модель для работы с изображениями по умолчанию (`"Copilot"`).

**Методы**:
- `on_auth_async`: Асинхронный метод для аутентификации.
- `create_authed`: Асинхронный метод для создания аутентифицированного запроса.

## Функции

### `cookies_to_dict`

```python
def cookies_to_dict():
    """
    Преобразует cookies в словарь.

    Returns:
        dict: Словарь, содержащий имена и значения cookie.
    """
```

**Назначение**: Преобразует cookies, полученные от Copilot, в формат словаря.

**Возвращает**:
- `dict`: Словарь, где ключами являются имена cookie, а значениями - их значения.

**Как работает функция**:
1. Проверяет, является ли `Copilot._cookies` уже словарем.
2. Если `Copilot._cookies` является списком объектов cookie, преобразует его в словарь.

**Примеры**:
```python
# Пример преобразования cookies в словарь
Copilot._cookies = [{"name": "cookie1", "value": "value1"}, {"name": "cookie2", "value": "value2"}]
cookies_dict = cookies_to_dict()
print(cookies_dict)  # Вывод: {'cookie1': 'value1', 'cookie2': 'value2'}
```

### `CopilotAccount.on_auth_async`

```python
@classmethod
async def on_auth_async(cls, proxy: str = None, **kwargs) -> AsyncIterator:
    """
    Асинхронно аутентифицирует аккаунт Copilot, используя HAR-файл или веб-драйвер.

    Args:
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Yields:
        AuthResult: Результат аутентификации, содержащий токен API и cookie.

    Raises:
        NoValidHarFileError: Если не удалось прочитать или найти HAR-файл.
    """
```

**Назначение**: Выполняет асинхронную аутентификацию для аккаунта Copilot.

**Параметры**:
- `proxy` (str, optional): Прокси-сервер для использования при аутентификации через веб-драйвер. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы, которые могут быть переданы.

**Возвращает**:
- `AsyncIterator[AuthResult]`: Асинхронный итератор, возвращающий результат аутентификации (`AuthResult`), содержащий токен API и cookie.

**Вызывает исключения**:
- `NoValidHarFileError`: Если не удается прочитать или найти HAR-файл, и веб-драйвер не настроен.

**Как работает функция**:

```
A[Чтение HAR-файла]
|
B[Обработка ошибки HAR-файла]
|   Y: да, N: нет
|   /   \
N  /     \  Y
| /       \ |
C[Проверка наличия веб-драйвера]
|
D[Запрос URL для логина]
|
E[Получение токена и cookie через веб-драйвер]
|
F[Результат аутентификации]
```

1. **Чтение HAR-файла**: Пытается прочитать токен доступа и cookie из HAR-файла, используя `Copilot._access_token, Copilot._cookies = readHAR(cls.url)`.
2. **Обработка ошибки HAR-файла**: Если возникает ошибка `NoValidHarFileError` при чтении HAR-файла, выполняется следующее:
   - Логируется сообщение об ошибке с использованием `debug.log(f"Copilot: {h}")`.
   - Проверяется, доступен ли веб-драйвер (`has_nodriver`).
3. **Проверка наличия веб-драйвера**: Если веб-драйвер доступен:
   - Запрашивается URL для логина с использованием `yield RequestLogin(cls.label, os.environ.get("G4F_LOGIN_URL", ""))`.
   - Получаются токен доступа и cookie с использованием веб-драйвера: `Copilot._access_token, Copilot._cookies = await get_access_token_and_cookies(cls.url, proxy)`.
4. **Результат аутентификации**: Возвращает результат аутентификации в виде `AuthResult`, содержащего токен API и cookie, используя `yield AuthResult(api_key=Copilot._access_token, cookies=cookies_to_dict())`.

**Примеры**:
```python
# Пример асинхронной аутентификации
async for result in CopilotAccount.on_auth_async():
    print(result)
```

### `CopilotAccount.create_authed`

```python
@classmethod
async def create_authed(
    cls,
    model: str,
    messages: Messages,
    auth_result: AuthResult,
    **kwargs
) -> AsyncResult:
    """
    Создает аутентифицированный запрос к Copilot.

    Args:
        model (str): Модель для использования.
        messages (Messages): Список сообщений для отправки.
        auth_result (AuthResult): Результат аутентификации.
        **kwargs: Дополнительные аргументы.

    Yields:
        str: Части ответа от API Copilot.
    """
```

**Назначение**: Создает аутентифицированный запрос к API Copilot.

**Параметры**:
- `model` (str): Модель, используемая для запроса.
- `messages` (Messages): Список сообщений, отправляемых в запросе.
- `auth_result` (AuthResult): Результат аутентификации, содержащий токен API и cookie.
- `**kwargs`: Дополнительные аргументы, передаваемые в функцию `Copilot.create_completion`.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, выдающий части ответа от API Copilot.

**Как работает функция**:

```
A[Присвоение токена и cookie]
|
B[Вызов create_completion]
|
C[Обновление cookie]
|
D[Выдача чанков ответа]
```

1. **Присвоение токена и cookie**: Устанавливает токен доступа и cookie из `auth_result` в `Copilot._access_token` и `Copilot._cookies` соответственно.
2. **Вызов `create_completion`**: Вызывает метод `Copilot.create_completion` для создания запроса к API Copilot.
3. **Обновление cookie**: Обновляет cookie в `auth_result` с использованием `auth_result.cookies = cookies_to_dict()`.
4. **Выдача чанков ответа**: Передает части ответа от API Copilot с использованием `yield chunk`.

**Примеры**:
```python
# Пример создания аутентифицированного запроса
messages = [{"role": "user", "content": "Hello, Copilot!"}]
auth_result = AuthResult(api_key="test_token", cookies={"cookie1": "value1"})
async for chunk in CopilotAccount.create_authed(model="default", messages=messages, auth_result=auth_result):
    print(chunk)
# Модуль CopilotAccount

## Обзор

Модуль `CopilotAccount` предоставляет асинхронный аутентифицированный провайдер для взаимодействия с Copilot. Он наследуется от `AsyncAuthedProvider` и `Copilot`, обеспечивая механизмы аутентификации и создания запросов к Copilot. Модуль поддерживает чтение данных аутентификации из HAR-файлов и, при необходимости, использует бездрайверный метод для получения токена доступа и cookies.

## Подробнее

Этот модуль предназначен для автоматизации процесса аутентификации и взаимодействия с Copilot. Он позволяет получать токен доступа и cookies, необходимые для выполнения запросов к Copilot API. Модуль также обеспечивает возможность использования прокси для аутентификации.

## Классы

### `CopilotAccount`

**Описание**: Класс `CopilotAccount` является асинхронным аутентифицированным провайдером для Copilot.

**Наследует**:
- `AsyncAuthedProvider`: Обеспечивает базовую структуру для асинхронных аутентифицированных провайдеров.
- `Copilot`: Предоставляет методы для взаимодействия с Copilot API.

**Атрибуты**:
- `needs_auth` (bool): Указывает, требуется ли аутентификация для использования провайдера (всегда `True`).
- `use_nodriver` (bool): Указывает, использовать ли бездрайверный метод для получения токена доступа и cookies (всегда `True`).
- `parent` (str): Указывает родительский класс ("Copilot").
- `default_model` (str): Модель, используемая по умолчанию ("Copilot").
- `default_vision_model` (str): Модель для обработки изображений по умолчанию (совпадает с `default_model`).

**Принцип работы**:
Класс `CopilotAccount` использует методы из класса `Copilot` для создания запросов к API. Он также реализует логику аутентификации, позволяя получать токен доступа и cookies из HAR-файла или с использованием бездрайверного метода.

### `cookies_to_dict`
**Описание**: Преобразует cookies в словарь.

```python
def cookies_to_dict():
    """Преобразует cookies в словарь.

    Returns:
        dict: Словарь, содержащий имя и значение каждого cookie.
    """
```
Функция проверяет, является ли `Copilot._cookies` словарем. Если да, она возвращает его. В противном случае она преобразует список объектов cookie в словарь, где ключами являются имена cookie, а значениями - их значения.

**Методы класса**:

### `on_auth_async`

```python
@classmethod
async def on_auth_async(cls, proxy: str = None, **kwargs) -> AsyncIterator:
    """Асинхронно выполняет процесс аутентификации.

    Args:
        proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Yields:
        AuthResult: Результат аутентификации с токеном доступа и cookies.
        RequestLogin: Объект запроса на ввод логина, если HAR-файл недействителен и используется бездрайверный метод.

    Raises:
        NoValidHarFileError: Если HAR-файл недействителен и бездрайверный метод не доступен.
    """
```

**Назначение**:
Метод `on_auth_async` асинхронно выполняет процесс аутентификации для получения доступа к Copilot. Он пытается прочитать токен доступа и cookies из HAR-файла. Если HAR-файл недействителен, метод пытается получить токен доступа и cookies с использованием бездрайверного подхода.

**Параметры**:
- `cls`: Ссылка на класс `CopilotAccount`.
- `proxy` (str, optional): Адрес прокси-сервера. По умолчанию `None`.
- `kwargs` (dict): Дополнительные параметры.

**Возвращает**:
- `AsyncIterator[AuthResult | RequestLogin]`: Асинхронный итератор, возвращающий результат аутентификации (`AuthResult`) или запрос на ввод логина (`RequestLogin`).

**Вызывает исключения**:
- `NoValidHarFileError`: Если HAR-файл недействителен и бездрайверный метод не доступен.

**Как работает функция**:
1. **Чтение из HAR-файла**:
   - Метод пытается прочитать токен доступа и cookies из HAR-файла, используя `Copilot._access_token, Copilot._cookies = readHAR(cls.url)`.
   - Если HAR-файл недействителен (`NoValidHarFileError`), выполняется переход к следующему шагу.

2. **Обработка ошибки HAR-файла**:
   - Если `NoValidHarFileError` возникла, метод логирует ошибку с использованием `debug.log(f"Copilot: {h}")`.
   - Проверяется, доступен ли бездрайверный метод (`has_nodriver`).
   - Если бездрайверный метод доступен, метод возвращает `RequestLogin` с URL для ввода логина (берется из переменной окружения `G4F_LOGIN_URL` или пустая строка, если переменная не установлена).
   - Затем метод пытается получить токен доступа и cookies с использованием `Copilot._access_token, Copilot._cookies = await get_access_token_and_cookies(cls.url, proxy)`.
   - Если бездрайверный метод не доступен, метод вызывает исключение `h` (`NoValidHarFileError`).

3. **Возврат результата аутентификации**:
   - Метод возвращает `AuthResult` с токеном доступа (`api_key`) и cookies, преобразованными в словарь.

**Примеры**:

```python
# Пример использования on_auth_async
async for result in CopilotAccount.on_auth_async(proxy="http://proxy.example.com"):
    if isinstance(result, AuthResult):
        print(f"Токен доступа: {result.api_key}")
        print(f"Cookies: {result.cookies}")
    elif isinstance(result, RequestLogin):
        print(f"Требуется логин по адресу: {result.url}")
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
    """Создает аутентифицированный запрос к Copilot.

    Args:
        cls: Ссылка на класс.
        model (str): Модель для использования.
        messages (Messages): Список сообщений для отправки.
        auth_result (AuthResult): Результат аутентификации с токеном доступа и cookies.
        **kwargs: Дополнительные параметры.

    Yields:
        str: Части ответа от Copilot.
    """
```

**Назначение**:
Метод `create_authed` создает аутентифицированный запрос к Copilot API. Он устанавливает токен доступа и cookies из результата аутентификации и отправляет запрос с использованием указанной модели и сообщений.

**Параметры**:
- `cls`: Ссылка на класс `CopilotAccount`.
- `model` (str): Модель для использования.
- `messages` (Messages): Список сообщений для отправки.
- `auth_result` (AuthResult): Результат аутентификации с токеном доступа и cookies.
- `kwargs` (dict): Дополнительные параметры.

**Возвращает**:
- `AsyncResult[str]`: Асинхронный итератор, возвращающий части ответа от Copilot.

**Как работает функция**:
1. **Установка токена доступа и cookies**:
   - Метод устанавливает токен доступа (`Copilot._access_token`) и cookies (`Copilot._cookies`) из объекта `auth_result`.
   - Устанавливает флаг `Copilot.needs_auth` в `cls.needs_auth`.

2. **Создание запроса**:
   - Метод вызывает `Copilot.create_completion(model, messages, **kwargs)` для создания запроса к Copilot API.
   - Он итерируется по частям ответа, возвращаемым `create_completion`, и передает их вызывающей стороне.

3. **Обновление cookies**:
   - После завершения запроса метод обновляет cookies в `auth_result` с текущими значениями из `Copilot._cookies`.

**Примеры**:

```python
# Пример использования create_authed
auth_result = AuthResult(api_key="токен", cookies={"cookie1": "значение1"})
async for chunk in CopilotAccount.create_authed(model="Copilot", messages=[{"role": "user", "content": "Привет"}], auth_result=auth_result):
    print(chunk)
print(f"Обновленные cookies: {auth_result.cookies}")
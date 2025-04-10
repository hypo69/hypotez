# Модуль для работы с Microsoft Copilot
=================================================

Модуль содержит класс :class:`Copilot`, который используется для взаимодействия с Microsoft Copilot API для генерации текста, изображений и предложений.

## Оглавление
- [Обзор](#обзор)
- [Классы](#классы)
    - [Conversation](#conversation)
    - [Copilot](#copilot)
- [Функции](#функции)
    - [get_access_token_and_cookies](#get_access_token_and_cookies)
    - [readHAR](#readhar)
    - [get_clarity](#get_clarity)

## Обзор

Этот модуль обеспечивает взаимодействие с Microsoft Copilot, позволяя генерировать текст и изображения, а также получать предложения. Он использует `curl_cffi` для выполнения HTTP-запросов и WebSocket-соединений, если библиотека доступна, в противном случае использует `nodriver`. Модуль поддерживает стриминг ответов, работу через прокси и аутентификацию с использованием access token и cookies.

## Подробнее

Этот модуль предоставляет класс `Copilot`, который упрощает взаимодействие с API Microsoft Copilot. Он поддерживает получение ответов в режиме стриминга, загрузку изображений и использование различных моделей, таких как "Copilot" и "Think Deeper". Модуль также содержит функции для получения access token и cookies, необходимые для аутентификации.

## Классы

### `Conversation`

**Описание**: Класс для представления объекта беседы с Copilot.

**Наследует**: `JsonConversation`

**Аттрибуты**:
- `conversation_id` (str): Уникальный идентификатор беседы.

**Методы**:
- `__init__(conversation_id: str)`: Инициализирует объект `Conversation` с заданным идентификатором.

### `Copilot`

**Описание**: Класс для взаимодействия с Microsoft Copilot API.

**Наследует**: `AbstractProvider`, `ProviderModelMixin`

**Аттрибуты**:
- `label` (str): Метка провайдера (Microsoft Copilot).
- `url` (str): URL главной страницы Microsoft Copilot.
- `working` (bool): Флаг, указывающий, работает ли провайдер (True).
- `supports_stream` (bool): Флаг, указывающий, поддерживает ли провайдер стриминг ответов (True).
- `default_model` (str): Модель, используемая по умолчанию (Copilot).
- `models` (List[str]): Список поддерживаемых моделей (Copilot, Think Deeper).
- `model_aliases` (Dict[str, str]): Алиасы моделей для удобства использования.
- `websocket_url` (str): URL для установления WebSocket-соединения.
- `conversation_url` (str): URL для управления беседами.
- `_access_token` (str): Access token для аутентификации.
- `_cookies` (dict): Cookies для аутентификации.

**Методы**:
- `create_completion(model: str, messages: Messages, stream: bool = False, proxy: str = None, timeout: int = 900, prompt: str = None, media: MediaListType = None, conversation: BaseConversation = None, return_conversation: bool = False, api_key: str = None, **kwargs) -> CreateResult`: Создает запрос к Copilot и возвращает результат.

## Функции

### `get_access_token_and_cookies`

```python
async def get_access_token_and_cookies(url: str, proxy: str = None, target: str = "ChatAI") -> tuple[str, dict]:
    """
    Асинхронно получает access token и cookies для аутентификации в Copilot.

    Args:
        url (str): URL для получения access token и cookies.
        proxy (str, optional): URL прокси-сервера. По умолчанию None.
        target (str, optional): Цель для access token. По умолчанию "ChatAI".

    Returns:
        tuple[str, dict]: Кортеж, содержащий access token и словарь cookies.
    """
```

**Назначение**: Получение access token и cookies, необходимых для аутентификации в Copilot. Функция использует `nodriver` для запуска браузера и выполнения JavaScript-кода для извлечения access token из localStorage.

**Параметры**:
- `url` (str): URL для получения access token и cookies.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `target` (str, optional): Цель для access token. По умолчанию `"ChatAI"`.

**Возвращает**:
- `tuple[str, dict]`: Кортеж, содержащий access token и словарь cookies.

**Как работает функция**:
1. Запускает браузер с использованием `nodriver` для имитации действий пользователя.
2. Открывает указанный `url` в браузере.
3. Выполняет JavaScript-код для извлечения access token из `localStorage`.
4. Получает cookies из браузера.
5. Закрывает браузер.
6. Возвращает access token и cookies.

ASCII flowchart:

```
A: Запуск браузера
|
B: Открытие URL
|
C: Извлечение access token из localStorage
|
D: Получение cookies
|
E: Закрытие браузера
|
F: Возврат access token и cookies
```

**Примеры**:
```python
import asyncio

async def main():
    url = "https://copilot.microsoft.com"
    access_token, cookies = await get_access_token_and_cookies(url)
    print(f"Access Token: {access_token[:10]}...")
    print(f"Cookies: {cookies}")

if __name__ == "__main__":
    asyncio.run(main())
```

### `readHAR`

```python
def readHAR(url: str) -> tuple[str, dict]:
    """
    Читает .har файлы для извлечения access token и cookies.

    Args:
        url (str): URL для поиска в .har файлах.

    Returns:
        tuple[str, dict]: Кортеж, содержащий access token и словарь cookies.

    Raises:
        NoValidHarFileError: Если access token не найден в .har файлах.
    """
```

**Назначение**: Чтение HAR (HTTP Archive) файлов для извлечения access token и cookies, необходимых для аутентификации.

**Параметры**:
- `url` (str): URL для поиска в HAR файлах.

**Возвращает**:
- `tuple[str, dict]`: Кортеж, содержащий access token и словарь cookies.

**Вызывает исключения**:
- `NoValidHarFileError`: Если access token не найден в HAR файлах.

**Как работает функция**:
1. Получает список HAR файлов с использованием `get_har_files()`.
2. Перебирает HAR файлы и пытается загрузить их содержимое как JSON.
3. Ищет записи, URL которых начинаются с заданного `url`.
4. Извлекает access token из заголовка `authorization` и cookies из запроса.
5. Если access token не найден, вызывает исключение `NoValidHarFileError`.

ASCII flowchart:

```
A: Получение списка HAR файлов
|
B: Перебор HAR файлов
|
C: Загрузка содержимого HAR файла как JSON
|
D: Поиск записей с заданным URL
|
E: Извлечение access token и cookies
|
F: Возврат access token и cookies
```

**Примеры**:
```python
try:
    url = "https://copilot.microsoft.com"
    access_token, cookies = readHAR(url)
    print(f"Access Token: {access_token[:10]}...")
    print(f"Cookies: {cookies}")
except NoValidHarFileError as ex:
    print(f"Error: {ex}")
```

### `get_clarity`

```python
def get_clarity() -> bytes:
    """
    Возвращает закодированное тело запроса для Clarity.

    Returns:
        bytes: Закодированное тело запроса для Clarity.
    """
```

**Назначение**: Возвращает закодированное тело запроса для Clarity, сервиса веб-аналитики.

**Возвращает**:
- `bytes`: Закодированное тело запроса для Clarity.

**Как работает функция**:
1. Определяет закодированную строку в формате base64.
2. Декодирует строку base64 и возвращает результат.

ASCII flowchart:

```
A: Определение закодированной строки
|
B: Декодирование строки base64
|
C: Возврат декодированного тела запроса
```

**Примеры**:
```python
body = get_clarity()
print(f"Clarity body: {body[:10]}...")
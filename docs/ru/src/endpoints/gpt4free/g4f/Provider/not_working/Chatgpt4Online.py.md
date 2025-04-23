# Модуль `Chatgpt4Online.py`

## Обзор

Модуль `Chatgpt4Online.py` предоставляет асинхронный интерфейс для взаимодействия с моделью GPT-4 через веб-сайт chatgpt4online.org. Он позволяет отправлять запросы к API и получать ответы в режиме реального времени. Модуль использует библиотеку `aiohttp` для асинхронных HTTP-запросов и поддерживает использование прокси-серверов.

## Подробней

Модуль предназначен для использования в асинхронных приложениях, где требуется взаимодействие с GPT-4. Он предоставляет класс `Chatgpt4Online`, который реализует методы для отправки запросов и получения ответов в виде асинхронного генератора.

## Классы

### `Chatgpt4Online`

**Описание**: Класс для взаимодействия с API GPT-4 через веб-сайт chatgpt4online.org.

**Наследует**:
- `AsyncGeneratorProvider`: Базовый класс для асинхронных провайдеров, использующих генераторы.

**Атрибуты**:
- `url` (str): URL веб-сайта chatgpt4online.org.
- `api_endpoint` (str): Endpoint API для отправки запросов.
- `working` (bool): Указывает, работает ли провайдер (в данном случае `False`).
- `default_model` (str): Модель, используемая по умолчанию (`gpt-4`).
- `models` (list[str]): Список поддерживаемых моделей (в данном случае только `gpt-4`).

**Методы**:
- `get_nonce(headers: dict) -> str`: Получает nonce (одноразовый код) для авторизации запросов.
- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: Создает асинхронный генератор для отправки запросов и получения ответов.

## Методы класса

### `get_nonce`

```python
async def get_nonce(headers: dict) -> str:
    """ Функция получает nonce (одноразовый код) для авторизации запросов.
    Args:
        headers (dict): Заголовки HTTP-запроса.

    Returns:
        str: Nonce, полученный из API.
    """
```
**Назначение**: Получение nonce (одноразового кода) для авторизации запросов.

**Параметры**:
- `headers` (dict): Заголовки HTTP-запроса.

**Возвращает**:
- `str`: Nonce, полученный из API.

**Как работает функция**:
- Функция `get_nonce` отправляет POST-запрос к API `https://chatgpt4online.org/wp-json/mwai/v1/start_session` для получения nonce.
- Она использует библиотеку `aiohttp` для отправки асинхронного запроса.
- Полученный ответ преобразуется в JSON, и из него извлекается значение ключа `"restNonce"`, которое и возвращается в качестве nonce.

**Примеры**:

```python
headers = {
    "accept": "application/json",
    "content-type": "application/json",
}
nonce = await Chatgpt4Online.get_nonce(headers)
print(nonce)
```

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    **kwargs
) -> AsyncResult:
    """ Функция создает асинхронный генератор для отправки запросов и получения ответов.
    Args:
        cls: Ссылка на класс.
        model (str): Модель для использования (например, "gpt-4").
        messages (Messages): Список сообщений для отправки в запросе.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от API.
    """
```
**Назначение**: Создание асинхронного генератора для отправки запросов и получения ответов от API.

**Параметры**:
- `cls`: Ссылка на класс.
- `model` (str): Модель для использования (например, `"gpt-4"`).
- `messages` (Messages): Список сообщений для отправки в запросе.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий ответы от API.

**Как работает функция**:
1. **Формирование заголовков**:
   - Функция формирует заголовки HTTP-запроса, включая User-Agent, Referer и другие необходимые параметры.
   - Получает `nonce` с помощью метода `cls.get_nonce(headers)` и добавляет его в заголовки.
2. **Создание сессии `aiohttp`**:
   - Создается асинхронная сессия с использованием `aiohttp.ClientSession` и настроенными заголовками.
3. **Форматирование запроса**:
   - Форматирует список сообщений `messages` в строку запроса `prompt` с использованием функции `format_prompt(messages)`.
4. **Подготовка данных для запроса**:
   - Формирует JSON-данные для отправки в запросе, включая `botId`, `newMessage` (с отформатированным запросом) и `stream`.
5. **Отправка POST-запроса**:
   - Отправляет POST-запрос к API (`f"{cls.url}{cls.api_endpoint}"`) с использованием `session.post`.
   - Если указан `proxy`, запрос отправляется через прокси-сервер.
6. **Обработка ответа**:
   - Читает ответ по частям (chunks) из `response.content.iter_any()`.
   - Извлекает JSON-объекты из каждой части, разделяя на строки и проверяя префикс `"data: "` для каждой строки.
   - Если `json_data["type"] == "live"`, добавляет данные (`json_data["data"]`) к `full_response`.
   - Если `json_data["type"] == "end"`, извлекает финальные данные (`final_data["reply"]`) и присваивает их `full_response`.
   - Возвращает `full_response` как результат работы генератора.
7. **Обработка ошибок JSON**:
   - Обрабатывает ошибки `json.JSONDecodeError`, возникающие при разборе JSON, и продолжает обработку.

**Примеры**:

```python
messages = [
    {"role": "user", "content": "Hello, GPT-4!"}
]
async for response in Chatgpt4Online.create_async_generator(model="gpt-4", messages=messages):
    print(response)
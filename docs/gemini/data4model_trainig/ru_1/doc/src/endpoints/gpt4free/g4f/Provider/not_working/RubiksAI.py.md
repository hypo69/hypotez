# Модуль для работы с RubiksAI
================================

Модуль предоставляет класс `RubiksAI`, который используется для взаимодействия с API Rubiks AI для генерации текста с использованием различных моделей.

## Оглавление
- [Обзор](#обзор)
- [Подробнее](#подробнее)
- [Классы](#классы)
    - [RubiksAI](#rubiksai)
- [Методы класса](#методы-класса)
    - [generate_mid](#generate_mid)
    - [create_referer](#create_referer)
    - [create_async_generator](#create_async_generator)

## Обзор

Модуль `RubiksAI` предназначен для асинхронного взаимодействия с API Rubiks AI. Он поддерживает потоковую передачу данных, системные сообщения и историю сообщений. Модуль позволяет выбирать различные модели, такие как `gpt-4o-mini`, `gpt-4o`, `o1-mini`, `claude-3.5-sonnet`, `grok-beta`, `gemini-1.5-pro`, `nova-pro` и `llama-3.1-70b-versatile`.

## Подробнее

Модуль использует `aiohttp` для выполнения асинхронных HTTP-запросов. Он генерирует уникальные идентификаторы (`mid`) для каждого запроса и формирует URL Referer для обеспечения правильной маршрутизации запросов. Поддерживается также использование прокси-серверов и веб-поиска для расширения возможностей генерации текста.

## Классы

### `RubiksAI`

**Описание**: Класс для взаимодействия с API Rubiks AI.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера ("Rubiks AI").
- `url` (str): URL главной страницы Rubiks AI ("https://rubiks.ai").
- `api_endpoint` (str): URL API для отправки запросов ("https://rubiks.ai/search/api/").
- `working` (bool): Указывает, работает ли провайдер (в данном случае `True`).
- `supports_stream` (bool): Поддерживает ли потоковую передачу данных (в данном случае `True`).
- `supports_system_message` (bool): Поддерживает ли системные сообщения (в данном случае `True`).
- `supports_message_history` (bool): Поддерживает ли историю сообщений (в данном случае `True`).
- `default_model` (str): Модель, используемая по умолчанию (`gpt-4o-mini`).
- `models` (list): Список поддерживаемых моделей.
- `model_aliases` (dict): Словарь псевдонимов моделей.

**Принцип работы**:
Класс `RubiksAI` использует асинхронный генератор для отправки запросов к API Rubiks AI и получения ответов. Он генерирует уникальные идентификаторы `mid` и URL Referer для каждого запроса. Поддерживается потоковая передача данных, что позволяет получать ответы в режиме реального времени.

## Методы класса

### `generate_mid`

```python
@staticmethod
def generate_mid() -> str:
    """
    Generates a 'mid' string following the pattern:
    6 characters - 4 characters - 4 characters - 4 characters - 12 characters
    Example: 0r7v7b-quw4-kdy3-rvdu-ekief6xbuuq4
    """
    ...
```

**Назначение**: Генерирует строку `mid` в формате `6 символов - 4 символа - 4 символа - 4 символа - 12 символов`.

**Возвращает**:
- `str`: Строка `mid`.

**Как работает функция**:
Функция генерирует пять частей строки `mid`, используя случайные символы из `string.ascii_lowercase` и `string.digits`. Затем соединяет эти части дефисами.

**Примеры**:
```python
>>> RubiksAI.generate_mid()
'a1b2c3-d4e5-f6g7-h8i9-j0k1l2m3n4o5'
```

### `create_referer`

```python
@staticmethod
def create_referer(q: str, mid: str, model: str = '') -> str:
    """
    Creates a Referer URL with dynamic q and mid values, using urlencode for safe parameter encoding.
    """
    ...
```

**Назначение**: Создает URL Referer с динамическими значениями `q` (запрос) и `mid` (идентификатор), используя `urlencode` для безопасного кодирования параметров.

**Параметры**:
- `q` (str): Строка запроса.
- `mid` (str): Идентификатор запроса.
- `model` (str, optional): Модель, используемая в запросе. По умолчанию ''.

**Возвращает**:
- `str`: URL Referer.

**Как работает функция**:
Функция создает словарь с параметрами `q`, `model` и `mid`, кодирует их с помощью `urlencode` и формирует URL Referer.

**Примеры**:
```python
>>> RubiksAI.create_referer(q='test query', mid='12345-6789-0abc-def0-123456789abc', model='gpt-4o-mini')
'https://rubiks.ai/search/?q=test+query&model=gpt-4o-mini&mid=12345-6789-0abc-def0-123456789abc'
```

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    web_search: bool = False,
    temperature: float = 0.6,
    **kwargs
) -> AsyncResult:
    """
    Creates an asynchronous generator that sends requests to the Rubiks AI API and yields the response.

    Parameters:
    - model (str): The model to use in the request.
    - messages (Messages): The messages to send as a prompt.
    - proxy (str, optional): Proxy URL, if needed.
    - web_search (bool, optional): Indicates whether to include search sources in the response. Defaults to False.
    """
    ...
```

**Назначение**: Создает асинхронный генератор, который отправляет запросы к API Rubiks AI и возвращает ответы.

**Параметры**:
- `model` (str): Модель для использования в запросе.
- `messages` (Messages): Сообщения для отправки в качестве запроса.
- `proxy` (str, optional): URL прокси-сервера, если необходимо. По умолчанию `None`.
- `web_search` (bool, optional): Указывает, следует ли включать источники поиска в ответ. По умолчанию `False`.
- `temperature` (float): Параметр температуры для управления случайностью генерации. По умолчанию `0.6`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий текст ответа.

**Как работает функция**:
Функция выполняет следующие шаги:
1. Получает модель из `cls.get_model(model)`.
2. Генерирует `mid_value` с помощью `cls.generate_mid()`.
3. Создает `referer` с помощью `cls.create_referer()`.
4. Формирует данные для запроса, включая сообщения, модель, параметры поиска и потоковой передачи.
5. Устанавливает заголовки запроса, включая `Referer` и `User-Agent`.
6. Отправляет асинхронный POST-запрос к API Rubiks AI.
7. Обрабатывает ответ, извлекая данные из потока событий (`text/event-stream`).
8. Извлекает источники (`url` и `title`) при включенном `web_search`.
9. Возвращает сгенерированный контент и источники (если `web_search` включен).

**Внутренние функции**:
- Отсутствуют внутренние функции.

**Примеры**:
```python
messages = [{"role": "user", "content": "Hello, how are you?"}]
async for message in RubiksAI.create_async_generator(model='gpt-4o-mini', messages=messages):
    print(message)
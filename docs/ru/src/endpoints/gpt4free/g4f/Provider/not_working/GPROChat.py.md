# Модуль GPROChat

## Обзор

Модуль `GPROChat` предназначен для асинхронного взаимодействия с сервисом gprochat.com. Он предоставляет функциональность для генерации текста на основе модели `gemini-1.5-pro` или других, поддерживаемых сервисом, с использованием API gprochat.com. Модуль поддерживает потоковую передачу данных и сохранение истории сообщений.

## Подробнее

Модуль определяет класс `GPROChat`, который наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`. Класс реализует методы для формирования запросов к API, включая генерацию подписи для аутентификации. Он использует `aiohttp` для асинхронных HTTP-запросов и предоставляет результаты в виде асинхронного генератора.

## Классы

### `GPROChat`

**Описание**: Класс для взаимодействия с сервисом GPROChat.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую структуру для асинхронных провайдеров генераторов.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `url` (str): URL сервиса GPROChat (`https://gprochat.com`).
- `api_endpoint` (str): URL API для генерации текста (`https://gprochat.com/api/generate`).
- `working` (bool): Флаг, указывающий на работоспособность провайдера (по умолчанию `False`).
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи данных (по умолчанию `True`).
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений (по умолчанию `True`).
- `default_model` (str): Модель, используемая по умолчанию (`gemini-1.5-pro`).

**Методы**:
- `generate_signature(timestamp: int, message: str) -> str`: Генерирует подпись для запроса к API.
- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: Создает асинхронный генератор для получения ответов от API.

## Функции

### `generate_signature`

```python
@staticmethod
def generate_signature(timestamp: int, message: str) -> str:
    """Генерирует подпись для запроса к API.

    Args:
        timestamp (int): Временная метка (timestamp) запроса.
        message (str): Сообщение, для которого генерируется подпись.

    Returns:
        str: Сгенерированная подпись.
    """
    ...
```

**Назначение**: Генерирует подпись для запроса к API, используя алгоритм SHA256.

**Параметры**:
- `timestamp` (int): Временная метка (timestamp) запроса.
- `message` (str): Сообщение, для которого генерируется подпись.

**Возвращает**:
- `str`: Сгенерированная подпись.

**Как работает функция**:
1.  Функция принимает временную метку (`timestamp`) и сообщение (`message`) в качестве входных данных.
2.  Определяет секретный ключ `secret_key`.
3.  Формирует строку `hash_input` путем конкатенации `timestamp`, `message` и `secret_key`, разделенных двоеточиями.
4.  Вычисляет SHA256-хеш строки `hash_input` в кодировке UTF-8.
5.  Возвращает полученный хеш в шестнадцатеричном формате.

```
Timestamp + Message:Secret Key -> Hash Input
|
SHA256 (Hash Input)
|
Hex Digest
|
Signature
```

**Примеры**:

```python
timestamp = int(time.time() * 1000)
message = "Пример сообщения"
signature = GPROChat.generate_signature(timestamp, message)
print(f"Signature: {signature}")
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
    """Создает асинхронный генератор для получения ответов от API.

    Args:
        model (str): Название модели для генерации текста.
        messages (Messages): Список сообщений для отправки в API.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий части ответа от API.
    """
    ...
```

**Назначение**: Создает асинхронный генератор для взаимодействия с API GPROChat.

**Параметры**:
- `model` (str): Название модели для генерации текста.
- `messages` (Messages): Список сообщений для отправки в API.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий части ответа от API.

**Как работает функция**:
1.  Функция принимает название модели (`model`), список сообщений (`messages`) и, опционально, URL прокси-сервера (`proxy`).
2.  Получает название модели, используя метод `cls.get_model(model)`.
3.  Генерирует временную метку `timestamp`.
4.  Форматирует сообщения, используя функцию `format_prompt(messages)`.
5.  Генерирует подпись `sign`, используя метод `cls.generate_signature(timestamp, prompt)`.
6.  Формирует заголовки `headers` для HTTP-запроса.
7.  Формирует данные `data` для отправки в API, включая сообщения, временную метку и подпись.
8.  Отправляет асинхронный POST-запрос к API `cls.api_endpoint` с использованием `aiohttp.ClientSession`.
9.  Получает ответ от API и итерируется по частям ответа, декодируя их и передавая в генератор.
10. В случае возникновения ошибки, вызывается исключение `response.raise_for_status()`.

```
Модель, Сообщения, Прокси -> Входные параметры
|
Получение имени модели -> get_model(model)
|
Генерация временной метки -> timestamp
|
Форматирование сообщений -> format_prompt(messages)
|
Генерация подписи -> generate_signature(timestamp, prompt)
|
Формирование заголовков -> headers
|
Формирование данных -> data
|
Асинхронный POST-запрос -> ClientSession.post(api_endpoint, data, proxy)
|
Итерация по частям ответа -> chunk.decode()
|
Вывод: Части ответа через генератор
```

**Примеры**:

```python
messages = [{"role": "user", "content": "Привет!"}]
async for chunk in GPROChat.create_async_generator(model="gemini-1.5-pro", messages=messages):
    print(chunk, end="")
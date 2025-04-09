# Модуль `OpenaiTemplate.py`

## Обзор

Модуль `OpenaiTemplate.py` предоставляет базовый класс `OpenaiTemplate` для взаимодействия с API OpenAI. Он поддерживает как генерацию текста, так и генерацию изображений, а также работу с инструментами (tools). Модуль содержит функциональность для получения списка доступных моделей, создания асинхронного генератора для обработки запросов и формирования заголовков запросов.

## Подробней

Этот модуль является шаблоном для реализации провайдеров, использующих API OpenAI. Он предоставляет общую логику для аутентификации, обработки ошибок, формирования запросов и парсинга ответов. Класс `OpenaiTemplate` наследует от `AsyncGeneratorProvider`, `ProviderModelMixin` и `RaiseErrorMixin`, что обеспечивает поддержку асинхронной генерации, получения списка моделей и обработки ошибок. Расположение файла в структуре проекта указывает на его роль как одного из шаблонов для работы с различными API, в данном случае, OpenAI.

## Классы

### `OpenaiTemplate`

**Описание**: Базовый класс для провайдеров, использующих API OpenAI. Предоставляет функциональность для взаимодействия с API, включая получение списка моделей, создание асинхронного генератора и формирование заголовков запросов.

**Принцип работы**:
Класс `OpenaiTemplate` предназначен для упрощения интеграции с API OpenAI. Он предоставляет методы для получения списка доступных моделей, создания асинхронного генератора для обработки запросов и формирования заголовков запросов. Класс также поддерживает обработку ошибок и логирование.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает поддержку асинхронной генерации.
- `ProviderModelMixin`: Предоставляет методы для получения списка моделей.
- `RaiseErrorMixin`: Обеспечивает обработку ошибок.

**Аттрибуты**:
- `api_base` (str): Базовый URL API OpenAI. По умолчанию пустая строка.
- `api_key` (str | None): Ключ API OpenAI. По умолчанию `None`.
- `api_endpoint` (str | None): Конечная точка API OpenAI. По умолчанию `None`.
- `supports_message_history` (bool): Поддержка истории сообщений. По умолчанию `True`.
- `supports_system_message` (bool): Поддержка системных сообщений. По умолчанию `True`.
- `default_model` (str): Модель, используемая по умолчанию. По умолчанию пустая строка.
- `fallback_models` (list[str]): Список моделей, используемых в случае ошибки. По умолчанию пустой список.
- `sort_models` (bool): Флаг, указывающий, нужно ли сортировать модели. По умолчанию `True`.
- `ssl` (bool | None): Параметр для проверки SSL сертификата. По умолчанию `None`.

**Методы**:
- `get_models()`: Возвращает список доступных моделей.
- `create_async_generator()`: Создает асинхронный генератор для обработки запросов.
- `get_headers()`: Формирует заголовки запроса.

## Функции

### `get_models`

```python
@classmethod
def get_models(cls, api_key: str = None, api_base: str = None) -> list[str]:
    """
    Возвращает список доступных моделей.

    Args:
        api_key (str, optional): Ключ API OpenAI. По умолчанию `None`.
        api_base (str, optional): Базовый URL API OpenAI. По умолчанию `None`.

    Returns:
        list[str]: Список доступных моделей.
    """
```

**Назначение**: Получение списка доступных моделей из API OpenAI.

**Параметры**:
- `api_key` (str, optional): Ключ API OpenAI. Если не указан, используется значение атрибута класса `cls.api_key`. По умолчанию `None`.
- `api_base` (str, optional): Базовый URL API OpenAI. Если не указан, используется значение атрибута класса `cls.api_base`. По умолчанию `None`.

**Возвращает**:
- `list[str]`: Список доступных моделей. В случае ошибки возвращает `cls.fallback_models`.

**Вызывает исключения**:
- `Exception`: В случае возникновения ошибки при выполнении запроса к API.

**Как работает функция**:

1. **Проверка наличия моделей в кэше**:
   - Функция сначала проверяет, были ли уже загружены модели (`if not cls.models`). Если модели уже загружены, функция возвращает их из кэша, чтобы избежать повторных запросов к API.

2. **Инициализация заголовков запроса**:
   - Создается словарь `headers` для хранения заголовков запроса.

3. **Определение базового URL и ключа API**:
   - Если `api_base` не предоставлен, используется значение по умолчанию из атрибута класса `cls.api_base`. Аналогично, если `api_key` не предоставлен, используется значение из `cls.api_key`.

4. **Добавление ключа API в заголовки**:
   - Если `api_key` предоставлен, он добавляется в заголовок `Authorization` в формате `Bearer <api_key>`.

5. **Выполнение запроса к API**:
   - Выполняется GET-запрос к эндпоинту `/models` API OpenAI. Используются предоставленные заголовки и параметры проверки SSL (`cls.ssl`).

6. **Обработка ответа**:
   - Проверяется статус ответа с помощью `raise_for_status(response)`, чтобы убедиться, что запрос выполнен успешно (код 200 OK).
   - Преобразует JSON-ответ в структуру данных Python.
   - Извлекает список моделей из поля `data` в ответе.
   - Разделяет список моделей на `image_models` и `models` в зависимости от наличия поля `image` в данных модели.

7. **Сортировка моделей**:
   - Если `cls.sort_models` имеет значение `True`, список моделей сортируется.

8. **Обработка ошибок**:
   - Если во время выполнения запроса или обработки ответа возникает исключение, оно логируется с использованием `debug.error(e)`, и функция возвращает `cls.fallback_models`.

9. **Возврат списка моделей**:
   - Если все прошло успешно, функция возвращает список доступных моделей (`cls.models`).

**ASCII flowchart**:

```
A: Проверка cls.models
|
No
B: Инициализация headers
|
C: Определение api_base и api_key
|
D: Добавление api_key в headers (если есть)
|
E: GET запрос к /models
|
F: Обработка ответа (извлечение data, image_models, models)
|
G: Сортировка моделей (если cls.sort_models)
|
Yes
H: Возврат cls.models
|
I: Обработка ошибок (логирование, возврат fallback_models)
```

**Примеры**:

```python
# Пример 1: Получение списка моделей без указания api_key и api_base
models = OpenaiTemplate.get_models()
print(models)
# > ['gpt-3.5-turbo', 'gpt-4', ...]

# Пример 2: Получение списка моделей с указанием api_key и api_base
models = OpenaiTemplate.get_models(api_key="YOUR_API_KEY", api_base="https://api.openai.com/v1")
print(models)
# > ['gpt-3.5-turbo', 'gpt-4', ...]

# Пример 3: Получение списка моделей при возникновении ошибки
# (В данном примере имитируется ошибка путем указания неверного api_base)
models = OpenaiTemplate.get_models(api_key="YOUR_API_KEY", api_base="https://api.openai.com/v1_invalid")
print(models)
# > []  # Возвращается fallback_models
```

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    timeout: int = 120,
    media: MediaListType = None,
    api_key: str = None,
    api_endpoint: str = None,
    api_base: str = None,
    temperature: float = None,
    max_tokens: int = None,
    top_p: float = None,
    stop: Union[str, list[str]] = None,
    stream: bool = False,
    prompt: str = None,
    headers: dict = None,
    impersonate: str = None,
    extra_parameters: list[str] = ["tools", "parallel_tool_calls", "tool_choice", "reasoning_effort", "logit_bias", "modalities", "audio"],
    extra_data: dict = {},
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для обработки запросов к API OpenAI.

    Args:
        model (str): Имя используемой модели.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        timeout (int, optional): Максимальное время ожидания запроса в секундах. По умолчанию 120.
        media (MediaListType, optional): Список медиафайлов для отправки. По умолчанию `None`.
        api_key (str, optional): Ключ API OpenAI. По умолчанию `None`.
        api_endpoint (str, optional): Конечная точка API OpenAI. По умолчанию `None`.
        api_base (str, optional): Базовый URL API OpenAI. По умолчанию `None`.
        temperature (float, optional): Температура генерации. По умолчанию `None`.
        max_tokens (int, optional): Максимальное количество токенов в ответе. По умолчанию `None`.
        top_p (float, optional): Параметр top_p. По умолчанию `None`.
        stop (Union[str, list[str]], optional): Список стоп-слов. По умолчанию `None`.
        stream (bool, optional): Флаг, указывающий, использовать ли потоковую передачу. По умолчанию `False`.
        prompt (str, optional): Дополнительный промпт. По умолчанию `None`.
        headers (dict, optional): Дополнительные заголовки запроса. По умолчанию `None`.
        impersonate (str, optional): Имя пользователя для имитации. По умолчанию `None`.
        extra_parameters (list[str], optional): Список дополнительных параметров.
        extra_data (dict, optional): Дополнительные данные. По умолчанию `{}`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор для обработки запросов.

    Raises:
        MissingAuthError: Если отсутствует ключ API и требуется аутентификация.
        ResponseError: Если получен неподдерживаемый content-type ответа.
    """
```

**Назначение**: Создание асинхронного генератора для взаимодействия с API OpenAI. Функция обрабатывает текстовые и графические запросы, поддерживает потоковую передачу данных и инструменты (tools).

**Параметры**:
- `model` (str): Имя используемой модели.
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `timeout` (int, optional): Максимальное время ожидания запроса в секундах. По умолчанию 120.
- `media` (MediaListType, optional): Список медиафайлов для отправки. По умолчанию `None`.
- `api_key` (str, optional): Ключ API OpenAI. По умолчанию `None`.
- `api_endpoint` (str, optional): Конечная точка API OpenAI. По умолчанию `None`.
- `api_base` (str, optional): Базовый URL API OpenAI. По умолчанию `None`.
- `temperature` (float, optional): Температура генерации. По умолчанию `None`.
- `max_tokens` (int, optional): Максимальное количество токенов в ответе. По умолчанию `None`.
- `top_p` (float, optional): Параметр top_p. По умолчанию `None`.
- `stop` (Union[str, list[str]], optional): Список стоп-слов. По умолчанию `None`.
- `stream` (bool, optional): Флаг, указывающий, использовать ли потоковую передачу. По умолчанию `False`.
- `prompt` (str, optional): Дополнительный промпт. По умолчанию `None`.
- `headers` (dict, optional): Дополнительные заголовки запроса. По умолчанию `None`.
- `impersonate` (str, optional): Имя пользователя для имитации. По умолчанию `None`.
- `extra_parameters` (list[str], optional): Список дополнительных параметров, таких как `tools`, `parallel_tool_calls`, `tool_choice`, `reasoning_effort`, `logit_bias`, `modalities`, `audio`.
- `extra_data` (dict, optional): Дополнительные данные. По умолчанию `{}`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор для обработки запросов.

**Вызывает исключения**:
- `MissingAuthError`: Если отсутствует ключ API и требуется аутентификация.
- `ResponseError`: Если получен неподдерживаемый `content-type` ответа.

**Как работает функция**:

1. **Инициализация параметров**:
   - Проверяет и устанавливает `api_key`, используя значение, переданное явно или из атрибута класса `cls.api_key`.
   - Проверяет необходимость аутентификации (`cls.needs_auth`) и наличие `api_key`. Если ключ отсутствует и аутентификация требуется, вызывает исключение `MissingAuthError`.

2. **Создание асинхронной сессии**:
   - Создает асинхронную сессию `StreamSession` для выполнения HTTP-запросов с использованием прокси, заголовков и таймаута.

3. **Определение модели**:
   - Получает имя модели с использованием `cls.get_model()`, передавая `model`, `api_key` и `api_base`.

4. **Обработка запросов на генерацию изображений**:
   - Проверяет, входит ли выбранная модель в список моделей для генерации изображений (`cls.image_models`).
   - Если модель поддерживает генерацию изображений, формирует данные запроса (`data`) с использованием `prompt` и выполняет POST-запрос к эндпоинту `/images/generations`.
   - Обрабатывает ответ, извлекая URL-адреса сгенерированных изображений и возвращая их в виде `ImageResponse`.

5. **Обработка текстовых запросов**:
   - Формирует данные запроса (`data`) для текстовых запросов, включая сообщения, модель, температуру, максимальное количество токенов, `top_p`, стоп-слова и другие параметры.
   - Определяет `api_endpoint`, используя значение, переданное явно или из атрибута класса `cls.api_endpoint`.
   - Выполняет POST-запрос к эндпоинту `/chat/completions` (или другому, если указан `api_endpoint`).

6. **Обработка потоковых и не потоковых ответов**:
   - Проверяет `content-type` ответа, чтобы определить, является ли он `application/json` (не потоковый) или `text/event-stream` (потоковый).
   - **Для `application/json`**:
     - Извлекает содержимое сообщения, вызовы инструментов (`tool_calls`), информацию об использовании (`usage`) и причину завершения (`finish_reason`) из ответа.
     - Возвращает эти данные через генератор.
   - **Для `text/event-stream`**:
     - Обрабатывает каждое SSE-сообщение (Server-Sent Events).
     - Извлекает дельту содержимого, информацию об использовании и причину завершения из каждого сообщения.
     - Возвращает дельту содержимого через генератор, удаляя начальные пробелы из первого сообщения.

7. **Обработка ошибок**:
   - Если `content-type` не поддерживается, вызывает исключение `ResponseError`.
   - В случае ошибок в API OpenAI, вызывает `cls.raise_error` для обработки и логирования ошибки.

**ASCII flowchart**:

```
A: Инициализация api_key
|
B: Проверка needs_auth и api_key
|
C: Создание StreamSession
|
D: Определение model
|
E: Проверка model in cls.image_models
|
Yes
F: Формирование data для генерации изображений
|
G: POST запрос к /images/generations
|
H: Обработка ответа (ImageResponse)
|
No
I: Формирование data для текстовых запросов
|
J: Определение api_endpoint
|
K: POST запрос к /chat/completions
|
L: Проверка content-type
|
application/json
M: Извлечение content, tool_calls, usage, finish_reason
|
N: Выдача данных через генератор
|
text/event-stream
O: Обработка SSE-сообщений
|
P: Извлечение delta, usage, finish_reason
|
Q: Выдача delta через генератор
|
other
R: Вызов ResponseError
```

**Примеры**:

```python
# Пример 1: Создание асинхронного генератора для текстового запроса
messages = [{"role": "user", "content": "Напиши короткий рассказ."}]
async def main():
    async for chunk in OpenaiTemplate.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        print(chunk, end="")

# Пример 2: Создание асинхронного генератора для запроса с использованием прокси
messages = [{"role": "user", "content": "Напиши короткий рассказ."}]
async def main():
    async for chunk in OpenaiTemplate.create_async_generator(model="gpt-3.5-turbo", messages=messages, proxy="http://your-proxy:8080"):
        print(chunk, end="")

# Пример 3: Создание асинхронного генератора для запроса с указанием температуры
messages = [{"role": "user", "content": "Напиши короткий рассказ."}]
async def main():
    async for chunk in OpenaiTemplate.create_async_generator(model="gpt-3.5-turbo", messages=messages, temperature=0.7):
        print(chunk, end="")
```

### `get_headers`

```python
@classmethod
def get_headers(cls, stream: bool, api_key: str = None, headers: dict = None) -> dict:
    """
    Формирует заголовки запроса.

    Args:
        stream (bool): Флаг, указывающий, использовать ли потоковую передачу.
        api_key (str, optional): Ключ API OpenAI. По умолчанию `None`.
        headers (dict, optional): Дополнительные заголовки запроса. По умолчанию `None`.

    Returns:
        dict: Словарь с заголовками запроса.
    """
```

**Назначение**: Формирование заголовков запроса для API OpenAI.

**Параметры**:
- `stream` (bool): Флаг, указывающий, использовать ли потоковую передачу.
- `api_key` (str, optional): Ключ API OpenAI. Если не указан, используется значение по умолчанию. По умолчанию `None`.
- `headers` (dict, optional): Дополнительные заголовки запроса. По умолчанию `None`.

**Возвращает**:
- `dict`: Словарь с заголовками запроса.

**Как работает функция**:

1. **Определение Accept**:
   - Устанавливает заголовок `Accept` в зависимости от параметра `stream`. Если `stream` равен `True`, то `Accept` устанавливается в `text/event-stream`, иначе в `application/json`.

2. **Установка Content-Type**:
   - Устанавливает заголовок `Content-Type` в `application/json`.

3. **Добавление Authorization (если api_key предоставлен)**:
   - Если `api_key` предоставлен, добавляет заголовок `Authorization` в формате `Bearer <api_key>`.

4. **Объединение заголовков**:
   - Объединяет базовые заголовки с дополнительными заголовками, переданными в параметре `headers`. Если `headers` не предоставлен, используется пустой словарь.

**ASCII flowchart**:

```
A: Определение Accept (stream=True -> text/event-stream, stream=False -> application/json)
|
B: Установка Content-Type (application/json)
|
C: Проверка api_key
|
Yes
D: Добавление Authorization (Bearer <api_key>)
|
No
E: Объединение заголовков (базовые + headers)
|
F: Возврат словаря с заголовками
```

**Примеры**:

```python
# Пример 1: Получение заголовков для потокового запроса без api_key
headers = OpenaiTemplate.get_headers(stream=True)
print(headers)
# > {'Accept': 'text/event-stream', 'Content-Type': 'application/json'}

# Пример 2: Получение заголовков для не потокового запроса с api_key
headers = OpenaiTemplate.get_headers(stream=False, api_key="YOUR_API_KEY")
print(headers)
# > {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer YOUR_API_KEY'}

# Пример 3: Получение заголовков с дополнительными заголовками
headers = OpenaiTemplate.get_headers(stream=True, api_key="YOUR_API_KEY", headers={"X-Custom-Header": "value"})
print(headers)
# > {'Accept': 'text/event-stream', 'Content-Type': 'application/json', 'Authorization': 'Bearer YOUR_API_KEY', 'X-Custom-Header': 'value'}
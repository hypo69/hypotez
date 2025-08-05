# Модуль OpenaiTemplate

## Обзор

Модуль `OpenaiTemplate` предоставляет реализацию класса `OpenaiTemplate`, который служит провайдером для взаимодействия с OpenAI API, предоставляя доступ к различным моделям OpenAI, включая модели для генерации текста и изображений.

## Подробнее

Класс `OpenaiTemplate` наследует от `AsyncGeneratorProvider`, `ProviderModelMixin` и `RaiseErrorMixin`, что позволяет ему предоставлять асинхронный генератор для обработки запросов к OpenAI API, а также управлять моделями OpenAI и обрабатывать ошибки.

## Классы

### `class OpenaiTemplate`

**Описание**: Класс `OpenaiTemplate` предоставляет реализацию провайдера для взаимодействия с OpenAI API.

**Наследует**:
- `AsyncGeneratorProvider`
- `ProviderModelMixin`
- `RaiseErrorMixin`

**Атрибуты**:

- `api_base` (str): Базовый URL для API OpenAI.
- `api_key` (str, optional): Ключ API OpenAI. По умолчанию `None`.
- `api_endpoint` (str, optional): Конечная точка API. По умолчанию `None`.
- `supports_message_history` (bool): Указывает, поддерживает ли модель OpenAI историю сообщений.
- `supports_system_message` (bool): Указывает, поддерживает ли модель OpenAI системные сообщения.
- `default_model` (str): Идентификатор модели OpenAI по умолчанию.
- `fallback_models` (list): Список моделей OpenAI, которые будут использоваться в качестве резервных, если основная модель недоступна.
- `sort_models` (bool): Указывает, нужно ли сортировать модели OpenAI.
- `ssl` (bool, optional): Указывает, следует ли использовать SSL-соединение. По умолчанию `None`.

**Методы**:

- `get_models(api_key: str = None, api_base: str = None) -> list[str]`: Возвращает список доступных моделей OpenAI.
- `create_async_generator(model: str, messages: Messages, proxy: str = None, timeout: int = 120, media: MediaListType = None, api_key: str = None, api_endpoint: str = None, api_base: str = None, temperature: float = None, max_tokens: int = None, top_p: float = None, stop: Union[str, list[str]] = None, stream: bool = False, prompt: str = None, headers: dict = None, impersonate: str = None, extra_parameters: list[str] = ["tools", "parallel_tool_calls", "tool_choice", "reasoning_effort", "logit_bias", "modalities", "audio"], extra_data: dict = {}, **kwargs) -> AsyncResult`: Создает асинхронный генератор для отправки запросов к OpenAI API.
- `get_headers(stream: bool, api_key: str = None, headers: dict = None) -> dict`: Возвращает заголовки HTTP-запроса.


## Методы класса

### `get_models(api_key: str = None, api_base: str = None) -> list[str]`

**Назначение**: Функция получает список доступных моделей OpenAI API.

**Параметры**:

- `api_key` (str, optional): Ключ API OpenAI. По умолчанию `None`.
- `api_base` (str, optional): Базовый URL для API OpenAI. По умолчанию `None`.

**Возвращает**:

- `list[str]`: Список идентификаторов доступных моделей OpenAI.

**Вызывает исключения**:

- `Exception`: Если возникает ошибка при получении списка моделей.

**Как работает функция**:

- Функция выполняет GET-запрос к `/models` API OpenAI, чтобы получить список доступных моделей.
- Если указан `api_key` и `api_base`, то они будут использоваться для запроса. В противном случае будут использоваться значения `api_key` и `api_base`, определенные в классе `OpenaiTemplate`.
- Если возникает ошибка, то функция возвращает список моделей по умолчанию `fallback_models`.

**Примеры**:

```python
# Получение списка моделей с использованием API-ключа
models = OpenaiTemplate.get_models(api_key="YOUR_API_KEY")
print(models)

# Получение списка моделей с использованием базового URL
models = OpenaiTemplate.get_models(api_base="https://api.openai.com/v1")
print(models)
```

### `create_async_generator(model: str, messages: Messages, proxy: str = None, timeout: int = 120, media: MediaListType = None, api_key: str = None, api_endpoint: str = None, api_base: str = None, temperature: float = None, max_tokens: int = None, top_p: float = None, stop: Union[str, list[str]] = None, stream: bool = False, prompt: str = None, headers: dict = None, impersonate: str = None, extra_parameters: list[str] = ["tools", "parallel_tool_calls", "tool_choice", "reasoning_effort", "logit_bias", "modalities", "audio"], extra_data: dict = {}, **kwargs) -> AsyncResult`

**Назначение**: Функция создает асинхронный генератор для отправки запросов к OpenAI API.

**Параметры**:

- `model` (str): Идентификатор модели OpenAI.
- `messages` (Messages): Список сообщений для модели OpenAI.
- `proxy` (str, optional): Прокси-сервер для отправки запросов. По умолчанию `None`.
- `timeout` (int, optional): Таймаут для запросов. По умолчанию 120 секунд.
- `media` (MediaListType, optional): Список медиа-файлов для отправки модели OpenAI. По умолчанию `None`.
- `api_key` (str, optional): Ключ API OpenAI. По умолчанию `None`.
- `api_endpoint` (str, optional): Конечная точка API. По умолчанию `None`.
- `api_base` (str, optional): Базовый URL для API OpenAI. По умолчанию `None`.
- `temperature` (float, optional): Параметр температуры для модели OpenAI. По умолчанию `None`.
- `max_tokens` (int, optional): Максимальное количество токенов для ответа модели OpenAI. По умолчанию `None`.
- `top_p` (float, optional): Параметр топ-p для модели OpenAI. По умолчанию `None`.
- `stop` (Union[str, list[str]], optional): Список стоп-слов для модели OpenAI. По умолчанию `None`.
- `stream` (bool, optional): Указывает, следует ли использовать потоковый режим. По умолчанию `False`.
- `prompt` (str, optional): Текстовый запрос для модели OpenAI. По умолчанию `None`.
- `headers` (dict, optional): Заголовки HTTP-запроса. По умолчанию `None`.
- `impersonate` (str, optional): Имя пользователя для имитации. По умолчанию `None`.
- `extra_parameters` (list[str], optional): Дополнительные параметры для запроса. По умолчанию `["tools", "parallel_tool_calls", "tool_choice", "reasoning_effort", "logit_bias", "modalities", "audio"]`.
- `extra_data` (dict, optional): Дополнительные данные для запроса. По умолчанию `{}`.
- `**kwargs`: Дополнительные аргументы для запроса.

**Возвращает**:

- `AsyncResult`: Асинхронный генератор для обработки ответов модели OpenAI.

**Вызывает исключения**:

- `MissingAuthError`: Если не указан ключ API.
- `ResponseError`: Если возникает ошибка при отправке запроса или обработке ответа.

**Как работает функция**:

- Функция создает асинхронный сеанс с помощью `StreamSession` и устанавливает заголовки запроса.
- Функция определяет модель OpenAI для отправки запроса.
- Если модель поддерживает генерацию изображений, то функция отправляет запрос к `/images/generations` API OpenAI, чтобы получить URL-адреса сгенерированных изображений.
- В противном случае функция отправляет запрос к `/chat/completions` API OpenAI, чтобы получить текст или вызовы инструментов.
- Функция обрабатывает ответы модели OpenAI в зависимости от типа ответа, а также обрабатывает ошибки.

**Примеры**:

```python
# Отправка запроса к модели OpenAI для генерации текста
async def send_request():
    async for response in OpenaiTemplate.create_async_generator(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Привет, мир!"}]):
        print(response)

# Отправка запроса к модели OpenAI для генерации изображения
async def send_request():
    async for response in OpenaiTemplate.create_async_generator(model="dall-e", prompt="Фото кошки на фоне заката", media=[]):
        print(response)
```

### `get_headers(stream: bool, api_key: str = None, headers: dict = None) -> dict`

**Назначение**: Функция возвращает заголовки HTTP-запроса для взаимодействия с OpenAI API.

**Параметры**:

- `stream` (bool): Указывает, следует ли использовать потоковый режим.
- `api_key` (str, optional): Ключ API OpenAI. По умолчанию `None`.
- `headers` (dict, optional): Дополнительные заголовки запроса. По умолчанию `None`.

**Возвращает**:

- `dict`: Словарь заголовков HTTP-запроса.

**Как работает функция**:

- Функция формирует словарь заголовков запроса.
- Если используется потоковый режим, то заголовок `Accept` устанавливается в `text/event-stream`.
- Если указан `api_key`, то заголовок `Authorization` устанавливается в `Bearer {api_key}`.
- Дополнительные заголовки запроса, указанные в `headers`, добавляются к основным заголовкам.

**Примеры**:

```python
# Получение заголовков для потокового режима
headers = OpenaiTemplate.get_headers(stream=True, api_key="YOUR_API_KEY")
print(headers)

# Получение заголовков с дополнительными заголовками
headers = OpenaiTemplate.get_headers(api_key="YOUR_API_KEY", headers={"X-Custom-Header": "value"})
print(headers)
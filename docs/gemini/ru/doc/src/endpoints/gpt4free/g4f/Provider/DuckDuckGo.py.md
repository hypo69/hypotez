# DuckDuckGo Provider

## Обзор

Модуль предоставляет реализацию асинхронного генератора для взаимодействия с DuckDuckGo AI Chat. 

## Подробности

Этот модуль содержит класс `DuckDuckGo`, который наследует от базовых классов `AsyncGeneratorProvider` и `ProviderModelMixin`. Он обеспечивает асинхронную генерацию ответов от DuckDuckGo AI Chat, поддерживает различные модели (gpt-4o-mini, meta-llama/Llama-3.3-70B-Instruct-Turbo, claude-3-haiku-20240307, o3-mini, mistralai/Mistral-Small-24B-Instruct-2501), а также предоставляет методы для проверки доступности API и настройки модели.

## Классы

### `class DuckDuckGo`

**Описание**: Класс `DuckDuckGo` реализует асинхронный генератор для получения ответов от DuckDuckGo AI Chat. 

**Наследует**: 
- `AsyncGeneratorProvider`: Базовый класс для асинхронных генераторов ответов.
- `ProviderModelMixin`: Базовый класс для управления моделями.

**Атрибуты**:
- `label` (str): Имя провайдера (например, "Duck.ai (duckduckgo_search)").
- `url` (str): URL-адрес сайта DuckDuckGo AI Chat.
- `api_base` (str): Базовый URL-адрес API.
- `working` (bool): Флаг, указывающий на готовность к работе провайдера.
- `supports_stream` (bool): Поддерживает ли провайдер потоковую передачу данных.
- `supports_system_message` (bool): Поддерживает ли провайдер системные сообщения.
- `supports_message_history` (bool): Поддерживает ли провайдер историю сообщений.
- `default_model` (str): Имя модели по умолчанию.
- `models` (list[str]): Список доступных моделей.
- `ddgs` (duckduckgo_search.DDGS): Экземпляр класса `DDGS` для взаимодействия с DuckDuckGo API.
- `model_aliases` (dict): Сопоставление альясов моделей (например, "gpt-4": "gpt-4o-mini").

**Методы**:

- `create_async_generator(model: str, messages: Messages, proxy: str = None, timeout: int = 60, **kwargs) -> AsyncResult`: 
    **Назначение**: Создает асинхронный генератор для получения ответов от модели DuckDuckGo AI Chat.
    **Параметры**:
    - `model` (str): Имя модели (например, "gpt-4o-mini").
    - `messages` (Messages): История сообщений.
    - `proxy` (str): Прокси-сервер (необязательно).
    - `timeout` (int): Таймаут запроса (в секундах).
    **Возвращает**:
    - `AsyncResult`: Асинхронный генератор, который можно использовать для получения ответов от DuckDuckGo AI Chat.
    **Вызывает исключения**:
    - `ImportError`: Если не установлен модуль `duckduckgo_search`.
- `nodriver_auth(proxy: str = None)`:
    **Назначение**: Выполняет аутентификацию для доступа к API DuckDuckGo AI Chat, используя nodriver.
    **Параметры**:
    - `proxy` (str): Прокси-сервер (необязательно).
    **Возвращает**:
    - `None`.
    **Как работает функция**:
    - Использует nodriver для открытия браузера и перехода на сайт DuckDuckGo AI Chat.
    - Выполняет проверку запросов, чтобы получить необходимые данные (X-Vqd-4, X-Vqd-Hash-1, F-Fe-Version) для аутентификации.
    - Сохраняет полученные данные в атрибутах класса `ddgs` для последующего использования.
    - Закрывает браузер после успешной аутентификации.

## Внутренние функции

### `nodriver_auth`

**Описание**:  Внутренняя функция, которая выполняет аутентификацию для доступа к API DuckDuckGo AI Chat, используя nodriver.

**Параметры**:
- `proxy` (str): Прокси-сервер (необязательно).

**Возвращает**:
- `None`.

**Как работает функция**:
- Использует nodriver для открытия браузера и перехода на сайт DuckDuckGo AI Chat.
- Выполняет проверку запросов, чтобы получить необходимые данные (X-Vqd-4, X-Vqd-Hash-1, F-Fe-Version) для аутентификации.
- Сохраняет полученные данные в атрибутах класса `ddgs` для последующего использования.
- Закрывает браузер после успешной аутентификации.

## Примеры

```python
# Создание инстанса DuckDuckGo провайдера
duckduckgo_provider = DuckDuckGo()

# Получение ответа от модели gpt-4o-mini
messages = [
    {"role": "user", "content": "Привет! Как дела?"},
    {"role": "assistant", "content": "Привет! У меня все отлично, а у тебя?"},
]
async_generator = await duckduckgo_provider.create_async_generator(model="gpt-4o-mini", messages=messages)

# Итерация по ответам от модели
async for chunk in async_generator:
    print(chunk)

# Использование альтернативного имени модели
async_generator = await duckduckgo_provider.create_async_generator(model="gpt-4", messages=messages)

# Использование прокси-сервера
async_generator = await duckduckgo_provider.create_async_generator(model="gpt-4o-mini", messages=messages, proxy="http://your_proxy:port")
```
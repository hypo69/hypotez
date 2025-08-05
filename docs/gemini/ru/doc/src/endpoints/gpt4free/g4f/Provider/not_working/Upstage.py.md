# Upstage.py

## Обзор

Модуль содержит класс `Upstage`, который предоставляет функциональность для взаимодействия с API Upstage.ai. 

## Подробнее

`Upstage` - это класс, который предоставляет функциональность для взаимодействия с API Upstage.ai. Он использует `aiohttp` для выполнения асинхронных запросов и `json` для работы с данными.

## Классы

### `Upstage`

**Описание**: Класс `Upstage` предоставляет асинхронный генератор для получения ответов от модели Upstage.ai.

**Наследует**: 
 - `AsyncGeneratorProvider`: Класс, который предоставляет асинхронный генератор.
 - `ProviderModelMixin`: Класс, который предоставляет методы для работы с моделями.

**Атрибуты**:

- `url (str)`: URL-адрес веб-интерфейса Upstage.ai.
- `api_endpoint (str)`: URL-адрес API Upstage.ai для получения ответов от модели.
- `working (bool)`: Флаг, указывающий, работает ли провайдер.
- `default_model (str)`: Имя модели по умолчанию.
- `models (List[str])`: Список поддерживаемых моделей Upstage.ai.
- `model_aliases (Dict[str, str])`: Словарь алиасов для моделей.

**Методы**:

- `get_model(model: str) -> str`: Возвращает имя модели, используя алиас, если он задан.
- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: Создает асинхронный генератор для получения ответов от модели Upstage.ai.

**Принцип работы**:

Класс `Upstage` использует `aiohttp` для выполнения асинхронных запросов к API Upstage.ai. Он передает в API запросы, содержащие `messages` и `model` в формате JSON. API возвращает ответ, который обрабатывается классом `Upstage` для преобразования его в список строк, которые передаются пользователю через асинхронный генератор.

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.Upstage import Upstage
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [
    {"role": "user", "content": "Привет!"},
]

provider = Upstage()

async for response in provider.create_async_generator(model="solar-pro", messages=messages):
    print(response)

```

## Внутренние функции

### `create_async_generator`

**Назначение**:  Создает асинхронный генератор для получения ответов от модели Upstage.ai.

**Параметры**:

- `model (str)`: Имя модели Upstage.ai.
- `messages (Messages)`: Список сообщений, которые необходимо передать модели.
- `proxy (str, optional)`: Прокси-сервер, который нужно использовать для запросов. По умолчанию `None`.

**Возвращает**:

- `AsyncResult`: Асинхронный генератор, который будет выдавать части ответа от модели Upstage.ai.

**Вызывает исключения**:

- `json.JSONDecodeError`: Возникает, если ответ от API Upstage.ai не может быть обработан как JSON.

**Как работает функция**:

1. Функция получает имя модели, список сообщений, которые необходимо передать модели, и опциональный прокси-сервер.
2. Она формирует запрос к API Upstage.ai, используя `aiohttp`.
3. Она передает `messages` и `model` в API в формате JSON.
4. Она получает ответ от API в виде JSON.
5. Она обрабатывает ответ и возвращает части ответа в виде строк через асинхронный генератор.

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.Upstage import Upstage
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [
    {"role": "user", "content": "Привет!"},
]

provider = Upstage()

async for response in provider.create_async_generator(model="solar-pro", messages=messages):
    print(response)

```
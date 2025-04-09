# Модуль backend_api.py

## Обзор

Модуль `backend_api.py` является частью проекта `hypotez` и отвечает за обработку различных API-запросов, связанных с серверной частью приложения. Он предоставляет функциональность для взаимодействия с моделями, провайдерами, управления беседами, обработки ошибок и управления версиями. Модуль использует Flask для создания API и включает в себя обработку запросов, связанных с моделями, провайдерами, файлами, куки и синтезом речи.

## Подробней

Модуль содержит класс `Backend_Api`, который наследуется от класса `Api` и расширяет его функциональность, добавляя обработку маршрутов Flask и взаимодействие с различными компонентами приложения. Он включает в себя обработку запросов, связанных с моделями, провайдерами, файлами, куки и синтезом речи.

## Классы

### `Backend_Api`

**Описание**: Класс `Backend_Api` обрабатывает различные endpoints в Flask-приложении для выполнения серверных операций.

**Наследует**: `Api`

**Атрибуты**:

- `app` (Flask): Экземпляр Flask-приложения.
- `chat_cache` (dict): Кэш для хранения данных чатов.
- `routes` (dict): Словарь, сопоставляющий API endpoints с соответствующими обработчиками.

**Методы**:

- `__init__(app: Flask) -> None`: Инициализирует API backend с заданным Flask-приложением.
- `handle_synthesize(provider: str)`: Обрабатывает запросы на синтез речи от указанного провайдера.
- `get_provider_models(provider: str)`: Возвращает модели, поддерживаемые указанным провайдером.
- `_format_json(response_type: str, content=None, **kwargs) -> str`: Форматирует и возвращает JSON-ответ.

### `__init__`

```python
def __init__(self, app: Flask) -> None:
    """
    Инициализирует API backend с заданным Flask-приложением.

    Args:
        app (Flask): Flask application instance to attach routes to.
    """
```

**Назначение**: Инициализирует экземпляр класса `Backend_Api`, привязывая к нему Flask-приложение и определяя маршруты для различных API-endpoint.

**Параметры**:

- `app` (Flask): Экземпляр Flask-приложения, к которому будут привязаны маршруты.

**Как работает функция**:

1. Сохраняет переданный экземпляр Flask-приложения в атрибуте `self.app`.
2. Инициализирует пустой словарь `self.chat_cache` для кэширования данных чатов.
3. Определяет маршруты Flask-приложения для различных endpoint, такие как главная страница (`/`), QR-код (`/qrcode`), модели (`/backend-api/v2/models`), провайдеры (`/backend-api/v2/providers`), обработка бесед (`/backend-api/v2/conversation`), использование (`/backend-api/v2/usage`), логирование (`/backend-api/v2/log`), управление памятью (`/backend-api/v2/memory`), версия (`/backend-api/v2/version`), синтез речи (`/backend-api/v2/synthesize`), изображения (`/images`), медиафайлы (`/media`), создание (`/backend-api/v2/create`), файлы (`/backend-api/v2/files`), загрузка куки (`/backend-api/v2/upload_cookies`), чаты (`/backend-api/v2/chat`).
4. Определяет словарь `self.routes`, который сопоставляет API endpoint с их соответствующими обработчиками.
```
Backend_Api -> app
    │
    ├── chat_cache = {}
    │
    └── Определяет маршруты Flask-приложения:
        │
        ├── '/' -> home()
        │
        ├── '/qrcode' -> qrcode()
        │
        ├── '/backend-api/v2/models' -> jsonify_models()
        │
        ├── '/backend-api/v2/models/<provider>' -> jsonify_provider_models()
        │
        ├── '/backend-api/v2/providers' -> jsonify_providers()
        │
        ├── '/backend-api/v2/conversation' -> handle_conversation()
        │
        ├── '/backend-api/v2/usage' -> add_usage()
        │
        ├── '/backend-api/v2/log' -> add_log()
        │
        ├── '/backend-api/v2/memory/<user_id>' -> add_memory() / read_memory()
        │
        ├── '/backend-api/v2/version' -> self.get_version()
        │
        ├── '/backend-api/v2/synthesize/<provider>' -> self.handle_synthesize()
        │
        ├── '/images/<path:name>' -> self.serve_images()
        │
        ├── '/media/<path:name>' -> self.serve_images()
        │
        ├── '/backend-api/v2/create' -> create()
        │
        ├── '/backend-api/v2/files/<bucket_id>' -> manage_files() / upload_files()
        │
        ├── '/files/<bucket_id>/media/<filename>' -> get_media()
        │
        ├── '/search/<search>' -> find_media()
        │
        ├── '/backend-api/v2/upload_cookies' -> upload_cookies()
        │
        └── '/backend-api/v2/chat/<share_id>' -> get_chat() / upload_chat()
```
**Примеры**:

```python
app = Flask(__name__)
backend_api = Backend_Api(app)
```

### `handle_synthesize`

```python
def handle_synthesize(self, provider: str):
    """
    Обрабатывает запросы на синтез речи от указанного провайдера.

    Args:
        provider (str): Имя провайдера синтеза речи.

    Returns:
        flask.Response: Ответ Flask с синтезированным контентом.
    """
```

**Назначение**: Обрабатывает запросы на синтез речи, используя указанного провайдера.

**Параметры**:

- `provider` (str): Имя провайдера синтеза речи.

**Возвращает**:

- `flask.Response`: Ответ Flask с синтезированным контентом.

**Вызывает исключения**:

- `ProviderNotFoundError`: Если указанный провайдер не найден.

**Как работает функция**:

1. Пытается преобразовать имя провайдера в обработчик провайдера с помощью `convert_to_provider`.
2. Если провайдер не найден, возвращает ошибку "Provider not found" с кодом 404.
3. Проверяет, поддерживает ли провайдер метод `synthesize`. Если нет, возвращает ошибку "Provider doesn't support synthesize" с кодом 500.
4. Вызывает метод `synthesize` у обработчика провайдера, передавая параметры запроса.
5. Если `synthesize` является асинхронной функцией, запускает её асинхронно.
6. Если возвращенный объект является асинхронным итератором, преобразует его в синхронный генератор.
7. Создает Flask-ответ с синтезированными данными и устанавливает заголовок `Content-Type` на основе атрибута `synthesize_content_type` провайдера (по умолчанию `application/octet-stream`).
8. Устанавливает заголовок `Cache-Control` для кэширования ответа в течение 7 дней.
```
handle_synthesize -> provider
    │
    ├── convert_to_provider(provider)
    │
    ├── Проверяет наличие метода synthesize у провайдера
    │
    ├── Вызывает provider_handler.synthesize({**request.args})
    │
    ├── Если synthesize является асинхронной функцией, запускает её асинхронно
    │
    ├── Если возвращенный объект является асинхронным итератором, преобразует его в синхронный генератор
    │
    └── Создает Flask-ответ с синтезированными данными
```
**Примеры**:

```python
response = backend_api.handle_synthesize("g4f.providers.GoogleBard")
```

### `get_provider_models`

```python
def get_provider_models(self, provider: str):
    """
    Возвращает модели, поддерживаемые указанным провайдером.

    Args:
        provider (str): Имя провайдера.

    Returns:
        list: Список моделей, поддерживаемых провайдером.
    """
```

**Назначение**: Получает список моделей, поддерживаемых указанным провайдером.

**Параметры**:

- `provider` (str): Имя провайдера.

**Возвращает**:

- `list`: Список моделей, поддерживаемых провайдером.

**Как работает функция**:

1. Получает API-ключ и базовый URL из заголовков запроса.
2. Вызывает метод `get_provider_models` родительского класса `Api`, передавая имя провайдера, API-ключ и базовый URL.
3. Если модели не найдены, возвращает ошибку "Provider not found" с кодом 404.
4. Возвращает список моделей, поддерживаемых провайдером.
```
get_provider_models -> provider
    │
    ├── Получает API-ключ и базовый URL из заголовков запроса
    │
    ├── Вызывает super().get_provider_models(provider, api_key, api_base)
    │
    └── Возвращает список моделей, поддерживаемых провайдером
```
**Примеры**:

```python
models = backend_api.get_provider_models("g4f.providers.GoogleBard")
```

### `_format_json`

```python
def _format_json(self, response_type: str, content = None, **kwargs) -> str:
    """
    Форматирует и возвращает JSON-ответ.

    Args:
        response_type (str): The type of the response.
        content: The content to be included in the response.

    Returns:
        str: A JSON formatted string.
    """
```

**Назначение**: Форматирует и возвращает JSON-ответ.

**Параметры**:

- `response_type` (str): Тип ответа.
- `content`: Содержимое, которое будет включено в ответ.

**Возвращает**:

- `str`: JSON-строка.

**Как работает функция**:

1. Вызывает метод `_format_json` родительского класса `Api`, передавая тип ответа, содержимое и дополнительные аргументы.
2. Преобразует результат в JSON-строку с помощью `json.dumps`.
3. Добавляет символ новой строки (`\n`) в конец JSON-строки.
4. Возвращает JSON-строку.
```
_format_json -> response_type, content, kwargs
    │
    ├── Вызывает super()._format_json(response_type, content, **kwargs)
    │
    ├── Преобразует результат в JSON-строку с помощью json.dumps
    │
    └── Добавляет символ новой строки (\n) в конец JSON-строки
```
**Примеры**:

```python
json_response = backend_api._format_json("success", {"message": "Operation completed successfully"})
```

## Функции

### `safe_iter_generator`

```python
def safe_iter_generator(generator: Generator) -> Generator:
    start = next(generator)
    def iter_generator():
        yield start
        yield from generator
    return iter_generator()
```

**Назначение**: Оборачивает генератор, чтобы обеспечить безопасную итерацию, гарантируя, что генератор всегда выдает хотя бы одно значение.

**Параметры**:

- `generator` (Generator): Генератор, который нужно обернуть.

**Возвращает**:

- `Generator`: Обернутый генератор.

**Как работает функция**:

1. Получает первое значение из исходного генератора с помощью `next(generator)` и сохраняет его в переменной `start`.
2. Определяет внутреннюю функцию `iter_generator`, которая сначала выдает сохраненное значение `start`, а затем выдает все остальные значения из исходного генератора с помощью `yield from generator`.
3. Возвращает внутреннюю функцию `iter_generator` как новый генератор.
```
safe_iter_generator -> generator
    │
    ├── start = next(generator)
    │
    └── Определяет внутреннюю функцию iter_generator:
        │
        ├── yield start
        │
        └── yield from generator
    │
    └── Возвращает iter_generator
```
**Примеры**:

```python
def my_generator():
    yield 1
    yield 2
    yield 3

safe_generator = safe_iter_generator(my_generator())
for value in safe_generator:
    print(value)
```
```python
def empty_generator():
    return
    yield # dummy

safe_generator = safe_iter_generator(empty_generator())
for value in safe_generator:
    print(value)
```

### `get_demo_models`

```python
def get_demo_models():
    return [{
        "name": model.name,
        "image": isinstance(model, models.ImageModel),
        "vision": isinstance(model, models.VisionModel),
        "providers": [
            getattr(provider, "parent", provider.__name__)
            for provider in providers
        ],
        "demo": True
    }
    for model, providers in models.demo_models.values()]
```

**Назначение**: Возвращает список демонстрационных моделей с информацией об их возможностях и провайдерах.

**Возвращает**:

- `list`: Список словарей, содержащих информацию о демонстрационных моделях.

**Как работает функция**:

1. Проходит по всем моделям и провайдерам в словаре `models.demo_models.values()`.
2. Для каждой модели создает словарь, содержащий имя модели, информацию о поддержке изображений и vision, список провайдеров и флаг `demo`.
3. Возвращает список этих словарей.
```
get_demo_models
    │
    └── Проходит по всем моделям и провайдерам в словаре models.demo_models.values():
        │
        └── Создает словарь с информацией о модели:
            │
            ├── "name": model.name
            │
            ├── "image": isinstance(model, models.ImageModel)
            │
            ├── "vision": isinstance(model, models.VisionModel)
            │
            ├── "providers": [getattr(provider, "parent", provider.__name__) for provider in providers]
            │
            └── "demo": True
    │
    └── Возвращает список словарей
```
**Примеры**:

```python
demo_models = get_demo_models()
```

### `handle_conversation`

```python
def handle_conversation():
    """
    Handles conversation requests and streams responses back.

    Returns:
        Response: A Flask response object for streaming.
    """
```

**Назначение**: Обрабатывает запросы на ведение бесед и передает ответы обратно в виде потока.

**Возвращает**:

- `Response`: Объект Flask-ответа для потоковой передачи.

**Как работает функция**:

1. Проверяет, содержатся ли данные в формате JSON в `request.form` или `request.json`.
2. Если в запросе есть файлы, добавляет их в данные запроса.
3. Если приложение находится в демонстрационном режиме и не указан провайдер, выбирает случайного провайдера из списка поддерживаемых моделей.
4. Подготавливает аргументы для функции `_create_response_stream`.
5. Возвращает объект Flask-ответа, созданный на основе потока, полученного от `_create_response_stream`.
```
handle_conversation
    │
    ├── Проверяет, содержатся ли данные в формате JSON в request.form или request.json
    │
    ├── Если в запросе есть файлы, добавляет их в данные запроса
    │
    ├── Если приложение находится в демонстрационном режиме и не указан провайдер, выбирает случайного провайдера из списка поддерживаемых моделей
    │
    ├── Подготавливает аргументы для функции _create_response_stream
    │
    └── Возвращает объект Flask-ответа, созданный на основе потока, полученного от _create_response_stream
```
**Примеры**:

```python
response = handle_conversation()
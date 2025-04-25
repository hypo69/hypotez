# Модуль Reka

## Обзор

Модуль `Reka` предоставляет класс `Reka`, который реализует провайдера для доступа к API Reka.ai. Reka.ai - это бесплатный LLM, который не требует ключа API, но требует авторизации пользователя.

## Подробности

Модуль `Reka` реализует провайдера, позволяющего взаимодействовать с API Reka.ai для генерации текста, перевода и других задач, использующих ИИ. Этот модуль расширяет абстрактный класс `AbstractProvider` и предоставляет функциональность для:

- Аутентификации пользователя с помощью cookies
- Загрузки изображений
- Получения access token для авторизации
- Отправки запросов к API Reka.ai
- Обработки ответов от API Reka.ai

## Классы

### `class Reka`

**Описание**: Класс `Reka` реализует провайдера для взаимодействия с API Reka.ai.

**Наследует**: `AbstractProvider`

**Атрибуты**:

- `domain` (str): Домен API Reka.ai.
- `url` (str): Базовый URL API Reka.ai.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `needs_auth` (bool): Флаг, указывающий на необходимость авторизации пользователя.
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи ответов.
- `default_vision_model` (str): Имя модели для обработки изображений.
- `cookies` (dict): Словарь cookies для аутентификации пользователя.

**Методы**:

#### `create_completion(model: str, messages: Messages, stream: bool, proxy: str = None, api_key: str = None, image: ImageType = None, **kwargs) -> CreateResult`

**Назначение**: Метод отправляет запрос к API Reka.ai для генерации текста.

**Параметры**:

- `model` (str): Имя модели, которую нужно использовать.
- `messages` (Messages): Список сообщений в диалоге.
- `stream` (bool): Флаг, указывающий на необходимость потоковой передачи ответа.
- `proxy` (str, optional): Прокси-сервер для отправки запроса. По умолчанию `None`.
- `api_key` (str, optional): Ключ API для авторизации. По умолчанию `None`.
- `image` (ImageType, optional): Изображение для обработки. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы для отправки запроса.

**Возвращает**:

- `CreateResult`: Результат выполнения запроса к API Reka.ai.

**Вызывает исключения**:

- `ValueError`: Если не найдены cookies или access token.

**Пример**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.Reka import Reka
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.Reka import Reka
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [
    {
        "role": "user",
        "content": "Привет, как дела?",
    },
]

response = Reka.create_completion(model='reka', messages=messages, stream=True)

for chunk in response:
    print(chunk)
```

#### `upload_image(cls, access_token, image: ImageType) -> str`

**Назначение**: Метод отправляет запрос к API Reka.ai для загрузки изображения.

**Параметры**:

- `access_token` (str): Access token для авторизации.
- `image` (ImageType): Изображение для загрузки.

**Возвращает**:

- `str`: URL загруженного изображения.

**Пример**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.Reka import Reka
from hypotez.src.endpoints.gpt4free.g4f.typing import ImageType

image: ImageType = 'path/to/image.png'

url = Reka.upload_image(access_token='your_access_token', image=image)

print(url)
```

#### `get_access_token(cls)`

**Назначение**: Метод получает access token для авторизации пользователя.

**Параметры**:

- `cls`: Класс `Reka`.

**Возвращает**:

- `str`: Access token.

**Вызывает исключения**:

- `ValueError`: Если не удалось получить access token.

**Пример**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.Reka import Reka

access_token = Reka.get_access_token()

print(access_token)
```

## Внутренние функции

#### `inner_function()`

**Назначение**: Внутренняя функция, которая выполняет некоторое действие.

**Параметры**:

- `param` (str): Описание параметра `param`.
- `param1` (Optional[str | dict | str], optional): Описание параметра `param1`. По умолчанию `None`.

**Возвращает**:

- `dict | None`: Описание возвращаемого значения. Возвращает словарь или `None`.

**Вызывает исключения**:

- `SomeError`: Описание ситуации, в которой возникает исключение `SomeError`.
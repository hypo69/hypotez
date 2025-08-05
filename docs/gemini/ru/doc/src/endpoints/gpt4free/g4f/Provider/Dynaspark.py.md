# Модуль Dynaspark
## Обзор
Этот модуль предоставляет класс `Dynaspark`, который реализует API-интерфейс для модели `Dynaspark`, предоставляющей услуги обработки естественного языка и генерации изображений. Класс `Dynaspark` наследует от `AsyncGeneratorProvider` и `ProviderModelMixin`, что обеспечивает асинхронную обработку и поддержку различных моделей.

## Подробнее
Модуль `Dynaspark` предоставляет доступ к модели `Dynaspark`, которая предоставляет услуги обработки естественного языка и генерации изображений. Класс `Dynaspark` реализует API-интерфейс, позволяющий отправлять запросы к сервису и получать ответы.

## Классы
### `class Dynaspark`
**Описание**: Класс `Dynaspark` реализует API-интерфейс для взаимодействия с сервисом Dynaspark, предоставляющим услуги обработки естественного языка и генерации изображений.

**Наследует**: 
- `AsyncGeneratorProvider`: Обеспечивает асинхронную обработку запросов.
- `ProviderModelMixin`: Предоставляет функциональность для управления моделями.

**Атрибуты**:
- `url`: Базовый URL-адрес сервиса Dynaspark.
- `login_url`: URL-адрес для авторизации (не используется).
- `api_endpoint`: URL-адрес для отправки запросов.
- `working`: Флаг, указывающий на то, что сервис работает.
- `needs_auth`: Флаг, указывающий на необходимость авторизации (не используется).
- `use_nodriver`: Флаг, указывающий на то, что сервис не использует веб-драйвер.
- `supports_stream`: Флаг, указывающий на поддержку потоковой передачи данных.
- `supports_system_message`: Флаг, указывающий на поддержку системных сообщений (не используется).
- `supports_message_history`: Флаг, указывающий на поддержку истории сообщений (не используется).
- `default_model`: Имя модели по умолчанию.
- `default_vision_model`: Имя модели для обработки изображений по умолчанию.
- `vision_models`: Список моделей для обработки изображений.
- `models`: Список всех поддерживаемых моделей.
- `model_aliases`: Словарь, содержащий псевдонимы для моделей.

**Методы**:
- `create_async_generator(model: str, messages: Messages, proxy: str = None, media: MediaListType = None, **kwargs) -> AsyncResult`: Асинхронный метод, который создает асинхронный генератор, отправляющий запросы к сервису и получающий ответы.

#### `create_async_generator(model: str, messages: Messages, proxy: str = None, media: MediaListType = None, **kwargs) -> AsyncResult`
**Назначение**: Метод создает асинхронный генератор, который отправляет запросы к сервису Dynaspark и получает ответы.

**Параметры**:
- `model`: Имя модели, которую нужно использовать.
- `messages`: Список сообщений, которые нужно обработать.
- `proxy`: URL-адрес прокси-сервера (не используется).
- `media`: Список файлов медиа (изображений), которые нужно обработать.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный результат, представляющий собой генератор ответов.

**Как работает функция**:
1. Метод `create_async_generator` создает HTTP-запрос с помощью библиотеки `aiohttp`.
2. Запрос отправляется к сервису Dynaspark с использованием метода `POST`.
3. В запросе передается `model` (имя модели), `messages` (список сообщений), `media` (список файлов медиа) и другие параметры.
4. Сервис Dynaspark обрабатывает запрос и возвращает ответ.
5. Метод `create_async_generator` получает ответ от сервиса и преобразует его в JSON-формат.
6. Метод возвращает `AsyncResult`, представляющий собой асинхронный генератор, который выдает элементы JSON-ответа.

**Примеры**:
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider import Dynaspark
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создание инстанса Dynaspark
dynaspark = Dynaspark()

# Пример запроса к модели для обработки естественного языка
messages: Messages = [
    {'role': 'user', 'content': 'Привет, как дела?'},
]
async_generator = dynaspark.create_async_generator(model='gemini-1.5-flash', messages=messages)
async for response in async_generator:
    print(response)

# Пример запроса к модели для обработки изображений
messages: Messages = [
    {'role': 'user', 'content': 'Сгенерируй картинку с котиком'},
]
media = [('path/to/image.jpg', 'image.jpg')]
async_generator = dynaspark.create_async_generator(model='gemini-1.5-flash', messages=messages, media=media)
async for response in async_generator:
    print(response)
```
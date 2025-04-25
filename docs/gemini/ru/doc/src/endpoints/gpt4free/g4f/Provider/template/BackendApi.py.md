# Модуль `BackendApi`

## Обзор

Этот модуль предоставляет класс `BackendApi`, который реализует асинхронный генератор для взаимодействия с API  платформы, используемой в проекте `hypotez`. `BackendApi` наследует от `AsyncGeneratorProvider` и `ProviderModelMixin`, что позволяет ему использовать общий механизм асинхронной генерации ответов и определять  модель обработки данных. 

## Классы

### `class BackendApi`

**Описание**: Класс `BackendApi`  представляет собой асинхронный генератор, который взаимодействует с бэкендом API через HTTP-запросы, предоставляя обработку полученных данных в виде потока событий.

**Наследует**:
- `AsyncGeneratorProvider`:  Интерфейс для асинхронных генераторов, которые предоставляют данные в виде потока.
- `ProviderModelMixin`: Обеспечивает возможность выбора модели для обработки данных.

**Атрибуты**:
- `ssl`:  Конфигурация SSL-соединения.
- `headers`: Словарь заголовков HTTP-запросов.

**Методы**:
- `create_async_generator(model: str, messages: Messages, media: MediaListType = None, api_key: str = None, **kwargs) -> AsyncResult`:  Асинхронная функция, которая создает асинхронный генератор для взаимодействия с API.

#### `create_async_generator(model: str, messages: Messages, media: MediaListType = None, api_key: str = None, **kwargs) -> AsyncResult`

**Назначение**: 
- Функция создает асинхронный генератор для взаимодействия с API.
- Использует HTTP-запрос POST к определенному URL, передавая JSON-данные с информацией о модели, сообщениях, медиафайлах и API-ключе. 
- Возвращает `AsyncResult`, который представляет собой асинхронный результат выполнения функции. 

**Параметры**:
- `model` (str): Название модели, которая будет использоваться для обработки запроса. 
- `messages` (Messages): Список сообщений, которые будут использоваться в запросе. 
- `media` (MediaListType, optional):  Список медиафайлов. По умолчанию `None`.
- `api_key` (str, optional): API-ключ для аутентификации. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы для API.

**Возвращает**:
- `AsyncResult`:  Асинхронный результат выполнения функции.

**Как работает функция**:
- Функция `create_async_generator` создает экземпляр `StreamSession` для передачи данных в формате `text/event-stream` (`Accept` заголовок).
- Затем она отправляет POST-запрос к указанному URL `/backend-api/v2/conversation`, передавая JSON-данные с указанием модели, сообщений, медиафайлов и API-ключа.
- В теле цикла `async for` функция `iter_lines` получает данные из ответа API, а `json.loads` преобразует их в объект Python.
-  Функция  `RawResponse`  оборачивает полученный объект JSON, чтобы предоставить удобный доступ к полям.
- Каждый раз, когда  `yield RawResponse(**json.loads(line))` выполняется, генератор возвращает объект `RawResponse` с данными из API.

**Примеры**:
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.template.BackendApi import BackendApi
from hypotez.src.endpoints.gpt4free.g4f.Provider.template.typing import Messages

model = "gpt-3.5-turbo"
messages = Messages(
    [
        {"role": "user", "content": "Привет! Как дела?"},
    ]
)
async_generator = await BackendApi.create_async_generator(model=model, messages=messages)
async for response in async_generator:
    print(response) 
```
```markdown
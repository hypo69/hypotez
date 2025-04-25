# Модуль RubiksAI

## Обзор

Модуль `RubiksAI` обеспечивает доступ к API-интерфейсу `Rubiks AI` для взаимодействия с различными моделями искусственного интеллекта (ИИ), такими как `GPT-4`, `GPT-4o`, `o1-mini`, `claude-3.5-sonnet`, `grok-beta`, `gemini-1.5-pro`, `nova-pro`, `llama-3.1-70b-versatile` и другие. Он реализует два класса:

- `RubiksAI`: Основной класс, предоставляющий методы для взаимодействия с API-интерфейсом `Rubiks AI`.
- `create_async_generator`: Класс-генератор, который позволяет асинхронно получать ответы от API `Rubiks AI` в виде потока данных.

## Подробнее

Модуль `RubiksAI` является частью проекта `hypotez` и используется для получения ответов от различных моделей ИИ, предоставляемых `Rubiks AI`. 
Он реализует класс `RubiksAI`, который предоставляет методы для асинхронного отправки запросов к API `Rubiks AI` и получения ответов в виде потока данных.
Модуль также содержит статические методы для генерации уникальных идентификаторов (`mid`) и создания URL-адресов для запросов (`referer`).
В модуле реализован `async generator`, который позволяет получить данные из API `Rubiks AI` в виде потока, что значительно снижает потребление ресурсов.

## Классы

### `RubiksAI`

**Описание**: Класс `RubiksAI` предоставляет методы для взаимодействия с API-интерфейсом `Rubiks AI` и получения ответов от различных моделей ИИ, поддерживаемых этим сервисом.

**Наследует**: 
- `AsyncGeneratorProvider`: Предоставляет асинхронный генератор для потоковой передачи ответов.
- `ProviderModelMixin`: Предоставляет методы для работы с моделями ИИ, такими как `get_model`, `get_model_by_alias`.

**Атрибуты**:

- `label (str)`:  Имя поставщика, в данном случае "Rubiks AI".
- `url (str)`: Базовый URL-адрес `Rubiks AI`.
- `api_endpoint (str)`:  Точный URL-адрес конечной точки API для отправки запросов.
- `working (bool)`:  Указывает, доступен ли сервис.
- `supports_stream (bool)`:  Указывает, поддерживает ли сервис потоковую передачу данных.
- `supports_system_message (bool)`:  Указывает, поддерживает ли сервис системные сообщения.
- `supports_message_history (bool)`:  Указывает, поддерживает ли сервис историю сообщений.
- `default_model (str)`:  Название модели ИИ по умолчанию.
- `models (list)`: Список поддерживаемых моделей ИИ.
- `model_aliases (dict)`:  Словарь для преобразования псевдонимов моделей в их фактические названия.

**Методы**:

- `generate_mid()`:  Генерирует уникальный идентификатор (`mid`) для каждого запроса.
- `create_referer(q: str, mid: str, model: str = '')`:  Создает URL-адрес `referer` с динамическими значениями `q` (запрос), `mid` и `model`.
- `create_async_generator(model: str, messages: Messages, proxy: str = None, web_search: bool = False, temperature: float = 0.6, **kwargs)`:  Создает асинхронный генератор, который отправляет запросы к API `Rubiks AI` и получает ответы в виде потока данных.

### `create_async_generator`

**Описание**:  Класс-генератор, который обеспечивает асинхронную передачу ответов от API `Rubiks AI` в виде потока данных.

**Наследует**:  `AsyncGeneratorProvider`: Предоставляет базовый функционал для асинхронных генераторов.

**Атрибуты**: 

- `model (str)`:  Название модели ИИ.
- `messages (Messages)`:  Список сообщений (входной текст) для запроса к модели ИИ.
- `proxy (str, optional)`: URL-адрес прокси-сервера (если требуется).
- `web_search (bool, optional)`:  Флаг, указывающий, следует ли включать источники веб-поиска в ответ.
- `temperature (float, optional)`:  Параметр, влияющий на креативность модели ИИ (по умолчанию 0.6).

**Методы**:

- `__init__(self, model: str, messages: Messages, proxy: str = None, web_search: bool = False, temperature: float = 0.6, **kwargs)`:  Инициализирует генератор с указанными параметрами.
- `__aiter__(self)`:  Возвращает себя для итерации по потоку данных.
- `__anext__(self)`:  Возвращает следующий фрагмент ответа от API `Rubiks AI`.

## Функции

### `generate_mid()`

**Назначение**:  Генерирует уникальный идентификатор (`mid`) для каждого запроса к API `Rubiks AI`.

**Параметры**:

- **Возвращает**:  `str`: Уникальный идентификатор (`mid`) в формате `6 символов - 4 символа - 4 символа - 4 символа - 12 символов`.

**Как работает функция**: 

- `generate_mid()`  генерирует случайный идентификатор (`mid`) длиной 26 символов.
- Идентификатор разделяется на пять частей с использованием дефиса (-) и состоит из случайных букв и цифр в нижнем регистре.

**Пример**: 

```python
>>> RubiksAI.generate_mid() 
'r4t23v-g3w9-z5y6-d8k4-f32h8y7654a'
```

### `create_referer()`

**Назначение**: Создает URL-адрес `referer` с динамическими значениями `q` (запрос), `mid` и `model` для отправки запроса к API `Rubiks AI`.

**Параметры**: 

- `q (str)`:  Текст запроса.
- `mid (str)`:  Уникальный идентификатор (`mid`) запроса.
- `model (str, optional)`:  Название модели ИИ (по умолчанию пустая строка).

**Возвращает**:  `str`: URL-адрес `referer` в формате `https://rubiks.ai/search/?q=<запрос>&mid=<mid>&model=<model>`.

**Как работает функция**: 

- `create_referer()` использует модуль `urllib.parse` для безопасного кодирования параметров `q`, `mid` и `model` в URL-адресе `referer`.
- Функция создает URL-адрес `referer`  с использованием `urlencode`, где параметры `q`, `mid` и `model` кодируются в соответствии с правилами URL-адресов.

**Пример**:

```python
>>> RubiksAI.create_referer(q='Что такое искусственный интеллект?', mid='r4t23v-g3w9-z5y6-d8k4-f32h8y7654a', model='gpt-4o-mini')
'https://rubiks.ai/search/?q=Что+такое+искусственный+интеллект%3F&mid=r4t23v-g3w9-z5y6-d8k4-f32h8y7654a&model=gpt-4o-mini'
```

### `create_async_generator()`

**Назначение**: Создает асинхронный генератор, который отправляет запросы к API `Rubiks AI` и получает ответы в виде потока данных.

**Параметры**: 

- `model (str)`:  Название модели ИИ.
- `messages (Messages)`:  Список сообщений (входной текст) для запроса к модели ИИ.
- `proxy (str, optional)`: URL-адрес прокси-сервера (если требуется).
- `web_search (bool, optional)`:  Флаг, указывающий, следует ли включать источники веб-поиска в ответ.
- `temperature (float, optional)`:  Параметр, влияющий на креативность модели ИИ (по умолчанию 0.6).

**Возвращает**:  `AsyncResult`:  Асинхронный генератор, который обеспечивает потоковую передачу ответов от API `Rubiks AI`.

**Как работает функция**: 

- `create_async_generator()` использует библиотеку `aiohttp` для асинхронной отправки HTTP-запросов к API `Rubiks AI`.
- Генератор отправляет запрос с указанными параметрами, такими как модель ИИ, текст запроса, прокси-сервер, источники веб-поиска и `temperature`.
- Он получает ответ в виде потока данных и выдает их по частям, чтобы обеспечить эффективный доступ к данным.

**Пример**:

```python
>>> from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.RubiksAI import RubiksAI
>>> from hypotez.src.endpoints.gpt4free.g4f.typing import Messages
>>> messages = Messages([{"role": "user", "content": "Привет! Расскажи мне про искусственный интеллект."}])
>>> async def main():
...     async for response in RubiksAI.create_async_generator(model='gpt-4o-mini', messages=messages):
...         print(response)
>>> asyncio.run(main())
...
Привет! Искусственный интеллект (ИИ) - это область компьютерных наук, которая занимается созданием интеллектуальных машин, способных выполнять задачи, которые обычно требуют человеческого интеллекта, такие как обучение, решение задач, принятие решений и др.
...
```

## Параметры класса 

- `label (str)`:  Имя поставщика, в данном случае "Rubiks AI".
- `url (str)`: Базовый URL-адрес `Rubiks AI`.
- `api_endpoint (str)`:  Точный URL-адрес конечной точки API для отправки запросов.
- `working (bool)`:  Указывает, доступен ли сервис.
- `supports_stream (bool)`:  Указывает, поддерживает ли сервис потоковую передачу данных.
- `supports_system_message (bool)`:  Указывает, поддерживает ли сервис системные сообщения.
- `supports_message_history (bool)`:  Указывает, поддерживает ли сервис историю сообщений.
- `default_model (str)`:  Название модели ИИ по умолчанию.
- `models (list)`: Список поддерживаемых моделей ИИ.
- `model_aliases (dict)`:  Словарь для преобразования псевдонимов моделей в их фактические названия.

## Примеры

### Пример использования класса `RubiksAI`

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.RubiksAI import RubiksAI
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages = Messages([{"role": "user", "content": "Привет! Расскажи мне про искусственный интеллект."}])

async def main():
    async for response in RubiksAI.create_async_generator(model='gpt-4o-mini', messages=messages):
        print(response)

asyncio.run(main())
```

### Пример использования функции `generate_mid()`

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.RubiksAI import RubiksAI

mid = RubiksAI.generate_mid()

print(mid)
```

### Пример использования функции `create_referer()`

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.RubiksAI import RubiksAI

referer = RubiksAI.create_referer(q='Что такое искусственный интеллект?', mid='r4t23v-g3w9-z5y6-d8k4-f32h8y7654a', model='gpt-4o-mini')

print(referer)
```

## Дополнительные замечания 

- Модуль `RubiksAI` использует библиотеку `aiohttp` для асинхронного взаимодействия с API-интерфейсом `Rubiks AI`.
- Он предоставляет асинхронный генератор, который позволяет эффективно получать данные от API в виде потока.
-  `RubiksAI` поддерживает различные модели ИИ, такие как `GPT-4`, `GPT-4o`, `o1-mini` и другие.
- Модуль включает в себя механизм обработки исключений с использованием `raise_for_status` для проверки статуса HTTP-запросов.
- Для работы с этим модулем необходимо иметь доступ к API `Rubiks AI`.
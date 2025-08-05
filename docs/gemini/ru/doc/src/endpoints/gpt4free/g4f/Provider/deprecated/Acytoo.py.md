# Модуль Acytoo

## Обзор

Этот модуль предоставляет класс `Acytoo`, который используется для взаимодействия с API-интерфейсом `Acytoo` для генерации текста с помощью моделей GPT. 
Класс `Acytoo` наследует от `AsyncGeneratorProvider` и обеспечивает асинхронную генерацию текста с использованием `aiohttp`.

## Подробнее

Модуль реализует асинхронный генератор для получения ответов от API-интерфейса `Acytoo`, который обеспечивает возможность отправки запросов и получения потоковых данных. 
Класс `Acytoo` использует стандартные заголовки `aiohttp` для отправки запросов и предоставляет методы для создания JSON-запросов.

## Классы

### `class Acytoo`

**Описание**: Класс `Acytoo` реализует асинхронный генератор для получения ответов от API-интерфейса `Acytoo`.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `url` (str): URL API-интерфейса `Acytoo`.
- `working` (bool): Флаг, указывающий, доступен ли API-интерфейс.
- `supports_message_history` (bool): Флаг, указывающий, поддерживает ли API-интерфейс историю сообщений.
- `supports_gpt_35_turbo` (bool): Флаг, указывающий, поддерживает ли API-интерфейс модель `gpt-3.5-turbo`.

**Методы**:

- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: Метод создает асинхронный генератор для получения ответов от API-интерфейса `Acytoo`. 
- `_create_header() -> dict`: Метод возвращает стандартные заголовки для запросов.
- `_create_payload(messages: Messages, temperature: float = 0.5, **kwargs) -> dict`: Метод создает JSON-запрос для отправки в API-интерфейс `Acytoo`.

## Функции

### `_create_header()`

**Назначение**: Функция создает стандартные заголовки для запросов к API-интерфейсу `Acytoo`.

**Параметры**:
- Нет.

**Возвращает**:
- `dict`: Словарь с заголовками запроса.

**Пример**:

```python
>>> _create_header()
{'accept': '*/*', 'content-type': 'application/json'}
```

### `_create_payload()`

**Назначение**: Функция создает JSON-запрос для отправки в API-интерфейс `Acytoo`.

**Параметры**:
- `messages` (Messages): Список сообщений для отправки.
- `temperature` (float): Температура для модели GPT. По умолчанию `0.5`.
- `**kwargs`: Дополнительные параметры для запроса.

**Возвращает**:
- `dict`: Словарь с JSON-запросом.

**Пример**:

```python
>>> messages = [
...     {'role': 'user', 'content': 'Привет! Как дела?'},
...     {'role': 'assistant', 'content': 'Хорошо, а у тебя?'}
... ]
>>> _create_payload(messages, temperature=0.7)
{'key': '', 'model': 'gpt-3.5-turbo', 'messages': [{'role': 'user', 'content': 'Привет! Как дела?'}, {'role': 'assistant', 'content': 'Хорошо, а у тебя?'}], 'temperature': 0.7, 'password': ''}
```

## Примеры

```python
# Импорт необходимых модулей
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Acytoo import Acytoo
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создание объекта Acytoo
acytoo = Acytoo()

# Создание списка сообщений
messages = [
    {'role': 'user', 'content': 'Привет! Как дела?'},
    {'role': 'assistant', 'content': 'Хорошо, а у тебя?'}
]

# Вызов асинхронного генератора для получения ответов
async_generator = acytoo.create_async_generator(model='gpt-3.5-turbo', messages=messages)

# Итерация по результатам генерации
async for stream in async_generator:
    print(stream)

```
```markdown
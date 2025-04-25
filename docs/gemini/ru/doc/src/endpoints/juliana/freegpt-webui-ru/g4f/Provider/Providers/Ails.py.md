# Модуль Ails
## Обзор

Этот модуль содержит класс `Utils` и функцию `_create_completion`, которые используются для работы с API-интерфейсом `caipacity.com`. 

## Подробней

Этот модуль реализует функции, необходимые для отправки запросов к API-интерфейсу `caipacity.com` для получения ответов от модели GPT-3.5-turbo. 

## Классы

### `class Utils`

**Описание**: 
Класс `Utils` предоставляет вспомогательные функции для работы с API-интерфейсом `caipacity.com`.

**Атрибуты**:
- `secretKey` (bytearray): Секретный ключ для хеширования данных.

**Методы**:
- `hash(json_data: Dict[str, str]) -> sha256`: 
   **Назначение**: Хеширует JSON-данные с использованием секретного ключа.
   **Параметры**: 
    - `json_data` (Dict[str, str]): JSON-данные для хеширования.
   **Возвращает**:
    - `sha256`: Хешированный текст.
- `format_timestamp(timestamp: int) -> str`:
    **Назначение**: Форматирует временную метку в миллисекундах.
    **Параметры**:
    - `timestamp` (int): Временная метка в миллисекундах.
    **Возвращает**:
    - `str`: Форматированная временная метка.

## Функции

### `_create_completion(model: str, messages: list, temperature: float = 0.6, stream: bool = False, **kwargs)`

**Назначение**: 
Создает запрос к API-интерфейсу `caipacity.com` и получает от него ответ от модели GPT-3.5-turbo.

**Параметры**:
- `model` (str): Имя модели GPT-3.5-turbo.
- `messages` (list): Список сообщений для модели GPT-3.5-turbo.
- `temperature` (float): Температура модели (по умолчанию `0.6`).
- `stream` (bool): Используется ли потоковый режим (по умолчанию `False`).
- `**kwargs`: Дополнительные параметры для API-запроса.

**Возвращает**:
- `Generator`: Генератор ответов от модели GPT-3.5-turbo.

**Пример**:
```python
messages = [
    {'role': 'user', 'content': 'Привет! Как дела?'},
]

for token in _create_completion(model='gpt-3.5-turbo', messages=messages, stream=True):
    print(token, end='')
```

**Как работает функция**:

- Формирует запрос к API-интерфейсу `caipacity.com` с указанием модели, сообщениями, температурой и другими параметрами.
- Выполняет запрос и получает ответ от модели.
- Возвращает генератор, который позволяет получить ответ от модели по частям, если `stream=True`.

**Примеры**:

```python
# Пример 1:
messages = [
    {'role': 'user', 'content': 'Привет! Как дела?'},
]
for token in _create_completion(model='gpt-3.5-turbo', messages=messages, stream=True):
    print(token, end='')

# Пример 2:
messages = [
    {'role': 'user', 'content': 'Напиши мне стихотворение про осень.'},
]
for token in _create_completion(model='gpt-3.5-turbo', messages=messages, stream=True):
    print(token, end='')

# Пример 3:
messages = [
    {'role': 'user', 'content': 'Переведи текст: "Hello, world!" на русский язык.'},
]
for token in _create_completion(model='gpt-3.5-turbo', messages=messages, stream=True):
    print(token, end='')
```

**Внутренние функции**:

Нет

## Параметры класса

Нет

## Примеры

```python
# Пример 1:
from g4f.Provider.Providers.Ails import _create_completion

messages = [
    {'role': 'user', 'content': 'Привет! Как дела?'},
]

for token in _create_completion(model='gpt-3.5-turbo', messages=messages, stream=True):
    print(token, end='')

# Пример 2:
from g4f.Provider.Providers.Ails import Utils

json_data = {'t': 1694058741062, 'm': 'Hello, world!'}

hashed_text = Utils.hash(json_data)
print(hashed_text)

# Пример 3:
from g4f.Provider.Providers.Ails import Utils

timestamp = 1694058741062

formatted_timestamp = Utils.format_timestamp(timestamp)
print(formatted_timestamp)
```
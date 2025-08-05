# Модуль Free2GPT

## Обзор

Этот модуль предоставляет класс `Free2GPT`, который реализует асинхронный генератор ответов от модели `Free2GPT` для проекта `hypotez`. 

## Подробнее

`Free2GPT`  - это бесплатный API, который предоставляет доступ к различным языковым моделям, включая модели Gemini от Google.  Этот модуль реализует асинхронный генератор для получения ответов от `Free2GPT` и использует `aiohttp` для отправки запросов. 
`Free2GPT`  обеспечивает возможность использования  истории сообщений (`supports_message_history = True`) для более контекстуального взаимодействия с языковой моделью.

## Классы

### `class Free2GPT`

**Описание**: 
   Класс `Free2GPT` реализует асинхронный генератор ответов от модели `Free2GPT`.  Он  наследует классы `AsyncGeneratorProvider` и `ProviderModelMixin` для обеспечения  более широкой функциональности.

**Атрибуты**:

- `url (str)`: Базовый URL API сервиса `Free2GPT`.
- `working (bool)`: Флаг, указывающий на доступность сервиса. По умолчанию `True`.
- `supports_message_history (bool)`: Флаг, указывающий на возможность использования истории сообщений. В данном случае, `True`.
- `default_model (str)`:  Идентификатор модели по умолчанию - `gemini-1.5-pro`.
- `models (list)`: Список поддерживаемых моделей -  `['gemini-1.5-pro', 'gemini-1.5-flash']`.

**Методы**:

- `create_async_generator(model: str, messages: Messages, proxy: str = None, connector: BaseConnector = None, **kwargs) -> AsyncResult`

    **Назначение**: 
        Создает асинхронный генератор для получения ответов от модели `Free2GPT`.

    **Параметры**:

    - `model (str)`: Идентификатор модели.
    - `messages (Messages)`: Список сообщений для отправки в модель.
    - `proxy (str, optional)`: Прокси-сервер для использования. По умолчанию `None`.
    - `connector (BaseConnector, optional)`: Подключение `aiohttp` для использования. По умолчанию `None`.

    **Возвращает**:
        `AsyncResult`: Асинхронный результат, который содержит асинхронный генератор.

    **Вызывает исключения**:
        `RateLimitError`: Возникает, если достигнуто ограничение скорости запросов.

    **Как работает функция**:
        - Функция  создает сессию `aiohttp` с заголовками для отправки запросов к `Free2GPT`.
        -  Собирает информацию о времени запроса (в миллисекундах), сообщениях,  и генерирует хэш-подпись с помощью функции `generate_signature`.
        -  Отправляет POST-запрос к  `Free2GPT` с данными, включая модель, сообщения, время и подпись. 
        -  Обрабатывает  ответ сервера и  генерирует  асинхронный генератор для потоковой передачи ответа модели.


## Функции

### `generate_signature(time: int, text: str, secret: str = "")`

**Назначение**:
   Генерирует хэш-подпись для аутентификации запросов к API  `Free2GPT`.

**Параметры**:

- `time (int)`:  Текущее время в миллисекундах.
- `text (str)`:  Текст сообщения.
- `secret (str, optional)`:  Секретный ключ. По умолчанию `""`.

**Возвращает**:
   `str`: Хэш-подпись в формате шестнадцатеричного кода.

**Как работает функция**:
    -  Функция  собирает  информацию о времени, тексте сообщения и секретном ключе.
    -  Шифрует эту информацию с использованием алгоритма  `sha256`.
    -  Возвращает хэш-подпись в шестнадцатеричном формате.

## Примеры

### `Free2GPT.create_async_generator`

```python
# Пример использования
from src.endpoints.gpt4free.g4f.Provider.Free2GPT import Free2GPT
from src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [
        {"role": "user", "content": "Привет, как дела?"},
        {"role": "assistant", "content": "Отлично, а у тебя?"},
    ]
async def main():
    async for chunk in await Free2GPT.create_async_generator(model='gemini-1.5-pro', messages=messages):
        print(chunk, end='')

```

### `generate_signature`

```python
# Пример использования
from src.endpoints.gpt4free.g4f.Provider.Free2GPT import generate_signature

time = int(time.time() * 1e3)
text = "Привет, мир!"

signature = generate_signature(time, text)

print(f"Время: {time}, текст: {text}, подпись: {signature}")
```
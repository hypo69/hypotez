# Модуль GPROChat

## Обзор

Модуль `GPROChat` предназначен для асинхронного взаимодействия с сервисом GPROChat для генерации текста на основе предоставленных сообщений. Он использует асинхронные генераторы для обработки ответов и поддерживает прокси.

## Подробнее

Этот модуль предоставляет класс `GPROChat`, который наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`. Он предназначен для работы с API GPROChat, позволяя отправлять запросы на генерацию текста и получать результаты в асинхронном режиме. Модуль включает в себя функциональность для форматирования запросов, подписи запросов для аутентификации и обработки потоковых ответов.

## Классы

### `GPROChat`

**Описание**: Класс для взаимодействия с сервисом GPROChat.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает поддержку асинхронных генераторов для потоковой передачи данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `url` (str): URL сервиса GPROChat.
- `api_endpoint` (str): URL API для генерации текста.
- `working` (bool): Указывает, работает ли сервис.
- `supports_stream` (bool): Указывает, поддерживает ли сервис потоковую передачу данных.
- `supports_message_history` (bool): Указывает, поддерживает ли сервис историю сообщений.
- `default_model` (str): Модель, используемая по умолчанию.

**Методы**:
- `generate_signature(timestamp: int, message: str) -> str`: Генерирует подпись для запроса.
- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: Создает асинхронный генератор для получения ответов от сервиса.

## Методы класса

### `generate_signature`

```python
@staticmethod
def generate_signature(timestamp: int, message: str) -> str:
    """Генерирует подпись для запроса к API GPROChat.

    Args:
        timestamp (int): Временная метка запроса.
        message (str): Сообщение для подписи.

    Returns:
        str: Сгенерированная подпись.
    """
    ...
```

**Назначение**: Функция `generate_signature` создает подпись для запроса к API GPROChat, используя временную метку, сообщение и секретный ключ. Эта подпись используется для аутентификации запроса.

**Параметры**:
- `timestamp` (int): Временная метка запроса в миллисекундах.
- `message` (str): Сообщение, которое необходимо подписать.

**Возвращает**:
- `str`: Сгенерированная подпись в виде шестнадцатеричной строки.

**Как работает функция**:
1. Определяется секретный ключ `secret_key`.
2. Формируется строка `hash_input` путем конкатенации временной метки, сообщения и секретного ключа.
3. Вычисляется SHA256 хеш от `hash_input`.
4. Возвращается хеш в шестнадцатеричном формате.

**Примеры**:

```python
timestamp = int(time.time() * 1000)
message = "Hello, world!"
signature = GPROChat.generate_signature(timestamp, message)
print(f"Signature: {signature}")
```

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    **kwargs
) -> AsyncResult:
    """Создает асинхронный генератор для получения ответов от API GPROChat.

    Args:
        model (str): Модель для генерации текста.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от API.
    """
    ...
```

**Назначение**: Функция `create_async_generator` создает асинхронный генератор, который отправляет запросы к API GPROChat и возвращает ответы в виде потока данных.

**Параметры**:
- `model` (str): Модель, используемая для генерации текста.
- `messages` (Messages): Список сообщений для отправки в запросе.
- `proxy` (str, optional): URL прокси-сервера, если необходимо его использовать. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры, которые могут быть переданы в функцию.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, который выдает части ответа от API.

**Как работает функция**:
1. Получает модель, используя `cls.get_model(model)`.
2. Генерирует временную метку.
3. Форматирует сообщения в строку, используя `format_prompt(messages)`.
4. Генерирует подпись, используя `cls.generate_signature(timestamp, prompt)`.
5. Определяет заголовки запроса, включая User-Agent, Referer и Content-Type.
6. Формирует данные запроса, включая сообщения, временную метку и подпись.
7. Отправляет POST-запрос к API GPROChat с использованием `ClientSession`.
8. Итерируется по частям ответа и декодирует их.
9. Выдает декодированные части ответа через генератор.

**Примеры**:

```python
async def main():
    messages = [{"role": "user", "content": "Hello, world!"}]
    async for chunk in GPROChat.create_async_generator(model="gemini-1.5-pro", messages=messages):
        print(chunk, end="")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```
```python
import asyncio
from aiohttp import ClientSession

async def call_api(messages):
    # prompt = format_prompt(messages)
    timestamp = int(time.time() * 1000)
    # sign = cls.generate_signature(timestamp, prompt)
    data = {
        "messages": [{"role": "user", "parts": [{"text": messages}]}],
        "time": timestamp,
        "pass": None,
        "sign": '...' # <инструкция для модели gemini:Замени этот знак `...` на правильный sign, вычисленный на основе параметров messages и timestamp>
    }
    headers = {
        "accept": "*/*",
        "origin": "https://gprochat.com",
        "referer": "https://gprochat.com/",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "content-type": "text/plain;charset=UTF-8"
    }

    async with ClientSession(headers=headers) as session:
        async with session.post("https://gprochat.com/api/generate", json=data) as response:
            response.raise_for_status()
            async for chunk in response.content.iter_any():
                if chunk:
                    yield chunk.decode()

async def main():
    messages = "Как создать веб-сервер на Python?"
    async for message in call_api(messages):
        print(message)

if __name__ == "__main__":
    asyncio.run(main())
```
```
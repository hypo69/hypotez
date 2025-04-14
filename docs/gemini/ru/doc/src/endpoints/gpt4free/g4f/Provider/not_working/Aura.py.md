# Модуль Aura.py

## Обзор

Модуль `Aura.py` предоставляет асинхронный генератор для взаимодействия с моделью OpenChat 3.6 через API `openchat.team`. Он позволяет отправлять сообщения и получать ответы в виде чанков, используя асинхронные запросы.

## Подробней

Этот модуль является частью проекта `hypotez` и предназначен для интеграции с различными AI-провайдерами. Он использует библиотеку `aiohttp` для выполнения асинхронных HTTP-запросов. Модуль поддерживает прокси и позволяет настраивать температуру и максимальное количество токенов для генерации ответов.

## Классы

### `Aura`

**Описание**: Класс `Aura` предоставляет асинхронный генератор для взаимодействия с моделью OpenChat 3.6 через API `openchat.team`.
**Наследует**: `AsyncGeneratorProvider`.

**Атрибуты**:

- `url` (str): URL API `openchat.team`.
- `working` (bool): Указывает, работает ли провайдер (в данном случае `False`).

**Методы**:

- `create_async_generator`: Создает асинхронный генератор для получения ответов от API.

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        temperature: float = 0.5,
        max_tokens: int = 8192,
        webdriver = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для получения ответов от API OpenChat 3.6.

        Args:
            model (str): Не используется.
            messages (Messages): Список сообщений для отправки в API.
            proxy (str, optional): Прокси-сервер для использования при подключении к API. По умолчанию `None`.
            temperature (float, optional): Температура для генерации ответов. По умолчанию 0.5.
            max_tokens (int, optional): Максимальное количество токенов в ответе. По умолчанию 8192.
            webdriver: Не используется.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, который возвращает чанки ответа от API.

        Raises:
            aiohttp.ClientResponseError: Если возникает ошибка при выполнении HTTP-запроса.
        """
        ...
```

**Как работает функция**:

1.  Получает аргументы из браузера, используя функцию `get_args_from_browser`.
2.  Инициализирует асинхронную сессию с использованием `aiohttp.ClientSession`.
3.  Разделяет входные сообщения на системные и обычные сообщения.
4.  Формирует данные для отправки в API, включая модель, сообщения, ключ, системное сообщение и температуру.
5.  Выполняет POST-запрос к API `openchat.team` с использованием асинхронной сессии.
6.  Итерируется по чанкам ответа от API и возвращает их через генератор.

```python
async with ClientSession(**args) as session:
    new_messages = []
    system_message = []
    for message in messages:
        if message["role"] == "system":
            system_message.append(message["content"])
        else:
            new_messages.append(message)
    data = {
        "model": {
            "id": "openchat_3.6",
            "name": "OpenChat 3.6 (latest)",
            "maxLength": 24576,
            "tokenLimit": max_tokens
        },
        "messages": new_messages,
        "key": "",
        "prompt": "\\n".join(system_message),
        "temperature": temperature
    }
    async with session.post(f"{cls.url}/api/chat", json=data, proxy=proxy) as response:
        response.raise_for_status()
        async for chunk in response.content.iter_any():
            yield chunk.decode(error="ignore")
```

**Примеры**:

Пример использования функции `create_async_generator`:

```python
model = "openchat_3.6"
messages = [
    {"role": "user", "content": "Hello, how are you?"},
]
#Предположим, что get_args_from_browser() определена где-то в другом месте кода и импортирована
#args = get_args_from_browser(cls.url, webdriver, proxy)  #Вызов невозможен. Требуется реализация get_args_from_browser

#async def main():
#    async for chunk in Aura.create_async_generator(model=model, messages=messages):
#        print(chunk, end="")

#import asyncio
#asyncio.run(main())
# Модуль Aibn
## Обзор

Модуль `Aibn` предоставляет реализацию асинхронного генератора `AsyncGeneratorProvider` для работы с API AIBN.CC. Он реализует поддержку истории сообщений и модели GPT-3.5 Turbo.

## Подробей

Модуль `Aibn` предоставляет доступ к API AIBN.CC для работы с различными моделями. Он реализован с помощью класса `Aibn`, который наследует от `AsyncGeneratorProvider`. В этом модуле используются такие библиотеки, как:
- `StreamSession` для управления HTTP запросами
- `hashlib` для создания хеш-сумм

Этот модуль играет важную роль в обработке запросов к AIBN.CC, предоставляя возможности для взаимодействия с этим API. 

## Классы

### `Aibn`

**Описание**: Класс `Aibn` реализует асинхронный генератор `AsyncGeneratorProvider` для работы с API AIBN.CC.
**Наследует**: `AsyncGeneratorProvider`
**Атрибуты**:
- `url` (str): URL API AIBN.CC.
- `working` (bool): Индикатор доступности сервиса.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `supports_gpt_35_turbo` (bool): Флаг, указывающий на поддержку модели GPT-3.5 Turbo.

**Методы**:
- `create_async_generator(model: str, messages: Messages, proxy: str = None, timeout: int = 120, **kwargs) -> AsyncResult`: Асинхронная функция, создающая асинхронный генератор для получения ответов от API AIBN.CC.

## Функции

### `generate_signature`

**Назначение**: Генерация хеш-суммы для подписи запроса к API AIBN.CC.

**Параметры**:
- `timestamp` (int): Время запроса в секундах.
- `message` (str): Текст последнего сообщения.
- `secret` (str): Секретный ключ для подписи запроса (по умолчанию `undefined`).

**Возвращает**:
- `str`: Хеш-сумма запроса в виде шестнадцатеричного кода.

**Как работает функция**:
- Функция объединяет timestamp, текст сообщения и секретный ключ в строку.
- Затем она создает хеш-сумму этой строки с помощью алгоритма SHA-256.
- Хеш-сумма возвращается в виде шестнадцатеричного кода.

**Пример**:

```python
>>> generate_signature(timestamp=1680571937, message="Hello, world!", secret="undefined")
'5121e4138f19a464345e2210a3a051e59a01e142653e3d1d32361e007827608e'
```

## Примеры

### Пример использования `Aibn`

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Aibn import Aibn
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages = Messages([
    {"role": "user", "content": "Hello, world!"}
])

async def main():
    async for chunk in await Aibn.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        print(chunk)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

```

### Пример использования `generate_signature`

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Aibn import generate_signature

timestamp = int(time.time())
message = "Hello, world!"
secret = "undefined"

signature = generate_signature(timestamp, message, secret)

print(signature)

```
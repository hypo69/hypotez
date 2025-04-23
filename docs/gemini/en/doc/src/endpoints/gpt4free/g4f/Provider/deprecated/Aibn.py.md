# Module `Aibn`

## Overview

Модуль предоставляет асинхронный генератор для взаимодействия с провайдером Aibn.cc.
Он поддерживает GPT-3.5 Turbo, предоставляет возможности для работы с историей сообщений,
а также обеспечивает генерацию подписи для запросов.

## More details

Этот модуль используется для асинхронной генерации ответов от модели Aibn.cc.
Он включает в себя функции для создания асинхронного генератора и генерации подписи для обеспечения безопасности запросов.

## Classes

### `Aibn`

**Description**:
Класс `Aibn` является асинхронным генераторным провайдером, который взаимодействует с сервисом Aibn.cc.

**Inherits**:
Наследуется от класса `AsyncGeneratorProvider`.

**Attributes**:
- `url` (str): URL адрес сервиса Aibn.cc.
- `working` (bool): Флаг, указывающий, работает ли провайдер в данный момент.
- `supports_message_history` (bool): Флаг, указывающий, поддерживает ли провайдер историю сообщений.
- `supports_gpt_35_turbo` (bool): Флаг, указывающий, поддерживает ли провайдер модель GPT-3.5 Turbo.

**Methods**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от Aibn.cc.

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    timeout: int = 120,
    **kwargs
) -> AsyncResult:
    """ Функция создает асинхронный генератор для получения ответов от Aibn.cc.

    Args:
        cls (Aibn): Класс Aibn.
        model (str): Название модели.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): Прокси-сервер для использования. Defaults to None.
        timeout (int, optional): Время ожидания ответа. Defaults to 120.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий ответы от Aibn.cc.

    How the function works:
        - Функция принимает параметры модели, сообщений, прокси и таймаута.
        - Создается асинхронная сессия с использованием `StreamSession`.
        - Формируются данные для отправки, включая подпись запроса.
        - Отправляется POST запрос к Aibn.cc.
        - Асинхронно читаются чанки ответа и декодируются.

    """
```

### Class Parameters

- `model` (str): Имя модели, используемой для генерации ответа.
- `messages` (Messages): Список сообщений, отправляемых в запросе.
- `proxy` (str, optional): Адрес прокси-сервера для использования при подключении. По умолчанию `None`.
- `timeout` (int, optional): Максимальное время ожидания ответа от сервера в секундах. По умолчанию 120.
- `**kwargs`: Дополнительные параметры, которые могут быть переданы.

**Examples**:

```python
# Пример использования create_async_generator
model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "Hello, Aibn!"}]
proxy = "http://your_proxy:8080"
timeout = 120

# Вызов функции create_async_generator
async def main():
    async for chunk in Aibn.create_async_generator(model=model, messages=messages, proxy=proxy, timeout=timeout):
        print(chunk)
```

## Functions

### `generate_signature`

```python
def generate_signature(timestamp: int, message: str, secret: str = "undefined"):
    """ Функция генерирует подпись запроса на основе временной метки, сообщения и секретного ключа.

    Args:
        timestamp (int): Временная метка.
        message (str): Сообщение для подписи.
        secret (str, optional): Секретный ключ. Defaults to "undefined".

    Returns:
        str: SHA256 хэш, представляющий подпись.

    How the function works:
        - Функция принимает временную метку, сообщение и секретный ключ.
        - Формируется строка данных для подписи.
        - Вычисляется SHA256 хэш от строки данных.
        - Возвращается хэш в шестнадцатеричном формате.
    """
```

### Function Parameters

- `timestamp` (int): Временная метка для генерации подписи.
- `message` (str): Сообщение, которое необходимо подписать.
- `secret` (str, optional): Секретный ключ, используемый при генерации подписи. По умолчанию `"undefined"`.

**Examples**:

```python
# Пример использования generate_signature
timestamp = int(time.time())
message = "Hello, Aibn!"
secret = "my_secret_key"

signature = generate_signature(timestamp=timestamp, message=message, secret=secret)
print(signature)
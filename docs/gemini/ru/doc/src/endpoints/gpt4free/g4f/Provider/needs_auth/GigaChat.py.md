# Модуль GigaChat

## Обзор

Модуль `GigaChat` предоставляет асинхронный генератор для взаимодействия с моделью GigaChat от Сбербанка. 

## Подробней

Этот модуль используется для отправки запросов к API GigaChat и получения ответов в виде потока текста. Он поддерживает различные модели, такие как `GigaChat:latest`, `GigaChat-Plus` и `GigaChat-Pro`, а также обеспечивает аутентификацию с помощью токена доступа. 

## Классы

### `class GigaChat`

**Описание**: Класс `GigaChat` наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`, предоставляет функциональность для работы с GigaChat API.

**Наследует**: 
 - `AsyncGeneratorProvider` - Базовый класс для асинхронных генераторов, предоставляющих доступ к API.
 - `ProviderModelMixin` - Класс-микшин, который предоставляет методы для управления моделями.

**Атрибуты**:

 - `url` (str): URL-адрес API GigaChat.
 - `working` (bool): Флаг, указывающий на доступность модели.
 - `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
 - `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений.
 - `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи ответов.
 - `needs_auth` (bool): Флаг, указывающий на необходимость аутентификации.
 - `default_model` (str): Имя модели по умолчанию.
 - `models` (list): Список доступных моделей.

**Методы**:

 - `create_async_generator(model: str, messages: Messages, stream: bool = True, proxy: str = None, api_key: str = None, connector: BaseConnector = None, scope: str = "GIGACHAT_API_PERS", update_interval: float = 0, **kwargs) -> AsyncResult`

#### `def create_async_generator`

**Назначение**: Асинхронная функция, которая создает генератор для обработки запросов к GigaChat API.

**Параметры**:

 - `model` (str): Имя модели, которую нужно использовать.
 - `messages` (Messages): Список сообщений для отправки в API.
 - `stream` (bool, optional): Флаг, указывающий на использование потоковой передачи. По умолчанию `True`.
 - `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
 - `api_key` (str, optional): Токен доступа для аутентификации. По умолчанию `None`.
 - `connector` (BaseConnector, optional): Подключение для отправки запросов. По умолчанию `None`.
 - `scope` (str, optional): Область действия токена доступа. По умолчанию `GIGACHAT_API_PERS`.
 - `update_interval` (float, optional): Интервал обновления потока в секундах. По умолчанию `0`.
 - `**kwargs`: Дополнительные параметры для запроса.

**Возвращает**:

 - `AsyncResult`: Асинхронный результат обработки запроса.

**Вызывает исключения**:

 - `MissingAuthError`: Если токен доступа не был указан.

**Пример**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.GigaChat import GigaChat

async def main():
    async with GigaChat.create_async_generator(model='GigaChat:latest', messages=[{'role': 'user', 'content': 'Привет'}], api_key='YOUR_API_KEY') as response:
        async for chunk in response:
            print(chunk)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

## Параметры класса

 - `access_token` (str): Токен доступа, используемый для аутентификации.
 - `token_expires_at` (int): Время истечения срока действия токена доступа в миллисекундах.
 - `RUSSIAN_CA_CERT` (str): Сертификат CA, используемый для проверки SSL-соединения.

**Пример**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.GigaChat import GigaChat

# Создать экземпляр класса GigaChat
gigachat = GigaChat()

# Получить токен доступа
access_token = gigachat.access_token

# Получить время истечения срока действия токена
token_expires_at = gigachat.token_expires_at

# Получить сертификат CA
russian_ca_cert = gigachat.RUSSIAN_CA_CERT
```

**Как работает функция**:

 - `create_async_generator`  сначала проверяет наличие токена доступа. Если токен не был указан, то вызывается исключение `MissingAuthError`.
 - Затем создается сертификат CA в директории `cookies_dir` и записывается в файл `russian_trusted_root_ca.crt`.
 - Создается сессия HTTP с использованием `ClientSession`.
 - Если токен доступа устарел, то он обновляется с помощью запроса к API `https://ngw.devices.sberbank.ru:9443/api/v2/oauth`.
 - Отправляется запрос к GigaChat API с использованием метода `session.post`.
 - Полученные данные декодируются из JSON и преобразуются в список строк.
 - Каждая строка в списке обрабатывается в цикле `for` и отправляется в генератор.

**Примеры**:

 - Отправить сообщение и получить ответ:

```python
async with GigaChat.create_async_generator(model='GigaChat:latest', messages=[{'role': 'user', 'content': 'Привет'}], api_key='YOUR_API_KEY') as response:
    async for chunk in response:
        print(chunk)
```

 - Отправить несколько сообщений и получить ответ:

```python
async with GigaChat.create_async_generator(model='GigaChat:latest', messages=[{'role': 'user', 'content': 'Привет'}, {'role': 'user', 'content': 'Как дела?'}], api_key='YOUR_API_KEY') as response:
    async for chunk in response:
        print(chunk)
```

 - Использовать прокси-сервер:

```python
async with GigaChat.create_async_generator(model='GigaChat:latest', messages=[{'role': 'user', 'content': 'Привет'}], api_key='YOUR_API_KEY', proxy='http://your_proxy_address:your_proxy_port') as response:
    async for chunk in response:
        print(chunk)
```

 - Установить интервал обновления потока:

```python
async with GigaChat.create_async_generator(model='GigaChat:latest', messages=[{'role': 'user', 'content': 'Привет'}], api_key='YOUR_API_KEY', update_interval=1) as response:
    async for chunk in response:
        print(chunk)
```

 - Использовать модель `GigaChat-Plus`:

```python
async with GigaChat.create_async_generator(model='GigaChat-Plus', messages=[{'role': 'user', 'content': 'Привет'}], api_key='YOUR_API_KEY') as response:
    async for chunk in response:
        print(chunk)
```

 - Использовать модель `GigaChat-Pro`:

```python
async with GigaChat.create_async_generator(model='GigaChat-Pro', messages=[{'role': 'user', 'content': 'Привет'}], api_key='YOUR_API_KEY') as response:
    async for chunk in response:
        print(chunk)
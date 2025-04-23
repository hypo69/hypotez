# Module `Koala.py`

## Overview

Модуль предоставляет асинхронтный генератор для взаимодействия с сервисом Koala.sh, используя его API для обмена сообщениями с моделью `gpt-4o-mini` или другой указанной моделью. Поддерживает прокси и передачу истории сообщений.

## More details

Модуль предназначен для интеграции с сервисом Koala.sh, предоставляющим доступ к различным моделям GPT. Он отправляет запросы к API Koala.sh и обрабатывает ответы в режиме реального времени. Модуль использует `aiohttp` для асинхронных HTTP-запросов и поддерживает проксирование.

## Classes

### `Koala`

**Description**: Класс `Koala` является асинхронным генератором провайдера и реализует взаимодействие с API Koala.sh.

**Inherits**:
- `AsyncGeneratorProvider`: Базовый класс для асинхронных генераторов провайдеров.
- `ProviderModelMixin`: Миксин для работы с моделями провайдера.

**Attributes**:
- `url` (str): URL сервиса Koala.sh.
- `api_endpoint` (str): URL API Koala.sh для обмена сообщениями.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `default_model` (str): Модель, используемая по умолчанию, если не указана другая.

**Working principle**:
Класс `Koala` использует асинхронные генераторы для обмена сообщениями с API Koala.sh. Он формирует HTTP-запросы с необходимыми заголовками и данными, отправляет их на сервер и обрабатывает ответы в режиме реального времени. Класс также поддерживает проксирование и передачу истории сообщений.

**Methods**:
- `create_async_generator`: Создает асинхронный генератор для обмена сообщениями.
- `_parse_event_stream`: Разбирает поток событий, возвращаемый сервером.

## Class Methods

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: Optional[str] = None,
        connector: Optional[BaseConnector] = None,
        **kwargs: Any
    ) -> AsyncGenerator[Dict[str, Union[str, int, float, List[Dict[str, Any]], None]], None]:
        """Создает асинхронный генератор для обмена сообщениями с API Koala.sh.

        Args:
            model (str): Модель, используемая для генерации ответов.
            messages (Messages): Список сообщений для отправки на сервер.
            proxy (Optional[str], optional): URL прокси-сервера. Defaults to None.
            connector (Optional[BaseConnector], optional): Aiohttp коннектор. Defaults to None.
            **kwargs (Any): Дополнительные параметры.

        Returns:
            AsyncGenerator[Dict[str, Union[str, int, float, List[Dict[str, Any]], None]], None]: Асинхронный генератор, возвращающий словари с данными от сервера.

        Raises:
            Exception: Если возникает ошибка при отправке запроса или обработке ответа.

        Принцип работы:
            Функция создает асинхронный генератор, который отправляет POST-запрос к API Koala.sh с использованием `aiohttp`.
            Она формирует заголовки и данные запроса, включая историю сообщений и параметры модели.
            Затем она разбирает поток событий, возвращаемый сервером, и передает данные через генератор.

        """
        ...
```

**Examples**:

```python
# Example of creating an asynchronous generator
# Assuming you have defined 'messages' and 'model'
# async for chunk in Koala.create_async_generator(model=model, messages=messages):
#     print(chunk)
```

### `_parse_event_stream`

```python
    @staticmethod
    async def _parse_event_stream(response: ClientResponse) -> AsyncGenerator[Dict[str, Any], None]:
        """Разбирает поток событий, возвращаемый сервером Koala.sh.

        Args:
            response (ClientResponse): Объект ответа `aiohttp.ClientResponse`.

        Returns:
            AsyncGenerator[Dict[str, Any], None]: Асинхронный генератор, возвращающий словари с данными из потока событий.

        Принцип работы:
            Функция асинхронно итерируется по содержимому ответа и извлекает данные, начинающиеся с префикса "data: ".
            Она преобразует эти данные из JSON-формата в словарь и передает их через генератор.

        """
        ...
```

**Examples**:

```python
# Example of parsing an event stream
# Assuming you have 'response' from a request
# async for chunk in Koala._parse_event_stream(response):
#     print(chunk)
```

## Class Parameters

- `url` (str): URL сервиса Koala.sh. Используется для формирования ссылок и заголовков запросов.
- `api_endpoint` (str): URL API Koala.sh для обмена сообщениями. Используется для отправки POST-запросов с данными.
- `working` (bool): Флаг, указывающий на работоспособность провайдера. Может использоваться для проверки доступности сервиса.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений. Определяет, будет ли история сообщений передаваться в запросах.
- `default_model` (str): Модель, используемая по умолчанию, если не указана другая. Например, "gpt-4o-mini".
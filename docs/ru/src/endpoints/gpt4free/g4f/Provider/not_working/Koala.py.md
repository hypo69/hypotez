# Документация для разработчика: `Koala.py`

## Обзор

Файл `Koala.py` является частью проекта `hypotez` и содержит класс `Koala`, который предоставляет асинхронный интерфейс для взаимодействия с моделью Koala AI. Этот класс позволяет генерировать текст на основе предоставленных сообщений, используя Koala API. Модуль поддерживает ведение истории сообщений и использует асинхронные генераторы для обработки потока данных.

## Подробнее

`Koala.py` расположен в директории `hypotez/src/endpoints/gpt4free/g4f/Provider/not_working/` и, судя по названию директории `not_working`, в данный момент не функционирует. Тем не менее, модуль содержит класс `Koala`, который реализует взаимодействие с API Koala для генерации текста на основе входных сообщений. Класс использует `aiohttp` для выполнения асинхронных HTTP-запросов и предоставляет метод для парсинга потока событий, возвращаемого API.

## Классы

### `Koala`

**Описание**: Класс `Koala` предоставляет асинхронный интерфейс для взаимодействия с моделью Koala AI. Он позволяет генерировать текст на основе предоставленных сообщений и поддерживает ведение истории сообщений.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `url` (str): URL главной страницы Koala.
- `api_endpoint` (str): URL API для взаимодействия с Koala.
- `working` (bool): Указывает, работает ли провайдер в данный момент.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
- `default_model` (str): Модель, используемая по умолчанию, если не указана другая.

**Методы**:
- `create_async_generator()`: Создает асинхронный генератор для получения ответов от Koala API.
- `_parse_event_stream()`: Статический метод для парсинга потока событий, возвращаемого API.

## Методы класса

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
    """
    Создает асинхронный генератор для получения ответов от Koala API.

    Args:
        model (str): Модель для использования.
        messages (Messages): Список сообщений для отправки в API.
        proxy (Optional[str], optional): Прокси-сервер для использования. По умолчанию `None`.
        connector (Optional[BaseConnector], optional): Aiohttp коннектор для использования. По умолчанию `None`.
        **kwargs (Any): Дополнительные аргументы.

    Returns:
        AsyncGenerator[Dict[str, Union[str, int, float, List[Dict[str, Any]], None]], None]:
            Асинхронный генератор, выдающий словарь с ответами от API.

    Raises:
        Exception: Если возникает ошибка при отправке запроса или обработке ответа.
    """
```

**Назначение**:
Создает асинхронный генератор, который отправляет сообщения в Koala API и возвращает ответы в виде асинхронного потока данных.

**Параметры**:
- `cls`: Ссылка на класс `Koala`.
- `model` (str): Модель для использования при генерации ответа. Если не указана, используется `gpt-4o-mini`.
- `messages` (Messages): Список сообщений, представляющих историю разговора. Каждое сообщение содержит роль (`user`, `assistant`, `system`) и содержимое.
- `proxy` (Optional[str], optional): Прокси-сервер для использования при отправке запроса. По умолчанию `None`.
- `connector` (Optional[BaseConnector], optional): Объект `BaseConnector` из `aiohttp` для управления соединениями. По умолчанию `None`.
- `**kwargs` (Any): Дополнительные параметры, которые могут быть переданы в API.

**Возвращает**:
- `AsyncGenerator[Dict[str, Union[str, int, float, List[Dict[str, Any]], None]], None]`: Асинхронный генератор, который выдает словари, содержащие ответы от API. Каждый словарь может содержать текст ответа, информацию о модели и другие данные.

**Как работает функция**:
1. **Подготовка заголовков**: Функция создает заголовки HTTP-запроса, включая User-Agent, Referer, Origin и другие необходимые параметры. Visitor-ID генерируется случайным образом.
2. **Формирование данных запроса**: На основе входных сообщений формируется тело запроса в формате JSON. История сообщений пользователя и ассистента разделяется и включается в запрос.
3. **Отправка запроса**: Используя `aiohttp.ClientSession`, функция отправляет POST-запрос на `api_endpoint` с сформированными заголовками и данными. Если указан прокси, он также используется.
4. **Обработка ответа**: Функция вызывает `raise_for_status` для проверки статуса ответа. Затем она передает ответ в функцию `_parse_event_stream` для парсинга потока событий.
5. **Генерация данных**: Асинхронно перебирает чанки (фрагменты) из потока событий, возвращаемого `_parse_event_stream`, и выдает их.

**Примеры**:

```python
import asyncio
from typing import List, Dict, Any, AsyncGenerator, Union
from aiohttp import ClientSession

# from src.endpoints.gpt4free.g4f.provider_helper import get_random_string # пришлось закомментировать, так как у меня нет этого модуля
# from src.endpoints.gpt4free.g4f.requests import raise_for_status # пришлось закомментировать, так как у меня нет этого модуля
# from src.endpoints.gpt4free.g4f.base_provider import AsyncGeneratorProvider # пришлось закомментировать, так как у меня нет этого модуля
# from src.endpoints.gpt4free.g4f.provider_helper import get_connector # пришлось закомментировать, так как у меня нет этого модуля

# class Koala(AsyncGeneratorProvider): # пришлось закомментировать, так как класс уже определен в коде
#     url = "https://koala.sh/chat" # пришлось закомментировать, так как класс уже определен в коде
#     api_endpoint = "https://koala.sh/api/gpt/" # пришлось закомментировать, так как класс уже определен в коде
#     working = True # пришлось закомментировать, так как класс уже определен в коде
#     supports_message_history = True # пришлось закомментировать, так как класс уже определен в коде
#     default_model = 'gpt-4o-mini' # пришлось закомментировать, так как класс уже определен в коде
#
#     @classmethod
#     async def create_async_generator(
#         cls,
#         model: str,
#         messages: List[Dict[str, str]],
#         proxy: str = None,
#         connector: ClientSession = None,
#         **kwargs: Any
#     ) -> AsyncGenerator[Dict[str, Union[str, int, float, List[Dict[str, Any]], None]], None]:
#         if not model:
#             model = "gpt-4o-mini"
#
#         headers = {
#             "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
#             "Accept": "text/event-stream",
#             "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
#             "Accept-Encoding": "gzip, deflate, br",
#             "Referer": f"{cls.url}",
#             "Flag-Real-Time-Data": "false",
#             # "Visitor-ID": get_random_string(20), # пришлось закомментировать, так как у меня нет этого модуля
#             "Origin": "https://koala.sh",
#             "Alt-Used": "koala.sh",
#             "Sec-Fetch-Dest": "empty",
#             "Sec-Fetch-Mode": "cors",
#             "Sec-Fetch-Site": "same-origin",
#             "TE": "trailers",
#         }
#
#         async with ClientSession(headers=headers) as session: # connector=get_connector(connector, proxy)
#             input_text = messages[-1]["content"]
#             system_messages = " ".join(
#                 message["content"] for message in messages if message["role"] == "system"
#             )
#             if system_messages:
#                 input_text += f" {system_messages}"
#
#             data = {
#                 "input": input_text,
#                 "inputHistory": [
#                     message["content"]
#                     for message in messages[:-1]
#                     if message["role"] == "user"
#                 ],
#                 "outputHistory": [
#                     message["content"]
#                     for message in messages
#                     if message["role"] == "assistant"
#                 ],
#                 "model": model,
#             }
#
#             async with session.post(f"{cls.api_endpoint}", json=data, proxy=proxy) as response:
#                 # await raise_for_status(response) # пришлось закомментировать, так как у меня нет этого модуля
#                 async for chunk in Koala._parse_event_stream(response):
#                     yield chunk
#
#     @staticmethod
#     async def _parse_event_stream(response: ClientResponse) -> AsyncGenerator[Dict[str, Any], None]:
#         async for chunk in response.content:
#             if chunk.startswith(b"data: "):
#                 yield json.loads(chunk[6:])

# Пример использования:
async def main():
    messages = [
        {"role": "user", "content": "Привет, как дела?"},
        {"role": "assistant", "content": "У меня все отлично, спасибо!"},
        {"role": "user", "content": "Расскажи что-нибудь интересное."},
    ]
    model = "gpt-4o-mini"
    proxy = None

    # generator = Koala.create_async_generator(model=model, messages=messages, proxy=proxy) # пришлось закомментировать, так как класс уже определен в коде
    # async for item in generator: # пришлось закомментировать, так как класс уже определен в коде
    #     print(item) # пришлось закомментировать, так как класс уже определен в коде

if __name__ == "__main__":
    asyncio.run(main())
```

### `_parse_event_stream`

```python
    @staticmethod
    async def _parse_event_stream(response: ClientResponse) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Разбирает поток событий, возвращаемый API, и извлекает данные.

        Args:
            response (ClientResponse): Объект ответа от API.

        Returns:
            AsyncGenerator[Dict[str, Any], None]: Асинхронный генератор, выдающий словари с данными из потока событий.
        """
```

**Назначение**:
Разбирает поток событий, полученный от Koala API, и извлекает полезные данные из каждого чанка.

**Параметры**:
- `response` (ClientResponse): Объект ответа от API, содержащий поток данных.

**Возвращает**:
- `AsyncGenerator[Dict[str, Any], None]`: Асинхронный генератор, который выдает словари, содержащие данные из потока событий.

**Как работает функция**:
1. **Чтение потока**: Функция асинхронно перебирает чанки (фрагменты) из содержимого ответа (`response.content`).
2. **Проверка префикса**: Для каждого чанка проверяется, начинается ли он с префикса `b"data: "`.
3. **Извлечение данных**: Если чанк начинается с указанного префикса, из него извлекаются данные, удаляется префикс (`chunk[6:]`), и строка преобразуется из JSON в словарь с помощью `json.loads()`.
4. **Генерация данных**: Извлеченный словарь выдается как результат работы генератора.

**Примеры**:

```python
import asyncio
from aiohttp import ClientSession

# from src.endpoints.gpt4free.g4f.provider_helper import get_random_string # пришлось закомментировать, так как у меня нет этого модуля
# from src.endpoints.gpt4free.g4f.requests import raise_for_status # пришлось закомментировать, так как у меня нет этого модуля

# class Koala: # пришлось закомментировать, так как класс уже определен в коде
#     url = "https://koala.sh/chat" # пришлось закомментировать, так как класс уже определен в коде
#     api_endpoint = "https://koala.sh/api/gpt/" # пришлось закомментировать, так как класс уже определен в коде
#     working = True # пришлось закомментировать, так как класс уже определен в коде
#     supports_message_history = True # пришлось закомментировать, так как класс уже определен в коде
#     default_model = 'gpt-4o-mini' # пришлось закомментировать, так как класс уже определен в коде

#     @staticmethod
#     async def _parse_event_stream(response: ClientResponse):
#         async for chunk in response.content:
#             if chunk.startswith(b"data: "):
#                 yield json.loads(chunk[6:])

async def main():
    # Пример использования _parse_event_stream
    async with ClientSession() as session:
        # Создаем фиктивный объект response для примера
        class MockResponse:
            async def __aiter__(self):
                yield b'data: {"text": "Первый фрагмент"} '
                yield b'data: {"text": "Второй фрагмент"} '
                yield b'data: {"text": "Третий фрагмент"} '

            @property
            def content(self):
                return self

        mock_response = MockResponse()

        async for item in Koala._parse_event_stream(mock_response):
            print(item)

if __name__ == "__main__":
    asyncio.run(main())
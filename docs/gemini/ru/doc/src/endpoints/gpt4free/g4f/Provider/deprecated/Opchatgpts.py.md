# Модуль Opchatgpts

## Обзор

Модуль `Opchatgpts` предоставляет асинхронный генератор для взаимодействия с сервисом `opchatgpts.net`, предоставляющим доступ к API модели GPT-3.5 Turbo. 

## Подробней

Модуль наследует класс `AsyncGeneratorProvider`, предоставляя базовый функционал для асинхронного генератора.

## Классы

### `Opchatgpts`

**Описание**: Класс реализует асинхронный генератор для получения ответов от API модели GPT-3.5 Turbo с использованием сервиса `opchatgpts.net`.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:

- `url` (str): URL-адрес сервиса `opchatgpts.net`.
- `working` (bool): Флаг, показывающий, работает ли сервис. 
- `supports_message_history` (bool): Флаг, показывающий, поддерживает ли сервис историю сообщений. 
- `supports_gpt_35_turbo` (bool): Флаг, показывающий, поддерживает ли сервис модель GPT-3.5 Turbo.

**Методы**:

- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: Асинхронный генератор, который отправляет сообщения в API модели GPT-3.5 Turbo и получает ответы. 

## Методы класса

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None, **kwargs) -> AsyncResult:
        
        headers = {
            "User-Agent"         : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
            "Accept"             : "*/*",
            "Accept-Language"    : "de,en-US;q=0.7,en;q=0.3",
            "Origin"             : cls.url,
            "Alt-Used"           : "opchatgpts.net",
            "Referer"            : f"{cls.url}/chatgpt-free-use/",
            "Sec-Fetch-Dest"     : "empty",
            "Sec-Fetch-Mode"     : "cors",
            "Sec-Fetch-Site"     : "same-origin",
        }
        async with ClientSession(
            headers=headers
        ) as session:
            data = {
                "botId": "default",
                "chatId": get_random_string(),
                "contextId": 28,
                "customId": None,
                "messages": messages,
                "newMessage": messages[-1]["content"],
                "session": "N/A",
                "stream": True
            }
            async with session.post(f"{cls.url}/wp-json/mwai-ui/v1/chats/submit", json=data, proxy=proxy) as response:
                response.raise_for_status()
                async for line in response.content:
                    if line.startswith(b"data: "):
                        try:
                            line = json.loads(line[6:])
                            assert "type" in line
                        except:
                            raise RuntimeError(f"Broken line: {line.decode()}")
                        if line["type"] == "live":
                            yield line["data"]
                        elif line["type"] == "end":
                            break
                ```

**Назначение**: Метод создает асинхронный генератор, который отправляет запросы к API модели GPT-3.5 Turbo через сервис `opchatgpts.net`.

**Параметры**:

- `model` (str):  Название модели GPT-3.5 Turbo.
- `messages` (Messages): Список сообщений для отправки в API. 
- `proxy` (str, optional): Прокси-сервер для отправки запросов. По умолчанию `None`.

**Возвращает**:

- `AsyncResult`: Асинхронный результат с генератором для получения ответов от модели GPT-3.5 Turbo.

**Как работает метод**:

1. Метод формирует заголовок запроса (headers).
2. Создает клиентское соединение с помощью `ClientSession`.
3. Формирует данные для отправки в API, включая `messages`, `chatId` и другие параметры.
4. Отправляет POST-запрос к `https://opchatgpts.net/wp-json/mwai-ui/v1/chats/submit`.
5. Проверяет статус ответа.
6. Читает ответ по частям (асинхронно) с использованием `response.content`.
7. Парсит полученные данные в JSON-формат.
8. Фильтрует данные по типу ("live" или "end").
9. Выдает данные с помощью генератора `yield`.

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Opchatgpts import Opchatgpts
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создание списка сообщений
messages: Messages = [
    {"role": "user", "content": "Привет! Как дела?"},
    {"role": "assistant", "content": "Хорошо, спасибо! А у тебя?"},
]

# Создание асинхронного генератора
async_generator = Opchatgpts.create_async_generator(model='gpt-3.5-turbo', messages=messages)

# Получение ответов от модели GPT-3.5 Turbo
async for response in async_generator:
    print(response)
```

## Параметры класса

- `url` (str): URL-адрес сервиса `opchatgpts.net`.
- `working` (bool): Флаг, показывающий, работает ли сервис. 
- `supports_message_history` (bool): Флаг, показывающий, поддерживает ли сервис историю сообщений. 
- `supports_gpt_35_turbo` (bool): Флаг, показывающий, поддерживает ли сервис модель GPT-3.5 Turbo.
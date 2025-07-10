# Модуль AiChats

## Обзор

Модуль `AiChats` реализует класс `AiChats`, который предоставляет асинхронный генератор для взаимодействия с API сервиса `Ai-Chats`. 
Сервис позволяет использовать модели `gpt-4` и `dalle` для генерации текста и изображений. 

## Подробнее

Модуль  используется для получения ответов от API сервиса `Ai-Chats`, 
при этом поддерживает историю сообщений и асинхронные запросы. 
Он реализует интерфейсы `AsyncGeneratorProvider` и `ProviderModelMixin`, 
что позволяет использовать его в рамках общей системы обработки запросов.

## Классы

### `class AiChats`

**Описание**: Класс `AiChats` реализует асинхронный генератор для взаимодействия с API сервиса `Ai-Chats`.

**Наследует**: 
- `AsyncGeneratorProvider`
- `ProviderModelMixin`

**Атрибуты**:

- `url (str)`: Базовый URL сервиса `Ai-Chats`.
- `api_endpoint (str)`: Конечная точка API для отправки запросов.
- `working (bool)`: Флаг, указывающий на доступность сервиса. 
- `supports_message_history (bool)`: Флаг, указывающий на поддержку истории сообщений.
- `default_model (str)`: Модель по умолчанию для использования.
- `models (list[str])`: Список поддерживаемых моделей.

**Методы**:

- `create_async_generator()`: Асинхронный генератор, который отправляет запросы к API `Ai-Chats` и возвращает результаты в виде потока.
- `create_async()`: Асинхронная функция, которая отправляет запрос к API `Ai-Chats` и возвращает первый результат в виде строки.

#### **Методы класса**

##### `create_async_generator()`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        """
        Асинхронный генератор для отправки запросов к API Ai-Chats и получения ответов.

        Args:
            model (str): Имя Используетсяой модели.
            messages (Messages): История сообщений.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию None.
            **kwargs: Дополнительные аргументы для отправки запроса.

        Returns:
            AsyncResult: Асинхронный результат, содержащий ответы API в виде потока.

        Raises:
            Exception: Если возникает ошибка во время отправки запроса или обработки ответа.
        """
        headers = {
            "accept": "application/json, text/event-stream",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "origin": cls.url,
            "pragma": "no-cache",
            "referer": f"{cls.url}/{\'image\' if model == \'dalle\' else \'chat\'}/",
            "sec-ch-ua": '"Chromium";v="127", "Not)A;Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            'cookie': 'muVyak=LSFNvUWqdgKkGprbDBsfieIoEMzjOQ; LSFNvUWqdgKkGprbDBsfieIoEMzjOQ=ac28831b98143847e83dbe004404e619-1725548624-1725548621; muVyak_hits=9; ai-chat-front=9d714d5dc46a6b47607c9a55e7d12a95; _csrf-front=76c23dc0a013e5d1e21baad2e6ba2b5fdab8d3d8a1d1281aa292353f8147b057a%3A2%3A%7Bi%3A0%3Bs%3A11%3A%22_csrf-front%22%3Bi%3A1%3Bs%3A32%3A%22K9lz0ezsNPMNnfpd_8gT5yEeh-55-cch%22%3B%7D',
        }

        async with ClientSession(headers=headers) as session:
            if model == 'dalle':
                prompt = messages[-1]['content'] if messages else ""
            else:
                prompt = format_prompt(messages)

            data = {
                "type": "image" if model == 'dalle' else "chat",
                "messagesHistory": [
                    {
                        "from": "you",
                        "content": prompt
                    }
                ]
            }

            try:
                async with session.post(cls.api_endpoint, json=data, proxy=proxy) as response:
                    response.raise_for_status()

                    if model == 'dalle':
                        response_json = await response.json()

                        if 'data' in response_json and response_json['data']:
                            image_url = response_json['data'][0].get('url')
                            if image_url:
                                async with session.get(image_url) as img_response:
                                    img_response.raise_for_status()
                                    image_data = await img_response.read()

                                base64_image = base64.b64encode(image_data).decode('utf-8')
                                base64_url = f"data:image/png;base64,{base64_image}"
                                yield ImageResponse(base64_url, prompt)
                            else:
                                yield f"Error: No image URL found in the response. Full response: {response_json}"
                        else:
                            yield f"Error: Unexpected response format. Full response: {response_json}"
                    else:
                        full_response = await response.text()
                        message = ""
                        for line in full_response.split('\n'):
                            if line.startswith('data: ') and line != 'data: ':
                                message += line[6:]

                        message = message.strip()
                        yield message
            except Exception as e:
                yield f"Error occurred: {str(e)}"
```

**Описание**: 
- Функция `create_async_generator()` отправляет асинхронный запрос к API `Ai-Chats` с использованием модели и истории сообщений, указанных в аргументах.
-  В зависимости от типа модели (`dalle` или `gpt-4`) формируется соответствующий JSON-запрос.
- В случае использования модели `dalle` функция получает URL изображения из ответа и загружает изображение, 
- после чего возвращает его в виде `ImageResponse`.
- Для модели `gpt-4` функция возвращает текст ответа из ответа API.
- В случае возникновения ошибок возвращается сообщение об ошибке.

##### `create_async()`

```python
    @classmethod
    async def create_async(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> str:
        """
        Асинхронная функция для отправки запросов к API Ai-Chats и получения первого ответа.

        Args:
            model (str): Имя Используетсяой модели.
            messages (Messages): История сообщений.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию None.
            **kwargs: Дополнительные аргументы для отправки запроса.

        Returns:
            str: Первый ответ API в виде строки.

        Raises:
            Exception: Если возникает ошибка во время отправки запроса или обработки ответа.
        """
        async for response in cls.create_async_generator(model, messages, proxy, **kwargs):
            if isinstance(response, ImageResponse):
                return response.images[0]
            return response
```

**Описание**:
-  Функция `create_async()` использует генератор `create_async_generator()` для получения первого ответа API. 
- Если ответ является изображением, то возвращается URL изображения. 
- В противном случае возвращается текстовый ответ.

**Примеры**:

```python
from src.endpoints.gpt4free.g4f.Provider.not_working.AiChats import AiChats
from ...typing import Messages

messages: Messages = [
    {'role': 'user', 'content': 'Привет!'},
    {'role': 'assistant', 'content': 'Привет! 👋 Как дела?'},
    {'role': 'user', 'content': 'Хорошо, спасибо!'},
]

# Получение ответа от модели gpt-4
async for response in AiChats.create_async_generator(model='gpt-4', messages=messages):
    print(response)

# Получение изображения от модели dalle
async for response in AiChats.create_async_generator(model='dalle', messages=messages):
    print(response)

# Получение первого ответа от модели gpt-4
response = await AiChats.create_async(model='gpt-4', messages=messages)
print(response)
# Module src.endpoints.gpt4free.g4f.Provider.Yqcloud
## Обзор

Модуль `Yqcloud` является частью проекта `hypotez` и предоставляет асинхронный генератор для взаимодействия с API `Yqcloud` для получения ответов от модели GPT-4. Этот модуль поддерживает потоковую передачу ответов, системные сообщения и историю сообщений.

## Подробнее

Модуль содержит класс `Yqcloud`, который наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`. Он используется для создания асинхронных запросов к API `Yqcloud`, форматирования запросов и обработки ответов в потоковом режиме. Модуль также включает класс `Conversation` для управления историей разговоров.

## Содержание

- [Классы](#Классы)
    - [Conversation](#Conversation)
    - [Yqcloud](#Yqcloud)
- [Функции](#Функции)
    - [create_async_generator](#create_async_generator)

## Классы

### `Conversation`

```python
class Conversation(JsonConversation):
    """Описание класса для управления историей разговоров с моделью Yqcloud.
    Inherits:
        JsonConversation: Наследуется от JsonConversation и предоставляет методы для работы с историей разговоров в формате JSON.

    Attributes:
        userId (str): Уникальный идентификатор пользователя для отслеживания разговора. По умолчанию `None`.
        message_history (Messages): Список сообщений в истории разговора. По умолчанию пустой список `[]`.

    Methods:
        __init__(model: str): Инициализирует новый экземпляр класса Conversation.
    """

    def __init__(self, model: str):
        """Инициализирует новый экземпляр класса Conversation.

        Args:
            model (str): Имя модели, используемой в разговоре.
        """
        self.model = model
        self.userId = f"#/chat/{int(time.time() * 1000)}"
```

### `Yqcloud`

```python
class Yqcloud(AsyncGeneratorProvider, ProviderModelMixin):
    """Описание класса для взаимодействия с API Yqcloud.
    Inherits:
        AsyncGeneratorProvider: Наследуется от AsyncGeneratorProvider и предоставляет методы для создания асинхронных генераторов.
        ProviderModelMixin: Наследуется от ProviderModelMixin и предоставляет методы для работы с моделями.

    Attributes:
        url (str): Базовый URL для Yqcloud.
        api_endpoint (str): URL для API-endpoint Yqcloud.
        working (bool): Указывает, работает ли провайдер в данный момент.
        supports_stream (bool): Указывает, поддерживает ли провайдер потоковую передачу.
        supports_system_message (bool): Указывает, поддерживает ли провайдер системные сообщения.
        supports_message_history (bool): Указывает, поддерживает ли провайдер историю сообщений.
        default_model (str): Модель, используемая по умолчанию.
        models (List[str]): Список поддерживаемых моделей.

    Methods:
        create_async_generator(model: str, messages: Messages, stream: bool = True, proxy: str = None, conversation: Conversation = None, return_conversation: bool = False, **kwargs) -> AsyncResult: Создает асинхронный генератор для взаимодействия с API Yqcloud.
    """
    url = "https://chat9.yqcloud.top"
    api_endpoint = "https://api.binjie.fun/api/generateStream"
    
    working = True
    supports_stream = True
    supports_system_message = True
    supports_message_history = True
    
    default_model = "gpt-4"
    models = [default_model]
```

## Функции

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        stream: bool = True,
        proxy: str = None,
        conversation: Conversation = None,
        return_conversation: bool = False,
        **kwargs
    ) -> AsyncResult:
        """Создает асинхронный генератор для взаимодействия с API Yqcloud.

        Args:
            model (str): Имя модели, используемой для генерации ответа.
            messages (Messages): Список сообщений для отправки в API.
            stream (bool, optional): Указывает, использовать ли потоковую передачу. По умолчанию `True`.
            proxy (str, optional): URL прокси-сервера для использования. По умолчанию `None`.
            conversation (Conversation, optional): Объект Conversation для хранения истории сообщений. По умолчанию `None`.
            return_conversation (bool, optional): Указывает, возвращать ли объект Conversation после завершения. По умолчанию `False`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий сообщения от API.

        Как работает функция:
        - Функция извлекает модель, создает или обновляет объект Conversation с историей сообщений.
        - Извлекает системное сообщение, если оно есть.
        - Форматирует запрос и отправляет его в API Yqcloud.
        - Получает ответ от API в потоковом режиме и возвращает сообщения через генератор.
        - Обновляет историю сообщений в объекте Conversation, если `return_conversation` установлен в `True`.
        - Завершает генератор сообщением `FinishReason("stop")`.

        Примеры:
            Пример 1: Создание асинхронного генератора с потоковой передачей.
            ```python
            messages = [{"role": "user", "content": "Hello, GPT-4!"}]
            generator = Yqcloud.create_async_generator(model="gpt-4", messages=messages)
            ```

            Пример 2: Создание асинхронного генератора с использованием прокси.
            ```python
            messages = [{"role": "user", "content": "Hello, GPT-4!"}]
            generator = Yqcloud.create_async_generator(model="gpt-4", messages=messages, proxy="http://proxy.example.com")
            ```

            Пример 3: Создание асинхронного генератора с сохранением истории разговора.
            ```python
            messages = [{"role": "user", "content": "Hello, GPT-4!"}]
            conversation = Conversation(model="gpt-4")
            generator = Yqcloud.create_async_generator(model="gpt-4", messages=messages, conversation=conversation, return_conversation=True)
            ```
        """
        model = cls.get_model(model)
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "origin": f"{cls.url}",
            "referer": f"{cls.url}/",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }
        
        if conversation is None:
            conversation = Conversation(model)
            conversation.message_history = messages
        else:
            conversation.message_history.append(messages[-1])

        # Функция извлекает системное сообщение, если оно есть
        system_message = ""
        current_messages = conversation.message_history
        if current_messages and current_messages[0]["role"] == "system":
            system_message = current_messages[0]["content"]
            current_messages = current_messages[1:]
        
        async with ClientSession(headers=headers) as session:
            prompt = format_prompt(current_messages)
            data = {
                "prompt": prompt,
                "userId": conversation.userId,
                "network": True,
                "system": system_message,
                "withoutContext": False,
                "stream": stream
            }
            
            async with session.post(cls.api_endpoint, json=data, proxy=proxy) as response:
                await raise_for_status(response)
                full_message = ""
                async for chunk in response.content:
                    if chunk:
                        message = chunk.decode()
                        yield message
                        full_message += message

                if return_conversation:
                    conversation.message_history.append({"role": "assistant", "content": full_message})
                    yield conversation
                
                yield FinishReason("stop")
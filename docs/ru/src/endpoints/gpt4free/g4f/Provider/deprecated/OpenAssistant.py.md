# Модуль `OpenAssistant`

## Обзор

Модуль `OpenAssistant` представляет собой асинхронный провайдер генерации текста, использующий модель `OA_SFT_Llama_30B_6` Open Assistant. Он обеспечивает взаимодействие с API Open Assistant для создания чатов, отправки сообщений и получения ответов ассистента. Модуль поддерживает использование прокси и cookies для аутентификации.

## Подробнее

Модуль предназначен для интеграции с другими компонентами системы, требующими взаимодействия с Open Assistant. Он предоставляет функциональность для создания асинхронного генератора текста, который можно использовать для получения потоковых ответов от модели Open Assistant.

## Классы

### `OpenAssistant`

**Описание**: Класс `OpenAssistant` является асинхронным провайдером, который взаимодействует с API Open Assistant для генерации текста.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `url` (str): URL для взаимодействия с Open Assistant (`"https://open-assistant.io/chat"`).
- `needs_auth` (bool): Указывает, требуется ли аутентификация (`True`).
- `working` (bool): Указывает, работает ли провайдер (`False`).
- `model` (str): Имя используемой модели (`"OA_SFT_Llama_30B_6"`).

## Методы класса

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        cookies: dict = None,
        **kwargs
    ) -> AsyncResult:
        """Создает асинхронный генератор для взаимодействия с Open Assistant.

        Args:
            model (str): Имя модели для использования.
            messages (Messages): Список сообщений для отправки.
            proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
            cookies (dict, optional): Cookies для аутентификации. По умолчанию `None`.
            **kwargs: Дополнительные параметры для передачи в API.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий текст ответа.

        Raises:
            RuntimeError: Если в ответе от API содержится сообщение об ошибке.
            aiohttp.ClientResponseError: Если возникает HTTP ошибка.

        
            1. Проверяет наличие cookies, если их нет, пытается получить их для домена "open-assistant.io".
            2. Создает сессию `aiohttp.ClientSession` с заданными cookies и заголовками.
            3. Отправляет POST-запрос на `"https://open-assistant.io/api/chat"` для создания нового чата и получает `chat_id`.
            4. Форматирует входные сообщения с использованием функции `format_prompt(messages)` и отправляет их как сообщение пользователя (prompter) в чат.
            5. Получает `parent_id` сообщения пользователя.
            6. Отправляет POST-запрос на `"https://open-assistant.io/api/chat/assistant_message"` с данными, включающими `chat_id`, `parent_id`, имя модели и параметры sampling.
            7. Получает `message_id` сообщения ассистента или выбрасывает исключение, если в ответе содержится сообщение об ошибке.
            8. Отправляет POST-запрос на `"https://open-assistant.io/api/chat/events"` для получения потоковых ответов от ассистента.
            9. Читает ответ построчно, декодирует его и извлекает текст токенов, которые передает через `yield`.
           10. После завершения получения ответов, отправляет DELETE-запрос на `"https://open-assistant.io/api/chat"` для удаления чата.

        Примеры:
            >>> async for message in OpenAssistant.create_async_generator(model="OA_SFT_Llama_30B_6", messages=[{"role": "user", "content": "Hello, how are you?"}]):
            ...     print(message, end="")
            # (Вывод будет содержать ответ от Open Assistant)

            >>> async for message in OpenAssistant.create_async_generator(model="OA_SFT_Llama_30B_6", messages=[{"role": "user", "content": "Translate to German: Hello, how are you?"}], proxy="http://your_proxy:8080"):
            ...     print(message, end="")
            # (Вывод будет содержать перевод фразы на немецкий язык)
        """
```

## Параметры класса

- `url` (str): URL для взаимодействия с Open Assistant.
- `needs_auth` (bool): Указывает, требуется ли аутентификация.
- `working` (bool): Указывает, работает ли провайдер.
- `model` (str): Имя используемой модели.

## Примеры
Примеры работы с классом `OpenAssistant` можно посмотреть в документации к методу `create_async_generator`.
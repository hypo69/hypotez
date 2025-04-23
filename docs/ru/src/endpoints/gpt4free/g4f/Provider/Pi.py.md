# Модуль `Pi`

## Обзор

Модуль `Pi` предоставляет асинхронный генератор для взаимодействия с AI-моделью Pi.ai через API. Он включает в себя функции для начала разговора, получения истории чата и отправки запросов. Модуль поддерживает потоковую передачу ответов и использует `StreamSession` для выполнения асинхронных HTTP-запросов.

## Подробней

Этот модуль предназначен для интеграции с Pi.ai, предоставляя удобный интерфейс для асинхронного взаимодействия с моделью Pi. Он автоматически управляет cookies и заголовками, необходимыми для аутентификации и поддержания сессии.

## Классы

### `Pi(AsyncGeneratorProvider)`

**Описание**: Класс `Pi` является асинхронным провайдером генераторов, который реализует взаимодействие с AI-моделью Pi.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `url` (str): URL для взаимодействия с Pi.ai ("https://pi.ai/talk").
- `working` (bool): Указывает, работает ли провайдер (True).
- `use_nodriver` (bool): Указывает, используется ли бездрайверный режим (True).
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу (True).
- `default_model` (str): Модель по умолчанию ("pi").
- `models` (list[str]): Список поддерживаемых моделей (["pi"]).
- `_headers` (dict | None): Заголовки HTTP-запроса.
- `_cookies` (Cookies): Cookies для сессии.

**Методы**:
- `create_async_generator()`: Создает асинхронный генератор для получения ответов от модели Pi.
- `start_conversation()`: Начинает новый разговор и возвращает идентификатор разговора.
- `get_chat_history()`: Получает историю чата по идентификатору разговора.
- `ask()`: Отправляет запрос к модели Pi и возвращает асинхронный генератор ответов.

## Методы класса

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        stream: bool,
        proxy: str = None,
        timeout: int = 180,
        conversation_id: str = None,
        **kwargs
    ) -> AsyncResult:
        """ Создает асинхронный генератор для получения ответов от модели Pi.

        Args:
            model (str): Название модели.
            messages (Messages): Список сообщений для отправки.
            stream (bool): Флаг, указывающий, использовать ли потоковую передачу.
            proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
            timeout (int, optional): Время ожидания запроса в секундах. По умолчанию 180.
            conversation_id (str, optional): Идентификатор существующего разговора. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, выдающий ответы от модели Pi.

        Raises:
            Exception: Если возникает ошибка при выполнении запроса.

        Как работает функция:
        - Проверяет, инициализированы ли заголовки (`cls._headers`). Если нет, получает их с помощью `get_args_from_nodriver`.
        - Создает `StreamSession` с использованием полученных заголовков и cookies.
        - Если `conversation_id` не указан, начинает новый разговор с помощью `start_conversation`.
        - Форматирует сообщения с помощью `format_prompt`.
        - Вызывает `ask` для отправки запроса и получения ответа.
        - Итерирует по ответам, извлекая текст из каждой строки и возвращая его через генератор.
        """
```

### `start_conversation`

```python
    @classmethod
    async def start_conversation(cls, session: StreamSession) -> str:
        """ Начинает новый разговор и возвращает идентификатор разговора.

        Args:
            session (StreamSession): Асинхронная HTTP-сессия.

        Returns:
            str: Идентификатор нового разговора.

        Raises:
            Exception: Если возникает ошибка при выполнении запроса.

         Как работает функция:
        - Выполняет POST-запрос к API Pi.ai для начала нового разговора.
        - Извлекает идентификатор разговора (`sid`) из JSON-ответа.
        - Возвращает идентификатор разговора.
        """
```

### `get_chat_history`

```python
    async def get_chat_history(session: StreamSession, conversation_id: str):
        """ Получает историю чата по идентификатору разговора.

        Args:
            session (StreamSession): Асинхронная HTTP-сессия.
            conversation_id (str): Идентификатор разговора.

        Returns:
            dict: JSON-ответ, содержащий историю чата.

        Raises:
            Exception: Если возникает ошибка при выполнении запроса.

         Как работает функция:
        - Определяет параметры запроса, включая идентификатор разговора.
        - Выполняет GET-запрос к API Pi.ai для получения истории чата.
        - Возвращает JSON-ответ, содержащий историю чата.
        """
```

### `ask`

```python
    @classmethod
    async def ask(cls, session: StreamSession, prompt: str, conversation_id: str):
        """ Отправляет запрос к модели Pi и возвращает асинхронный генератор ответов.

        Args:
            session (StreamSession): Асинхронная HTTP-сессия.
            prompt (str): Текст запроса.
            conversation_id (str): Идентификатор разговора.

        Yields:
            str: Части ответа от модели Pi.

        Raises:
            Exception: Если возникает ошибка при выполнении запроса.

        Как работает функция:
        - Формирует JSON-данные для отправки запроса, включая текст запроса и идентификатор разговора.
        - Выполняет POST-запрос к API Pi.ai для отправки запроса.
        - Обновляет cookies сессии.
        - Итерирует по строкам ответа, извлекая текст из строк, начинающихся с "data: {\"text\":" или "data: {\"title\":", и возвращая его через генератор.
        """
```

## Примеры

Пример использования класса `Pi` для получения ответа от модели:

```python
from src.endpoints.gpt4free.g4f.Provider import Pi
from src.requests import StreamSession

import asyncio

async def main():
    # Пример использования методов класса Pi
    session = StreamSession()
    conversation_id = await Pi.start_conversation(session)
    prompt = "Привет, как дела?"
    async for line in Pi.ask(session, prompt, conversation_id):
        print(line)

if __name__ == "__main__":
    asyncio.run(main())
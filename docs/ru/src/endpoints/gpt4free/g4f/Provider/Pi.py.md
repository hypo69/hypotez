# Модуль для работы с Pi.ai
==========================

Модуль :file:`Pi.py` предоставляет асинхронный интерфейс для взаимодействия с AI-моделью Pi.ai. Он позволяет начинать разговор, отправлять запросы и получать ответы в режиме реального времени.

## Обзор

Модуль предназначен для интеграции с gpt4free, обеспечивая возможность использования Pi.ai в качестве одного из доступных провайдеров. Он использует асинхронные запросы для обеспечения неблокирующего взаимодействия с API Pi.ai. Модуль поддерживает потоковую передачу ответов, что позволяет получать ответы по частям в режиме реального времени.

## Подробнее

Модуль `Pi` является асинхронным провайдером, который использует `StreamSession` для отправки запросов к API Pi.ai. Он автоматически получает необходимые заголовки и cookies, а также поддерживает проксирование запросов. Модуль предоставляет методы для начала разговора, получения истории чата и отправки запросов.

## Классы

### `Pi(AsyncGeneratorProvider)`

**Описание**: Класс `Pi` предоставляет асинхронный интерфейс для взаимодействия с AI-моделью Pi.ai.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую функциональность для асинхронных провайдеров, генерирующих данные.

**Атрибуты**:
- `url` (str): URL для взаимодействия с Pi.ai (`https://pi.ai/talk`).
- `working` (bool): Указывает, работает ли провайдер (всегда `True`).
- `use_nodriver` (bool): Указывает, использует ли провайдер "nodriver" (всегда `True`).
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных (всегда `True`).
- `default_model` (str): Модель, используемая по умолчанию (`pi`).
- `models` (List[str]): Список поддерживаемых моделей (только `["pi"]`).
- `_headers` (dict): Заголовки HTTP-запросов, используемые для взаимодействия с API Pi.ai.
- `_cookies` (Cookies): Cookies, используемые для аутентификации и поддержания сессии с Pi.ai.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для взаимодействия с API Pi.ai.
- `start_conversation`: Начинает новый разговор с Pi.ai и возвращает идентификатор разговора.
- `get_chat_history`: Получает историю чата по идентификатору разговора.
- `ask`: Отправляет запрос к Pi.ai и возвращает асинхронный генератор ответов.

## Функции

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
        """Создает асинхронный генератор для взаимодействия с API Pi.ai.

        Args:
            model (str): Модель для использования (всегда "pi").
            messages (Messages): Список сообщений для отправки в запросе.
            stream (bool): Указывает, использовать ли потоковую передачу данных.
            proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
            timeout (int, optional): Время ожидания запроса в секундах. По умолчанию `180`.
            conversation_id (str, optional): Идентификатор существующего разговора. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий ответы от API Pi.ai.
        
        Как работает функция:
        1. Проверяет, инициализированы ли заголовки HTTP-запросов (`cls._headers`). Если нет, выполняет их инициализацию с использованием `get_args_from_nodriver`.
        2. Создает асинхронную сессию `StreamSession` с использованием полученных заголовков и cookies.
        3. Если `conversation_id` не предоставлен, начинает новый разговор с использованием `start_conversation` и получает `conversation_id`.
        4. Форматирует запрос с использованием `format_prompt` или берет последнее сообщение из списка `messages`, если `conversation_id` уже существует.
        5. Вызывает функцию `ask` для отправки запроса и получения ответа в виде асинхронного генератора.
        6. Итерируется по ответам, возвращаемым генератором `ask`, и извлекает текстовые данные из каждого ответа.
        7. Возвращает текстовые данные, полученные из ответов, как результат работы генератора.

        Блок-схема работы функции:

        Инициализация заголовков? --> Создание сессии --> Новый разговор? --> Форматирование запроса --> Отправка запроса --> Извлечение текста

        Примеры:
            Пример 1: Запуск нового разговора и получение ответа.
            ```python
            messages = [{"role": "user", "content": "Hello, Pi!"}]
            async for response in Pi.create_async_generator(model="pi", messages=messages, stream=True):
                print(response)
            ```

            Пример 2: Продолжение существующего разговора.
            ```python
            messages = [{"role": "user", "content": "Tell me more."}]
            async for response in Pi.create_async_generator(model="pi", messages=messages, stream=True, conversation_id="existing_conversation_id"):
                print(response)
            ```
        """
        if cls._headers is None:
            args = await get_args_from_nodriver(cls.url, proxy=proxy, timeout=timeout)
            cls._cookies = args.get("cookies", {})
            cls._headers = args.get("headers")
        async with StreamSession(headers=cls._headers, cookies=cls._cookies, proxy=proxy) as session:
            if not conversation_id:
                conversation_id = await cls.start_conversation(session)
                prompt = format_prompt(messages)
            else:
                prompt = messages[-1]["content"]
            answer = cls.ask(session, prompt, conversation_id)
            async for line in answer:
                if "text" in line:
                    yield line["text"]
```

### `start_conversation`

```python
    @classmethod
    async def start_conversation(cls, session: StreamSession) -> str:
        """Начинает новый разговор с Pi.ai.

        Args:
            session (StreamSession): Асинхронная сессия для отправки запросов.

        Returns:
            str: Идентификатор нового разговора.

        Как работает функция:
        1. Отправляет POST-запрос к API Pi.ai для начала нового разговора.
        2. Извлекает идентификатор разговора из JSON-ответа.

        Блок-схема работы функции:

        Отправка POST-запроса --> Извлечение идентификатора разговора

        Примеры:
            Пример: Запуск нового разговора и получение идентификатора.
            ```python
            async with StreamSession() as session:
                conversation_id = await Pi.start_conversation(session)
                print(conversation_id)
            ```
        """
        async with session.post('https://pi.ai/api/chat/start', data="{}", headers={
            'accept': 'application/json',
            'x-api-version': '3'
        }) as response:
            await raise_for_status(response)
            return (await response.json())['conversations'][0]['sid']
```

### `get_chat_history`

```python
    async def get_chat_history(session: StreamSession, conversation_id: str):
        """Получает историю чата по идентификатору разговора.

        Args:
            session (StreamSession): Асинхронная сессия для отправки запросов.
            conversation_id (str): Идентификатор разговора.

        Returns:
            Awaitable[Any]:  JSON-ответ с историей чата.

        Как работает функция:

        1. Подготавливает параметры запроса, включая идентификатор разговора.
        2. Отправляет GET-запрос к API Pi.ai для получения истории чата.
        3. Возвращает JSON-ответ с историей чата.

        Блок-схема работы функции:

        Подготовка параметров запроса --> Отправка GET-запроса --> Возврат JSON-ответа

        Примеры:
            Пример: Получение истории чата.
            ```python
            async with StreamSession() as session:
                chat_history = await Pi.get_chat_history(session, "conversation_id")
                print(chat_history)
            ```
        """
        params = {
            'conversation': conversation_id,
        }
        async with session.get('https://pi.ai/api/chat/history', params=params) as response:
            await raise_for_status(response)
            return await response.json()
```

### `ask`

```python
    @classmethod
    async def ask(cls, session: StreamSession, prompt: str, conversation_id: str):
        """Отправляет запрос к Pi.ai и возвращает асинхронный генератор ответов.

        Args:
            session (StreamSession): Асинхронная сессия для отправки запросов.
            prompt (str): Текст запроса.
            conversation_id (str): Идентификатор разговора.

        Yields:
            Awaitable[Any]: Части ответа от API Pi.ai.

        Как работает функция:

        1. Подготавливает JSON-данные для отправки запроса, включая текст запроса, идентификатор разговора и режим.
        2. Отправляет POST-запрос к API Pi.ai с JSON-данными.
        3. Обновляет cookies сессии.
        4. Итерируется по строкам ответа и извлекает JSON-данные из строк, начинающихся с `data: {"text":` или `data: {"title":`.
        5. Возвращает извлеченные JSON-данные.

        Блок-схема работы функции:

        Подготовка JSON-данных --> Отправка POST-запроса --> Обновление cookies --> Извлечение JSON-данных из ответа

        Примеры:
            Пример: Отправка запроса и получение ответа.
            ```python
            async with StreamSession() as session:
                async for line in Pi.ask(session, "Hello, Pi!", "conversation_id"):
                    print(line)
            ```
        """
        json_data = {
            'text': prompt,
            'conversation': conversation_id,
            'mode': 'BASE',
        }
        async with session.post('https://pi.ai/api/chat', json=json_data) as response:
            await raise_for_status(response)
            cls._cookies = merge_cookies(cls._cookies, response)
            async for line in response.iter_lines():
                if line.startswith(b'data: {"text":'):
                    yield json.loads(line.split(b'data: ')[1])
                elif line.startswith(b'data: {"title":'):
                    yield json.loads(line.split(b'data: ')[1])
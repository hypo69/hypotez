# Модуль `Pi`

## Обзор

Модуль `Pi` предоставляет асинхронный интерфейс для взаимодействия с чат-ботом Pi.ai. Он позволяет начать разговор, отправлять сообщения и получать ответы в потоковом режиме. Модуль использует `StreamSession` для асинхронных HTTP-запросов и поддерживает работу через прокси.

## Подробней

Модуль `Pi` предназначен для интеграции с gpt4free, чтобы обеспечить доступ к модели Pi.ai. Он обрабатывает установку соединения, отправку запросов и получение ответов, разбивая их на части для потоковой передачи.

## Классы

### `Pi`

**Описание**:
Класс `Pi` является асинхронным провайдером, который обеспечивает взаимодействие с API Pi.ai.

**Наследует**:
`AsyncGeneratorProvider` - базовый класс для асинхронных провайдеров, поддерживающих генерацию потока данных.

**Атрибуты**:
- `url` (str): URL для взаимодействия с Pi.ai ("https://pi.ai/talk").
- `working` (bool): Указывает, что провайдер в рабочем состоянии (True).
- `use_nodriver` (bool): Указывает, что не требуется использование веб-драйвера (True).
- `supports_stream` (bool): Указывает, что провайдер поддерживает потоковую передачу данных (True).
- `default_model` (str): Модель по умолчанию ("pi").
- `models` (list): Список поддерживаемых моделей (["pi"]).
- `_headers` (dict): Заголовки HTTP-запроса.
- `_cookies` (Cookies): Куки для сессии.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от Pi.ai.
- `start_conversation`: Начинает новый разговор с Pi.ai и возвращает идентификатор разговора.
- `get_chat_history`: Получает историю чата по идентификатору разговора.
- `ask`: Отправляет запрос к Pi.ai и возвращает асинхронный генератор с ответами.

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
        """Создает асинхронный генератор для получения ответов от Pi.ai.

        Args:
            model (str): Имя используемой модели.
            messages (Messages): Список сообщений для отправки.
            stream (bool): Флаг, указывающий, использовать ли потоковый режим.
            proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
            timeout (int, optional): Время ожидания запроса. По умолчанию 180.
            conversation_id (str, optional): Идентификатор существующего разговора. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, выдающий ответы от Pi.ai.

        Как работает функция:
        1. Проверяет, инициализированы ли заголовки (_headers). Если нет, получает их с помощью `get_args_from_nodriver`.
        2. Открывает асинхронную сессию `StreamSession` с заданными заголовками, куками и прокси.
        3. Если `conversation_id` не указан, начинает новый разговор с помощью `start_conversation` и форматирует промпт.
        4. Если `conversation_id` указан, использует его и берет последнее сообщение из `messages` в качестве промпта.
        5. Вызывает метод `ask` для отправки запроса и получения ответа.
        6. Итерируется по ответам, возвращаемым генератором `ask`, и извлекает текст из каждой строки.

        ASCII flowchart:
        A: Проверка инициализации _headers
        |
        B: Получение _headers и _cookies (если A == False)
        |
        C: Открытие StreamSession
        |
        D: Проверка conversation_id
        |
        E: start_conversation (если D == False)
        |
        F: format_prompt (если D == False)
        |
        G: Извлечение последнего сообщения (если D == True)
        |
        H: Вызов ask
        |
        I: Итерация по ответам из ask
        |
        J: Извлечение текста из ответа и yield

        A -> B (если _headers is None)
        A -> C (если _headers is not None)
        B -> C
        C -> D
        D -> E (если conversation_id is None)
        D -> G (если conversation_id is not None)
        E -> F
        F -> H
        G -> H
        H -> I
        I -> J

        Raises:
            Exception: Возникает, если при запросе к API Pi.ai происходит ошибка.
        """
```

Примеры:
```python
# Пример использования create_async_generator
model = "pi"
messages = [{"role": "user", "content": "Hello, Pi!"}]
stream = True
# result = await Pi.create_async_generator(model=model, messages=messages, stream=stream)
# async for message in result:
#     print(message)
```

### `start_conversation`

```python
    @classmethod
    async def start_conversation(cls, session: StreamSession) -> str:
        """Начинает новый разговор с Pi.ai и возвращает идентификатор разговора.

        Args:
            session (StreamSession): Асинхронная сессия для выполнения запросов.

        Returns:
            str: Идентификатор нового разговора.

        Как работает функция:
        1. Отправляет POST-запрос к API Pi.ai для начала нового разговора.
        2. Извлекает идентификатор разговора из JSON-ответа.

        ASCII flowchart:
        A: Отправка POST-запроса к API
        |
        B: Извлечение conversation_id из JSON-ответа

        A -> B

        Raises:
            Exception: Возникает, если при запросе к API Pi.ai происходит ошибка.
        """
```

Примеры:
```python
# Пример использования start_conversation
# async with StreamSession() as session:
#     conversation_id = await Pi.start_conversation(session)
#     print(conversation_id)
```

### `get_chat_history`

```python
    async def get_chat_history(session: StreamSession, conversation_id: str):
        """Получает историю чата по идентификатору разговора.

        Args:
            session (StreamSession): Асинхронная сессия для выполнения запросов.
            conversation_id (str): Идентификатор разговора.

        Returns:
            json: JSON-ответ с историей чата.

        Как работает функция:
        1. Определяет параметры запроса, включая `conversation_id`.
        2. Отправляет GET-запрос к API Pi.ai для получения истории чата.
        3. Возвращает JSON-ответ с историей чата.

        ASCII flowchart:
        A: Отправка GET-запроса к API
        |
        B: Возврат JSON-ответа

        A -> B

        Raises:
            Exception: Возникает, если при запросе к API Pi.ai происходит ошибка.
        """
```

Примеры:
```python
# Пример использования get_chat_history
# async with StreamSession() as session:
#     history = await Pi.get_chat_history(session, "some_conversation_id")
#     print(history)
```

### `ask`

```python
    @classmethod
    async def ask(cls, session: StreamSession, prompt: str, conversation_id: str):
        """Отправляет запрос к Pi.ai и возвращает асинхронный генератор с ответами.

        Args:
            session (StreamSession): Асинхронная сессия для выполнения запросов.
            prompt (str): Текст запроса.
            conversation_id (str): Идентификатор разговора.

        Yields:
            str: Части ответа от Pi.ai.

        Как работает функция:
        1. Формирует JSON-данные для запроса, включая текст запроса и `conversation_id`.
        2. Отправляет POST-запрос к API Pi.ai.
        3. Итерируется по строкам ответа и извлекает текст из строк, начинающихся с `data: {"text":` или `data: {"title":`.

        ASCII flowchart:
        A: Формирование JSON-данных
        |
        B: Отправка POST-запроса к API
        |
        C: Итерация по строкам ответа
        |
        D: Проверка начала строки (data: {"text": или data: {"title":)
        |
        E: Извлечение и yield текста (если D == True)

        A -> B
        B -> C
        C -> D
        D -> E (если строка начинается с 'data: {"text":' или 'data: {"title":')

        Raises:
            Exception: Возникает, если при запросе к API Pi.ai происходит ошибка.
        """
```

Примеры:
```python
# Пример использования ask
# async with StreamSession() as session:
#     async for message in Pi.ask(session, "Tell me a story", "some_conversation_id"):
#         print(message)
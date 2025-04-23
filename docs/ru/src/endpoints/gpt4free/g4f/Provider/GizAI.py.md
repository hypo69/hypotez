# Модуль `GizAI`

## Обзор

Модуль `GizAI` предоставляет асинхронный генератор для взаимодействия с API GizAI. Он позволяет отправлять запросы к API для получения ответов от AI-моделей, таких как `chat-gemini-flash`. Модуль поддерживает отправку системных сообщений и сохранение истории сообщений.

## Подробнее

Модуль использует библиотеку `aiohttp` для выполнения асинхронных HTTP-запросов. Он форматирует сообщения в соответствии с требованиями API GizAI и обрабатывает ответы, возвращая сгенерированный текст.

## Классы

### `GizAI`

**Описание**: Класс `GizAI` является асинхронным провайдером генератора, предназначенным для взаимодействия с API GizAI. Он наследует функциональность от `AsyncGeneratorProvider` и `ProviderModelMixin`.

**Наследует**:
- `AsyncGeneratorProvider`: Предоставляет базовый интерфейс для асинхронных провайдеров генераторов.
- `ProviderModelMixin`: Добавляет функциональность для управления моделями и их псевдонимами.

**Атрибуты**:
- `url` (str): URL главной страницы GizAI.
- `api_endpoint` (str): URL API для отправки запросов на получение выводов.
- `working` (bool): Указывает, работает ли провайдер в данный момент.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер отправку системных сообщений.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер сохранение истории сообщений.
- `default_model` (str): Модель, используемая по умолчанию (`chat-gemini-flash`).
- `models` (list): Список поддерживаемых моделей.
- `model_aliases` (dict): Словарь псевдонимов моделей.

**Методы**:
- `get_model(model: str) -> str`: Возвращает имя модели на основе псевдонима или имени, если модель поддерживается.
- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: Создает асинхронный генератор для получения ответов от API GizAI.

## Методы класса

### `get_model`

```python
    @classmethod
    def get_model(cls, model: str) -> str:
        """
        Функция определяет и возвращает имя модели для использования в API GizAI.

        Args:
            model (str): Имя или псевдоним модели.

        Returns:
            str: Имя модели, если она поддерживается, иначе имя модели по умолчанию.
        """
        if model in cls.models:
            return model
        elif model in cls.model_aliases:
            return cls.model_aliases[model]
        else:
            return cls.default_model
```

**Назначение**:
Определяет и возвращает имя модели для использования в API GizAI. Если указанная модель есть в списке поддерживаемых моделей, она и возвращается. Если модель является псевдонимом, возвращается соответствующее ей имя. В противном случае возвращается имя модели по умолчанию.

**Параметры**:
- `model` (str): Имя или псевдоним модели.

**Возвращает**:
- `str`: Имя модели, если она поддерживается, иначе имя модели по умолчанию.

**Примеры**:

```python
GizAI.get_model('chat-gemini-flash')  # Возвращает 'chat-gemini-flash'
GizAI.get_model('gemini-1.5-flash')   # Возвращает 'chat-gemini-flash'
GizAI.get_model('unknown_model')      # Возвращает 'chat-gemini-flash'
```

### `create_async_generator`

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
        Создает асинхронный генератор для получения ответов от API GizAI.

        Args:
            model (str): Имя модели для использования.
            messages (Messages): Список сообщений для отправки в API.
            proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
            **kwargs: Дополнительные параметры.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий ответы от API.

        Raises:
            Exception: Если статус ответа от API не равен 201.
        """
        model = cls.get_model(model)
        
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'DNT': '1',
            'Origin': 'https://app.giz.ai',
            'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not?A_Brand";v="99", "Chromium";v="130"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"'
        }
        
        async with ClientSession(headers=headers) as session:
            data = {
                "model": model,
                "input": {
                    "messages": [
                        {"content": message.get("content")}
                        if message.get("role") == "system" else
                        {"type": "human" if message.get("role") == "user" else "ai", "content": message.get("content")}
                        for message in messages
                    ],
                    "mode": "plan"
                },
                "noStream": True
            }
            async with session.post(cls.api_endpoint, json=data, proxy=proxy) as response:
                if response.status == 201:
                    result = await response.json()
                    yield result['output'].strip()
                else:
                    raise Exception(f"Unexpected response status: {response.status}\n{await response.text()}")
```

**Назначение**:
Создает асинхронный генератор для получения ответов от API GizAI. Формирует заголовки и данные запроса, отправляет POST-запрос к API и обрабатывает ответ. Возвращает текст ответа от API.

**Параметры**:
- `model` (str): Имя модели для использования.
- `messages` (Messages): Список сообщений для отправки в API.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий ответы от API.

**Вызывает исключения**:
- `Exception`: Если статус ответа от API не равен 201.

**Как работает функция**:
1. **Определение модели**: Функция `get_model` вызывается для получения имени модели на основе входного параметра `model`.
2. **Формирование заголовков**: Создается словарь `headers` с необходимыми HTTP-заголовками для запроса.
3. **Создание сессии**: Асинхронно создается сессия `ClientSession` с заданными заголовками.
4. **Формирование данных запроса**: Создается словарь `data` с информацией о модели и сообщениях. Сообщения форматируются в соответствии с API GizAI.
5. **Отправка запроса**: Отправляется POST-запрос к API GizAI с использованием `session.post`.
6. **Обработка ответа**:
   - Если статус ответа равен 201, извлекается текст ответа из JSON-формата и возвращается с помощью `yield`.
   - Если статус ответа не равен 201, выбрасывается исключение `Exception` с информацией об ошибке.

**Примеры**:

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
]
async for response in GizAI.create_async_generator(model='chat-gemini-flash', messages=messages):
    print(response)  # Выводит: Paris
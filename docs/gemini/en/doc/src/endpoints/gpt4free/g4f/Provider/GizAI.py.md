# Module GizAI

## Обзор

Модуль `GizAI` предоставляет асинхронный генератор для взаимодействия с API GizAI. Он поддерживает потоковую передачу сообщений и использование системных сообщений.

## Более подробно

Модуль предназначен для интеграции с сервисом GizAI для получения ответов от AI-моделей. Он использует `aiohttp` для выполнения асинхронных запросов к API GizAI. Модуль поддерживает выбор модели и форматирование запросов в соответствии с требованиями API GizAI.

## Классы

### `GizAI`

**Описание**: Класс `GizAI` является асинхронным генератором провайдером и миксином для работы с моделями.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию ответов.
- `ProviderModelMixin`: Предоставляет методы для работы с моделями.

**Атрибуты**:
- `url` (str): URL сервиса GizAI.
- `api_endpoint` (str): URL API для запросов к GizAI.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_stream` (bool): Поддерживает ли провайдер потоковую передачу.
- `supports_system_message` (bool): Поддерживает ли провайдер системные сообщения.
- `supports_message_history` (bool): Поддерживает ли провайдер историю сообщений.
- `default_model` (str): Модель по умолчанию.
- `models` (list[str]): Список поддерживаемых моделей.
- `model_aliases` (dict[str, str]): Псевдонимы моделей.

**Принцип работы**:
Класс использует асинхронные запросы для взаимодействия с API GizAI, отправляя сообщения и получая ответы в формате генератора. Он также предоставляет методы для выбора и получения моделей.

**Методы**:
- `get_model`: Возвращает модель на основе предоставленного имени или псевдонима.
- `create_async_generator`: Создает асинхронный генератор для получения ответов от API GizAI.

## Методы класса

### `get_model`

```python
@classmethod
def get_model(cls, model: str) -> str:
    """
    Функция получает имя модели на основе предоставленного имени или псевдонима.
    
    Args:
        model (str): Имя модели или псевдоним.

    Returns:
        str: Имя модели.
    """
    # Функция проверяет, есть ли модель в списке поддерживаемых моделей.
    if model in cls.models:
        # Если модель есть в списке, функция возвращает имя модели.
        return model
    # Если модель не найдена в основном списке, функция проверяет, есть ли псевдоним для этой модели.
    elif model in cls.model_aliases:
        # Если псевдоним найден, функция возвращает соответствующее имя модели из словаря псевдонимов.
        return cls.model_aliases[model]
    # Если модель не найдена и псевдоним отсутствует, функция возвращает имя модели по умолчанию.
    else:
        return cls.default_model
```

**Назначение**: Получение имени модели на основе предоставленного имени или псевдонима.

**Параметры**:
- `model` (str): Имя модели или псевдоним.

**Возвращает**:
- `str`: Имя модели.

**Примеры**:
```python
model = GizAI.get_model('chat-gemini-flash')
print(model)  # chat-gemini-flash

model = GizAI.get_model('gemini-1.5-flash')
print(model)  # chat-gemini-flash

model = GizAI.get_model('unknown_model')
print(model)  # chat-gemini-flash
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
    Функция создает асинхронный генератор для получения ответов от API GizAI.

    Args:
        model (str): Имя модели.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий ответы от API.
    """
    # Функция получает имя модели, используя метод `get_model`.
    model = cls.get_model(model)

    # Функция определяет заголовки для HTTP-запроса.
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

    # Функция создает асинхронную сессию с использованием `ClientSession` из библиотеки `aiohttp`.
    async with ClientSession(headers=headers) as session:
        # Функция формирует данные для отправки в теле запроса.
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

        # Функция выполняет POST-запрос к API GizAI.
        async with session.post(cls.api_endpoint, json=data, proxy=proxy) as response:
            # Функция обрабатывает ответ от API.
            if response.status == 201:
                # Если статус ответа 201, функция извлекает результат из JSON-ответа.
                result = await response.json()
                # Функция извлекает текст ответа из поля 'output' и удаляет лишние пробелы.
                yield result['output'].strip()
            else:
                # Если статус ответа не 201, функция вызывает исключение с информацией об ошибке.
                raise Exception(f"Unexpected response status: {response.status}\n{await response.text()}")
```

**Назначение**: Создание асинхронного генератора для получения ответов от API GizAI.

**Параметры**:
- `model` (str): Имя модели.
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, выдающий ответы от API.

**Примеры**:
```python
messages = [
    {"role": "user", "content": "Привет!"},
    {"role": "system", "content": "Ты ассистент."}
]

async def get_response():
    async for response in GizAI.create_async_generator(model='chat-gemini-flash', messages=messages):
        print(response)

# Запуск асинхронной функции (требуется асинхронная среда)
# asyncio.run(get_response())
```
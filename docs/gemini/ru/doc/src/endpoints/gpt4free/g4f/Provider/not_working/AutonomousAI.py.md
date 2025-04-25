# Модуль AutonomousAI

## Обзор

Модуль `AutonomousAI` предоставляет класс `AutonomousAI`, который реализует асинхронный генератор ответов для различных моделей искусственного интеллекта, доступных на платформе Autonomous.ai.  Он включает в себя поддержку различных моделей, таких как `llama`, `qwen_coder`, `hermes`, `vision` и `summary`, а также обеспечивает возможность отправки сообщений в виде асинхронного генератора, что позволяет получать ответы в режиме реального времени. 

## Подробнее

Модуль `AutonomousAI` взаимодействует с API платформы Autonomous.ai для получения ответов от различных моделей ИИ. Он использует `aiohttp` для выполнения асинхронных запросов к API, `base64` для кодирования данных и `json` для обработки данных JSON.  

`AutonomousAI` предоставляет следующие возможности:

- **Выбор моделей:**  `AutonomousAI` позволяет выбирать различные модели ИИ, доступные на платформе Autonomous.ai, такие как `llama`, `qwen_coder`, `hermes`, `vision` и `summary`. 
- **Асинхронная генерация:** `AutonomousAI` реализует асинхронный генератор, который позволяет получать ответы от модели в режиме реального времени.
- **Поддержка потоковой передачи:**  `AutonomousAI` поддерживает потоковую передачу данных (streaming), что позволяет получать ответы от модели по частям.
- **Поддержка системных сообщений:**  `AutonomousAI` поддерживает отправку системных сообщений, которые могут влиять на поведение модели.
- **Поддержка истории сообщений:** `AutonomousAI` поддерживает использование истории сообщений, что позволяет модели иметь контекст для более точных ответов.

## Классы

### `class AutonomousAI`

**Описание**: Класс `AutonomousAI` реализует асинхронный генератор для получения ответов от различных моделей ИИ, доступных на платформе Autonomous.ai. 

**Наследует**: 
- `AsyncGeneratorProvider`:  Предоставляет базовые функции для асинхронной генерации ответов.
- `ProviderModelMixin`:  Предоставляет дополнительные функции для работы с моделями.

**Атрибуты**:

- `url (str)`: Базовый URL для API Autonomous.ai.
- `api_endpoints (dict)`: Словарь, содержащий URL-адреса для различных моделей.
- `working (bool)`:  Флаг, указывающий, работает ли провайдер (по умолчанию `False`).
- `supports_stream (bool)`:  Флаг, указывающий, поддерживает ли провайдер потоковую передачу данных (streaming) (по умолчанию `True`).
- `supports_system_message (bool)`:  Флаг, указывающий, поддерживает ли провайдер отправку системных сообщений (по умолчанию `True`).
- `supports_message_history (bool)`:  Флаг, указывающий, поддерживает ли провайдер использование истории сообщений (по умолчанию `True`).
- `default_model (str)`:  Название модели по умолчанию.
- `models (list)`:  Список доступных моделей.
- `model_aliases (dict)`:  Словарь, содержащий псевдонимы для моделей.

**Методы**:

- `create_async_generator(model: str, messages: Messages, proxy: str = None, stream: bool = False, **kwargs) -> AsyncResult`
    - **Описание**: Создает асинхронный генератор для получения ответов от указанной модели.
    - **Параметры**:
        - `model (str)`: Название модели.
        - `messages (Messages)`: Список сообщений для отправки модели.
        - `proxy (str, optional)`: Прокси-сервер для использования при запросах. По умолчанию `None`.
        - `stream (bool, optional)`:  Флаг, указывающий, нужно ли использовать потоковую передачу данных (streaming). По умолчанию `False`.
    - **Возвращает**: 
        - `AsyncResult`:  Объект, представляющий асинхронный результат.

**Внутренние функции**: 
- **`inner_function`**
    - **Описание**: Внутренняя функция, которая обрабатывает полученный кусок данных.
    - **Параметры**:
        - `chunk_data (dict)`: JSON-данные, полученные из ответа от сервера.
    - **Возвращает**: 
        - `None` 
    - **Как работает**:  Внутренняя функция анализирует полученные JSON-данные, извлекает текст ответа и 
        передает его в виде строки через генератор. 
        Если в данных содержится признак окончания ответа (например, `finish_reason`),  
        функция также передает соответствующий объект `FinishReason` через генератор.

## Методы класса

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        stream: bool = False,
        **kwargs
    ) -> AsyncResult:
        api_endpoint = cls.api_endpoints[model]
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'country-code': 'US',
            'origin': 'https://www.autonomous.ai',
            'referer': 'https://www.autonomous.ai/',
            'time-zone': 'America/New_York',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }
        
        async with ClientSession(headers=headers) as session:
            message_json = json.dumps(messages)
            encoded_message = base64.b64encode(message_json.encode()).decode(errors="ignore")
            
            data = {
                "messages": encoded_message,
                "threadId": model,
                "stream": stream,
                "aiAgent": model
            }
            
            async with session.post(api_endpoint, json=data, proxy=proxy) as response:
                await raise_for_status(response)
                async for chunk in response.content:
                    if chunk:
                        chunk_str = chunk.decode()
                        if chunk_str == "data: [DONE]":
                            continue
                        
                        try:
                            # Remove "data: " prefix and parse JSON
                            chunk_data = json.loads(chunk_str.replace("data: ", ""))
                            if "choices" in chunk_data and chunk_data["choices"]:\
                                delta = chunk_data["choices"][0].get("delta", {})
                                if "content" in delta and delta["content"]:\
                                    yield delta["content"]
                            if "finish_reason" in chunk_data and chunk_data["finish_reason"]:\
                                yield FinishReason(chunk_data["finish_reason"])
                        except json.JSONDecodeError:\
                            continue
```
- **Описание**:  Функция `create_async_generator` создает асинхронный генератор для получения ответов от указанной модели.
- **Параметры**:
    - `model (str)`: Название модели.
    - `messages (Messages)`: Список сообщений для отправки модели.
    - `proxy (str, optional)`: Прокси-сервер для использования при запросах. По умолчанию `None`.
    - `stream (bool, optional)`:  Флаг, указывающий, нужно ли использовать потоковую передачу данных (streaming). По умолчанию `False`.
- **Возвращает**: 
    - `AsyncResult`:  Объект, представляющий асинхронный результат.
- **Как работает**: 
    - Функция извлекает URL-адрес API для указанной модели из словаря `api_endpoints`.
    -  Создает заголовки HTTP-запроса, включая информацию о типе контента, языке, стране и агенте пользователя.
    -  Преобразует список сообщений `messages` в формат JSON и кодирует его в base64.
    -  Создает словарь `data`, который содержит кодированные сообщения, идентификатор модели, информацию о потоковой передаче и агенте модели.
    -  Использует `aiohttp` для отправки POST-запроса к API Autonomous.ai с данными `data`.
    -  Проверяет код ответа от сервера.
    -  Использует асинхронный генератор `async for` для получения данных из ответа от сервера.
    -  Декодирует полученные данные.
    -  Парсит JSON-данные.
    -  Извлекает текст ответа и признак окончания ответа.
    -  Передает текст ответа и признак окончания ответа через генератор.

## Параметры класса

- `url (str)`: Базовый URL для API Autonomous.ai.
- `api_endpoints (dict)`:  Словарь, содержащий URL-адреса для различных моделей.
- `working (bool)`:  Флаг, указывающий, работает ли провайдер (по умолчанию `False`).
- `supports_stream (bool)`:  Флаг, указывающий, поддерживает ли провайдер потоковую передачу данных (streaming) (по умолчанию `True`).
- `supports_system_message (bool)`:  Флаг, указывающий, поддерживает ли провайдер отправку системных сообщений (по умолчанию `True`).
- `supports_message_history (bool)`:  Флаг, указывающий, поддерживает ли провайдер использование истории сообщений (по умолчанию `True`).
- `default_model (str)`:  Название модели по умолчанию.
- `models (list)`:  Список доступных моделей.
- `model_aliases (dict)`:  Словарь, содержащий псевдонимы для моделей.

## Примеры

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.AutonomousAI import AutonomousAI
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создание инстанса класса AutonomousAI
autonomous_ai = AutonomousAI()

# Список сообщений для отправки модели
messages: Messages = [
    {"role": "user", "content": "Привет! Как дела?"}
]

# Вызов функции `create_async_generator` для получения ответа от модели "llama"
async_result = await autonomous_ai.create_async_generator(model="llama", messages=messages)

# Получение ответа от модели
async for chunk in async_result:
    print(chunk)

# Получение признака окончания ответа
if isinstance(chunk, FinishReason):
    print(f"Ответ завершен по причине: {chunk.value}")
# Модуль `AmigoChat`

## Обзор

Модуль `AmigoChat` предоставляет класс `AmigoChat` для взаимодействия с API AmigoChat.io, который позволяет использовать различные модели для чата и генерации изображений.

## Подробней

Модуль предоставляет возможности:

- Инициализации драйвера для работы с различными моделями AmigoChat.
- Вызова API AmigoChat.io для генерации текста или изображений.
- Обработки ответов API, включая потоковую передачу текста и обработку изображений.
- Поддержки различных настроек, таких как температура, максимальное количество токенов, штрафы за частоту и присутствие.

## Классы

### `class AmigoChat`

**Описание**: Класс `AmigoChat` представляет собой асинхронный генератор, который предоставляет интерфейс для взаимодействия с API AmigoChat.io. Он наследует классы `AsyncGeneratorProvider` и `ProviderModelMixin`, которые обеспечивают общую функциональность для взаимодействия с API.

**Наследует**:

- `AsyncGeneratorProvider`: Предоставляет базовые функции для асинхронной работы с генераторами.
- `ProviderModelMixin`: Предоставляет методы для работы с моделями, поддерживаемыми API.

**Атрибуты**:

- `url (str)`: Базовый URL API AmigoChat.io.
- `chat_api_endpoint (str)`: URL конечной точки API для чата.
- `image_api_endpoint (str)`: URL конечной точки API для генерации изображений.
- `working (bool)`: Флаг, указывающий, работает ли API.
- `supports_stream (bool)`: Флаг, указывающий, поддерживает ли API потоковую передачу текста.
- `supports_system_message (bool)`: Флаг, указывающий, поддерживает ли API системные сообщения.
- `supports_message_history (bool)`: Флаг, указывающий, поддерживает ли API историю сообщений.
- `default_model (str)`: Модель по умолчанию, которая используется при создании нового экземпляра.
- `chat_models (list)`: Список поддерживаемых моделей для чата.
- `image_models (list)`: Список поддерживаемых моделей для генерации изображений.
- `models (list)`: Список всех поддерживаемых моделей.
- `model_aliases (dict)`: Словарь псевдонимов для моделей.

**Методы**:

- `get_personaId(cls, model: str) -> str`: Возвращает идентификатор личности (persona ID) для указанной модели.
- `generate_chat_id(cls) -> str`: Генерирует уникальный идентификатор чата в формате 8-4-4-4-12 шестнадцатеричных цифр.
- `create_async_generator(cls, model: str, messages: Messages, proxy: str = None, stream: bool = False, timeout: int = 300, frequency_penalty: float = 0, max_tokens: int = 4000, presence_penalty: float = 0, temperature: float = 0.5, top_p: float = 0.95, **kwargs) -> AsyncResult`: Создает асинхронный генератор для взаимодействия с API AmigoChat.io. 

**Принцип работы**:

Класс `AmigoChat` обеспечивает следующие функции:

- **Выбор модели:** 
    - Использует метод `get_personaId` для получения идентификатора личности (persona ID) для выбранной модели.
    - Использует метод `generate_chat_id` для создания уникального идентификатора чата.
- **Формирование запроса:** 
    - Формирует запрос к API AmigoChat.io с помощью словаря данных, содержащего параметры запроса, такие как модель, идентификатор чата, настройки запроса (температура, максимальное количество токенов и т. д.) и список сообщений.
    - Отправляет POST-запрос на соответствующую конечную точку API (для чата или генерации изображений).
- **Обработка ответа:**
    - Обрабатывает ответ API и передает полученные данные в виде потока текста или изображений.
    - Использует асинхронный генератор для потоковой передачи текста, что позволяет эффективно обрабатывать большие объемы текста.
    - Для генерации изображений извлекает URL-адреса сгенерированных изображений из ответа API и возвращает их в виде списка.

## Методы класса

### `create_async_generator`

**Назначение**: Создает асинхронный генератор для взаимодействия с API AmigoChat.io. 

**Параметры**:

- `model (str)`: Название модели, которую нужно использовать.
- `messages (Messages)`: Список сообщений, которые будут отправлены в чат.
- `proxy (str, optional)`: Прокси-сервер, который нужно использовать для отправки запроса. По умолчанию None.
- `stream (bool, optional)`: Флаг, указывающий, нужно ли использовать потоковую передачу текста. По умолчанию False.
- `timeout (int, optional)`: Время ожидания ответа от API в секундах. По умолчанию 300.
- `frequency_penalty (float, optional)`: Штраф за частоту использования слов. По умолчанию 0.
- `max_tokens (int, optional)`: Максимальное количество токенов, которое может быть сгенерировано моделью. По умолчанию 4000.
- `presence_penalty (float, optional)`: Штраф за присутствие слов. По умолчанию 0.
- `temperature (float, optional)`: Температура, которая управляет случайностью модели. По умолчанию 0.5.
- `top_p (float, optional)`: Вероятность, которая используется для отбора токенов. По умолчанию 0.95.

**Возвращает**:

- `AsyncResult`: Асинхронный результат, который представляет собой генератор, предоставляющий доступ к сгенерированному тексту или изображениям.

**Как работает функция**:

- **Выбор модели:** 
    - Получает идентификатор личности (persona ID) для выбранной модели с помощью метода `get_personaId`.
    - Генерирует уникальный идентификатор чата с помощью метода `generate_chat_id`.
- **Формирование запроса:** 
    - Формирует запрос к API AmigoChat.io с помощью словаря данных, содержащего параметры запроса, такие как модель, идентификатор чата, настройки запроса (температура, максимальное количество токенов и т. д.) и список сообщений.
    - Отправляет POST-запрос на соответствующую конечную точку API (для чата или генерации изображений).
- **Обработка ответа:**
    - Обрабатывает ответ API и передает полученные данные в виде потока текста или изображений.
    - Использует асинхронный генератор для потоковой передачи текста, что позволяет эффективно обрабатывать большие объемы текста.
    - Для генерации изображений извлекает URL-адреса сгенерированных изображений из ответа API и возвращает их в виде списка.

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.AmigoChat import AmigoChat
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [
    {'role': 'user', 'content': 'Привет! Расскажи мне о себе.'}
]

async def main():
    provider = AmigoChat()
    async for chunk in provider.create_async_generator(model='gpt-4o-mini', messages=messages):
        print(chunk)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.AmigoChat import AmigoChat
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [
    {'role': 'user', 'content': 'Сгенерируй изображение с котиком.'}
]

async def main():
    provider = AmigoChat()
    async for chunk in provider.create_async_generator(model='flux-realism', messages=messages):
        if isinstance(chunk, ImageResponse):
            print(f"Сгенерировано изображение: {chunk.image_urls}")
        else:
            print(chunk)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.AmigoChat import AmigoChat
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [
    {'role': 'system', 'content': 'Ты – дружелюбный помощник.'},
    {'role': 'user', 'content': 'Привет! Как дела?'}
]

async def main():
    provider = AmigoChat()
    async for chunk in provider.create_async_generator(model='gpt-4o-mini', messages=messages, stream=True):
        print(chunk, end='')

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

## Параметры класса

- `model (str)`: Название модели, которую нужно использовать. Доступные модели:
    - **Chat:**
        - `gpt-4o-2024-11-20`
        - `gpt-4o`
        - `gpt-4o-mini`
        - `o1-preview-`
        - `o1-preview-2024-09-12-`
        - `o1-mini-`
        - `meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo`
        - `meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo`
        - `codellama/CodeLlama-34b-Instruct-hf`
        - `gemini-1.5-pro`
        - `gemini-1.5-flash`
        - `claude-3-5-sonnet-20240620`
        - `claude-3-5-sonnet-20241022`
        - `claude-3-5-haiku-latest`
        - `Qwen/Qwen2.5-72B-Instruct-Turbo`
        - `google/gemma-2b-it`
        - `google/gemma-7b`
        - `Gryphe/MythoMax-L2-13b`
        - `mistralai/Mistral-7B-Instruct-v0.3`
        - `mistralai/mistral-tiny`
        - `mistralai/mistral-nemo`
        - `deepseek-ai/deepseek-llm-67b-chat`
        - `databricks/dbrx-instruct`
        - `NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO`
        - `x-ai/grok-beta`
        - `anthracite-org/magnum-v4-72b`
        - `cohere/command-r-plus`
        - `ai21/jamba-1-5-mini`
        - `zero-one-ai/Yi-34B`
    - **Image:**
        - `flux-pro/v1.1`
        - `flux-realism`
        - `flux-pro`
        - `flux-pro/v1.1-ultra`
        - `flux-pro/v1.1-ultra-raw`
        - `flux/dev`
        - `dall-e-3`
        - `recraft-v3`
- `proxy (str, optional)`: Прокси-сервер, который нужно использовать для отправки запроса. По умолчанию None.
- `stream (bool, optional)`: Флаг, указывающий, нужно ли использовать потоковую передачу текста. По умолчанию False.
- `timeout (int, optional)`: Время ожидания ответа от API в секундах. По умолчанию 300.
- `frequency_penalty (float, optional)`: Штраф за частоту использования слов. По умолчанию 0.
- `max_tokens (int, optional)`: Максимальное количество токенов, которое может быть сгенерировано моделью. По умолчанию 4000.
- `presence_penalty (float, optional)`: Штраф за присутствие слов. По умолчанию 0.
- `temperature (float, optional)`: Температура, которая управляет случайностью модели. По умолчанию 0.5.
- `top_p (float, optional)`: Вероятность, которая используется для отбора токенов. По умолчанию 0.95.

## Примеры

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.AmigoChat import AmigoChat

# Инициализация драйвера с моделью по умолчанию
driver = AmigoChat()

# Создание нового чата с моделью "gpt-4o-mini" и отправка сообщения
chat_id = driver.generate_chat_id()
response = driver.create_chat(model='gpt-4o-mini', chat_id=chat_id, messages=[{'role': 'user', 'content': 'Привет!'}])
print(response)

# Создание нового чата с моделью "flux-realism" и генерация изображения
image_response = driver.create_image(model='flux-realism', prompt='Сгенерируй изображение с котиком')
print(f"Сгенерировано изображение: {image_response}")

# Вывод потока текста от модели "gpt-4o-mini"
response = driver.stream_chat(model='gpt-4o-mini', chat_id=chat_id, messages=[{'role': 'user', 'content': 'Как дела?'}], stream=True)
for chunk in response:
    print(chunk, end='')

# Использование прокси-сервера
response = driver.create_chat(model='gpt-4o-mini', chat_id=chat_id, messages=[{'role': 'user', 'content': 'Привет!'}], proxy='http://proxy.example.com:8080')
print(response)
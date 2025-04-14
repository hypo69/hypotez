# Модуль `CohereForAI_C4AI_Command`

## Обзор

Модуль `CohereForAI_C4AI_Command` предназначен для взаимодействия с моделями CohereForAI C4AI Command через API. Он предоставляет функциональность для генерации текста на основе предоставленных сообщений, управления беседами и обработки ответов от API. Модуль поддерживает асинхронное взаимодействие, что позволяет эффективно использовать ресурсы при работе с API.

## Подробнее

Модуль является частью проекта `hypotez` и предназначен для использования в качестве провайдера моделей в рамках этого проекта. Он реализует специфическую логику для взаимодействия с API CohereForAI C4AI Command, включая форматирование запросов, обработку ответов и управление состоянием беседы.

## Классы

### `CohereForAI_C4AI_Command`

**Описание**: Класс `CohereForAI_C4AI_Command` реализует асинхронный генератор для взаимодействия с API CohereForAI C4AI Command. Он наследует от `AsyncGeneratorProvider` и `ProviderModelMixin`, предоставляя методы для создания асинхронных генераторов и управления моделями.

**Наследует**:

- `AsyncGeneratorProvider`: Обеспечивает базовую функциональность для асинхронных провайдеров генераторов.
- `ProviderModelMixin`: Предоставляет методы для управления моделями, такие как получение модели по имени.

**Атрибуты**:

- `label` (str): Метка провайдера, используемая для идентификации. Значение: `"CohereForAI C4AI Command"`.
- `url` (str): URL API CohereForAI C4AI Command. Значение: `"https://cohereforai-c4ai-command.hf.space"`.
- `conversation_url` (str): URL для управления беседами. Значение: `f"{url}/conversation"`.
- `working` (bool): Указывает, работает ли провайдер. Значение: `True`.
- `default_model` (str): Модель, используемая по умолчанию. Значение: `"command-a-03-2025"`.
- `model_aliases` (dict): Словарь псевдонимов моделей, позволяющий использовать короткие имена для указания конкретных моделей.
- `models` (list): Список поддерживаемых моделей, полученный из ключей `model_aliases`.

**Принцип работы**:

Класс использует `aiohttp.ClientSession` для асинхронного взаимодействия с API. Он поддерживает создание новых бесед, отправку сообщений в существующие беседы и получение ответов в виде асинхронного генератора. Класс также обрабатывает ошибки и исключения, возникающие при взаимодействии с API.

**Методы**:

- `get_model(model: str, **kwargs) -> str`: Возвращает полное имя модели на основе псевдонима.
- `create_async_generator(model: str, messages: Messages, api_key: str = None, proxy: str = None, conversation: JsonConversation = None, return_conversation: bool = False, **kwargs) -> AsyncResult`: Создает асинхронный генератор для получения ответов от API.

## Методы класса

### `get_model`

```python
@classmethod
def get_model(cls, model: str, **kwargs) -> str:
    """
    Получает полное имя модели на основе псевдонима.

    Args:
        model (str): Имя модели или псевдоним.
        **kwargs: Дополнительные аргументы.

    Returns:
        str: Полное имя модели.
    """
    ...
```

**Назначение**:
Метод `get_model` класса `CohereForAI_C4AI_Command` используется для получения полного имени модели на основе предоставленного псевдонима или имени модели. Если указанная модель присутствует в `model_aliases`, метод возвращает соответствующее значение; в противном случае, он вызывает метод `get_model` родительского класса.

**Параметры**:

- `model` (str): Имя модели или псевдоним, который необходимо преобразовать в полное имя модели.
- `**kwargs`: Дополнительные параметры, которые могут быть переданы в метод `get_model` родительского класса.

**Возвращает**:

- `str`: Полное имя модели. Если `model` есть в `model_aliases`, возвращается соответствующее значение. В противном случае, возвращается результат вызова метода `get_model` родительского класса.

**Как работает функция**:

1. Проверяет, есть ли указанная модель в словаре `model_aliases`.
2. Если модель найдена в `model_aliases`, возвращает соответствующее значение (полное имя модели).
3. Если модель не найдена в `model_aliases`, вызывает метод `get_model` родительского класса (`super().get_model(model, **kwargs)`) для обработки.
4. Возвращает результат вызова метода `get_model` родительского класса.

**Примеры**:

```python
# Пример 1: Получение полного имени модели по псевдониму
model_name = CohereForAI_C4AI_Command.get_model("command-r")
print(model_name)  # Вывод: command-r

# Пример 2: Получение полного имени модели, которое уже является полным именем
model_name = CohereForAI_C4AI_Command.get_model("command-r-08-2024")
print(model_name)  # Вывод: command-r-08-2024
```

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls, model: str, messages: Messages,
    api_key: str = None, 
    proxy: str = None,
    conversation: JsonConversation = None,
    return_conversation: bool = False,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для получения ответов от API.

    Args:
        model (str): Имя модели для использования.
        messages (Messages): Список сообщений для отправки в API.
        api_key (str, optional): API ключ для аутентификации. По умолчанию `None`.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        conversation (JsonConversation, optional): Объект, представляющий текущую беседу. По умолчанию `None`.
        return_conversation (bool, optional): Указывает, нужно ли возвращать объект беседы. По умолчанию `False`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от API.
    """
    ...
```

**Назначение**:
Метод `create_async_generator` класса `CohereForAI_C4AI_Command` создает асинхронный генератор для взаимодействия с API CohereForAI C4AI Command. Он принимает список сообщений, параметры аутентификации и прокси, а также объект беседы для поддержания состояния разговора. Генератор возвращает ответы от API в асинхронном режиме.

**Параметры**:

- `model` (str): Имя модели, которую следует использовать для генерации ответа.
- `messages` (Messages): Список сообщений, составляющих контекст запроса. Каждое сообщение содержит роль (`role`) и содержимое (`content`).
- `api_key` (str, optional): API ключ для аутентификации. Если предоставлен, используется для добавления заголовка `Authorization`. По умолчанию `None`.
- `proxy` (str, optional): URL прокси-сервера для перенаправления запросов. По умолчанию `None`.
- `conversation` (JsonConversation, optional): Объект, представляющий текущую беседу. Если предоставлен, используется для поддержания контекста разговора и повторного использования cookies. По умолчанию `None`.
- `return_conversation` (bool, optional): Флаг, указывающий, следует ли возвращать объект `conversation` в качестве первого элемента генератора. По умолчанию `False`.
- `**kwargs`: Дополнительные параметры, которые могут быть переданы в API.

**Возвращает**:

- `AsyncResult`: Асинхронный генератор, который возвращает ответы от API. Генератор может возвращать строки с текстом ответа, объекты `TitleGeneration` (если API возвращает заголовок) и, опционально, объект `JsonConversation` (если `return_conversation` установлен в `True`).

**Как работает функция**:

1. **Подготовка**:
   - Получает полное имя модели с помощью метода `cls.get_model(model)`.
   - Формирует заголовки (`headers`) для HTTP-запросов, включая `Origin`, `User-Agent`, `Accept` и другие. Если предоставлен `api_key`, добавляет заголовок `Authorization`.
2. **Создание сессии**:
   - Использует `aiohttp.ClientSession` для выполнения асинхронных HTTP-запросов. Если предоставлен объект `conversation`, использует его cookies для поддержания состояния сессии.
3. **Обработка сообщений**:
   - Разделяет сообщения на системные (`role` == "system") и пользовательские/ассистентские.
   - Извлекает системные сообщения и объединяет их в строку `system_prompt`.
   - Форматирует пользовательские/ассистентские сообщения с помощью `format_prompt(messages)`, если это начало новой беседы (т.е., `conversation` is `None`), или извлекает последнее сообщение пользователя с помощью `get_last_user_message(messages)`, если беседа уже существует.
4. **Создание или обновление беседы**:
   - Если `conversation` is `None` или параметры беседы изменились (модель или системный промпт), создает новый объект `JsonConversation`.
   - Отправляет POST-запрос на `cls.conversation_url` с данными модели и системным промптом.
   - Получает ответ, создает объект `JsonConversation` и, если `return_conversation` is `True`, возвращает его в качестве первого элемента генератора.
5. **Отправка запроса и получение ответа**:
   - Отправляет GET-запрос на `f"{cls.conversation_url}/{conversation.conversationId}/__data.json?x-sveltekit-invalidated=11"` для получения `message_id`.
   - Формирует данные (`data`) для POST-запроса, включая `inputs` (сообщение пользователя), `id` (идентификатор сообщения), и другие параметры.
   - Отправляет POST-запрос на `f"{cls.conversation_url}/{conversation.conversationId}"` с данными запроса.
   - Получает ответ в виде асинхронного потока (`response.content`) и обрабатывает каждый чанк:
     - Пытается распарсить чанк как JSON.
     - Если `data["type"]` is `"stream"`, извлекает текст (`data["token"]`) и возвращает его.
     - Если `data["type"]` is `"title"`, создает объект `TitleGeneration` и возвращает его.
     - Если `data["type"]` is `"finalAnswer"`, завершает генерацию.
6. **Обработка ошибок**:
   - Перехватывает исключения `json.JSONDecodeError` при попытке распарсить JSON и `RuntimeError` при получении ошибок от API.

**Примеры**:

```python
# Пример 1: Создание асинхронного генератора для новой беседы
messages = [
    {"role": "user", "content": "Hello, how are you?"}
]
async def run():
    async for response in CohereForAI_C4AI_Command.create_async_generator(model="command-r", messages=messages):
        print(response)

# Пример 2: Создание асинхронного генератора с использованием API ключа и прокси
messages = [
    {"role": "user", "content": "Tell me a joke."}
]
async def run():
    async for response in CohereForAI_C4AI_Command.create_async_generator(model="command-r", messages=messages, api_key="YOUR_API_KEY", proxy="http://your.proxy:8080"):
        print(response)

# Пример 3: Создание асинхронного генератора для продолжения беседы
conversation = JsonConversation(...)  # Объект JsonConversation, представляющий существующую беседу
messages = [
    {"role": "user", "content": "What was the previous joke about?"}
]
async def run():
    async for response in CohereForAI_C4AI_Command.create_async_generator(model="command-r", messages=messages, conversation=conversation):
        print(response)
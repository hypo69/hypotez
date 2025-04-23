# Модуль `AllenAI`

## Обзор

Модуль `AllenAI` предоставляет класс `AllenAI`, который является асинхронным провайдером для взаимодействия с моделями AllenAI Playground. Он поддерживает потоковую передачу данных и предоставляет возможность ведения истории разговоров. Модуль использует `aiohttp` для асинхронных HTTP-запросов.

## Подробнее

Модуль предназначен для интеграции с AllenAI Playground, позволяя отправлять запросы к различным моделям и получать ответы в асинхронном режиме. Он поддерживает различные модели, такие как `tulu3-405b`, `OLMo-2-1124-13B-Instruct`, `tulu-3-1-8b`, `Llama-3-1-Tulu-3-70B` и `olmoe-0125`.

## Классы

### `Conversation`

**Описание**: Класс `Conversation` представляет собой контейнер для хранения истории разговора с AI-моделью.

**Наследует**: `JsonConversation`

**Атрибуты**:

-   `parent` (str): Идентификатор родительского сообщения в контексте разговора.
-   `x_anonymous_user_id` (str): Уникальный идентификатор анонимного пользователя.
-   `model` (str): Название используемой модели.
-   `messages` (List[dict]): Список сообщений в разговоре, где каждое сообщение представляет собой словарь с ключами "role" (роль, например, "user" или "assistant") и "content" (содержимое сообщения).

**Методы**:

-   `__init__(self, model: str)`:
    Инициализирует новый объект `Conversation`. При создании нового объекта генерируется уникальный `x_anonymous_user_id`, если он еще не задан.

### `AllenAI`

**Описание**: Класс `AllenAI` предоставляет методы для взаимодействия с API AllenAI Playground.

**Наследует**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Атрибуты**:

-   `label` (str): Метка провайдера ("Ai2 Playground").
-   `url` (str): URL AllenAI Playground ("https://playground.allenai.org").
-   `login_url` (str): URL для логина (в данном случае `None`).
-   `api_endpoint` (str): URL API для отправки сообщений ("https://olmo-api.allen.ai/v4/message/stream").
-   `working` (bool): Флаг, указывающий, работает ли провайдер (True).
-   `needs_auth` (bool): Флаг, указывающий, требуется ли аутентификация (False).
-   `use_nodriver` (bool): Флаг, указывающий, используется ли драйвер (False).
-   `supports_stream` (bool): Флаг, указывающий, поддерживает ли провайдер потоковую передачу (True).
-   `supports_system_message` (bool): Флаг, указывающий, поддерживает ли провайдер системные сообщения (False).
-   `supports_message_history` (bool): Флаг, указывающий, поддерживает ли провайдер историю сообщений (True).
-    `default_model` (str): Модель по умолчанию (`tulu3-405b`).
-   `models` (List[str]): Список поддерживаемых моделей.
-   `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей для упрощения использования.

**Методы класса**:

#### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    host: str = "inferd",
    private: bool = True,
    top_p: float = None,
    temperature: float = None,
    conversation: Conversation = None,
    return_conversation: bool = False,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для взаимодействия с API AllenAI.

    Args:
        model (str): Название используемой модели.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        host (str, optional): Хост для отправки запроса. По умолчанию "inferd".
        private (bool, optional): Флаг, указывающий, является ли разговор приватным. По умолчанию `True`.
        top_p (float, optional): Параметр top_p для модели. По умолчанию `None`.
        temperature (float, optional): Температура для модели. По умолчанию `None`.
        conversation (Conversation, optional): Объект разговора. По умолчанию `None`.
        return_conversation (bool, optional): Флаг, указывающий, нужно ли возвращать объект разговора. По умолчанию `False`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий результаты от API AllenAI.

    
        1.  Формирует промпт на основе предоставленных сообщений. Если объект `conversation` не предоставлен, используется функция `format_prompt` для форматирования всех сообщений. В противном случае используется функция `get_last_user_message` для получения последнего сообщения пользователя.
        2.  Инициализирует или обновляет объект `conversation`. Если `conversation` не предоставлен, создается новый объект `Conversation`.
        3.  Генерирует уникальную границу (`boundary`) для multipart/form-data запроса.
        4.  Определяет заголовки запроса, включая `content-type`, `origin`, `referer` и `x-anonymous-user-id`.
        5.  Создает multipart/form-data из параметров, таких как `model`, `host`, `content` (промпт) и `private`.
        6.  Добавляет идентификатор родительского сообщения (`parent`) в запрос, если он существует в объекте `conversation`.
        7.  Добавляет необязательные параметры, такие как `temperature` и `top_p`, если они предоставлены.
        8.  Отправляет POST-запрос к API AllenAI и обрабатывает ответ в потоковом режиме.
        9.  Извлекает данные из каждого чанка ответа, декодирует его и преобразует каждую строку в JSON.
        10. Обновляет идентификатор родительского сообщения и добавляет сообщение в историю разговора при получении ответа от ассистента.
        11. Возвращает объект `conversation`, если `return_conversation` имеет значение `True`.
        12. Возвращает причину завершения (`FinishReason("stop")`) после получения финального ответа.

    Примеры:
        Пример 1: Создание асинхронного генератора с минимальными параметрами.

        ```python
        model = "tulu3-405b"
        messages = [{"role": "user", "content": "Hello, AllenAI!"}]
        generator = await AllenAI.create_async_generator(model=model, messages=messages)
        ```

        Пример 2: Создание асинхронного генератора с использованием прокси и температуры.

        ```python
        model = "tulu3-405b"
        messages = [{"role": "user", "content": "Tell me a joke."}]
        proxy = "http://your_proxy:8080"
        temperature = 0.7
        generator = await AllenAI.create_async_generator(model=model, messages=messages, proxy=proxy, temperature=temperature)
        ```

        Пример 3: Создание асинхронного генератора с сохранением истории разговора.

        ```python
        model = "tulu3-405b"
        messages = [{"role": "user", "content": "What is AI?"}]
        conversation = Conversation(model=model)
        return_conversation = True
        generator = await AllenAI.create_async_generator(
            model=model, messages=messages, conversation=conversation, return_conversation=return_conversation
        )
        ```
    """
# Модуль `AllenAI`

## Обзор

Модуль `AllenAI` предоставляет реализацию асинхронного генератора для взаимодействия с API Ai2 Playground. Он позволяет отправлять запросы к различным моделям Ai2, таким как `tulu3-405b`, `OLMo-2-1124-13B-Instruct` и другие, и получать ответы в виде асинхронного генератора. Модуль поддерживает стриминг ответов, передачу истории сообщений и настройку параметров запроса, таких как температура и top_p.

## Подробнее

Модуль предназначен для интеграции с платформой Ai2 Playground, предоставляя удобный интерфейс для отправки запросов к API и обработки ответов. Он использует `aiohttp` для асинхронных HTTP-запросов и `uuid` для генерации уникальных идентификаторов. Модуль также включает классы для управления состоянием разговора (`Conversation`) и обработки ошибок (`raise_for_status`).

## Классы

### `Conversation`

**Описание**: Класс для хранения состояния разговора с моделью Ai2.

**Наследует**:
- `JsonConversation`: Базовый класс для управления историей разговора в формате JSON.

**Атрибуты**:
- `parent` (str | None): Идентификатор родительского сообщения в разговоре.
- `x_anonymous_user_id` (str | None): Анонимный идентификатор пользователя.
- `model` (str): Название используемой модели.
- `messages` (List[dict]): Список сообщений в разговоре, где каждое сообщение представлено в виде словаря с ключами "role" и "content".

**Методы**:
- `__init__(self, model: str)`:
    - **Описание**: Инициализирует новый экземпляр класса `Conversation`.
    - **Параметры**:
        - `model` (str): Название модели, используемой в разговоре.

### `AllenAI`

**Описание**: Класс, предоставляющий асинхронный генератор для взаимодействия с API Ai2 Playground.

**Наследует**:
- `AsyncGeneratorProvider`: Базовый класс для асинхронных генераторов.
- `ProviderModelMixin`: Класс для управления моделями провайдера.

**Атрибуты**:
- `label` (str): Метка провайдера ("Ai2 Playground").
- `url` (str): URL Ai2 Playground ("https://playground.allenai.org").
- `login_url` (str | None): URL для входа (в данном случае `None`, так как не требуется).
- `api_endpoint` (str): URL API для отправки сообщений ("https://olmo-api.allen.ai/v4/message/stream").
- `working` (bool): Флаг, указывающий, работает ли провайдер (в данном случае `True`).
- `needs_auth` (bool): Флаг, указывающий, требуется ли аутентификация (в данном случае `False`).
- `use_nodriver` (bool): Флаг, указывающий, используется ли драйвер (в данном случае `False`).
- `supports_stream` (bool): Флаг, указывающий, поддерживает ли провайдер стриминг ответов (в данном случае `True`).
- `supports_system_message` (bool): Флаг, указывающий, поддерживает ли провайдер системные сообщения (в данном случае `False`).
- `supports_message_history` (bool): Флаг, указывающий, поддерживает ли провайдер историю сообщений (в данном случае `True`).
- `default_model` (str): Модель по умолчанию (`tulu3-405b`).
- `models` (List[str]): Список поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей для удобства использования.

## Методы класса

### `create_async_generator`

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
    Создает асинхронный генератор для взаимодействия с API Ai2 Playground.

    Args:
        cls (AllenAI): Класс `AllenAI`.
        model (str): Название используемой модели.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
        host (str, optional): Хост для запроса. По умолчанию "inferd".
        private (bool, optional): Флаг, указывающий, является ли запрос приватным. По умолчанию `True`.
        top_p (float, optional): Значение top_p для настройки генерации. По умолчанию `None`.
        temperature (float, optional): Температура для настройки генерации. По умолчанию `None`.
        conversation (Conversation, optional): Объект разговора. По умолчанию `None`.
        return_conversation (bool, optional): Флаг, указывающий, нужно ли возвращать объект разговора. По умолчанию `False`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий ответы от API.

    How the function works:
    - Формирует запрос к API Ai2 Playground с использованием предоставленных параметров.
    - Создает или обновляет объект разговора (`Conversation`).
    - Генерирует уникальный boundary для multipart/form-data.
    - Формирует multipart/form-data с параметрами запроса.
    - Отправляет POST-запрос к API и обрабатывает ответы, выдавая их через асинхронный генератор.
    - Обновляет состояние разговора на основе полученных ответов.

    Internal functions:
    - format_prompt(messages) - форматирует список сообщений в строку, при отсутствии conversation.
    - get_last_user_message(messages) - извлекает последнее сообщение пользователя из списка сообщений.
    - raise_for_status(response) - вызывает исключение в случае ошибки HTTP-ответа.

    Examples:
        # Пример использования с минимальными параметрами
        async for response in AllenAI.create_async_generator(model="tulu3-405b", messages=[{"role": "user", "content": "Hello, world!"}]):
            print(response)

        # Пример использования с указанием прокси и температуры
        async for response in AllenAI.create_async_generator(model="tulu3-405b", messages=[{"role": "user", "content": "Explain the meaning of life."}], proxy="http://proxy.example.com", temperature=0.7):
            print(response)

        # Пример использования с передачей объекта разговора
        conversation = Conversation(model="tulu3-405b")
        async for response in AllenAI.create_async_generator(model="tulu3-405b", messages=[{"role": "user", "content": "What is your name?"}], conversation=conversation, return_conversation=True):
            if isinstance(response, Conversation):
                conversation = response
            else:
                print(response)
    """
```

## Параметры класса

- `label` (str): "Ai2 Playground" - Метка, идентифицирующая провайдера.
- `url` (str): "https://playground.allenai.org" - URL веб-сайта Ai2 Playground.
- `login_url` (str | None): None - URL страницы входа (отсутствует в данном случае).
- `api_endpoint` (str): "https://olmo-api.allen.ai/v4/message/stream" - URL API для отправки запросов.
- `working` (bool): True - Указывает, что провайдер находится в рабочем состоянии.
- `needs_auth` (bool): False - Указывает, что для использования провайдера не требуется аутентификация.
- `use_nodriver` (bool): False - Указывает, что для работы не требуется веб-драйвер.
- `supports_stream` (bool): True - Указывает, что провайдер поддерживает потоковую передачу ответов.
- `supports_system_message` (bool): False - Указывает, что провайдер не поддерживает системные сообщения.
- `supports_message_history` (bool): True - Указывает, что провайдер поддерживает историю сообщений.
- `default_model` (str): 'tulu3-405b' - Модель, используемая по умолчанию.
- `models` (List[str]): ['tulu3-405b', 'OLMo-2-1124-13B-Instruct', 'tulu-3-1-8b', 'Llama-3-1-Tulu-3-70B', 'olmoe-0125'] - Список поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Псевдонимы для моделей, облегчающие их использование.

## Примеры

Примеры использования класса `AllenAI` и его метода `create_async_generator`:

```python
# Пример 1: Простейший запрос к модели
async for chunk in AllenAI.create_async_generator(model="tulu3-405b", messages=[{"role": "user", "content": "Напиши короткий стих о весне."}]):
    print(chunk)

# Пример 2: Запрос с указанием прокси-сервера
async for chunk in AllenAI.create_async_generator(model="tulu3-405b", messages=[{"role": "user", "content": "Расскажи анекдот."}], proxy="http://your.proxy:8080"):
    print(chunk)

# Пример 3: Использование conversation для поддержания контекста разговора
conversation = Conversation(model="tulu3-405b")
async for chunk in AllenAI.create_async_generator(model="tulu3-405b", messages=[{"role": "user", "content": "Как тебя зовут?"}], conversation=conversation):
    print(chunk)
async for chunk in AllenAI.create_async_generator(model="tulu3-405b", messages=[{"role": "user", "content": "А сколько тебе лет?"}], conversation=conversation):
    print(chunk)
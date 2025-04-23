## src/endpoints/gpt4free/g4f/Provider/Blackbox.py

## Обзор

Модуль предоставляет класс `Blackbox`, который является асинхронным провайдером для взаимодействия с API Blackbox AI. Поддерживает текстовые и графические модели, а также различные режимы агентов.
Этот модуль предназначен для интеграции с API Blackbox AI и предоставляет удобный интерфейс для отправки запросов и получения ответов, включая поддержку различных моделей и режимов агентов.

## Подробнее

Модуль `Blackbox` является частью проекта `hypotez` и предназначен для работы с API Blackbox AI. Он предоставляет функциональность для асинхронного взаимодействия с API, поддерживая различные модели, режимы агентов и функциональность для работы с изображениями. Этот модуль позволяет интегрировать возможности Blackbox AI в другие части проекта, обеспечивая гибкость и расширяемость.

## Классы

### `Conversation`

**Описание**: Класс для хранения состояния разговора с Blackbox AI.
**Наследует**: `JsonConversation`

**Атрибуты**:
- `validated_value` (str): Валидированное значение для сессии.
- `chat_id` (str): Идентификатор чата.
- `message_history` (Messages): История сообщений в разговоре.

**Методы**:
- `__init__(self, model: str)`: Инициализирует экземпляр класса `Conversation`.

### `Blackbox`

**Описание**: Класс, предоставляющий асинхронный интерфейс для взаимодействия с API Blackbox AI.
**Наследует**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Атрибуты**:
- `label` (str): Метка провайдера ("Blackbox AI").
- `url` (str): URL Blackbox AI ("https://www.blackbox.ai").
- `api_endpoint` (str): URL API Blackbox AI ("https://www.blackbox.ai/api/chat").
- `working` (bool): Флаг, указывающий на работоспособность провайдера (True).
- `supports_stream` (bool): Поддержка потоковой передачи (True).
- `supports_system_message` (bool): Поддержка системных сообщений (True).
- `supports_message_history` (bool): Поддержка истории сообщений (True).
- `default_model` (str): Модель по умолчанию ("blackboxai").
- `default_vision_model` (str): Модель для работы с изображениями по умолчанию (`default_model`).
- `default_image_model` (str): Графическая модель по умолчанию ('flux').
- `fallback_models` (list): Список бесплатных моделей.
- `image_models` (list): Список графических моделей.
- `vision_models` (list): Список моделей для анализа изображений.
- `userSelectedModel` (list): Список моделей, выбранных пользователем.
- `agentMode` (dict): Конфигурации режимов агентов.
- `trendingAgentMode` (dict): Конфигурации популярных режимов агентов.
- `_all_models` (list): Полный список моделей (для авторизованных пользователей).
- `models` (list): Список доступных моделей (инициализируется `fallback_models`).
- `model_aliases` (dict): Псевдонимы моделей.

**Принцип работы**:
Класс `Blackbox` предоставляет методы для генерации сессий, получения валидированных значений, генерации идентификаторов, получения списка доступных моделей и создания асинхронных генераторов для взаимодействия с API Blackbox AI. Он также поддерживает проверку премиум-доступа пользователя на основе HAR-файлов.

**Методы**:
- `generate_session(cls, id_length: int = 21, days_ahead: int = 365) -> dict`: Генерирует динамическую сессию с правильным ID и форматом срока действия.
- `fetch_validated(cls, url: str = "https://www.blackbox.ai", force_refresh: bool = False) -> Optional[str]`: Получает валидированное значение с веб-сайта Blackbox AI.
- `generate_id(cls, length: int = 7) -> str`: Генерирует случайный идентификатор заданной длины.
- `get_models(cls) -> list`: Возвращает список доступных моделей в зависимости от статуса авторизации пользователя.
- `_check_premium_access(cls) -> bool`: Проверяет наличие авторизованной сессии в HAR-файлах.
- `create_async_generator(cls, model: str, messages: Messages, prompt: str = None, proxy: str = None, media: MediaListType = None, top_p: float = None, temperature: float = None, max_tokens: int = None, conversation: Conversation = None, return_conversation: bool = False, **kwargs) -> AsyncResult`: Создает асинхронный генератор для взаимодействия с API Blackbox AI.

## Методы класса

### `generate_session`

```python
@classmethod
def generate_session(cls, id_length: int = 21, days_ahead: int = 365) -> dict:
    """
    Generate a dynamic session with proper ID and expiry format.
    
    Args:
        id_length: Length of the numeric ID (default: 21)
        days_ahead: Number of days ahead for expiry (default: 365)
    
    Returns:
        dict: A session dictionary with user information and expiry
    """
```

**Назначение**:
Генерирует динамическую сессию с правильным ID и форматом срока действия.

**Параметры**:
- `id_length` (int, optional): Длина числового идентификатора. По умолчанию 21.
- `days_ahead` (int, optional): Количество дней до истечения срока действия. По умолчанию 365.

**Возвращает**:
- `dict`: Словарь сессии с информацией о пользователе и сроком действия.

**Принцип работы**:
Функция генерирует числовой ID заданной длины, вычисляет дату истечения срока действия на основе текущей даты и заданного количества дней, декодирует base64-encoded email, генерирует случайный ID изображения и формирует словарь сессии с информацией о пользователе (имя, email, URL изображения, ID) и сроком действия.

**Примеры**:

```python
session = Blackbox.generate_session()
print(session)
```

```python
session = Blackbox.generate_session(id_length=25, days_ahead=400)
print(session)
```

### `fetch_validated`

```python
@classmethod
async def fetch_validated(cls, url: str = "https://www.blackbox.ai", force_refresh: bool = False) -> Optional[str]:
    """
    ...
    """
```

**Назначение**:
Получает валидированное значение с веб-сайта Blackbox AI.

**Параметры**:
- `url` (str, optional): URL веб-сайта Blackbox AI. По умолчанию "https://www.blackbox.ai".
- `force_refresh` (bool, optional): Флаг, указывающий на необходимость принудительного обновления кэша. По умолчанию `False`.

**Возвращает**:
- `Optional[str]`: Валидированное значение или `None`, если не удалось получить.

**Принцип работы**:
Функция пытается получить валидированное значение из кэш-файла. Если кэш не найден или `force_refresh` установлен в `True`, функция выполняет HTTP-запрос к веб-сайту Blackbox AI, извлекает JavaScript-файлы, ищет UUID в содержимом JavaScript-файлов и проверяет контекст для подтверждения валидности. Если валидированное значение найдено, оно сохраняется в кэш-файл и возвращается. В случае возникновения ошибок функция логирует их и возвращает `None`.

**Внутренние функции**:
- `is_valid_context(text: str) -> bool`: Проверяет, является ли контекст действительным.

**Примеры**:

```python
validated_value = await Blackbox.fetch_validated()
if validated_value:
    print(f"Валидированное значение: {validated_value}")
else:
    print("Не удалось получить валидированное значение.")
```

```python
validated_value = await Blackbox.fetch_validated(force_refresh=True)
if validated_value:
    print(f"Валидированное значение: {validated_value}")
else:
    print("Не удалось получить валидированное значение.")
```

### `generate_id`

```python
@classmethod
def generate_id(cls, length: int = 7) -> str:
    """
        ...
    """
```

**Назначение**:
Генерирует случайный идентификатор заданной длины.

**Параметры**:
- `length` (int, optional): Длина идентификатора. По умолчанию 7.

**Возвращает**:
- `str`: Случайный идентификатор.

**Принцип работы**:
Функция генерирует случайный идентификатор заданной длины, используя символы из `string.ascii_letters` и `string.digits`.

**Примеры**:

```python
id = Blackbox.generate_id()
print(f"Сгенерированный ID: {id}")
```

```python
id = Blackbox.generate_id(length=10)
print(f"Сгенерированный ID: {id}")
```

### `get_models`

```python
@classmethod
def get_models(cls) -> list:
    """
        ...
    """
```

**Назначение**:
Возвращает список доступных моделей в зависимости от статуса авторизации пользователя.

**Параметры**:
- Нет

**Возвращает**:
- `list`: Список доступных моделей.

**Принцип работы**:
Функция проверяет наличие премиум-доступа пользователя с помощью метода `_check_premium_access`. Если у пользователя есть премиум-доступ, функция возвращает полный список моделей (`cls._all_models`). В противном случае функция возвращает список бесплатных моделей (`cls.fallback_models`).

**Примеры**:

```python
models = Blackbox.get_models()
print(f"Доступные модели: {models}")
```

### `_check_premium_access`

```python
@classmethod
def _check_premium_access(cls) -> bool:
    """
        ...
    """
```

**Назначение**:
Проверяет наличие авторизованной сессии в HAR-файлах.

**Параметры**:
- Нет

**Возвращает**:
- `bool`: `True`, если найдена валидная сессия, отличная от демо-сессии, иначе `False`.

**Принцип работы**:
Функция пытается найти HAR-файлы в директории `get_cookies_dir()`. Если HAR-файлы найдены, функция анализирует их содержимое, чтобы найти информацию о сессии Blackbox AI. Если найдена валидная сессия, отличная от демо-сессии, функция возвращает `True`. В случае возникновения ошибок функция логирует их и возвращает `False`.

**Примеры**:

```python
has_premium_access = Blackbox._check_premium_access()
print(f"Премиум-доступ: {has_premium_access}")
```

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    prompt: str = None,
    proxy: str = None,
    media: MediaListType = None,
    top_p: float = None,
    temperature: float = None,
    max_tokens: int = None,
    conversation: Conversation = None,
    return_conversation: bool = False,
    **kwargs
) -> AsyncResult:
    """
    ...
    """
```

**Назначение**:
Создает асинхронный генератор для взаимодействия с API Blackbox AI.

**Параметры**:
- `model` (str): Используемая модель.
- `messages` (Messages): Список сообщений для отправки.
- `prompt` (str, optional): Промпт для генерации. По умолчанию `None`.
- `proxy` (str, optional): HTTP-прокси для использования. По умолчанию `None`.
- `media` (MediaListType, optional): Список медиафайлов для отправки. По умолчанию `None`.
- `top_p` (float, optional): Параметр top_p. По умолчанию `None`.
- `temperature` (float, optional): Температура генерации. По умолчанию `None`.
- `max_tokens` (int, optional): Максимальное количество токенов в ответе. По умолчанию `None`.
- `conversation` (Conversation, optional): Объект разговора. По умолчанию `None`.
- `return_conversation` (bool, optional): Флаг, указывающий на необходимость возврата объекта разговора. По умолчанию `False`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий части ответа от API Blackbox AI.

**Принцип работы**:
Функция создает или использует существующий объект `Conversation`, получает валидированное значение и генерирует идентификатор чата. Затем функция форматирует сообщения для отправки, добавляет медиафайлы (если они есть) и пытается получить данные сессии из HAR-файлов. После этого функция формирует JSON-данные для отправки в API Blackbox AI и выполняет асинхронный POST-запрос. Ответ от API возвращается частями через асинхронный генератор. Если `return_conversation` установлен в `True`, функция добавляет ответ в историю разговора и возвращает объект `Conversation`. Для графических моделей функция ищет URL изображения в ответе и возвращает `ImageResponse`.

**Примеры**:

```python
messages = [{"role": "user", "content": "Привет!"}]
async for chunk in Blackbox.create_async_generator(model="blackboxai", messages=messages):
    print(chunk, end="")
```
```python
messages = [{"role": "user", "content": "Нарисуй кошку."}]
async for chunk in Blackbox.create_async_generator(model="flux", messages=messages):
    print(chunk, end="")
```
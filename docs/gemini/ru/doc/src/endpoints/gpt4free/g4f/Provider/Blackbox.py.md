# Модуль `Blackbox`

## Обзор

Модуль `Blackbox` предоставляет класс `Blackbox`, который является асинхронным провайдером для взаимодействия с API Blackbox AI. Он поддерживает генерацию текста и изображений, а также управление сессиями пользователей. Модуль предназначен для интеграции в систему `hypotez` и обеспечивает доступ к различным моделям, включая как бесплатные, так и премиум-модели Blackbox AI.

## Подробнее

Модуль содержит класс `Blackbox`, который наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`. Он определяет методы для генерации сессий, получения списка доступных моделей, проверки премиум-доступа и создания асинхронного генератора для взаимодействия с API Blackbox AI. Класс также поддерживает работу с изображениями и предоставляет возможность использования различных моделей для генерации текста и изображений.

## Классы

### `Conversation(JsonConversation)`

**Описание**: Класс `Conversation` представляет собой контейнер для хранения информации о текущем разговоре с Blackbox AI.

**Наследует**: `JsonConversation`

**Атрибуты**:

-   `validated_value` (str): Валидированное значение, используемое для аутентификации.
-   `chat_id` (str): Уникальный идентификатор чата.
-   `message_history` (Messages): История сообщений в чате.
-   `model` (str): Модель, используемая в разговоре.

**Методы**:

-   `__init__(self, model: str)`:
    -   **Назначение**: Инициализирует объект `Conversation`.
    -   **Параметры**:
        -   `model` (str): Модель, используемая в разговоре.
    -   **Возвращает**: `None`

### `Blackbox(AsyncGeneratorProvider, ProviderModelMixin)`

**Описание**: Класс `Blackbox` является провайдером для взаимодействия с API Blackbox AI.

**Наследует**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Атрибуты**:

-   `label` (str): Метка провайдера ("Blackbox AI").
-   `url` (str): URL веб-сайта Blackbox AI ("https://www.blackbox.ai").
-   `api_endpoint` (str): URL API Blackbox AI ("https://www.blackbox.ai/api/chat").
-   `working` (bool): Флаг, указывающий на работоспособность провайдера (True).
-   `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи данных (True).
-   `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений (True).
-   `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений (True).
-   `default_model` (str): Модель, используемая по умолчанию ("blackboxai").
-   `default_vision_model` (str): Модель для обработки изображений по умолчанию ("blackboxai").
-   `default_image_model` (str): Модель для генерации изображений по умолчанию ('flux').
-   `fallback_models` (list): Список бесплатных моделей, доступных для использования.
-    `image_models` (list): Список моделей для генерации изображений
-   `vision_models` (list): Список моделей для обработки изображений.
-   `userSelectedModel` (list): Список моделей, выбранных пользователем.
-   `agentMode` (dict): Конфигурации режимов агента для различных моделей.
-   `trendingAgentMode` (dict): Конфигурации популярных режимов агента.
-   `_all_models` (list): Полный список всех моделей, доступных для авторизованных пользователей.
-   `models` (list): Список моделей, используемых по умолчанию (инициализируется как `fallback_models`).
-   `model_aliases` (dict): Словарь псевдонимов моделей.

## Методы класса

### `generate_session(cls, id_length: int = 21, days_ahead: int = 365) -> dict`

**Назначение**: Генерирует динамическую сессию с правильным ID и форматом срока действия.

**Параметры**:

-   `id_length` (int, optional): Длина числового ID. По умолчанию 21.
-   `days_ahead` (int, optional): Количество дней до истечения срока действия. По умолчанию 365.

**Возвращает**:

-   `dict`: Словарь сессии с информацией о пользователе и сроком действия.

**Как работает функция**:

-   Генерирует числовой ID заданной длины.
-   Вычисляет дату истечения срока действия на основе текущей даты и заданного количества дней.
-   Кодирует email в base64.
-   Генерирует случайный ID изображения для нового формата URL.
-   Возвращает словарь с информацией о пользователе, email, URL изображения, ID и сроком действия.

**Примеры**:

```python
session = Blackbox.generate_session()
print(session)
# {'user': {'name': 'BLACKBOX AI', 'email': 'gisele@blackbox.ai', 'image': 'https://lh3.googleusercontent.com/a/ACg8oc...=s96-c', 'id': '...'}, 'expires': '...'}
```

### `fetch_validated(cls, url: str = "https://www.blackbox.ai", force_refresh: bool = False) -> Optional[str]`

**Назначение**: Извлекает валидированное значение с веб-страницы Blackbox AI.

**Параметры**:

-   `url` (str, optional): URL для получения валидированного значения. По умолчанию "https://www.blackbox.ai".
-   `force_refresh` (bool, optional): Флаг, указывающий на необходимость принудительного обновления кэша. По умолчанию `False`.

**Возвращает**:

-   `Optional[str]`: Валидированное значение или `None`, если не удалось получить.

**Как работает функция**:

-   Проверяет наличие кэшированного значения в файле `blackbox.json`.
-   Если `force_refresh` установлен в `True` или кэш отсутствует, выполняет следующие действия:
    -   Получает содержимое веб-страницы Blackbox AI.
    -   Извлекает URL JS-файлов, содержащих UUID.
    -   Извлекает UUID из JS-файлов.
    -   Проверяет контекст UUID на валидность.
    -   Сохраняет валидированное значение в кэш.
-   Возвращает валидированное значение.

**Внутренние функции**:

-   `is_valid_context(text: str) -> bool`:
    -   **Назначение**: Проверяет, является ли контекст валидным.
    -   **Параметры**:
        -   `text` (str): Контекст для проверки.
    -   **Возвращает**:
        -   `bool`: `True`, если контекст валиден, `False` в противном случае.

**Примеры**:

```python
validated_value = await Blackbox.fetch_validated()
if validated_value:
    print(f"Validated value: {validated_value}")
else:
    print("Failed to fetch validated value")
```

### `generate_id(cls, length: int = 7) -> str`

**Назначение**: Генерирует случайный ID заданной длины.

**Параметры**:

-   `length` (int, optional): Длина генерируемого ID. По умолчанию 7.

**Возвращает**:

-   `str`: Случайный ID.

**Как работает функция**:

-   Генерирует случайную строку из букв и цифр заданной длины.

**Примеры**:

```python
id = Blackbox.generate_id()
print(f"Generated ID: {id}")
```

### `get_models(cls) -> list`

**Назначение**: Возвращает список доступных моделей на основе статуса авторизации.

**Параметры**:

-   `cls`: Ссылка на класс `Blackbox`.

**Возвращает**:

-   `list`: Список доступных моделей.

**Как работает функция**:

-   Проверяет наличие премиум-доступа путем вызова метода `_check_premium_access`.
-   Если премиум-доступ есть, возвращает полный список моделей (`cls._all_models`).
-   Если премиум-доступа нет, возвращает список бесплатных моделей (`cls.fallback_models`).

**Примеры**:

```python
models = Blackbox.get_models()
print(f"Available models: {models}")
```

### `_check_premium_access(cls) -> bool`

**Назначение**: Проверяет наличие авторизованной сессии в HAR-файлах.

**Параметры**:

-   `cls`: Ссылка на класс `Blackbox`.

**Возвращает**:

-   `bool`: `True`, если найдена валидная сессия, отличающаяся от демо-сессии, `False` в противном случае.

**Как работает функция**:

-   Проверяет наличие HAR-файлов в директории cookies.
-   Просматривает HAR-файлы в поисках запросов к API Blackbox AI.
-   Извлекает данные сессии из ответов API.
-   Проверяет, является ли сессия валидной и отличается ли она от демо-сессии.
-   Если найдена валидная сессия, возвращает `True`.

**Примеры**:

```python
has_premium_access = Blackbox._check_premium_access()
print(f"Premium access: {has_premium_access}")
```

### `create_async_generator(cls, model: str, messages: Messages, prompt: str = None, proxy: str = None, media: MediaListType = None, top_p: float = None, temperature: float = None, max_tokens: int = None, conversation: Conversation = None, return_conversation: bool = False, **kwargs) -> AsyncResult`

**Назначение**: Создает асинхронный генератор для взаимодействия с API Blackbox AI.

**Параметры**:

-   `model` (str): Модель для использования.
-   `messages` (Messages): Список сообщений для отправки.
-   `prompt` (str, optional): Дополнительный промпт. По умолчанию `None`.
-   `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
-   `media` (MediaListType, optional): Список медиафайлов для отправки. По умолчанию `None`.
-   `top_p` (float, optional): Параметр top_p. По умолчанию `None`.
-   `temperature` (float, optional): Параметр temperature. По умолчанию `None`.
-   `max_tokens` (int, optional): Максимальное количество токенов. По умолчанию `None`.
-   `conversation` (Conversation, optional): Объект `Conversation` для продолжения существующего разговора. По умолчанию `None`.
-   `return_conversation` (bool, optional): Флаг, указывающий на необходимость возврата объекта `Conversation`. По умолчанию `False`.
-   `**kwargs`: Дополнительные аргументы.

**Возвращает**:

-   `AsyncResult`: Асинхронный генератор для получения ответов от API Blackbox AI.

**Как работает функция**:

1.  **Подготовка**:
    -   Получает модель, используя `cls.get_model(model)`.
    -   Определяет заголовки запроса.
    -   Если объект `conversation` не предоставлен или у него нет `chat_id`, создает новый объект `Conversation` и генерирует `validated_value` и `chat_id`.
    -   Преобразует список сообщений в формат, ожидаемый API Blackbox AI.
    -   Если предоставлены медиафайлы, добавляет их в последнее сообщение.
2.  **Поиск данных сессии**:
    -   Пытается получить данные сессии из HAR-файлов.
    -   Если данные сессии не найдены, использует `cls.generate_session()` для создания новой сессии.
3.  **Формирование данных запроса**:
    -   Формирует словарь `data` с информацией о сообщении, модели, параметрах и сессии.
4.  **Отправка запроса**:
    -   Отправляет POST-запрос к API Blackbox AI с использованием `aiohttp.ClientSession`.
    -   Обрабатывает ответ от API.
    -   Для моделей изображений извлекает URL изображения из ответа и возвращает объект `ImageResponse`.
    -   Для текстовых моделей возвращает текст ответа.
5.  **Обработка истории разговора**:
    -   Если `return_conversation` установлен в `True`, добавляет ответ ассистента в историю разговора и возвращает объект `conversation`.

**Примеры**:

```python
messages = [{"role": "user", "content": "Hello, how are you?"}]
async for response in Blackbox.create_async_generator(model="blackboxai", messages=messages):
    print(response)
```

## Параметры класса

-   `label` (str): Метка провайдера ("Blackbox AI").
-   `url` (str): URL веб-сайта Blackbox AI ("https://www.blackbox.ai").
-   `api_endpoint` (str): URL API Blackbox AI ("https://www.blackbox.ai/api/chat").
-   `working` (bool): Флаг, указывающий на работоспособность провайдера (True).
-   `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи данных (True).
-   `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений (True).
-   `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений (True).
-   `default_model` (str): Модель, используемая по умолчанию ("blackboxai").
-   `default_vision_model` (str): Модель для обработки изображений по умолчанию ("blackboxai").
-   `default_image_model` (str): Модель для генерации изображений по умолчанию ('flux').
-   `fallback_models` (list): Список бесплатных моделей, доступных для использования.
-    `image_models` (list): Список моделей для генерации изображений
-   `vision_models` (list): Список моделей для обработки изображений.
-   `userSelectedModel` (list): Список моделей, выбранных пользователем.
-   `agentMode` (dict): Конфигурации режимов агента для различных моделей.
-   `trendingAgentMode` (dict): Конфигурации популярных режимов агента.
-   `_all_models` (list): Полный список всех моделей, доступных для авторизованных пользователей.
-   `models` (list): Список моделей, используемых по умолчанию (инициализируется как `fallback_models`).
-   `model_aliases` (dict): Словарь псевдонимов моделей.
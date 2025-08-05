# HailuoAI.py

## Обзор

Этот файл содержит класс `HailuoAI`, который реализует асинхронного провайдера для Hailuo AI, предоставляющего доступ к модели MiniMax через API.

## Подробнее

Этот файл реализует асинхронного провайдера для Hailuo AI, предоставляющего доступ к модели MiniMax. Он реализует интерфейс `AsyncAuthedProvider` и `ProviderModelMixin` для совместимости с другими провайдерами в проекте.

**Основные функции:**

- **Аутентификация:**  `HailuoAI` использует `on_auth_async` для аутентификации в Hailuo AI.
- **Создание беседы:**  `create_authed` инициализирует беседу с моделью MiniMax.
- **Обработка ответов:**  `create_authed` использует `async for` для обработки ответов модели, включая обработку событий `send_result`, `message_result` и `close_chunk`.

## Классы

### `class Conversation`

**Описание**: Класс `Conversation` представляет собой объект беседы с Hailuo AI, содержащий необходимую информацию для взаимодействия с API.

**Атрибуты**:

- `token` (str): Токен аутентификации пользователя.
- `chatID` (str): Идентификатор текущей беседы.
- `characterID` (str, optional): Идентификатор персонажа, по умолчанию 1.

### `class HailuoAI`

**Описание**: Класс `HailuoAI` реализует асинхронного провайдера для Hailuo AI, предоставляющего доступ к модели MiniMax.

**Наследует**:
- `AsyncAuthedProvider`:  Предоставляет функциональность асинхронной аутентификации и взаимодействия с API.
- `ProviderModelMixin`:  Предоставляет функциональность для работы с моделями.

**Атрибуты**:

- `label` (str):  "Hailuo AI".
- `url` (str): "https://www.hailuo.ai".
- `working` (bool):  `True`.
- `use_nodriver` (bool): `True`.
- `supports_stream` (bool): `True`.
- `default_model` (str): "MiniMax".

**Методы**:

#### `async def on_auth_async(cls, proxy: str = None, **kwargs) -> AsyncIterator`:

**Описание**: Асинхронная функция аутентификации для Hailuo AI.

**Параметры**:

- `proxy` (str, optional): Прокси-сервер для доступа к Hailuo AI.

**Возвращает**:
- `AsyncIterator`: Генератор, который возвращает объекты `RequestLogin` и `AuthResult`.

**Как работает**:

-  Получает URL для входа из переменной окружения `G4F_LOGIN_URL`.
-  Использует `get_args_from_nodriver` для получения аргументов для `ClientSession`.
-  Использует `get_browser_callback` для создания обратного вызова для получения данных от браузера.
-  Возвращает объект `AuthResult` с токеном и другой информацией, необходимой для взаимодействия с API Hailuo AI.

#### `async def create_authed(cls, model: str, messages: Messages, auth_result: AuthResult, return_conversation: bool = False, conversation: Conversation = None, **kwargs) -> AsyncResult`:

**Описание**: Асинхронная функция для создания беседы с моделью MiniMax в Hailuo AI.

**Параметры**:

- `model` (str):  Название модели, по умолчанию "MiniMax".
- `messages` (Messages):  Список сообщений в текущей беседе.
- `auth_result` (AuthResult):  Результат аутентификации, полученный из `on_auth_async`.
- `return_conversation` (bool, optional):  Если `True`, возвращает объект `Conversation` для текущей беседы, по умолчанию `False`.
- `conversation` (Conversation, optional):  Объект `Conversation` для продолжения существующей беседы.

**Возвращает**:
- `AsyncResult`:  Генератор, который возвращает объекты `TitleGeneration`, `Conversation` и текст ответа модели.

**Как работает**:

-  Создает экземпляр `ClientSession` с аргументами из `auth_result`.
-  Создает объект `FormData` для отправки запроса на API Hailuo AI.
-  Отправляет POST-запрос на API с использованием `session.post`.
-  Использует `async for` для обработки ответов модели.
-  Обрабатывает события `send_result`, `message_result` и `close_chunk`.
-  Возвращает объекты `TitleGeneration`, `Conversation` и текст ответа модели.
# Модуль `HailuoAI`

## Обзор

Модуль `HailuoAI` представляет собой асинхронный провайдер для взаимодействия с Hailuo AI, использующий API MiniMax. Он обеспечивает аутентификацию, создание бесед и потоковую передачу сообщений.

## Подробней

Модуль предназначен для интеграции с платформой Hailuo AI, предоставляя возможность использовать её функциональность в асинхронном режиме. Он включает в себя механизмы аутентификации, формирования запросов и обработки ответов от сервера Hailuo AI. Модуль поддерживает потоковую передачу данных, что позволяет получать ответы в режиме реального времени.

## Классы

### `Conversation`

**Описание**: Класс представляет собой структуру данных для хранения информации о беседе с Hailuo AI.

**Аттрибуты**:
- `token` (str): Токен авторизации для доступа к API Hailuo AI.
- `chatID` (str): Идентификатор чата.
- `characterID` (str): Идентификатор персонажа (по умолчанию `1`).

### `HailuoAI`

**Описание**: Класс `HailuoAI` является асинхронным провайдером для взаимодействия с Hailuo AI. Он наследуется от `AsyncAuthedProvider` и `ProviderModelMixin` и реализует методы для аутентификации и создания бесед.

**Наследует**:
- `AsyncAuthedProvider`: Обеспечивает асинхронную аутентификацию.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.

**Аттрибуты**:
- `label` (str): Метка провайдера ("Hailuo AI").
- `url` (str): URL адрес Hailuo AI ("https://www.hailuo.ai").
- `working` (bool): Флаг, указывающий на работоспособность провайдера (`True`).
- `use_nodriver` (bool): Флаг, указывающий на использование без драйвера (`True`).
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи данных (`True`).
- `default_model` (str): Модель по умолчанию ("MiniMax").

**Методы**:

- `on_auth_async`: Метод для выполнения асинхронной аутентификации.
- `create_authed`: Метод для создания аутентифицированного запроса к Hailuo AI.

## Функции

### `on_auth_async`

```python
@classmethod
async def on_auth_async(cls, proxy: str = None, **kwargs) -> AsyncIterator:
    """Метод для выполнения асинхронной аутентификации.

    Args:
        proxy (str, optional): Прокси-сервер для использования при аутентификации. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncIterator: Асинхронный итератор, возвращающий результаты аутентификации.
    """
    ...
```

**Назначение**: Выполняет асинхронную аутентификацию на платформе Hailuo AI.

**Параметры**:
- `proxy` (str, optional): Прокси-сервер для использования при аутентификации. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы, которые могут потребоваться для аутентификации.

**Возвращает**:
- `AsyncIterator`: Асинхронный итератор, который возвращает объекты `RequestLogin` и `AuthResult`, содержащие информацию об аутентификации.

**Как работает функция**:
1. **Проверка переменной окружения `G4F_LOGIN_URL`**: Функция проверяет, установлена ли переменная окружения `G4F_LOGIN_URL`. Если она установлена, то генерируется объект `RequestLogin` с URL для логина.
2. **Получение результатов обратного вызова браузера**: Функция вызывает `get_browser_callback` для получения результатов аутентификации из браузера.
3. **Получение аргументов из nodriver**: Функция вызывает `get_args_from_nodriver` для получения аргументов аутентификации без использования драйвера.
4. **Генерация объекта `AuthResult`**: На основе полученных данных создается объект `AuthResult`, содержащий результаты аутентификации.

```
    Начало
    │
    ├── Проверка переменной окружения G4F_LOGIN_URL
    │   └── Если установлена:
    │       └── Генерация объекта RequestLogin
    │
    ├── Получение результатов обратного вызова браузера (get_browser_callback)
    │
    └── Получение аргументов из nodriver (get_args_from_nodriver)
        │
        └── Генерация объекта AuthResult
            │
            └── Завершение
```

**Примеры**:

```python
# Пример вызова функции on_auth_async без прокси
async for result in HailuoAI.on_auth_async():
    print(result)

# Пример вызова функции on_auth_async с прокси
async for result in HailuoAI.on_auth_async(proxy='http://proxy.example.com'):
    print(result)
```

### `create_authed`

```python
@classmethod
async def create_authed(
    cls,
    model: str,
    messages: Messages,
    auth_result: AuthResult,
    return_conversation: bool = False,
    conversation: Conversation = None,
    **kwargs
) -> AsyncResult:
    """Создает аутентифицированный запрос к Hailuo AI.

    Args:
        model (str): Модель для использования.
        messages (Messages): Список сообщений для отправки.
        auth_result (AuthResult): Результат аутентификации.
        return_conversation (bool, optional): Флаг, указывающий на необходимость возврата информации о беседе. По умолчанию `False`.
        conversation (Conversation, optional): Объект беседы. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный итератор, возвращающий результаты запроса.
    """
    ...
```

**Назначение**: Создает аутентифицированный запрос к Hailuo AI.

**Параметры**:
- `model` (str): Модель для использования.
- `messages` (Messages): Список сообщений для отправки.
- `auth_result` (AuthResult): Результат аутентификации.
- `return_conversation` (bool, optional): Флаг, указывающий на необходимость возврата информации о беседе. По умолчанию `False`.
- `conversation` (Conversation, optional): Объект беседы. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный итератор, возвращающий результаты запроса.

**Как работает функция**:

1. **Извлечение данных из `auth_result`**: Извлекаются необходимые данные (токен, путь и запрос, временная метка) из объекта `auth_result`.
2. **Инициализация `ClientSession`**: Создается асинхронная сессия клиента `ClientSession` с параметрами из `auth_result`.
3. **Формирование данных запроса**:
   - Если `conversation` не задан, формируются данные для начала новой беседы.
   - Если `conversation` задан, используются его параметры (идентификатор персонажа, идентификатор чата) и последнее сообщение пользователя.
4. **Создание `FormData`**: Данные запроса упаковываются в объект `FormData`.
5. **Формирование заголовков запроса**: Создаются заголовки запроса, включая токен и заголовок `yy`.
6. **Отправка запроса**: Отправляется POST-запрос к API Hailuo AI с использованием `ClientSession`.
7. **Обработка ответа**:
   - Читается ответ построчно.
   - Извлекаются события (`event`) из каждой строки.
   - Обрабатываются события `close_chunk`, `send_result` и `message_result`.
   - Генерируются объекты `TitleGeneration` (если есть заголовок чата) и `Conversation` (если запрошено возвращение информации о беседе).
   - Извлекается и передается содержимое сообщения.

```
    Начало
    │
    ├── Извлечение данных из auth_result
    │
    ├── Инициализация ClientSession
    │
    ├── Формирование данных запроса
    │   ├── Если conversation is None:
    │   │   └── Формирование данных для новой беседы
    │   └── Иначе:
    │       └── Использование параметров conversation и последнего сообщения
    │
    ├── Создание FormData
    │
    ├── Формирование заголовков запроса
    │
    ├── Отправка POST-запроса
    │
    └── Обработка ответа
        ├── Чтение ответа построчно
        ├── Извлечение событий (event)
        ├── Обработка событий
        │   ├── close_chunk: Завершение обработки
        │   ├── send_result: Генерация TitleGeneration и Conversation
        │   └── message_result: Извлечение и передача содержимого сообщения
        │
        └── Завершение
```

**Примеры**:

```python
# Пример вызова функции create_authed без conversation
auth_result = AuthResult(token='test_token', path_and_query='/api/chat', timestamp='12345')
messages = [{'role': 'user', 'content': 'Hello'}]
async for result in HailuoAI.create_authed(model='MiniMax', messages=messages, auth_result=auth_result):
    print(result)

# Пример вызова функции create_authed с conversation
conversation = Conversation(token='test_token', chatID='123', characterID=1)
messages = [{'role': 'user', 'content': 'Hello again'}]
async for result in HailuoAI.create_authed(model='MiniMax', messages=messages, auth_result=auth_result, conversation=conversation):
    print(result)
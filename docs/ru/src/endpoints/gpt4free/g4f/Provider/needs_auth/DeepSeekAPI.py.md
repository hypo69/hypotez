# Модуль `DeepSeekAPI`

## Обзор

Модуль `DeepSeekAPI` предназначен для взаимодействия с API DeepSeek для получения ответов от AI-моделей. Он предоставляет асинхронный интерфейс для аутентификации и создания чат-сессий с использованием DeepSeek API. Этот модуль интегрирован с системой `g4f` и использует вспомогательные функции из других модулей для обработки запросов и аутентификации.

## Подробней

Модуль реализует класс `DeepSeekAPI`, который наследуется от `AsyncAuthedProvider` и `ProviderModelMixin`. Он обеспечивает аутентификацию через веб-интерфейс и позволяет создавать чат-сессии для взаимодействия с AI-моделями DeepSeek. В модуле используются асинхронные функции для неблокирующих операций, что важно для эффективной работы с API.

## Классы

### `DeepSeekAPI`

**Описание**: Класс `DeepSeekAPI` предоставляет интерфейс для взаимодействия с DeepSeek API. Он реализует методы для аутентификации, создания чат-сессий и получения ответов от AI-моделей.

**Наследует**:
- `AsyncAuthedProvider`: Обеспечивает асинхронную аутентификацию.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `url` (str): URL для доступа к DeepSeek API.
- `working` (bool): Указывает, работает ли модуль (зависит от наличия библиотеки `dsk`).
- `needs_auth` (bool): Указывает, требуется ли аутентификация.
- `use_nodriver` (bool): Указывает, используется ли бездрайверный режим.
- `_access_token` (str | None): Токен доступа для аутентификации.
- `default_model` (str): Модель, используемая по умолчанию (`deepseek-v3`).
- `models` (List[str]): Список поддерживаемых моделей (`deepseek-v3`, `deepseek-r1`).

**Методы**:
- `on_auth_async`: Асинхронный метод для аутентификации пользователя.
- `create_authed`: Асинхронный метод для создания аутентифицированной сессии и получения ответов от AI-модели.

## Функции

### `on_auth_async`

```python
@classmethod
async def on_auth_async(cls, proxy: str = None, **kwargs) -> AsyncIterator:
    """Асинхронно аутентифицирует пользователя для доступа к DeepSeek API.

    Args:
        proxy (str, optional): Прокси-сервер для использования при подключении. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Yields:
        RequestLogin: Объект, содержащий информацию о необходимости логина.
        AuthResult: Объект, содержащий результат аутентификации и токен доступа.

    Raises:
        Exception: Если возникает ошибка при аутентификации.

    Как работает функция:
    1. Проверяет, инициализирован ли браузер (`cls.browser`). Если нет, то запускает бездрайверный браузер с помощью `get_nodriver()`.
    2. Отправляет запрос на логин, используя `yield RequestLogin`.
    3. Определяет асинхронную функцию `callback`, которая ожидает появления токена доступа (`userToken`) в `localStorage` страницы.
    4. Получает аргументы для запуска браузера с помощью `get_args_from_nodriver`, передавая URL, прокси и функцию `callback`.
    5. Возвращает результат аутентификации, содержащий токен доступа, используя `yield AuthResult`.

    Внутренние функции:
        callback(page): Асинхронная функция, ожидающая появления токена доступа в `localStorage` страницы.
            Args:
                page: Объект страницы браузера.
            Как работает внутренняя функция:
            1.  Бесконечно ждет, пока не будет получен токен доступа из `localStorage`.
            2.  Считывает значение `userToken` из `localStorage` страницы с помощью `await page.evaluate`.
            3.  Преобразует полученное значение из JSON в словарь и извлекает токен доступа из ключа `"value"`.
            4.  Если токен доступа получен, присваивает его `cls._access_token` и завершает ожидание.

    ASCII flowchart:
    A: Проверка инициализации браузера
    |
    B: Запуск бездрайверного браузера
    |
    C: Запрос на логин (RequestLogin)
    |
    D: Определение асинхронной функции callback
    |
    E: Получение аргументов для запуска браузера (get_args_from_nodriver)
    |
    F: Возврат результата аутентификации (AuthResult)

    Примеры:
    ```python
    # Пример вызова функции on_auth_async
    async for result in DeepSeekAPI.on_auth_async(proxy="http://example.com:8080"):
        print(result)
    ```
    """
    ...
```

### `create_authed`

```python
@classmethod
async def create_authed(
    cls,
    model: str,
    messages: Messages,
    auth_result: AuthResult,
    conversation: JsonConversation = None,
    web_search: bool = False,
    **kwargs
) -> AsyncResult:
    """Создает аутентифицированную сессию и получает ответы от AI-модели DeepSeek.

    Args:
        model (str): Имя используемой модели.
        messages (Messages): Список сообщений для отправки в AI-модель.
        auth_result (AuthResult): Результат аутентификации, содержащий токен доступа.
        conversation (JsonConversation, optional): Объект разговора, содержащий ID чат-сессии. По умолчанию `None`.
        web_search (bool, optional): Указывает, следует ли использовать поиск в интернете. По умолчанию `False`.
        **kwargs: Дополнительные аргументы.

    Yields:
        conversation (JsonConversation): Объект разговора с ID чат-сессии.
        Reasoning (str): Объект, содержащий информацию о процессе мышления модели.
        str: Ответ от AI-модели.
        FinishReason (str): Объект, содержащий причину завершения разговора.

    Raises:
        Exception: Если возникает ошибка при создании сессии или получении ответа.

    Как работает функция:
    1. Инициализирует API DeepSeek с использованием токена доступа из `auth_result`.
    2. Если `conversation` не предоставлен, создает новую чат-сессию с помощью `api.create_chat_session()` и создает объект `JsonConversation`.
    3. Отправляет последнее сообщение пользователя в AI-модель с использованием `api.chat_completion()`.
    4. Итерируется по чанкам ответа, обрабатывая каждый чанк в зависимости от его типа:
        - Если тип `'thinking'`, возвращает объект `Reasoning` с информацией о процессе мышления модели.
        - Если тип `'text'`, возвращает текст ответа модели.
        - Если есть `finish_reason`, возвращает объект `FinishReason` с причиной завершения разговора.

    ASCII flowchart:
    A: Инициализация API DeepSeek
    |
    B: Проверка наличия conversation
    |
    C: Создание новой чат-сессии (если conversation отсутствует)
    |
    D: Отправка сообщения в AI-модель (api.chat_completion)
    |
    E: Итерация по чанкам ответа
    |
    F: Обработка чанков в зависимости от типа
    |
    G: Возврат результата (conversation, Reasoning, str, FinishReason)

    Примеры:
    ```python
    # Пример вызова функции create_authed
    auth_result = AuthResult(api_key="your_api_key")
    messages = [{"role": "user", "content": "Hello, how are you?"}]
    async for result in DeepSeekAPI.create_authed(model="deepseek-v3", messages=messages, auth_result=auth_result):
        print(result)
    ```
    """
    ...
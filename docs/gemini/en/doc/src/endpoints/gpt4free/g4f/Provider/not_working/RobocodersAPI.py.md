# Модуль `RobocodersAPI.py`

## Обзор

Модуль `RobocodersAPI.py` предоставляет реализацию асинхронного провайдера для взаимодействия с API Robocoders AI. Он позволяет общаться с различными агентами, такими как `GeneralCodingAgent`, `RepoAgent` и `FrontEndAgent`. Модуль поддерживает сохранение истории сообщений и использует кэширование для хранения токена доступа и идентификатора сессии.

## Более подробная информация

Модуль предназначен для интеграции с системой `hypotez` и предоставляет удобный интерфейс для взаимодействия с Robocoders AI. Он автоматически обновляет и кэширует необходимые данные для авторизации, что упрощает использование API.

## Классы

### `RobocodersAPI`

**Описание**: Класс `RobocodersAPI` реализует асинхронный провайдер для взаимодействия с API Robocoders AI.

**Наследует**:
- `AsyncGeneratorProvider`: Предоставляет базовую функциональность для асинхронных генераторов.
- `ProviderModelMixin`: Добавляет поддержку выбора модели.

**Атрибуты**:
- `label` (str): Метка провайдера ("API Robocoders AI").
- `url` (str): URL документации API ("https://api.robocoders.ai/docs").
- `api_endpoint` (str): URL конечной точки API ("https://api.robocoders.ai/chat").
- `working` (bool): Флаг, указывающий, работает ли провайдер (False).
- `supports_message_history` (bool): Флаг, указывающий, поддерживает ли провайдер историю сообщений (True).
- `default_model` (str): Модель по умолчанию ('GeneralCodingAgent').
- `agent` (List[str]): Список доступных агентов.
- `models` (List[str]): Список доступных моделей.
- `CACHE_DIR` (Path): Директория для кэширования данных.
- `CACHE_FILE` (Path): Файл для кэширования данных (robocoders.json).

**Принцип работы**:

Класс использует асинхронные запросы для взаимодействия с API Robocoders AI. Он автоматически получает и кэширует токен доступа и идентификатор сессии, что упрощает процесс аутентификации. При отправке запросов класс обрабатывает возможные ошибки, такие как неавторизованный доступ, ошибки валидации и серверные ошибки.

### Методы класса

- `create_async_generator`
- `_get_or_create_access_and_session`
- `_fetch_and_cache_access_token`
- `_create_and_cache_session`
- `_save_cached_data`
- `_update_cached_data`
- `_clear_cached_data`
- `_get_cached_data`

## Методы

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для взаимодействия с API Robocoders AI.

    Args:
        cls (RobocodersAPI): Класс RobocodersAPI.
        model (str): Модель для использования.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий сообщения от API.

    Raises:
        Exception: Если не удалось инициализировать взаимодействие с API, возникла ошибка авторизации,
                   ошибка валидации или серверная ошибка.
    """
```

**Назначение**:
Создает асинхронный генератор для взаимодействия с API Robocoders AI. Генератор отправляет сообщения в API и возвращает ответы в асинхронном режиме.

**Параметры**:
- `cls` (RobocodersAPI): Класс `RobocodersAPI`.
- `model` (str): Модель для использования.
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий сообщения от API.

**Исключения**:
- `Exception`: Если не удалось инициализировать взаимодействие с API, возникла ошибка авторизации, ошибка валидации или серверная ошибка.

**Как работает функция**:
1. Устанавливает таймаут для HTTP-клиента.
2. Создает асинхронную сессию HTTP-клиента.
3. Получает или создает токен доступа и идентификатор сессии.
4. Формирует заголовки запроса с токеном доступа.
5. Формирует данные запроса, включая идентификатор сессии, промпт и модель.
6. Отправляет POST-запрос к API.
7. Обрабатывает различные коды состояния HTTP-ответа, такие как 401 (неавторизованный доступ), 422 (ошибка валидации) и 500+ (серверные ошибки).
8. Итерируется по содержимому ответа, декодирует JSON и извлекает сообщения из полей `args.content` или `message`.
9. Проверяет, достигнут ли лимит ресурсов, и автоматически продолжает диалог, если это необходимо.

**Примеры**:

```python
# Пример использования асинхронного генератора
async for message in RobocodersAPI.create_async_generator(model='GeneralCodingAgent', messages=[{'role': 'user', 'content': 'Привет!'}]):
    print(message)
```

### `_get_or_create_access_and_session`

```python
@staticmethod
async def _get_or_create_access_and_session(session: aiohttp.ClientSession):
    """
    Получает или создает токен доступа и идентификатор сессии.

    Args:
        session (aiohttp.ClientSession): Асинхронная сессия HTTP-клиента.

    Returns:
        Tuple[str, str]: Токен доступа и идентификатор сессии.

    Raises:
        Exception: Если не удалось получить токен доступа или создать сессию.
    """
```

**Назначение**:
Получает токен доступа и идентификатор сессии из кэша, если они существуют и валидны. В противном случае создает новые токен и сессию и сохраняет их в кэше.

**Параметры**:
- `session` (aiohttp.ClientSession): Асинхронная сессия HTTP-клиента.

**Возвращает**:
- `Tuple[str, str]`: Токен доступа и идентификатор сессии.

**Исключения**:
- `Exception`: Если не удалось получить токен доступа или создать сессию.

**Как работает функция**:
1. Создает директорию для кэширования, если она не существует.
2. Проверяет, существует ли файл кэша.
3. Если файл кэша существует, загружает данные из файла.
4. Проверяет, валидны ли токен доступа и идентификатор сессии.
5. Если токен и сессия валидны, возвращает их.
6. Если токен или сессия невалидны, получает новый токен доступа и создает новый идентификатор сессии.
7. Сохраняет новые токен и сессию в кэше.

**Примеры**:

```python
# Пример получения токена и сессии
async with aiohttp.ClientSession() as session:
    access_token, session_id = await RobocodersAPI._get_or_create_access_and_session(session)
    print(f"Access Token: {access_token}, Session ID: {session_id}")
```

### `_fetch_and_cache_access_token`

```python
@staticmethod
async def _fetch_and_cache_access_token(session: aiohttp.ClientSession) -> str:
    """
    Получает и кэширует токен доступа.

    Args:
        session (aiohttp.ClientSession): Асинхронная сессия HTTP-клиента.

    Returns:
        str: Токен доступа.

    Raises:
        MissingRequirementsError: Если отсутствует библиотека BeautifulSoup4.
    """
```

**Назначение**:
Получает токен доступа с использованием BeautifulSoup4 для парсинга HTML-страницы и кэширует его.

**Параметры**:
- `session` (aiohttp.ClientSession): Асинхронная сессия HTTP-клиента.

**Возвращает**:
- `str`: Токен доступа.

**Исключения**:
- `MissingRequirementsError`: Если отсутствует библиотека BeautifulSoup4.

**Как работает функция**:
1. Проверяет, установлена ли библиотека BeautifulSoup4.
2. Отправляет GET-запрос к URL аутентификации.
3. Парсит HTML-ответ с помощью BeautifulSoup4.
4. Ищет элемент `<pre>` с id `token`.
5. Извлекает текст из элемента, который является токеном доступа.
6. Кэширует токен доступа.

**Примеры**:

```python
# Пример получения и кэширования токена
async with aiohttp.ClientSession() as session:
    token = await RobocodersAPI._fetch_and_cache_access_token(session)
    print(f"Access Token: {token}")
```

### `_create_and_cache_session`

```python
@staticmethod
async def _create_and_cache_session(session: aiohttp.ClientSession, access_token: str) -> str:
    """
    Создает и кэширует идентификатор сессии.

    Args:
        session (aiohttp.ClientSession): Асинхронная сессия HTTP-клиента.
        access_token (str): Токен доступа.

    Returns:
        str: Идентификатор сессии.

    Raises:
        Exception: Если произошла ошибка авторизации или ошибка валидации.
    """
```

**Назначение**:
Создает идентификатор сессии, отправляя запрос к API, и кэширует его.

**Параметры**:
- `session` (aiohttp.ClientSession): Асинхронная сессия HTTP-клиента.
- `access_token` (str): Токен доступа.

**Возвращает**:
- `str`: Идентификатор сессии.

**Исключения**:
- `Exception`: Если произошла ошибка авторизации или ошибка валидации.

**Как работает функция**:
1. Формирует заголовки запроса с токеном доступа.
2. Отправляет GET-запрос к URL создания сессии.
3. Извлекает идентификатор сессии из JSON-ответа.
4. Кэширует идентификатор сессии.

**Примеры**:

```python
# Пример создания и кэширования сессии
async with aiohttp.ClientSession() as session:
    access_token = "your_access_token"
    session_id = await RobocodersAPI._create_and_cache_session(session, access_token)
    print(f"Session ID: {session_id}")
```

### `_save_cached_data`

```python
@staticmethod
def _save_cached_data(new_data: dict):
    """Save new data to cache file"""
```

**Назначение**:
Сохраняет новые данные в файл кэша.

**Параметры**:
- `new_data` (dict): Новые данные для сохранения.

**Как работает функция**:
1. Создает директорию кэша, если она не существует.
2. Создает файл кэша, если он не существует.
3. Открывает файл кэша для записи.
4. Записывает данные в файл в формате JSON.

**Примеры**:

```python
# Пример сохранения данных в кэш
RobocodersAPI._save_cached_data({"access_token": "new_token"})
```

### `_update_cached_data`

```python
@staticmethod
def _update_cached_data(updated_data: dict):
    """Update existing cache data with new values"""
```

**Назначение**:
Обновляет существующие данные в файле кэша новыми значениями.

**Параметры**:
- `updated_data` (dict): Обновленные данные для сохранения.

**Как работает функция**:
1. Инициализирует пустой словарь для хранения данных.
2. Проверяет, существует ли файл кэша.
3. Если файл кэша существует, пытается загрузить данные из него.
4. Если файл кэша поврежден, начинает с пустого словаря.
5. Обновляет загруженные данные новыми значениями.
6. Записывает обновленные данные в файл кэша в формате JSON.

**Примеры**:

```python
# Пример обновления данных в кэше
RobocodersAPI._update_cached_data({"sid": "new_session_id"})
```

### `_clear_cached_data`

```python
@staticmethod
def _clear_cached_data():
    """Remove cache file"""
```

**Назначение**:
Удаляет файл кэша.

**Как работает функция**:
1. Проверяет, существует ли файл кэша.
2. Если файл кэша существует, пытается его удалить.
3. Ловит исключения, если возникают ошибки при удалении файла.

**Примеры**:

```python
# Пример очистки кэша
RobocodersAPI._clear_cached_data()
```

### `_get_cached_data`

```python
@staticmethod
def _get_cached_data() -> dict:
    """Get all cached data"""
```

**Назначение**:
Получает все кэшированные данные из файла.

**Возвращает**:
- `dict`: Кэшированные данные.

**Как работает функция**:
1. Проверяет, существует ли файл кэша.
2. Если файл кэша существует, пытается загрузить данные из него.
3. Если файл кэша поврежден, возвращает пустой словарь.
4. Если файл кэша не существует, возвращает пустой словарь.

**Примеры**:

```python
# Пример получения данных из кэша
cached_data = RobocodersAPI._get_cached_data()
print(cached_data)
```
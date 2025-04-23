# Microsoft Copilot

## Обзор

Модуль `Copilot.py` предоставляет реализацию доступа к Microsoft Copilot в качестве поставщика услуг для создания завершений текста. Он использует библиотеку `curl_cffi` для выполнения HTTP-запросов и WebSocket-соединений. Модуль поддерживает как стриминг ответов, так и работу с изображениями.

## Подробнее

Модуль `Copilot` интегрируется в проект `hypotez` как один из поставщиков AI-сервисов. Он обеспечивает взаимодействие с Microsoft Copilot, используя WebSocket для обмена сообщениями в реальном времени. В случае отсутствия необходимых библиотек (`curl_cffi` или `nodriver`) модуль сообщает об ошибке и предлагает установить их.

## Классы

### `Conversation`

**Описание**: Класс представляет собой разговор с Copilot и хранит идентификатор разговора.
**Наследует**: `JsonConversation`

**Атрибуты**:
- `conversation_id` (str): Уникальный идентификатор разговора.

### `Copilot`

**Описание**: Класс реализует взаимодействие с Microsoft Copilot.
**Наследует**: `AbstractProvider`, `ProviderModelMixin`

**Атрибуты**:
- `label` (str): Метка провайдера - "Microsoft Copilot".
- `url` (str): URL сервиса - "https://copilot.microsoft.com".
- `working` (bool): Указывает, что провайдер работает - `True`.
- `supports_stream` (bool): Указывает, что провайдер поддерживает потоковую передачу - `True`.
- `default_model` (str): Модель по умолчанию - "Copilot".
- `models` (list): Список поддерживаемых моделей - `["Copilot", "Think Deeper"]`.
- `model_aliases` (dict): Псевдонимы моделей.
- `websocket_url` (str): URL для WebSocket-соединения - "wss://copilot.microsoft.com/c/api/chat?api-version=2".
- `conversation_url` (str): URL для управления беседами - "https://copilot.microsoft.com/c/api/conversations".
- `_access_token` (str): Приватный атрибут для хранения токена доступа.
- `_cookies` (dict): Приватный атрибут для хранения cookie.

## Методы класса

### `create_completion`

```python
@classmethod
def create_completion(
    cls,
    model: str,
    messages: Messages,
    stream: bool = False,
    proxy: str = None,
    timeout: int = 900,
    prompt: str = None,
    media: MediaListType = None,
    conversation: BaseConversation = None,
    return_conversation: bool = False,
    api_key: str = None,
    **kwargs
) -> CreateResult:
    """ Функция выполняет запрос к Microsoft Copilot для получения завершения текста или генерации изображения.
    Args:
        model (str): Имя используемой модели.
        messages (Messages): Список сообщений для контекста беседы.
        stream (bool, optional): Флаг, указывающий, использовать ли потоковую передачу. По умолчанию `False`.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
        timeout (int, optional): Время ожидания запроса в секундах. По умолчанию `900`.
        prompt (str, optional): Текст запроса. По умолчанию `None`.
        media (MediaListType, optional): Список медиафайлов для отправки. По умолчанию `None`.
        conversation (BaseConversation, optional): Объект беседы. По умолчанию `None`.
        return_conversation (bool, optional): Флаг, указывающий, нужно ли возвращать объект беседы. По умолчанию `False`.
        api_key (str, optional): API ключ для аутентификации. По умолчанию `None`.

    Returns:
        CreateResult: Генератор, возвращающий результаты завершения текста или сгенерированные изображения.

    Raises:
        MissingRequirementsError: Если отсутствует библиотека `curl_cffi`.
        NoValidHarFileError: Если не найден валидный HAR-файл или не удалось получить токен доступа.
        MissingAuthError: Если получен статус 401 при запросе к API (невалидный токен).
        RuntimeError: Если получен некорректный ответ от Copilot.

    
    - Проверяет наличие необходимых библиотек (`curl_cffi`).
    - Определяет URL для WebSocket-соединения.
    - Устанавливает заголовки для запроса, включая токен доступа.
    - Создает или использует существующую беседу.
    - Отправляет запрос к Copilot через WebSocket.
    - Получает и обрабатывает ответы от Copilot, включая текст, изображения и предложения.
    - Возвращает результаты через генератор.
    - Вызывает исключение в случае ошибки.

    Внутренние функции: отсутствуют.

    Примеры:
    Пример 1:
    ```python
    messages = [{"role": "user", "content": "Напиши Hello World на Python"}]
    result = Copilot.create_completion(model="Copilot", messages=messages)
    for item in result:
        print(item)
    ```

    Пример 2:
    ```python
    messages = [{"role": "user", "content": "Сгенерируй изображение котика"}]
    result = Copilot.create_completion(model="Copilot", messages=messages)
    for item in result:
        print(item)
    ```
    """
    ...
```

## Функции

### `get_access_token_and_cookies`

```python
async def get_access_token_and_cookies(url: str, proxy: str = None, target: str = "ChatAI",):
    """ Функция асинхронно получает токен доступа и cookie для Copilot с использованием `nodriver`.

    Args:
        url (str): URL для получения токена и cookie.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
        target (str, optional): Целевая строка для поиска токена. По умолчанию "ChatAI".

    Returns:
        tuple[str, dict]: Токен доступа и словарь cookie.

    Raises:
        Exception: Если не удается получить токен доступа или cookie.

    
    - Запускает браузер с помощью `nodriver`.
    - Открывает указанный URL.
    - Выполняет JavaScript-код для извлечения токена доступа из localStorage.
    - Получает cookie из браузера.
    - Закрывает браузер.
    - Возвращает токен доступа и cookie.

    Примеры:
    ```python
    token, cookies = asyncio.run(get_access_token_and_cookies("https://copilot.microsoft.com"))
    print(f"Token: {token}")
    print(f"Cookies: {cookies}")
    ```
    """
    ...
```

### `readHAR`

```python
def readHAR(url: str):
    """ Функция считывает токен доступа и cookie из HAR-файлов.

    Args:
        url (str): URL для поиска HAR-файлов.

    Returns:
        tuple[str, dict]: Токен доступа и словарь cookie.

    Raises:
        NoValidHarFileError: Если не найдены HAR-файлы с токеном доступа.

    
    - Получает список HAR-файлов.
    - Читает HAR-файлы и ищет токен доступа и cookie.
    - Возвращает токен доступа и cookie.

    Примеры:
    ```python
    token, cookies = readHAR("https://copilot.microsoft.com")
    print(f"Token: {token}")
    print(f"Cookies: {cookies}")
    ```
    """
    ...
```

### `get_clarity`

```python
def get_clarity() -> bytes:
    """ Функция возвращает закодированный в base64 бинарный блок данных.

    Args:
        None

    Returns:
        bytes: Закодированные данные.

    
    - Возвращает предопределенный base64-закодированный бинарный блок данных.

    Примеры:
    ```python
    data = get_clarity()
    print(f"Data: {data}")
    ```
    """
    ...
```

## Параметры класса

- `websocket_url` (str): URL для установления WebSocket-соединения с сервером Copilot.
- `conversation_url` (str): URL для создания новых бесед с Copilot.
- `_access_token` (str): Приватный атрибут, хранящий токен доступа для аутентификации.
- `_cookies` (dict): Приватный атрибут, хранящий cookie для аутентификации.
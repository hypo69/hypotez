# Модуль `Copilot.py`

## Обзор

Модуль предоставляет класс `Copilot`, который является провайдером для взаимодействия с Microsoft Copilot. Он поддерживает потоковую передачу данных и предоставляет методы для создания запросов и обработки ответов.

## Подробнее

Этот модуль позволяет интегрировать приложение с Microsoft Copilot для выполнения различных задач, таких как генерация текста, обработка изображений и предоставление советов. Он использует библиотеку `curl_cffi` для выполнения HTTP-запросов и WebSocket-соединений.

## Классы

### `Conversation(JsonConversation)`

**Описание**: Представляет собой класс для хранения информации о текущем диалоге с Copilot.

**Наследует**: `JsonConversation`

**Атрибуты**:
- `conversation_id` (str): Уникальный идентификатор диалога.

**Методы**:
- `__init__(self, conversation_id: str)`: Конструктор класса.
    - **Назначение**: Инициализирует объект `Conversation` с заданным идентификатором диалога.
    - **Параметры**:
        - `conversation_id` (str): Идентификатор диалога.

### `Copilot(AbstractProvider, ProviderModelMixin)`

**Описание**: Класс, реализующий взаимодействие с Microsoft Copilot.

**Наследует**: `AbstractProvider`, `ProviderModelMixin`

**Атрибуты**:
- `label` (str): Метка провайдера ("Microsoft Copilot").
- `url` (str): URL-адрес Copilot ("https://copilot.microsoft.com").
- `working` (bool): Флаг, указывающий на работоспособность провайдера (True).
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи данных (True).
- `default_model` (str): Модель по умолчанию ("Copilot").
- `models` (list): Список поддерживаемых моделей (["Copilot", "Think Deeper"]).
- `model_aliases` (dict): Словарь псевдонимов моделей.
- `websocket_url` (str): URL-адрес WebSocket для обмена сообщениями ("wss://copilot.microsoft.com/c/api/chat?api-version=2").
- `conversation_url` (str): URL-адрес для управления диалогами ("https://copilot.microsoft.com/c/api/conversations").
- `_access_token` (str): Приватный атрибут для хранения токена доступа.
- `_cookies` (dict): Приватный атрибут для хранения cookie.

**Методы**:
- `create_completion(cls, model: str, messages: Messages, stream: bool = False, proxy: str = None, timeout: int = 900, prompt: str = None, media: MediaListType = None, conversation: BaseConversation = None, return_conversation: bool = False, api_key: str = None, **kwargs) -> CreateResult`

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
    """
    Создает запрос к Copilot и обрабатывает ответ.

    Args:
        model (str): Используемая модель.
        messages (Messages): Список сообщений для отправки.
        stream (bool, optional): Флаг потоковой передачи данных. По умолчанию False.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию None.
        timeout (int, optional): Время ожидания запроса. По умолчанию 900.
        prompt (str, optional): Текст запроса. По умолчанию None.
        media (MediaListType, optional): Список медиафайлов для отправки. По умолчанию None.
        conversation (BaseConversation, optional): Объект диалога. По умолчанию None.
        return_conversation (bool, optional): Флаг возврата объекта диалога. По умолчанию False.
        api_key (str, optional): API-ключ для аутентификации. По умолчанию None.
        **kwargs: Дополнительные параметры.

    Yields:
        CreateResult: Результат запроса. Может возвращать как текст, так и медиа-контент.

    Raises:
        MissingRequirementsError: Если не установлена библиотека `curl_cffi`.
        NoValidHarFileError: Если не найден файл HAR с токеном доступа.
        MissingAuthError: Если отсутствует токен доступа или произошла ошибка аутентификации.
        RuntimeError: Если получен некорректный ответ от Copilot.

    Как работает функция:
    - Проверяет наличие необходимых библиотек (curl_cffi).
    - Получает или обновляет токен доступа и cookie.
    - Создает или использует существующий диалог с Copilot.
    - Отправляет запрос с текстом и медиафайлами через WebSocket.
    - Обрабатывает ответы от Copilot, включая текст, изображения и предложения.
    - Возвращает результаты в виде потока данных.

    Примеры:
    Пример 1: Отправка текстового запроса без потоковой передачи данных.
    >>> Copilot.create_completion(model='Copilot', messages=[{'role': 'user', 'content': 'Hello'}])

    Пример 2: Отправка запроса с потоковой передачей данных.
    >>> Copilot.create_completion(model='Think Deeper', messages=[{'role': 'user', 'content': 'Tell me a story'}], stream=True)

    Пример 3: Отправка запроса с использованием прокси-сервера.
    >>> Copilot.create_completion(model='Copilot', messages=[{'role': 'user', 'content': 'What is the weather today?'}], proxy='http://proxy.example.com:8080')

    Пример 4: Отправка запроса с медиафайлом.
    >>> Copilot.create_completion(model='Copilot', messages=[{'role': 'user', 'content': 'Describe this image'}], media=[{'type': 'image', 'data': b'...'}]
    """
    ...
```

## Вспомогательные функции

### `get_access_token_and_cookies`

```python
async def get_access_token_and_cookies(url: str, proxy: str = None, target: str = "ChatAI") -> tuple[str, dict]:
    """
    Асинхронно получает токен доступа и cookie из браузера.

    Args:
        url (str): URL-адрес для получения токена и cookie.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию None.
        target (str, optional): Цель поиска токена. По умолчанию "ChatAI".

    Returns:
        tuple[str, dict]: Кортеж, содержащий токен доступа и словарь cookie.

    Как работает функция:
    - Запускает браузер с использованием `nodriver`.
    - Переходит на указанный URL.
    - Извлекает токен доступа из локального хранилища браузера.
    - Получает cookie для данного URL.
    - Закрывает страницу и останавливает браузер.

    Примеры:
    Пример 1: Получение токена доступа и cookie без использования прокси.
    >>> asyncio.run(get_access_token_and_cookies(url='https://copilot.microsoft.com'))

    Пример 2: Получение токена доступа и cookie с использованием прокси.
    >>> asyncio.run(get_access_token_and_cookies(url='https://copilot.microsoft.com', proxy='http://proxy.example.com:8080'))
    """
    ...
```

### `readHAR`

```python
def readHAR(url: str) -> tuple[str, dict]:
    """
    Читает токен доступа и cookie из HAR-файлов.

    Args:
        url (str): URL-адрес для поиска в HAR-файлах.

    Returns:
        tuple[str, dict]: Кортеж, содержащий токен доступа и словарь cookie.

    Raises:
        NoValidHarFileError: Если не найдены HAR-файлы с токеном доступа.

    Как работает функция:
    - Ищет HAR-файлы в известных местах.
    - Читает содержимое каждого HAR-файла.
    - Извлекает токен доступа и cookie, если они есть в файле.

    Примеры:
    Пример 1: Чтение токена доступа и cookie из HAR-файлов.
    >>> readHAR(url='https://copilot.microsoft.com')
    """
    ...
```

### `get_clarity`

```python
def get_clarity() -> bytes:
    """
    Возвращает тело запроса для Clarity.

    Returns:
        bytes: Тело запроса в виде байтов.

    Как работает функция:
    - Возвращает base64-декодированное тело запроса Clarity.

    Примеры:
    Пример 1: Получение тела запроса Clarity.
    >>> get_clarity()
    """
    ...
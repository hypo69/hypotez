# Модуль для работы с провайдером Vercel

## Обзор

Модуль предоставляет интерфейс для взаимодействия с моделями, размещенными на платформе Vercel. Он включает в себя функции для получения токена аутентификации, формирования запросов к API Vercel и генерации текста на основе выбранной модели и входных параметров.

## Подробней

Модуль содержит класс `Client`, который инкапсулирует логику взаимодействия с API Vercel, включая аутентификацию и отправку запросов. Также в модуле определены списки поддерживаемых моделей и их параметры, используемые для формирования запросов к API.

## Классы

### `Client`

**Описание**: Класс `Client` предоставляет методы для взаимодействия с API Vercel.

**Атрибуты**:
- `session`: Объект `requests.Session` для выполнения HTTP-запросов с сохранением сессии.
- `headers`: Словарь HTTP-заголовков, используемых в запросах.

**Методы**:
- `__init__()`: Инициализирует объект класса `Client` и устанавливает HTTP-заголовки.
- `get_token()`: Получает токен аутентификации для доступа к API Vercel.
- `get_default_params(model_id: str) -> dict`: Возвращает словарь параметров по умолчанию для указанной модели.
- `generate(model_id: str, prompt: str, params: dict = {}) -> Generator[str, None, None]`: Генерирует текст на основе указанной модели и промпта.

#### `__init__`
```python
def __init__(self):
    """
    Инициализирует клиентский сеанс и устанавливает заголовки.

    Args:
        self (Client): Экземпляр класса Client.

    Returns:
        None
    """
    ...
```
    **Назначение**: Конструктор класса `Client`. Инициализирует сессию `requests.Session()` и устанавливает заголовки `headers` для последующих HTTP-запросов.

    **Как работает функция**:
    - Создает экземпляр `requests.Session()` и сохраняет его в атрибуте `session`.
    - Определяет словарь `headers`, содержащий User-Agent, Accept, Accept-Encoding, Accept-Language, Te и Upgrade-Insecure-Requests.
    - Обновляет заголовки сессии, используя `self.session.headers.update(self.headers)`.

#### `get_token`
```python
def get_token(self) -> str:
    """
    Получает токен аутентификации для доступа к API Vercel.

    Args:
        self (Client): Экземпляр класса Client.

    Returns:
        str: Токен аутентификации в формате base64.
    """
    ...
```
    **Назначение**: Метод `get_token` получает токен аутентификации, необходимый для доступа к API Vercel.

    **Как работает функция**:
    1.  Выполняет GET-запрос к `https://sdk.vercel.ai/openai.jpeg`, чтобы получить base64-encoded JSON.
    2.  Декодирует полученную строку из base64 в JSON.
    3.  Извлекает значения `c` и `a` из JSON.
    4.  Формирует JavaScript-код, используя полученные значения.
    5.  Выполняет JavaScript-код с помощью `execjs.compile(code).call('token')`, чтобы получить токен.
    6.  Формирует JSON-объект с ключами `r` (токен) и `t` (значение из исходного JSON).
    7.  Кодирует полученный JSON-объект в base64 и возвращает результат.

    **Примеры**:
    ```python
    client = Client()
    token = client.get_token()
    print(token)
    ```

#### `get_default_params`
```python
def get_default_params(self, model_id: str) -> dict:
    """
    Извлекает параметры по умолчанию для заданной модели из словаря vercel_models.

    Args:
        self (Client): Экземпляр класса Client.
        model_id (str): Идентификатор модели.

    Returns:
        dict: Словарь параметров по умолчанию для указанной модели.
    """
    ...
```
    **Назначение**: Метод `get_default_params` извлекает параметры по умолчанию для заданной модели из словаря `vercel_models`.

    **Как работает функция**:
    1.  Получает словарь параметров из `vercel_models` для указанного `model_id`.
    2.  Формирует новый словарь, где ключи — имена параметров, а значения — значения параметров.

    **Примеры**:
    ```python
    client = Client()
    default_params = client.get_default_params('anthropic:claude-instant-v1')
    print(default_params)
    ```

#### `generate`
```python
def generate(self, model_id: str, prompt: str, params: dict = {}) -> Generator[str, None, None]:
    """
    Генерирует текст на основе указанной модели и промпта.

    Args:
        self (Client): Экземпляр класса Client.
        model_id (str): Идентификатор модели.
        prompt (str): Входной текст для генерации.
        params (dict, optional): Дополнительные параметры для модели. По умолчанию {}.

    Yields:
        str: Части сгенерированного текста.
    """
    ...
```
    **Назначение**: Метод `generate` генерирует текст на основе указанной модели и входного запроса (prompt).

    **Как работает функция**:
    1.  Определяет `model_id`, используя словарь `models`, если `model_id` не содержит `:`.
    2.  Получает параметры по умолчанию для `model_id`, используя метод `self.get_default_params(model_id)`.
    3.  Формирует `payload`, объединяя параметры по умолчанию, переданные параметры и `prompt`.
    4.  Получает токен, используя метод `self.get_token()`.
    5.  Формирует заголовки `headers` для запроса.
    6.  Использует `queue.Queue()` для асинхронной обработки чанков текста.
    7.  Определяет функцию `callback(data)`, которая помещает декодированные чанки текста в очередь `chunks_queue`.
    8.  Определяет функцию `request_thread()`, которая отправляет POST-запрос к `https://sdk.vercel.ai/api/generate` и обрабатывает ответ с использованием `content_callback=callback`.
    9.  Запускает `request_thread()` в отдельном потоке.
    10. Читает данные из `chunks_queue` и генерирует (`yield`) каждый полученный чанк текста.

    **Примеры**:
    ```python
    client = Client()
    completion = client.generate('gpt-3.5-turbo', 'Translate to English: Je t\'aime.')
    for token in completion:
        print(token)
    ```

## Функции

### `_create_completion`
```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs) -> Generator[str, None, None]:
    """
    Создает завершение текста на основе указанной модели и списка сообщений.

    Args:
        model (str): Идентификатор модели.
        messages (list): Список сообщений для генерации текста.
        stream (bool): Признак потоковой передачи данных.
        **kwargs: Дополнительные параметры.

    Yields:
        str: Части сгенерированного текста.
    """
    ...
```
    **Назначение**: Функция `_create_completion` генерирует текст на основе указанной модели и списка сообщений.

    **Как работает функция**:
    1.  Возвращает сообщение `'Vercel is currently not working.'`. Это означает, что в текущей версии код не работает с Vercel.
    2.  Формирует строку `conversation` из списка сообщений, где каждое сообщение добавляется в формате `role: content`.
    3.  Добавляет префикс `assistant: ` к строке `conversation`.
    4.  Использует класс `Client` для генерации завершения текста, вызывая метод `Client().generate(model, conversation)`.
    5.  Генерирует каждый токен, полученный от `Client().generate(model, conversation)`.

    **Примеры**:
    ```python
    model = 'gpt-3.5-turbo'
    messages = [{'role': 'user', 'content': 'Translate to English: Je t\'aime.'}]
    stream = True

    for token in _create_completion(model, messages, stream):
        print(token)
    ```

## Параметры

- `url`: URL-адрес API Vercel.
- `supports_stream`: Флаг, указывающий на поддержку потоковой передачи данных.
- `needs_auth`: Флаг, указывающий на необходимость аутентификации.
- `models`: Список поддерживаемых моделей.
- `vercel_models`: Подробное описание параметров для каждой модели, включая минимальный уровень биллинга, температурные режимы и прочее.

## Переменные

- `params`: Строка, содержащая информацию о поддерживаемых параметрах для функции `_create_completion`.
```python
params: str
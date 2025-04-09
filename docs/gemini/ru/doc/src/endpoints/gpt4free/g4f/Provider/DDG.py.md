# Модуль `DDG.py`

## Обзор

Модуль `DDG.py` предоставляет асинхронный интерфейс для взаимодействия с чат-ботом DuckDuckGo AI. Он включает в себя функциональность для установления соединения, обмена сообщениями и обработки ответов в режиме реального времени. Модуль поддерживает различные модели, такие как `gpt-4o-mini`, `meta-llama/Llama-3.3-70B-Instruct-Turbo`, `claude-3-haiku-20240307`, `o3-mini` и `mistralai/Mistral-Small-24B-Instruct-2501`.

## Подробнее

Модуль предназначен для интеграции в проекты, требующие взаимодействия с AI-ассистентом DuckDuckGo. Он обеспечивает удобный способ отправки запросов и получения ответов, а также поддерживает управление состоянием разговора (conversation).

## Классы

### `DuckDuckGoSearchException`

**Описание**: Базовый класс исключений для модуля `duckduckgo_search`.

### `Conversation`

**Описание**: Класс для представления состояния разговора с DuckDuckGo AI.

**Наследует**:
- `JsonConversation`

**Атрибуты**:
- `vqd` (str): VQD токен для текущей сессии.
- `vqd_hash_1` (str): VQD хэш для текущей сессии.
- `message_history` (Messages): История сообщений в разговоре.
- `cookies` (dict): Куки для текущей сессии.
- `fe_version` (str): Версия фронтенда, используемая для запросов.
- `model` (str): Модель, используемая в разговоре.

**Методы**:
- `__init__(model: str)`: Инициализирует экземпляр класса `Conversation`.

### `DDG`

**Описание**: Класс, предоставляющий асинхронный интерфейс для взаимодействия с чат-ботом DuckDuckGo AI.

**Наследует**:
- `AsyncGeneratorProvider`
- `ProviderModelMixin`

**Атрибуты**:
- `label` (str): Метка провайдера, `"DuckDuckGo AI Chat"`.
- `url` (str): URL для доступа к DuckDuckGo AI Chat, `"https://duckduckgo.com/aichat"`.
- `api_endpoint` (str): URL для API чата DuckDuckGo, `"https://duckduckgo.com/duckchat/v1/chat"`.
- `status_url` (str): URL для получения статуса DuckDuckGo AI, `"https://duckduckgo.com/duckchat/v1/status"`.
- `working` (bool): Флаг, указывающий на работоспособность провайдера, `True`.
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи данных, `True`.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений, `True`.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений, `True`.
- `default_model` (str): Модель по умолчанию, `"gpt-4o-mini"`.
- `models` (list[str]): Список поддерживаемых моделей.
- `model_aliases` (dict[str, str]): Псевдонимы моделей для удобства использования.
- `last_request_time` (float): Время последнего запроса.
- `max_retries` (int): Максимальное количество повторных попыток при запросе.
- `base_delay` (int): Базовая задержка между повторными попытками.
- `_chat_xfe` (str): версия DuckDuckGo AI Chat.

**Методы**:
- `sha256_base64(text: str) -> str`: Возвращает base64-представление SHA256-хеша текста.
- `parse_dom_fingerprint(js_text: str) -> str`: Извлекает отпечаток DOM из JavaScript кода.
- `parse_server_hashes(js_text: str) -> list`: Извлекает хеши сервера из JavaScript кода.
- `build_x_vqd_hash_1(vqd_hash_1: str, headers: dict) -> str`: Создает заголовок `x-vqd-hash-1` на основе предоставленных данных.
- `validate_model(model: str) -> str`: Проверяет и возвращает корректное имя модели.
- `sleep(multiplier: float = 1.0)`: Реализует ограничение скорости запросов.
- `get_default_cookies(session: ClientSession) -> dict`: Получает куки по умолчанию, необходимые для API-запросов.
- `fetch_fe_version(session: ClientSession) -> str`: Получает версию фронтенда (`fe-version`) со страницы.
- `fetch_vqd_and_hash(session: ClientSession, retry_count: int = 0) -> tuple[str, str]`: Получает VQD токен и хеш для сессии чата с повторными попытками.
- `create_async_generator(...) -> AsyncResult`: Создает асинхронный генератор для взаимодействия с чат-ботом DuckDuckGo AI.

## Функции

### `sha256_base64`

```python
@staticmethod
def sha256_base64(text: str) -> str:
    """Return the base64 encoding of the SHA256 digest of the text."""
    sha256_hash = hashlib.sha256(text.encode("utf-8")).digest()
    return base64.b64encode(sha256_hash).decode()
```

**Назначение**: Вычисляет SHA256-хеш заданной строки и возвращает его base64-представление.

**Параметры**:
- `text` (str): Строка для хеширования.

**Возвращает**:
- `str`: Base64-представление SHA256-хеша.

**Как работает функция**:

1.  Кодирует входную строку `text` в байты, используя кодировку UTF-8.
2.  Вычисляет SHA256-хеш полученных байтов.
3.  Кодирует полученный хеш в base64.
4.  Декодирует base64-представление в строку UTF-8 и возвращает его.

```
Текст -> SHA256 хеш -> Base64 кодирование -> Строка
```

**Примеры**:

```python
text = "example"
result = DDG.sha256_base64(text)
print(result)  # Вывод: rnuN87xbWTjEY6diutH+iYcjo1m1EdKrqQD5Qm4NuGg=
```

### `parse_dom_fingerprint`

```python
@staticmethod
def parse_dom_fingerprint(js_text: str) -> str:
    """ """
    if not has_bs4:
        # Fallback if BeautifulSoup is not available
        return "1000"
    
    try:
        html_snippet = js_text.split("e.innerHTML = \'")[1].split("\';")[0]
        offset_value = js_text.split("return String(")[1].split(" ")[0]
        soup = BeautifulSoup(html_snippet, "html.parser")
        corrected_inner_html = soup.body.decode_contents()
        inner_html_length = len(corrected_inner_html)
        fingerprint = int(offset_value) + inner_html_length
        return str(fingerprint)
    except Exception:
        # Return a fallback value if parsing fails
        return "1000"
```

**Назначение**: Извлекает "отпечаток" DOM из JavaScript-кода, используя BeautifulSoup для парсинга HTML. Если BeautifulSoup недоступен, возвращает `"1000"`.

**Параметры**:
- `js_text` (str): JavaScript-код, содержащий HTML-фрагмент и значение смещения.

**Возвращает**:
- `str`: Строковое представление "отпечатка" DOM.

**Как работает функция**:

1. Проверяет, установлен ли BeautifulSoup (`has_bs4`). Если нет, возвращает `"1000"`.
2. Извлекает HTML-фрагмент из `js_text`, разделяя строку по `"e.innerHTML = '"` и `";"`.
3. Извлекает значение смещения из `js_text`, разделяя строку по `"return String("` и `" "`.
4. Создает объект BeautifulSoup из HTML-фрагмента.
5. Извлекает содержимое тега `body` и вычисляет его длину.
6. Складывает значение смещения и длину содержимого `body`, преобразует результат в строку и возвращает его.
7. В случае возникновения исключения на любом этапе возвращает `"1000"`.

```
Проверка BeautifulSoup -> Извлечение HTML -> Извлечение смещения -> Парсинг HTML -> Вычисление длины -> Вычисление отпечатка -> Строка
```

**Примеры**:

```python
js_text = "e.innerHTML = '<div class=\"test\">Test</div>';" \
          "return String(100) "
result = DDG.parse_dom_fingerprint(js_text)
print(result)  # Вывод: 124
```

### `parse_server_hashes`

```python
@staticmethod
def parse_server_hashes(js_text: str) -> list:
    try:
        return js_text.split('server_hashes: ["', maxsplit=1)[1].split('"]', maxsplit=1)[0].split('","')
    except Exception:
        # Return a fallback value if parsing fails
        return ["1", "2"]
```

**Назначение**: Извлекает список хешей сервера из JavaScript-кода. Если извлечение не удается, возвращает `["1", "2"]`.

**Параметры**:
- `js_text` (str): JavaScript-код, содержащий список хешей сервера.

**Возвращает**:
- `list`: Список хешей сервера.

**Как работает функция**:

1. Пытается извлечь список хешей, разделяя `js_text` по строкам `'server_hashes: ["'`, `'"]'` и `'","'`.
2. Если извлечение не удается, возвращает `["1", "2"]`.

```
Извлечение хешей -> Список хешей
```

**Примеры**:

```python
js_text = 'server_hashes: ["hash1","hash2"]'
result = DDG.parse_server_hashes(js_text)
print(result)  # Вывод: ['hash1', 'hash2']
```

### `build_x_vqd_hash_1`

```python
@classmethod
def build_x_vqd_hash_1(cls, vqd_hash_1: str, headers: dict) -> str:
    """Build the x-vqd-hash-1 header value."""
    try:
        decoded = base64.b64decode(vqd_hash_1).decode()
        server_hashes = cls.parse_server_hashes(decoded)
        dom_fingerprint = cls.parse_dom_fingerprint(decoded)

        ua_fingerprint = headers.get("User-Agent", "") + headers.get("sec-ch-ua", "")
        ua_hash = cls.sha256_base64(ua_fingerprint)
        dom_hash = cls.sha256_base64(dom_fingerprint)

        final_result = {
            "server_hashes": server_hashes,
            "client_hashes": [ua_hash, dom_hash],
            "signals": {},
        }
        base64_final_result = base64.b64encode(json.dumps(final_result).encode()).decode()
        return base64_final_result
    except Exception as e:
        # If anything fails, return an empty string
        return ""
```

**Назначение**: Строит значение заголовка `x-vqd-hash-1` на основе предоставленных данных.

**Параметры**:
- `vqd_hash_1` (str): Base64-представление данных для построения хеша.
- `headers` (dict): Словарь HTTP-заголовков.

**Возвращает**:
- `str`: Значение заголовка `x-vqd-hash-1`.

**Как работает функция**:

1.  Декодирует `vqd_hash_1` из base64 в строку.
2.  Извлекает хеши сервера и отпечаток DOM.
3.  Создает отпечаток пользовательского агента (UA).
4.  Вычисляет SHA256-хеши для UA и отпечатка DOM.
5.  Формирует структуру данных, содержащую хеши сервера и клиента.
6.  Кодирует структуру данных в JSON и затем в base64.
7.  Возвращает полученное base64-представление.
8.  В случае возникновения исключения на любом этапе возвращает пустую строку.

```
Декодирование vqd_hash_1 -> Извлечение хешей сервера -> Извлечение отпечатка DOM -> Создание отпечатка UA -> Вычисление хешей -> Формирование структуры данных -> JSON кодирование -> Base64 кодирование -> Строка
```

**Примеры**:

```python
vqd_hash_1 = "some_base64_encoded_string"
headers = {"User-Agent": "Mozilla/5.0", "sec-ch-ua": '"Chromium";v="133"'}
result = DDG.build_x_vqd_hash_1(vqd_hash_1, headers)
print(result)  # Вывод: base64 encoded result or ""
```

### `validate_model`

```python
@classmethod
def validate_model(cls, model: str) -> str:
    """Validates and returns the correct model name"""
    if not model:
        return cls.default_model
    if model in cls.model_aliases:
        model = cls.model_aliases[model]
    if model not in cls.models:
        raise ModelNotSupportedError(f"Model {model} not supported. Available models: {cls.models}")
    return model
```

**Назначение**: Проверяет и возвращает корректное имя модели.

**Параметры**:
- `model` (str): Имя модели для валидации.

**Возвращает**:
- `str`: Корректное имя модели.

**Вызывает исключения**:
- `ModelNotSupportedError`: Если указанная модель не поддерживается.

**Как работает функция**:

1. Если `model` не указана, возвращает модель по умолчанию (`cls.default_model`).
2. Если `model` есть в `cls.model_aliases`, заменяет ее на соответствующий псевдоним.
3. Если `model` нет в списке поддерживаемых моделей (`cls.models`), вызывает исключение `ModelNotSupportedError`.
4. Возвращает проверенное имя модели.

```
Проверка наличия модели -> Замена псевдонима -> Проверка поддержки -> Возврат модели
```

**Примеры**:

```python
model = "gpt-4"
result = DDG.validate_model(model)
print(result)  # Вывод: gpt-4o-mini

model = "unsupported_model"
# Вызов DDG.validate_model(model) вызовет ModelNotSupportedError
```

### `sleep`

```python
@classmethod
async def sleep(cls, multiplier=1.0):
    """Implements rate limiting between requests"""
    now = time.time()
    if cls.last_request_time > 0:
        delay = max(0.0, 1.5 - (now - cls.last_request_time)) * multiplier
        if delay > 0:
            await asyncio.sleep(delay)
    cls.last_request_time = time.time()
```

**Назначение**: Реализует ограничение скорости запросов, чтобы не превышать лимиты API.

**Параметры**:
- `multiplier` (float, optional): Множитель для корректировки времени задержки. По умолчанию `1.0`.

**Как работает функция**:

1.  Получает текущее время.
2.  Если `cls.last_request_time` больше 0 (то есть, уже был выполнен хотя бы один запрос), вычисляет задержку как `max(0.0, 1.5 - (now - cls.last_request_time)) * multiplier`.
3.  Если вычисленная задержка больше 0, вызывает `asyncio.sleep` для приостановки выполнения на это время.
4.  Обновляет `cls.last_request_time` текущим временем.

```
Получение текущего времени -> Вычисление задержки -> Приостановка выполнения -> Обновление времени последнего запроса
```

**Примеры**:

```python
await DDG.sleep()  # Задержка с множителем по умолчанию 1.0
await DDG.sleep(multiplier=0.5)  # Задержка с множителем 0.5
```

### `get_default_cookies`

```python
@classmethod
async def get_default_cookies(cls, session: ClientSession) -> dict:
    """Obtains default cookies needed for API requests"""
    try:
        await cls.sleep()
        # Make initial request to get cookies
        async with session.get(cls.url) as response:
            # We also manually set required cookies
            cookies = {}
            cookies_dict = {'dcs': '1', 'dcm': '3'}
            
            for name, value in cookies_dict.items():
                cookies[name] = value
                url_obj = URL(cls.url)
                session.cookie_jar.update_cookies({name: value}, url_obj)
            
            return cookies
    except Exception as e:
        return {}
```

**Назначение**: Получает куки по умолчанию, необходимые для API-запросов.

**Параметры**:
- `session` (ClientSession): Асинхронная клиентская сессия.

**Возвращает**:
- `dict`: Словарь с куки.

**Как работает функция**:

1.  Вызывает `await cls.sleep()` для ограничения скорости запросов.
2.  Выполняет GET-запрос к `cls.url` для получения куки.
3.  Устанавливает необходимые куки вручную (`dcs` и `dcm`).
4.  Возвращает словарь с установленными куки.
5.  В случае ошибки возвращает пустой словарь.

```
Ограничение скорости -> GET-запрос -> Установка куки -> Возврат куки
```

**Примеры**:

```python
async with ClientSession() as session:
    cookies = await DDG.get_default_cookies(session)
    print(cookies)  # Вывод: {'dcs': '1', 'dcm': '3'}
```

### `fetch_fe_version`

```python
@classmethod
async def fetch_fe_version(cls, session: ClientSession) -> str:
    """Fetches the fe-version from the initial page load."""
    if cls._chat_xfe:
        return cls._chat_xfe
        
    try:
        url = "https://duckduckgo.com/?q=DuckDuckGo+AI+Chat&ia=chat&duckai=1"
        await cls.sleep()
        async with session.get(url) as response:
            await raise_for_status(response)
            content = await response.text()
            
            # Extract x-fe-version components
            try:
                xfe1 = content.split('__DDG_BE_VERSION__="', 1)[1].split('"', 1)[0]
                xfe2 = content.split('__DDG_FE_CHAT_HASH__="', 1)[1].split('"', 1)[0]
                cls._chat_xfe = f"{xfe1}-{xfe2}"
                return cls._chat_xfe
            except Exception:
                # If extraction fails, return an empty string
                return ""
    except Exception:
        return ""
```

**Назначение**: Получает версию фронтенда (`fe-version`) со страницы.

**Параметры**:
- `session` (ClientSession): Асинхронная клиентская сессия.

**Возвращает**:
- `str`: Версия фронтенда.

**Как работает функция**:

1.  Если `cls._chat_xfe` уже установлено, возвращает его.
2.  Выполняет GET-запрос к указанному URL.
3.  Извлекает компоненты версии из содержимого страницы.
4.  Формирует полную версию и возвращает её.
5.  В случае ошибки возвращает пустую строку.

```
Проверка наличия версии -> GET-запрос -> Извлечение компонентов -> Формирование версии -> Возврат версии
```

**Примеры**:

```python
async with ClientSession() as session:
    fe_version = await DDG.fetch_fe_version(session)
    print(fe_version)  # Вывод: версия фронтенда или ""
```

### `fetch_vqd_and_hash`

```python
@classmethod
async def fetch_vqd_and_hash(cls, session: ClientSession, retry_count: int = 0) -> tuple[str, str]:
    """Fetches the required VQD token and hash for the chat session with retries."""
    headers = {
        "accept": "text/event-stream",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/json", 
        "pragma": "no-cache",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "origin": "https://duckduckgo.com",
        "referer": "https://duckduckgo.com/",
        "x-vqd-accept": "1",
    }

    # Make sure we have cookies first
    if len(session.cookie_jar) == 0:
        await cls.get_default_cookies(session)

    try:
        await cls.sleep(multiplier=1.0 + retry_count * 0.5)
        async with session.get(cls.status_url, headers=headers) as response:
            await raise_for_status(response)
            
            vqd = response.headers.get("x-vqd-4", "")
            vqd_hash_1 = response.headers.get("x-vqd-hash-1", "")
            
            if vqd:
                # Return the fetched vqd and vqd_hash_1
                return vqd, vqd_hash_1
            
            response_text = await response.text()
            raise RuntimeError(f"Failed to fetch VQD token and hash: {response.status} {response_text}")
            
    except Exception as e:
        if retry_count < cls.max_retries:
            wait_time = cls.base_delay * (2 ** retry_count) * (1 + random.random())
            await asyncio.sleep(wait_time)
            return await cls.fetch_vqd_and_hash(session, retry_count + 1)
        else:
            raise RuntimeError(f"Failed to fetch VQD token and hash after {cls.max_retries} attempts: {str(e)}")
```

**Назначение**: Получает VQD токен и хеш для сессии чата с повторными попытками.

**Параметры**:
- `session` (ClientSession): Асинхронная клиентская сессия.
- `retry_count` (int, optional): Количество повторных попыток. По умолчанию `0`.

**Возвращает**:
- `tuple[str, str]`: Кортеж, содержащий VQD токен и хеш.

**Вызывает исключения**:
- `RuntimeError`: Если не удается получить VQD токен и хеш после нескольких попыток.

**Как работает функция**:

1.  Устанавливает заголовки запроса.
2.  Проверяет наличие куки и получает их при необходимости.
3.  Выполняет GET-запрос к `cls.status_url`.
4.  Извлекает VQD токен и хеш из заголовков ответа.
5.  Если токен получен, возвращает его вместе с хешем.
6.  В случае ошибки повторяет попытку, пока не будет достигнуто максимальное количество повторов.
7.  Если после нескольких попыток не удается получить токен, вызывает исключение.

```
Установка заголовков -> Проверка куки -> GET-запрос -> Извлечение токена и хеша -> Повторные попытки -> Возврат результата
```

**Примеры**:

```python
async with ClientSession() as session:
    vqd, vqd_hash = await DDG.fetch_vqd_and_hash(session)
    print(vqd, vqd_hash)  # Вывод: VQD токен и хеш
```

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    timeout: int = 60,
    cookies: Cookies = None,
    conversation: Conversation = None,
    return_conversation: bool = False,
    **kwargs
) -> AsyncResult:
    """ """
    model = cls.validate_model(model)
    retry_count = 0

    while retry_count <= cls.max_retries:
        try:
            session_timeout = ClientTimeout(total=timeout)
            async with ClientSession(timeout=session_timeout, cookies=cookies) as session:
                # Step 1: Ensure we have the fe_version
                if not cls._chat_xfe:
                    cls._chat_xfe = await cls.fetch_fe_version(session)
                
                # Step 2: Initialize or update conversation
                if conversation is None:
                    # Get initial cookies if not provided
                    if not cookies:
                        await cls.get_default_cookies(session)
                    
                    # Create a new conversation
                    conversation = Conversation(model)
                    conversation.fe_version = cls._chat_xfe
                    
                    # Step 3: Get VQD tokens
                    vqd, vqd_hash_1 = await cls.fetch_vqd_and_hash(session)
                    conversation.vqd = vqd
                    conversation.vqd_hash_1 = vqd_hash_1
                    conversation.message_history = [{"role": "user", "content": format_prompt(messages)}]\n                else:\n                    # Update existing conversation with new message\n                    last_message = get_last_user_message(messages.copy())\n                    conversation.message_history.append({"role": "user", "content": last_message})\n                \n                # Step 4: Prepare headers - IMPORTANT: send empty x-vqd-hash-1 for the first request\n                headers = {\n                    "accept": "text/event-stream",\n                    "accept-language": "en-US,en;q=0.9",\n                    "content-type": "application/json",\n                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",\n                    "origin": "https://duckduckgo.com",\n                    "referer": "https://duckduckgo.com/",\n                    "sec-ch-ua": \'"Chromium";v="133", "Not_A Brand";v="8"\'\n                    "x-fe-version": conversation.fe_version or cls._chat_xfe,\n                    "x-vqd-4": conversation.vqd,\n                    "x-vqd-hash-1": "",  # Send empty string initially\n                }\n\n                # Step 5: Prepare the request data\n                data = {\n                    "model": model,\n                    "messages": conversation.message_history,\n                }\n\n                # Step 6: Send the request\n                await cls.sleep(multiplier=1.0 + retry_count * 0.5)\n                async with session.post(cls.api_endpoint, json=data, headers=headers, proxy=proxy) as response:\n                    # Handle 429 errors specifically\n                    if response.status == 429:\n                        response_text = await response.text()\n                        \n                        if retry_count < cls.max_retries:\n                            retry_count += 1\n                            wait_time = cls.base_delay * (2 ** retry_count) * (1 + random.random())\n                            await asyncio.sleep(wait_time)\n                            \n                            # Get fresh tokens and cookies\n                            cookies = await cls.get_default_cookies(session)\n                            continue\n                        else:\n                            raise RateLimitError(f"Rate limited after {cls.max_retries} retries")\n                    \n                    await raise_for_status(response)\n                    reason = None\n                    full_message = ""\n\n                    # Step 7: Process the streaming response\n                    async for line in response.content:\n                        line = line.decode("utf-8").strip()\n\n                        if line.startswith("data:"):\n                            try:\n                                message = json.loads(line[5:].strip())\n                            except json.JSONDecodeError:\n                                continue\n\n                            if "action" in message and message["action"] == "error":\n                                error_type = message.get("type", "")\n                                if message.get("status") == 429:\n                                    if error_type == "ERR_CONVERSATION_LIMIT":\n                                        raise ConversationLimitError(error_type)\n                                    raise RateLimitError(error_type)\n                                raise DuckDuckGoSearchException(error_type)\n\n                            if "message" in message:\n                                if message["message"]:\n                                    yield message["message"]\n                                    full_message += message["message"]\n                                    reason = "length"\n                                else:\n                                    reason = "stop"\n\n                    # Step 8: Update conversation with response information\n                    if return_conversation:\n                        conversation.message_history.append({"role": "assistant", "content": full_message})\n                        # Update tokens from response headers\n                        conversation.vqd = response.headers.get("x-vqd-4", conversation.vqd)\n                        conversation.vqd_hash_1 = response.headers.get("x-vqd-hash-1", conversation.vqd_hash_1)\n                        conversation.cookies = {\n                            n: c.value \n                            for n, c in session.cookie_jar.filter_cookies(URL(cls.url)).items()\n                        }\n                        yield conversation\n\n                    if reason is not None:\n                        yield FinishReason(reason)\n                    \n                    # If we got here, the request was successful\n                    break\n\n        except (RateLimitError, ResponseStatusError) as e:\n            if "429" in str(e) and retry_count < cls.max_retries:\n                retry_count += 1\n                wait_time = cls.base_delay * (2 ** retry_count) * (1 + random.random())\n                await asyncio.sleep(wait_time)\n            else:\n                raise\n        except asyncio.TimeoutError as e:\n            raise TimeoutError(f"Request timed out: {str(e)}")\n        except Exception as e:\n            raise
```

**Назначение**: Создает асинхронный генератор для взаимодействия с чат-ботом DuckDuckGo AI.

**Параметры**:
- `model` (str): Имя модели.
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `timeout` (int, optional): Время ожидания запроса в секундах. По умолчанию `60`.
- `cookies` (Cookies, optional): Куки для использования в сессии. По умолчанию `None`.
- `conversation` (Conversation, optional): Объект разговора для продолжения сессии. По умолчанию `None`.
- `return_conversation` (bool, optional): Флаг, указывающий, нужно ли возвращать объект разговора. По умолчанию `False`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий ответы от чат-бота.

**Вызывает исключения**:
- `ModelNotSupportedError`: Если указанная модель не поддерживается.
- `RateLimitError`: Если превышен лимит запросов.
- `TimeoutError`: Если время ожидания запроса истекло.
- `DuckDuckGoSearchException`: При возникновении ошибки при обработке ответа.
- `ConversationLimitError`: Если превышен лимит разговоров.

**Как работает функция**:

1.  Проверяет и валидирует имя модели.
2.  Инициализирует асинхронную клиентскую сессию.
3.  Получает версию фронтенда (`fe_version`).
4.  Если объект разговора не предоставлен, создает новый и получает VQD токен и хеш.
5.  Подготавливает заголовки запроса.
6.  Формирует данные запроса.
7.  Отправляет POST-запрос к API чата.
8.  Обрабатывает потоковый ответ, извлекая сообщения и возвращая их через генератор.
9.  Обновляет объект разговора информацией об ответе, если `return_conversation` установлен в `True`.
10. Обрабатывает возможные ошибки и повторяет попытки при необходимости.

```
Валидация модели -> Инициализация сессии -> Получение версии фронтенда -> Инициализация разговора -> Подготовка заголовков -> Формирование данных -> POST-запрос -> Обработка ответа -> Обновление разговора -> Обработка ошибок
```

**Примеры**:

```python
messages = [{"role": "user", "content": "Hello, world!"}]
async for response in DDG.create_async_generator(model="gpt-4o-mini", messages=messages):
    print(response)
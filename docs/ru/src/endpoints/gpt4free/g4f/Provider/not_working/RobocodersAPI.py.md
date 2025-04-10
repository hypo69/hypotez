# Модуль `RobocodersAPI.py`

## Обзор

Модуль `RobocodersAPI.py` предназначен для взаимодействия с API Robocoders AI. Он предоставляет асинхронный интерфейс для обмена сообщениями с различными агентами, такими как `GeneralCodingAgent`, `RepoAgent` и `FrontEndAgent`. Модуль также включает механизмы для кэширования и обновления токенов доступа и идентификаторов сессий, чтобы обеспечить стабильное и безопасное соединение с API.

## Подробней

Этот модуль является частью проекта `hypotez` и обеспечивает интеграцию с API Robocoders AI для генерации кода и выполнения других задач, связанных с искусственным интеллектом. Он использует асинхронные запросы для обеспечения неблокирующего взаимодействия с API, что позволяет эффективно использовать ресурсы и обеспечивать высокую производительность.

## Классы

### `RobocodersAPI`

**Описание**: Класс `RobocodersAPI` является основным классом, предоставляющим функциональность для взаимодействия с API Robocoders AI. Он наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`, что обеспечивает поддержку асинхронной генерации и выбора моделей.

**Принцип работы**:
1.  **Инициализация**: При инициализации класса определяются основные параметры, такие как URL API, поддерживаемые модели и местоположение кэш-файлов.
2.  **Аутентификация и сессия**: Класс использует кэширование для хранения токена доступа и идентификатора сессии. Если они не найдены в кэше или недействительны, класс получает новый токен и создает новую сессию.
3.  **Взаимодействие с API**: Для отправки запросов к API используется асинхронный HTTP-клиент `aiohttp`. Запросы отправляются с использованием токена доступа и идентификатора сессии.
4.  **Обработка ответов**: Ответы от API обрабатываются построчно, при этом каждая строка декодируется из JSON. Извлекаются сообщения и, при необходимости, отправляются дополнительные запросы для продолжения диалога.
5.  **Кэширование**: Токен доступа и идентификатор сессии сохраняются в кэш-файле для повторного использования.

**Методы**:

-   `create_async_generator`: Создает асинхронный генератор для обмена сообщениями с API.
-   `_get_or_create_access_and_session`: Получает или создает токен доступа и идентификатор сессии.
-   `_fetch_and_cache_access_token`: Получает токен доступа и сохраняет его в кэше.
-   `_create_and_cache_session`: Создает идентификатор сессии и сохраняет его в кэше.
-   `_save_cached_data`: Сохраняет данные в кэш-файл.
-   `_update_cached_data`: Обновляет данные в кэш-файле.
-   `_clear_cached_data`: Удаляет кэш-файл.
-   `_get_cached_data`: Получает данные из кэш-файла.

### `create_async_generator`

```python
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    **kwargs
) -> AsyncResult:
    """Создает асинхронный генератор для обмена сообщениями с API Robocoders AI.

    Args:
        cls: Класс RobocodersAPI.
        model (str): Модель, используемая для генерации ответов.
        messages (Messages): Список сообщений для отправки в API.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию None.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий сообщения от API.

    Raises:
        Exception: Если не удалось инициализировать взаимодействие с API или возникли ошибки при обработке запросов.

    **Как работает функция**:
    1. **Инициализация**: Устанавливает таймаут для HTTP-клиента.
    2. **Получение или создание токена и сессии**: Вызывает `cls._get_or_create_access_and_session` для получения токена доступа и идентификатора сессии. Если получение не удалось, выбрасывается исключение.
    3. **Формирование заголовков и данных запроса**: Формирует заголовки запроса с токеном доступа и данные запроса, включающие идентификатор сессии, промпт и модель.
    4. **Отправка запроса и обработка ответов**: Отправляет POST-запрос к API и обрабатывает ответы построчно.
    5. **Декодирование JSON**: Каждая строка ответа декодируется из JSON. Извлекается сообщение из полей `args.content` или `message`.
    6. **Обработка лимитов ресурсов**: Если достигнут лимит ресурсов, отправляется запрос на продолжение диалога.
    7. **Обработка ошибок**: Обрабатываются ошибки декодирования JSON и другие исключения, возникающие при обработке ответов.
    8. **Генерация сообщений**: Сгенерированные сообщения передаются через асинхронный генератор.

    ```
    Инициализация -> Получение/Создание токена и сессии
    │                  │
    │                  ├─> Ошибка: Не удалось инициализировать API
    │                  │
    │                  V
    │        Формирование заголовков и данных запроса
    │                  │
    │                  V
    │ Отправка запроса -> Обработка ответов
    │        │           │
    │        │           ├─> Ошибка HTTP: Unauthorized, Validation Error, Server Error, Unexpected Error
    │        │           │
    │        │           V
    │        │    Декодирование JSON -> Извлечение сообщения
    │        │                  │        │
    │        │                  │        ├─> Сообщение отсутствует
    │        │                  │        │
    │        │                  │        V
    │        │                  │    Проверка лимита ресурсов
    │        │                  │        │
    │        │                  │        ├─> Лимит достигнут: Отправка запроса на продолжение
    │        │                  │        │
    │        │                  │        V
    │        │                  │    Генерация сообщения
    │        │                  │
    │        │                  V
    │        │    Обработка ошибок JSON и исключений
    │        │
    │        V
    │    Асинхронный генератор сообщений
    │
    V
    Конец
    ```

    **Примеры**:

    ```python
    # Пример использования функции create_async_generator
    async def main():
        model = 'GeneralCodingAgent'
        messages = [{'role': 'user', 'content': 'Напиши функцию на Python, которая вычисляет факториал числа.'}]
        async for message in RobocodersAPI.create_async_generator(model=model, messages=messages):
            print(message)

    if __name__ == "__main__":
        import asyncio
        asyncio.run(main())
    ```
    """
    timeout = ClientTimeout(total=600)
    
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # Load or create access token and session ID
        access_token, session_id = await cls._get_or_create_access_and_session(session)
        if not access_token or not session_id:
            raise Exception("Failed to initialize API interaction")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        
        prompt = format_prompt(messages)
        
        data = {
            "sid": session_id,
            "prompt": prompt,
            "agent": model
        }
        
        async with session.post(cls.api_endpoint, headers=headers, json=data, proxy=proxy) as response:
            if response.status == 401:  # Unauthorized, refresh token
                cls._clear_cached_data()
                raise Exception("Unauthorized: Invalid token, please retry.")
            elif response.status == 422:
                raise Exception("Validation Error: Invalid input.")
            elif response.status >= 500:
                raise Exception(f"Server Error: {response.status}")
            elif response.status != 200:
                raise Exception(f"Unexpected Error: {response.status}")
            
            async for line in response.content:
                if line:
                    try:
                        # Decode bytes into a string
                        line_str = line.decode('utf-8')
                        response_data = json.loads(line_str)
                        
                        # Get the message from the 'args.content' or 'message' field
                        message = (response_data.get('args', {}).get('content') or 
                                 response_data.get('message', ''))
                        
                        if message:
                            yield message
                            
                        # Check for reaching the resource limit
                        if (response_data.get('action') == 'message' and 
                            response_data.get('args', {}).get('wait_for_response')):
                            # Automatically continue the dialog
                            continue_data = {
                                "sid": session_id,
                                "prompt": "continue",
                                "agent": model
                            }
                            async with session.post(
                                cls.api_endpoint, 
                                headers=headers, 
                                json=continue_data, 
                                proxy=proxy
                            ) as continue_response:
                                if continue_response.status == 200:
                                    async for continue_line in continue_response.content:
                                        if continue_line:
                                            try:
                                                continue_line_str = continue_line.decode('utf-8')
                                                continue_data = json.loads(continue_line_str)
                                                continue_message = (
                                                    continue_data.get('args', {}).get('content') or 
                                                    continue_data.get('message', '')
                                                )
                                                if continue_message:
                                                    yield continue_message
                                            except json.JSONDecodeError:
                                                debug.log(f"Failed to decode continue JSON: {continue_line}")
                                            except Exception as ex:
                                                debug.log(f"Error processing continue response: {ex}")
                        
                    except json.JSONDecodeError:
                        debug.log(f"Failed to decode JSON: {line}")
                    except Exception as ex:
                        debug.log(f"Error processing response: {ex}")
        
### `_get_or_create_access_and_session`

```python
@staticmethod
async def _get_or_create_access_and_session(session: aiohttp.ClientSession) -> tuple[str, str]:
    """Получает или создает токен доступа и идентификатор сессии для взаимодействия с API Robocoders AI.

    Args:
        session (aiohttp.ClientSession): Асинхронная клиентская сессия.

    Returns:
        tuple[str, str]: Кортеж, содержащий токен доступа и идентификатор сессии.

    Raises:
        Exception: Если не удалось получить токен доступа или создать сессию.

    **Как работает функция**:
    1.  **Проверка кэша**: Проверяет наличие кэш-файла и загружает данные из него, если файл существует.
    2.  **Валидация данных**: Проверяет, существуют ли в загруженных данных токен доступа и идентификатор сессии.
    3.  **Создание новых данных**: Если данные в кэше отсутствуют или недействительны, вызываются функции `_fetch_and_cache_access_token` и `_create_and_cache_session` для получения нового токена и создания новой сессии.
    4.  **Возврат данных**: Возвращает токен доступа и идентификатор сессии.

    ```
    Проверка кэша -> Загрузка данных из кэша (если есть)
    │              │
    │              V
    │        Валидация данных из кэша
    │              │
    │              ├─> Данные валидны: Возврат данных
    │              │
    │              V
    │        Получение токена доступа -> Кэширование токена
    │              │
    │              V
    │        Создание сессии -> Кэширование идентификатора сессии
    │              │
    │              V
    │        Возврат токена доступа и идентификатора сессии
    │
    V
    Конец
    ```

    **Примеры**:

    ```python
    # Пример использования функции _get_or_create_access_and_session
    async def main():
        async with aiohttp.ClientSession() as session:
            access_token, session_id = await RobocodersAPI._get_or_create_access_and_session(session)
            print(f"Access Token: {access_token}")
            print(f"Session ID: {session_id}")

    if __name__ == "__main__":
        import asyncio
        asyncio.run(main())
    ```
    """
    RobocodersAPI.CACHE_DIR.mkdir(exist_ok=True)  # Ensure cache directory exists

    # Load data from cache
    if RobocodersAPI.CACHE_FILE.exists():
        with open(RobocodersAPI.CACHE_FILE, "r") as f:
            data = json.load(f)
            access_token = data.get("access_token")
            session_id = data.get("sid")

            # Validate loaded data
            if access_token and session_id:
                return access_token, session_id

    # If data not valid, create new access token and session ID
    access_token = await RobocodersAPI._fetch_and_cache_access_token(session)
    session_id = await RobocodersAPI._create_and_cache_session(session, access_token)
    return access_token, session_id
```

### `_fetch_and_cache_access_token`

```python
@staticmethod
async def _fetch_and_cache_access_token(session: aiohttp.ClientSession) -> str:
    """Получает токен доступа из API Robocoders AI и сохраняет его в кэше.

    Args:
        session (aiohttp.ClientSession): Асинхронная клиентская сессия.

    Returns:
        str: Токен доступа.

    Raises:
        MissingRequirementsError: Если отсутствует библиотека BeautifulSoup4.
        Exception: Если не удалось получить токен доступа.

    **Как работает функция**:
    1.  **Проверка зависимостей**: Проверяет, установлена ли библиотека `beautifulsoup4`. Если нет, выбрасывается исключение `MissingRequirementsError`.
    2.  **Выполнение запроса**: Выполняет GET-запрос к URL аутентификации API для получения HTML-страницы.
    3.  **Извлечение токена**: Использует BeautifulSoup для парсинга HTML и извлечения токена доступа из элемента `<pre>` с `id='token'`.
    4.  **Кэширование токена**: Сохраняет токен доступа в кэш с помощью функции `_save_cached_data`.
    5.  **Возврат токена**: Возвращает извлеченный токен доступа.

    ```
    Проверка зависимостей (BeautifulSoup4)
    │
    ├─> Отсутствует BeautifulSoup4: MissingRequirementsError
    │
    V
    Выполнение GET-запроса к URL аутентификации
    │
    V
    Парсинг HTML с помощью BeautifulSoup
    │
    V
    Извлечение токена доступа из элемента <pre id='token'>
    │
    ├─> Элемент отсутствует: Возврат None
    │
    V
    Кэширование токена доступа
    │
    V
    Возврат токена доступа
    ```

    **Примеры**:

    ```python
    # Пример использования функции _fetch_and_cache_access_token
    async def main():
        async with aiohttp.ClientSession() as session:
            try:
                access_token = await RobocodersAPI._fetch_and_cache_access_token(session)
                print(f"Access Token: {access_token}")
            except MissingRequirementsError as ex:
                print(f"Error: {ex}")

    if __name__ == "__main__":
        import asyncio
        asyncio.run(main())
    ```
    """
    if not HAS_BEAUTIFULSOUP:
        raise MissingRequirementsError('Install "beautifulsoup4" package | pip install -U beautifulsoup4')

    url_auth = 'https://api.robocoders.ai/auth'
    headers_auth = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    async with session.get(url_auth, headers=headers_auth) as response:
        if response.status == 200:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            token_element = soup.find('pre', id='token')
            if token_element:
                token = token_element.text.strip()

                # Cache the token
                RobocodersAPI._save_cached_data({"access_token": token})
                return token
    return None
```

### `_create_and_cache_session`

```python
@staticmethod
async def _create_and_cache_session(session: aiohttp.ClientSession, access_token: str) -> str:
    """Создает сессию в API Robocoders AI и сохраняет идентификатор сессии в кэше.

    Args:
        session (aiohttp.ClientSession): Асинхронная клиентская сессия.
        access_token (str): Токен доступа.

    Returns:
        str: Идентификатор сессии.

    Raises:
        Exception: Если не удалось создать сессию.

    **Как работает функция**:
    1.  **Выполнение запроса**: Выполняет GET-запрос к URL создания сессии API с токеном доступа в заголовке.
    2.  **Обработка ответа**: Если запрос выполнен успешно (status code 200), извлекает идентификатор сессии из JSON-ответа.
    3.  **Кэширование идентификатора сессии**: Сохраняет идентификатор сессии в кэш с помощью функции `_update_cached_data`.
    4.  **Обработка ошибок**: Если запрос не выполнен (status code 401 или 422), очищает кэш и выбрасывает исключение.
    5.  **Возврат идентификатора сессии**: Возвращает извлеченный идентификатор сессии.

    ```
    Выполнение GET-запроса к URL создания сессии
    │
    V
    Обработка ответа
    │
    ├─> Status code 200: Извлечение идентификатора сессии из JSON
    │   │
    │   V
    │   Кэширование идентификатора сессии
    │   │
    │   V
    │   Возврат идентификатора сессии
    │
    ├─> Status code 401 или 422: Очистка кэша и выброс исключения
    │
    V
    Конец (возврат None)
    ```

    **Примеры**:

    ```python
    # Пример использования функции _create_and_cache_session
    async def main():
        async with aiohttp.ClientSession() as session:
            # Предположим, что access_token уже получен
            access_token = "your_access_token"  # Замените на ваш токен
            try:
                session_id = await RobocodersAPI._create_and_cache_session(session, access_token)
                print(f"Session ID: {session_id}")
            except Exception as ex:
                print(f"Error: {ex}")

    if __name__ == "__main__":
        import asyncio
        asyncio.run(main())
    ```
    """
    url_create_session = 'https://api.robocoders.ai/create-session'
    headers_create_session = {
        'Authorization': f'Bearer {access_token}'
    }

    async with session.get(url_create_session, headers=headers_create_session) as response:
        if response.status == 200:
            data = await response.json()
            session_id = data.get('sid')

            # Cache session ID
            RobocodersAPI._update_cached_data({"sid": session_id})
            return session_id
        elif response.status == 401:
            RobocodersAPI._clear_cached_data()
            raise Exception("Unauthorized: Invalid token during session creation.")
        elif response.status == 422:
            raise Exception("Validation Error: Check input parameters.")
    return None
```

### `_save_cached_data`

```python
@staticmethod
def _save_cached_data(new_data: dict):
    """Сохраняет новые данные в кэш-файл.

    Args:
        new_data (dict): Данные для сохранения в кэш.

    **Как работает функция**:
    1.  **Создание директории**: Проверяет, существует ли директория для кэша, и создает ее, если она отсутствует.
    2.  **Создание файла**: Проверяет, существует ли кэш-файл, и создает его, если он отсутствует.
    3.  **Сохранение данных**: Открывает кэш-файл в режиме записи и сохраняет переданные данные в формате JSON.

    ```
    Создание директории (если отсутствует)
    │
    V
    Создание файла (если отсутствует)
    │
    V
    Открытие файла в режиме записи
    │
    V
    Сохранение данных в формате JSON
    │
    V
    Конец
    ```

    **Примеры**:

    ```python
    # Пример использования функции _save_cached_data
    new_data = {"access_token": "your_access_token"}
    RobocodersAPI._save_cached_data(new_data)
    ```
    """
    RobocodersAPI.CACHE_DIR.mkdir(exist_ok=True)
    RobocodersAPI.CACHE_FILE.touch(exist_ok=True)
    with open(RobocodersAPI.CACHE_FILE, "w") as f:
        json.dump(new_data, f)
```

### `_update_cached_data`

```python
@staticmethod
def _update_cached_data(updated_data: dict):
    """Обновляет существующие данные в кэш-файле новыми значениями.

    Args:
        updated_data (dict): Данные для обновления кэша.

    **Как работает функция**:
    1.  **Чтение существующих данных**: Пытается прочитать существующие данные из кэш-файла. Если файл не существует или поврежден, создает пустой словарь.
    2.  **Обновление данных**: Обновляет прочитанные данные новыми значениями из `updated_data`.
    3.  **Сохранение обновленных данных**: Сохраняет обновленные данные в кэш-файл в формате JSON.

    ```
    Чтение существующих данных из кэша
    │
    ├─> Файл отсутствует или поврежден: Создание пустого словаря
    │
    V
    Обновление данных
    │
    V
    Сохранение обновленных данных в формате JSON
    │
    V
    Конец
    ```

    **Примеры**:

    ```python
    # Пример использования функции _update_cached_data
    updated_data = {"sid": "new_session_id"}
    RobocodersAPI._update_cached_data(updated_data)
    ```
    """
    data = {}
    if RobocodersAPI.CACHE_FILE.exists():
        with open(RobocodersAPI.CACHE_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                # If cache file is corrupted, start with empty dict
                data = {}
    
    data.update(updated_data)
    with open(RobocodersAPI.CACHE_FILE, "w") as f:
        json.dump(data, f)
```

### `_clear_cached_data`

```python
@staticmethod
def _clear_cached_data():
    """Удаляет кэш-файл.

    **Как работает функция**:
    1.  **Проверка наличия файла**: Проверяет, существует ли кэш-файл.
    2.  **Удаление файла**: Если файл существует, пытается его удалить.
    3.  **Обработка ошибок**: Если при удалении файла возникает ошибка, логирует ее.

    ```
    Проверка наличия файла
    │
    ├─> Файл отсутствует: Конец
    │
    V
    Удаление файла
    │
    ├─> Ошибка при удалении: Логирование ошибки
    │
    V
    Конец
    ```

    **Примеры**:

    ```python
    # Пример использования функции _clear_cached_data
    RobocodersAPI._clear_cached_data()
    ```
    """
    try:
        if RobocodersAPI.CACHE_FILE.exists():
            RobocodersAPI.CACHE_FILE.unlink()
    except Exception as ex:
        debug.log(f"Error clearing cache: {ex}")
```

### `_get_cached_data`

```python
@staticmethod
def _get_cached_data() -> dict:
    """Получает все данные из кэш-файла.

    Returns:
        dict: Данные из кэш-файла.

    **Как работает функция**:
    1.  **Проверка наличия файла**: Проверяет, существует ли кэш-файл.
    2.  **Чтение данных**: Если файл существует, пытается прочитать данные из него.
    3.  **Обработка ошибок**: Если при чтении данных возникает ошибка (например, файл поврежден), возвращает пустой словарь.
    4.  **Возврат данных**: Возвращает прочитанные данные из кэш-файла.

    ```
    Проверка наличия файла
    │
    ├─> Файл отсутствует: Возврат пустого словаря
    │
    V
    Чтение данных из файла
    │
    ├─> Ошибка при чтении: Возврат пустого словаря
    │
    V
    Возврат данных
    ```

    **Примеры**:

    ```python
    # Пример использования функции _get_cached_data
    cached_data = RobocodersAPI._get_cached_data()
    print(cached_data)
    ```
    """
    if RobocodersAPI.CACHE_FILE.exists():
        try:
            with open(RobocodersAPI.CACHE_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}
```

## Функции

В данном модуле нет отдельных функций, не являющихся методами класса `RobocodersAPI`. Все основные операции выполняются через методы этого класса.
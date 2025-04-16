# Модуль для работы с GigaChat от Sber

## Обзор

Модуль `GigaChat.py` предоставляет асинхронный интерфейс для взаимодействия с GigaChat API от Sber. Он поддерживает потоковую передачу данных, управление историей сообщений и системными сообщениями. Модуль требует аутентификации через API-ключ и использует SSL для безопасного соединения.

## Подробней

Модуль предназначен для интеграции с GigaChat API, позволяя отправлять запросы на генерацию текста и получать ответы в асинхронном режиме. Он автоматически обновляет токен доступа и обрабатывает потоковые ответы от сервера.

## Классы

### `GigaChat`

**Описание**: Класс `GigaChat` предоставляет асинхронный генератор для взаимодействия с API GigaChat.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую функциональность для асинхронных генераторов.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `url` (str): URL для доступа к API GigaChat (`https://developers.sber.ru/gigachat`).
- `working` (bool): Указывает, работает ли провайдер (True).
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений (True).
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения (True).
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу (True).
- `needs_auth` (bool): Указывает, требуется ли аутентификация (True).
- `default_model` (str): Модель, используемая по умолчанию ("GigaChat:latest").
- `models` (List[str]): Список поддерживаемых моделей (["GigaChat:latest", "GigaChat-Plus", "GigaChat-Pro"]).

**Методы**:
- `create_async_generator()`: Создает асинхронный генератор для взаимодействия с API GigaChat.

## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    stream: bool = True,
    proxy: str = None,
    api_key: str = None,
    connector: BaseConnector = None,
    scope: str = "GIGACHAT_API_PERS",
    update_interval: float = 0,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для взаимодействия с API GigaChat.

    Args:
        model (str): Название используемой модели.
        messages (Messages): Список сообщений для отправки в API.
        stream (bool): Флаг, указывающий, использовать ли потоковую передачу (по умолчанию True).
        proxy (str): URL прокси-сервера (по умолчанию None).
        api_key (str): API-ключ для аутентификации.
        connector (BaseConnector): Aiohttp connector (по умолчанию None).
        scope (str): Область действия для получения токена доступа (по умолчанию "GIGACHAT_API_PERS").
        update_interval (float): Интервал обновления (по умолчанию 0).
        **kwargs: Дополнительные аргументы для API.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий части ответа от API.

    Raises:
        MissingAuthError: Если отсутствует API-ключ.
        Exception: Если возникает ошибка при запросе к API.

    Как работает функция:
    - Проверяет наличие API-ключа. Если ключ отсутствует, вызывает исключение MissingAuthError.
    - Определяет путь к файлу сертификата для доверенного соединения SSL.
    - Если файл сертификата не существует, он будет создан.
    - Если SSL доступен и коннектор не передан, создает SSL контекст и TCP коннектор.
    - Создает сессию клиента aiohttp для выполнения запросов.
    - Проверяет срок действия токена доступа и, если он истек или скоро истечет, обновляет его.
    - Отправляет POST запрос к API GigaChat с использованием токена доступа, модели, сообщений и других параметров.
    - Обрабатывает потоковые и не потоковые ответы от API, извлекая и выдавая содержимое сообщений.
    - Если ответ потоковый, извлекает данные из каждой строки ответа и выдает их.
    - Если ответ не потоковый, извлекает содержимое сообщения из JSON ответа и возвращает его.
    """

    @classmethod
    async def create_async_generator(
            cls,
            model: str,
            messages: Messages,
            stream: bool = True,
            proxy: str = None,
            api_key: str = None,
            connector: BaseConnector = None,
            scope: str = "GIGACHAT_API_PERS",
            update_interval: float = 0,
            **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для взаимодействия с API GigaChat.

        Args:
            model (str): Название используемой модели.
            messages (Messages): Список сообщений для отправки в API.
            stream (bool): Флаг, указывающий, использовать ли потоковую передачу (по умолчанию True).
            proxy (str): URL прокси-сервера (по умолчанию None).
            api_key (str): API-ключ для аутентификации.
            connector (BaseConnector): Aiohttp connector (по умолчанию None).
            scope (str): Область действия для получения токена доступа (по умолчанию "GIGACHAT_API_PERS").
            update_interval (float): Интервал обновления (по умолчанию 0).
            **kwargs: Дополнительные аргументы для API.

        Returns:
            AsyncResult: Асинхронный генератор, выдающий части ответа от API.

        Raises:
            MissingAuthError: Если отсутствует API-ключ.

        Как работает функция:
        - Проверяет наличие API-ключа. Если ключ отсутствует, вызывает исключение MissingAuthError.
        - Определяет путь к файлу сертификата для доверенного соединения SSL.
        - Если файл сертификата не существует, он будет создан.
        - Если SSL доступен и коннектор не передан, создает SSL контекст и TCP коннектор.
        - Создает сессию клиента aiohttp для выполнения запросов.
        - Проверяет срок действия токена доступа и, если он истек или скоро истечет, обновляет его.
        - Отправляет POST запрос к API GigaChat с использованием токена доступа, модели, сообщений и других параметров.
        - Обрабатывает потоковые и не потоковые ответы от API, извлекая и выдавая содержимое сообщений.
        - Если ответ потоковый, извлекает данные из каждой строки ответа и выдает их.
        - Если ответ не потоковый, извлекает содержимое сообщения из JSON ответа и возвращает его.
        """
        global access_token, token_expires_at # <инструкция для модели gemini: глобальные переменные необходимо использовать внутри этой функции>
        model = cls.get_model(model) # <инструкция для модели gemini:Присваивает результат вызова `cls.get_model(model)` переменной `model`.>
        if not api_key: # <инструкция для модели gemini:Проверяет, что `api_key` не является пустым (то есть, что он существует).>
            raise MissingAuthError('Missing "api_key"') # <инструкция для модели gemini:Если `api_key` пустой, поднимается исключение `MissingAuthError` с сообщением 'Missing "api_key"'.>

        # Create certificate file in cookies directory
        cookies_dir = Path(get_cookies_dir()) # <инструкция для модели gemini:Получает путь к директории для хранения cookies, используя функцию `get_cookies_dir()`, и сохраняет его в переменной `cookies_dir`.>
        cert_file = cookies_dir / 'russian_trusted_root_ca.crt' # <инструкция для модели gemini:Формирует путь к файлу сертификата `russian_trusted_root_ca.crt` в директории cookies и сохраняет его в переменной `cert_file`.>

        # Write certificate if it doesn't exist
        if not cert_file.exists(): # <инструкция для модели gemini:Проверяет, существует ли файл сертификата (`cert_file`) по указанному пути.>
            cert_file.write_text(RUSSIAN_CA_CERT) # <инструкция для модели gemini:Если файл сертификата не существует, записывает текст сертификата, хранящийся в переменной `RUSSIAN_CA_CERT`, в файл.>

        if has_ssl and connector is None: # <инструкция для модели gemini:Проверяет, поддерживается ли SSL (`has_ssl`) и не передан ли коннектор (`connector` is None).>
            ssl_context = ssl.create_default_context(cafile=str(cert_file)) # <инструкция для модели gemini:Создает SSL-контекст по умолчанию, используя файл сертификата (`cert_file`), и сохраняет его в переменной `ssl_context`.>
            connector = TCPConnector(ssl_context=ssl_context) # <инструкция для модели gemini:Создает TCP-коннектор с использованием созданного SSL-контекста и сохраняет его в переменной `connector`.>

        async with ClientSession(connector=get_connector(connector, proxy)) as session: # <инструкция для модели gemini:Создает асинхронную сессию клиента (`ClientSession`) с использованием коннектора, полученного из функции `get_connector(connector, proxy)`.>
            if token_expires_at - int(time.time() * 1000) < 60000: # <инструкция для модели gemini:Проверяет, истек ли срок действия токена доступа (`token_expires_at`) или осталось менее 60 секунд до истечения срока действия.>
                async with session.post(url="https://ngw.devices.sberbank.ru:9443/api/v2/oauth", # <инструкция для модели gemini:Отправляет POST-запрос на URL для получения токена доступа.>
                                        headers={"Authorization": f"Bearer {api_key}", # <инструкция для модели gemini:Формирует заголовки запроса, включая API-ключ для авторизации.>
                                                 "RqUID": str(uuid.uuid4()), # <инструкция для модели gemini:Генерирует уникальный идентификатор запроса (RqUID).>
                                                 "Content-Type": "application/x-www-form-urlencoded"}, # <инструкция для модели gemini:Устанавливает тип контента как `application/x-www-form-urlencoded`.>
                                        data={"scope": scope}) as response: # <инструкция для модели gemini:Передает область действия (`scope`) в теле запроса.>
                    await raise_for_status(response) # <инструкция для модели gemini:Проверяет статус ответа и вызывает исключение, если статус указывает на ошибку.>
                    data = await response.json() # <инструкция для модели gemini:Преобразует ответ в формат JSON и сохраняет его в переменной `data`.>
                access_token = data['access_token'] # <инструкция для модели gemini:Извлекает токен доступа из JSON-ответа и сохраняет его в глобальной переменной `access_token`.>
                token_expires_at = data['expires_at'] # <инструкция для модели gemini:Извлекает время истечения срока действия токена из JSON-ответа и сохраняет его в глобальной переменной `token_expires_at`.>

            async with session.post(url="https://gigachat.devices.sberbank.ru/api/v1/chat/completions", # <инструкция для модели gemini:Отправляет POST-запрос к API GigaChat для получения завершения чата.>
                                    headers={"Authorization": f"Bearer {access_token}"}, # <инструкция для модели gemini:Формирует заголовки запроса, включая токен доступа для авторизации.>
                                    json={ # <инструкция для модели gemini:Формирует JSON-тело запроса, включая модель, сообщения, флаг потоковой передачи и другие параметры.>
                                        "model": model,
                                        "messages": messages,
                                        "stream": stream,
                                        "update_interval": update_interval,
                                        **kwargs
                                    }) as response:
                await raise_for_status(response) # <инструкция для модели gemini:Проверяет статус ответа и вызывает исключение, если статус указывает на ошибку.>

                async for line in response.content: # <инструкция для модели gemini:Асинхронно перебирает строки содержимого ответа.>
                    if not stream: # <инструкция для модели gemini:Проверяет, используется ли потоковая передача.>
                        yield json.loads(line.decode("utf-8"))['choices'][0]['message']['content'] # <инструкция для модели gemini:Если потоковая передача не используется, преобразует строку в JSON, извлекает содержимое сообщения и возвращает его.>
                        return # <инструкция для модели gemini:Завершает выполнение генератора.>

                    if line and line.startswith(b"data:"): # <инструкция для модели gemini:Проверяет, начинается ли строка с префикса "data:".>
                        line = line[6:-1]  # remove "data: " prefix and "\\n" suffix # <инструкция для модели gemini:Удаляет префикс "data: " и суффикс "\\n" из строки.>
                        if line.strip() == b"[DONE]": # <инструкция для модели gemini:Проверяет, является ли строка индикатором завершения ("[DONE]").>
                            return # <инструкция для модели gemini:Завершает выполнение генератора, если строка является индикатором завершения.>
                        else: # <инструкция для модели gemini:Если строка не является индикатором завершения, продолжает обработку.>
                            msg = json.loads(line.decode("utf-8"))['choices'][0] # <инструкция для модели gemini:Преобразует строку в JSON и извлекает первую часть выбора.>
                            content = msg['delta']['content'] # <инструкция для модели gemini:Извлекает содержимое из дельты сообщения.>

                            if content: # <инструкция для модели gemini:Проверяет, есть ли содержимое.>
                                yield content # <инструкция для модели gemini:Возвращает содержимое.>

                            if 'finish_reason' in msg: # <инструкция для модели gemini:Проверяет, присутствует ли причина завершения в сообщении.>
                                return # <инструкция для модели gemini:Завершает выполнение генератора, если присутствует причина завершения.>

## Параметры класса

- `model` (str): Название используемой модели.
- `messages` (Messages): Список сообщений для отправки в API.
- `stream` (bool): Флаг, указывающий, использовать ли потоковую передачу (по умолчанию True).
- `proxy` (str): URL прокси-сервера (по умолчанию None).
- `api_key` (str): API-ключ для аутентификации.
- `connector` (BaseConnector): Aiohttp connector (по умолчанию None).
- `scope` (str): Область действия для получения токена доступа (по умолчанию "GIGACHAT_API_PERS").
- `update_interval` (float): Интервал обновления (по умолчанию 0).
- `**kwargs`: Дополнительные аргументы для API.

## Примеры

```python
# Пример использования асинхронного генератора GigaChat
import asyncio
from src.endpoints.gpt4free.g4f.Provider.needs_auth.GigaChat import GigaChat

async def main():
    api_key = "YOUR_API_KEY"  # Замените на ваш фактический API-ключ
    messages = [{"role": "user", "content": "Привет, как дела?"}]

    generator = await GigaChat.create_async_generator(model="GigaChat:latest", messages=messages, api_key=api_key)

    async for message in generator:
        print(message, end="")

if __name__ == "__main__":
    asyncio.run(main())
```

```python
# Пример использования с прокси
import asyncio
from src.endpoints.gpt4free.g4f.Provider.needs_auth.GigaChat import GigaChat

async def main():
    api_key = "YOUR_API_KEY"  # Замените на ваш фактический API-ключ
    messages = [{"role": "user", "content": "Привет, как дела?"}]
    proxy = "http://your_proxy:8080"  # Замените на ваш прокси-сервер

    generator = await GigaChat.create_async_generator(model="GigaChat:latest", messages=messages, api_key=api_key, proxy=proxy)

    async for message in generator:
        print(message, end="")

if __name__ == "__main__":
    asyncio.run(main())
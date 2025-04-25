# Модуль Chatgpt4o

## Обзор

Модуль предоставляет асинхронный класс `Chatgpt4o`, который реализует взаимодействие с API сервиса `chatgpt4o.one` для работы с моделью `gpt-4o-mini`. Класс наследует от `AsyncProvider` и `ProviderModelMixin`, обеспечивая базовые функции для отправки запросов и обработки ответов.

## Подробности

Класс `Chatgpt4o`  предназначен для использования в проекте `hypotez` в качестве провайдера для работы с моделью `gpt-4o-mini`. Он реализует асинхронную отправку запросов и обработку ответов от API `chatgpt4o.one`.

## Классы

### `class Chatgpt4o`

**Описание**: Асинхронный класс, предоставляющий интерфейс для работы с API `chatgpt4o.one`. 

**Наследует**:
- `AsyncProvider`: Базовый класс для асинхронных провайдеров.
- `ProviderModelMixin`: Обеспечивает функциональность работы с моделями.

**Атрибуты**:

- `url (str)`: Базовый URL API сервиса `chatgpt4o.one`.
- `working (bool)`: Флаг, указывающий на доступность сервиса.
- `_post_id (str)`: ID сообщения для отслеживания сессии.
- `_nonce (str)`: Строка, используемая для защиты от подделки межсайтовых запросов (CSRF).
- `default_model (str)`: Имя модели по умолчанию.
- `models (List[str])`: Список поддерживаемых моделей.
- `model_aliases (Dict[str, str])`: Словарь псевдонимов для моделей.

**Методы**:

- `create_async(model: str, messages: Messages, proxy: str = None, timeout: int = 120, cookies: dict = None, **kwargs) -> str`: Асинхронная функция для отправки запроса к API `chatgpt4o.one`.

## Методы класса

### `create_async`

```python
    @classmethod
    async def create_async(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        timeout: int = 120,
        cookies: dict = None,
        **kwargs
    ) -> str:
        """
        Асинхронная функция для отправки запроса к API `chatgpt4o.one`.

        Args:
            model (str): Имя модели.
            messages (Messages): Список сообщений для отправки в модель.
            proxy (str, optional): Прокси-сервер. По умолчанию `None`.
            timeout (int, optional): Время ожидания ответа. По умолчанию 120 секунд.
            cookies (dict, optional): Словарь cookie для отправки. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            str: Ответ модели в формате JSON.

        Raises:
            RuntimeError: В случае ошибок при получении ID сообщения или nonce, или при неожиданной структуре ответа.
        """
        headers = {
            'authority': 'chatgpt4o.one',
            'accept': '*/*',
            'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
            'origin': 'https://chatgpt4o.one',
            'referer': 'https://chatgpt4o.one',
            'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        }

        async with StreamSession(
            headers=headers,
            cookies=cookies,
            impersonate="chrome",
            proxies={"all": proxy},
            timeout=timeout
        ) as session:

            if not cls._post_id or not cls._nonce:
                async with session.get(f"{cls.url}/") as response:
                    await raise_for_status(response)
                    response_text = await response.text()

                    post_id_match = re.search(r'data-post-id="([0-9]+)"', response_text)
                    nonce_match = re.search(r'data-nonce="(.*?)"', response_text)

                    if not post_id_match:
                        raise RuntimeError("No post ID found")
                    cls._post_id = post_id_match.group(1)

                    if not nonce_match:
                        raise RuntimeError("No nonce found")
                    cls._nonce = nonce_match.group(1)

            prompt = format_prompt(messages)
            data = {
                "_wpnonce": cls._nonce,
                "post_id": cls._post_id,
                "url": cls.url,
                "action": "wpaicg_chat_shortcode_message",
                "message": prompt,
                "bot_id": "0"
            }

            async with session.post(f"{cls.url}/wp-admin/admin-ajax.php", data=data, cookies=cookies) as response:
                await raise_for_status(response)
                response_json = await response.json()
                if "data" not in response_json:
                    raise RuntimeError("Unexpected response structure: 'data' field missing")
                return response_json["data"]

```

**Назначение**: Функция отправляет запрос к API `chatgpt4o.one` с заданным набором сообщений для модели и возвращает полученный ответ в формате JSON.

**Параметры**:

- `model (str)`: Имя модели, к которой отправляется запрос.
- `messages (Messages)`: Список сообщений для отправки.
- `proxy (str, optional)`: Прокси-сервер. По умолчанию `None`.
- `timeout (int, optional)`: Время ожидания ответа. По умолчанию 120 секунд.
- `cookies (dict, optional)`: Словарь cookie для отправки. По умолчанию `None`.

**Возвращает**:

- `str`: Ответ модели в формате JSON.

**Вызывает исключения**:

- `RuntimeError`: В случае ошибок при получении ID сообщения или nonce, или при неожиданной структуре ответа.

**Как работает функция**:

- Функция `create_async` получает имя модели, список сообщений, а также дополнительные параметры, такие как прокси-сервер, время ожидания и cookie.
- Если ID сообщения и nonce не заданы, функция получает их с помощью GET-запроса к API `chatgpt4o.one`. 
- Затем функция формирует данные для POST-запроса, включая ID сообщения, nonce, модель, список сообщений и другие параметры.
- Используя объект `StreamSession`, функция отправляет POST-запрос к API `chatgpt4o.one` с сформированными данными.
- После получения ответа от API, функция проверяет наличие поля `data` в JSON-ответе и, если оно присутствует, возвращает его значение.
- В случае возникновения ошибок, функция вызывает исключение `RuntimeError` с описанием ошибки.

**Примеры**:

```python
# Пример отправки запроса к модели "gpt-4o-mini"
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.Chatgpt4o import Chatgpt4o
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [
    {'role': 'user', 'content': 'Привет!'},
    {'role': 'assistant', 'content': 'Привет!'}
]

response = await Chatgpt4o.create_async(
    model="gpt-4o-mini",
    messages=messages,
)
print(response)
```

## Параметры класса

- `url (str)`: Базовый URL API сервиса `chatgpt4o.one`, который используется для отправки запросов.
- `working (bool)`: Флаг, указывающий на доступность сервиса.
- `_post_id (str)`: ID сообщения для отслеживания сессии.
- `_nonce (str)`: Строка, используемая для защиты от подделки межсайтовых запросов (CSRF).
- `default_model (str)`: Имя модели по умолчанию.
- `models (List[str])`: Список поддерживаемых моделей.
- `model_aliases (Dict[str, str])`: Словарь псевдонимов для моделей.

**Примеры**:

```python
# Пример использования модели "gpt-4o-mini" с использованием псевдонима
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.Chatgpt4o import Chatgpt4o
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [
    {'role': 'user', 'content': 'Привет!'},
    {'role': 'assistant', 'content': 'Привет!'}
]

response = await Chatgpt4o.create_async(
    model="gpt-4o-mini",
    messages=messages,
)
print(response)
```
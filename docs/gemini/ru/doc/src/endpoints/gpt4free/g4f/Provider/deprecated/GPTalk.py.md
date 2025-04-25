# Модуль GPTalk
## Обзор

Модуль предоставляет класс `GPTalk` для асинхронного взаимодействия с API gptalk.net, который основан на модели GPT-3.5-turbo.

## Подробей

`GPTalk` - это асинхронный провайдер, который использует API gptalk.net для генерации ответов от модели GPT-3.5-turbo. 
Он реализован как класс, который наследует от `AsyncGeneratorProvider`, что позволяет использовать его в асинхронных 
контекстах.

В данный момент `GPTalk` устарел и его использование не рекомендуется, поскольку API gptalk.net больше не доступен 
для новых пользователей. 

## Классы

### `class GPTalk`

**Описание**: 
Класс `GPTalk` реализует асинхронный генератор ответов от GPT-3.5-turbo, используя API gptalk.net.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
 - `url (str)`: URL адрес API gptalk.net.
 - `working (bool)`: Флаг, указывающий на активность провайдера. 
 - `supports_gpt_35_turbo (bool)`: Флаг, указывающий на поддержку модели GPT-3.5-turbo.
 - `_auth (dict)`: Словарь с информацией об авторизации, получаемый при вызове `create_async_generator`.
 - `used_times (int)`: Счетчик использованных запросов к API.

**Методы**:
 - `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: 
    Создает асинхронный генератор, который выдает ответы от модели GPT-3.5-turbo, используя API gptalk.net.
    - **Назначение**: 
        Функция создает асинхронный генератор ответов от модели GPT-3.5-turbo, используя API gptalk.net.
        Генератор выдает ответы в виде строк.
    - **Параметры**:
        - `model (str)`: Название модели. По умолчанию `gpt-3.5-turbo`.
        - `messages (Messages)`: Список сообщений для контекста модели.
        - `proxy (str)`: URL прокси-сервера (опционально).
    - **Возвращает**:
        - `AsyncResult`: Асинхронный генератор ответов от модели GPT-3.5-turbo.
    - **Вызывает исключения**:
        - `requests.exceptions.RequestException`: При возникновении ошибки во время запроса к API.
    - **Пример**:
        ```python
        messages = [
            {'role': 'user', 'content': 'Привет, как дела?'},
            {'role': 'assistant', 'content': 'Привет! У меня все хорошо, спасибо за вопрос.'},
        ]
        async for response in GPTalk.create_async_generator(messages=messages):
            print(response)
        ```


## Внутренние функции 

- **`create_async_generator`**:
    - **Назначение**: Создает асинхронный генератор, который выдает ответы от модели GPT-3.5-turbo, используя API gptalk.net.
        Генератор выдает ответы в виде строк.
    - **Как работает**: 
        Функция формирует запрос к API gptalk.net с указанием модели, сообщений и прокси (если указан).
        Получает токен авторизации, если он истек или использовалось максимальное количество запросов.
        Использует полученный токен авторизации для отправки запроса к API gptalk.net.
        Получает поток ответов от API gptalk.net и формирует асинхронный генератор, который выдает ответы по частям.
    - **Пример**: 
        ```python
        async def create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult:
            if not model:
                model = "gpt-3.5-turbo"
            timestamp = int(time.time())
            headers = {
                'authority': 'gptalk.net',
                'accept': '*/*',
                'accept-language': 'de-DE,de;q=0.9,en-DE;q=0.8,en;q=0.7,en-US;q=0.6,nl;q=0.5,zh-CN;q=0.4,zh-TW;q=0.3,zh;q=0.2',
                'content-type': 'application/json',
                'origin': 'https://gptalk.net',
                'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Linux"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
                'x-auth-appid': '2229',
                'x-auth-openid': '',
                'x-auth-platform': '',
                'x-auth-timestamp': f"{timestamp}",
            }
            async with ClientSession(headers=headers) as session:
                if not cls._auth or cls._auth["expires_at"] < timestamp or cls.used_times == 5:
                    data = {
                        "fingerprint": secrets.token_hex(16).zfill(32),
                        "platform": "fingerprint"
                    }
                    async with session.post(f"{cls.url}/api/chatgpt/user/login", json=data, proxy=proxy) as response:
                        response.raise_for_status()
                        cls._auth = (await response.json())["data"]
                    cls.used_times = 0
                data = {
                    "content": format_prompt(messages),
                    "accept": "stream",
                    "from": 1,
                    "model": model,
                    "is_mobile": 0,
                    "user_agent": headers["user-agent"],
                    "is_open_ctx": 0,
                    "prompt": "",
                    "roid": 111,
                    "temperature": 0,
                    "ctx_msg_count": 3,
                    "created_at": timestamp
                }
                headers = {
                    'authorization': f'Bearer {cls._auth["token"]}',
                }
                async with session.post(f"{cls.url}/api/chatgpt/chatapi/text", json=data, headers=headers, proxy=proxy) as response:
                    response.raise_for_status()
                    token = (await response.json())["data"]["token"]
                    cls.used_times += 1
                last_message = ""
                async with session.get(f"{cls.url}/api/chatgpt/chatapi/stream", params={"token": token}, proxy=proxy) as response:
                    response.raise_for_status()
                    async for line in response.content:
                        if line.startswith(b"data: "):
                            if line.startswith(b"data: [DONE]"):
                                break
                            message = json.loads(line[6:-1])["content"]
                            yield message[len(last_message):]
                            last_message = message
        ```
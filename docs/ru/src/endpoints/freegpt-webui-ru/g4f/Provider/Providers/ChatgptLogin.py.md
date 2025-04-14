# Модуль ChatgptLogin

## Обзор

Модуль `ChatgptLogin.py` предназначен для взаимодействия с сервисом chatgptlogin.ac для получения ответов от модели gpt-3.5-turbo. Он включает функции для создания запросов к API, преобразования сообщений и обработки ответов. Модуль не требует авторизации и не поддерживает потоковую передачу данных.

## Подробней

Этот модуль используется для обхода ограничений доступа к ChatGPT путем использования стороннего сервиса `chatgptlogin.ac`. Он отправляет запросы к API этого сервиса и обрабатывает полученные ответы.
Модуль преобразует входящие сообщения в формат, ожидаемый API, и извлекает полезную информацию из ответов.
В проекте модуль позволяет использовать альтернативный источник для получения ответов от языковой модели.

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """
    Создает запрос к сервису chatgptlogin.ac и возвращает ответ.

    Args:
        model (str): Имя используемой модели (например, "gpt-3.5-turbo").
        messages (list): Список сообщений для отправки в запросе. Каждое сообщение должно быть словарем с ключами "role" и "content".
        stream (bool): Флаг, указывающий, использовать ли потоковую передачу (не поддерживается).
        **kwargs: Дополнительные аргументы.

    Returns:
        str: Ответ от сервиса chatgptlogin.ac.

    Raises:
        requests.exceptions.RequestException: В случае ошибки при выполнении HTTP-запроса.
        KeyError: Если в ответе JSON отсутствует ключ 'reply'.

    Внутренние функции:
        get_nonce(): Получает одноразовый токен (nonce) с веб-сайта chatgptlogin.ac.
        transform(messages: list) -> list: Преобразует список сообщений в формат, ожидаемый API.
        html_encode(string: str) -> str: Экранирует HTML-специальные символы в строке.

    Как работает функция:
    1. Функция `_create_completion` принимает параметры модели, сообщения и флаг потоковой передачи.
    2. Вызывает внутреннюю функцию `get_nonce` для получения одноразового токена (nonce) с веб-сайта chatgptlogin.ac.
    3. Вызывает внутреннюю функцию `transform` для преобразования списка сообщений в формат, ожидаемый API.
    4. Формирует JSON-данные для отправки в запросе.
    5. Выполняет POST-запрос к `https://chatgptlogin.ac/wp-json/ai-chatbot/v1/chat` с использованием библиотеки `requests`.
    6. Возвращает значение ключа 'reply' из JSON-ответа.

    Блок-схема:
    A: Получение nonce
    |
    B: Преобразование сообщений
    |
    C: Отправка запроса
    |
    D: Получение ответа
    |
    E: Извлечение reply
    |
    F: Возврат reply

    Примеры:
    >>> _create_completion(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'Hello'}], stream=False)
    "Hello there! How can I assist you today?"
    """

    def get_nonce():
        """
        Получает одноразовый токен (nonce) с веб-сайта chatgptlogin.ac.

        Returns:
            str: Одноразовый токен.
        """
        res = requests.get('https://chatgptlogin.ac/use-chatgpt-free/', headers={
            "Referer": "https://chatgptlogin.ac/use-chatgpt-free/",
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        })

        src = re.search(r'class="mwai-chat mwai-chatgpt">.*<span>Send</span></button></div></div></div> <script defer src="(.*?)">', res.text).group(1)
        decoded_string = base64.b64decode(src.split(",")[-1]).decode('utf-8')
        return re.search(r"let restNonce = \'(.*?)\';", decoded_string).group(1)

    def transform(messages: list) -> list:
        """
        Преобразует список сообщений в формат, ожидаемый API.

        Args:
            messages (list): Список сообщений для преобразования.

        Returns:
            list: Преобразованный список сообщений.
        """
        def html_encode(string: str) -> str:
            """
            Экранирует HTML-специальные символы в строке.

            Args:
                string (str): Строка для экранирования.

            Returns:
                str: Экранированная строка.
            """
            table = {
                '"': '&quot;',
                "'": '&#39;',
                '&': '&amp;',
                '>': '&gt;',
                '<': '&lt;',
                '\n': '<br>',
                '\t': '&nbsp;&nbsp;&nbsp;&nbsp;',
                ' ': '&nbsp;'
            }

            for key in table:
                string = string.replace(key, table[key])

            return string

        return [{'id': os.urandom(6).hex(),
                 'role': message['role'],
                 'content': message['content'],
                 'who': 'AI: ' if message['role'] == 'assistant' else 'User: ',
                 'html': html_encode(message['content'])} for message in messages]

    headers = {
        'authority': 'chatgptlogin.ac',
        'accept': '*/*',
        'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
        'content-type': 'application/json',
        'origin': 'https://chatgptlogin.ac',
        'referer': 'https://chatgptlogin.ac/use-chatgpt-free/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'x-wp-nonce': get_nonce()
    }

    conversation = transform(messages)

    json_data = {
        'env': 'chatbot',
        'session': 'N/A',
        'prompt': 'Converse as if you were an AI assistant. Be friendly, creative.',
        'context': 'Converse as if you were an AI assistant. Be friendly, creative.',
        'messages': conversation,
        'newMessage': messages[-1]['content'],
        'userName': '<div class="mwai-name-text">User:</div>',
        'aiName': '<div class="mwai-name-text">AI:</div>',
        'model': 'gpt-3.5-turbo',
        'temperature': 0.8,
        'maxTokens': 1024,
        'maxResults': 1,
        'apiKey': '',
        'service': 'openai',
        'embeddingsIndex': '',
        'stop': '',
        'clientId': os.urandom(6).hex()
    }

    response = requests.post('https://chatgptlogin.ac/wp-json/ai-chatbot/v1/chat',
                             headers=headers, json=json_data)

    return response.json()['reply']

### `get_nonce`

```python
def get_nonce():
    """
    Получает одноразовый токен (nonce) с веб-сайта chatgptlogin.ac.
    Используется для защиты от CSRF атак.

    Returns:
        str: Одноразовый токен.

    Как работает функция:
    1. Функция `get_nonce` выполняет GET-запрос к `https://chatgptlogin.ac/use-chatgpt-free/` с определенными заголовками.
    2. Извлекает значение атрибута `src` тега `<script>`, содержащего nonce, с использованием регулярного выражения.
    3. Декодирует base64-encoded часть URL, содержащего nonce.
    4. Извлекает сам nonce с использованием другого регулярного выражения.
    5. Возвращает извлеченный nonce.
    """
    res = requests.get('https://chatgptlogin.ac/use-chatgpt-free/', headers={
        "Referer": "https://chatgptlogin.ac/use-chatgpt-free/",
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    })

    src = re.search(r'class="mwai-chat mwai-chatgpt">.*<span>Send</span></button></div></div></div> <script defer src="(.*?)">', res.text).group(1)
    decoded_string = base64.b64decode(src.split(",")[-1]).decode('utf-8')
    return re.search(r"let restNonce = \'(.*?)\';", decoded_string).group(1)
```

### `transform`

```python
def transform(messages: list) -> list:
    """
    Преобразует список сообщений в формат, ожидаемый API.
    Кодирует HTML-специальные символы в содержимом сообщений.

    Args:
        messages (list): Список сообщений для преобразования. Каждое сообщение должно быть словарем с ключами "role" и "content".

    Returns:
        list: Преобразованный список сообщений.

    Внутренние функции:
        html_encode(string: str) -> str: Экранирует HTML-специальные символы в строке.

    Как работает функция:
    1. Функция `transform` принимает список сообщений.
    2. Для каждого сообщения создает новый словарь с ключами 'id', 'role', 'content', 'who' и 'html'.
       - 'id' генерируется случайным образом.
       - 'role' и 'content' копируются из входного сообщения.
       - 'who' зависит от роли ('AI: ' или 'User: ').
       - 'html' получается путем вызова внутренней функции `html_encode` для экранирования содержимого.
    3. Возвращает новый список преобразованных сообщений.
    """
    def html_encode(string: str) -> str:
        """
        Экранирует HTML-специальные символы в строке.

        Args:
            string (str): Строка для экранирования.

        Returns:
            str: Экранированная строка.
        """
        table = {
            '"': '&quot;',
            "'": '&#39;',
            '&': '&amp;',
            '>': '&gt;',
            '<': '&lt;',
            '\n': '<br>',
            '\t': '&nbsp;&nbsp;&nbsp;&nbsp;',
            ' ': '&nbsp;'
        }

        for key in table:
            string = string.replace(key, table[key])

        return string

    return [{'id': os.urandom(6).hex(),
             'role': message['role'],
             'content': message['content'],
             'who': 'AI: ' if message['role'] == 'assistant' else 'User: ',
             'html': html_encode(message['content'])} for message in messages]
```

### `html_encode`

```python
def html_encode(string: str) -> str:
    """
    Экранирует HTML-специальные символы в строке.

    Args:
        string (str): Строка для экранирования.

    Returns:
        str: Экранированная строка.

    Как работает функция:
    1. Функция `html_encode` принимает строку в качестве аргумента.
    2. Определяет словарь `table`, содержащий соответствия между символами и их HTML-эквивалентами.
    3. Итерируется по словарю `table`.
    4. Заменяет каждый символ в строке на его HTML-эквивалент.
    5. Возвращает экранированную строку.
    """
    table = {
        '"': '&quot;',
        "'": '&#39;',
        '&': '&amp;',
        '>': '&gt;',
        '<': '&lt;',
        '\n': '<br>',
        '\t': '&nbsp;&nbsp;&nbsp;&nbsp;',
        ' ': '&nbsp;'
    }

    for key in table:
        string = string.replace(key, table[key])

    return string
```

## Переменные

### `url`

```python
url = 'https://chatgptlogin.ac'
```

URL сервиса chatgptlogin.ac.

### `model`

```python
model = ['gpt-3.5-turbo']
```

Список поддерживаемых моделей (в данном случае, только "gpt-3.5-turbo").

### `supports_stream`

```python
supports_stream = False
```

Флаг, указывающий, поддерживает ли провайдер потоковую передачу данных. В данном случае, не поддерживает.

### `needs_auth`

```python
needs_auth = False
```

Флаг, указывающий, требуется ли авторизация для использования провайдера. В данном случае, не требуется.

### `params`

```python
params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join(
        [f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
```

Строка, содержащая информацию о поддерживаемых типах параметров функции `_create_completion`.
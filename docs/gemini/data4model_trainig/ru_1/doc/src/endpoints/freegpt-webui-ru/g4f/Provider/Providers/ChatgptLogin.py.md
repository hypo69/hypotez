# Модуль `ChatgptLogin.py`

## Обзор

Модуль предоставляет реализацию провайдера `ChatgptLogin` для взаимодействия с `ChatGPT` через веб-интерфейс `chatgptlogin.ac`. Он содержит функции для создания запросов к `ChatGPT` и получения ответов. Модуль использует библиотеки `requests`, `re` и `base64` для выполнения `HTTP`-запросов, обработки текста и кодирования данных.

## Подробней

Этот модуль предназначен для интеграции с `ChatGPT` через веб-сайт `chatgptlogin.ac`. Он автоматизирует процесс отправки запросов и получения ответов от `ChatGPT`, используя `HTTP`-запросы и обработку `HTML`. Модуль включает функции для получения `nonce`, преобразования сообщений и создания `JSON`-данных для запроса.

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """
    Создает запрос к ChatGPTLogin и возвращает ответ.

    Args:
        model (str): Модель для использования.
        messages (list): Список сообщений для отправки.
        stream (bool): Флаг, указывающий, использовать ли потоковую передачу.
        **kwargs: Дополнительные аргументы.

    Returns:
        str: Ответ от ChatGPTLogin.

    **Внутренние функции**:

    ### `get_nonce`

    ```python
    def get_nonce():
        """
        Получает nonce с веб-сайта chatgptlogin.ac.

        Returns:
            str: Nonce.
        """
    ```

    **Как работает функция**:
    - Функция отправляет `GET`-запрос к `https://chatgptlogin.ac/use-chatgpt-free/` для получения значения `nonce`, необходимого для последующих запросов.
    - Использует библиотеку `requests` для выполнения `HTTP`-запроса.
    - Извлекает значение `nonce` из `HTML`-кода ответа, используя регулярные выражения и `base64` декодирование.
    - Возвращает извлеченное значение `nonce`.

    ### `transform`

    ```python
    def transform(messages: list) -> list:
        """
        Преобразует список сообщений в формат, необходимый для запроса к ChatGPTLogin.

        Args:
            messages (list): Список сообщений для преобразования.

        Returns:
            list: Преобразованный список сообщений.
        """
    ```

    **Внутренние функции**:

    #### `html_encode`

    ```python
    def html_encode(string: str) -> str:
        """
        Преобразует специальные символы в HTML-сущности.

        Args:
            string (str): Строка для преобразования.

        Returns:
            str: Преобразованная строка.
        """
    ```

    **Как работает функция**:
    - Функция принимает строку и заменяет специальные символы (`"`, `'`, `&`, `>`, `<`, `\n`, `\t`, ` `) на соответствующие `HTML`-сущности.
    - Использует словарь `table` для хранения соответствий между символами и их `HTML`-эквивалентами.
    - Выполняет замену символов в строке и возвращает преобразованную строку.

    **Как работает функция `transform`**:
    - Функция принимает список сообщений и преобразует каждое сообщение в формат, необходимый для запроса к `ChatGPTLogin`.
    - Добавляет случайный `id` к каждому сообщению.
    - Добавляет ключи `role`, `content`, `who`, `html` к каждому сообщению.
    - Кодирует `HTML` содержимое каждого сообщения с помощью функции `html_encode`.
    - Возвращает преобразованный список сообщений.

    **Как работает функция `_create_completion`**:
    - Функция создает `HTTP`-запрос к `chatgptlogin.ac` для получения ответа от `ChatGPT`.
    - Определяет функцию `get_nonce` для получения значения `nonce`.
    - Определяет функцию `transform` для преобразования списка сообщений.
    - Формирует заголовки `HTTP`-запроса, включая `nonce`, полученный с помощью `get_nonce`.
    - Преобразует список сообщений с помощью `transform`.
    - Формирует `JSON`-данные для запроса, включая преобразованные сообщения.
    - Отправляет `POST`-запрос к `https://chatgptlogin.ac/wp-json/ai-chatbot/v1/chat` с заголовками и `JSON`-данными.
    - Извлекает ответ из `JSON`-ответа и возвращает его.

    **Примеры**:
    ```python
    messages = [{"role": "user", "content": "Hello, ChatGPT!"}]
    response = _create_completion(model="gpt-3.5-turbo", messages=messages, stream=False)
    print(response)
    ```
    """
    def get_nonce():
        res = requests.get('https://chatgptlogin.ac/use-chatgpt-free/', headers={
            "Referer": "https://chatgptlogin.ac/use-chatgpt-free/",
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        })

        src = re.search(r'class="mwai-chat mwai-chatgpt">.*<span>Send</span></button></div></div></div> <script defer src="(.*?)">', res.text).group(1)
        decoded_string = base64.b64decode(src.split(",")[-1]).decode('utf-8')
        return re.search(r"let restNonce = '(.*?)';", decoded_string).group(1)
    
    def transform(messages: list) -> list:
        def html_encode(string: str) -> str:
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
        
        return [{
            'id': os.urandom(6).hex(),
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
```

### `params`

```python
params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join(
        [f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
```

**Назначение**:

Формирует строку с информацией о поддерживаемых параметрах функции `_create_completion`.

**Как работает**:

- Использует f-строку для создания строки, содержащей имя текущего файла (без расширения `.py`) и информацию о поддерживаемых параметрах функции `_create_completion`.
- Извлекает имена параметров и их типы из аннотаций типов функции `_create_completion` с помощью `get_type_hints`.
- Форматирует имена параметров и их типы в виде строки `name: type`.
- Объединяет отформатированные параметры в строку, разделенную запятыми.

**Примеры**:

```python
print(params)
# g4f.Providers.ChatgptLogin supports: (model: str, messages: list, stream: bool, kwargs: dict)
```
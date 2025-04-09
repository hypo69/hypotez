# Модуль `ChatgptAi.py`

## Обзор

Модуль предназначен для взаимодействия с моделью GPT-4 через веб-сервис chatgpt.ai. Он предоставляет функцию `_create_completion`, которая отправляет запросы к API chatgpt.ai и возвращает ответ модели.

## Подробнее

Модуль содержит настройки для подключения к API `chatgpt.ai`.

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """Функция отправляет запрос к API chatgpt.ai и возвращает ответ модели.

    Args:
        model (str): Идентификатор используемой модели.
        messages (list): Список сообщений в формате [{"role": "user" | "assistant" | "system", "content": "text"}]
        stream (bool): Определяет, возвращать ли ответ в виде потока.
        **kwargs: Дополнительные аргументы.

    Yields:
        str: Ответ модели.

    Raises:
        requests.exceptions.RequestException: Если возникает ошибка при отправке запроса к API.
        KeyError: Если в ответе API отсутствует поле 'data'.

    Как работает функция:
    1.  Формирует строку `chat`, объединяя сообщения из входного списка `messages`, добавляя роль и содержимое каждого сообщения.
    2.  Выполняет GET-запрос к `https://chatgpt.ai/gpt-4/` для получения данных `nonce`, `post_id`, `bot_id`, необходимых для последующего POST-запроса.
    3.  Извлекает значения `nonce`, `post_id`, `bot_id` с использованием регулярного выражения из текста ответа на GET-запрос.
    4.  Формирует заголовки `headers` для POST-запроса, включая `authority`, `accept`, `origin` и другие необходимые параметры.
    5.  Формирует данные `data` для POST-запроса, включая `_wpnonce`, `post_id`, `message` (сформированная строка `chat`) и `bot_id`.
    6.  Выполняет POST-запрос к `https://chatgpt.ai/wp-admin/admin-ajax.php` с использованием сформированных заголовков и данных.
    7.  Извлекает данные из JSON-ответа и возвращает их с помощью `yield`.

    Внутренние функции:
    - Нет

    ASCII flowchart:

    Формирование запроса
    │
    └──> GET-запрос к chatgpt.ai/gpt-4/ -> Получение nonce, post_id, bot_id
    │
    └──> Формирование headers и data для POST-запроса
    │
    └──> POST-запрос к chatgpt.ai/wp-admin/admin-ajax.php -> Получение ответа от API
    │
    └──> Извлечение данных из JSON-ответа
    │
    └──> Выдача результата

    Примеры:
        >>> messages = [{"role": "user", "content": "Hello, GPT-4!"}]
        >>> for response in _create_completion(model="gpt-4", messages=messages, stream=False):
        ...     print(response)
        Привет! Чем я могу помочь вам сегодня?
    """
    chat = ''
    for message in messages:
        chat += '%s: %s\n' % (message['role'], message['content'])
    chat += 'assistant: '

    response = requests.get('https://chatgpt.ai/gpt-4/')

    nonce, post_id, _, bot_id = re.findall(r'data-nonce="(.*)"\n     data-post-id="(.*)"\n     data-url="(.*)"\n     data-bot-id="(.*)"\n     data-width', response.text)[0]

    headers = {
        'authority': 'chatgpt.ai',
        'accept': '*/*',
        'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
        'cache-control': 'no-cache',
        'origin': 'https://chatgpt.ai',
        'pragma': 'no-cache',
        'referer': 'https://chatgpt.ai/gpt-4/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
    data = {
        '_wpnonce': nonce,
        'post_id': post_id,
        'url': 'https://chatgpt.ai/gpt-4',
        'action': 'wpaicg_chat_shortcode_message',
        'message': chat,
        'bot_id': bot_id
    }

    response = requests.post('https://chatgpt.ai/wp-admin/admin-ajax.php', 
                            headers=headers, data=data)

    yield (response.json()['data'])

```

### `params`

```python
params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
```

Содержит строку с информацией о поддерживаемых параметрах функции `_create_completion`.
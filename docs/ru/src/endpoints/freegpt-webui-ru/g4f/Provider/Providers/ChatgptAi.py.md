# Модуль `ChatgptAi.py`

## Обзор

Модуль предоставляет реализацию взаимодействия с моделью GPT-4 через веб-сайт chatgpt.ai. Он содержит функцию `_create_completion`, которая отправляет запросы к API чата и возвращает ответы.

## Подробнее

Модуль предназначен для использования в проекте `hypotez` в качестве одного из провайдеров для доступа к языковым моделям. Он использует библиотеки `requests` для выполнения HTTP-запросов и `re` для извлечения данных из HTML-страницы. Модуль определяет параметры, такие как URL, поддерживаемые модели и необходимость аутентификации.

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """ Функция отправляет запросы к API чата на chatgpt.ai и возвращает ответ модели.

    Args:
        model (str): Идентификатор используемой модели.
        messages (list): Список сообщений в формате [{"role": "user" | "assistant", "content": "text"}].
        stream (bool): Флаг, указывающий на необходимость потоковой передачи данных.
        **kwargs: Дополнительные параметры.

    Returns:
        Generator[str, None, None]: Генератор, возвращающий ответ модели.

    Raises:
        requests.exceptions.RequestException: В случае ошибки при выполнении HTTP-запроса.
        re.exceptions.ReError: В случае ошибки регулярного выражения.

    Как работает функция:
    1. Формирует строку `chat`, объединяя сообщения из параметра `messages` в формате "role: content".
    2. Выполняет GET-запрос к `https://chatgpt.ai/gpt-4/` для получения значений `nonce`, `post_id`, `_`, `bot_id`, необходимых для последующего POST-запроса.
    3. Извлекает значения `nonce`, `post_id`, `_`, `bot_id` с использованием регулярных выражений из текста ответа на GET-запрос.
    4. Определяет заголовки `headers` для POST-запроса, включая `authority`, `accept`, `origin` и другие параметры.
    5. Формирует данные `data` для POST-запроса, включая `_wpnonce`, `post_id`, `url`, `action`, `message` и `bot_id`.
    6. Выполняет POST-запрос к `https://chatgpt.ai/wp-admin/admin-ajax.php` с использованием заголовков `headers` и данных `data`.
    7. Извлекает данные из JSON-ответа и возвращает их в виде генератора.

    Внутренние функции:
    - Отсутствуют

    ASCII Flowchart:
    Формирование сообщения -> GET-запрос -> Извлечение данных -> POST-запрос -> Получение ответа
    Сообщение --> GET --> Данные --> POST --> Ответ

    Примеры:
        Пример 1:
        messages = [{"role": "user", "content": "Hello, how are you?"}]
        for response in _create_completion(model="gpt-4", messages=messages, stream=False):
            print(response)

        Пример 2:
        messages = [{"role": "user", "content": "Tell me a joke."}, {"role": "assistant", "content": "Why don't scientists trust atoms? Because they make up everything!"}]
        for response in _create_completion(model="gpt-4", messages=messages, stream=False, temperature=0.7):
            print(response)
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
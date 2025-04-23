### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код реализует функцию `_create_completion`, которая отправляет запрос к сайту `chatgpt.ai` для получения ответа от модели `gpt-4` на основе предоставленных сообщений. Он извлекает необходимые параметры (nonce, post_id, bot_id) из HTML-кода страницы и отправляет POST-запрос с сообщением пользователя, чтобы получить ответ от модели.

Шаги выполнения
-------------------------
1. **Формирование сообщения для чата**:
   - Функция `_create_completion` принимает список сообщений (`messages`) и преобразует их в строку `chat`, объединяя роль и содержание каждого сообщения.
   - Добавляет префикс "assistant: " к строке чата.

2. **Получение параметров nonce, post_id, bot_id**:
   - Отправляет GET-запрос к `https://chatgpt.ai/gpt-4/`.
   - Извлекает значения `nonce`, `post_id` и `bot_id` из HTML-ответа, используя регулярное выражение. Эти параметры необходимы для последующего POST-запроса.

3. **Формирование заголовков (headers) и данных (data) для POST-запроса**:
   - Определяет заголовки, включая `user-agent`, `referer` и другие необходимые для имитации запроса от браузера.
   - Формирует данные для POST-запроса, включая `_wpnonce`, `post_id`, `url`, `action`, `message` и `bot_id`.

4. **Отправка POST-запроса и получение ответа**:
   - Отправляет POST-запрос к `https://chatgpt.ai/wp-admin/admin-ajax.php` с сформированными заголовками и данными.
   - Извлекает данные (`data`) из JSON-ответа и возвращает их как результат генератора.

5. **Определение параметров (`params`)**:
   - Формирует строку `params`, которая содержит информацию о поддерживаемых типах параметров функции `_create_completion`.

Пример использования
-------------------------

```python
import os
import requests, re
from typing import sha256, Dict, get_type_hints

url = 'https://chatgpt.ai/gpt-4/'
model = ['gpt-4']
supports_stream = False
needs_auth = False

def _create_completion(model: str, messages: list, stream: bool, **kwargs):
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

params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])

# Пример вызова функции
messages = [
    {'role': 'user', 'content': 'Hello, who are you?'}
]

for response in _create_completion(model='gpt-4', messages=messages, stream=False):
    print(response)
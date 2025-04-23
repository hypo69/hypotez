Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код реализует взаимодействие с API chatgpt.ai для получения ответов от модели gpt-4. Он отправляет сообщения пользователя в чат и извлекает ответы от ассистента. Код выполняет GET-запрос для получения необходимых параметров nonce, post_id, bot_id из HTML-страницы, а затем отправляет POST-запрос с сообщением пользователя для получения ответа от модели.

Шаги выполнения
-------------------------
1. **Формирование сообщения чата**:
   - Собирает все сообщения из истории `messages` в единую строку `chat`, добавляя роль и содержимое каждого сообщения.
   - Добавляет префикс `'assistant: '` к строке, чтобы указать, что ожидается ответ от ассистента.

2. **Выполнение GET-запроса**:
   - Выполняет GET-запрос к `https://chatgpt.ai/gpt-4/` для получения HTML-контента страницы.
   - Извлекает значения `nonce`, `post_id`, и `bot_id` из HTML-кода с использованием регулярного выражения `re.findall`.

3. **Формирование заголовков и данных для POST-запроса**:
   - Определяет `headers` для POST-запроса, включая `user-agent`, `referer` и другие необходимые параметры.
   - Создает словарь `data` с параметрами, необходимыми для отправки сообщения, такими как `_wpnonce`, `post_id`, `message` и `bot_id`.

4. **Выполнение POST-запроса и получение ответа**:
   - Выполняет POST-запрос к `https://chatgpt.ai/wp-admin/admin-ajax.php` с использованием сформированных `headers` и `data`.
   - Извлекает данные ответа в формате JSON и возвращает поле `data` из JSON-ответа.

5. **Генерация строки параметров**:
   - Создает строку `params`, которая описывает параметры, поддерживаемые функцией `_create_completion`.
   - Использует `get_type_hints` для получения аннотаций типов параметров и форматирует их в строку.

Пример использования
-------------------------

```python
import os
import requests, re
from typing import Dict, get_type_hints

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

# Пример использования функции
messages = [{'role': 'user', 'content': 'Hello, how are you?'}]
model = 'gpt-4'
stream = False
kwargs = {}

for completion in _create_completion(model, messages, stream, **kwargs):
    print(completion)

params = 'g4f.Providers.ChatgptAi supports: ' + \
    '(%s)' % ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
print(params)
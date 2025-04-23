Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет функцию `_create_completion`, которая отправляет запрос к API `chat-gpt.org` для генерации текстового ответа на основе предоставленных сообщений. Функция формирует запрос с использованием истории сообщений, настраивает заголовки и параметры запроса, отправляет POST-запрос и возвращает ответ, полученный от API.

Шаги выполнения
-------------------------
1. **Импорт модулей**: Импортируются необходимые модули `os`, `requests` и типы из пакета `typing`.
2. **Определение URL и модели**: Определяются базовый URL для API (`https://chat-gpt.org/chat`) и поддерживаемая модель (`gpt-3.5-turbo`). Также указывается, что стриминг не поддерживается и аутентификация не требуется.
3. **Формирование тела запроса**:
   - Функция `_create_completion` принимает параметры `model`, `messages`, `stream` и `kwargs`.
   - Формируется строка `base` путем объединения ролей и содержимого сообщений из списка `messages`.
   - Добавляется префикс `'assistant:'` к строке `base`.
4. **Настройка заголовков запроса**:
   - Определяется словарь `headers` с необходимыми HTTP-заголовками для запроса.
5. **Настройка данных запроса**:
   - Определяется словарь `json_data` с сообщением, температурой и штрафами для частотности и присутствия.
6. **Отправка POST-запроса**:
   - Отправляется POST-запрос к API `https://chat-gpt.org/api/text` с использованием библиотеки `requests`.
   - В запросе передаются заголовки `headers` и данные `json_data`.
7. **Обработка ответа**:
   - Извлекается сообщение из JSON-ответа и возвращается с использованием `yield`, что делает функцию генератором.
8. **Параметры**:
   - Формируется строка `params` для описания поддерживаемых параметров функции `_create_completion`.

Пример использования
-------------------------

```python
import os, requests
from typing import sha256, Dict, get_type_hints

url = 'https://chat-gpt.org/chat'
model = ['gpt-3.5-turbo']
supports_stream = False
needs_auth = False

def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    base = ''
    for message in messages:
        base += '%s: %s\n' % (message['role'], message['content'])
    base += 'assistant:'
    
    headers = {
        'authority': 'chat-gpt.org',
        'accept': '*/*',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://chat-gpt.org',
        'pragma': 'no-cache',
        'referer': 'https://chat-gpt.org/chat',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }

    json_data = {
        'message': base,
        'temperature': 1,
        'presence_penalty': 0,
        'top_p': 1,
        'frequency_penalty': 0
    }
    
    response = requests.post('https://chat-gpt.org/api/text', headers=headers, json=json_data)
    yield response.json()['message']

# Пример вызова функции _create_completion
messages = [{'role': 'user', 'content': 'Hello, how are you?'}]
generator = _create_completion(model='gpt-3.5-turbo', messages=messages, stream=False)
for response in generator:
    print(response)

params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
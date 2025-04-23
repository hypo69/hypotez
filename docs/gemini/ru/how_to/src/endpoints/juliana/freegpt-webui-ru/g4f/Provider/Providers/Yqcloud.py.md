Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный код реализует взаимодействие с API `api.aichatos.cloud` для генерации текста на основе модели `gpt-3.5-turbo`. Он отправляет POST-запрос с заданным запросом пользователя и возвращает сгенерированный текст в потоковом режиме.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: Импортируются модули `os`, `time`, `requests`, а также типы `sha256`, `Dict`, `get_type_hints` из пакета `...typing`.
2. **Определение констант**:
   - `url`: URL основного сайта (`https://chat9.yqcloud.top/`).
   - `model`: Список поддерживаемых моделей (`gpt-3.5-turbo`).
   - `supports_stream`: Указывает, поддерживает ли провайдер потоковую передачу (`True`).
   - `needs_auth`: Указывает, требуется ли аутентификация (`False`).
3. **Функция `_create_completion`**:
   - Принимает параметры: `model` (строка), `messages` (список сообщений), `stream` (булево значение) и `**kwargs` (дополнительные аргументы).
   - Формирует HTTP-заголовки для запроса к API.
   - Создает JSON-данные для запроса, включающие промпт пользователя, идентификатор пользователя, флаг сети и другие параметры.
   - Отправляет POST-запрос к `https://api.aichatos.cloud/api/generateStream` с заголовками и JSON-данными, настроив потоковую передачу (`stream=True`).
   - Итерируется по содержимому ответа, полученному по частям (`chunk_size=2046`).
   - Декодирует каждый токен, проверяет, содержит ли он фразу `b'always respond in english'`, и возвращает его, если эта фраза отсутствует.
4. **Параметры**: Формируется строка `params`, содержащая информацию о поддержке типов данных функцией `_create_completion`.

Пример использования
-------------------------

```python
import os
import time
import requests

from typing import sha256, Dict, get_type_hints

url = 'https://chat9.yqcloud.top/'
model = [
    'gpt-3.5-turbo',
]
supports_stream = True
needs_auth = False

def _create_completion(model: str, messages: list, stream: bool, **kwargs):

    headers = {
        'authority': 'api.aichatos.cloud',
        'origin': 'https://chat9.yqcloud.top',
        'referer': 'https://chat9.yqcloud.top/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }

    json_data = {
        'prompt': 'always respond in english | %s' % messages[-1]['content'],
        'userId': f'#/chat/{int(time.time() * 1000)}',
        'network': True,
        'apikey': '',
        'system': '',
        'withoutContext': False,
    }

    response = requests.post('https://api.aichatos.cloud/api/generateStream', headers=headers, json=json_data, stream=True)
    for token in response.iter_content(chunk_size=2046):
        if not b'always respond in english' in token:
            yield (token.decode('utf-8'))

    
# Пример вызова функции _create_completion
messages = [{"role": "user", "content": "Hello, how are you?"}]
for token in _create_completion(model='gpt-3.5-turbo', messages=messages, stream=True):
    print(token, end='')

params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
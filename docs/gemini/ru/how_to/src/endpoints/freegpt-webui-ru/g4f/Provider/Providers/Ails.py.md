### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предоставляет функциональность для взаимодействия с API `ai.ls` для генерации текста с использованием модели `gpt-3.5-turbo`. Он включает функции для форматирования временных меток, создания хешей и отправки запросов к API.

Шаги выполнения
-------------------------
1. **Определение класса `Utils`**:
   - Внутри класса `Utils` определяются два статических метода: `hash` и `format_timestamp`.
     - `hash`: Функция вычисляет SHA256 хеш на основе входных данных JSON и секретного ключа.
     - `format_timestamp`: Функция форматирует временную метку, изменяя последнее число в зависимости от четности.
2. **Определение функции `_create_completion`**:
   - Функция отправляет POST-запрос к API `ai.ls` для генерации текста.
   - Формирует заголовки (`headers`) и параметры (`params`) запроса.
   - Создает JSON-данные (`json_data`), включающие сообщения, модель, температуру и подпись.
   - Отправляет запрос и итерируется по ответу для извлечения контента.
   - Возвращает контент в виде генератора токенов.

Пример использования
-------------------------

```python
import os
import time
import json
import uuid
import random
import hashlib
import requests

from typing import Dict, get_type_hints
from datetime import datetime

url: str = 'https://ai.ls'
model: str = 'gpt-3.5-turbo'
supports_stream = True
needs_auth = False

class Utils:
    def hash(json_data: Dict[str, str]) -> str:
        secretKey: bytearray = bytearray([79, 86, 98, 105, 91, 84, 80, 78, 123, 83,
                                         35, 41, 99, 123, 51, 54, 37, 57, 63, 103, 59, 117, 115, 108, 41, 67, 76])

        base_string: str = '%s:%s:%s:%s' % (
            json_data['t'],
            json_data['m'],
            'WI,2rU#_r:r~aF4aJ36[.Z(/8Rv93Rf',
            len(json_data['m'])
        )
        
        return hashlib.sha256(base_string.encode()).hexdigest()

    def format_timestamp(timestamp: int) -> str:
        e = timestamp
        n = e % 10
        r = n + 1 if n % 2 == 0 else n
        return str(e - n + r)

def _create_completion(model: str, messages: list, temperature: float = 0.6, stream: bool = False, **kwargs):
    headers = {
        'authority': 'api.caipacity.com',
        'accept': '*/*',
        'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
        'authorization': 'Bearer free',
        'client-id': str(uuid.uuid4()),
        'client-v': '0.1.217',
        'content-type': 'application/json',
        'origin': 'https://ai.ls',
        'referer': 'https://ai.ls/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    params = {
        'full': 'false',
    }

    timestamp = Utils.format_timestamp(int(time.time() * 1000))

    sig = {
        'd': datetime.now().strftime('%Y-%m-%d'),
        't': timestamp,
        's': Utils.hash({
            't': timestamp,
            'm': messages[-1]['content']})}

    json_data = json.dumps(separators=(',', ':'), obj={
        'model': 'gpt-3.5-turbo',
        'temperature': 0.6,
        'stream': True,
         'messages': messages} | sig)

    response = requests.post('https://api.caipacity.com/v1/chat/completions', 
                             headers=headers, data=json_data, stream=True)

    for token in response.iter_lines():
        if b'content' in token:
            completion_chunk = json.loads(token.decode().replace('data: ', ''))
            token = completion_chunk['choices'][0]['delta'].get('content')
            if token != None:
                yield token

    
# Пример использования функции _create_completion
messages = [{"role": "user", "content": "Расскажи о Python"}]
for token in _create_completion(model='gpt-3.5-turbo', messages=messages):
    print(token, end="")
```
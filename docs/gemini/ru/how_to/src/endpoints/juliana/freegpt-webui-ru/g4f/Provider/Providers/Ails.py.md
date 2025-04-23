### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предоставляет функциональность для взаимодействия с AI.LS API, в частности, для создания запросов к модели gpt-3.5-turbo и получения ответов. Он включает в себя функции для форматирования временных меток, вычисления хешей и создания запросов к API с использованием библиотеки `requests`. Код также обрабатывает потоковую передачу данных для получения ответов в реальном времени.

Шаги выполнения
-------------------------
1. **Определение класса `Utils`**:
   - Класс содержит статические методы `hash` и `format_timestamp`.
   - `hash` вычисляет SHA256-хеш на основе входных данных, используя секретный ключ и форматированную строку.
   - `format_timestamp` форматирует временную метку, изменяя последнее число в зависимости от его чётности.

2. **Функция `_create_completion`**:
   - Принимает параметры, такие как модель, список сообщений, температуру и флаг потоковой передачи.
   - Формирует заголовки запроса, включая Client ID, User-Agent и Authorization.
   - Создает JSON-данные для отправки в API, включая сообщения, временную метку и подпись.
   - Отправляет POST-запрос к API `https://api.caipacity.com/v1/chat/completions` с использованием библиотеки `requests`.
   - Обрабатывает ответ, извлекая контент из каждого чанка данных и генерируя токены.

3. **Обработка потоковой передачи**:
   - Использует `response.iter_lines()` для чтения потока данных ответа.
   - Извлекает JSON-данные из каждого токена, удаляя префикс `data: `.
   - Извлекает контент из поля `content` в структуре JSON и генерирует его.

4. **Параметры**:
   - Определяет строку `params`, содержащую информацию о типах параметров функции `_create_completion`.

Пример использования
-------------------------

```python
import os
import time
import json
import uuid
import hashlib
import requests

from ...typing import sha256, Dict, get_type_hints
from datetime import datetime

url: str = 'https://ai.ls'
model: str = 'gpt-3.5-turbo'
supports_stream = True
needs_auth = False

class Utils:
    def hash(json_data: Dict[str, str]) -> sha256:

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

# Пример вызова функции
messages = [{"role": "user", "content": "Hello, who are you?"}]
for token in _create_completion(model="gpt-3.5-turbo", messages=messages):
    print(token, end="")
### **Как использовать этот блок кода**

=========================================================================================

Описание
-------------------------
Этот код предоставляет реализацию взаимодействия с API `chat.getgpt.world` для получения ответов от модели `gpt-3.5-turbo`. Он включает в себя функции для шифрования данных, формирования запроса и обработки потоковых ответов.

Шаги выполнения
-------------------------
1. **Определение функций шифрования**:
   - Функция `encrypt(e)` шифрует входные данные `e` с использованием алгоритма AES. Она генерирует случайные векторы инициализации и соли, шифрует данные с дополнением и возвращает шестнадцатеричное представление зашифрованного текста вместе с векторами инициализации и соли.
   - Функция `pad_data(data)` дополняет входные данные до размера блока AES, чтобы обеспечить правильное шифрование.

2. **Формирование заголовков запроса**:
   - Определяются заголовки HTTP-запроса, включающие `Content-Type`, `Referer` и `user-agent`.

3. **Формирование данных запроса**:
   - Создается JSON-объект с параметрами запроса, такими как сообщения, параметры штрафов, максимальное количество токенов, модель, температура и другие параметры. Также генерируется уникальный UUID для идентификации запроса.

4. **Отправка запроса и обработка потока ответов**:
   - Отправляется POST-запрос на `https://chat.getgpt.world/api/chat/stream` с зашифрованными данными.
   - Функция `_create_completion` итерируется по строкам потокового ответа, извлекает содержимое из JSON-строк и генерирует его.

Пример использования
-------------------------

```python
import os
import json
import uuid
import requests
from Crypto.Cipher import AES
from typing import Dict, get_type_hints

url = 'https://chat.getgpt.world/'
model = ['gpt-3.5-turbo']
supports_stream = True
needs_auth = False

def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    def encrypt(e):
        t = os.urandom(8).hex().encode('utf-8')
        n = os.urandom(8).hex().encode('utf-8')
        r = e.encode('utf-8')
        cipher = AES.new(t, AES.MODE_CBC, n)
        ciphertext = cipher.encrypt(pad_data(r))
        return ciphertext.hex() + t.decode('utf-8') + n.decode('utf-8')

    def pad_data(data: bytes) -> bytes:
        block_size = AES.block_size
        padding_size = block_size - len(data) % block_size
        padding = bytes([padding_size] * padding_size)
        return data + padding

    headers = {
        'Content-Type': 'application/json',
        'Referer': 'https://chat.getgpt.world/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    data = json.dumps({
        'messages': messages,
        'frequency_penalty': kwargs.get('frequency_penalty', 0),
        'max_tokens': kwargs.get('max_tokens', 4000),
        'model': 'gpt-3.5-turbo',
        'presence_penalty': kwargs.get('presence_penalty', 0),
        'temperature': kwargs.get('temperature', 1),
        'top_p': kwargs.get('top_p', 1),
        'stream': True,
        'uuid': str(uuid.uuid4())
    })

    res = requests.post('https://chat.getgpt.world/api/chat/stream', 
                        headers=headers, json={'signature': encrypt(data)}, stream=True)

    for line in res.iter_lines():
        if b'content' in line:
            line_json = json.loads(line.decode('utf-8').split('data: ')[1])
            yield (line_json['choices'][0]['delta']['content'])


# Пример использования функции _create_completion
messages = [{"role": "user", "content": "Привет, как дела?"}]
for chunk in _create_completion(model='gpt-3.5-turbo', messages=messages, stream=True):
    print(chunk, end="")

params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join(
        [f'{name}: {get_type_hints(_create_completion)[name].__name__}' for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
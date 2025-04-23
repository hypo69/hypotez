### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный код предоставляет класс `Client` для взаимодействия с API Vercel для генерации текста с использованием различных моделей машинного обучения. Он включает в себя методы для получения токена аутентификации, формирования параметров запроса и отправки запросов на генерацию текста. Также определена функция `_create_completion` для создания диалоговых завершений на основе истории сообщений.

Шаги выполнения
-------------------------
1. **Инициализация клиента**: Создается экземпляр класса `Client`, который инициализирует сессию `requests` и устанавливает заголовки запроса.
2. **Получение токена**: Метод `get_token` отправляет запрос на `https://sdk.vercel.ai/openai.jpeg`, декодирует полученный base64-encoded JSON, компилирует JavaScript код из полученных данных и выполняет его для получения токена, который затем кодируется в base64.
3. **Получение параметров по умолчанию**: Метод `get_default_params` извлекает параметры по умолчанию для указанной модели из словаря `vercel_models`.
4. **Генерация текста**: Метод `generate` принимает идентификатор модели, промпт и параметры, объединяет их с параметрами по умолчанию, добавляет токен в заголовки и отправляет POST-запрос на `https://sdk.vercel.ai/api/generate`. Ответ возвращается в виде потока чанков.
5. **Создание диалогового завершения**: Функция `_create_completion` формирует строку диалога из списка сообщений, отправляет запрос на генерацию текста с использованием метода `generate` класса `Client` и возвращает токены завершения в виде генератора.

Пример использования
-------------------------

```python
import os
import json
import base64
import execjs
import queue
import threading

from curl_cffi import requests

class Client:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Te': 'trailers',
            'Upgrade-Insecure-Requests': '1'
        }
        self.session.headers.update(self.headers)

    def get_token(self):
            b64 = self.session.get('https://sdk.vercel.ai/openai.jpeg').text
            data = json.loads(base64.b64decode(b64))

            code = 'const globalThis = {data: `sentinel`}; function token() {return (%s)(%s)}' % (
                data['c'], data['a'])

            token_string = json.dumps(separators=(',', ':'),
                                    obj={'r': execjs.compile(code).call('token'), 't': data['t']})

            return base64.b64encode(token_string.encode()).decode()

    def get_default_params(self, model_id):
        return {key: param['value'] for key, param in vercel_models[model_id]['parameters'].items()}

    def generate(self, model_id: str, prompt: str, params: dict = {}):
        if not ':' in model_id:
            model_id = models[model_id]

        defaults = self.get_default_params(model_id)

        payload = defaults | params | {
            'prompt': prompt,
            'model': model_id,
        }

        headers = self.headers | {
            'Accept-Encoding': 'gzip, deflate, br',
            'Custom-Encoding': self.get_token(),
            'Host': 'sdk.vercel.ai',
            'Origin': 'https://sdk.vercel.ai',
            'Referrer': 'https://sdk.vercel.ai',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }

        chunks_queue = queue.Queue()
        error = None
        response = None

        def callback(data):
            chunks_queue.put(data.decode())

        def request_thread():
            nonlocal response, error
            for _ in range(3):
                try:
                    response = self.session.post('https://sdk.vercel.ai/api/generate',
                                                 json=payload, headers=headers, content_callback=callback)
                    response.raise_for_status()

                except Exception as e:
                    if _ == 2:
                        error = e

                    else:
                        continue

        thread = threading.Thread(target=request_thread, daemon=True)
        thread.start()

        text = ''
        index = 0
        while True:
            try:
                chunk = chunks_queue.get(block=True, timeout=0.1)

            except queue.Empty:
                if error:
                    raise error

                elif response:
                    break

                else:
                    continue

            text += chunk
            lines = text.split('\n')

            if len(lines) - 1 > index:
                new = lines[index:-1]
                for word in new:
                    yield json.loads(word)
                index = len(lines) - 1

def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    conversation = 'This is a conversation between a human and a language model, respond to the last message accordingly, referring to the past history of messages if needed.\n'
    
    for message in messages:
        conversation += '%s: %s\n' % (message['role'], message['content'])
    
    conversation += 'assistant: '
    
    completion = Client().generate(model, conversation)

    for token in completion:
        yield token

# Пример использования
model_name = "claude-instant-v1"  # или любой другой поддерживаемый model_id
messages = [{"role": "user", "content": "Hello, how are you?"}]

# Генерация ответа
for token in _create_completion(model_name, messages, stream=True):
    print(token, end="")
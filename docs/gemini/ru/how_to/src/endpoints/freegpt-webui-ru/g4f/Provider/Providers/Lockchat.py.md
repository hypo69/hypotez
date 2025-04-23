### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода реализует функцию `_create_completion`, которая отправляет запросы к API Lockchat для генерации ответов на основе предоставленных сообщений и модели. Он также обрабатывает стриминговый вывод ответов и ошибки, такие как отсутствие запрошенной модели.

Шаги выполнения
-------------------------
1. **Определение параметров запроса**:
   - Формируется `payload` (полезная нагрузка) с параметрами, необходимыми для запроса к API, такими как температура, сообщения, модель и флаг стриминга.

2. **Установка заголовков**:
   - Устанавливаются заголовки запроса, включая `user-agent`, который идентифицирует клиентское приложение.

3. **Отправка запроса к API**:
   - Выполняется POST-запрос к API Lockchat (`http://super.lockchat.app/v1/chat/completions?auth=FnMNPlwZEnGFqvEc9470Vw==`) с использованием библиотеки `requests`. Запрос отправляется в стриминговом режиме (`stream=True`).

4. **Обработка стримингового ответа**:
   - Функция итерируется по строкам ответа, полученного от API.

5. **Проверка на ошибки**:
   - Проверяется наличие сообщения об ошибке, указывающего на отсутствие запрошенной модели (`The model: \`gpt-4\` does not exist`). Если ошибка обнаружена, функция выводит сообщение в консоль и рекурсивно вызывает себя для повторной попытки запроса.

6. **Извлечение содержимого**:
   - Если в строке ответа содержится `"content"`, строка декодируется из формата UTF-8, разделяется по строке `data: `, извлекается JSON-объект, и из него извлекается текст ответа из поля `content`.

7. **Генерация токенов**:
   - Если извлеченный токен не пустой, он возвращается через `yield`, что позволяет использовать функцию как генератор.

Пример использования
-------------------------

```python
import requests
import os
import json
from typing import get_type_hints

url = 'http://super.lockchat.app'
model = ['gpt-4', 'gpt-3.5-turbo']
supports_stream = True
needs_auth = False

def _create_completion(model: str, messages: list, stream: bool, temperature: float = 0.7, **kwargs):

    payload = {
        "temperature": 0.7,
        "messages": messages,
        "model": model,
        "stream": True,
    }
    headers = {
        "user-agent": "ChatX/39 CFNetwork/1408.0.4 Darwin/22.5.0",
    }
    response = requests.post("http://super.lockchat.app/v1/chat/completions?auth=FnMNPlwZEnGFqvEc9470Vw==", 
                            json=payload, headers=headers, stream=True)
    for token in response.iter_lines():
        if b'The model: `gpt-4` does not exist' in token:
            print('error, retrying...')
            _create_completion(model=model, messages=messages, stream=stream, temperature=temperature, **kwargs)
        if b"content" in token:
            token = json.loads(token.decode('utf-8').split('data: ')[1])['choices'][0]['delta'].get('content')
            if token: yield (token)
            
    params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
        '(%s)' % ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])

# Пример вызова функции
messages = [{"role": "user", "content": "Hello, how are you?"}]
for token in _create_completion(model="gpt-3.5-turbo", messages=messages, stream=True):
    print(token, end="")
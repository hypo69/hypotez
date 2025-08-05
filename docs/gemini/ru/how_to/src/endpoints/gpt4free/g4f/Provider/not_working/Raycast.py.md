```python
                from __future__ import annotations

import json

import requests

from ...typing import CreateResult, Messages
from ..base_provider import AbstractProvider


class Raycast(AbstractProvider):
    url                     = "https://raycast.com"
    supports_stream         = True
    needs_auth              = True
    working                 = False

    models = [
        "gpt-3.5-turbo",
        "gpt-4"
    ]

    @staticmethod
    def create_completion(
        model: str,
        messages: Messages,
        stream: bool,
        proxy: str = None,
        **kwargs,
    ) -> CreateResult:
        auth = kwargs.get('auth')
        if not auth:
            raise ValueError("Raycast needs an auth token, pass it with the `auth` parameter")

        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Authorization': f'Bearer {auth}',
            'Content-Type': 'application/json',
            'User-Agent': 'Raycast/0 CFNetwork/1410.0.3 Darwin/22.6.0',
        }
        parsed_messages = [
            {'author': message['role'], 'content': {'text': message['content']}}
            for message in messages
        ]
        data = {
            "debug": False,
            "locale": "en-CN",
            "messages": parsed_messages,
            "model": model,
            "provider": "openai",
            "source": "ai_chat",
            "system_instruction": "markdown",
            "temperature": 0.5
        }
        response = requests.post(
            "https://backend.raycast.com/api/v1/ai/chat_completions",
            headers=headers,
            json=data,
            stream=True,
            proxies={"https": proxy}
        )
        for token in response.iter_lines():
            if b'data: ' not in token:
                continue
            completion_chunk = json.loads(token.decode().replace('data: ', ''))
            token = completion_chunk['text']
            if token != None:
                yield token

                ```
```markdown
## Как использовать этот блок кода
=========================================================================================

### Описание
-------------------------
Данный блок кода представляет собой класс `Raycast`, реализующий интерфейс `AbstractProvider` для работы с API Raycast. 
Он позволяет отправлять запросы к модели GPT-3.5-turbo или GPT-4, получать ответы в режиме потоковой передачи и 
использовать аутентификацию для доступа к API.

### Шаги выполнения
-------------------------
1. **Инициализация**: Создается объект класса `Raycast`, передавая в него необходимые параметры.
2. **Аутентификация**: Проверяется наличие токена аутентификации в параметрах. 
3. **Формирование запроса**: Подготавливаются данные для запроса, включая модель, сообщения, 
    прокси-сервер (при необходимости) и прочие параметры. 
4. **Отправка запроса**: Используется `requests.post` для отправки POST-запроса к API Raycast.
5. **Обработка ответа**: 
    - Ответ считывается по частям (в потоковом режиме) с помощью `response.iter_lines()`.
    - Из каждой части ответа извлекается текст, который затем отправляется в качестве результата. 

### Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.Raycast import Raycast

# Токен аутентификации
auth_token = "YOUR_RAYCAST_API_TOKEN"

# Создание объекта класса Raycast
raycast_provider = Raycast(auth=auth_token)

# Сообщения для отправки
messages = [
    {"role": "user", "content": "Привет, как дела?"},
    {"role": "assistant", "content": "У меня все хорошо, спасибо!"},
]

# Отправка запроса к модели GPT-4
for token in raycast_provider.create_completion(model="gpt-4", messages=messages, stream=True):
    print(token)
```
```
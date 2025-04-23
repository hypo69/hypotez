### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код реализует взаимодействие с API Forefront для генерации текста на основе предоставленных сообщений. Он отправляет POST-запросы к API и возвращает сгенерированный текст в виде потока (stream).

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: Импортируются модули `os`, `json`, `requests` и типы из пакета `...typing`.
2. **Определение констант**:
   - `url`: URL веб-сайта Forefront.
   - `model`: Список поддерживаемых моделей (в данном случае `gpt-3.5-turbo`).
   - `supports_stream`: Флаг, указывающий, поддерживает ли провайдер потоковую передачу данных (установлен в `True`).
   - `needs_auth`: Флаг, указывающий, требуется ли аутентификация (установлен в `False`).
3. **Функция `_create_completion`**:
   - Принимает параметры `model` (строка), `messages` (список сообщений) и `stream` (логическое значение).
   - Формирует JSON-данные для отправки в API Forefront. Данные включают:
     - `text`: Последнее сообщение из списка `messages`.
     - `action`: Установлено в `'noauth'`, что указывает на отсутствие аутентификации.
     - `id`, `parentId`, `workspaceId`: Пустые строки.
     - `messagePersona`: Идентификатор персонажа сообщения.
     - `model`: Установлено в `'gpt-4'`.
     - `messages`: Все сообщения из списка `messages`, кроме последнего.
     - `internetMode`: Установлено в `'auto'`.
   - Отправляет POST-запрос к API Forefront (`https://streaming.tenant-forefront-default.knative.chi.coreweave.com/free-chat`) с использованием библиотеки `requests`.
   - Итерируется по строкам ответа, полученного от API (`response.iter_lines()`).
   - Если строка содержит `b'delta'`, она декодируется и извлекается полезная нагрузка JSON, после чего передается как часть потока.
4. **Параметры `params`**:
   - Формируется строка с информацией о поддерживаемых типах параметров функции `_create_completion`.

Пример использования
-------------------------

```python
import os
import json
import requests
from typing import Dict, get_type_hints

url = 'https://forefront.com'
model = ['gpt-3.5-turbo']
supports_stream = True
needs_auth = False

def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    json_data = {
        'text': messages[-1]['content'],
        'action': 'noauth',
        'id': '',
        'parentId': '',
        'workspaceId': '',
        'messagePersona': '607e41fe-95be-497e-8e97-010a59b2e2c0',
        'model': 'gpt-4',
        'messages': messages[:-1] if len(messages) > 1 else [],
        'internetMode': 'auto'
    }
    response = requests.post( 'https://streaming.tenant-forefront-default.knative.chi.coreweave.com/free-chat',
        json=json_data, stream=True)
    for token in response.iter_lines(): 
        if b'delta' in token:
            token = json.loads(token.decode().split('data: ')[1])['delta']
            yield (token)
# Пример вызова функции _create_completion
messages = [{"role": "user", "content": "Hello, Forefront!"}]
for token in _create_completion(model='gpt-3.5-turbo', messages=messages, stream=True):
    print(token, end='')
```
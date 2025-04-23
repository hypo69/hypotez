### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода предназначен для взаимодействия с API Forefront. Он отправляет запрос к API для генерации текста на основе предоставленных сообщений и настроек модели, а затем возвращает сгенерированный текст по частям в режиме реального времени.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: Импортируются модули `os`, `json`, `requests` и необходимые типы из библиотеки `typing`.
2. **Определение глобальных переменных**:
   - `url`: URL сайта Forefront.
   - `model`: Список поддерживаемых моделей (`gpt-3.5-turbo`).
   - `supports_stream`: Указывает, поддерживает ли провайдер потоковую передачу данных (`True`).
   - `needs_auth`: Указывает, требуется ли аутентификация (`False`).
3. **Функция `_create_completion`**:
   - Принимает параметры: `model` (модель для генерации), `messages` (список сообщений), `stream` (флаг потоковой передачи) и дополнительные аргументы `kwargs`.
   - Формирует JSON-данные для запроса к API Forefront, включая текст последнего сообщения, параметры идентификации, настройки модели и историю сообщений.
   - Отправляет POST-запрос к API (`https://streaming.tenant-forefront-default.knative.chi.coreweave.com/free-chat`) с использованием библиотеки `requests` и потоковой передачи.
   - Итерируется по строкам ответа, извлекая и декодируя полезные данные (`delta`) из каждой строки, если в ней содержится `b'delta'`.
   - Возвращает сгенерированные токены по частям с использованием `yield`.
4. **Параметры**
   - Сохраняет в `params` информацию о поддержке типов данных для функции `_create_completion`.

Пример использования
-------------------------

```python
import os
import json
import requests
from typing import sha256, Dict, get_type_hints

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
    response = requests.post(
        'https://streaming.tenant-forefront-default.knative.chi.coreweave.com/free-chat',
        json=json_data, stream=True)
    for token in response.iter_lines():
        if b'delta' in token:
            token = json.loads(token.decode().split('data: ')[1])['delta']
            yield (token)

params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '({})'.format(', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]]))

# Пример использования функции _create_completion
messages = [{"role": "user", "content": "Hello, how are you?"}]
for token in _create_completion(model='gpt-3.5-turbo', messages=messages, stream=True):
    print(token, end='')
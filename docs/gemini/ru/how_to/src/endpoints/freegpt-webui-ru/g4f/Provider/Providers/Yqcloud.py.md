Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предоставляет интерфейс для взаимодействия с моделью `gpt-3.5-turbo` через API `api.aichatos.cloud`. Он отправляет запросы к API и возвращает сгенерированный текст.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются модули `os`, `time`, `requests`.
   - Импортируются типы данных `sha256`, `Dict`, `get_type_hints` из модуля `...typing`.
2. **Определение глобальных переменных**:
   - `url`: URL для взаимодействия с API (`https://chat9.yqcloud.top/`).
   - `model`: Список поддерживаемых моделей (в данном случае `gpt-3.5-turbo`).
   - `supports_stream`: Флаг, указывающий на поддержку потоковой передачи данных (установлен в `True`).
   - `needs_auth`: Флаг, указывающий на необходимость аутентификации (установлен в `False`).
3. **Определение функции `_create_completion`**:
   - Функция принимает аргументы: `model` (модель для генерации), `messages` (список сообщений), `stream` (флаг потоковой передачи) и `**kwargs` (дополнительные аргументы).
   - Формируются заголовки `headers` для HTTP-запроса.
   - Формируются данные `json_data` для отправки в теле запроса:
     - `prompt`: Содержит текст последнего сообщения из списка `messages` с префиксом `always respond in english`.
     - `userId`: Уникальный идентификатор пользователя, формируемый на основе текущего времени.
     - `network`: Флаг, указывающий на использование сети (установлен в `True`).
     - `apikey`: Пустая строка (предположительно, API key не требуется).
     - `system`: Пустая строка (предположительно, системное сообщение не требуется).
     - `withoutContext`: Флаг, указывающий на отсутствие контекста (установлен в `False`).
   - Отправляется POST-запрос к `https://api.aichatos.cloud/api/generateStream` с использованием `requests.post`.
   - Полученные данные передаются в виде потока (`stream=True`).
   - Для каждого чанка данных, полученного из потока, проверяется наличие строки `always respond in english`. Если её нет, чанк декодируется в UTF-8 и возвращается как часть сгенерированного текста.
4. **Определение строки `params`**:
   - Формируется строка `params`, содержащая информацию о поддерживаемых типах данных для функции `_create_completion`.

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
    """
    Функция отправляет запрос к API для генерации текста на основе предоставленных сообщений.

    Args:
        model (str): Идентификатор модели для генерации текста.
        messages (list): Список сообщений, используемых в качестве входных данных для генерации текста.
        stream (bool): Флаг, указывающий, следует ли возвращать сгенерированный текст в виде потока.
        **kwargs: Дополнительные параметры, которые могут быть переданы в API.

    Returns:
        Generator[str, None, None]: Генератор, который возвращает сгенерированный текст по частям.

    Raises:
        requests.exceptions.RequestException: Если возникает ошибка при отправке запроса к API.
    """
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


# Пример использования функции _create_completion
messages = [{'content': 'Translate to Russian: Hello, how are you?'}]
generator = _create_completion(model='gpt-3.5-turbo', messages=messages, stream=True)
for chunk in generator:
    print(chunk)

params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
print(params)
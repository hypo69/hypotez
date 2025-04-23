Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код реализует взаимодействие с API DeepAI для получения ответов в чат-стиле. Он включает функции для генерации ключа API, отправки запросов к API и обработки потоковых ответов.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются модули `os`, `json`, `random`, `hashlib` и `requests`.
   - Импортируются типы данных `sha256`, `Dict` и функция `get_type_hints` из модуля `...typing`.

2. **Определение констант**:
   - Устанавливается `url` равным `'https://deepai.org'`.
   - Указывается список поддерживаемых моделей `model = ['gpt-3.5-turbo']`.
   - Устанавливается поддержка потоковой передачи данных `supports_stream = True`.
   - Указывается, что для работы не требуется аутентификация `needs_auth = False`.

3. **Функция `_create_completion`**:
   - Определяется функция `_create_completion`, которая принимает аргументы:
     - `model` (строка): Модель для использования.
     - `messages` (список): Список сообщений для отправки.
     - `stream` (логическое значение): Флаг потоковой передачи.
     - `**kwargs`: Дополнительные аргументы.
   - Функция содержит вложенную функцию `md5`, которая вычисляет MD5-хеш строки.
   - Функция содержит вложенную функцию `get_api_key`, которая генерирует ключ API на основе User-Agent.

4. **Генерация заголовков**:
   - Определяется User-Agent:
     ```python
     user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
     ```
   - Создаются заголовки запроса, включающие ключ API и User-Agent:
     ```python
     headers = {
         "api-key": get_api_key(user_agent),
         "user-agent": user_agent
     }
     ```

5. **Формирование данных для запроса**:
   - Создается словарь `files` с данными для отправки:
     ```python
     files = {
         "chat_style": (None, "chat"),
         "chatHistory": (None, json.dumps(messages))
     }
     ```

6. **Отправка запроса и обработка ответа**:
   - Отправляется POST-запрос к API:
     ```python
     r = requests.post("https://api.deepai.org/chat_response", headers=headers, files=files, stream=True)
     ```
   - Итерируемся по чанкам ответа и декодируем их:
     ```python
     for chunk in r.iter_content(chunk_size=None):
         r.raise_for_status()
         yield chunk.decode()
     ```

7. **Параметры**:
   - Формируется строка `params`, содержащая информацию о поддержке типов данных функцией `_create_completion`.

Пример использования
-------------------------

```python
import os
import json
import random
import hashlib
import requests

from typing import sha256, Dict, get_type_hints

url = 'https://deepai.org'
model = ['gpt-3.5-turbo']
supports_stream = True
needs_auth = False

def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    def md5(text: str) -> str:
        return hashlib.md5(text.encode()).hexdigest()[::-1]


    def get_api_key(user_agent: str) -> str:
        part1 = str(random.randint(0, 10**11))
        part2 = md5(user_agent + md5(user_agent + md5(user_agent + part1 + "x")))
        
        return f"tryit-{part1}-{part2}"

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'

    headers = {
        "api-key": get_api_key(user_agent),
        "user-agent": user_agent
    }

    files = {
        "chat_style": (None, "chat"),
        "chatHistory": (None, json.dumps(messages))
    }

    r = requests.post("https://api.deepai.org/chat_response", headers=headers, files=files, stream=True)

    for chunk in r.iter_content(chunk_size=None):
        r.raise_for_status()
        yield chunk.decode()


params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join(
        [f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])

# Пример вызова функции _create_completion
messages = [{"role": "user", "content": "Hello, DeepAI!"}]
for chunk in _create_completion(model="gpt-3.5-turbo", messages=messages, stream=True):
    print(chunk, end="")
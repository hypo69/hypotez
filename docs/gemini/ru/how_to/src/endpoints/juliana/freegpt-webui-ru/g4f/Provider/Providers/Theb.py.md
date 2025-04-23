### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода предназначен для взаимодействия с API Theb.ai для генерации текста на основе предоставленных сообщений и модели. Он использует подпроцесс Python для выполнения вспомогательного скрипта `theb.py`, который отправляет запросы к API Theb.ai.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: Импортируются модули `os`, `json`, `time` и `subprocess`, а также типы данных `sha256` и `Dict` и функция `get_type_hints` из пакета `...typing`.
2. **Определение параметров**: Определяются параметры `url` (URL API Theb.ai), `model` (список поддерживаемых моделей), `supports_stream` (поддержка потоковой передачи) и `needs_auth` (требование аутентификации).
3. **Функция `_create_completion`**:
    - Принимает параметры `model` (модель для генерации), `messages` (список сообщений для отправки) и `stream` (флаг потоковой передачи).
    - Определяет путь к текущему файлу с помощью `os.path.dirname(os.path.realpath(__file__))`.
    - Преобразует параметры `messages` и `model` в JSON-строку с помощью `json.dumps`.
    - Формирует команду для вызова подпроцесса Python, который выполняет скрипт `theb.py` с переданной JSON-конфигурацией.
    - Запускает подпроцесс с помощью `subprocess.Popen`, перенаправляя стандартный вывод в канал.
    - Итерируется по строкам вывода подпроцесса, декодирует их в кодировке UTF-8 и возвращает как генератор.
4. **Параметры**: Определяет строку `params`, содержащую информацию о поддержке параметров функцией `_create_completion`.

Пример использования
-------------------------

```python
    import os
import json
import time
import subprocess

from ...typing import sha256, Dict, get_type_hints

url = 'https://theb.ai'
model = ['gpt-3.5-turbo']
supports_stream = True
needs_auth = False

def _create_completion(model: str, messages: list, stream: bool, **kwargs):

    path = os.path.dirname(os.path.realpath(__file__))
    config = json.dumps({
        'messages': messages,
        'model': model}, separators=(',', ':'))
    
    cmd = ['python3', f'{path}/helpers/theb.py', config]

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    for line in iter(p.stdout.readline, b''):
        yield line.decode('utf-8')
        
params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])

# Пример использования функции _create_completion
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
]
for response in _create_completion(model="gpt-3.5-turbo", messages=messages, stream=True):
    print(response, end="")
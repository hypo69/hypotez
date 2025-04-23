### **Как использовать этот блок кода**

=========================================================================================

Описание
-------------------------
Этот код реализует функцию `_create_completion`, которая отправляет запросы к API Gravityengine для генерации ответов на основе предоставленных сообщений. Функция использует `requests` для отправки POST-запросов и возвращает сгенерированный контент. Также определены параметры для указания поддерживаемых моделей и типов данных.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются модули `json`, `os`, `requests` и `uuid`.
   - Из пакета `...typing` импортируются `sha256`, `Dict` и `get_type_hints`.

2. **Определение глобальных переменных**:
   - `url`: URL-адрес API Gravityengine (`https://gpt4.gravityengine.cc`).
   - `model`: Список поддерживаемых моделей (`gpt-3.5-turbo-16k`, `gpt-3.5-turbo-0613`).
   - `supports_stream`: Флаг, указывающий на поддержку потоковой передачи (`True`).
   - `needs_auth`: Флаг, указывающий на необходимость аутентификации (`False`).

3. **Функция `_create_completion`**:
   - Определяется функция `_create_completion`, которая принимает следующие аргументы:
     - `model` (str): Модель для использования.
     - `messages` (list): Список сообщений для отправки.
     - `stream` (bool): Флаг, указывающий на использование потоковой передачи.
     - `**kwargs`: Дополнительные аргументы.
   - Функция выполняет следующие действия:
     - Создает словарь `headers` с указанием типа контента `'application/json'`.
     - Создает словарь `data` с параметрами запроса, включая модель, температуру, штраф за присутствие и сообщения.
     - Отправляет POST-запрос к API (`url + '/api/openai/v1/chat/completions'`) с использованием библиотеки `requests`.
     - Перебирает поток ответов и извлекает контент из каждого ответа.
     - Возвращает контент в виде yield.

4. **Определение параметров**:
   - Формируется строка `params`, содержащая информацию о поддерживаемых типах данных для функции `_create_completion`.
   - Используется `get_type_hints` для получения аннотаций типов аргументов функции.
   - Строка содержит имя файла и поддерживаемые типы аргументов.

Пример использования
-------------------------

```python
import requests
import json

url = 'https://gpt4.gravityengine.cc/api/openai/v1/chat/completions'
model = 'gpt-3.5-turbo-16k'
messages = [
    {"role": "user", "content": "Hello, how are you?"}
]
headers = {
    'Content-Type': 'application/json',
}
data = {
    'model': model,
    'temperature': 0.7,
    'presence_penalty': 0,
    'messages': messages
}

try:
    response = requests.post(url, headers=headers, json=data, stream=True)
    response.raise_for_status()  # Проверка на HTTP ошибки

    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            try:
                json_data = json.loads(decoded_line)
                if 'choices' in json_data and len(json_data['choices']) > 0:
                    content = json_data['choices'][0]['message']['content']
                    print(content)
            except json.JSONDecodeError:
                print(f"JSONDecodeError: {decoded_line}")
except requests.exceptions.RequestException as e:
    print(f"RequestException: {e}")
except Exception as e:
    print(f"Exception: {e}")
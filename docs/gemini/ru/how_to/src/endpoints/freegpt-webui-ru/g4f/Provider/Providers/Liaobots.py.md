### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода предназначен для взаимодействия с API сервиса Liaobots для генерации текста на основе моделей GPT-3.5-turbo и GPT-4. Он отправляет запросы к API Liaobots и возвращает сгенерированный текст в режиме реального времени (stream).

Шаги выполнения
-------------------------
1. **Импорт необходимых библиотек**: Импортируются библиотеки `os`, `uuid`, `requests` и типы данных из `...typing`.
2. **Определение констант**: Определяются базовый URL (`url`), список поддерживаемых моделей (`model`), флаги поддержки потоковой передачи (`supports_stream`) и необходимости авторизации (`needs_auth`).
3. **Определение структуры данных моделей**: Создается словарь `models`, содержащий информацию о каждой поддерживаемой модели, такую как ID, имя, максимальная длина и лимит токенов.
4. **Функция `_create_completion`**:
   - Принимает параметры: `model` (имя модели), `messages` (список сообщений для генерации), `stream` (флаг потоковой передачи) и дополнительные аргументы `kwargs`.
   - Формирует заголовки запроса, включая `x-auth-code` для авторизации.
   - Создает JSON-тело запроса, включающее `conversationId`, информацию о модели, сообщения и промпт.
   - Отправляет POST-запрос к API Liaobots с использованием библиотеки `requests` и потоковой передачи.
   - Итерируется по содержимому ответа, декодирует каждый чанк и возвращает его как часть генератора.
5. **Определение `params`**: Формируется строка `params`, содержащая информацию о поддерживаемых параметрах функции `_create_completion` для логирования или документации.

Пример использования
-------------------------

```python
import os, uuid, requests
from typing import Dict, get_type_hints

url = 'https://liaobots.com'
model = ['gpt-3.5-turbo', 'gpt-4']
supports_stream = True
needs_auth = True

models = {
    'gpt-4': {
        "id":"gpt-4",
        "name":"GPT-4",
        "maxLength":24000,
        "tokenLimit":8000
    },
    'gpt-3.5-turbo': {
        "id":"gpt-3.5-turbo",
        "name":"GPT-3.5",
        "maxLength":12000,
        "tokenLimit":4000
    },
}

def _create_completion(model: str, messages: list, stream: bool, auth: str = None):
    """
    Генерирует текст на основе API Liaobots.

    Args:
        model (str): Имя модели для использования ('gpt-3.5-turbo' или 'gpt-4').
        messages (list): Список сообщений для отправки в API.
        stream (bool): Флаг потоковой передачи.
        auth (str, optional): Код авторизации. По умолчанию None.

    Yields:
        str: Части сгенерированного текста в режиме реального времени.

    Raises:
        requests.exceptions.RequestException: Если возникает ошибка при отправке запроса.

    Example:
        >>> messages = [{"role": "user", "content": "Hello, how are you?"}]
        >>> for token in _create_completion(model="gpt-3.5-turbo", messages=messages, stream=True, auth="your_auth_code"):
        ...     print(token, end="")
        ...
    """

    headers = {
        'authority': 'liaobots.com',
        'content-type': 'application/json',
        'origin': 'https://liaobots.com',
        'referer': 'https://liaobots.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'x-auth-code': auth
    }

    json_data = {
        'conversationId': str(uuid.uuid4()),
        'model': models[model],
        'messages': messages,
        'key': '',
        'prompt': "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown.",
    }

    response = requests.post('https://liaobots.com/api/chat', 
                             headers=headers, json=json_data, stream=True)

    for token in response.iter_content(chunk_size=2046):
        yield (token.decode('utf-8'))

# Пример использования
if __name__ == '__main__':
    messages = [{"role": "user", "content": "Напиши небольшое стихотворение о весне."}]
    # Замените 'your_auth_code' на ваш фактический код авторизации
    auth_code = "your_auth_code"  
    for token in _create_completion(model="gpt-3.5-turbo", messages=messages, stream=True, auth=auth_code):
        print(token, end="")
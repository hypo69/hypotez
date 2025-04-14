# Модуль для работы с Forefront
## Обзор

Модуль предоставляет класс `Forefront`, который позволяет взаимодействовать с сервисом Forefront для получения ответов от модели gpt-3.5-turbo. Он поддерживает потоковую передачу данных и не требует аутентификации.

## Подробней

Этот модуль используется для интеграции с Forefront, предоставляя возможность использовать их API для генерации текста. Он отправляет запросы к API Forefront и возвращает результаты в потоковом режиме.

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """Функция отправляет запрос в Forefront и получает ответ в потоковом режиме.

    Args:
        model (str): Название модели, используемой для генерации текста.
        messages (list): Список сообщений для передачи в модель.
        stream (bool): Флаг, указывающий, следует ли использовать потоковый режим.
        **kwargs: Дополнительные параметры.

    Returns:
        Generator[str, None, None]: Генератор, возвращающий токены ответа.

    Raises:
        Exception: Если возникает ошибка при отправке запроса или обработке ответа.

    Как работает функция:
        - Формирует JSON-данные для отправки в Forefront.
        - Отправляет POST-запрос к API Forefront.
        - Итерируется по строкам ответа, извлекая токены и возвращая их.

    Примеры:
        >>> model = 'gpt-3.5-turbo'
        >>> messages = [{'role': 'user', 'content': 'Hello, world!'}]
        >>> stream = True
        >>> generator = _create_completion(model, messages, stream)
        >>> for token in generator:
        ...     print(token)
        #Вывод: Hello, world!
    """
```

### Параметры `_create_completion`
   - `model` (str):  Название модели, используемой для генерации текста.
   - `messages` (list): Список сообщений для передачи в модель. Каждое сообщение должно быть словарем, содержащим ключи `role` и `content`.
   - `stream` (bool):  Флаг, определяющий, следует ли использовать потоковый режим передачи данных. Если `True`, функция будет возвращать генератор токенов.
   - `**kwargs`:  Дополнительные параметры, которые могут быть переданы в функцию.

### Как работает функция `_create_completion`
1. **Формирование JSON-данных**: Функция формирует JSON-данные, которые будут отправлены в API Forefront. Эти данные включают:
   - `text`: Последнее сообщение пользователя.
   - `action`: Тип действия (`noauth`, так как аутентификация не требуется).
   - `id`, `parentId`, `workspaceId`: Пустые строки.
   - `messagePersona`: Идентификатор персонажа сообщения.
   - `model`: Модель для использования (`gpt-4`).
   - `messages`: Предыдущие сообщения (если есть).
   - `internetMode`: Режим работы с интернетом (`auto`).
2. **Отправка POST-запроса**: Функция отправляет POST-запрос к API Forefront (`https://streaming.tenant-forefront-default.knative.chi.coreweave.com/free-chat`) с сформированными JSON-данными и параметром `stream=True`.
3. **Обработка потока ответов**: Функция итерируется по строкам ответа, полученного от API. Для каждой строки:
   - Проверяет, содержит ли строка маркер `b'delta'`.
   - Если маркер присутствует, строка декодируется и преобразуется в JSON.
   - Извлекается значение `delta` (токен ответа) и возвращается через генератор.

### Пример вызова `_create_completion`
```python
model = 'gpt-3.5-turbo'
messages = [{'role': 'user', 'content': 'Hello, world!'}]
stream = True
generator = _create_completion(model, messages, stream)
for token in generator:
    print(token)
```

### `params`

```python
params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '({})'.format(', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]]))
```

Глобальная переменная, содержащая строку с информацией о поддерживаемых параметрах функции `_create_completion`.

```python
import os
import json
import requests
from ...typing import sha256, Dict, get_type_hints

url = 'https://forefront.com'
model = ['gpt-3.5-turbo']
supports_stream = True
needs_auth = False

def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """
    Функция отправляет запрос в Forefront и получает ответ в потоковом режиме.

    Args:
        model (str): Название модели, используемой для генерации текста.
        messages (list): Список сообщений для передачи в модель.
        stream (bool): Флаг, указывающий, следует ли использовать потоковый режим.
        **kwargs: Дополнительные параметры.

    Returns:
        Generator[str, None, None]: Генератор, возвращающий токены ответа.

    Raises:
        Exception: Если возникает ошибка при отправке запроса или обработке ответа.

    """
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

params = 'g4f.Providers.{} supports: ({})'.format(os.path.basename(__file__)[:-3], ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]]))
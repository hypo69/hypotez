# Модуль Aichat.py
## Обзор
Модуль предоставляет класс для взаимодействия с провайдером Aichat, используя API chat-gpt.org. Он включает функцию `_create_completion` для создания запросов к API и получения ответов.
## Подробней
Этот модуль предназначен для отправки запросов к API `chat-gpt.org` и получения ответов на основе предоставленных сообщений. Он формирует JSON-запрос с необходимыми параметрами и заголовками, отправляет его на сервер и возвращает сгенерированное сообщение.

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """ Функция создает запрос к API `chat-gpt.org` и возвращает сгенерированный ответ.

    Args:
        model (str): Название используемой модели.
        messages (list): Список сообщений для отправки в запросе. Каждое сообщение содержит роль и контент.
        stream (bool): Параметр, определяющий, использовать ли потоковую передачу данных.
        **kwargs: Дополнительные параметры.

    Returns:
        Generator[str, None, None]: Генератор, возвращающий сгенерированное сообщение от API.

    Raises:
        requests.exceptions.RequestException: Если возникает ошибка при отправке запроса.
        json.JSONDecodeError: Если возникает ошибка при декодировании JSON-ответа.

    Как работает функция:
    1. Формирует базовый текст запроса из списка сообщений, объединяя роль и контент каждого сообщения.
    2. Создает словарь с необходимыми HTTP-заголовками для запроса.
    3. Формирует JSON-данные для отправки, включая сообщение, температуру, штрафы за присутствие и частоту, а также значение top_p.
    4. Отправляет POST-запрос к API `chat-gpt.org/api/text` с установленными заголовками и JSON-данными.
    5. Извлекает сгенерированное сообщение из JSON-ответа и возвращает его через генератор.

    ASCII flowchart:
    Сообщения -> Формирование базового текста
           ↓
    Формирование HTTP-заголовков
           ↓
    Формирование JSON-данных
           ↓
    Отправка POST-запроса -> Получение ответа
           ↓
    Извлечение сообщения из JSON -> Вывод сообщения

    Примеры:
        Пример 1: Создание простого запроса с одним сообщением.
        >>> messages = [{'role': 'user', 'content': 'Привет, как дела?'}]
        >>> for response in _create_completion(model='gpt-3.5-turbo', messages=messages, stream=False):
        ...     print(response)
        Ответ от API

        Пример 2: Создание запроса с несколькими сообщениями.
        >>> messages = [{'role': 'user', 'content': 'Привет'}, {'role': 'assistant', 'content': 'Здравствуйте'}, {'role': 'user', 'content': 'Как дела?'}]
        >>> for response in _create_completion(model='gpt-3.5-turbo', messages=messages, stream=False):
        ...     print(response)
        Ответ от API
    """
    base = ''
    for message in messages:
        base += '%s: %s\n' % (message['role'], message['content'])
    base += 'assistant:'

    headers = {
        'authority': 'chat-gpt.org',
        'accept': '*/*',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://chat-gpt.org',
        'pragma': 'no-cache',
        'referer': 'https://chat-gpt.org/chat',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }

    json_data = {
        'message': base,
        'temperature': 1,
        'presence_penalty': 0,
        'top_p': 1,
        'frequency_penalty': 0
    }

    response = requests.post('https://chat-gpt.org/api/text', headers=headers, json=json_data)
    yield response.json()['message']

```

### `params`

```python
params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
```

**Назначение**:
Строка `params` формируется для отображения поддерживаемых параметров функцией `_create_completion`.

**Как работает переменная**:

1.  Извлекает имя текущего файла модуля без расширения `.py`.
2.  Формирует строку, указывающую, что провайдер `g4f.Providers.<имя_файла>` поддерживает определенные параметры.
3.  Использует `get_type_hints` для получения аннотаций типов параметров функции `_create_completion`.
4.  Создает список строк вида `"имя_параметра: тип_параметра"` для каждого параметра функции.
5.  Объединяет полученные строки параметров в одну строку, разделенную запятыми.
6.  Вставляет строку с параметрами в основное сообщение `f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: (%s)'`.

**Пример**:

Предположим, имя файла `Aichat.py` и функция `_create_completion` имеет параметры `model: str, messages: list, stream: bool`.
Тогда строка `params` будет иметь вид:
```text
'g4f.Providers.Aichat supports: (model: str, messages: list, stream: bool)'
# Документация для модуля Lockchat.py

## Обзор

Модуль `Lockchat.py` предназначен для взаимодействия с API Lockchat для генерации текстовых ответов на основе предоставленных запросов. Он включает в себя функцию `_create_completion`, которая отправляет запросы к API Lockchat и возвращает результаты в потоковом режиме. Модуль поддерживает модели `gpt-4` и `gpt-3.5-turbo`.

## Подробней

Модуль предоставляет возможность взаимодействия с Lockchat API для генерации текста. Он использует библиотеку `requests` для отправки HTTP-запросов и `json` для обработки данных в формате JSON.

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, temperature: float = 0.7, **kwargs):
    """ Функция отправляет запрос в Lockchat API для генерации текста и возвращает результат.

    Args:
        model (str): Имя используемой модели (например, 'gpt-4', 'gpt-3.5-turbo').
        messages (list): Список сообщений для отправки в API.
        stream (bool): Флаг, указывающий, использовать ли потоковый режим.
        temperature (float, optional): Температура генерации текста. По умолчанию 0.7.
        **kwargs: Дополнительные аргументы.

    Yields:
        str: Часть сгенерированного текста в потоковом режиме.

    Raises:
        Exception: Если возникает ошибка при запросе к API или обработке ответа.

    Как работает функция:
    - Функция формирует payload с данными для отправки в Lockchat API, включая температуру, сообщения, модель и флаг потоковой передачи.
    - Устанавливает заголовки запроса, включая user-agent.
    - Отправляет POST-запрос к API Lockchat по адресу "http://super.lockchat.app/v1/chat/completions?auth=FnMNPlwZEnGFqvEc9470Vw==".
    - Итерируется по строкам ответа, полученного от API.
    - Если в ответе содержится сообщение об ошибке (например, модель не существует), функция выводит сообщение об ошибке и рекурсивно вызывает себя для повторной попытки.
    - Если в ответе содержится поле "content", функция извлекает текст из JSON-ответа и передает его в yield для потоковой передачи.

    Внутренние функции:
        В данной функции нет внутренних функций.

    """
    payload: Dict = {
        "temperature": 0.7,
        "messages": messages,
        "model": model,
        "stream": True,
    }
    headers: Dict = {
        "user-agent": "ChatX/39 CFNetwork/1408.0.4 Darwin/22.5.0",
    }
    response = requests.post("http://super.lockchat.app/v1/chat/completions?auth=FnMNPlwZEnGFqvEc9470Vw==",
                            json=payload, headers=headers, stream=True)
    for token in response.iter_lines():
        if b'The model: `gpt-4` does not exist' in token:
            print('error, retrying...')
            _create_completion(model=model, messages=messages, stream=stream, temperature=temperature, **kwargs)
        if b"content" in token:
            token = json.loads(token.decode('utf-8').split('data: ')[1])['choices'][0]['delta'].get('content')
            if token: yield (token)
```

**Примеры**:
```python
# Пример вызова функции _create_completion
model = 'gpt-3.5-turbo'
messages = [{'role': 'user', 'content': 'Hello, how are you?'}]
stream = True
temperature = 0.7

# Предполагается, что вызов функции _create_completion выполняется внутри генератора
# и возвращает части текста в потоковом режиме.
# Этот пример показывает, как можно итерироваться по результатам генератора.
# for token in _create_completion(model=model, messages=messages, stream=stream, temperature=temperature):
#     print(token)
```

## Переменные модуля

- `url` (str): URL Lockchat API (`http://super.lockchat.app`).
- `model` (list): Список поддерживаемых моделей ([`gpt-4`, `gpt-3.5-turbo`]).
- `supports_stream` (bool): Указывает, поддерживается ли потоковый режим (True).
- `needs_auth` (bool): Указывает, требуется ли аутентификация (False).
- `params` (str): Строка, содержащая информацию о поддержке параметров функцией `_create_completion`.
```python
params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
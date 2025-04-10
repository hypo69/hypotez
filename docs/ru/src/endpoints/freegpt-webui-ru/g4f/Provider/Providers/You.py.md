# Модуль для взаимодействия с You.com

## Обзор

Модуль предназначен для взаимодействия с моделью `gpt-3.5-turbo` через веб-сервис `you.com`. Он использует подпроцесс для выполнения Python-скрипта `you.py`, который, в свою очередь, взаимодействует с API `you.com`. Модуль поддерживает потоковую передачу данных и не требует аутентификации.

## Подробней

Этот модуль предоставляет функцию `_create_completion`, которая принимает сообщения, модель и другие параметры, необходимые для генерации текста. Он создает JSON-конфигурацию из входных сообщений и вызывает внешний Python-скрипт `you.py` в качестве подпроцесса. Результат работы этого скрипта передается обратно в виде потока текста. Этот подход позволяет взаимодействовать с API `you.com` через внешний скрипт, что может быть полезно для обхода ограничений или упрощения логики взаимодействия.

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """ Функция создает запрос к you.com и возвращает результат.

    Args:
        model (str): Имя модели для использования. В данном случае всегда 'gpt-3.5-turbo'.
        messages (list): Список сообщений для отправки в API.
        stream (bool): Флаг, указывающий, использовать ли потоковую передачу данных.
        **kwargs: Дополнительные аргументы (не используются).

    Returns:
        Generator[str, None, None]: Генератор строк, содержащий ответ от API.

    Как работает функция:
    1. Определяет путь к текущему файлу.
    2. Преобразует сообщения в JSON-формат.
    3. Формирует команду для вызова подпроцесса `you.py` с JSON-конфигурацией.
    4. Запускает подпроцесс и читает его вывод построчно.
    5. Передает каждую строку вывода как часть потока.

    ASCII flowchart:
    A: Получение параметров (model, messages, stream, kwargs)
    ↓
    B: Определение пути к файлу и формирование JSON-конфигурации
    ↓
    C: Формирование команды для запуска подпроцесса
    ↓
    D: Запуск подпроцесса
    ↓
    E: Чтение вывода подпроцесса построчно и передача в виде потока
    """

    path = os.path.dirname(os.path.realpath(__file__))
    config = json.dumps({
        'messages': messages}, separators=(',', ':'))
    
    cmd = ['python3', f'{path}/helpers/you.py', config]

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    for line in iter(p.stdout.readline, b''):
        yield line.decode('utf-8')

```

**Параметры**:

*   `model` (str): Имя модели, которая будет использоваться для генерации ответа. В данном случае всегда `'gpt-3.5-turbo'`.
*   `messages` (list): Список сообщений, которые будут отправлены в API. Каждое сообщение представляет собой словарь с ключами `role` и `content`.
*   `stream` (bool): Флаг, указывающий, будет ли использоваться потоковая передача данных. Если `True`, ответ будет возвращаться частями по мере генерации.
*   `**kwargs`: Дополнительные параметры, которые могут быть переданы в API. В данном случае не используются.

**Возвращает**:

*   `Generator[str, None, None]`: Генератор строк, который предоставляет ответ от API частями (если `stream=True`) или целиком (если `stream=False`).

**Примеры**:

```python
messages = [
    {"role": "user", "content": "Hello, how are you?"}
]
stream = True
generator = _create_completion(model='gpt-3.5-turbo', messages=messages, stream=stream)
for chunk in generator:
    print(chunk, end='')
```
```python
messages = [
    {"role": "user", "content": "Tell me a joke."}
]
stream = False
generator = _create_completion(model='gpt-3.5-turbo', messages=messages, stream=stream)
for chunk in generator:
    print(chunk, end='')
```
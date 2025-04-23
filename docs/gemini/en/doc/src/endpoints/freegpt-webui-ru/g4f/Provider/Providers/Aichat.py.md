# Документация модуля `Aichat.py`

## Обзор

Модуль предоставляет класс для взаимодействия с провайдером Aichat, используя API `chat-gpt.org`. Он включает функцию `_create_completion` для генерации текста на основе предоставленных сообщений.

## Подробнее

Модуль предназначен для работы с API `chat-gpt.org` и предоставляет функциональность для отправки запросов на генерацию текста. Он определяет URL, поддерживаемые модели, а также указывает на отсутствие необходимости в аутентификации.

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """
    Функция для создания запроса к API для генерации текста.

    Args:
        model (str): Идентификатор используемой модели.
        messages (list): Список сообщений для формирования запроса.
        stream (bool): Флаг, указывающий на необходимость потоковой передачи данных.
        **kwargs: Дополнительные параметры запроса.

    Returns:
        Generator[str, None, None]: Генератор, возвращающий сгенерированный текст.
    """
```

**Описание**: Функция `_create_completion` отвечает за отправку запроса к API `chat-gpt.org` и получение сгенерированного текста. Она формирует запрос на основе переданных сообщений и параметров, а затем отправляет его, используя библиотеку `requests`.

**Параметры**:
- `model` (str): Идентификатор используемой модели.
- `messages` (list): Список сообщений для формирования запроса. Каждое сообщение содержит роль и контент.
- `stream` (bool): Флаг, указывающий, нужно ли использовать потоковую передачу данных.
- `**kwargs`: Дополнительные параметры запроса.

**Возвращает**:
- `Generator[str, None, None]`: Генератор, который возвращает сгенерированный текст.

**Как работает функция**:
1. Формирует базовый текст запроса, объединяя сообщения с указанием их ролей.
2. Определяет заголовки HTTP-запроса, включая `authority`, `accept`, `content-type` и другие.
3. Формирует JSON-данные для отправки, включая сообщение, температуру, штрафы за присутствие и частоту, а также верхний предел `p`.
4. Отправляет POST-запрос к API `chat-gpt.org/api/text` с указанными заголовками и данными.
5. Получает ответ от API и извлекает сгенерированное сообщение из JSON-ответа.
6. Возвращает сгенерированный текст через генератор.

**Пример**:

```python
messages = [{"role": "user", "content": "Hello, how are you?"}]
model = "gpt-3.5-turbo"
stream = False
for response in _create_completion(model=model, messages=messages, stream=stream):
    print(response)
```

## Переменные

### `url`

```python
url = 'https://chat-gpt.org/chat'
```

**Описание**: URL для взаимодействия с `chat-gpt.org`.

### `model`

```python
model = ['gpt-3.5-turbo']
```

**Описание**: Список поддерживаемых моделей.

### `supports_stream`

```python
supports_stream = False
```

**Описание**: Флаг, указывающий на поддержку потоковой передачи данных.

### `needs_auth`

```python
needs_auth = False
```

**Описание**: Флаг, указывающий на необходимость аутентификации.

### `params`

```python
params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' +     \'(%s)\' % \', \'.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
```

**Описание**: Строка, содержащая информацию о поддерживаемых параметрах функции `_create_completion`.

## Примеры

Пример вызова функции `_create_completion`:

```python
messages = [{"role": "user", "content": "Напиши короткий стих о весне."}]
model = "gpt-3.5-turbo"
stream = False
for response in _create_completion(model=model, messages=messages, stream=stream):
    print(response)
```
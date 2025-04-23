# Документация для `Yqcloud.py`

## Обзор

Файл `Yqcloud.py` предоставляет реализацию провайдера `Yqcloud` для работы с моделью `gpt-3.5-turbo` через API `aichatos.cloud`. Он поддерживает потоковую передачу данных и не требует аутентификации.

## Детали

Этот файл содержит функцию `_create_completion`, которая отправляет запросы к API `aichatos.cloud` и возвращает результат в потоковом режиме.

## Классы

В данном файле классы отсутствуют.

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """ Функция создает запрос к API aichatos.cloud и возвращает результат в потоковом режиме.

    Args:
        model (str): Идентификатор модели, используемой для генерации.
        messages (list): Список сообщений для передачи в модель.
        stream (bool): Флаг, указывающий на необходимость потоковой передачи данных.
        **kwargs: Дополнительные параметры.

    Returns:
        Generator[str, None, None]: Генератор токенов ответа.

    Raises:
        requests.exceptions.RequestException: Если возникает ошибка при выполнении HTTP-запроса.

    Как работает функция:
    - Функция принимает модель, список сообщений и флаг потоковой передачи.
    - Формирует заголовок запроса, включая User-Agent и Referer.
    - Создает JSON-данные для отправки, включая сообщение пользователя, ID пользователя и другие параметры.
    - Отправляет POST-запрос к API `aichatos.cloud/api/generateStream` с потоковой передачей.
    - Итерируется по содержимому ответа, декодирует каждый токен и возвращает его.
    """
```

### Параметры функции `_create_completion`

- `model` (str): Идентификатор модели, используемой для генерации.
- `messages` (list): Список сообщений для передачи в модель.
- `stream` (bool): Флаг, указывающий на необходимость потоковой передачи данных.
- `**kwargs`: Дополнительные параметры.

### Примеры вызова функции `_create_completion`

```python
# Пример вызова функции _create_completion
model_name = "gpt-3.5-turbo"
messages_example = [{"role": "user", "content": "Привет, как дела?"}]
stream_flag = True

# В данном примере функция должна быть вызвана внутри асинхронной функции
# for token in _create_completion(model=model_name, messages=messages_example, stream=stream_flag):
#     print(token)
```

### `params`

```python
params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
```

Описание переменной `params`:
- `params` (str): Строка, формирующая информацию о поддержке типов данных для параметров функции `_create_completion`.

```python
# Пример использования переменной params
print(params)
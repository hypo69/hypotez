# Модуль `Liaobots.py`

## Обзор

Модуль предоставляет функциональность для взаимодействия с провайдером Liaobots, использующим модели GPT-3.5-turbo и GPT-4. Он включает в себя функцию для создания запросов к API Liaobots и получения ответов в потоковом режиме.

## Подробней

Модуль предназначен для интеграции с API Liaobots, который предоставляет доступ к моделям GPT-3.5-turbo и GPT-4. Он поддерживает потоковую передачу данных и требует аутентификации для использования.

## Переменные модуля

- `url` (str): URL адрес сервиса liaobots.com.
- `model` (list): Список поддерживаемых моделей (`gpt-3.5-turbo`, `gpt-4`).
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи данных (True).
- `needs_auth` (bool): Флаг, указывающий на необходимость аутентификации (True).
- `models` (dict): Словарь, содержащий информацию о поддерживаемых моделях, включая их идентификаторы, названия, максимальную длину и лимит токенов.

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, **kwargs) -> Generator[str, None, None]:
    """ Функция создает запрос к API Liaobots и возвращает ответ в потоковом режиме.

    Args:
        model (str): Идентификатор модели (`gpt-3.5-turbo` или `gpt-4`).
        messages (list): Список сообщений для отправки в API.
        stream (bool): Флаг, указывающий на необходимость потоковой передачи данных.
        **kwargs: Дополнительные параметры, такие как ключ аутентификации (`auth`).

    Returns:
        Generator[str, None, None]: Генератор токенов ответа от API.

    Raises:
        requests.exceptions.RequestException: В случае ошибки при отправке запроса к API.
        Exception: Если возникает ошибка при обработке ответа от API.

    Внутренние функции:
        - Отсутствуют.

    Как работает функция:
        1. Функция принимает идентификатор модели, список сообщений, флаг потоковой передачи и дополнительные параметры, включая ключ аутентификации.
        2. Формирует заголовки запроса, включая ключ аутентификации.
        3. Формирует JSON-данные для отправки в API, включая идентификатор разговора, модель, сообщения и промпт.
        4. Отправляет POST-запрос к API Liaobots с заголовками и данными.
        5. Итерируется по содержимому ответа в чанках размером 2046 байт.
        6. Декодирует каждый чанк в строку UTF-8 и передает его в генератор.

    Примеры:
        Пример 1:
            model = 'gpt-3.5-turbo'
            messages = [{'role': 'user', 'content': 'Hello, how are you?'}]
            auth_key = 'your_auth_key'
            response_generator = _create_completion(model, messages, stream=True, auth=auth_key)
            for token in response_generator:
                print(token)
    """
```

### `params`

```python
params: str = f\'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: \' + \\\n    \'(%s)\' % \', \'.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
```

**Назначение**: Строка, содержащая информацию о поддерживаемых параметрах функцией `_create_completion`.

**Как работает**:

1.  Получает имя файла текущего модуля (`os.path.basename(__file__)`) и удаляет расширение `.py` (`[:-3]`).
2.  Формирует строку `g4f.Providers.<имя_модуля> supports:`.
3.  Извлекает аннотации типов для параметров функции `_create_completion` (`get_type_hints(_create_completion)`).
4.  Создает список строк вида `"<имя_параметра>: <тип_параметра>"` для каждого параметра функции.
5.  Объединяет строки списка через запятую и заключает их в круглые скобки.
6.  Объединяет все части в одну строку и присваивает переменной `params`.

**Примеры**:

```python
print(params)
# g4f.Providers.Liaobots supports: (model: str, messages: list, stream: bool, kwargs: dict)
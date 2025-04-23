# Документация для `Lockchat.py`

## Обзор

Файл `Lockchat.py` предоставляет реализацию провайдера Lockchat для работы с моделями GPT через API `http://super.lockchat.app`. Он содержит функцию для создания запросов к API Lockchat и обработки потоковых ответов.

## Детали

В данном файле реализована поддержка моделей `gpt-4` и `gpt-3.5-turbo`. Он отправляет POST-запросы к API Lockchat и обрабатывает потоковые ответы, извлекая полезный контент.

## Функции

### `_create_completion`

```python
def _create_completion(model: str, messages: list, stream: bool, temperature: float = 0.7, **kwargs):
    """ Функция создает запрос к API Lockchat для генерации текста на основе предоставленных входных данных.

    Args:
        model (str): Имя используемой модели (`gpt-4` или `gpt-3.5-turbo`).
        messages (list): Список сообщений для отправки в API.
        stream (bool): Определяет, использовать ли потоковый режим.
        temperature (float, optional): Температура генерации текста. По умолчанию 0.7.
        **kwargs: Дополнительные аргументы.

    Returns:
        Generator[str, None, None]: Генератор токенов из потокового ответа API.

    Raises:
        Exception: Если возникает ошибка при запросе к API или обработке ответа.

    Как работает функция:
    - Функция формирует полезную нагрузку (payload) с параметрами, такими как температура, сообщения, модель и флаг потоковой передачи.
    - Устанавливает заголовки, включая User-Agent.
    - Отправляет POST-запрос к API Lockchat (`http://super.lockchat.app/v1/chat/completions?auth=FnMNPlwZEnGFqvEc9470Vw==`) с указанными полезными данными и заголовками.
    - Итерируется по строкам ответа, проверяя наличие ошибок (например, отсутствие модели `gpt-4`).
    - Извлекает контент из JSON-ответа и возвращает его как генератор токенов.

    Внутренние функции:
    - Отсутствуют.

    Пример:
        messages = [{"role": "user", "content": "Hello, world!"}]
        generator = _create_completion(model="gpt-3.5-turbo", messages=messages, stream=True)
        for token in generator:
            print(token)
    """
```

## Переменные

- `url` (str): URL API Lockchat (`http://super.lockchat.app`).
- `model` (list): Список поддерживаемых моделей (`gpt-4`, `gpt-3.5-turbo`).
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу (True).
- `needs_auth` (bool): Указывает, требуется ли аутентификация (False).
- `params` (str): Строка, содержащая информацию о поддерживаемых типах параметров функции `_create_completion`.
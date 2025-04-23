# Документация для модуля Forefront

## Обзор

Модуль `Forefront` представляет собой реализацию провайдера для взаимодействия с сервисом Forefront. Forefront — это платформа, предоставляющая доступ к различным моделям искусственного интеллекта, включая `gpt-4`. Модуль поддерживает потоковую передачу данных и предназначен для работы с моделью `gpt-3.5-turbo`.

## Подробней

Модуль использует библиотеку `requests` для выполнения HTTP-запросов к API Forefront. Он формирует JSON-данные на основе входных параметров и отправляет их в Forefront для получения ответа. Полученные данные обрабатываются потоково, что позволяет эффективно обрабатывать большие объемы информации.

## Классы

### `Forefront(AbstractProvider)`

**Описание**: Класс `Forefront` предоставляет интерфейс для взаимодействия с API Forefront.

**Наследует**: `AbstractProvider`

**Атрибуты**:

- `url` (str): URL сервиса Forefront (`https://forefront.com`).
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи данных (всегда `True`).
- `supports_gpt_35_turbo` (bool): Флаг, указывающий на поддержку модели `gpt-3.5-turbo` (всегда `True`).

**Методы**:

- `create_completion(model: str, messages: list[dict[str, str]], stream: bool, **kwargs: Any) -> CreateResult`: Создает запрос на завершение текста к API Forefront.

## Методы класса

### `create_completion`

```python
def create_completion(model: str, messages: list[dict[str, str]], stream: bool, **kwargs: Any) -> CreateResult:
    """
    Функция создает запрос на завершение текста к API Forefront.

    Args:
        model (str): Имя используемой модели.
        messages (list[dict[str, str]]): Список сообщений для контекста запроса. Каждое сообщение представляет собой словарь с ключами "role" и "content".
        stream (bool): Флаг, указывающий, следует ли использовать потоковую передачу данных.
        **kwargs (Any): Дополнительные аргументы.

    Returns:
        CreateResult: Генератор, возвращающий части завершенного текста.

    Raises:
        requests.exceptions.HTTPError: Если HTTP-запрос завершается с ошибкой.

    Как работает функция:
    - Формирует JSON-данные для запроса на основе входных параметров, включая текст последнего сообщения, историю сообщений, параметры модели и режим работы в интернете.
    - Выполняет POST-запрос к API Forefront с использованием потоковой передачи данных.
    - Обрабатывает ответ, извлекая из каждого токена (строки) JSON-структуры, содержащие дельту (изменение) текста.
    - Генерирует дельты текста, возвращая их вызывающей стороне.
    """
```

## Примеры

### Пример вызова `create_completion`

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
]

# model = "gpt-4"
# stream = True
# result = Forefront.create_completion(model, messages, stream)
# for token in result:
#     print(token)
```
```python
messages = [
    {"role": "system", "content": "You are a code generator."},
    {"role": "user", "content": "Write simple hello world in python"}
]

# model = "gpt-4"
# stream = True
# result = Forefront.create_completion(model, messages, stream)
# for token in result:
#     print(token)
# Module Name

## Обзор

Модуль предоставляет класс `Forefront` для взаимодействия с API Forefront. Forefront - это платформа, предоставляющая доступ к различным моделям, включая GPT-3.5 Turbo и GPT-4. Класс `Forefront` поддерживает потоковую передачу данных и предоставляет метод для создания завершений на основе предоставленных сообщений.

## Подробнее

Этот модуль позволяет интегрировать `hypotez` с сервисом Forefront для использования их моделей в задачах генерации текста. Модуль предназначен для упрощения процесса взаимодействия с API Forefront, предоставляя удобный интерфейс для отправки запросов и получения ответов.

## Классы

### `Forefront`

**Описание**: Класс для взаимодействия с API Forefront.

**Наследует**:
- `AbstractProvider`: Класс `Forefront` наследуется от `AbstractProvider`, который, вероятно, предоставляет общую структуру для работы с различными провайдерами моделей.

**Атрибуты**:
- `url` (str): URL сервиса Forefront ("https://forefront.com").
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных (True).
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель GPT-3.5 Turbo (True).

**Принцип работы**:
Класс `Forefront` использует библиотеку `requests` для отправки POST-запросов к API Forefront. Он формирует JSON-данные на основе входных сообщений и параметров модели, а затем отправляет запрос на указанный URL. Полученные данные обрабатываются потоково, и извлекаются полезные фрагменты текста.

### Методы:
- `create_completion`: Статический метод для создания завершений на основе предоставленных сообщений.

## Методы класса

### `create_completion`

```python
@staticmethod
def create_completion(
    model: str,
    messages: list[dict[str, str]],
    stream: bool, **kwargs: Any) -> CreateResult:
    """ Функция создает завершение на основе предоставленных сообщений, используя API Forefront.
    Args:
        model (str): Имя модели, которую нужно использовать.
        messages (list[dict[str, str]]): Список сообщений для отправки в API.
        stream (bool): Указывает, нужно ли использовать потоковую передачу данных.
        **kwargs (Any): Дополнительные аргументы.

    Returns:
        CreateResult: Результат создания завершения.

    Raises:
        requests.exceptions.HTTPError: Если HTTP-запрос завершается с ошибкой.
        json.JSONDecodeError: Если не удается декодировать JSON из ответа API.

    Как работает функция:
    - Формирует JSON-данные для отправки в API Forefront, включая текст последнего сообщения, историю сообщений (если есть), параметры модели и другие необходимые поля.
    - Отправляет POST-запрос на URL "https://streaming.tenant-forefront-default.knative.chi.coreweave.com/free-chat" с использованием библиотеки requests.
    - Если `stream` равен `True`, обрабатывает ответ потоково, извлекая фрагменты текста из JSON-ответов, содержащих поле "delta".
    - В случае ошибки при выполнении HTTP-запроса или декодировании JSON, вызывает исключение `requests.exceptions.HTTPError` или `json.JSONDecodeError` соответственно.
    - Возвращает результат в виде генератора токенов (если `stream` равен `True`) или полного текста ответа (если `stream` равен `False`).

    Примеры:
        >>> model = "gpt-4"
        >>> messages = [{"role": "user", "content": "Hello, how are you?"}]
        >>> stream = True
        >>> result = Forefront.create_completion(model, messages, stream)
        >>> for token in result:
        ...     print(token)
    """
```

## Параметры класса

- `model` (str): Имя модели, которую нужно использовать для создания завершения. Например, "gpt-4".
- `messages` (list[dict[str, str]]): Список сообщений, отправляемых в API. Каждое сообщение представляет собой словарь с ключами "role" (например, "user" или "assistant") и "content" (текст сообщения).
- `stream` (bool): Указывает, нужно ли использовать потоковую передачу данных. Если `True`, функция возвращает генератор токенов. Если `False`, функция возвращает полный текст ответа.
- `**kwargs` (Any): Дополнительные аргументы, которые можно передать в API Forefront.

**Примеры**:

```python
model = "gpt-4"
messages = [{"role": "user", "content": "Напиши короткий рассказ."}]
stream = True
result = Forefront.create_completion(model, messages, stream)
for token in result:
    print(token)
```
```python
model = "gpt-4"
messages = [
    {"role": "system", "content": "Ты - полезный ассистент."},
    {"role": "user", "content": "Как дела?"}
]
stream = True
result = Forefront.create_completion(model, messages, stream)
for token in result:
    print(token)
# Модуль EasyChat

## Обзор

Модуль `EasyChat` предоставляет класс `EasyChat`, который является провайдером для взаимодействия с сервисом EasyChat для получения ответов от AI моделей.
Он поддерживает потоковую передачу ответов и использование модели `gpt-3.5-turbo`.

## Подробней

Модуль определяет класс `EasyChat`, который наследуется от `AbstractProvider`. Он использует API сервиса EasyChat для отправки запросов и получения ответов от AI моделей. Модуль предназначен для интеграции с другими частями проекта, где требуется взаимодействие с AI моделями через провайдера EasyChat.

## Классы

### `EasyChat`

**Описание**: Класс для взаимодействия с сервисом EasyChat.

**Наследует**:
- `AbstractProvider`: Абстрактный класс, определяющий интерфейс для провайдеров.

**Атрибуты**:
- `url` (str): URL сервиса EasyChat.
- `supports_stream` (bool): Поддержка потоковой передачи ответов.
- `supports_gpt_35_turbo` (bool): Поддержка модели `gpt-3.5-turbo`.
- `working` (bool): Индикатор работоспособности провайдера.

**Методы**:
- `create_completion()`: Отправляет запрос к сервису EasyChat и возвращает ответ.

### `create_completion`

```python
@staticmethod
def create_completion(
    model: str,
    messages: list[dict[str, str]],
    stream: bool, **kwargs: Any) -> CreateResult:
    """
    Создает запрос к сервису EasyChat и возвращает ответ.

    Args:
        model (str): Название модели для использования.
        messages (list[dict[str, str]]): Список сообщений для отправки.
        stream (bool): Флаг потоковой передачи данных.
        **kwargs (Any): Дополнительные параметры запроса.

    Returns:
        CreateResult: Результат запроса.

    Raises:
        Exception: Если возникает ошибка при запросе к сервису.
    """
```

**Назначение**: Отправляет запрос к сервису EasyChat и возвращает ответ.

**Параметры**:
- `model` (str): Название модели для использования.
- `messages` (list[dict[str, str]]): Список сообщений для отправки.
- `stream` (bool): Флаг потоковой передачи данных.
- `**kwargs` (Any): Дополнительные параметры запроса.

**Возвращает**:
- `CreateResult`: Результат запроса.

**Вызывает исключения**:
- `Exception`: Если возникает ошибка при запросе к сервису.

**Как работает функция**:
- Определяет список активных серверов для отправки запроса.
- Выбирает случайный сервер из списка активных серверов.
- Формирует заголовки запроса, включая информацию о браузере и платформе.
- Формирует JSON данные для отправки, включая сообщения, модель, температуру и другие параметры.
- Создает сессию `requests.Session()` и получает куки с сервера.
- Отправляет POST запрос к сервису EasyChat с использованием указанных заголовков и данных.
- Обрабатывает ответ от сервиса. Если `stream` равен `False`, возвращает содержимое ответа. Если `stream` равен `True`, возвращает содержимое ответа по частям.
- В случае ошибки поднимает исключение `Exception` с описанием ошибки.

**Внутренние функции**:
- Отсутствуют.

**Примеры**:

```python
# Пример использования функции create_completion
model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "Hello, how are you?"}]
stream = False
kwargs = {"temperature": 0.7, "top_p": 0.9}

result = EasyChat.create_completion(model, messages, stream, **kwargs)
# result - генератор, возвращающий ответ от сервиса EasyChat
```
```python
# Пример использования функции create_completion c потоковой передачей данных
model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "Tell me a story."}]
stream = True
kwargs = {}

result = EasyChat.create_completion(model, messages, stream, **kwargs)
# result - генератор, возвращающий части ответа от сервиса EasyChat
for part in result:
    print(part)
```
```python
# Пример обработки ошибки при вызове функции create_completion
try:
    model = "gpt-3.5-turbo"
    messages = [{"role": "user", "content": "Hello, how are you?"}]
    stream = False
    kwargs = {}

    result = EasyChat.create_completion(model, messages, stream, **kwargs)
    # обработка result
except Exception as ex:
    print(f"Error: {ex}")
```

## Параметры класса

- `url` (str): URL сервиса EasyChat.
- `supports_stream` (bool): Поддержка потоковой передачи ответов.
- `supports_gpt_35_turbo` (bool): Поддержка модели `gpt-3.5-turbo`.
- `working` (bool): Индикатор работоспособности провайдера.
# Модуль Lockchat

## Обзор

Модуль `Lockchat` предоставляет класс `Lockchat`, который является провайдером для взаимодействия с API Lockchat. Он поддерживает потоковую передачу данных и модели `gpt-35-turbo` и `gpt-4`. Модуль позволяет отправлять запросы к API Lockchat и получать ответы в потоковом режиме.

## Подробней

Этот модуль является частью проекта `hypotez` и предназначен для обеспечения взаимодействия с сервисом Lockchat. Он использует библиотеку `requests` для отправки HTTP-запросов и `json` для обработки данных в формате JSON.

## Классы

### `Lockchat`

**Описание**:
Класс `Lockchat` является провайдером для взаимодействия с API Lockchat.

**Наследует**:
`AbstractProvider`

**Атрибуты**:
- `url` (str): URL-адрес API Lockchat. По умолчанию `"http://supertest.lockchat.app"`.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных. По умолчанию `True`.
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель `gpt-35-turbo`. По умолчанию `True`.
- `supports_gpt_4` (bool): Указывает, поддерживает ли провайдер модель `gpt-4`. По умолчанию `True`.

**Методы**:
- `create_completion`: Создает запрос на завершение текста к API Lockchat.

## Методы класса

### `create_completion`

```python
@staticmethod
def create_completion(
    model: str,
    messages: list[dict[str, str]],
    stream: bool, **kwargs: Any) -> CreateResult:
    """
    Создает запрос на завершение текста к API Lockchat.

    Args:
        model (str): Имя модели для использования.
        messages (list[dict[str, str]]): Список сообщений для отправки.
        stream (bool): Указывает, использовать ли потоковую передачу данных.
        **kwargs (Any): Дополнительные аргументы.

    Returns:
        CreateResult: Генератор токенов ответа.

    Raises:
        requests.exceptions.HTTPError: Если HTTP-запрос завершается с ошибкой.

    Как работает функция:
    - Извлекает значение температуры из `kwargs` или устанавливает значение по умолчанию 0.7.
    - Формирует полезную нагрузку (payload) для запроса, включая температуру, сообщения, модель и флаг потоковой передачи.
    - Устанавливает заголовки запроса, включая User-Agent.
    - Отправляет POST-запрос к API Lockchat с использованием `requests.post` и потоковой передачи.
    - Обрабатывает ответ в потоковом режиме, итерируя по строкам ответа.
    - Проверяет наличие ошибок, таких как "The model: `gpt-4` does not exist", и выполняет повторную попытку запроса в случае ошибки.
    - Извлекает содержимое токенов из JSON-ответа и возвращает их с использованием `yield`.

    Внутренние функции:
        Нет.
    """
    ...
```

**Параметры**:
- `model` (str): Имя модели для использования.
- `messages` (list[dict[str, str]]): Список сообщений для отправки.
- `stream` (bool): Указывает, использовать ли потоковую передачу данных.
- `**kwargs` (Any): Дополнительные аргументы, такие как `temperature`.

**Примеры**:

```python
# Пример вызова create_completion
model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "Hello, how are you?"}]
stream = True
temperature = 0.8

# Предполагается, что Lockchat.create_completion - это статический метод
response = Lockchat.create_completion(model=model, messages=messages, stream=stream, temperature=temperature)

# Итерирование по токенам ответа
for token in response:
    print(token, end="")
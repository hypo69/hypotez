# Документация для модуля `AutonomousAI.py`

## Обзор

Модуль предоставляет асинхронную реализацию взаимодействия с API AutonomousAI для генерации текста.
Он поддерживает потоковую передачу данных, системные сообщения и историю сообщений.
Модуль включает в себя поддержку различных моделей, таких как "llama", "qwen_coder", "hermes", "vision" и "summary".

## Более подробная информация

Этот модуль является частью проекта `hypotez` и предназначен для интеграции с другими компонентами,
требующими доступа к API AutonomousAI. Модуль использует библиотеку `aiohttp` для выполнения асинхронных HTTP-запросов
и `base64` для кодирования сообщений. Важной особенностью является поддержка потоковой передачи данных, что позволяет
получать ответы от API частями, не дожидаясь полной генерации текста.

## Классы

### `AutonomousAI`

**Описание**: Класс для взаимодействия с API AutonomousAI.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.

**Атрибуты**:
- `url` (str): Базовый URL для AutonomousAI.
- `api_endpoints` (dict): Словарь с конечными точками API для различных моделей.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
- `default_model` (str): Модель по умолчанию.
- `models` (list): Список поддерживаемых моделей.
- `model_aliases` (dict): Словарь псевдонимов моделей.

**Принцип работы**:
Класс использует `aiohttp.ClientSession` для выполнения асинхронных POST-запросов к API AutonomousAI.
Сообщения кодируются в base64 для передачи в запросе. Поддерживается потоковая передача данных, при которой ответы от API
обрабатываются по частям.

## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    stream: bool = False,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для получения ответов от API AutonomousAI.

    Args:
        cls (AutonomousAI): Класс AutonomousAI.
        model (str): Название модели для использования.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        stream (bool, optional): Включить потоковую передачу данных. По умолчанию `False`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий части ответа.

    Raises:
        Exception: В случае ошибки при выполнении запроса.

    Как работает функция:
    1. Функция определяет конечную точку API на основе выбранной модели.
    2. Формирует заголовки запроса, включая `content-type`, `user-agent` и другие необходимые параметры.
    3. Кодирует сообщения в формат JSON и затем в base64.
    4. Создает тело запроса с закодированными сообщениями, идентификатором потока, флагом потоковой передачи и выбранной моделью.
    5. Выполняет асинхронный POST-запрос к API.
    6. Обрабатывает ответ от API, извлекая и выдавая части контента (delta) из JSON-ответов.
    7. Обрабатывает ошибки JSON при декодировании ответа.
    8. При получении `finish_reason` генерирует соответствующее значение `FinishReason`.
    """
```

**Параметры**:
- `model` (str): Название модели для использования.
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `stream` (bool, optional): Включить потоковую передачу данных. По умолчанию `False`.
- `**kwargs`: Дополнительные параметры.

**Примеры**:

```python
# Пример использования create_async_generator
messages = [{"role": "user", "content": "Hello, how are you?"}]
async for chunk in AutonomousAI.create_async_generator(model="llama", messages=messages, stream=True):
    print(chunk)
```
```python
# Пример использования create_async_generator без потоковой передачи
messages = [{"role": "user", "content": "Tell me a joke."}]
async for chunk in AutonomousAI.create_async_generator(model="qwen_coder", messages=messages, stream=False):
    print(chunk)
```
```python
# Пример использования create_async_generator с прокси-сервером
messages = [{"role": "user", "content": "Write a short story."}]
async for chunk in AutonomousAI.create_async_generator(model="hermes", messages=messages, proxy="http://proxy.example.com", stream=True):
    print(chunk)
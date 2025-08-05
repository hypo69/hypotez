# Документация для модуля `Aivvm.py`

## Обзор

Модуль `Aivvm.py` предоставляет класс `Aivvm`, который является устаревшим провайдером для взаимодействия с API Aivvm (chat.aivvm.com). Он позволяет отправлять запросы к различным моделям, включая GPT-3.5 и GPT-4, и получать ответы в потоковом режиме.

## Подробнее

Модуль определяет словарь `models`, содержащий информацию о поддерживаемых моделях, таких как `gpt-3.5-turbo` и `gpt-4`. Класс `Aivvm` наследуется от `AbstractProvider` и реализует метод `create_completion` для отправки запросов к API Aivvm.

## Классы

### `Aivvm(AbstractProvider)`

**Описание**: Класс `Aivvm` предоставляет функциональность для взаимодействия с API Aivvm и получения ответов от различных моделей.
**Наследует**: `AbstractProvider`

**Атрибуты**:
- `url` (str): URL-адрес API Aivvm (`https://chat.aivvm.com`).
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковый режим (`True`).
- `working` (bool): Указывает, работает ли провайдер в данный момент (`False`).
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модели GPT-3.5 turbo (`True`).
- `supports_gpt_4` (bool): Указывает, поддерживает ли провайдер модели GPT-4 (`True`).

**Методы**:
- `create_completion()`: Отправляет запрос к API Aivvm и возвращает ответ в потоковом режиме.

## Методы класса

### `create_completion(model: str, messages: Messages, stream: bool, **kwargs) -> CreateResult`

```python
@classmethod
def create_completion(cls,
    model: str,
    messages: Messages,
    stream: bool,
    **kwargs
) -> CreateResult:
    """ Функция отправляет запрос к API Aivvm и возвращает ответ в потоковом режиме.

    Args:
        model (str): Идентификатор модели для использования (например, "gpt-3.5-turbo").
        messages (Messages): Список сообщений для отправки в запросе.
        stream (bool): Указывает, следует ли возвращать ответ в потоковом режиме.
        **kwargs: Дополнительные аргументы, такие как `system_message` и `temperature`.

    Returns:
        CreateResult: Генератор, возвращающий чанки ответа в кодировке UTF-8.

    Raises:
        ValueError: Если указанная модель не поддерживается.
        requests.exceptions.HTTPError: Если HTTP-запрос завершается с ошибкой.

    
        - Проверяет, указана ли модель. Если нет, использует "gpt-3.5-turbo" по умолчанию.
        - Проверяет, поддерживается ли указанная модель. Если нет, вызывает исключение ValueError.
        - Формирует JSON-данные для отправки в запросе, включая модель, сообщения, ключ API, системное сообщение и температуру.
        - Устанавливает заголовки запроса, включая тип контента, User-Agent и Referrer.
        - Отправляет POST-запрос к API Aivvm с указанными заголовками и данными.
        - Обрабатывает ответ от API Aivvm в потоковом режиме, декодируя каждый чанк в кодировке UTF-8 и возвращая его.
        - Если возникает ошибка при декодировании, пытается декодировать чанк с использованием "unicode-escape".
    """
```

**Параметры**:
- `model` (str): Идентификатор модели для использования (например, "gpt-3.5-turbo").
- `messages` (Messages): Список сообщений для отправки в запросе.
- `stream` (bool): Указывает, следует ли возвращать ответ в потоковом режиме.
- `**kwargs`: Дополнительные аргументы, такие как `system_message` и `temperature`.

**Возвращает**:
- `CreateResult`: Генератор, возвращающий чанки ответа в кодировке UTF-8.

**Вызывает исключения**:
- `ValueError`: Если указанная модель не поддерживается.
- `requests.exceptions.HTTPError`: Если HTTP-запрос завершается с ошибкой.

**Примеры**:

```python
# Пример использования create_completion
messages = [{"role": "user", "content": "Hello, how are you?"}]
stream = True
kwargs = {"temperature": 0.8}

# Предположим, что Aivvm.create_completion вызывается где-то в коде
# for chunk in Aivvm.create_completion(model="gpt-3.5-turbo", messages=messages, stream=stream, **kwargs):
#     print(chunk)
# Модуль Jmuz

## Обзор

Модуль `Jmuz` предоставляет класс для взаимодействия с моделью GPT-4o через API jmuz.me. Он наследует базовый класс `OpenaiTemplate` и адаптирует запросы и ответы для соответствия требованиям API `jmuz.me`. Модуль поддерживает стриминг ответов и предоставляет методы для получения списка доступных моделей.

## Подробней

Модуль `Jmuz` предназначен для упрощения работы с API `jmuz.me` в рамках проекта `hypotez`. Он содержит настройки для подключения к API, определения моделей и форматирования запросов. Класс `Jmuz` использует `OpenaiTemplate` для обработки запросов и ответов, а также включает дополнительную логику для фильтрации нежелательных сообщений, таких как приглашения в Discord.

## Классы

### `Jmuz(OpenaiTemplate)`

**Описание**: Класс `Jmuz` предназначен для взаимодействия с API `jmuz.me`. Он наследует функциональность от `OpenaiTemplate` и предоставляет методы для отправки запросов и получения ответов от модели GPT-4o.

**Наследует**:

- `OpenaiTemplate`: Базовый класс, предоставляющий общую логику для взаимодействия с API OpenAI-подобных моделей.

**Атрибуты**:

- `url` (str): URL Discord-сервера.
- `api_base` (str): Базовый URL API `jmuz.me`.
- `api_key` (str): Ключ API для доступа к `jmuz.me`.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений (в данном случае `False`).
- `default_model` (str): Модель, используемая по умолчанию (`gpt-4o`).
- `model_aliases` (dict): Словарь псевдонимов моделей.

**Методы**:

- `get_models()`: Возвращает список доступных моделей.
- `create_async_generator()`: Создает асинхронный генератор для получения ответов от API.

### Методы класса

### `get_models`

```python
@classmethod
def get_models(cls, **kwargs) -> list[str]:
    """Получает список доступных моделей.

    Args:
        **kwargs: Дополнительные аргументы (например, `api_key`, `api_base`).

    Returns:
        list[str]: Список доступных моделей.
    """
    ...
```

**Назначение**: Получение списка доступных моделей с использованием API.

**Параметры**:

- `cls` (type[Jmuz]): Ссылка на класс `Jmuz`.
- `**kwargs`: Дополнительные аргументы, передаваемые в `super().get_models()`.

**Возвращает**:

- `list[str]`: Список доступных моделей.

**Как работает функция**:

- Проверяет, если список моделей (`cls.models`) пуст. Если да, вызывает метод `get_models` родительского класса (`super().get_models()`) для получения списка моделей из API, используя `cls.api_key` и `cls.api_base` для аутентификации и указания базового URL.
- Возвращает список моделей (`cls.models`).

**Примеры**:

```python
models = Jmuz.get_models()
print(models)
# Вывод: ['gpt-4o', 'qwq-32b-preview', 'gemini-flash', ...]
```

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    stream: bool = True,
    api_key: str = None,  # Remove api_key from kwargs
    **kwargs
) -> AsyncResult:
    """Создает асинхронный генератор для получения ответов от API.

    Args:
        model (str): Название модели.
        messages (Messages): Список сообщений для отправки в API.
        stream (bool, optional): Флаг, указывающий на использование стриминга. По умолчанию `True`.
        api_key (str, optional): Ключ API (удален из kwargs). По умолчанию `None`.
        **kwargs: Дополнительные аргументы для передачи в API.

    Yields:
        AsyncResult: Части ответа от API.
    """
    ...
```

**Назначение**: Создание асинхронного генератора для получения чанков ответа от API `jmuz.me`.

**Параметры**:

- `cls` (type[Jmuz]): Ссылка на класс `Jmuz`.
- `model` (str): Название модели для использования.
- `messages` (Messages): Список сообщений для отправки в API.
- `stream` (bool, optional): Флаг, указывающий, следует ли использовать стриминг. По умолчанию `True`.
- `api_key` (str, optional): Ключ API (удален из `kwargs`). По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы для передачи в API.

**Возвращает**:

- `AsyncResult`: Асинхронный генератор, выдающий части ответа от API.

**Как работает функция**:

1.  **Подготовка**:
    *   Получает название модели с помощью `cls.get_model(model)`.
    *   Формирует заголовки (`headers`) для HTTP-запроса, включая `Authorization` с ключом API, `Content-Type` и `user-agent`.
    *   Инициализирует переменные `started` (для отслеживания начала полезного ответа) и `buffer` (для накопления чанков).

2.  **Асинхронный запрос**:
    *   Использует `super().create_async_generator()` для отправки запроса к API и получения асинхронного генератора чанков. Передает параметры, такие как `model`, `messages`, `api_base`, `api_key`, `stream`, `headers` и другие `kwargs`.

3.  **Обработка чанков**:
    *   Итерируется по чанкам, полученным от `super().create_async_generator()`.
    *   Если чанк является строкой (`isinstance(chunk, str)`):
        *   Добавляет чанк в `buffer`.
        *   Фильтрует нежелательные сообщения:
            *   Проверяет, начинается ли `buffer` с "Join for free" или содержит ли "https://discord.gg/". Если да, очищает `buffer` и переходит к следующему чанку.
            *   Проверяет, начинается ли `buffer` с "o1-preview". Если да, и если в `buffer` есть символ новой строки, очищает `buffer` и переходит к следующему чанку.
        *   Удаляет начальные пробелы из `buffer`, если `started` равно `False`.
        *   Если `buffer` не пустой, устанавливает `started` в `True`, выдает (`yield`) содержимое `buffer` и очищает `buffer`.
    *   Если чанк не является строкой, выдает его напрямую (`yield chunk`).

**Примеры**:

```python
messages = [{"role": "user", "content": "Hello, how are you?"}]
async for chunk in Jmuz.create_async_generator(model="gpt-4o", messages=messages):
    print(chunk, end="")
# Вывод: Hello! I am doing well. How can I assist you today?
```

## Параметры класса

- `url` (str): URL Discord-сервера.
- `api_base` (str): Базовый URL API `jmuz.me`.
- `api_key` (str): Ключ API для доступа к `jmuz.me`.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений (в данном случае `False`).
- `default_model` (str): Модель, используемая по умолчанию (`gpt-4o`).
- `model_aliases` (dict): Словарь псевдонимов моделей.
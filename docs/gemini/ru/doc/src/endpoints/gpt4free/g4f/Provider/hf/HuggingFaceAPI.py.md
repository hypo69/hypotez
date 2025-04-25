# Модуль HuggingFaceAPI

## Обзор

Модуль `HuggingFaceAPI` предоставляет функционал для взаимодействия с API Hugging Face для генерации текста с использованием различных моделей. 
Он наследует от класса `OpenaiTemplate` и предоставляет возможность выбора модели, получения списка доступных моделей, 
обработки входящих сообщений и генерации ответа. 

## Подробнее

Модуль использует API Hugging Face для работы с различными моделями. 
Он предоставляет следующие возможности:

- Получение списка доступных моделей (метод `get_models`).
- Выбор модели для генерации текста (метод `get_model`).
- Обработка входных сообщений и генерация ответа с использованием выбранной модели (метод `create_async_generator`).

## Классы

### `class HuggingFaceAPI`

**Описание**: Класс `HuggingFaceAPI` реализует функционал для взаимодействия с API Hugging Face. 
Он наследует от класса `OpenaiTemplate`, обеспечивая базовый набор функций для работы с API.

**Наследует**: `OpenaiTemplate`

**Атрибуты**:

- `label` (str): Тег для идентификации провайдера.
- `parent` (str): Родительский провайдер.
- `url` (str): Базовый URL API.
- `api_base` (str): URL для вызова API.
- `working` (bool): Флаг, указывающий на доступность API.
- `needs_auth` (bool): Флаг, указывающий на необходимость авторизации.
- `default_model` (str): Имя модели по умолчанию.
- `default_vision_model` (str): Имя модели по умолчанию для работы с изображениями.
- `vision_models` (list[str]): Список моделей, поддерживающих работу с изображениями.
- `model_aliases` (dict[str, str]): Словарь с псевдонимами моделей.
- `fallback_models` (list[str]): Список моделей, используемых в случае, если основная модель недоступна.
- `provider_mapping` (dict[str, dict]): Словарь, содержащий соответствие между моделями и их провайдерами.

**Методы**:

- `get_model(model: str, **kwargs) -> str`: Возвращает имя модели, соответствующей переданному аргументу.
- `get_models(**kwargs) -> list[str]`: Возвращает список доступных моделей.
- `get_mapping(model: str, api_key: str = None) -> dict`: Возвращает соответствие между моделью и ее провайдером.
- `create_async_generator(model: str, messages: Messages, api_base: str = None, api_key: str = None, max_tokens: int = 2048, max_inputs_lenght: int = 10000, media: MediaListType = None, **kwargs) -> Generator`: Создает асинхронный генератор для обработки входных сообщений и генерации ответа.

## Функции

### `calculate_lenght(messages: Messages) -> int`

**Назначение**: Функция подсчитывает общее количество символов во входных сообщениях.

**Параметры**:

- `messages` (Messages): Список входных сообщений.

**Возвращает**:

- `int`: Общее количество символов во входных сообщениях.

**Примеры**:

```python
>>> messages = [{"role": "user", "content": "Привет!"}, {"role": "assistant", "content": "Привет!"}]
>>> calculate_lenght(messages)
25
```

### `get_model(cls, model: str, **kwargs) -> str`

**Назначение**: Функция возвращает имя модели, соответствующей переданному аргументу.

**Параметры**:

- `model` (str): Имя модели.

**Возвращает**:

- `str`: Имя модели.

**Примеры**:

```python
>>> HuggingFaceAPI.get_model("gpt-3.5-turbo")
'gpt-3.5-turbo'
```

### `get_models(cls, **kwargs) -> list[str]`

**Назначение**: Функция возвращает список доступных моделей.

**Возвращает**:

- `list[str]`: Список доступных моделей.

**Примеры**:

```python
>>> HuggingFaceAPI.get_models()
['gpt-3.5-turbo', 'text-davinci-003', 'text-curie-001', 'text-babbage-001', 'text-ada-001', 'code-davinci-002', 'code-cushman-001']
```

### `get_mapping(cls, model: str, api_key: str = None) -> dict`

**Назначение**: Функция возвращает соответствие между моделью и ее провайдером.

**Параметры**:

- `model` (str): Имя модели.
- `api_key` (str, optional): Ключ API. По умолчанию `None`.

**Возвращает**:

- `dict`: Словарь, содержащий соответствие между моделью и ее провайдером.

**Примеры**:

```python
>>> HuggingFaceAPI.get_mapping("gpt-3.5-turbo")
{'task': 'conversational', 'providerId': 'gpt-3.5-turbo'}
```

### `create_async_generator(cls, model: str, messages: Messages, api_base: str = None, api_key: str = None, max_tokens: int = 2048, max_inputs_lenght: int = 10000, media: MediaListType = None, **kwargs) -> Generator`

**Назначение**: Функция создает асинхронный генератор для обработки входных сообщений и генерации ответа.

**Параметры**:

- `model` (str): Имя модели.
- `messages` (Messages): Список входных сообщений.
- `api_base` (str, optional): Базовый URL API. По умолчанию `None`.
- `api_key` (str, optional): Ключ API. По умолчанию `None`.
- `max_tokens` (int, optional): Максимальное количество токенов в ответе. По умолчанию `2048`.
- `max_inputs_lenght` (int, optional): Максимальная длина входных сообщений. По умолчанию `10000`.
- `media` (MediaListType, optional): Список медиа-файлов. По умолчанию `None`.
- `kwargs` (dict): Дополнительные параметры.

**Возвращает**:

- `Generator`: Асинхронный генератор, который выдает части ответа.

**Примеры**:

```python
>>> messages = [{"role": "user", "content": "Привет!"}]
>>> async for chunk in HuggingFaceAPI.create_async_generator("gpt-3.5-turbo", messages):
...     print(chunk)
...
{'role': 'assistant', 'content': 'Привет!'}
```

## Параметры класса

- `label` (str): Тег для идентификации провайдера.
- `parent` (str): Родительский провайдер.
- `url` (str): Базовый URL API.
- `api_base` (str): URL для вызова API.
- `working` (bool): Флаг, указывающий на доступность API.
- `needs_auth` (bool): Флаг, указывающий на необходимость авторизации.
- `default_model` (str): Имя модели по умолчанию.
- `default_vision_model` (str): Имя модели по умолчанию для работы с изображениями.
- `vision_models` (list[str]): Список моделей, поддерживающих работу с изображениями.
- `model_aliases` (dict[str, str]): Словарь с псевдонимами моделей.
- `fallback_models` (list[str]): Список моделей, используемых в случае, если основная модель недоступна.
- `provider_mapping` (dict[str, dict]): Словарь, содержащий соответствие между моделями и их провайдерами.

## Примеры

```python
# Получение списка доступных моделей
>>> models = HuggingFaceAPI.get_models()
>>> print(models)
['gpt-3.5-turbo', 'text-davinci-003', 'text-curie-001', 'text-babbage-001', 'text-ada-001', 'code-davinci-002', 'code-cushman-001']

# Генерация ответа с использованием модели gpt-3.5-turbo
>>> messages = [{"role": "user", "content": "Привет!"}]
>>> async for chunk in HuggingFaceAPI.create_async_generator("gpt-3.5-turbo", messages):
...     print(chunk)
...
{'role': 'assistant', 'content': 'Привет!'}
```
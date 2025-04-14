# Модуль HuggingFaceAPI

## Обзор

Модуль `HuggingFaceAPI` предназначен для взаимодействия с моделями Hugging Face для генерации текста. Он наследует функциональность из класса `OpenaiTemplate` и предоставляет методы для получения списка моделей, создания асинхронного генератора и выполнения других операций, связанных с API Hugging Face.

## Подробней

Этот модуль предоставляет интерфейс для доступа к API Hugging Face, позволяя пользователям использовать различные модели для генерации текста и обработки изображений. Он включает в себя поддержку различных задач, таких как разговорная генерация текста, и обеспечивает гибкость в настройке параметров запросов.

## Классы

### `HuggingFaceAPI`

**Описание**: Класс `HuggingFaceAPI` предоставляет методы для взаимодействия с API Hugging Face для генерации текста.

**Наследует**:
- `OpenaiTemplate`: Класс наследует функциональность из `OpenaiTemplate`, который предоставляет базовые методы для работы с API OpenAI.

**Атрибуты**:
- `label` (str): Метка провайдера, `"HuggingFace (Text Generation)"`.
- `parent` (str): Родительский провайдер, `"HuggingFace"`.
- `url` (str): URL API, `"https://api-inference.huggingface.com"`.
- `api_base` (str): Базовый URL API, `"https://api-inference.huggingface.co/v1"`.
- `working` (bool): Флаг, указывающий, работает ли провайдер, `True`.
- `needs_auth` (bool): Флаг, указывающий, требуется ли аутентификация, `True`.
- `default_model` (str): Модель по умолчанию, `default_llama_model`.
- `default_vision_model` (str): Модель для обработки изображений по умолчанию, `default_vision_model`.
- `vision_models` (list[str]): Список моделей для обработки изображений.
- `model_aliases` (dict[str, str]): Словарь псевдонимов моделей.
- `fallback_models` (list[str]): Список запасных моделей.
- `provider_mapping` (dict[str, dict]): Словарь соответствий моделей и провайдеров.

**Методы**:
- `get_model(model: str, **kwargs) -> str`: Возвращает модель для использования.
- `get_models(cls, **kwargs) -> list[str]`: Возвращает список доступных моделей.
- `get_mapping(cls, model: str, api_key: str = None)`: Возвращает соответствие моделей и провайдеров.
- `create_async_generator(cls, model: str, messages: Messages, api_base: str = None, api_key: str = None, max_tokens: int = 2048, max_inputs_lenght: int = 10000, media: MediaListType = None, **kwargs)`: Создает асинхронный генератор для получения ответов от API.

## Функции

### `get_model`

```python
    @classmethod
    def get_model(cls, model: str, **kwargs) -> str:
        """Возвращает модель для использования.

        Args:
            model (str): Название модели.
            **kwargs: Дополнительные аргументы.

        Returns:
            str: Название модели.

        Raises:
            ModelNotSupportedError: Если модель не поддерживается.
        """
        ...
```

**Назначение**: Возвращает название модели для использования. Если модель не поддерживается, возвращает исходное название модели.

**Параметры**:
- `model` (str): Название модели.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `str`: Название модели.

**Вызывает исключения**:
- `ModelNotSupportedError`: Если модель не поддерживается.

**Как работает функция**:

1. Пытается получить модель с использованием метода `super().get_model(model, **kwargs)`.
2. Если возникает исключение `ModelNotSupportedError`, возвращает исходное название модели.

**Примеры**:
```python
# Пример 1: Получение поддерживаемой модели
model = HuggingFaceAPI.get_model("llama-2-7b")

# Пример 2: Получение неподдерживаемой модели
model = HuggingFaceAPI.get_model("unsupported-model")
```

### `get_models`

```python
    @classmethod
    def get_models(cls, **kwargs) -> list[str]:
        """Возвращает список доступных моделей.

        Args:
            **kwargs: Дополнительные аргументы.

        Returns:
            list[str]: Список доступных моделей.
        """
        ...
```

**Назначение**: Возвращает список доступных моделей из API Hugging Face. Если список моделей еще не был получен, он запрашивается из API и кэшируется.

**Параметры**:
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `list[str]`: Список доступных моделей.

**Как работает функция**:

1. Проверяет, был ли уже получен список моделей (хранится в `cls.models`).
2. Если список моделей отсутствует, функция выполняет HTTP-запрос к API Hugging Face для получения списка моделей.
3. Если запрос успешен, извлекаются идентификаторы моделей, у которых статус `"live"` и задача `"conversational"`.
4. Полученный список моделей объединяется с ключами из `cls.provider_mapping`.
5. Если запрос не успешен, используется запасной список моделей `cls.fallback_models`.
6. Возвращает список доступных моделей.

**Примеры**:
```python
# Пример 1: Получение списка моделей
models = HuggingFaceAPI.get_models()
print(models)
```

### `get_mapping`

```python
    @classmethod
    async def get_mapping(cls, model: str, api_key: str = None):
        """Получает соответствие моделей и провайдеров.

        Args:
            model (str): Название модели.
            api_key (str, optional): API-ключ. По умолчанию `None`.

        Returns:
            dict: Соответствие моделей и провайдеров.
        """
        ...
```

**Назначение**: Получает соответствие между моделями и провайдерами из API Hugging Face. Если соответствие уже известно, возвращает его из кэша.

**Параметры**:
- `model` (str): Название модели.
- `api_key` (str, optional): API-ключ. По умолчанию `None`.

**Возвращает**:
- `dict`: Соответствие моделей и провайдеров.

**Как работает функция**:

1. Проверяет, есть ли соответствие для данной модели в `cls.provider_mapping`. Если есть, возвращает его.
2. Если соответствие отсутствует, функция выполняет HTTP-запрос к API Hugging Face для получения информации о модели.
3. Извлекает `inferenceProviderMapping` из полученных данных и сохраняет его в `cls.provider_mapping` для данной модели.
4. Возвращает полученное соответствие.

**Примеры**:
```python
# Пример 1: Получение соответствия для модели
mapping = await HuggingFaceAPI.get_mapping("llama-2-7b", api_key="your_api_key")
print(mapping)
```

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        api_base: str = None,
        api_key: str = None,
        max_tokens: int = 2048,
        max_inputs_lenght: int = 10000,
        media: MediaListType = None,
        **kwargs
    ):
        """Создает асинхронный генератор для получения ответов от API.

        Args:
            model (str): Название модели.
            messages (Messages): Список сообщений для отправки в API.
            api_base (str, optional): Базовый URL API. По умолчанию `None`.
            api_key (str, optional): API-ключ. По умолчанию `None`.
            max_tokens (int, optional): Максимальное количество токенов в ответе. По умолчанию 2048.
            max_inputs_lenght (int, optional): Максимальная длина входных данных. По умолчанию 10000.
            media (MediaListType, optional): Список медиафайлов для отправки в API. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Yields:
            ProviderInfo | str: Информация о провайдере или чанк ответа.

        Raises:
            ModelNotSupportedError: Если модель не поддерживается.
            PaymentRequiredError: Если требуется оплата.
        """
        ...
```

**Назначение**: Создает асинхронный генератор для получения ответов от API Hugging Face. Генератор возвращает информацию о провайдере и чанки ответа.

**Параметры**:
- `model` (str): Название модели.
- `messages` (Messages): Список сообщений для отправки в API.
- `api_base` (str, optional): Базовый URL API. По умолчанию `None`.
- `api_key` (str, optional): API-ключ. По умолчанию `None`.
- `max_tokens` (int, optional): Максимальное количество токенов в ответе. По умолчанию 2048.
- `max_inputs_lenght` (int, optional): Максимальная длина входных данных. По умолчанию 10000.
- `media` (MediaListType, optional): Список медиафайлов для отправки в API. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `ProviderInfo | str`: Информация о провайдере или чанк ответа.

**Вызывает исключения**:
- `ModelNotSupportedError`: Если модель не поддерживается.
- `PaymentRequiredError`: Если требуется оплата.

**Как работает функция**:

1. Определяет модель для использования, если не указана явно, и если предоставлены медиафайлы, использует модель для обработки изображений по умолчанию.
2. Получает соответствие между моделью и провайдерами с помощью метода `cls.get_mapping`.
3. Если соответствие не найдено, вызывает исключение `ModelNotSupportedError`.
4. Перебирает провайдеров из соответствия. Для каждого провайдера:
    - Определяет базовый URL API и задачу (task).
    - Если задача не `"conversational"`, вызывает исключение `ModelNotSupportedError`.
    - Возвращает информацию о провайдере с помощью `yield ProviderInfo(...)`.
    - Вызывает `super().create_async_generator` для получения чанков ответа.
    - Передает каждый чанк ответа с помощью `yield chunk`.
5. Если в процессе возникает исключение `PaymentRequiredError`, оно сохраняется и обрабатывается следующим провайдером.
6. Если ни один провайдер не смог обработать запрос и было сохранено исключение `PaymentRequiredError`, оно вызывается.

**Примеры**:
```python
# Пример 1: Создание асинхронного генератора
messages = [{"role": "user", "content": "Hello, world!"}]
async for item in HuggingFaceAPI.create_async_generator(model="llama-2-7b", messages=messages, api_key="your_api_key"):
    print(item)
```

### `calculate_lenght`

```python
def calculate_lenght(messages: Messages) -> int:
    """Вычисляет суммарную длину содержимого сообщений.

    Args:
        messages (Messages): Список сообщений.

    Returns:
        int: Суммарная длина содержимого сообщений.
    """
    ...
```

**Назначение**: Вычисляет суммарную длину содержимого сообщений в списке, добавляя 16 к длине каждого сообщения.

**Параметры**:
- `messages` (Messages): Список сообщений.

**Возвращает**:
- `int`: Суммарная длина содержимого сообщений.

**Как работает функция**:

1. Проходит по каждому сообщению в списке `messages`.
2. Вычисляет длину содержимого каждого сообщения (`len(message["content"])`).
3. Добавляет 16 к длине каждого сообщения.
4. Суммирует полученные значения для всех сообщений.
5. Возвращает суммарную длину.

**Примеры**:
```python
# Пример 1: Вычисление длины сообщений
messages = [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "World!"}
]
total_length = calculate_lenght(messages)
print(total_length)  # Вывод: 27
```
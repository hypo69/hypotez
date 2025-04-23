# Модуль HuggingFaceInference

## Обзор

Модуль `HuggingFaceInference` предназначен для взаимодействия с моделями Hugging Face Inference API. Он предоставляет асинхронный генератор для получения ответов от моделей, поддерживает текстовые и графические модели, а также обработку различных форматов запросов.

## Детали

Этот модуль является частью проекта `hypotez` и обеспечивает интеграцию с платформой Hugging Face для использования различных моделей машинного обучения. Модуль включает в себя функции для получения списка доступных моделей, форматирования запросов и обработки ответов от API Hugging Face.

## Классы

### `HuggingFaceInference`

**Описание**: Класс `HuggingFaceInference` предоставляет функциональность для взаимодействия с API Hugging Face Inference.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию ответов.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.

**Атрибуты**:
- `url` (str): URL Hugging Face.
- `parent` (str): Родительский провайдер.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `default_model` (str): Модель, используемая по умолчанию.
- `default_image_model` (str): Графическая модель, используемая по умолчанию.
- `model_aliases` (dict): Псевдонимы моделей.
- `image_models` (list): Список графических моделей.
- `model_data` (dict): Данные о моделях.

**Принцип работы**:
Класс `HuggingFaceInference` использует API Hugging Face Inference для получения ответов от различных моделей. Он поддерживает как текстовые, так и графические модели, и может использоваться для генерации текста или изображений на основе входных данных. Класс также предоставляет методы для получения списка доступных моделей и форматирования запросов в соответствии с требованиями API Hugging Face.

**Методы**:
- `get_models()`: Возвращает список доступных моделей.
- `get_model_data(session: StreamSession, model: str) -> str`: Асинхронно получает данные о модели.
- `create_async_generator(...)`: Создает асинхронный генератор для получения ответов от модели.

## Функции

### `get_models()`

```python
@classmethod
def get_models(cls) -> list[str]:
    """
    Возвращает список доступных моделей из Hugging Face API.

    Args:
        cls (HuggingFaceInference): Класс HuggingFaceInference.

    Returns:
        list[str]: Список идентификаторов доступных моделей.

    Как работает:
        Функция выполняет запросы к Hugging Face API для получения списка текстовых и графических моделей,
        а также моделей с высоким рейтингом. Она объединяет эти списки и возвращает общий список доступных моделей.
    """
    ...
```

### `get_model_data`

```python
@classmethod
async def get_model_data(cls, session: StreamSession, model: str) -> str:
    """
    Асинхронно получает данные о модели из Hugging Face API.

    Args:
        cls (HuggingFaceInference): Класс HuggingFaceInference.
        session (StreamSession): Асинхронная сессия для выполнения HTTP-запросов.
        model (str): Идентификатор модели.

    Returns:
        str: Данные о модели в формате JSON.

    Raises:
        ModelNotSupportedError: Если модель не поддерживается.

    Как работает:
        Функция выполняет запрос к Hugging Face API для получения данных о конкретной модели.
        Если модель не найдена, выбрасывается исключение ModelNotSupportedError.
        Полученные данные кэшируются для последующего использования.
    """
    ...
```

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    stream: bool = True,
    proxy: str = None,
    timeout: int = 600,
    api_base: str = "https://api-inference.huggingface.co",
    api_key: str = None,
    max_tokens: int = 1024,
    temperature: float = None,
    prompt: str = None,
    action: str = None,
    extra_data: dict = {},
    seed: int = None,
    aspect_ratio: str = None,
    width: int = None,
    height: int = None,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для получения ответов от модели Hugging Face.

    Args:
        cls (HuggingFaceInference): Класс HuggingFaceInference.
        model (str): Идентификатор модели.
        messages (Messages): Список сообщений для отправки модели.
        stream (bool, optional): Флаг, указывающий на потоковую передачу данных. По умолчанию `True`.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        timeout (int, optional): Время ожидания запроса в секундах. По умолчанию 600.
        api_base (str, optional): Базовый URL API Hugging Face. По умолчанию "https://api-inference.huggingface.co".
        api_key (str, optional): API-ключ для доступа к Hugging Face. По умолчанию `None`.
        max_tokens (int, optional): Максимальное количество токенов в ответе. По умолчанию 1024.
        temperature (float, optional): Температура для генерации текста. По умолчанию `None`.
        prompt (str, optional): Дополнительный промпт для модели. По умолчанию `None`.
        action (str, optional): Действие, которое необходимо выполнить (например, "continue"). По умолчанию `None`.
        extra_data (dict, optional): Дополнительные данные для отправки в запросе. По умолчанию `{}`.
        seed (int, optional): Зерно для генерации случайных чисел. По умолчанию `None`.
        aspect_ratio (str, optional): Соотношение сторон изображения. По умолчанию `None`.
        width (int, optional): Ширина изображения. По умолчанию `None`.
        height (int, optional): Высота изображения. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от модели.

    Raises:
        ModelNotSupportedError: Если модель не поддерживается.
        ResponseError: Если произошла ошибка при получении ответа.

    Как работает:
        Функция создает асинхронный генератор, который отправляет запросы к API Hugging Face
        и возвращает ответы от модели. Она поддерживает потоковую передачу данных,
        а также обработку различных типов моделей (текстовые и графические).
        Функция также выполняет форматирование запросов и обработку ошибок.
    """
    ...
```

### `format_prompt_mistral`

```python
def format_prompt_mistral(messages: Messages, do_continue: bool = False) -> str:
    """
    Форматирует сообщения для модели Mistral.

    Args:
        messages (Messages): Список сообщений.
        do_continue (bool, optional): Флаг, указывающий на продолжение предыдущего диалога. По умолчанию `False`.

    Returns:
        str: Отформатированный промпт для модели Mistral.

    Как работает:
        Функция форматирует список сообщений в строку, пригодную для использования с моделью Mistral.
        Она объединяет системные сообщения и последние сообщения пользователя,
        а также добавляет историю предыдущих сообщений.
    """
    ...
```

### `format_prompt_qwen`

```python
def format_prompt_qwen(messages: Messages, do_continue: bool = False) -> str:
    """
    Форматирует сообщения для модели Qwen.

    Args:
        messages (Messages): Список сообщений.
        do_continue (bool, optional): Флаг, указывающий на продолжение предыдущего диалога. По умолчанию `False`.

    Returns:
        str: Отформатированный промпт для модели Qwen.

    Как работает:
        Функция форматирует список сообщений в строку, пригодную для использования с моделью Qwen.
        Она добавляет специальные теги для обозначения роли каждого сообщения.
    """
    ...
```

### `format_prompt_qwen2`

```python
def format_prompt_qwen2(messages: Messages, do_continue: bool = False) -> str:
    """
    Форматирует сообщения для модели Qwen2.

    Args:
        messages (Messages): Список сообщений.
        do_continue (bool, optional): Флаг, указывающий на продолжение предыдущего диалога. По умолчанию `False`.

    Returns:
        str: Отформатированный промпт для модели Qwen2.

    Как работает:
        Функция форматирует список сообщений в строку, пригодную для использования с моделью Qwen2.
        Она добавляет специальные теги для обозначения роли каждого сообщения.
    """
    ...
```

### `format_prompt_llama`

```python
def format_prompt_llama(messages: Messages, do_continue: bool = False) -> str:
    """
    Форматирует сообщения для модели Llama.

    Args:
        messages (Messages): Список сообщений.
        do_continue (bool, optional): Флаг, указывающий на продолжение предыдущего диалога. По умолчанию `False`.

    Returns:
        str: Отформатированный промпт для модели Llama.

    Как работает:
        Функция форматирует список сообщений в строку, пригодную для использования с моделью Llama.
        Она добавляет специальные теги для обозначения ролей и заголовков сообщений.
    """
    ...
```

### `format_prompt_custom`

```python
def format_prompt_custom(messages: Messages, end_token: str = "</s>", do_continue: bool = False) -> str:
    """
    Форматирует сообщения для пользовательских моделей.

    Args:
        messages (Messages): Список сообщений.
        end_token (str, optional): Токен конца сообщения. По умолчанию "</s>".
        do_continue (bool, optional): Флаг, указывающий на продолжение предыдущего диалога. По умолчанию `False`.

    Returns:
        str: Отформатированный промпт для пользовательской модели.

    Как работает:
        Функция форматирует список сообщений в строку, добавляя теги ролей и токен конца сообщения.
    """
    ...
```

### `get_inputs`

```python
def get_inputs(messages: Messages, model_data: dict, model_type: str, do_continue: bool = False) -> str:
    """
    Получает входные данные для модели на основе типа модели и данных.

    Args:
        messages (Messages): Список сообщений.
        model_data (dict): Данные о модели.
        model_type (str): Тип модели.
        do_continue (bool, optional): Флаг, указывающий на продолжение предыдущего диалога. По умолчанию `False`.

    Returns:
        str: Входные данные для модели.

    Как работает:
        Функция определяет формат входных данных на основе типа модели и данных о модели.
        Она вызывает соответствующие функции форматирования промптов
        и возвращает отформатированные входные данные.
    """
    ...
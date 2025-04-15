# Модуль `PollinationsAI`

## Обзор

Модуль `PollinationsAI` предоставляет класс `PollinationsAI`, который является асинхронным генератором для взаимодействия с API Pollinations AI. Он поддерживает генерацию текста и изображений на основе различных моделей, включая OpenAI, Flux и другие. Модуль также обеспечивает возможность работы с историей сообщений и системными сообщениями.

## Подробней

Этот модуль предназначен для интеграции с Pollinations AI, позволяя пользователям генерировать как текстовый контент, так и изображения, используя различные модели и параметры. Он также обрабатывает ошибки и обеспечивает гибкость в выборе моделей и настройках генерации.

## Классы

### `PollinationsAI`

**Описание**: Класс `PollinationsAI` является асинхронным генератором, который предоставляет интерфейс для взаимодействия с API Pollinations AI.

**Наследует**:

- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Добавляет функциональность для работы с моделями.

**Атрибуты**:

- `label` (str): Метка провайдера, `"Pollinations AI"`.
- `url` (str): URL провайдера, `"https://pollinations.ai"`.
- `working` (bool): Указывает, работает ли провайдер, `True`.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения, `True`.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений, `True`.
- `text_api_endpoint` (str): URL для API генерации текста, `"https://text.pollinations.ai"`.
- `openai_endpoint` (str): URL для API OpenAI, `"https://text.pollinations.ai/openai"`.
- `image_api_endpoint` (str): URL для API генерации изображений, `"https://image.pollinations.ai/"`.
- `default_model` (str): Модель по умолчанию, `"openai"`.
- `default_image_model` (str): Модель для генерации изображений по умолчанию, `"flux"`.
- `default_vision_model` (str): Модель для обработки изображений по умолчанию, `"openai"`.
- `text_models` (List[str]): Список поддерживаемых текстовых моделей, включая модель по умолчанию.
- `image_models` (List[str]): Список поддерживаемых моделей для генерации изображений, включая модель по умолчанию.
- `extra_image_models` (List[str]): Список дополнительных моделей для генерации изображений.
- `vision_models` (List[str]): Список моделей для обработки изображений.
- `extra_text_models` (List[str]): Список дополнительных текстовых моделей.
- `_models_loaded` (bool): Флаг, указывающий, загружены ли модели, `False`.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей, сопоставляющих различные имена моделей с их базовыми эквивалентами.

**Принцип работы**:

Класс `PollinationsAI` предназначен для упрощения взаимодействия с API Pollinations AI. Он предоставляет методы для генерации текста и изображений, поддерживает различные модели и параметры, а также обрабатывает ошибки. Класс использует асинхронные вызовы для эффективной работы с API и предоставляет гибкость в настройке процесса генерации.

**Методы**:

- `get_models(**kwargs)`: Возвращает список поддерживаемых моделей.
- `create_async_generator(model: str, messages: Messages, stream: bool = True, proxy: str = None, cache: bool = False, prompt: str = None, aspect_ratio: str = "1:1", width: int = None, height: int = None, seed: Optional[int] = None, nologo: bool = True, private: bool = False, enhance: bool = False, safe: bool = False, n: int = 1, media: MediaListType = None, temperature: float = None, presence_penalty: float = None, top_p: float = None, frequency_penalty: float = None, response_format: Optional[dict] = None, extra_parameters: list[str] = ["tools", "parallel_tool_calls", "tool_choice", "reasoning_effort", "logit_bias", "voice", "modalities", "audio"], **kwargs) -> AsyncResult`: Создает асинхронный генератор для генерации текста или изображений.
- `_generate_image(model: str, prompt: str, proxy: str, aspect_ratio: str, width: int, height: int, seed: Optional[int], cache: bool, nologo: bool, private: bool, enhance: bool, safe: bool, n: int) -> AsyncResult`: Генерирует изображения на основе заданных параметров.
- `_generate_text(model: str, messages: Messages, media: MediaListType, proxy: str, temperature: float, presence_penalty: float, top_p: float, frequency_penalty: float, response_format: Optional[dict], seed: Optional[int], cache: bool, stream: bool, extra_parameters: list[str], **kwargs) -> AsyncResult`: Генерирует текст на основе заданных параметров.

## Методы класса

### `get_models`

```python
@classmethod
def get_models(cls, **kwargs) -> List[str]:
    """
    Обновляет и возвращает список поддерживаемых моделей для генерации текста и изображений.

    Args:
        **kwargs: Дополнительные параметры.

    Returns:
        List[str]: Список поддерживаемых моделей.

    Raises:
        Exception: Если не удается получить список моделей с API.

    Как работает функция:
    - Функция пытается получить списки моделей для изображений и текста с API Pollinations AI.
    - Если получение удаётся, она обновляет атрибуты `cls.image_models` и `cls.text_models` класса.
    - В случае ошибки при получении списка моделей, используются модели по умолчанию.

    Примеры:
    >>> PollinationsAI.get_models()
    ['openai', 'flux']
    """
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
    cache: bool = False,
    # Image generation parameters
    prompt: str = None,
    aspect_ratio: str = "1:1",
    width: int = None,
    height: int = None,
    seed: Optional[int] = None,
    nologo: bool = True,
    private: bool = False,
    enhance: bool = False,
    safe: bool = False,
    n: int = 1,
    # Text generation parameters
    media: MediaListType = None,
    temperature: float = None,
    presence_penalty: float = None,
    top_p: float = None,
    frequency_penalty: float = None,
    response_format: Optional[dict] = None,
    extra_parameters: list[str] = ["tools", "parallel_tool_calls", "tool_choice", "reasoning_effort", "logit_bias", "voice", "modalities", "audio"],
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для генерации текста или изображений.

    Args:
        model (str): Модель для использования.
        messages (Messages): Список сообщений для генерации.
        stream (bool): Флаг для потоковой генерации.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        cache (bool, optional): Флаг для использования кэша. По умолчанию `False`.
        prompt (str, optional): Текст запроса для генерации изображения. По умолчанию `None`.
        aspect_ratio (str, optional): Соотношение сторон изображения. По умолчанию `"1:1"`.
        width (int, optional): Ширина изображения. По умолчанию `None`.
        height (int, optional): Высота изображения. По умолчанию `None`.
        seed (Optional[int], optional): Зерно для случайной генерации. По умолчанию `None`.
        nologo (bool, optional): Флаг для удаления логотипа. По умолчанию `True`.
        private (bool, optional): Флаг для приватной генерации. По умолчанию `False`.
        enhance (bool, optional): Флаг для улучшения изображения. По умолчанию `False`.
        safe (bool, optional): Флаг для безопасной генерации. По умолчанию `False`.
        n (int, optional): Количество генерируемых изображений. По умолчанию `1`.
        media (MediaListType, optional): Список медиафайлов для генерации текста. По умолчанию `None`.
        temperature (float, optional): Температура для генерации текста. По умолчанию `None`.
        presence_penalty (float, optional): Штраф за присутствие для генерации текста. По умолчанию `None`.
        top_p (float, optional): Значение top_p для генерации текста. По умолчанию `None`.
        frequency_penalty (float, optional): Штраф за частоту для генерации текста. По умолчанию `None`.
        response_format (Optional[dict], optional): Формат ответа. По умолчанию `None`.
        extra_parameters (list[str], optional): Дополнительные параметры.
        **kwargs: Дополнительные параметры.

    Yields:
        AsyncResult: Асинхронный результат генерации.

    Raises:
        ModelNotFoundError: Если модель не найдена.

    Как работает функция:
    - Загружает список моделей с помощью `cls.get_models()`.
    - Определяет, является ли запрошенная модель моделью для генерации изображений или текста.
    - Вызывает соответствующий метод (`_generate_image` или `_generate_text`) для генерации контента.
    - Возвращает асинхронный генератор, который выдает результаты генерации.

    Примеры:
    >>> async for chunk in PollinationsAI.create_async_generator(model="openai", messages=[{"role": "user", "content": "Hello"}]):
    ...     print(chunk)
    Hello
    """
```

### `_generate_image`

```python
@classmethod
async def _generate_image(
    cls,
    model: str,
    prompt: str,
    proxy: str,
    aspect_ratio: str,
    width: int,
    height: int,
    seed: Optional[int],
    cache: bool,
    nologo: bool,
    private: bool,
    enhance: bool,
    safe: bool,
    n: int
) -> AsyncResult:
    """
    Генерирует изображения на основе заданных параметров.

    Args:
        model (str): Модель для использования.
        prompt (str): Текст запроса для генерации изображения.
        proxy (str): Прокси-сервер для использования.
        aspect_ratio (str): Соотношение сторон изображения.
        width (int): Ширина изображения.
        height (int): Высота изображения.
        seed (Optional[int], optional): Зерно для случайной генерации. По умолчанию `None`.
        cache (bool): Флаг для использования кэша.
        nologo (bool): Флаг для удаления логотипа.
        private (bool): Флаг для приватной генерации.
        enhance (bool): Флаг для улучшения изображения.
        safe (bool): Флаг для безопасной генерации.
        n (int): Количество генерируемых изображений.

    Yields:
        AsyncResult: Асинхронный результат генерации изображения.

    Raises:
        Exception: Если происходит ошибка при получении изображения.

    Как работает функция:
    - Формирует параметры запроса на основе предоставленных аргументов.
    - Генерирует URL для запроса к API генерации изображений.
    - Отправляет асинхронный запрос к API и получает изображение.
    - Возвращает URL изображения в виде асинхронного генератора.

    Внутренние функции:

    `get_image_url(i: int = 0, seed: Optional[int] = None) -> str`:
        Внутренняя функция для создания URL-адреса изображения на основе индекса и зерна.

        Args:
            i (int, optional): Индекс изображения. По умолчанию 0.
            seed (Optional[int], optional): Зерно для случайной генерации. По умолчанию None.

        Returns:
            str: URL-адрес изображения.

    `get_image(i: int = 0, seed: Optional[int] = None) -> str`:
        Внутренняя асинхронная функция для получения изображения по URL-адресу.

        Args:
            i (int, optional): Индекс изображения. По умолчанию 0.
            seed (Optional[int], optional): Зерно для случайной генерации. По умолчанию None.

        Returns:
            str: URL-адрес полученного изображения.

        Raises:
            Exception: Если происходит ошибка при получении изображения.
    
    Примеры:
    >>> async for chunk in PollinationsAI._generate_image(model="flux", prompt="A cat", proxy=None, aspect_ratio="1:1", width=512, height=512, seed=None, cache=False, nologo=True, private=False, enhance=False, safe=True, n=1):
    ...     print(chunk)
    https://image.pollinations.ai/prompt/A%20cat?width=512&height=512&model=flux&nologo=true&private=false&enhance=false&safe=true&seed=12345
    """
```

### `_generate_text`

```python
@classmethod
async def _generate_text(
    cls,
    model: str,
    messages: Messages,
    media: MediaListType,
    proxy: str,
    temperature: float,
    presence_penalty: float,
    top_p: float,
    frequency_penalty: float,
    response_format: Optional[dict],
    seed: Optional[int],
    cache: bool,
    stream: bool,
    extra_parameters: list[str],
    **kwargs
) -> AsyncResult:
    """
    Генерирует текст на основе заданных параметров.

    Args:
        model (str): Модель для использования.
        messages (Messages): Список сообщений для генерации.
        media (MediaListType): Список медиафайлов для генерации текста.
        proxy (str): Прокси-сервер для использования.
        temperature (float): Температура для генерации текста.
        presence_penalty (float): Штраф за присутствие для генерации текста.
        top_p (float): Значение top_p для генерации текста.
        frequency_penalty (float): Штраф за частоту для генерации текста.
        response_format (Optional[dict], optional): Формат ответа. По умолчанию `None`.
        seed (Optional[int], optional): Зерно для случайной генерации. По умолчанию `None`.
        cache (bool): Флаг для использования кэша.
        stream (bool): Флаг для потоковой генерации.
        extra_parameters (list[str]): Список дополнительных параметров.
        **kwargs: Дополнительные параметры.

    Yields:
        AsyncResult: Асинхронный результат генерации текста.

    Raises:
        Exception: Если происходит ошибка при генерации текста.

    Как работает функция:
    - Формирует параметры запроса на основе предоставленных аргументов.
    - Определяет URL для запроса к API генерации текста (текстовый или OpenAI).
    - Отправляет асинхронный запрос к API и получает текст.
    - Возвращает текст в виде асинхронного генератора.
    - Обрабатывает различные типы ответов (text/plain, text/event-stream, application/json).
    - Поддерживает потоковую передачу данных.

    Примеры:
    >>> async for chunk in PollinationsAI._generate_text(model="openai", messages=[{"role": "user", "content": "Hello"}], media=None, proxy=None, temperature=0.7, presence_penalty=0.0, top_p=1.0, frequency_penalty=0.0, response_format=None, seed=None, cache=False, stream=True, extra_parameters=[]):
    ...     print(chunk)
    Hello
    """
```

## Параметры класса

- `label` (str): Метка провайдера, `"Pollinations AI"`.
- `url` (str): URL провайдера, `"https://pollinations.ai"`.
- `working` (bool): Указывает, работает ли провайдер, `True`.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения, `True`.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений, `True`.
- `text_api_endpoint` (str): URL для API генерации текста, `"https://text.pollinations.ai"`.
- `openai_endpoint` (str): URL для API OpenAI, `"https://text.pollinations.ai/openai"`.
- `image_api_endpoint` (str): URL для API генерации изображений, `"https://image.pollinations.ai/"`.
- `default_model` (str): Модель по умолчанию, `"openai"`.
- `default_image_model` (str): Модель для генерации изображений по умолчанию, `"flux"`.
- `default_vision_model` (str): Модель для обработки изображений по умолчанию, `"openai"`.
- `text_models` (List[str]): Список поддерживаемых текстовых моделей, включая модель по умолчанию.
- `image_models` (List[str]): Список поддерживаемых моделей для генерации изображений, включая модель по умолчанию.
- `extra_image_models` (List[str]): Список дополнительных моделей для генерации изображений.
- `vision_models` (List[str]): Список моделей для обработки изображений.
- `extra_text_models` (List[str]): Список дополнительных текстовых моделей.
- `_models_loaded` (bool): Флаг, указывающий, загружены ли модели, `False`.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей, сопоставляющих различные имена моделей с их базовыми эквивалентами.
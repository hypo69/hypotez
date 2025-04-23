# Модуль PollinationsAI

## Обзор

Модуль `PollinationsAI.py` представляет собой реализацию асинхронного провайдера для работы с API Pollinations AI, который предоставляет возможности генерации текста и изображений. Этот модуль предназначен для интеграции с другими частями проекта `hypotez` и обеспечивает удобный интерфейс для взаимодействия с сервисами Pollinations AI.

## Более подробно

Этот модуль является асинхронным провайдером, что позволяет ему эффективно обрабатывать запросы к API Pollinations AI, не блокируя основной поток выполнения. Он поддерживает как генерацию текста, так и генерацию изображений, а также предоставляет возможность настройки параметров запросов. Модуль также включает поддержку моделей машинного обучения и обработку ошибок.

## Классы

### `PollinationsAI`

**Описание**:
Класс `PollinationsAI` является основным классом, реализующим асинхронный провайдер для работы с API Pollinations AI. Он наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет методы для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера ("Pollinations AI").
- `url` (str): URL сайта Pollinations AI ("https://pollinations.ai").
- `working` (bool): Флаг, указывающий на работоспособность провайдера (True).
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений (True).
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений (True).
- `text_api_endpoint` (str): URL API для генерации текста ("https://text.pollinations.ai").
- `openai_endpoint` (str): URL API OpenAI ("https://text.pollinations.ai/openai").
- `image_api_endpoint` (str): URL API для генерации изображений ("https://image.pollinations.ai/").
- `default_model` (str): Модель по умолчанию для генерации текста ("openai").
- `default_image_model` (str): Модель по умолчанию для генерации изображений ("flux").
- `default_vision_model` (str): Модель по умолчанию для обработки изображений (`default_model`).
- `text_models` (list[str]): Список моделей для генерации текста ([`default_model`]).
- `image_models` (list[str]): Список моделей для генерации изображений ([`default_image_model`]).
- `extra_image_models` (list[str]): Список дополнительных моделей для генерации изображений (["flux-pro", "flux-dev", "flux-schnell", "midjourney", "dall-e-3", "turbo"]).
- `vision_models` (list[str]): Список моделей для обработки изображений ([`default_vision_model`, "gpt-4o-mini", "o3-mini", "openai", "openai-large"]).
- `extra_text_models` (list[str]): Список дополнительных моделей для генерации текста (`vision_models`).
- `_models_loaded` (bool): Флаг, указывающий на загрузку моделей (False).
- `model_aliases` (dict[str, str]): Словарь псевдонимов моделей.

**Принцип работы**:
Класс `PollinationsAI` предоставляет интерфейс для взаимодействия с API Pollinations AI, поддерживая генерацию текста и изображений. Он использует асинхронные запросы для обеспечения высокой производительности и предоставляет возможность настройки параметров запросов. Класс также управляет списком доступных моделей и их псевдонимами.

**Методы**:
- `get_models(**kwargs)`: Возвращает список доступных моделей.
- `create_async_generator(model: str, messages: Messages, stream: bool = True, proxy: str = None, cache: bool = False, prompt: str = None, aspect_ratio: str = "1:1", width: int = None, height: int = None, seed: Optional[int] = None, nologo: bool = True, private: bool = False, enhance: bool = False, safe: bool = False, n: int = 1, media: MediaListType = None, temperature: float = None, presence_penalty: float = None, top_p: float = None, frequency_penalty: float = None, response_format: Optional[dict] = None, extra_parameters: list[str] = ["tools", "parallel_tool_calls", "tool_choice", "reasoning_effort", "logit_bias", "voice", "modalities", "audio"], **kwargs) -> AsyncResult`: Создает асинхронный генератор для генерации текста или изображений.
- `_generate_image(model: str, prompt: str, proxy: str, aspect_ratio: str, width: int, height: int, seed: Optional[int], cache: bool, nologo: bool, private: bool, enhance: bool, safe: bool, n: int) -> AsyncResult`: Асинхронно генерирует изображения.
- `_generate_text(model: str, messages: Messages, media: MediaListType, proxy: str, temperature: float, presence_penalty: float, top_p: float, frequency_penalty: float, response_format: Optional[dict], seed: Optional[int], cache: bool, stream: bool, extra_parameters: list[str], **kwargs) -> AsyncResult`: Асинхронно генерирует текст.

## Методы класса

### `get_models`

```python
@classmethod
def get_models(cls, **kwargs)
```

**Назначение**:
Обновляет и возвращает список доступных моделей для генерации текста и изображений.

**Параметры**:
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `list[str]`: Список доступных моделей.

**Принцип работы**:
Функция пытается получить списки доступных моделей с серверов `image.pollinations.ai` и `text.pollinations.ai`. В случае успеха она объединяет полученные списки с локальными списками моделей и сохраняет их в атрибутах класса `cls.image_models` и `cls.text_models`. Если получение списков с серверов не удается, используются локальные списки моделей по умолчанию. В случае возникновения исключения, информация об ошибке логируется.

**Пример**:

```python
PollinationsAI.get_models()
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
    media: MediaListType = None,
    temperature: float = None,
    presence_penalty: float = None,
    top_p: float = None,
    frequency_penalty: float = None,
    response_format: Optional[dict] = None,
    extra_parameters: list[str] = ["tools", "parallel_tool_calls", "tool_choice", "reasoning_effort", "logit_bias", "voice", "modalities", "audio"],
    **kwargs
) -> AsyncResult
```

**Назначение**:
Создает асинхронный генератор для генерации текста или изображений в зависимости от указанной модели.

**Параметры**:
- `model` (str): Модель для генерации.
- `messages` (Messages): Список сообщений для генерации текста.
- `stream` (bool): Флаг, указывающий на потоковую генерацию текста (по умолчанию `True`).
- `proxy` (str): URL прокси-сервера (по умолчанию `None`).
- `cache` (bool): Флаг, указывающий на использование кэша (по умолчанию `False`).
- `prompt` (str): Текст запроса для генерации изображения (по умолчанию `None`).
- `aspect_ratio` (str): Соотношение сторон изображения (по умолчанию `"1:1"`).
- `width` (int): Ширина изображения (по умолчанию `None`).
- `height` (int): Высота изображения (по умолчанию `None`).
- `seed` (Optional[int]): Зерно для генерации случайных чисел (по умолчанию `None`).
- `nologo` (bool): Флаг, указывающий на отсутствие логотипа на изображении (по умолчанию `True`).
- `private` (bool): Флаг, указывающий на приватность изображения (по умолчанию `False`).
- `enhance` (bool): Флаг, указывающий на улучшение изображения (по умолчанию `False`).
- `safe` (bool): Флаг, указывающий на безопасную генерацию (по умолчанию `False`).
- `n` (int): Количество генерируемых изображений (по умолчанию `1`).
- `media` (MediaListType): Список медиафайлов для генерации текста (по умолчанию `None`).
- `temperature` (float): Температура для генерации текста (по умолчанию `None`).
- `presence_penalty` (float): Штраф за присутствие токенов в тексте (по умолчанию `None`).
- `top_p` (float): Параметр `top_p` для генерации текста (по умолчанию `None`).
- `frequency_penalty` (float): Штраф за частоту токенов в тексте (по умолчанию `None`).
- `response_format` (Optional[dict]): Формат ответа (по умолчанию `None`).
- `extra_parameters` (list[str]): Список дополнительных параметров для генерации текста (по умолчанию `["tools", "parallel_tool_calls", "tool_choice", "reasoning_effort", "logit_bias", "voice", "modalities", "audio"]`).
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор для получения результатов.

**Принцип работы**:
Функция сначала загружает список доступных моделей. Затем, в зависимости от указанной модели, она вызывает либо `_generate_image` для генерации изображений, либо `_generate_text` для генерации текста. Если указана аудиомодель, то для нее выбирается первая доступная модель. В случае, если модель не найдена в списке доступных, выбрасывается исключение `ModelNotFoundError`.

**Примеры**:

```python
async for chunk in PollinationsAI.create_async_generator(
    model="openai",
    messages=[{"role": "user", "content": "Hello, world!"}]
):
    print(chunk)
```

```python
async for chunk in PollinationsAI.create_async_generator(
    model="flux",
    prompt="A cat sitting on a mat",
    aspect_ratio="16:9"
):
    print(chunk)
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
) -> AsyncResult
```

**Назначение**:
Асинхронно генерирует изображения на основе заданных параметров.

**Параметры**:
- `model` (str): Модель для генерации изображений.
- `prompt` (str): Текст запроса для генерации изображения.
- `proxy` (str): URL прокси-сервера.
- `aspect_ratio` (str): Соотношение сторон изображения.
- `width` (int): Ширина изображения.
- `height` (int): Высота изображения.
- `seed` (Optional[int]): Зерно для генерации случайных чисел.
- `cache` (bool): Флаг, указывающий на использование кэша.
- `nologo` (bool): Флаг, указывающий на отсутствие логотипа на изображении.
- `private` (bool): Флаг, указывающий на приватность изображения.
- `enhance` (bool): Флаг, указывающий на улучшение изображения.
- `safe` (bool): Флаг, указывающий на безопасную генерацию.
- `n` (int): Количество генерируемых изображений.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор для получения результатов.

**Принцип работы**:
Функция формирует URL для запроса к API генерации изображений на основе заданных параметров. Она использует `ClientSession` для выполнения асинхронных запросов и возвращает URL сгенерированных изображений.

**Примеры**:

```python
async for chunk in PollinationsAI._generate_image(
    model="flux",
    prompt="A cat sitting on a mat",
    aspect_ratio="16:9",
    proxy=None,
    width=512,
    height=512,
    seed=None,
    cache=False,
    nologo=True,
    private=False,
    enhance=False,
    safe=True,
    n=1
):
    print(chunk)
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
) -> AsyncResult
```

**Назначение**:
Асинхронно генерирует текст на основе заданных параметров.

**Параметры**:
- `model` (str): Модель для генерации текста.
- `messages` (Messages): Список сообщений для генерации текста.
- `media` (MediaListType): Список медиафайлов для генерации текста.
- `proxy` (str): URL прокси-сервера.
- `temperature` (float): Температура для генерации текста.
- `presence_penalty` (float): Штраф за присутствие токенов в тексте.
- `top_p` (float): Параметр `top_p` для генерации текста.
- `frequency_penalty` (float): Штраф за частоту токенов в тексте.
- `response_format` (Optional[dict]): Формат ответа.
- `seed` (Optional[int]): Зерно для генерации случайных чисел.
- `cache` (bool): Флаг, указывающий на использование кэша.
- `stream` (bool): Флаг, указывающий на потоковую генерацию текста.
- `extra_parameters` (list[str]): Список дополнительных параметров для генерации текста.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор для получения результатов.

**Принцип работы**:
Функция формирует запрос к API генерации текста на основе заданных параметров. Она использует `ClientSession` для выполнения асинхронных запросов и обрабатывает ответы в различных форматах (текст, JSON, потоковое вещание). В зависимости от формата ответа, функция возвращает либо текст, либо информацию об использовании, либо причину завершения генерации.

**Примеры**:

```python
async for chunk in PollinationsAI._generate_text(
    model="openai",
    messages=[{"role": "user", "content": "Hello, world!"}],
    media=None,
    proxy=None,
    temperature=0.7,
    presence_penalty=0.0,
    top_p=1.0,
    frequency_penalty=0.0,
    response_format=None,
    seed=None,
    cache=False,
    stream=True,
    extra_parameters=["tools"]
):
    print(chunk)
```
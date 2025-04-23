# Модуль Airforce
## Обзор

Модуль `Airforce` предоставляет асинхронный интерфейс для взаимодействия с API Airforce для генерации текста и изображений. Он поддерживает потоковую передачу текста, настройку системных сообщений и использование истории сообщений. Модуль включает в себя функции для фильтрации контента и обработки ответов, чтобы обеспечить чистый и управляемый результат.

## Подробнее

Этот модуль является частью проекта `hypotez` и предназначен для обеспечения доступа к моделям Airforce для генерации текста и изображений. Он включает в себя методы для получения списка доступных моделей, фильтрации содержимого и обработки ответов от API. Модуль также поддерживает потоковую передачу текста и генерацию изображений.

## Классы

### `Airforce`

**Описание**: Класс `Airforce` предоставляет асинхронный интерфейс для взаимодействия с API Airforce для генерации текста и изображений.

**Наследует**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Атрибуты**:
- `url` (str): Базовый URL API Airforce.
- `api_endpoint_completions` (str): URL для API завершения текста.
- `api_endpoint_imagine2` (str): URL для API генерации изображений.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
- `default_model` (str): Модель, используемая по умолчанию для генерации текста.
- `default_image_model` (str): Модель, используемая по умолчанию для генерации изображений.
- `models` (List[str]): Список доступных моделей для генерации текста.
- `image_models` (List[str]): Список доступных моделей для генерации изображений.
- `hidden_models` (Set[str]): Набор скрытых моделей.
- `additional_models_imagine` (List[str]): Список дополнительных моделей для генерации изображений.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей.

**Методы**:
- `get_models()`: Получает список доступных моделей.
- `get_model(model: str) -> str`: Получает фактическое имя модели из псевдонима.
- `_filter_content(part_response: str) -> str`: Фильтрует нежелательный контент из частичного ответа.
- `_filter_response(response: str) -> str`: Фильтрует полный ответ для удаления системных ошибок и другого нежелательного текста.
- `generate_image(model: str, prompt: str, size: str, seed: int, proxy: str = None) -> AsyncResult`: Генерирует изображение на основе предоставленных параметров.
- `generate_text(model: str, messages: Messages, max_tokens: int, temperature: float, top_p: float, stream: bool, proxy: str = None) -> AsyncResult`: Генерирует текст на основе предоставленных параметров.
- `create_async_generator(model: str, messages: Messages, prompt: str = None, proxy: str = None, max_tokens: int = 512, temperature: float = 1, top_p: float = 1, stream: bool = True, size: str = "1:1", seed: int = None, **kwargs) -> AsyncResult`: Создает асинхронный генератор для генерации текста или изображений.

## Функции

### `split_message`

```python
def split_message(message: str, max_length: int = 1000) -> List[str]:
    """Splits the message into parts up to (max_length)."""
```

**Назначение**: Разделяет сообщение на части длиной не более `max_length`.

**Параметры**:
- `message` (str): Сообщение для разделения.
- `max_length` (int, optional): Максимальная длина каждой части. По умолчанию `1000`.

**Возвращает**:
- `List[str]`: Список частей сообщения.

**Как работает функция**:
Функция `split_message` разделяет входное сообщение на несколько частей, где каждая часть имеет длину не более `max_length`. Если в пределах `max_length` находится пробел, разделение происходит по этому пробелу. Если пробелов нет, разделение происходит по достижении `max_length`.

**Примеры**:
```python
>>> split_message("This is a long message that needs to be split", max_length=10)
['This is a ', 'long messa', 'ge that ne', 'eds to be ', 'split']

>>> split_message("Short message", max_length=100)
['Short message']
```

### `Airforce.get_models`

```python
    @classmethod
    def get_models(cls):
        """Get available models with error handling"""
```

**Назначение**: Получает список доступных моделей из API Airforce.

**Параметры**:
- Нет

**Возвращает**:
- `List[str]`: Список доступных моделей.

**Как работает функция**:
Функция `get_models` пытается получить список доступных моделей для генерации изображений и текста из API Airforce. Если запрос успешен, она объединяет списки моделей для изображений и текста, удаляет скрытые модели и возвращает результат. В случае ошибки возвращает список псевдонимов моделей.

**Примеры**:
```python
>>> Airforce.get_models()
['llama-3.1-70b-chat', 'flux-1.1-pro', 'midjourney', 'dall-e-3', ...]
```

### `Airforce.get_model`

```python
    @classmethod
    def get_model(cls, model: str) -> str:\n        """Get the actual model name from alias"""
```

**Назначение**: Получает фактическое имя модели из псевдонима.

**Параметры**:
- `model` (str): Псевдоним модели.

**Возвращает**:
- `str`: Фактическое имя модели.

**Как работает функция**:
Функция `get_model` принимает псевдоним модели и возвращает соответствующее фактическое имя модели из словаря `model_aliases`. Если псевдоним не найден, возвращается либо переданное имя модели, либо `default_model`.

**Примеры**:
```python
>>> Airforce.get_model("openchat-3.5")
'openchat-3.5-0106'

>>> Airforce.get_model("unknown_model")
'unknown_model'
```

### `Airforce._filter_content`

```python
    @classmethod
    def _filter_content(cls, part_response: str) -> str:
        """
        Filters out unwanted content from the partial response.
        """
```

**Назначение**: Фильтрует нежелательный контент из частичного ответа.

**Параметры**:
- `part_response` (str): Частичный ответ для фильтрации.

**Возвращает**:
- `str`: Отфильтрованный частичный ответ.

**Как работает функция**:
Функция `_filter_content` использует регулярные выражения для удаления нежелательного контента из частичного ответа, такого как сообщения об ограничении длины и превышении лимита запросов.

**Примеры**:
```python
>>> Airforce._filter_content("One message exceeds the 1000 chars per message limit. Join our discord...")
''

>>> Airforce._filter_content("Rate limit (10/minute) exceeded. Join our discord for more...")
''
```

### `Airforce._filter_response`

```python
    @classmethod
    def _filter_response(cls, response: str) -> str:
        """
        Filters the full response to remove system errors and other unwanted text.
        """
```

**Назначение**: Фильтрует полный ответ для удаления системных ошибок и другого нежелательного текста.

**Параметры**:
- `response` (str): Полный ответ для фильтрации.

**Возвращает**:
- `str`: Отфильтрованный полный ответ.

**Вызывает исключения**:
- `ValueError`: Если ответ содержит сообщение об ошибке "Model not found or too long input. Or any other error (xD)".

**Как работает функция**:
Функция `_filter_response` использует регулярные выражения для удаления системных ошибок и нежелательного текста из полного ответа. Она также вызывает исключение `ValueError`, если ответ содержит сообщение об ошибке, указывающее на то, что модель не найдена или входные данные слишком длинные.

**Примеры**:
```python
>>> Airforce._filter_response("[ERROR] 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx' Some text")
'Some text'

>>> Airforce._filter_response("<|im_end|> Some text")
'Some text'
```

### `Airforce.generate_image`

```python
    @classmethod
    async def generate_image(
        cls,
        model: str,
        prompt: str,
        size: str,
        seed: int,
        proxy: str = None
    ) -> AsyncResult:
        """
        Генерирует изображение на основе предоставленных параметров.
        """
```

**Назначение**: Генерирует изображение, используя API Airforce.

**Параметры**:
- `model` (str): Модель для генерации изображения.
- `prompt` (str): Текст запроса для генерации изображения.
- `size` (str): Размер изображения.
- `seed` (int): Зерно для генерации изображения.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.

**Возвращает**:
- `AsyncResult`: Асинхронный результат, содержащий URL-адрес сгенерированного изображения.

**Вызывает исключения**:
- `RuntimeError`: Если генерация изображения завершается с ошибкой.

**Как работает функция**:
Функция `generate_image` отправляет запрос к API Airforce для генерации изображения на основе предоставленных параметров. Если запрос успешен, она возвращает URL-адрес сгенерированного изображения. В случае ошибки выбрасывается исключение `RuntimeError`.

**Примеры**:
```python
>>> async for result in Airforce.generate_image(model="flux", prompt="A cat", size="1:1", seed=123):
...     print(result)
ImageResponse(images='https://example.com/image.png', alt='A cat')
```

### `Airforce.generate_text`

```python
    @classmethod
    async def generate_text(
        cls,
        model: str,
        messages: Messages,
        max_tokens: int,
        temperature: float,
        top_p: float,
        stream: bool,
        proxy: str = None
    ) -> AsyncResult:
        """
        Generates text, buffers the response, filters it, and returns the final result.
        """
```

**Назначение**: Генерирует текст, используя API Airforce.

**Параметры**:
- `model` (str): Модель для генерации текста.
- `messages` (Messages): Список сообщений для генерации текста.
- `max_tokens` (int): Максимальное количество токенов в ответе.
- `temperature` (float): Температура для генерации текста.
- `top_p` (float): Top-p для генерации текста.
- `stream` (bool): Указывает, использовать ли потоковую передачу.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.

**Возвращает**:
- `AsyncResult`: Асинхронный результат, содержащий сгенерированный текст.

**Как работает функция**:
Функция `generate_text` отправляет запрос к API Airforce для генерации текста на основе предоставленных параметров. Если `stream` установлен в `True`, она использует потоковую передачу для получения ответа. В противном случае она получает полный ответ и фильтрует его.

**Примеры**:
```python
>>> messages = [{"role": "user", "content": "Hello"}]
>>> async for result in Airforce.generate_text(model="llama-3.1-70b-chat", messages=messages, max_tokens=100, temperature=0.7, top_p=0.9, stream=True):
...     print(result)
Hello
```

### `Airforce.create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        prompt: str = None,
        proxy: str = None,
        max_tokens: int = 512,
        temperature: float = 1,
        top_p: float = 1,
        stream: bool = True,
        size: str = "1:1",
        seed: int = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для генерации текста или изображений.
        """
```

**Назначение**: Создает асинхронный генератор для генерации текста или изображений.

**Параметры**:
- `model` (str): Модель для генерации.
- `messages` (Messages): Список сообщений для генерации текста.
- `prompt` (str, optional): Текст запроса для генерации изображения. По умолчанию `None`.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `max_tokens` (int, optional): Максимальное количество токенов в ответе. По умолчанию `512`.
- `temperature` (float, optional): Температура для генерации текста. По умолчанию `1`.
- `top_p` (float, optional): Top-p для генерации текста. По умолчанию `1`.
- `stream` (bool, optional): Указывает, использовать ли потоковую передачу. По умолчанию `True`.
- `size` (str, optional): Размер изображения. По умолчанию `"1:1"`.
- `seed` (int, optional): Зерно для генерации изображения. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный результат, содержащий сгенерированный текст или изображение.

**Как работает функция**:
Функция `create_async_generator` создает асинхронный генератор для генерации текста или изображений. Если модель находится в списке моделей изображений, вызывается `generate_image`. В противном случае вызывается `generate_text`.

**Примеры**:
```python
>>> messages = [{"role": "user", "content": "Hello"}]
>>> async for result in Airforce.create_async_generator(model="llama-3.1-70b-chat", messages=messages):
...     print(result)
Hello
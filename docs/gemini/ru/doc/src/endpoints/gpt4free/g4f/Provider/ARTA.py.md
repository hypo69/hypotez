# Модуль ARTA для генерации изображений

## Обзор

Модуль `ARTA` предоставляет реализацию асинхронного генератора изображений с использованием API `ai-arta.com`.

## Подробности

Модуль использует асинхронную генерацию с использованием `asyncio` и `aiohttp` для оптимизации запросов к API. Предоставляет возможность использовать различные модели для генерации изображений.

## Классы

### `class ARTA`

**Описание**: Класс `ARTA` реализует асинхронный генератор изображений, предоставляя методы для аутентификации и генерации изображений.

**Наследует**: 
    - `AsyncGeneratorProvider`: Класс, предоставляющий асинхронный генератор для обработки данных.
    - `ProviderModelMixin`: Класс, предоставляющий функциональность выбора модели.

**Атрибуты**:

    - `url (str)`: Базовый URL для API.
    - `auth_url (str)`: URL для получения токена аутентификации.
    - `token_refresh_url (str)`: URL для обновления токена.
    - `image_generation_url (str)`: URL для генерации изображений.
    - `status_check_url (str)`: URL для проверки статуса генерации.
    - `working (bool)`: Флаг, показывающий, доступен ли провайдер.
    - `default_model (str)`: Модель по умолчанию.
    - `default_image_model (str)`: Модель по умолчанию для генерации изображений.
    - `model_aliases (dict)`: Словарь алиасов для моделей.
    - `image_models (list)`: Список доступных моделей для генерации изображений.
    - `models (list)`: Список доступных моделей.

**Методы**:

    - `get_auth_file()`: Возвращает путь к файлу с данными аутентификации.
    - `create_token(path: Path, proxy: str | None = None)`: Создает новый токен аутентификации и сохраняет его в файл.
    - `refresh_token(refresh_token: str, proxy: str = None) -> tuple[str, str]`: Обновляет токен аутентификации.
    - `read_and_refresh_token(proxy: str | None = None) -> str`: Считывает и обновляет токен аутентификации из файла, если необходимо.
    - `create_async_generator(model: str, messages: Messages, proxy: str = None, prompt: str = None, negative_prompt: str = "blurry, deformed hands, ugly", n: int = 1, guidance_scale: int = 7, num_inference_steps: int = 30, aspect_ratio: str = "1:1", seed: int = None, **kwargs) -> AsyncResult`: Асинхронный генератор, который выполняет генерацию изображений и возвращает результаты.
    - `get_model(model: str) -> str`: Возвращает модель по имени или алиасу.


###  `create_token(path: Path, proxy: str | None = None)`

**Назначение**: Функция создает токен аутентификации, отправляя запрос на API `ai-arta.com`.

**Параметры**:

    - `path (Path)`: Путь к файлу для сохранения данных аутентификации.
    - `proxy (str | None)`: Прокси-сервер для запросов, если требуется.

**Возвращает**:

    - `dict`: Данные аутентификации, включая токен и информацию об обновлении.

**Вызывает исключения**:

    - `ResponseError`: Если не удалось получить токен аутентификации.

**Пример**:

```python
>>> from hypotez.src.endpoints.gpt4free.g4f.Provider.ARTA import ARTA
>>> from pathlib import Path
>>> path = Path("auth_data.json")
>>> token_data = ARTA.create_token(path)
>>> print(token_data) 
```

### `refresh_token(refresh_token: str, proxy: str = None) -> tuple[str, str]`

**Назначение**: Обновляет токен аутентификации, используя предоставленный `refresh_token`.

**Параметры**:

    - `refresh_token (str)`: Токен обновления.
    - `proxy (str)`: Прокси-сервер для запросов, если требуется.

**Возвращает**:

    - `tuple[str, str]`: Новый токен аутентификации и обновленный токен обновления.

**Вызывает исключения**:

    - `ResponseError`: Если не удалось обновить токен.

**Пример**:

```python
>>> from hypotez.src.endpoints.gpt4free.g4f.Provider.ARTA import ARTA
>>> refresh_token = "your_refresh_token"
>>> new_token, new_refresh_token = ARTA.refresh_token(refresh_token)
>>> print(new_token, new_refresh_token) 
```

### `read_and_refresh_token(proxy: str | None = None) -> str`

**Назначение**:  Считывает данные аутентификации из файла и обновляет токен, если требуется.

**Параметры**:

    - `proxy (str | None)`: Прокси-сервер для запросов, если требуется.

**Возвращает**:

    - `str`: Токен аутентификации.

**Пример**:

```python
>>> from hypotez.src.endpoints.gpt4free.g4f.Provider.ARTA import ARTA
>>> token = ARTA.read_and_refresh_token()
>>> print(token) 
```

### `create_async_generator(model: str, messages: Messages, proxy: str = None, prompt: str = None, negative_prompt: str = "blurry, deformed hands, ugly", n: int = 1, guidance_scale: int = 7, num_inference_steps: int = 30, aspect_ratio: str = "1:1", seed: int = None, **kwargs) -> AsyncResult`

**Назначение**: Асинхронный генератор, который создает и возвращает изображения, используя  API `ai-arta.com`.

**Параметры**:

    - `model (str)`: Модель для генерации изображений.
    - `messages (Messages)`: Сообщения для контекста.
    - `proxy (str)`: Прокси-сервер для запросов, если требуется.
    - `prompt (str)`: Текстовый запрос для генерации изображений.
    - `negative_prompt (str)`: Текстовый запрос, описывающий то, чего не должно быть на изображении.
    - `n (int)`: Количество изображений для генерации.
    - `guidance_scale (int)`: Уровень  "направляющего" сигнала модели.
    - `num_inference_steps (int)`: Количество шагов  генерации изображений.
    - `aspect_ratio (str)`: Соотношение сторон для изображений.
    - `seed (int)`: Случайное число для инициализации генератора, если требуется.
    - `**kwargs`: Дополнительные аргументы для модели.

**Возвращает**:

    - `AsyncResult`: Асинхронный результат, представляющий процесс генерации изображений.

**Вызывает исключения**:

    - `ResponseError`: Если не удалось создать или получить изображения.

**Пример**:

```python
>>> from hypotez.src.endpoints.gpt4free.g4f.Provider.ARTA import ARTA
>>> from hypotez.src.endpoints.gpt4free.g4f.typing import Messages
>>> messages = Messages(history=[])
>>> async def main():
...     async for response in ARTA.create_async_generator(model="Flux", messages=messages, prompt="a cat sitting on a chair"):
...         print(response)
... 
>>> asyncio.run(main())
```

## Параметры класса

    - `model (str)`: Модель для генерации изображений. Список доступных моделей:
    ```python
    >>> from hypotez.src.endpoints.gpt4free.g4f.Provider.ARTA import ARTA
    >>> print(ARTA.models)
    ```
    - `messages (Messages)`: Сообщения для контекста. 
    - `proxy (str)`: Прокси-сервер для запросов, если требуется.
    - `prompt (str)`: Текстовый запрос для генерации изображений.
    - `negative_prompt (str)`: Текстовый запрос, описывающий то, чего не должно быть на изображении.
    - `n (int)`: Количество изображений для генерации.
    - `guidance_scale (int)`: Уровень  "направляющего" сигнала модели.
    - `num_inference_steps (int)`: Количество шагов  генерации изображений.
    - `aspect_ratio (str)`: Соотношение сторон для изображений.
    - `seed (int)`: Случайное число для инициализации генератора, если требуется.
    - `**kwargs`: Дополнительные аргументы для модели.

## Примеры

### Генерация изображения с использованием модели Flux

```python
>>> from hypotez.src.endpoints.gpt4free.g4f.Provider.ARTA import ARTA
>>> from hypotez.src.endpoints.gpt4free.g4f.typing import Messages
>>> messages = Messages(history=[])
>>> async def main():
...     async for response in ARTA.create_async_generator(model="Flux", messages=messages, prompt="a cat sitting on a chair"):
...         print(response)
... 
>>> asyncio.run(main())
```

### Генерация изображения с использованием модели "Vincent Van Gogh"

```python
>>> from hypotez.src.endpoints.gpt4free.g4f.Provider.ARTA import ARTA
>>> from hypotez.src.endpoints.gpt4free.g4f.typing import Messages
>>> messages = Messages(history=[])
>>> async def main():
...     async for response in ARTA.create_async_generator(model="Vincent Van Gogh", messages=messages, prompt="a portrait of a woman in a field of sunflowers"):
...         print(response)
... 
>>> asyncio.run(main())
```

### Генерация нескольких изображений с использованием модели "Anything-xl"

```python
>>> from hypotez.src.endpoints.gpt4free.g4f.Provider.ARTA import ARTA
>>> from hypotez.src.endpoints.gpt4free.g4f.typing import Messages
>>> messages = Messages(history=[])
>>> async def main():
...     async for response in ARTA.create_async_generator(model="Anything-xl", messages=messages, prompt="a futuristic cityscape", n=3):
...         print(response)
... 
>>> asyncio.run(main())
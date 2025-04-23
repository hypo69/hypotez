# Модуль `DeepInfra`

## Обзор

Модуль `DeepInfra` предоставляет класс для взаимодействия с сервисом DeepInfra, который предоставляет доступ к различным моделям машинного обучения, включая модели генерации текста и изображений. Класс `DeepInfra` наследуется от `OpenaiTemplate` и предоставляет методы для получения списка доступных моделей, а также для создания асинхронных генераторов и запросов на генерацию изображений.

## Подробней

Модуль предназначен для интеграции с сервисом DeepInfra для использования его моделей машинного обучения. Он поддерживает как текстовые, так и графические модели. Для работы с сервисом требуется аутентификация с использованием API ключа.

## Классы

### `DeepInfra`

**Описание**: Класс для взаимодействия с сервисом DeepInfra.

**Наследует**:
- `OpenaiTemplate`: Предоставляет базовый функционал для работы с OpenAI-совместимыми API.

**Атрибуты**:
- `url` (str): URL сервиса DeepInfra.
- `login_url` (str): URL страницы для получения API ключа.
- `api_base` (str): Базовый URL для API запросов.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `needs_auth` (bool): Флаг, указывающий на необходимость аутентификации.
- `default_model` (str): Модель, используемая по умолчанию для генерации текста.
- `default_image_model` (str): Модель, используемая по умолчанию для генерации изображений.
- `models` (list): Список доступных моделей для генерации текста.
- `image_models` (list): Список доступных моделей для генерации изображений.

**Методы**:
- `get_models(**kwargs)`: Получает список доступных моделей.
- `get_image_models(**kwargs)`: Получает список доступных моделей для генерации изображений.
- `create_async_generator(model: str, messages: Messages, stream: bool, prompt: str = None, temperature: float = 0.7, max_tokens: int = 1028, **kwargs) -> AsyncResult`: Создает асинхронный генератор для получения ответов от модели.
- `create_async_image(prompt: str, model: str, api_key: str = None, api_base: str = "https://api.deepinfra.com/v1/inference", proxy: str = None, timeout: int = 180, extra_data: dict = {}, **kwargs) -> ImageResponse`: Создает асинхронный запрос на генерацию изображения.

## Методы класса

### `get_models`

```python
@classmethod
def get_models(cls, **kwargs)
```

**Назначение**: Получает список доступных моделей из API DeepInfra.

**Параметры**:
- `cls` (DeepInfra): Ссылка на класс `DeepInfra`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `list`: Список доступных моделей.

**Как работает функция**:
- Функция проверяет, если список моделей `cls.models` уже заполнен. Если да, то функция возвращает существующий список.
- Если список моделей пуст, функция отправляет GET запрос на `https://api.deepinfra.com/models/featured`.
- Разбирает JSON ответ, чтобы заполнить списки `cls.models` и `cls.image_models` на основе поля `type` и `reported_type`.
- Расширяет `cls.models` моделями изображений.
- Возвращает `cls.models`.

**Примеры**:

```python
models = DeepInfra.get_models()
print(models)
```

### `get_image_models`

```python
@classmethod
def get_image_models(cls, **kwargs)
```

**Назначение**: Получает список доступных моделей для генерации изображений.

**Параметры**:
- `cls` (DeepInfra): Ссылка на класс `DeepInfra`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `list`: Список доступных моделей для генерации изображений.

**Как работает функция**:
- Функция проверяет, если список моделей изображений `cls.image_models` уже заполнен. Если нет, вызывает `cls.get_models()` для заполнения.
- Возвращает `cls.image_models`.

**Примеры**:

```python
image_models = DeepInfra.get_image_models()
print(image_models)
```

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    stream: bool,
    prompt: str = None,
    temperature: float = 0.7,
    max_tokens: int = 1028,
    **kwargs
) -> AsyncResult
```

**Назначение**: Создает асинхронный генератор для получения ответов от модели.

**Параметры**:
- `cls` (DeepInfra): Ссылка на класс `DeepInfra`.
- `model` (str): Название модели.
- `messages` (Messages): Список сообщений для отправки в модель.
- `stream` (bool): Флаг, указывающий на использование потоковой передачи.
- `prompt` (str, optional): Промпт для генерации изображения. По умолчанию `None`.
- `temperature` (float, optional): Температура для генерации текста. По умолчанию `0.7`.
- `max_tokens` (int, optional): Максимальное количество токенов в ответе. По умолчанию `1028`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор для получения ответов от модели.

**Как работает функция**:
- Функция сначала проверяет, является ли указанная модель моделью для генерации изображений, используя `cls.get_image_models()`.
- Если это модель для генерации изображений, функция вызывает `cls.create_async_image()` для создания изображения и возвращает результат как генератор.
- Если это модель для генерации текста, функция устанавливает заголовки HTTP запроса, необходимые для взаимодействия с API DeepInfra.
- Затем, функция вызывает метод `create_async_generator` из родительского класса `OpenaiTemplate` с переданными параметрами и заголовками.
- Возвращает асинхронный генератор, который выдает чанки данных из ответа API DeepInfra.

**Примеры**:

```python
async def main():
    messages = [{"role": "user", "content": "Hello, world!"}]
    async for chunk in DeepInfra.create_async_generator(model="meta-llama/Meta-Llama-3.1-70B-Instruct", messages=messages, stream=True):
        print(chunk)

import asyncio
asyncio.run(main())
```

### `create_async_image`

```python
@classmethod
async def create_async_image(
    cls,
    prompt: str,
    model: str,
    api_key: str = None,
    api_base: str = "https://api.deepinfra.com/v1/inference",
    proxy: str = None,
    timeout: int = 180,
    extra_data: dict = {},
    **kwargs
) -> ImageResponse
```

**Назначение**: Создает асинхронный запрос на генерацию изображения.

**Параметры**:
- `cls` (DeepInfra): Ссылка на класс `DeepInfra`.
- `prompt` (str): Промпт для генерации изображения.
- `model` (str): Название модели.
- `api_key` (str, optional): API ключ для аутентификации. По умолчанию `None`.
- `api_base` (str, optional): Базовый URL для API запросов. По умолчанию `"https://api.deepinfra.com/v1/inference"`.
- `proxy` (str, optional): Прокси сервер. По умолчанию `None`.
- `timeout` (int, optional): Время ожидания ответа. По умолчанию `180`.
- `extra_data` (dict, optional): Дополнительные данные для отправки в запросе. По умолчанию `{}`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `ImageResponse`: Объект, содержащий сгенерированное изображение.

**Вызывает исключения**:
- `RuntimeError`: Если ответ от API не содержит изображений.

**Как работает функция**:
- Функция устанавливает заголовки HTTP запроса, необходимые для взаимодействия с API DeepInfra.
- Если предоставлен `api_key`, он добавляется в заголовок `Authorization`.
- Используется `StreamSession` для отправки асинхронного POST запроса к API DeepInfra.
- Формирует данные запроса, включая `prompt` и `extra_data`.
- Если модель совпадает с `cls.default_model`, данные оборачиваются в словарь `{"input": data}`.
- Отправляет запрос на `f"{api_base.rstrip('/')}/{model}"`.
- Обрабатывает ответ, извлекая URL изображения из JSON ответа.
- Если изображения не найдены, вызывается исключение `RuntimeError`.
- Возвращает объект `ImageResponse` с URL изображения и промптом.

**Примеры**:

```python
async def main():
    image = await DeepInfra.create_async_image(prompt="A cat", model="stabilityai/sd3.5", api_key="YOUR_API_KEY")
    print(image.image_url)

import asyncio
asyncio.run(main())
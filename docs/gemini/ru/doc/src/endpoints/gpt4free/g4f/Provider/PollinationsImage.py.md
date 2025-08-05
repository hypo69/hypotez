# Модуль `PollinationsImage`

## Обзор

Модуль `PollinationsImage` предоставляет класс `PollinationsImage`, который наследует от `PollinationsAI`. 
Он позволяет использовать API `Pollinations` для генерации изображений с помощью моделей, поддерживающих генерацию 
изображений.

## Классы

### `class PollinationsImage`

**Описание**: 
Класс `PollinationsImage` реализует функциональность для генерации изображений с помощью API `Pollinations`.
Он предоставляет методы для обработки запросов к API, создания асинхронных генераторов для получения 
результатов генерации и другие вспомогательные функции.

**Наследует**:
- `PollinationsAI`

**Атрибуты**:

- `label (str)`:  Идентификатор класса, по умолчанию - `"PollinationsImage"`.
- `default_model (str)`:  Название модели по умолчанию для генерации изображений, по умолчанию - `"flux"`.
- `default_vision_model (None)`:  Название модели для обработки видеоряда, по умолчанию - `None`.
- `default_image_model (str)`:  Название модели по умолчанию для генерации изображений, по умолчанию - `"flux"`.
- `image_models (list[str])`:  Список моделей, поддерживающих генерацию изображений.
- `_models_loaded (bool)`:  Флаг, указывающий, загружены ли модели, по умолчанию - `False`.

**Методы**:

- `get_models(cls, **kwargs)`: Статический метод, который возвращает список моделей, поддерживающих генерацию изображений.
    - **Параметры**: 
        - `**kwargs`:  Дополнительные аргументы, которые могут быть переданы в метод.
    - **Возвращает**:
        - `list[str]`: Список моделей.
- `create_async_generator(cls, model: str, messages: Messages, proxy: str = None, prompt: str = None, aspect_ratio: str = "1:1", width: int = None, height: int = None, seed: Optional[int] = None, cache: bool = False, nologo: bool = True, private: bool = False, enhance: bool = False, safe: bool = False, n: int = 4, **kwargs) -> AsyncResult`:  
    - **Описание**:  Асинхронный генератор для генерации изображений.
    - **Параметры**: 
        - `model (str)`:  Название модели для генерации.
        - `messages (Messages)`:  Список сообщений, которые используются для генерации.
        - `proxy (str, optional)`:  Прокси-сервер, который будет использоваться для доступа к API.
        - `prompt (str, optional)`:  Текст запроса для генерации изображения.
        - `aspect_ratio (str, optional)`:  Соотношение сторон генерируемого изображения.
        - `width (int, optional)`:  Ширина генерируемого изображения.
        - `height (int, optional)`:  Высота генерируемого изображения.
        - `seed (int, optional)`:  Случайное число, которое используется для генерации.
        - `cache (bool, optional)`:  Флаг, указывающий, нужно ли кэшировать результат генерации.
        - `nologo (bool, optional)`:  Флаг, указывающий, нужно ли включать логотип `Pollinations` на генерируемом изображении.
        - `private (bool, optional)`:  Флаг, указывающий, является ли генерация приватной.
        - `enhance (bool, optional)`:  Флаг, указывающий, нужно ли улучшать качество изображения.
        - `safe (bool, optional)`:  Флаг, указывающий, нужно ли использовать безопасный режим генерации.
        - `n (int, optional)`:  Количество генерируемых изображений.
        - `**kwargs`:  Дополнительные аргументы, которые могут быть переданы в метод.
    - **Возвращает**: 
        - `AsyncResult`:  Объект `AsyncResult`, который представляет результат генерации.

**Внутренние функции**:

- `_generate_image(cls, model: str, prompt: str, proxy: str = None, aspect_ratio: str = "1:1", width: int = None, height: int = None, seed: Optional[int] = None, cache: bool = False, nologo: bool = True, private: bool = False, enhance: bool = False, safe: bool = False, n: int = 4, **kwargs) -> AsyncResult`:  
    - **Описание**:  Асинхронный генератор, который отправляет запросы к API `Pollinations` и возвращает результаты генерации.
    - **Параметры**: 
        - `model (str)`:  Название модели для генерации.
        - `prompt (str)`:  Текст запроса для генерации изображения.
        - `proxy (str, optional)`:  Прокси-сервер, который будет использоваться для доступа к API.
        - `aspect_ratio (str, optional)`:  Соотношение сторон генерируемого изображения.
        - `width (int, optional)`:  Ширина генерируемого изображения.
        - `height (int, optional)`:  Высота генерируемого изображения.
        - `seed (int, optional)`:  Случайное число, которое используется для генерации.
        - `cache (bool, optional)`:  Флаг, указывающий, нужно ли кэшировать результат генерации.
        - `nologo (bool, optional)`:  Флаг, указывающий, нужно ли включать логотип `Pollinations` на генерируемом изображении.
        - `private (bool, optional)`:  Флаг, указывающий, является ли генерация приватной.
        - `enhance (bool, optional)`:  Флаг, указывающий, нужно ли улучшать качество изображения.
        - `safe (bool, optional)`:  Флаг, указывающий, нужно ли использовать безопасный режим генерации.
        - `n (int, optional)`:  Количество генерируемых изображений.
        - `**kwargs`:  Дополнительные аргументы, которые могут быть переданы в метод.
    - **Возвращает**: 
        - `AsyncResult`:  Объект `AsyncResult`, который представляет результат генерации.

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.PollinationsImage import PollinationsImage
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создание инстанса класса PollinationsImage
image_generator = PollinationsImage()

# Список сообщений для генерации
messages = Messages([
    {"role": "user", "content": "Generate an image of a cat playing piano."},
])

# Генерация изображения
async for chunk in image_generator.create_async_generator(
    model="stable-diffusion",
    messages=messages,
    n=1
):
    print(chunk)

```

## Параметры класса

- `label (str)`:  Идентификатор класса.
- `default_model (str)`:  Название модели по умолчанию для генерации изображений.
- `default_vision_model (None)`:  Название модели для обработки видеоряда.
- `default_image_model (str)`:  Название модели по умолчанию для генерации изображений.
- `image_models (list[str])`:  Список моделей, поддерживающих генерацию изображений.
- `_models_loaded (bool)`:  Флаг, указывающий, загружены ли модели.

## Как работает класс

Класс `PollinationsImage` обеспечивает взаимодействие с API `Pollinations` для генерации изображений.
 Он наследует от базового класса `PollinationsAI`, предоставляя доступ к общим методам API, 
 а также предоставляет собственные методы, специфичные для генерации изображений.

**Метод `get_models`** отвечает за определение доступных моделей для генерации изображений.
Он загружает список моделей из базы данных, а затем дополняет его моделями, доступными через API `Pollinations`.

**Метод `create_async_generator`** позволяет получить асинхронный генератор, который выдает 
результаты генерации изображений. Он принимает различные параметры, определяющие модель для генерации, 
текст запроса, соотношение сторон, размер изображения, seed и другие настройки. 

**Внутренняя функция `_generate_image`** отправляет запросы к API `Pollinations` для генерации 
изображений. Она использует предоставленные параметры для определения настроек генерации 
и возвращает результаты в виде асинхронного генератора, который выдает изображения по частям.

## Примеры

**Пример 1**:  Генерация изображения с помощью `PollinationsImage`

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.PollinationsImage import PollinationsImage
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создание инстанса класса PollinationsImage
image_generator = PollinationsImage()

# Список сообщений для генерации
messages = Messages([
    {"role": "user", "content": "Generate an image of a cat playing piano."},
])

# Генерация изображения
async for chunk in image_generator.create_async_generator(
    model="stable-diffusion",
    messages=messages,
    n=1
):
    print(chunk)

```
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.PollinationsImage import PollinationsImage
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создание инстанса класса PollinationsImage
image_generator = PollinationsImage()

# Список сообщений для генерации
messages = Messages([
    {"role": "user", "content": "Generate an image of a cat playing piano."},
])

# Генерация изображения
async for chunk in image_generator.create_async_generator(
    model="stable-diffusion",
    messages=messages,
    n=1
):
    print(chunk)

```
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.PollinationsImage import PollinationsImage
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создание инстанса класса PollinationsImage
image_generator = PollinationsImage()

# Список сообщений для генерации
messages = Messages([
    {"role": "user", "content": "Generate an image of a cat playing piano."},
])

# Генерация изображения
async for chunk in image_generator.create_async_generator(
    model="stable-diffusion",
    messages=messages,
    n=1
):
    print(chunk)

```
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.PollinationsImage import PollinationsImage
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создание инстанса класса PollinationsImage
image_generator = PollinationsImage()

# Список сообщений для генерации
messages = Messages([
    {"role": "user", "content": "Generate an image of a cat playing piano."},
])

# Генерация изображения
async for chunk in image_generator.create_async_generator(
    model="stable-diffusion",
    messages=messages,
    n=1
):
    print(chunk)

```
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.PollinationsImage import PollinationsImage
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создание инстанса класса PollinationsImage
image_generator = PollinationsImage()

# Список сообщений для генерации
messages = Messages([
    {"role": "user", "content": "Generate an image of a cat playing piano."},
])

# Генерация изображения
async for chunk in image_generator.create_async_generator(
    model="stable-diffusion",
    messages=messages,
    n=1
):
    print(chunk)

```

## Дополнительно

- Модуль `PollinationsImage` предоставляет  **гибкость** в использовании различных моделей для генерации изображений.
- Он также позволяет настраивать параметры генерации, такие как размер изображения, соотношение сторон, seed и другие.
- Класс  `PollinationsImage`  позволяет  **генерировать изображения с помощью моделей**  `stable-diffusion`,  `dalle2`,  `flux`  и других.
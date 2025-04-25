# PollinationsAI.py

## Обзор

Этот модуль предоставляет класс `PollinationsAI`, который реализует провайдера для генерации текста и изображений с помощью сервиса Pollinations.ai. 

## Подробности

Данный класс предоставляет возможности для взаимодействия с различными моделями, доступными на Pollinations.ai,  включая текстовые модели (например, GPT-4, Gemini) и модели для генерации изображений (например, Stable Diffusion). Он также включает в себя функции для обработки сообщений,  обработки мультимедийных данных, а также загрузки и кэширования моделей.

## Классы

### `class PollinationsAI`

**Описание**:  Класс, реализующий провайдера для Pollinations.ai, поддерживающий генерацию текста и изображений.

**Наследует**:
    - `AsyncGeneratorProvider`: Базовый класс для асинхронных генераторов ответов.
    - `ProviderModelMixin`: Миксин для управления моделями и их метаданными.


**Атрибуты**:
    - `label (str)`: Название провайдера ("Pollinations AI").
    - `url (str)`: Базовый URL сервиса Pollinations.ai.
    - `working (bool)`: Флаг, указывающий, доступен ли провайдер для использования.
    - `supports_system_message (bool)`: Флаг, указывающий, поддерживает ли провайдер системные сообщения.
    - `supports_message_history (bool)`: Флаг, указывающий, поддерживает ли провайдер историю сообщений.
    - `text_api_endpoint (str)`: URL API-пункта для генерации текста.
    - `openai_endpoint (str)`: URL API-пункта для взаимодействия с OpenAI.
    - `image_api_endpoint (str)`: URL API-пункта для генерации изображений.
    - `default_model (str)`: Название модели по умолчанию для генерации текста.
    - `default_image_model (str)`: Название модели по умолчанию для генерации изображений.
    - `default_vision_model (str)`: Название модели по умолчанию для визуальных задач.
    - `text_models (list[str])`: Список текстовых моделей, поддерживаемых провайдером.
    - `image_models (list[str])`: Список моделей для генерации изображений, поддерживаемых провайдером.
    - `extra_image_models (list[str])`: Дополнительные модели для генерации изображений.
    - `vision_models (list[str])`: Список моделей для визуальных задач.
    - `extra_text_models (list[str])`: Дополнительные текстовые модели.
    - `_models_loaded (bool)`: Флаг, указывающий, загружены ли модели.
    - `model_aliases (dict[str, str])`: Словарь алиасов моделей для сопоставления имен.


**Методы**:

    - `get_models(cls, **kwargs) -> list[str]`: Получает список доступных моделей, обновляя списки `text_models` и `image_models`.
    - `create_async_generator(cls, model: str, messages: Messages, stream: bool = True, proxy: str = None, cache: bool = False, **kwargs) -> AsyncResult`:  Создает асинхронный генератор для генерации текста или изображений.
    - `_generate_image(cls, model: str, prompt: str, proxy: str, aspect_ratio: str, width: int, height: int, seed: Optional[int], cache: bool, nologo: bool, private: bool, enhance: bool, safe: bool, n: int) -> AsyncResult`:  Генерирует изображения с использованием указанной модели.
    - `_generate_text(cls, model: str, messages: Messages, media: MediaListType, proxy: str, temperature: float, presence_penalty: float, top_p: float, frequency_penalty: float, response_format: Optional[dict], seed: Optional[int], cache: bool, stream: bool, extra_parameters: list[str], **kwargs) -> AsyncResult`:  Генерирует текст с использованием указанной модели.


**Принцип работы**:
    Класс `PollinationsAI` реализует два основных метода: `_generate_text` и `_generate_image`, которые отвечают за  генерацию текста и изображений, соответственно.  Он использует API Pollinations.ai  для отправки запросов и получения ответов от моделей. 
    
    Класс также включает в себя методы для обработки сообщений (`render_messages`), загрузки и кэширования моделей (`get_models`).

## Методы класса

### `get_models`

**Назначение**: Получает список доступных моделей от Pollinations.ai и обновляет списки `text_models` и `image_models`.

**Параметры**:
    - `**kwargs`:  Дополнительные аргументы.


**Возвращает**:
    - `list[str]`: Список всех доступных моделей.


**Как работает**:
    - Метод `get_models`  использует  `requests.get`  для получения данных от API  Pollinations.ai для  текстовых  и  изображений.
    - Полученные списки моделей используются для обновления `text_models`  и  `image_models`. 


### `create_async_generator`

**Назначение**: Создает асинхронный генератор для генерации текста или изображений с использованием указанной модели и параметров.


**Параметры**:
    - `model (str)`: Название модели.
    - `messages (Messages)`: Список сообщений.
    - `stream (bool)`: Флаг, указывающий, нужно ли использовать потоковую передачу.
    - `proxy (str)`:  Прокси-сервер, который нужно использовать для запросов.
    - `cache (bool)`: Флаг, указывающий, нужно ли кэшировать результаты.
    - `prompt (str)`:  Подсказка для модели.
    - `aspect_ratio (str)`: Соотношение сторон изображения.
    - `width (int)`: Ширина изображения.
    - `height (int)`: Высота изображения.
    - `seed (Optional[int])`:  Случайное число, которое нужно использовать для генерации.
    - `nologo (bool)`: Флаг, указывающий, нужно ли удалять логотип Pollinations.ai с изображения.
    - `private (bool)`: Флаг, указывающий, нужно ли генерировать изображения в частном режиме.
    - `enhance (bool)`: Флаг, указывающий, нужно ли использовать улучшенное качество генерации.
    - `safe (bool)`: Флаг, указывающий, нужно ли использовать безопасный режим.
    - `n (int)`: Количество изображений для генерации.
    - `media (MediaListType)`: Список мультимедийных данных.
    - `temperature (float)`: Температура модели.
    - `presence_penalty (float)`:  Штраф за присутствие определенных слов или фраз.
    - `top_p (float)`:  Вероятность отбора наиболее вероятных слов.
    - `frequency_penalty (float)`: Штраф за частоту слов.
    - `response_format (Optional[dict])`:  Формат ответа.
    - `extra_parameters (list[str])`:  Дополнительные параметры.
    - `**kwargs`: Дополнительные аргументы.


**Возвращает**:
    - `AsyncResult`: Асинхронный генератор, который возвращает результаты генерации.

**Как работает**:
    - Метод `create_async_generator`  проверяет наличие  `model`  и выбирает подходящую модель, в том числе, используя список `audio_models`. 
    - В зависимости от типа  `model`  (текстовая или изображения) вызывает `_generate_text`  или  `_generate_image`,  передавая соответствующие параметры. 

### `_generate_image`

**Назначение**: Генерирует изображения с помощью указанной модели.


**Параметры**:
    - `model (str)`: Название модели.
    - `prompt (str)`:  Подсказка для модели.
    - `proxy (str)`:  Прокси-сервер, который нужно использовать для запросов.
    - `aspect_ratio (str)`:  Соотношение сторон изображения.
    - `width (int)`:  Ширина изображения.
    - `height (int)`:  Высота изображения.
    - `seed (Optional[int])`:  Случайное число, которое нужно использовать для генерации.
    - `cache (bool)`: Флаг, указывающий, нужно ли кэшировать результаты.
    - `nologo (bool)`: Флаг, указывающий, нужно ли удалять логотип Pollinations.ai с изображения.
    - `private (bool)`: Флаг, указывающий, нужно ли генерировать изображения в частном режиме.
    - `enhance (bool)`: Флаг, указывающий, нужно ли использовать улучшенное качество генерации.
    - `safe (bool)`: Флаг, указывающий, нужно ли использовать безопасный режим.
    - `n (int)`: Количество изображений для генерации.


**Возвращает**:
    - `AsyncResult`: Асинхронный генератор, который возвращает результаты генерации.

**Как работает**:
    - `_generate_image`  использует  `use_aspect_ratio`  для вычисления  `width`  и  `height`  в соответствии с  `aspect_ratio`.
    - Он  формирует URL  запроса к API Pollinations.ai  и отправляет  `POST`  запрос с использованием  `ClientSession`. 
    - Полученные ответы  обрабатываются и возвращаются в виде  `ImageResponse`  через  `asyncio.gather`.


### `_generate_text`

**Назначение**: Генерирует текст с помощью указанной модели.


**Параметры**:
    - `model (str)`: Название модели.
    - `messages (Messages)`: Список сообщений.
    - `media (MediaListType)`: Список мультимедийных данных.
    - `proxy (str)`:  Прокси-сервер, который нужно использовать для запросов.
    - `temperature (float)`:  Температура модели.
    - `presence_penalty (float)`:  Штраф за присутствие определенных слов или фраз.
    - `top_p (float)`:  Вероятность отбора наиболее вероятных слов.
    - `frequency_penalty (float)`:  Штраф за частоту слов.
    - `response_format (Optional[dict])`:  Формат ответа.
    - `seed (Optional[int])`:  Случайное число, которое нужно использовать для генерации.
    - `cache (bool)`: Флаг, указывающий, нужно ли кэшировать результаты.
    - `stream (bool)`: Флаг, указывающий, нужно ли использовать потоковую передачу.
    - `extra_parameters (list[str])`:  Дополнительные параметры.
    - `**kwargs`: Дополнительные аргументы.


**Возвращает**:
    - `AsyncResult`: Асинхронный генератор, который возвращает результаты генерации.

**Как работает**:
    - `_generate_text`   формирует URL  запроса к API Pollinations.ai  и отправляет  `POST`  запрос с использованием  `ClientSession`.
    - Он использует  `render_messages`  для преобразования  `messages`  и  `media`  в формат, который требуется API.
    - Он получает ответы от API  и  обрабатывает их  в соответствии с  `response_format`  и  `stream`  флагами.
    - В зависимости от типа  `model`  (текстовая или  `audio`)  он отправляет запрос к  `text_api_endpoint`  или  `openai_endpoint`.


## Параметры класса

    - `model_aliases (dict[str, str])`: Словарь алиасов моделей для сопоставления имен.  Ключом является  `alias`  модели, а значением -  `real_name`  модели.
        - `gpt-4o-mini`: "openai"
        - `gpt-4`: "openai-large"
        - `gpt-4o`: "openai-large"
        - `o3-mini`: "openai-reasoning"
        - `qwen-2.5-coder-32b`: "qwen-coder"
        - `llama-3.3-70b`: "llama"
        - `mistral-nemo`: "mistral"
        - `gpt-4o-mini`: "searchgpt"
        - `llama-3.1-8b`: "llamalight"
        - `llama-3.3-70b`: "llama-scaleway"
        - `phi-4`: "phi"
        - `gemini-2.0`: "gemini"
        - `gemini-2.0-flash`: "gemini"
        - `gemini-2.0-flash-thinking`: "gemini-thinking"
        - `deepseek-r1`: "deepseek-r1-llama"
        - `gpt-4o-audio`: "openai-audio"
        
        - `sdxl-turbo`: "turbo"


## Примеры

### Пример создания объекта и использования метода `create_async_generator`

```python
from src.endpoints.gpt4free.g4f.Provider.PollinationsAI import PollinationsAI
from src.endpoints.gpt4free.g4f.typing import Messages

# Создание объекта провайдера
provider = PollinationsAI()

# Список сообщений
messages = Messages(
    [
        {"role": "user", "content": "Привет, расскажи мне про свой любимый фильм."},
    ]
)

# Генерация текста с помощью модели 'openai'
async for chunk in provider.create_async_generator(model='openai', messages=messages):
    print(chunk)
```

### Пример генерации изображения с помощью модели 'flux'

```python
from src.endpoints.gpt4free.g4f.Provider.PollinationsAI import PollinationsAI

# Создание объекта провайдера
provider = PollinationsAI()

# Подсказка для модели
prompt = "Кошка играет на пианино"

# Генерация изображения с помощью модели 'flux'
async for chunk in provider.create_async_generator(model='flux', prompt=prompt):
    print(chunk)
```
# Модуль StabilityAI_SD35Large

## Обзор

Модуль `StabilityAI_SD35Large` предоставляет асинхронный генератор изображений, основанный на модели Stable Diffusion 3.5 Large от StabilityAI, доступной через Hugging Face Spaces.

## Подробней

Модуль `StabilityAI_SD35Large` реализует асинхронный генератор изображений, который взаимодействует с API модели Stable Diffusion 3.5 Large. 

## Классы

### `class StabilityAI_SD35Large(AsyncGeneratorProvider, ProviderModelMixin)`

**Описание**: 
Класс реализует асинхронный генератор изображений на основе модели Stable Diffusion 3.5 Large, используя API Hugging Face Spaces.

**Наследует**:
- `AsyncGeneratorProvider`:  Базовый класс для асинхронных генераторов.
- `ProviderModelMixin`:  Класс для работы с моделями и их атрибутами.

**Атрибуты**:

- `label (str)`: "StabilityAI SD-3.5-Large" - название модели.
- `url (str)`: "https://stabilityai-stable-diffusion-3-5-large.hf.space" - URL-адрес Hugging Face Spaces.
- `api_endpoint (str)`: "/gradio_api/call/infer" - конечная точка API для вызова генерации изображения.
- `working (bool)`: `True` - флаг, указывающий, что модель работает.
- `default_model (str)`: 'stabilityai-stable-diffusion-3.5-large' - имя модели по умолчанию.
- `default_image_model (str)`: `default_model` - имя модели по умолчанию для изображений.
- `model_aliases (dict)`: {"sd-3.5": `default_model`} - словарь псевдонимов для моделей.
- `image_models (list)`: список ключей из `model_aliases` - допустимые модели для изображений.
- `models (list)`: `image_models` - список моделей.

**Методы**:

- `create_async_generator()`:  Асинхронный генератор, который принимает конфигурацию и возвращает `AsyncResult` объект, представляющий результат генерации изображения.

#### `async def create_async_generator(cls, model: str, messages: Messages, prompt: str = None, negative_prompt: str = None, api_key: str = None, proxy: str = None, aspect_ratio: str = "1:1", width: int = None, height: int = None, guidance_scale: float = 4.5, num_inference_steps: int = 50, seed: int = 0, randomize_seed: bool = True, **kwargs) -> AsyncResult:`

**Назначение**: 
Асинхронный генератор изображений, который отправляет запрос на API и возвращает поток с превью и конечным результатом.

**Параметры**:

- `model (str)`: Имя модели.
- `messages (Messages)`: Сообщение, содержащее контекст для генерации.
- `prompt (str, optional)`: Текстовый запрос для генерации. По умолчанию `None`.
- `negative_prompt (str, optional)`: Текстовый запрос для исключения из результата. По умолчанию `None`.
- `api_key (str, optional)`: Ключ API для аутентификации. По умолчанию `None`.
- `proxy (str, optional)`: Прокси-сервер для соединения. По умолчанию `None`.
- `aspect_ratio (str, optional)`: Соотношение сторон изображения. По умолчанию "1:1".
- `width (int, optional)`: Ширина изображения в пикселях. По умолчанию `None`.
- `height (int, optional)`: Высота изображения в пикселях. По умолчанию `None`.
- `guidance_scale (float, optional)`: Коэффициент направляющей. По умолчанию `4.5`.
- `num_inference_steps (int, optional)`: Количество шагов для генерации. По умолчанию `50`.
- `seed (int, optional)`: Значение для генерации случайных чисел. По умолчанию `0`.
- `randomize_seed (bool, optional)`: Флаг, указывающий, нужно ли использовать случайное значение для `seed`. По умолчанию `True`.
- `kwargs (dict)`: Дополнительные аргументы для генератора.

**Возвращает**:
- `AsyncResult`: Асинхронный результат, содержащий `ImagePreview` (превью) и `ImageResponse` (конечный результат).

**Принцип работы**:

1. Форматирование запроса: 
    - `format_image_prompt()`: Форматирует `prompt` для API.
    - `use_aspect_ratio()`: Проверяет и вычисляет ширину и высоту изображения на основе `aspect_ratio`.
2. Отправка запроса на API:
    - `ClientSession()`: Открывает HTTP-сессию.
    - `post()`: Отправляет POST-запрос на API с данными `data` и заголовками `headers`.
3. Обработка ответа: 
    - `json()`:  Декодирует JSON-ответ.
    - `get(event_id)`:  Получает `event_id`  из ответа для отслеживания статуса.
4. Поток событий: 
    - `get()`:  Осуществляет GET-запрос на `/gradio_api/call/infer/<event_id>`.
    - `content`:  Итерация по данным в ответе.
    - `chunk.startswith(b"event: ")`:  Проверяет, является ли текущая часть данных событием.
    - `chunk.startswith(b"data: ")`:  Проверяет, являются ли текущие данные данными.
5. Вывод результатов:
    - `ImagePreview`: Выводит превью изображения.
    - `ImageResponse`: Выводит конечный результат изображения.

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.StabilityAI_SD35Large import StabilityAI_SD35Large
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

async def main():
    model = "stabilityai-stable-diffusion-3.5-large"
    messages = Messages(
        role='user',
        content='photo of a cat'
    )
    provider = StabilityAI_SD35Large()
    async for result in provider.create_async_generator(model=model, messages=messages):
        if isinstance(result, ImageResponse):
            print(f"Generated image URL: {result.url}")
        elif isinstance(result, ImagePreview):
            print(f"Generated image preview URL: {result.url}")
```

##  Примечания

- Модуль `StabilityAI_SD35Large` предоставляет удобный способ использования модели Stable Diffusion 3.5 Large от StabilityAI через Hugging Face Spaces. 
- Модуль обрабатывает передачу данных, аутентификацию, управление потоком событий и обработку результатов API.
- Используйте `StabilityAI_SD35Large.create_async_generator()` для запуска генерации изображения с заданными параметрами.
- Модель `StabilityAI_SD35Large` доступна по адресу `https://stabilityai-stable-diffusion-3-5-large.hf.space`.

## Дополнительные сведения

- [Hugging Face Spaces](https://huggingface.co/spaces)
- [Stable Diffusion](https://stability.ai/blog/stable-diffusion-public-release)
- [Stable Diffusion API](https://api.stability.ai/)
- [aiohttp](https://docs.aiohttp.org/en/stable/)
- [json](https://docs.python.org/3/library/json.html)
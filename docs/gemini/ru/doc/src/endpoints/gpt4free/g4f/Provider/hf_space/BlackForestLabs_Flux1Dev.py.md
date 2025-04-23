# Модуль `BlackForestLabs_Flux1Dev`

## Обзор

Модуль `BlackForestLabs_Flux1Dev` предоставляет интерфейс для взаимодействия с моделью генерации изображений Flux-1-Dev от Black Forest Labs через Hugging Face Space. Он позволяет генерировать изображения на основе текстовых запросов, используя асинхронные генераторы для обработки данных в реальном времени.

## Подробнее

Этот модуль является частью проекта `hypotez` и предназначен для интеграции с другими компонентами, такими как веб-интерфейсы или API, для предоставления функциональности генерации изображений. Он использует HTTP-запросы к Hugging Face Space для взаимодействия с моделью Flux-1-Dev и обрабатывает ответы в формате JSON для извлечения сгенерированных изображений и информации о процессе генерации.

## Классы

### `BlackForestLabs_Flux1Dev`

**Описание**: Класс `BlackForestLabs_Flux1Dev` предоставляет методы для асинхронной генерации изображений с использованием модели Flux-1-Dev от Black Forest Labs.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера ("BlackForestLabs Flux-1-Dev").
- `url` (str): URL Hugging Face Space, где размещена модель.
- `space` (str): Название Hugging Face Space.
- `referer` (str): Referer для HTTP-запросов.
- `working` (bool): Указывает, что провайдер работает.
- `default_model` (str): Модель по умолчанию ('black-forest-labs-flux-1-dev').
- `default_image_model` (str): Модель изображения по умолчанию (совпадает с `default_model`).
- `model_aliases` (dict): Псевдонимы моделей.
- `image_models` (list): Список моделей изображений.
- `models` (list): Список моделей.

**Методы**:
- `run(method: str, session: StreamSession, conversation: JsonConversation, data: list = None)`: Выполняет HTTP-запрос к Hugging Face Space.
- `create_async_generator(...)`: Создает асинхронный генератор для генерации изображений.

## Методы класса

### `run`

```python
@classmethod
def run(cls, method: str, session: StreamSession, conversation: JsonConversation, data: list = None):
    """Выполняет HTTP-запрос к Hugging Face Space.

    Args:
        method (str): HTTP-метод ("post" или "get").
        session (StreamSession): Асинхровая сессия для выполнения HTTP-запросов.
        conversation (JsonConversation): Объект, содержащий информацию о сессии.
        data (list, optional): Данные для отправки в запросе. По умолчанию `None`.

    Returns:
        AsyncResult: Асинхронный результат выполнения запроса.
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
    prompt: str = None,
    proxy: str = None,
    aspect_ratio: str = "1:1",
    width: int = None,
    height: int = None,
    guidance_scale: float = 3.5,
    num_inference_steps: int = 28,
    seed: int = 0,
    randomize_seed: bool = True,
    cookies: dict = None,
    api_key: str = None,
    zerogpu_uuid: str = "[object Object]",
    **kwargs
) -> AsyncResult:
    """Создает асинхронный генератор для генерации изображений.

    Args:
        model (str): Название модели.
        messages (Messages): Список сообщений для формирования запроса.
        prompt (str, optional): Текстовый запрос. По умолчанию `None`.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
        aspect_ratio (str, optional): Соотношение сторон изображения. По умолчанию "1:1".
        width (int, optional): Ширина изображения. По умолчанию `None`.
        height (int, optional): Высота изображения. По умолчанию `None`.
        guidance_scale (float, optional): Масштаб соответствия запросу. По умолчанию 3.5.
        num_inference_steps (int, optional): Количество шагов генерации. По умолчанию 28.
        seed (int, optional): Зерно для генерации случайных чисел. По умолчанию 0.
        randomize_seed (bool, optional): Флаг рандомизации зерна. По умолчанию `True`.
        cookies (dict, optional): Cookie для HTTP-запросов. По умолчанию `None`.
        api_key (str, optional): API-ключ. По умолчанию `None`.
        zerogpu_uuid (str, optional): UUID для ZeroGPU. По умолчанию "[object Object]".
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий результаты генерации изображений.

    Raises:
        RuntimeError: Если не удается обработать сообщение от сервера.
        ResponseError: Если сервер возвращает ошибку.
    """
    ...
```

## Параметры класса

- `label` (str): Метка провайдера ("BlackForestLabs Flux-1-Dev").
- `url` (str): URL Hugging Face Space, где размещена модель.
- `space` (str): Название Hugging Face Space.
- `referer` (str): Referer для HTTP-запросов.
- `working` (bool): Указывает, что провайдер работает.
- `default_model` (str): Модель по умолчанию ('black-forest-labs-flux-1-dev').
- `default_image_model` (str): Модель изображения по умолчанию (совпадает с `default_model`).
- `model_aliases` (dict): Псевдонимы моделей.
- `image_models` (list): Список моделей изображений.
- `models` (list): Список моделей.

## Примеры

```python
# Пример использования create_async_generator
import asyncio
from src.requests import StreamSession  #  Предположим, что StreamSession определен в src.requests
from src.providers.response import JsonConversation  #  Предположим, что JsonConversation определен в src.providers.response

async def main():
    model = "black-forest-labs-flux-1-dev"
    messages = [{"role": "user", "content": "Generate an image of a cat"}]
    async for result in BlackForestLabs_Flux1Dev.create_async_generator(model=model, messages=messages):
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
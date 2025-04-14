# Модуль BlackForestLabs_Flux1Dev
## Обзор

Модуль `BlackForestLabs_Flux1Dev` предоставляет асинхронный генератор для создания изображений с использованием модели BlackForestLabs Flux-1-Dev. Он взаимодействует с API Black Forest Labs через HTTP-запросы, отправляет запросы на генерацию изображений и возвращает результаты в виде последовательности обновлений статуса, превью изображений и финальных изображений.

## Подробнее

Модуль использует `StreamSession` для асинхронных HTTP-запросов и предоставляет методы для отправки запросов к API Black Forest Labs. Он также обрабатывает ответы, извлекая информацию о статусе, превью изображений и финальные изображения.

## Классы

### `BlackForestLabs_Flux1Dev`

**Описание**: Класс `BlackForestLabs_Flux1Dev` является асинхронным генератором изображений, использующим модель BlackForestLabs Flux-1-Dev. Он наследует функциональность от `AsyncGeneratorProvider` и `ProviderModelMixin`.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую структуру для асинхронных генераторов.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями провайдера.

**Атрибуты**:
- `label` (str): Метка провайдера (BlackForestLabs Flux-1-Dev).
- `url` (str): URL API Black Forest Labs.
- `space` (str): Имя space Black Forest Labs.
- `referer` (str): Referer для HTTP-запросов.
- `working` (bool): Указывает, работает ли провайдер.
- `default_model` (str): Модель, используемая по умолчанию ('black-forest-labs-flux-1-dev').
- `default_image_model` (str): Модель изображения, используемая по умолчанию.
- `model_aliases` (dict): Псевдонимы моделей.
- `image_models` (list): Список моделей изображений.
- `models` (list): Список моделей.

**Методы**:
- `run()`: Выполняет HTTP-запрос к API Black Forest Labs.
- `create_async_generator()`: Создает асинхронный генератор для генерации изображений.

## Методы класса

### `run`

```python
@classmethod
def run(cls, method: str, session: StreamSession, conversation: JsonConversation, data: list = None) -> None:
    """Выполняет HTTP-запрос к API Black Forest Labs.

    Args:
        cls (BlackForestLabs_Flux1Dev): Ссылка на класс.
        method (str): HTTP-метод ("post" или "get").
        session (StreamSession): Асинхровая HTTP-сессия.
        conversation (JsonConversation): Объект JsonConversation, содержащий информацию о сессии.
        data (list, optional): Данные для отправки в запросе (только для "post"). По умолчанию `None`.

    Returns:
        Awaitable: Асинхронный объект ответа.
    """
    ...
```
**Как работает функция**:
Функция `run` выполняет HTTP-запрос к API Black Forest Labs в зависимости от указанного метода (`post` или `get`). Она использует предоставленную сессию (`StreamSession`) и объект `JsonConversation` для установки необходимых заголовков и параметров запроса. Если метод `post`, функция отправляет данные в формате JSON. Если метод `get`, функция отправляет запрос на получение данных о сессии.

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
        cls (BlackForestLabs_Flux1Dev): Ссылка на класс.
        model (str): Модель для генерации изображений.
        messages (Messages): Список сообщений.
        prompt (str, optional): Текст запроса. По умолчанию `None`.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        aspect_ratio (str, optional): Соотношение сторон изображения. По умолчанию "1:1".
        width (int, optional): Ширина изображения. По умолчанию `None`.
        height (int, optional): Высота изображения. По умолчанию `None`.
        guidance_scale (float, optional): Масштаб соответствия запросу. По умолчанию 3.5.
        num_inference_steps (int, optional): Количество шагов для генерации. По умолчанию 28.
        seed (int, optional): Зерно для генерации. По умолчанию 0.
        randomize_seed (bool, optional): Флаг для рандомизации зерна. По умолчанию `True`.
        cookies (dict, optional): Куки для HTTP-запросов. По умолчанию `None`.
        api_key (str, optional): API ключ. По умолчанию `None`.
        zerogpu_uuid (str, optional): UUID для ZeroGPU. По умолчанию "[object Object]".
        **kwargs: Дополнительные параметры.

    Yields:
        AsyncResult: Обновления статуса, превью изображений и финальные изображения.

    Raises:
        RuntimeError: Если не удалось разобрать сообщение от API.
        ResponseError: Если API вернул ошибку.
    """
    ...
```

**Как работает функция**:

1.  **Инициализация**:
    *   Функция принимает различные параметры, включая модель, сообщения, прокси, соотношение сторон, размеры изображения, параметры генерации и учетные данные.

2.  **Подготовка данных**:
    *   Форматирует текст запроса с использованием `format_image_prompt`.
    *   Вычисляет размеры изображения на основе соотношения сторон с использованием `use_aspect_ratio`.
    *   Создает список `data` с параметрами запроса.
    *   Инициализирует объект `JsonConversation` для хранения информации о сессии.
    *   Если `zerogpu_token` не предоставлен, получает его с использованием `get_zerogpu_token`.

3.  **Выполнение запросов**:
    *   Отправляет POST-запрос к API для присоединения к очереди с использованием `cls.run` и проверяет успешность запроса.
    *   Отправляет GET-запрос для получения данных о событии и обрабатывает ответы в цикле.
    *   Для каждого чанка данных, полученного от API, пытается извлечь информацию о статусе, превью изображения или финальном изображении.

4.  **Обработка ответов**:

    *   Если сообщение имеет тип `'log'`, извлекает статус из поля `"log"` и передает его как `Reasoning`.
    *   Если сообщение имеет тип `'progress'`, извлекает информацию о прогрессе и передает ее как `Reasoning`.
    *   Если сообщение имеет тип `'process_generating'`, извлекает URL превью изображения и передает его как `ImagePreview`.
    *   Если сообщение имеет тип `'process_completed'`, извлекает URL финального изображения и передает его как `ImageResponse`.
    *   Обрабатывает ошибки, возникающие при разборе JSON или при наличии ошибок в ответе API.

**Примеры**:

```python
# Пример вызова функции create_async_generator
import asyncio
from typing import AsyncGenerator, Optional, List, Dict

from src.providers.response import AsyncResult, Messages
from src.requests import StreamSession
from src.providers.helper import JsonConversation

async def main():
    model = "black-forest-labs-flux-1-dev"
    messages: Messages = [{"role": "user", "content": "A cat"}]
    prompt = "A cat"
    proxy = None
    aspect_ratio = "1:1"
    width = 512
    height = 512
    guidance_scale = 3.5
    num_inference_steps = 28
    seed = 0
    randomize_seed = True
    cookies: Optional[Dict[str, str]] = None
    api_key = None
    zerogpu_uuid = "[object Object]"

    generator: AsyncGenerator = BlackForestLabs_Flux1Dev.create_async_generator(
        model=model,
        messages=messages,
        prompt=prompt,
        proxy=proxy,
        aspect_ratio=aspect_ratio,
        width=width,
        height=height,
        guidance_scale=guidance_scale,
        num_inference_steps=num_inference_steps,
        seed=seed,
        randomize_seed=randomize_seed,
        cookies=cookies,
        api_key=api_key,
        zerogpu_uuid=zerogpu_uuid
    )

    async for item in generator:
        print(item)

if __name__ == "__main__":
    asyncio.run(main())

```
## Параметры класса

- `label` (str): Метка провайдера (BlackForestLabs Flux-1-Dev).
- `url` (str): URL API Black Forest Labs.
- `space` (str): Имя space Black Forest Labs.
- `referer` (str): Referer для HTTP-запросов.
- `working` (bool): Указывает, работает ли провайдер.
- `default_model` (str): Модель, используемая по умолчанию ('black-forest-labs-flux-1-dev').
- `default_image_model` (str): Модель изображения, используемая по умолчанию.
- `model_aliases` (dict): Псевдонимы моделей.
- `image_models` (list): Список моделей изображений.
- `models` (list): Список моделей.
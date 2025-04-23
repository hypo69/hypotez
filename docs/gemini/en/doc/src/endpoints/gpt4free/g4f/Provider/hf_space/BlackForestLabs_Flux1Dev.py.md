# Module BlackForestLabs_Flux1Dev

## Overview

Модуль предоставляет класс `BlackForestLabs_Flux1Dev` для взаимодействия с моделью BlackForestLabs Flux-1-Dev через API Hugging Face Space.
Он поддерживает генерацию изображений на основе текстовых запросов.

## More details

Этот модуль позволяет генерировать изображения, используя модель BlackForestLabs Flux-1-Dev, размещенную на Hugging Face Space.
Он включает в себя функции для установки соединения, отправки запросов и обработки ответов для получения сгенерированных изображений.
Модуль обрабатывает как промежуточные результаты (просмотры изображений и статусы генерации), так и окончательные результаты (URL-адреса изображений).

## Classes

### `BlackForestLabs_Flux1Dev`

**Description**:
Класс для взаимодействия с моделью BlackForestLabs Flux-1-Dev для генерации изображений.

**Inherits**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Добавляет функциональность для работы с моделями провайдера.

**Attributes**:
- `label` (str): Название провайдера ("BlackForestLabs Flux-1-Dev").
- `url` (str): URL Hugging Face Space ("https://black-forest-labs-flux-1-dev.hf.space").
- `space` (str): Имя Space на Hugging Face ("black-forest-labs/FLUX.1-dev").
- `referer` (str): Referer URL для запросов.
- `working` (bool): Указывает, что провайдер работает (True).
- `default_model` (str): Модель, используемая по умолчанию ('black-forest-labs-flux-1-dev').
- `default_image_model` (str): Модель изображения, используемая по умолчанию (совпадает с `default_model`).
- `model_aliases` (dict): Псевдонимы моделей для удобства использования.
- `image_models` (list): Список моделей изображений.
- `models` (list): Список всех поддерживаемых моделей (в данном случае, моделей изображений).

**Methods**:
- `run`: Выполняет HTTP-запрос к API Hugging Face Space.
- `create_async_generator`: Асинхронно генерирует изображения на основе текстового запроса.

## Class Methods

### `run`

```python
@classmethod
def run(cls, method: str, session: StreamSession, conversation: JsonConversation, data: list = None):
    """Выполняет HTTP-запрос к API Hugging Face Space.

    Args:
        cls (type): Класс `BlackForestLabs_Flux1Dev`.
        method (str): HTTP-метод ("post" или "get").
        session (StreamSession): Асинхровая сессия для выполнения запросов.
        conversation (JsonConversation): Объект, содержащий данные для conversation (токен, UUID, hash сессии).
        data (list, optional): Данные для отправки в запросе (для метода "post"). По умолчанию `None`.

    Returns:
        aiohttp.ClientResponse: Объект ответа от API.

    Raises:
        ResponseError: Если возникает ошибка при выполнении запроса.

    How the function works:
    - Формирует заголовки запроса, включая токен и UUID.
    - Если метод "post", отправляет POST-запрос с данными.
    - Если метод "get", отправляет GET-запрос для получения данных о событии.
    - Возвращает объект ответа от API.
    """
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
    """Асинхронно генерирует изображения на основе текстового запроса.

    Args:
        cls (type): Класс `BlackForestLabs_Flux1Dev`.
        model (str): Название модели для генерации изображений.
        messages (Messages): Список сообщений для формирования запроса.
        prompt (str, optional): Текст запроса. По умолчанию `None`.
        proxy (str, optional): Proxy server URL. Defaults to `None`.
        aspect_ratio (str, optional): Соотношение сторон изображения. По умолчанию "1:1".
        width (int, optional): Ширина изображения. По умолчанию `None`.
        height (int, optional): Высота изображения. По умолчанию `None`.
        guidance_scale (float, optional): Масштаб соответствия запросу. По умолчанию 3.5.
        num_inference_steps (int, optional): Количество шагов для генерации изображения. По умолчанию 28.
        seed (int, optional): Зерно для генерации случайных чисел. По умолчанию 0.
        randomize_seed (bool, optional): Флаг для рандомизации зерна. По умолчанию `True`.
        cookies (dict, optional): Cookies для отправки в запросе. По умолчанию `None`.
        api_key (str, optional): API key для доступа к сервису. По умолчанию `None`.
        zerogpu_uuid (str, optional): UUID для zerogpu. По умолчанию "[object Object]".
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий промежуточные и конечные результаты генерации изображений.

    Raises:
        RuntimeError: Если не удается распарсить сообщение от API.
        ResponseError: Если API возвращает ошибку.

   How the function works:
    - Инициализирует асинхровую сессию и формирует запрос на основе входных параметров.
    - Получает токен zerogpu, если он не был предоставлен.
    - Отправляет POST-запрос для запуска генерации.
    - Отправляет GET-запрос для получения данных о событии в режиме реального времени.
    - Обрабатывает чанки данных, извлекая сообщения о прогрессе, предварительные просмотры изображений и окончательные URL-адреса изображений.
    - Возвращает результаты через асинхронный генератор.
    """
```

## Class Parameters

- `label` (str): Название провайдера.
- `url` (str): URL Hugging Face Space.
- `space` (str): Имя Space на Hugging Face.
- `referer` (str): Referer URL для запросов.
- `working` (bool): Указывает, что провайдер работает.
- `default_model` (str): Модель, используемая по умолчанию.
- `default_image_model` (str): Модель изображения, используемая по умолчанию.
- `model_aliases` (dict): Псевдонимы моделей.
- `image_models` (list): Список моделей изображений.
- `models` (list): Список всех поддерживаемых моделей.

## Examples

Пример использования класса `BlackForestLabs_Flux1Dev` для создания изображения:

```python
from src.endpoints.gpt4free.g4f.Provider.hf_space.BlackForestLabs_Flux1Dev import BlackForestLabs_Flux1Dev
from src.requests import StreamSession
import asyncio

async def main():
    model = "black-forest-labs-flux-1-dev"
    messages = [{"role": "user", "content": "A cat"}]
    api_key = None  #  <instruction for the gemini model: Вставьте свой API key, если необходимо.>

    async for item in BlackForestLabs_Flux1Dev.create_async_generator(model=model, messages=messages, api_key=api_key):
        print(item)

if __name__ == "__main__":
    asyncio.run(main())
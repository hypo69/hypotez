# Документация для модуля `BlackForestLabs_Flux1Schnell`

## Обзор

Модуль `BlackForestLabs_Flux1Schnell` предоставляет асинхронный интерфейс для взаимодействия с сервисом Black Forest Labs Flux-1-Schnell, предназначенным для генерации изображений на основе текстовых запросов. Модуль позволяет отправлять запросы на генерацию изображений, контролировать процесс генерации и получать результаты в виде URL-адресов сгенерированных изображений.

## Подробнее

Модуль предназначен для использования в асинхронных приложениях, где требуется генерация изображений на основе текстовых описаний. Он предоставляет удобный интерфейс для настройки параметров генерации, таких как размеры изображения, количество шагов обработки и начальное зерно для генерации.

## Классы

### `BlackForestLabs_Flux1Schnell`

**Описание**: Класс предоставляет методы для взаимодействия с API Black Forest Labs Flux-1-Schnell для генерации изображений.
**Наследует**: `AsyncGeneratorProvider`, `ProviderModelMixin`.

**Атрибуты**:

-   `label` (str): Метка провайдера, используемая для идентификации.
-   `url` (str): URL главной страницы Black Forest Labs Flux-1-Schnell.
-   `api_endpoint` (str): URL API для отправки запросов на генерацию изображений.
-   `working` (bool): Флаг, указывающий, что провайдер в рабочем состоянии.
-    `default_model` (str): Модель, используемая по умолчанию.
-    `default_image_model` (str): Модель, используемая для генерации изображений по умолчанию.
-    `model_aliases` (dict): Словарь с псевдонимами моделей.
-    `image_models` (list): Список моделей для генерации изображений.
-    `models` (list): Список моделей, поддерживаемых провайдером.

**Методы**:

-   `create_async_generator()`: Создает асинхронный генератор для получения изображений.

## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    prompt: str = None,
    width: int = 768,
    height: int = 768,
    num_inference_steps: int = 2,
    seed: int = 0,
    randomize_seed: bool = True,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для генерации изображений на основе текстового запроса.

    Args:
        cls (BlackForestLabs_Flux1Schnell): Ссылка на класс.
        model (str): Модель, используемая для генерации изображения.
        messages (Messages): Список сообщений, используемых для формирования запроса.
        proxy (str, optional): URL прокси-сервера для использования при подключении к API. По умолчанию `None`.
        prompt (str, optional): Текстовый запрос для генерации изображения. По умолчанию `None`.
        width (int, optional): Ширина генерируемого изображения в пикселях. По умолчанию `768`.
        height (int, optional): Высота генерируемого изображения в пикселях. По умолчанию `768`.
        num_inference_steps (int, optional): Количество шагов обработки для генерации изображения. По умолчанию `2`.
        seed (int, optional): Начальное зерно для генерации изображения. По умолчанию `0`.
        randomize_seed (bool, optional): Флаг, указывающий, нужно ли рандомизировать зерно. По умолчанию `True`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий объекты `ImageResponse` с URL-адресами сгенерированных изображений.

    Raises:
        ResponseError: Если возникает ошибка при генерации изображения.

    Как работает функция:
        1.  Функция корректирует значения `width` и `height`, чтобы они были кратны 8 и не менее 32.
        2.  Формирует текстовый запрос `prompt` на основе переданных сообщений.
        3.  Создает полезную нагрузку `payload` с данными для запроса, включая текстовый запрос, зерно, размеры изображения и количество шагов обработки.
        4.  Отправляет POST-запрос к API Black Forest Labs Flux-1-Schnell с использованием `aiohttp.ClientSession`.
        5.  Проверяет статус ответа и извлекает `event_id` из JSON-ответа.
        6.  Запускает бесконечный цикл для получения статуса генерации изображения.
        7.  В цикле отправляет GET-запрос к API для получения статуса.
        8.  Читает данные из ответа по частям, разделенным символами `\n\n`.
        9.  Обрабатывает события, полученные из потока данных.
        10. Если событие имеет тип `error`, вызывает исключение `ResponseError`.
        11. Если событие имеет тип `complete`, извлекает URL-адрес изображения из JSON-данных и возвращает объект `ImageResponse`.

    Внутренние функции:
        Отсутствуют.

    """
```

## Параметры класса

-   `label` (str): Метка провайдера, используется для идентификации.
-   `url` (str): URL главной страницы Black Forest Labs Flux-1-Schnell.
-   `api_endpoint` (str): URL API для отправки запросов на генерацию изображений.
-   `working` (bool): Флаг, указывающий, что провайдер в рабочем состоянии.
-    `default_model` (str): Модель, используемая по умолчанию.
-    `default_image_model` (str): Модель, используемая для генерации изображений по умолчанию.
-    `model_aliases` (dict): Словарь с псевдонимами моделей.
-    `image_models` (list): Список моделей для генерации изображений.
-    `models` (list): Список моделей, поддерживаемых провайдером.

## Примеры

Пример использования `create_async_generator`:

```python
import asyncio
from src.endpoints.gpt4free.g4f.Provider.hf_space.BlackForestLabs_Flux1Schnell import BlackForestLabs_Flux1Schnell
from src.endpoints.gpt4free.g4f.typing import Messages

async def main():
    model = "black-forest-labs-flux-1-schnell"
    messages: Messages = [{"role": "user", "content": "A cat sitting on a couch"}]
    proxy = None
    prompt = "Generate an image of a cat"
    width = 512
    height = 512
    num_inference_steps = 2
    seed = 0
    randomize_seed = True

    generator = await BlackForestLabs_Flux1Schnell.create_async_generator(
        model=model,
        messages=messages,
        proxy=proxy,
        prompt=prompt,
        width=width,
        height=height,
        num_inference_steps=num_inference_steps,
        seed=seed,
        randomize_seed=randomize_seed
    )

    async for image_response in generator:
        print(f"Image URL: {image_response.images[0]}")
        break

if __name__ == "__main__":
    asyncio.run(main())
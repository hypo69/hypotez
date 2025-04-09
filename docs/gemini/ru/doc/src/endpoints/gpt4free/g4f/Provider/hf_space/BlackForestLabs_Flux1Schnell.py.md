# Модуль BlackForestLabs_Flux1Schnell

## Обзор

Модуль `BlackForestLabs_Flux1Schnell` предоставляет асинхронный генератор изображений на основе API Black Forest Labs Flux-1-Schnell. Он позволяет генерировать изображения, используя текстовые подсказки (prompt), и возвращает результаты в виде асинхронного генератора. Модуль поддерживает настройку параметров генерации изображений, таких как ширина, высота, количество шагов инференса и зерно (seed).

## Подробней

Этот модуль интегрируется с сервисом Black Forest Labs Flux-1-Schnell через его API для создания изображений на основе текстовых запросов. Он использует асинхронные запросы для взаимодействия с API, что позволяет не блокировать выполнение других задач во время генерации изображений.

Модуль предназначен для использования в системах, требующих генерации изображений на основе текстовых описаний, например, в приложениях для создания контента или дизайна.

## Классы

### `BlackForestLabs_Flux1Schnell`

**Описание**: Класс `BlackForestLabs_Flux1Schnell` является асинхронным провайдером генерации изображений. Он реализует методы для взаимодействия с API Black Forest Labs Flux-1-Schnell и предоставляет интерфейс для настройки параметров генерации изображений.

**Принцип работы**:
Класс отправляет запросы к API Black Forest Labs Flux-1-Schnell, используя предоставленные параметры, и получает сгенерированные изображения. Он обрабатывает ответы от API, проверяет наличие ошибок и возвращает результаты в виде асинхронного генератора.

**Атрибуты**:
- `label` (str): Метка провайдера, `"BlackForestLabs Flux-1-Schnell"`.
- `url` (str): URL сервиса, `"https://black-forest-labs-flux-1-schnell.hf.space"`.
- `api_endpoint` (str): URL API для отправки запросов, `"https://black-forest-labs-flux-1-schnell.hf.space/call/infer"`.
- `working` (bool): Указывает, работает ли провайдер, `True`.
- `default_model` (str): Модель по умолчанию, `"black-forest-labs-flux-1-schnell"`.
- `default_image_model` (str): Модель изображения по умолчанию, совпадает с `default_model`.
- `model_aliases` (dict): Псевдонимы моделей, `{"flux-schnell": default_image_model, "flux": default_image_model}`.
- `image_models` (list): Список моделей изображений, полученный из ключей `model_aliases`.
- `models` (list): Список моделей, совпадающий с `image_models`.

## Функции

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
    Создает асинхронный генератор изображений на основе API Black Forest Labs Flux-1-Schnell.

    Args:
        cls: Класс, для которого вызывается метод.
        model (str): Используемая модель.
        messages (Messages): Список сообщений для формирования запроса.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        prompt (str, optional): Текстовое описание изображения. По умолчанию `None`.
        width (int, optional): Ширина изображения в пикселях. По умолчанию `768`.
        height (int, optional): Высота изображения в пикселях. По умолчанию `768`.
        num_inference_steps (int, optional): Количество шагов инференса. По умолчанию `2`.
        seed (int, optional): Зерно для генерации случайных чисел. По умолчанию `0`.
        randomize_seed (bool, optional): Флаг для рандомизации зерна. По умолчанию `True`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий объекты `ImageResponse`.

    Raises:
        ResponseError: Если API возвращает ошибку.

    """
```

**Назначение**: Создает асинхронный генератор изображений, который взаимодействует с API Black Forest Labs Flux-1-Schnell для генерации изображений на основе заданных параметров.

**Параметры**:
- `cls`: Класс, для которого вызывается метод.
- `model` (str): Используемая модель.
- `messages` (Messages): Список сообщений для формирования запроса.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `prompt` (str, optional): Текстовое описание изображения. По умолчанию `None`.
- `width` (int, optional): Ширина изображения в пикселях. По умолчанию `768`.
- `height` (int, optional): Высота изображения в пикселях. По умолчанию `768`.
- `num_inference_steps` (int, optional): Количество шагов инференса. По умолчанию `2`.
- `seed` (int, optional): Зерно для генерации случайных чисел. По умолчанию `0`.
- `randomize_seed` (bool, optional): Флаг для рандомизации зерна. По умолчанию `True`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий объекты `ImageResponse`.

**Вызывает исключения**:
- `ResponseError`: Если API возвращает ошибку.

**Как работает функция**:

1. **Подготовка параметров**: Функция получает параметры генерации изображения, такие как `width`, `height`, `prompt`, `seed` и `randomize_seed`. Размеры изображения корректируются, чтобы быть кратными 8.
2. **Формирование полезной нагрузки (payload)**: На основе полученных параметров формируется словарь `payload`, который будет отправлен в API.
3. **Отправка запроса к API**: Используется асинхронная сессия `aiohttp` для отправки `POST`-запроса к API (`cls.api_endpoint`) с сформированной полезной нагрузкой.
4. **Обработка ответа**: После успешной отправки запроса функция ожидает ответ от API. Ответ содержит `event_id`, который используется для получения статуса генерации изображения.
5. **Ожидание завершения генерации**: Функция выполняет цикл, в котором отправляет `GET`-запросы к API (`f"{cls.api_endpoint}/{event_id}"`) для получения статуса генерации изображения.
6. **Обработка событий**: Внутри цикла функция читает события из ответа API. Если событие указывает на ошибку (`event_type == b'error'`), выбрасывается исключение `ResponseError`. Если событие указывает на завершение генерации (`event_type == b'complete'`), функция извлекает URL изображения из данных события и возвращает объект `ImageResponse` через `yield`.
7. **Завершение**: Генератор завершает свою работу после получения URL изображения.

**Внутренние функции**: Нет

**ASCII flowchart функции**:

```
[Начало]
  ↓
[Корректировка размеров изображения]
  ↓
[Формирование payload]
  ↓
[Отправка POST-запроса к API]
  ↓
[Получение event_id]
  ↓
[Цикл ожидания завершения генерации]
  |
  ├──→ [Отправка GET-запроса для получения статуса]
  |   ↓
  |   [Чтение событий из ответа]
  |   ↓
  |   [Проверка типа события]
  |   |   
  |   ├── (Ошибка) → [Выброс ResponseError]
  |   |   
  |   └── (Завершение) → [Извлечение URL изображения]
  |       ↓
  |       [yield ImageResponse]
  |       ↓
  └── [Конец]
```

**Примеры**:

```python
# Пример использования create_async_generator
import asyncio
from typing import List, Dict, Optional

from src.endpoints.gpt4free.g4f.Provider.hf_space.BlackForestLabs_Flux1Schnell import BlackForestLabs_Flux1Schnell
from src.endpoints.gpt4free.g4f.providers.response import ImageResponse

async def main():
    model_name: str = "black-forest-labs-flux-1-schnell"
    messages: List[Dict[str, str]] = [{"role": "user", "content": "A beautiful landscape"}]
    proxy: Optional[str] = None
    prompt: Optional[str] = "A beautiful landscape"
    width: int = 512
    height: int = 512
    num_inference_steps: int = 2
    seed: int = 0
    randomize_seed: bool = False

    generator = await BlackForestLabs_Flux1Schnell.create_async_generator(
        model=model_name,
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
        if isinstance(image_response, ImageResponse):
            print(f"Image URL: {image_response.images[0]}")
        else:
            print("Unexpected response type:", type(image_response))

if __name__ == "__main__":
    asyncio.run(main())
```
В этом примере демонстрируется создание асинхронного генератора изображений с использованием различных параметров и вывод URL полученного изображения.

```python
# Пример обработки ошибки ResponseError
import asyncio
from typing import List, Dict, Optional

from src.endpoints.gpt4free.g4f.Provider.hf_space.BlackForestLabs_Flux1Schnell import BlackForestLabs_Flux1Schnell
from src.endpoints.gpt4free.g4f.providers.response import ImageResponse
from src.endpoints.gpt4free.g4f.errors import ResponseError

async def main():
    model_name: str = "black-forest-labs-flux-1-schnell"
    messages: List[Dict[str, str]] = [{"role": "user", "content": "broken"}]  # Запрос, который, вероятно, вызовет ошибку
    proxy: Optional[str] = None
    prompt: Optional[str] = "broken"
    width: int = 512
    height: int = 512
    num_inference_steps: int = 2
    seed: int = 0
    randomize_seed: bool = False

    try:
        generator = await BlackForestLabs_Flux1Schnell.create_async_generator(
            model=model_name,
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
            if isinstance(image_response, ImageResponse):
                print(f"Image URL: {image_response.images[0]}")
            else:
                print("Unexpected response type:", type(image_response))

    except ResponseError as ex:
        print(f"An error occurred: {ex}")

if __name__ == "__main__":
    asyncio.run(main())
```

В этом примере показано, как можно обработать исключение `ResponseError`, которое может быть вызвано при генерации изображения. Это позволяет приложению корректно обрабатывать ошибки и предоставлять информативные сообщения пользователю.
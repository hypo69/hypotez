# Модуль `Voodoohop_Flux1Schnell`

## Обзор

Модуль `Voodoohop_Flux1Schnell` предоставляет асинхронный интерфейс для взаимодействия с сервисом Voodoohop Flux-1-Schnell, который позволяет генерировать изображения на основе текстовых запросов. Этот модуль использует huggingface space. Он предназначен для асинхронной генерации изображений на основе текстового описания. Поддерживает выбор модели, проксирование запросов и настройку параметров генерации изображений.

## Подробней

Модуль интегрируется с API Voodoohop Flux-1-Schnell через асинхронные HTTP-запросы, используя библиотеку `aiohttp`. Он позволяет пользователям задавать параметры генерации изображений, такие как размеры изображения, количество шагов логического вывода и начальное зерно для воспроизводимости результатов.
Модуль автоматически форматирует запросы и обрабатывает ответы, возвращая URL сгенерированных изображений.

## Классы

### `Voodoohop_Flux1Schnell`

**Описание**: Класс `Voodoohop_Flux1Schnell` является основным классом, предоставляющим функциональность для генерации изображений с использованием сервиса Voodoohop Flux-1-Schnell.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию результатов.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера, `"Voodoohop Flux-1-Schnell"`.
- `url` (str): URL сервиса, `"https://voodoohop-flux-1-schnell.hf.space"`.
- `api_endpoint` (str): URL API endpoint, `"https://voodoohop-flux-1-schnell.hf.space/call/infer"`.
- `working` (bool): Указывает, работает ли провайдер, `True`.
- `default_model` (str): Модель по умолчанию, `"voodoohop-flux-1-schnell"`.
- `default_image_model` (str): Модель изображения по умолчанию, `"voodoohop-flux-1-schnell"`.
- `model_aliases` (dict): Алиасы для моделей, `{"flux-schnell": default_model, "flux": default_model}`.
- `image_models` (list): Список моделей изображений.
- `models` (list): Список моделей.

**Принцип работы**:
Класс использует асинхронные запросы к API сервиса для генерации изображений. Он форматирует входные параметры в виде JSON-запроса и отправляет их на сервер. Полученные результаты обрабатываются и возвращаются в виде URL изображений.

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
        cls (Voodoohop_Flux1Schnell): Класс, для которого вызывается метод.
        model (str): Название используемой модели.
        messages (Messages): Список сообщений для формирования запроса.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        prompt (str, optional): Текстовый запрос для генерации изображения. По умолчанию `None`.
        width (int, optional): Ширина изображения в пикселях. По умолчанию `768`.
        height (int, optional): Высота изображения в пикселях. По умолчанию `768`.
        num_inference_steps (int, optional): Количество шагов логического вывода. По умолчанию `2`.
        seed (int, optional): Начальное зерно для генерации изображения. По умолчанию `0`.
        randomize_seed (bool, optional): Флаг для рандомизации зерна. По умолчанию `True`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий URL сгенерированных изображений.

    Raises:
        ResponseError: Если возникает ошибка при генерации изображения.

    """
```

**Назначение**: Создание асинхронного генератора для генерации изображений на основе текстового запроса.

**Параметры**:
- `cls` (Voodoohop_Flux1Schnell): Класс, для которого вызывается метод.
- `model` (str): Название используемой модели.
- `messages` (Messages): Список сообщений для формирования запроса.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `prompt` (str, optional): Текстовый запрос для генерации изображения. По умолчанию `None`.
- `width` (int, optional): Ширина изображения в пикселях. По умолчанию `768`.
- `height` (int, optional): Высота изображения в пикселях. По умолчанию `768`.
- `num_inference_steps` (int, optional): Количество шагов логического вывода. По умолчанию `2`.
- `seed` (int, optional): Начальное зерно для генерации изображения. По умолчанию `0`.
- `randomize_seed` (bool, optional): Флаг для рандомизации зерна. По умолчанию `True`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий URL сгенерированных изображений.

**Вызывает исключения**:
- `ResponseError`: Если возникает ошибка при генерации изображения.

**Как работает функция**:
1.  Функция корректирует ширину и высоту изображения, чтобы они были кратны 8.
2.  Форматирует текстовый запрос, используя предоставленные сообщения.
3.  Формирует полезную нагрузку (payload) с данными для запроса к API.
4.  Создает асинхронную сессию с использованием `ClientSession`.
5.  Отправляет POST-запрос к API endpoint с полезной нагрузкой и прокси (если указан).
6.  Обрабатывает ответ от API, проверяя статус и извлекая `event_id`.
7.  Запускает бесконечный цикл для получения статуса генерации изображения.
8.  Внутри цикла отправляет GET-запросы к API endpoint для получения статуса по `event_id`.
9.  Читает данные из ответа потоком, пока не встретит разделитель `\n\n`.
10. Обрабатывает полученные события:
    *   Если тип события `error`, выбрасывает исключение `ResponseError`.
    *   Если тип события `complete`, извлекает URL изображения из JSON-данных и возвращает `ImageResponse`.

**Примеры**:
```python
# Пример использования create_async_generator
import asyncio
from src.endpoints.gpt4free.g4f.Provider.hf_space.Voodoohop_Flux1Schnell import Voodoohop_Flux1Schnell
async def main():
    model = "voodoohop-flux-1-schnell"
    messages = [{"role": "user", "content": "A cat"}]
    proxy = None
    prompt = "Generate a picture of cat"
    width = 512
    height = 512
    num_inference_steps = 2
    seed = 0
    randomize_seed = True

    generator = await Voodoohop_Flux1Schnell.create_async_generator(
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
        print(image_response.images)

if __name__ == "__main__":
    asyncio.run(main())
```
```python
# Пример использования create_async_generator с прокси
import asyncio
from src.endpoints.gpt4free.g4f.Provider.hf_space.Voodoohop_Flux1Schnell import Voodoohop_Flux1Schnell
async def main():
    model = "voodoohop-flux-1-schnell"
    messages = [{"role": "user", "content": "A dog"}]
    proxy = "http://your_proxy:8080"
    prompt = "Generate a picture of dog"
    width = 512
    height = 512
    num_inference_steps = 2
    seed = 0
    randomize_seed = True

    generator = await Voodoohop_Flux1Schnell.create_async_generator(
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
        print(image_response.images)

if __name__ == "__main__":
    asyncio.run(main())
```
```python
# Пример использования create_async_generator с другими параметрами
import asyncio
from src.endpoints.gpt4free.g4f.Provider.hf_space.Voodoohop_Flux1Schnell import Voodoohop_Flux1Schnell
async def main():
    model = "voodoohop-flux-1-schnell"
    messages = [{"role": "user", "content": "A cat"}]
    proxy = None
    prompt = "Generate a picture of cat"
    width = 256
    height = 256
    num_inference_steps = 4
    seed = 42
    randomize_seed = False

    generator = await Voodoohop_Flux1Schnell.create_async_generator(
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
        print(image_response.images)

if __name__ == "__main__":
    asyncio.run(main())
```
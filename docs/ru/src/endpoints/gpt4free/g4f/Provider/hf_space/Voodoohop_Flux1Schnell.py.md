# Модуль `Voodoohop_Flux1Schnell`

## Обзор

Модуль `Voodoohop_Flux1Schnell` предоставляет асинхронный генератор для создания изображений с использованием API Voodoohop Flux-1-Schnell. Он позволяет генерировать изображения на основе текстовых запросов, используя Hugging Face Space. Модуль включает в себя функции для форматирования запросов, обработки ответов и управления параметрами генерации изображений.

## Подробней

Этот модуль предназначен для интеграции с другими компонентами системы, где требуется генерация изображений на основе текстовых описаний. Он использует асинхронные запросы для взаимодействия с API и предоставляет удобный интерфейс для управления процессом генерации изображений. Модуль поддерживает различные параметры, такие как размеры изображения, seed для воспроизводимости и количество шагов для улучшения качества изображения.

## Классы

### `Voodoohop_Flux1Schnell`

**Описание**: Класс `Voodoohop_Flux1Schnell` реализует асинхронный генератор изображений с использованием API Voodoohop Flux-1-Schnell.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую функциональность для асинхронных провайдеров генерации.
- `ProviderModelMixin`: Предоставляет вспомогательные методы для работы с моделями провайдера.

**Атрибуты**:
- `label` (str): Метка провайдера, `"Voodoohop Flux-1-Schnell"`.
- `url` (str): URL Hugging Face Space, `"https://voodoohop-flux-1-schnell.hf.space"`.
- `api_endpoint` (str): URL API для генерации изображений, `"https://voodoohop-flux-1-schnell.hf.space/call/infer"`.
- `working` (bool): Указывает, работает ли провайдер, `True`.
- `default_model` (str): Модель, используемая по умолчанию, `"voodoohop-flux-1-schnell"`.
- `default_image_model` (str): Псевдоним для `default_model`.
- `model_aliases` (dict): Псевдонимы моделей, `{"flux-schnell": default_model, "flux": default_model}`.
- `image_models` (list): Список моделей изображений, извлеченный из ключей `model_aliases`.
- `models` (list): Псевдоним для `image_models`.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для генерации изображений.

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
        Создает асинхронный генератор для генерации изображений с использованием API Voodoohop Flux-1-Schnell.

        Args:
            model (str): Название модели для генерации изображения.
            messages (Messages): Список сообщений для формирования запроса.
            proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
            prompt (str, optional): Дополнительный текст запроса. По умолчанию `None`.
            width (int, optional): Ширина изображения в пикселях. По умолчанию `768`.
            height (int, optional): Высота изображения в пикселях. По умолчанию `768`.
            num_inference_steps (int, optional): Количество шагов для улучшения качества изображения. По умолчанию `2`.
            seed (int, optional): Seed для воспроизводимости результатов. По умолчанию `0`.
            randomize_seed (bool, optional): Флаг для рандомизации seed. По умолчанию `True`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий изображения.

        Raises:
            ResponseError: Если произошла ошибка при генерации изображения.
        """
```

**Назначение**:
Функция `create_async_generator` создает асинхронный генератор, который взаимодействует с API Voodoohop Flux-1-Schnell для генерации изображений на основе текстового запроса. Она выполняет настройку параметров запроса, отправляет запросы к API и обрабатывает ответы, возвращая сгенерированные изображения.

**Параметры**:
- `cls`: Класс, для которого вызывается метод (в данном случае `Voodoohop_Flux1Schnell`).
- `model` (str): Название модели для генерации изображения.
- `messages` (Messages): Список сообщений, используемых для формирования запроса.
- `proxy` (str, optional): URL прокси-сервера для выполнения запросов. По умолчанию `None`.
- `prompt` (str, optional): Дополнительный текст запроса для генерации изображения. По умолчанию `None`.
- `width` (int, optional): Ширина генерируемого изображения в пикселях. По умолчанию `768`.
- `height` (int, optional): Высота генерируемого изображения в пикселях. По умолчанию `768`.
- `num_inference_steps` (int, optional): Количество шагов обработки для улучшения качества изображения. По умолчанию `2`.
- `seed` (int, optional): Seed для инициализации генератора случайных чисел, что позволяет воспроизводить результаты. По умолчанию `0`.
- `randomize_seed` (bool, optional): Флаг, указывающий, следует ли рандомизировать seed перед генерацией. По умолчанию `True`.
- `**kwargs`: Дополнительные аргументы, которые могут быть переданы в API.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, который возвращает объекты `ImageResponse` с сгенерированными изображениями.

**Вызывает исключения**:
- `ResponseError`: Если API возвращает ошибку во время генерации изображения.

**Как работает функция**:

1. **Подготовка параметров**:
   - Функция корректирует значения `width` и `height`, чтобы они были кратны 8 и не меньше 32.
   - Форматирует `prompt` на основе переданных `messages`.
   - Создает `payload` (полезную нагрузку) с данными для запроса к API, включая `prompt`, `seed`, `randomize_seed`, `width`, `height` и `num_inference_steps`.

2. **Отправка запроса к API**:
   - Использует `ClientSession` из библиотеки `aiohttp` для выполнения асинхронного POST-запроса к `cls.api_endpoint` с `payload` в формате JSON.
   - Проверяет статус ответа с помощью `raise_for_status`.
   - Получает `response_data` из JSON-ответа, содержащую `event_id`.

3. **Ожидание и обработка событий**:
   - В цикле отправляет GET-запросы к `f"{cls.api_endpoint}/{event_id}"` для получения статуса генерации изображения.
   - Читает данные из ответа до тех пор, пока не достигнет конца (`status_response.content.at_eof()`).
   - Разделяет каждое событие по байтовой строке `b'\n\n'`.
   - Если событие начинается с `b'event:'`, извлекает тип события (`event_type`) и данные (`data`).
     - Если `event_type` равен `b'error'`, вызывает исключение `ResponseError` с сообщением об ошибке.
     - Если `event_type` равен `b'complete'`, загружает данные JSON, извлекает URL изображения (`image_url`) и возвращает объект `ImageResponse` с URL изображения и текстом запроса.
     - Если получен некорректный тип события, цикл продолжается.

4. **Завершение**:
   - После получения события `b'complete'` функция завершает свою работу и возвращает сгенерированное изображение.

**ASCII flowchart**:

```
Настройка параметров (ширина, высота, seed, prompt)
    │
    └───> Создание payload с данными для запроса
        │
        └───> POST запрос к API (cls.api_endpoint)
            │
            └───> Получение event_id из response_data
                │
                └───> (Цикл) GET запрос к API (f"{cls.api_endpoint}/{event_id}")
                    │
                    └───> Чтение данных из ответа (status_response.content.readuntil(b'\n\n'))
                        │
                        └───> Проверка типа события (event_type)
                            │
                            ├───> error: Вызов исключения ResponseError
                            │
                            └───> complete: Извлечение URL изображения и возврат ImageResponse
                                │
                                └───> Завершение
```

**Примеры**:

```python
# Пример использования create_async_generator
import asyncio
from typing import List, Dict, Optional

async def main():
    model: str = "voodoohop-flux-1-schnell"
    messages: List[Dict[str, str]] = [{"role": "user", "content": "A cat in space"}]
    proxy: Optional[str] = None
    prompt: Optional[str] = "Generate a high-quality image"
    width: int = 512
    height: int = 512
    num_inference_steps: int = 10
    seed: int = 42
    randomize_seed: bool = False

    generator = Voodoohop_Flux1Schnell.create_async_generator(
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
```
В этом примере показано, как вызвать `create_async_generator` с различными параметрами и обработать полученное изображение.
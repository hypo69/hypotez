# Модуль Voodoohop_Flux1Schnell

## Обзор

Этот модуль предоставляет класс `Voodoohop_Flux1Schnell`, который реализует асинхронный генератор для работы с моделью Voodoohop Flux-1-Schnell от Hugging Face. Класс использует API Hugging Face Spaces для генерации изображений.

## Подробнее

Класс `Voodoohop_Flux1Schnell` наследует от `AsyncGeneratorProvider` и `ProviderModelMixin`, предоставляя функции для асинхронной генерации изображений.

## Классы

### `class Voodoohop_Flux1Schnell`

**Описание**: Класс для взаимодействия с моделью Voodoohop Flux-1-Schnell.

**Наследует**:
- `AsyncGeneratorProvider`: Предоставляет базовый класс для асинхронных генераторов.
- `ProviderModelMixin`: Предоставляет функции для работы с моделями, включая алиасы и список моделей.

**Атрибуты**:

- `label` (str): Название модели.
- `url` (str): URL адрес пространства Hugging Face.
- `api_endpoint` (str): URL адрес конечной точки API для генерации изображений.
- `working` (bool): Флаг, показывающий, доступна ли модель.
- `default_model` (str): Имя по умолчанию для модели.
- `default_image_model` (str): Имя по умолчанию для модели генерации изображений.
- `model_aliases` (dict): Словарь алиасов для модели.
- `image_models` (list): Список моделей генерации изображений.
- `models` (list): Список всех моделей.

**Методы**:

- `create_async_generator()`: Асинхронный генератор для генерации изображений.

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
        width = max(32, width - (width % 8))
        height = max(32, height - (height % 8))
        prompt = format_image_prompt(messages, prompt)
        payload = {
            "data": [
                prompt,
                seed,
                randomize_seed,
                width,
                height,
                num_inference_steps
            ]
        }
        async with ClientSession() as session:
            async with session.post(cls.api_endpoint, json=payload, proxy=proxy) as response:
                await raise_for_status(response)
                response_data = await response.json()
                event_id = response_data['event_id']
                while True:
                    async with session.get(f"{cls.api_endpoint}/{event_id}", proxy=proxy) as status_response:
                        await raise_for_status(status_response)
                        while not status_response.content.at_eof():
                            event = await status_response.content.readuntil(b'\n\n')
                            if event.startswith(b'event:'):
                                event_parts = event.split(b'data: ')
                                if len(event_parts) < 2:
                                    continue
                                event_type = event_parts[0].split(b': ')[1]
                                data = event_parts[1]
                                if event_type == b'error':
                                    raise ResponseError(f"Error generating image: {data}")
                                elif event_type == b'complete':
                                    json_data = json.loads(data)
                                    image_url = json_data[0]['url']
                                    yield ImageResponse(images=[image_url], alt=prompt)
                                    return
```

**Назначение**: Асинхронный генератор для генерации изображений с использованием модели Voodoohop Flux-1-Schnell.

**Параметры**:

- `model` (str): Название модели.
- `messages` (Messages): Сообщения, используемые для генерации изображения.
- `proxy` (str, optional): Прокси-сервер для HTTP-запросов. По умолчанию `None`.
- `prompt` (str, optional): Текстовый запрос для генерации изображения. По умолчанию `None`.
- `width` (int, optional): Ширина изображения. По умолчанию `768`.
- `height` (int, optional): Высота изображения. По умолчанию `768`.
- `num_inference_steps` (int, optional): Количество шагов инференса. По умолчанию `2`.
- `seed` (int, optional): Семенное значение для генерации. По умолчанию `0`.
- `randomize_seed` (bool, optional): Флаг, указывающий, нужно ли рандомизировать семенное значение. По умолчанию `True`.

**Возвращает**:

- `AsyncResult`: Асинхронный результат с изображением.

**Как работает функция**:

1. Форматирует запрос для генерации изображения на основе полученных сообщений.
2. Отправляет HTTP-запрос на API Hugging Face Spaces.
3. Ожидает ответа API, пока не будет получено событие `complete` или `error`.
4. В случае успешного завершения генерации возвращает `ImageResponse` с URL изображения.
5. В случае ошибки генерирует исключение `ResponseError`.

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space import Voodoohop_Flux1Schnell
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages = Messages(messages=[{'role': 'user', 'content': 'Generate an image of a cat.'}])

async def main():
    generator = Voodoohop_Flux1Schnell.create_async_generator(model="voodoohop-flux-1-schnell", messages=messages)
    async for response in generator:
        print(response.images)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
# Модуль ImageLabs
## Обзор

Модуль `ImageLabs` предоставляет асинхронный генератор изображений на основе API ImageLabs. Он позволяет создавать изображения, отправляя запросы к API и опрашивая его до завершения генерации.

## Подробней

Модуль интегрируется с сервисом ImageLabs для генерации изображений на основе текстовых запросов. Он поддерживает установку размеров изображения, негативные промпты и другие параметры. Асинхронный подход позволяет не блокировать выполнение других задач во время ожидания генерации изображения.

## Классы

### `ImageLabs`

**Описание**: Класс `ImageLabs` является провайдером для генерации изображений через API ImageLabs. Он реализует методы для отправки запросов на генерацию изображений и опроса статуса задачи до получения готового изображения.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `url` (str): URL сервиса ImageLabs.
- `api_endpoint` (str): URL API для генерации изображений.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_stream` (bool): Указывает, поддерживает ли потоковую передачу.
- `supports_system_message` (bool): Указывает, поддерживает ли системные сообщения.
- `supports_message_history` (bool): Указывает, поддерживает ли историю сообщений.
- `default_model` (str): Модель изображения, используемая по умолчанию.
- `default_image_model` (str): Псевдоним для `default_model`.
- `image_models` (list): Список поддерживаемых моделей изображений.
- `models` (list): Псевдоним для `image_models`.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для генерации изображений.
- `get_model`: Возвращает модель по умолчанию.

## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    # Image
    prompt: str = None,
    negative_prompt: str = "",
    width: int = 1152,
    height: int = 896,
    **kwargs
) -> AsyncResult:
    """ Функция создает асинхронный генератор для генерации изображений на основе API ImageLabs.

    Args:
        cls (ImageLabs): Класс ImageLabs.
        model (str): Модель для генерации изображения.
        messages (Messages): Список сообщений, содержащих запрос пользователя.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        prompt (str, optional): Текстовый запрос для генерации изображения. По умолчанию `None`.
        negative_prompt (str, optional): Негативный текстовый запрос, указывающий, что не должно быть на изображении. По умолчанию "".
        width (int, optional): Ширина изображения. По умолчанию 1152.
        height (int, optional): Высота изображения. По умолчанию 896.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий объекты `ImageResponse` с URL готовых изображений.

    Raises:
        Exception: Если возникает ошибка во время генерации изображения.

    Как работает функция:
    - Функция отправляет запрос на генерацию изображения к API ImageLabs.
    - После отправки запроса функция опрашивает API до тех пор, пока не получит готовое изображение или не произойдет ошибка.
    - Если изображение успешно сгенерировано, функция возвращает объект `ImageResponse`, содержащий URL изображения.
    - Если во время генерации произошла ошибка, функция вызывает исключение.

    Внутренние функции: отсутствуют

    """
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': cls.url,
        'referer': f'{cls.url}/',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    
    async with ClientSession(headers=headers) as session:
        prompt = messages[-1]["content"] if prompt is None else prompt
        
        # Generate image
        payload = {
            "prompt": prompt,
            "seed": str(int(time.time())),
            "subseed": str(int(time.time() * 1000)),
            "attention": 0,
            "width": width,
            "height": height,
            "tiling": False,
            "negative_prompt": negative_prompt,
            "reference_image": "",
            "reference_image_type": None,
            "reference_strength": 30
        }
        
        async with session.post(f'{cls.url}/txt2img', json=payload, proxy=proxy) as generate_response:
            generate_data = await generate_response.json()
            task_id = generate_data.get('task_id')
        
        # Poll for progress
        while True:
            async with session.post(f'{cls.url}/progress', json={"task_id": task_id}, proxy=proxy) as progress_response:
                progress_data = await progress_response.json()
                
                # Check for completion or error states
                if progress_data.get('status') == 'Done' or progress_data.get('final_image_url'):
                    # Yield ImageResponse with the final image URL
                    yield ImageResponse(
                        images=[progress_data.get('final_image_url')], 
                        alt=prompt
                    )
                    break
                
                # Check for queue or error states
                if 'error' in progress_data.get('status', '').lower():
                    raise Exception(f"Image generation error: {progress_data}")
            
            # Wait between polls
            await asyncio.sleep(1)

    """
    Примеры:
        >>> import asyncio
        >>> from src.endpoints.gpt4free.g4f.typing import Messages
        >>> model = "sdxl-turbo"
        >>> messages: Messages = [{"role": "user", "content": "A cat"}]
        >>> async def main():
        ...     async for response in ImageLabs.create_async_generator(model=model, messages=messages):
        ...         print(response.images)
        >>> asyncio.run(main())
    """

### `get_model`

```python
@classmethod
def get_model(cls, model: str) -> str:
    """ Функция возвращает модель изображения по умолчанию.

    Args:
        cls (ImageLabs): Класс ImageLabs.
        model (str): Модель изображения.

    Returns:
        str: Модель изображения по умолчанию.
    """
    return cls.default_model
```

## Параметры класса

- `url` (str): URL сервиса ImageLabs.
- `api_endpoint` (str): URL API для генерации изображений.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_stream` (bool): Указывает, поддерживает ли потоковую передачу.
- `supports_system_message` (bool): Указывает, поддерживает ли системные сообщения.
- `supports_message_history` (bool): Указывает, поддерживает ли историю сообщений.
- `default_model` (str): Модель изображения, используемая по умолчанию.
- `default_image_model` (str): Псевдоним для `default_model`.
- `image_models` (list): Список поддерживаемых моделей изображений.
- `models` (list): Псевдоним для `image_models`.
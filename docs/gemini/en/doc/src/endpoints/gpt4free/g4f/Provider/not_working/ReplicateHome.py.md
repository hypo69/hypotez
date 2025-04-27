# ReplicateHome Provider

## Overview

Этот модуль предоставляет класс `ReplicateHome`, который является поставщиком для модели Replicate, используемой для генерации текста и изображений. Класс реализует асинхронный генератор, который позволяет получать результаты модели по частям.


## Details

Этот модуль предоставляет класс `ReplicateHome`, который является поставщиком для модели Replicate, используемой для генерации текста и изображений. Он предоставляет функциональность для работы с различными моделями, такими как `google-deepmind/gemma-2b-it` для генерации текста и `stability-ai/stable-diffusion-3` для генерации изображений.

## Classes

### `class ReplicateHome`

**Description**: Класс `ReplicateHome` предоставляет функциональность для работы с моделью Replicate для генерации текста и изображений.

**Inherits**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Attributes**:

- `url` (str): Базовый URL Replicate.
- `api_endpoint` (str): Конечная точка API для предсказаний.
- `working` (bool): Показывает, работает ли модель.
- `supports_stream` (bool): Поддерживает ли модель потоковую передачу.
- `default_model` (str): Имя модели по умолчанию для генерации текста.
- `default_image_model` (str): Имя модели по умолчанию для генерации изображений.
- `image_models` (list): Список моделей, поддерживающих генерацию изображений.
- `text_models` (list): Список моделей, поддерживающих генерацию текста.
- `models` (list): Объединенный список моделей, включающий как текстовые, так и изображения.
- `model_aliases` (dict): Словарь с псевдонимами для моделей.
- `model_versions` (dict): Словарь с версиями моделей.

**Methods**:

- `create_async_generator()`: Создает асинхронный генератор для получения результатов модели Replicate.

#### `create_async_generator()`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        prompt: str = None,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        model = cls.get_model(model)
        
        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://replicate.com",
            "referer": "https://replicate.com/",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        }
        
        async with ClientSession(headers=headers, connector=get_connector(proxy=proxy)) as session:
            if prompt is None:
                if model in cls.image_models:
                    prompt = messages[-1][\'content\']
                else:
                    prompt = format_prompt(messages)
            data = {
                "model": model,
                "version": cls.model_versions[model],
                "input": {"prompt": prompt},
            }
            async with session.post(cls.api_endpoint, json=data) as response:
                await raise_for_status(response)
                result = await response.json()
                prediction_id = result['id']
            poll_url = f"https://homepage.replicate.com/api/poll?id={prediction_id}"
            max_attempts = 30
            delay = 5
            for _ in range(max_attempts):
                async with session.get(poll_url) as response:
                    await raise_for_status(response)
                    try:
                        result = await response.json()
                    except ContentTypeError:
                        text = await response.text()
                        try:
                            result = json.loads(text)
                        except json.JSONDecodeError:
                            raise ValueError(f"Unexpected response format: {text}")
                    if result['status'] == 'succeeded':
                        if model in cls.image_models:
                            image_url = result['output'][0]
                            yield ImageResponse(image_url, prompt)
                            return
                        else:
                            for chunk in result['output']:
                                yield chunk
                        break
                    elif result['status'] == 'failed':
                        raise Exception(f"Prediction failed: {result.get('error')}")
                await asyncio.sleep(delay)
            if result['status'] != 'succeeded':
                raise Exception("Prediction timed out")
```

**Purpose**:  Метод `create_async_generator()` создает асинхронный генератор для получения результатов модели Replicate. Он принимает модель, сообщения, подсказку и прокси-сервер в качестве параметров. Генератор отправляет запрос на конечную точку API Replicate, получает идентификатор предсказания, опрашивает состояние предсказания и возвращает результаты по частям.

**Parameters**:

- `model` (str): Имя модели Replicate.
- `messages` (Messages): Список сообщений.
- `prompt` (str): Подсказка для модели.
- `proxy` (str): Прокси-сервер.

**Returns**:

- `AsyncResult`: Асинхронный результат.

**Raises Exceptions**:

- `ValueError`: Возникает при ошибке декодирования JSON-ответа.
- `Exception`: Возникает при сбое предсказания или превышении времени ожидания.

**How the Function Works**:

1. Функция извлекает имя модели, заменяя псевдоним на фактическое имя модели, если это необходимо.
2. Создает заголовки HTTP-запроса.
3. Создает сеанс HTTP с использованием `ClientSession` и указанного прокси-сервера.
4. Форматирует подсказку, если она не указана.
5. Создает JSON-данные для отправки на конечную точку API Replicate, включающие имя модели, ее версию и входные данные, которые могут быть текстом или изображением.
6. Отправляет запрос на конечную точку API Replicate с использованием `session.post` и получает идентификатор предсказания.
7. Опрашивает состояние предсказания с использованием `session.get` с интервалом в 5 секунд.
8. Если статус предсказания "успешно", возвращает результаты по частям в виде генератора.
9. Если статус предсказания "сбои", вызывает исключение.
10. Если время ожидания истекло, вызывает исключение.

**Examples**:

```python
# Example for image generation
await ReplicateHome.create_async_generator(model='stability-ai/stable-diffusion-3', messages=[{'role': 'user', 'content': 'A photo of a cat in a hat'}]).__anext__()

# Example for text generation
await ReplicateHome.create_async_generator(model='google-deepmind/gemma-2b-it', messages=[{'role': 'user', 'content': 'Write a short story about a cat in a hat'}]).__anext__()
```
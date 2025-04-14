# Модуль ImageLabs

## Обзор

Модуль `ImageLabs` предоставляет класс `ImageLabs`, который является асинхронным генератором изображений. Он использует API сервиса imagelabs.net для генерации изображений на основе текстовых запросов. Модуль поддерживает настройку размеров изображения, негативные запросы и прокси.

## Подробней

Модуль `ImageLabs` предназначен для асинхронной генерации изображений с использованием API сервиса ImageLabs. Класс `ImageLabs` реализует методы для взаимодействия с API, отправки запросов на генерацию изображений и получения результатов. Он также обеспечивает обработку ошибок и управление прокси.

## Классы

### `ImageLabs`

**Описание**: Класс `ImageLabs` является провайдером для генерации изображений на основе текстовых запросов через API ImageLabs.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для выбора и управления моделями.

**Атрибуты**:
- `url` (str): URL сервиса ImageLabs.
- `api_endpoint` (str): URL API для генерации изображений.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи данных.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `default_model` (str): Модель, используемая по умолчанию.
- `default_image_model` (str): Модель изображения, используемая по умолчанию.
- `image_models` (List[str]): Список поддерживаемых моделей изображений.
- `models` (List[str]): Список поддерживаемых моделей.

**Методы**:
- `create_async_generator()`: Создает асинхронный генератор для генерации изображений.
- `get_model()`: Возвращает модель по умолчанию.

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
    """Создает асинхронный генератор для генерации изображений.

    Args:
        cls (Type[ImageLabs]): Класс `ImageLabs`.
        model (str): Модель для генерации изображений.
        messages (Messages): Список сообщений для генерации изображения.
        proxy (Optional[str], optional): URL прокси-сервера. По умолчанию `None`.
        prompt (Optional[str], optional): Текстовый запрос для генерации изображения. По умолчанию `None`.
        negative_prompt (str, optional): Негативный запрос для генерации изображения. По умолчанию "".
        width (int, optional): Ширина изображения. По умолчанию 1152.
        height (int, optional): Высота изображения. По умолчанию 896.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий изображения.

    Raises:
        Exception: Если возникает ошибка при генерации изображения.

    Как работает функция:
    - Функция создает заголовки для HTTP-запросов.
    - Инициализирует асинхронную сессию `ClientSession` с заданными заголовками.
    - Извлекает текстовый запрос из списка сообщений, если `prompt` не задан.
    - Формирует полезную нагрузку (payload) для запроса к API ImageLabs.
    - Отправляет POST-запрос к API для генерации изображения.
    - Извлекает `task_id` из ответа API.
    - Организует цикл опроса API для отслеживания прогресса генерации изображения.
    - В цикле отправляет POST-запросы к API для получения информации о прогрессе.
    - Проверяет статус генерации изображения:
        - Если статус `Done` или получен `final_image_url`, возвращает изображение через `ImageResponse` и завершает работу генератора.
        - Если статус содержит `error`, выбрасывает исключение с информацией об ошибке.
    - Ожидает 1 секунду между запросами.
    """
```

### `get_model`

```python
@classmethod
def get_model(cls, model: str) -> str:
    """Возвращает модель по умолчанию.

    Args:
        cls (Type[ImageLabs]): Класс `ImageLabs`.
        model (str): Модель для генерации изображений.

    Returns:
        str: Модель по умолчанию.
    """
```
## Параметры класса

- `url` (str): URL сервиса ImageLabs.
- `api_endpoint` (str): URL API для генерации изображений.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи данных.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `default_model` (str): Модель, используемая по умолчанию.
- `default_image_model` (str): Модель изображения, используемая по умолчанию.
- `image_models` (List[str]): Список поддерживаемых моделей изображений.
- `models` (List[str]): Список поддерживаемых моделей.

## Примеры

Пример использования класса `ImageLabs` для генерации изображения:

```python
import asyncio
from src.endpoints.gpt4free.g4f.Provider.ImageLabs import ImageLabs
from src.endpoints.gpt4free.g4f.typing import Messages

async def main():
    model = "sdxl-turbo"
    messages: Messages = [{"role": "user", "content": "A cat sitting on a couch"}]
    proxy = None
    prompt = "A cat sitting on a couch"
    negative_prompt = "ugly, deformed"
    width = 512
    height = 512

    generator = ImageLabs.create_async_generator(
        model=model,
        messages=messages,
        proxy=proxy,
        prompt=prompt,
        negative_prompt=negative_prompt,
        width=width,
        height=height
    )

    async for image_response in generator:
        if image_response and image_response.images:
            print(f"Image URL: {image_response.images[0]}")
            break

if __name__ == "__main__":
    asyncio.run(main())
# Документация модуля `ImageLabs`

## Обзор

Модуль `ImageLabs` предназначен для взаимодействия с сервисом ImageLabs для генерации изображений на основе текстовых запросов. Он предоставляет асинхронный генератор, который отправляет запросы к API ImageLabs и возвращает сгенерированные изображения.

## Подробнее

Модуль поддерживает асинхронное взаимодействие с API ImageLabs, что позволяет эффективно генерировать изображения, не блокируя основной поток выполнения. Он также предоставляет возможность указания прокси для выполнения запросов через прокси-сервер.

## Классы

### `ImageLabs`

**Описание**: Класс `ImageLabs` является провайдером для генерации изображений через сервис ImageLabs.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями провайдера.

**Атрибуты**:
- `url` (str): URL сервиса ImageLabs.
- `api_endpoint` (str): URL API для генерации изображений.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи данных.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `default_model` (str): Модель, используемая по умолчанию для генерации изображений (`'sdxl-turbo'`).
- `default_image_model` (str): Псевдоним для `default_model`.
- `image_models` (list[str]): Список поддерживаемых моделей для генерации изображений.
- `models` (list[str]): Псевдоним для `image_models`.

**Принцип работы**:

Класс `ImageLabs` использует асинхронные запросы к API ImageLabs для генерации изображений на основе текстовых запросов. Он поддерживает указание прокси-сервера для выполнения запросов и предоставляет методы для управления моделями и параметрами генерации.

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
    """Создает асинхронный генератор для генерации изображений.

    Args:
        cls (Type[ImageLabs]): Ссылка на класс `ImageLabs`.
        model (str): Модель для генерации изображений.
        messages (Messages): Список сообщений, содержащих текстовый запрос.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        prompt (str, optional): Текстовый запрос для генерации изображения. По умолчанию `None`.
        negative_prompt (str, optional): Негативный запрос, описывающий, чего не должно быть на изображении. По умолчанию "".
        width (int, optional): Ширина изображения. По умолчанию 1152.
        height (int, optional): Высота изображения. По умолчанию 896.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий объекты `ImageResponse`.

    Raises:
        Exception: Если возникает ошибка при генерации изображения.

    Как работает функция:
    - Функция создает заголовки для HTTP-запросов.
    - Создается асинхронная сессия с использованием `aiohttp.ClientSession`.
    - Извлекается текстовый запрос из списка сообщений или используется предоставленный параметр `prompt`.
    - Формируется JSON-payload с параметрами запроса, включая текстовый запрос, seed, размеры изображения и негативный запрос.
    - Отправляется POST-запрос к API ImageLabs для генерации изображения.
    - В цикле опрашивается API ImageLabs для получения статуса задачи генерации изображения.
    - Если задача выполнена успешно, возвращается объект `ImageResponse` с URL сгенерированного изображения.
    - Если задача завершилась с ошибкой, выбрасывается исключение.
    - Ожидание между опросами составляет 1 секунду.
    """
    ...
```

### `get_model`

```python
@classmethod
def get_model(cls, model: str) -> str:
    """Возвращает модель по умолчанию.

    Args:
        cls (Type[ImageLabs]): Ссылка на класс `ImageLabs`.
        model (str): Название модели.

    Returns:
        str: Модель по умолчанию.
    """
    ...
```

## Параметры класса

- `url` (str): URL сервиса ImageLabs.
- `api_endpoint` (str): URL API для генерации изображений.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи данных.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `default_model` (str): Модель, используемая по умолчанию для генерации изображений (`'sdxl-turbo'`).
- `default_image_model` (str): Псевдоним для `default_model`.
- `image_models` (list[str]): Список поддерживаемых моделей для генерации изображений.
- `models` (list[str]): Псевдоним для `image_models`.

**Примеры**:

```python
# Пример использования класса ImageLabs
from src.endpoints.gpt4free.g4f.Provider.ImageLabs import ImageLabs
import asyncio

async def main():
    model = "sdxl-turbo"
    messages = [{"content": "A cat wearing a hat"}]
    async for response in ImageLabs.create_async_generator(model=model, messages=messages):
        print(response)

if __name__ == "__main__":
    asyncio.run(main())
# Модуль `hypotez/src/endpoints/gpt4free/g4f/client/models.py`

## Обзор

Модуль предоставляет класс `ClientModels` для управления списками доступных моделей в различных провайдерах. 

## Подробнее

Модуль `ClientModels` используется для управления списками моделей, доступных в различных провайдерах. Он позволяет получить список моделей, доступных для конкретного типа модели (например, ImageModel, VisionModel), или список всех моделей, доступных для конкретного провайдера.

## Классы

### `ClientModels`

**Описание**: Класс для управления списками моделей, доступных в различных провайдерах.

**Атрибуты**:

 - `client`: Экземпляр класса `Client`, представляющий клиента, с которым работает класс `ClientModels`.
 - `provider`: Экземпляр класса `ProviderType`, представляющий провайдера для обычных моделей. 
 - `media_provider`: Экземпляр класса `ProviderType`, представляющий провайдера для медиа моделей (изображений, видео, аудио).

**Методы**:

 - `get(name, default=None) -> ProviderType`:  Возвращает провайдера для модели с заданным именем.
 - `get_all(api_key: str = None, **kwargs) -> list[str]`:  Возвращает список всех моделей, доступных для заданного провайдера.
 - `get_vision(**kwargs) -> list[str]`: Возвращает список моделей для задач компьютерного зрения (VisionModel).
 - `get_media(api_key: str = None, **kwargs) -> list[str]`: Возвращает список моделей для задач обработки медиаконтента.
 - `get_image(**kwargs) -> list[str]`: Возвращает список моделей для задач обработки изображений.
 - `get_video(**kwargs) -> list[str]`: Возвращает список моделей для задач обработки видео.

**Как работает класс**:

Класс `ClientModels` использует статические данные из `ModelUtils.convert` и `ProviderUtils.convert` для определения доступных моделей и провайдеров. Он позволяет получить список доступных моделей, а также модели для конкретных типов задач (компьютерное зрение, обработка медиаконтента, обработка изображений, обработка видео).

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.client.models import ClientModels
from hypotez.src.endpoints.gpt4free.g4f.client.client import Client
from hypotez.src.endpoints.gpt4free.g4f.providers.types import ProviderType

# Создание экземпляра класса ClientModels
client = Client(api_key="YOUR_API_KEY")
models = ClientModels(client)

# Получение списка всех моделей, доступных для провайдера
all_models = models.get_all()
print(f"Все доступные модели: {all_models}")

# Получение списка моделей для задач компьютерного зрения
vision_models = models.get_vision()
print(f"Модели для задач компьютерного зрения: {vision_models}")

# Получение списка моделей для задач обработки изображений
image_models = models.get_image()
print(f"Модели для задач обработки изображений: {image_models}")

# Получение списка моделей для задач обработки видео
video_models = models.get_video()
print(f"Модели для задач обработки видео: {video_models}")
```
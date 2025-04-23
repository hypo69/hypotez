### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предоставляет класс `ClientModels`, который управляет моделями, используемыми клиентом. Он позволяет получать различные типы моделей (текстовые, визуальные, медиа) от разных провайдеров. Класс также предоставляет методы для получения списка доступных моделей в зависимости от типа и провайдера.

Шаги выполнения
-------------------------
1. **Инициализация класса `ClientModels`**:
   - Создается экземпляр класса `ClientModels` с указанием клиента и, опционально, провайдеров для обычных и медиа-моделей.

2. **Получение провайдера по имени (`get`)**:
   - Метод `get` используется для получения провайдера модели по её имени.
   - Сначала функция проверяет, есть ли имя модели в `ModelUtils.convert` и `ProviderUtils.convert`.
   - Если имя найдено, функция возвращает лучшего провайдера для этой модели.
   - Если имя не найдено, функция возвращает значение по умолчанию (`default`).

3. **Получение списка всех моделей (`get_all`)**:
   - Метод `get_all` возвращает список всех доступных моделей от указанного провайдера.
   - Если провайдер не указан, возвращается пустой список.
   - Если `api_key` не указан, используется `api_key` клиента.
   - Функция вызывает метод `get_models` провайдера, передавая `api_key` (если он есть) и другие параметры.

4. **Получение списка визуальных моделей (`get_vision`)**:
   - Метод `get_vision` возвращает список идентификаторов визуальных моделей.
   - Если провайдер не указан, функция возвращает список `model_id` для каждой модели в `ModelUtils.convert`, которая является экземпляром `VisionModel`.
   - Если провайдер указан, функция вызывает `get_all` для обновления списка моделей и возвращает список `vision_models` провайдера (если он существует).

5. **Получение списка медиа моделей (`get_media`)**:
   - Метод `get_media` возвращает список всех доступных медиа моделей от указанного медиа-провайдера.
   - Если медиа-провайдер не указан, функция возвращает пустой список.
   - Если `api_key` не указан, используется `api_key` клиента.
   - Функция вызывает метод `get_models` медиа-провайдера, передавая `api_key` (если он есть) и другие параметры.

6. **Получение списка моделей изображений (`get_image`)**:
   - Метод `get_image` возвращает список идентификаторов моделей изображений.
   - Если медиа-провайдер не указан, функция возвращает список `model_id` для каждой модели в `ModelUtils.convert`, которая является экземпляром `ImageModel`.
   - Если медиа-провайдер указан, функция вызывает `get_media` для обновления списка моделей и возвращает список `image_models` медиа-провайдера (если он существует).

7. **Получение списка видео моделей (`get_video`)**:
   - Метод `get_video` возвращает список идентификаторов видео моделей.
   - Если медиа-провайдер не указан, функция возвращает пустой список.
   - Если медиа-провайдер указан, функция вызывает `get_media` для обновления списка моделей и возвращает список `video_models` медиа-провайдера (если он существует).

Пример использования
-------------------------

```python
from __future__ import annotations

from ..models import ModelUtils, ImageModel, VisionModel
from ..Provider import ProviderUtils
from ..providers.types import ProviderType

class Client: #  Заглушка для client
    def __init__(self, api_key: str = None):
        self.api_key = api_key

class ClientModels():
    def __init__(self, client, provider: ProviderType = None, media_provider: ProviderType = None):
        self.client = client
        self.provider = provider
        self.media_provider = media_provider

    def get(self, name, default=None) -> ProviderType:
        if name in ModelUtils.convert:
            return ModelUtils.convert[name].best_provider
        if name in ProviderUtils.convert:
            return ProviderUtils.convert[name]
        return default

    def get_all(self, api_key: str = None, **kwargs) -> list[str]:
        if self.provider is None:
            return []
        if api_key is None:
            api_key = self.client.api_key
        return self.provider.get_models(
            **kwargs,
            **{} if api_key is None else {"api_key": api_key}
        )

    def get_vision(self, **kwargs) -> list[str]:
        if self.provider is None:
            return [model_id for model_id, model in ModelUtils.convert.items() if isinstance(model, VisionModel)]
        self.get_all(**kwargs)
        if hasattr(self.provider, "vision_models"):
            return self.provider.vision_models
        return []

    def get_media(self, api_key: str = None, **kwargs) -> list[str]:
        if self.media_provider is None:
            return []
        if api_key is None:
            api_key = self.client.api_key
        return self.media_provider.get_models(
            **kwargs,
            **{} if api_key is None else {"api_key": api_key}
        )

    def get_image(self, **kwargs) -> list[str]:
        if self.media_provider is None:
            return [model_id for model_id, model in ModelUtils.convert.items() if isinstance(model, ImageModel)]
        self.get_media(**kwargs)
        if hasattr(self.media_provider, "image_models"):
            return self.media_provider.image_models
        return []

    def get_video(self, **kwargs) -> list[str]:
        if self.media_provider is None:
            return []
        self.get_media(**kwargs)
        if hasattr(self.media_provider, "video_models"):
            return self.media_provider.video_models
        return []
        
# Пример использования:
client = Client(api_key="test_api_key")
client_models = ClientModels(client=client)

# Получение списка всех моделей (требуется настроенный provider)
# all_models = client_models.get_all()
# print(f"All Models: {all_models}")

# Получение списка визуальных моделей (если provider не задан)
vision_models = client_models.get_vision()
print(f"Vision Models: {vision_models}")
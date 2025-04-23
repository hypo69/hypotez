# Модуль `models.py`

## Обзор

Модуль `models.py` предназначен для управления и получения информации о моделях, доступных через различных провайдеров в контексте клиента. Он предоставляет классы и функции для получения списка моделей, моделей компьютерного зрения и мультимедийных моделей.

## Подробней

Модуль содержит класс `ClientModels`, который инициализируется с клиентом и может включать провайдеров для обычных моделей и мультимедийных моделей. Этот класс предоставляет методы для получения моделей по имени, получения всех моделей, моделей компьютерного зрения, а также мультимедийных моделей (изображений и видео). Он использует утилиты `ModelUtils` и `ProviderUtils` для конвертации и получения информации о моделях.

## Классы

### `ClientModels`

**Описание**: Класс `ClientModels` управляет получением списка доступных моделей от различных провайдеров, таких как модели для обработки текста, изображений и видео.

**Атрибуты**:

- `client`: Клиент, используемый для выполнения запросов к провайдерам.
- `provider` (Optional[`ProviderType`]): Провайдер для обычных моделей (например, текстовых). По умолчанию `None`.
- `media_provider` (Optional[`ProviderType`]): Провайдер для мультимедийных моделей (изображения, видео). По умолчанию `None`.

**Методы**:

- `get(name, default=None)`: Возвращает тип провайдера по имени модели или провайдера.
- `get_all(api_key=None, **kwargs)`: Возвращает список всех моделей, доступных у данного провайдера.
- `get_vision(**kwargs)`: Возвращает список моделей компьютерного зрения.
- `get_media(api_key=None, **kwargs)`: Возвращает список мультимедийных моделей.
- `get_image(**kwargs)`: Возвращает список моделей для работы с изображениями.
- `get_video(**kwargs)`: Возвращает список моделей для работы с видео.

### `ClientModels.get`

```python
    def get(self, name, default=None) -> ProviderType:
        """ Функция извлекает провайдера по имени.

        Args:
            name (str): Имя модели или провайдера, для которого требуется получить информацию.
            default (Any, optional): Значение по умолчанию, которое возвращается, если модель или провайдер не найдены. По умолчанию `None`.

        Returns:
            ProviderType: Тип провайдера, соответствующий запрошенному имени, или значение по умолчанию, если ничего не найдено.
        """
        if name in ModelUtils.convert:
            return ModelUtils.convert[name].best_provider
        if name in ProviderUtils.convert:
            return ProviderUtils.convert[name]
        return default
```

**Как работает функция**:

- Функция `get` принимает имя модели или провайдера и возвращает соответствующий тип провайдера.
- Сначала проверяет, есть ли имя в `ModelUtils.convert`. Если да, возвращает `best_provider` для этой модели.
- Если имя не найдено в `ModelUtils.convert`, проверяет, есть ли оно в `ProviderUtils.convert`. Если да, возвращает соответствующего провайдера.
- Если имя не найдено ни в одном из словарей, возвращает значение `default`.

**Примеры**:
```python
#Предположим, что ModelUtils.convert = {"model1": Model(best_provider="provider1")}
#         ProviderUtils.convert = {"provider2": "provider2"}
client_models = ClientModels(client=None)
provider = client_models.get("model1") # вернет "provider1"
provider = client_models.get("provider2") # вернет "provider2"
provider = client_models.get("model3", default="default_provider") # вернет "default_provider"
```

### `ClientModels.get_all`

```python
    def get_all(self, api_key: str = None, **kwargs) -> list[str]:
        """ Функция извлекает все модели, доступные для данного провайдера.

        Args:
            api_key (str, optional): API-ключ для аутентификации у провайдера. По умолчанию `None`.
            **kwargs: Дополнительные аргументы, которые могут потребоваться провайдеру для получения списка моделей.

        Returns:
            list[str]: Список идентификаторов всех доступных моделей.
        """
        if self.provider is None:
            return []
        if api_key is None:
            api_key = self.client.api_key
        return self.provider.get_models(
            **kwargs,
            **{} if api_key is None else {"api_key": api_key}
        )
```

**Как работает функция**:

- Функция `get_all` возвращает список всех моделей, доступных у данного провайдера.
- Сначала проверяет, установлен ли провайдер (`self.provider`). Если нет, возвращает пустой список.
- Если `api_key` не предоставлен, использует `api_key` из клиента.
- Вызывает метод `get_models` у провайдера, передавая все дополнительные аргументы (`kwargs`) и API-ключ (если он предоставлен).

**Примеры**:
```python
#Предположим, что provider.get_models возвращает ["model1", "model2"]
class MockProvider:
    def get_models(self, **kwargs):
        return ["model1", "model2"]

client = type('client', (object,), {'api_key': 'test_key'})()
client_models = ClientModels(client=client, provider=MockProvider())
all_models = client_models.get_all() # вернет ["model1", "model2"]
```

### `ClientModels.get_vision`

```python
    def get_vision(self, **kwargs) -> list[str]:
        """ Функция извлекает все модели компьютерного зрения.

        Args:
            **kwargs: Дополнительные аргументы, которые могут потребоваться провайдеру для получения списка моделей.

        Returns:
            list[str]: Список идентификаторов моделей компьютерного зрения.
        """
        if self.provider is None:
            return [model_id for model_id, model in ModelUtils.convert.items() if isinstance(model, VisionModel)]
        self.get_all(**kwargs)
        if hasattr(self.provider, "vision_models"):
            return self.provider.vision_models
        return []
```

**Как работает функция**:

- Функция `get_vision` возвращает список моделей компьютерного зрения.
- Если провайдер не установлен, функция выполняет итерацию по `ModelUtils.convert` и возвращает все `model_id`, для которых модель является экземпляром `VisionModel`.
- Если провайдер установлен, вызывает `get_all` для обновления списка моделей и проверяет, есть ли у провайдера атрибут `vision_models`. Если да, возвращает значение этого атрибута.

**Примеры**:
```python
#Предположим, что ModelUtils.convert = {"model1": VisionModel(), "model2": object()}
class MockProvider:
    vision_models = ["vision_model1", "vision_model2"]

client_models = ClientModels(client=None, provider=MockProvider())
vision_models = client_models.get_vision() # вернет ["vision_model1", "vision_model2"]
```

### `ClientModels.get_media`

```python
    def get_media(self, api_key: str = None, **kwargs) -> list[str]:
        """ Функция извлекает все мультимедийные модели.

        Args:
            api_key (str, optional): API-ключ для аутентификации у провайдера. По умолчанию `None`.
            **kwargs: Дополнительные аргументы, которые могут потребоваться провайдеру для получения списка моделей.

        Returns:
            list[str]: Список идентификаторов мультимедийных моделей.
        """
        if self.media_provider is None:
            return []
        if api_key is None:
            api_key = self.client.api_key
        return self.media_provider.get_models(
            **kwargs,
            **{} if api_key is None else {"api_key": api_key}
        )
```

**Как работает функция**:

- Функция `get_media` возвращает список мультимедийных моделей.
- Сначала проверяет, установлен ли `media_provider`. Если нет, возвращает пустой список.
- Если `api_key` не предоставлен, использует `api_key` из клиента.
- Вызывает метод `get_models` у `media_provider`, передавая все дополнительные аргументы (`kwargs`) и API-ключ (если он предоставлен).

**Примеры**:
```python
#Предположим, что media_provider.get_models возвращает ["media_model1", "media_model2"]
class MockMediaProvider:
    def get_models(self, **kwargs):
        return ["media_model1", "media_model2"]

client = type('client', (object,), {'api_key': 'test_key'})()
client_models = ClientModels(client=client, media_provider=MockMediaProvider())
media_models = client_models.get_media() # вернет ["media_model1", "media_model2"]
```

### `ClientModels.get_image`

```python
    def get_image(self, **kwargs) -> list[str]:
        """ Функция извлекает все модели для обработки изображений.

        Args:
            **kwargs: Дополнительные аргументы, которые могут потребоваться провайдеру для получения списка моделей.

        Returns:
            list[str]: Список идентификаторов моделей для обработки изображений.
        """
        if self.media_provider is None:
            return [model_id for model_id, model in ModelUtils.convert.items() if isinstance(model, ImageModel)]
        self.get_media(**kwargs)
        if hasattr(self.media_provider, "image_models"):
            return self.media_provider.image_models
        return []
```

**Как работает функция**:

- Функция `get_image` возвращает список моделей для работы с изображениями.
- Если `media_provider` не установлен, функция выполняет итерацию по `ModelUtils.convert` и возвращает все `model_id`, для которых модель является экземпляром `ImageModel`.
- Если `media_provider` установлен, вызывает `get_media` для обновления списка моделей и проверяет, есть ли у провайдера атрибут `image_models`. Если да, возвращает значение этого атрибута.

**Примеры**:
```python
#Предположим, что ModelUtils.convert = {"model1": ImageModel(), "model2": object()}
class MockMediaProvider:
    image_models = ["image_model1", "image_model2"]

client_models = ClientModels(client=None, media_provider=MockMediaProvider())
image_models = client_models.get_image() # вернет ["image_model1", "image_model2"]
```

### `ClientModels.get_video`

```python
    def get_video(self, **kwargs) -> list[str]:
        """ Функция извлекает все модели для обработки видео.

        Args:
            **kwargs: Дополнительные аргументы, которые могут потребоваться провайдеру для получения списка моделей.

        Returns:
            list[str]: Список идентификаторов моделей для обработки видео.
        """
        if self.media_provider is None:
            return []
        self.get_media(**kwargs)
        if hasattr(self.media_provider, "video_models"):
            return self.media_provider.video_models
        return []
```

**Как работает функция**:

- Функция `get_video` возвращает список моделей для работы с видео.
- Если `media_provider` не установлен, возвращает пустой список.
- Вызывает `get_media` для обновления списка моделей и проверяет, есть ли у `media_provider` атрибут `video_models`. Если да, возвращает значение этого атрибута.

**Примеры**:
```python
#Предположим, что media_provider.video_models возвращает ["video_model1", "video_model2"]
class MockMediaProvider:
    video_models = ["video_model1", "video_model2"]

client_models = ClientModels(client=None, media_provider=MockMediaProvider())
video_models = client_models.get_video() # вернет ["video_model1", "video_model2"]
```
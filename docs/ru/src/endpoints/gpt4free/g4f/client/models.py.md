# Модуль для управления моделями клиентов

## Обзор

Модуль `models.py` предназначен для управления и получения информации о моделях, доступных для клиента, включая текстовые, визуальные и медиа-модели. Он предоставляет интерфейс для взаимодействия с различными поставщиками моделей, такими как GPT4Free, и получения списка доступных моделей в зависимости от типа поставщика.

## Подробней

Этот модуль содержит класс `ClientModels`, который инкапсулирует логику получения и фильтрации моделей. Он использует классы `ModelUtils`, `ImageModel`, `VisionModel`, `ProviderUtils` и `ProviderType` из других модулей для определения типов моделей и поставщиков.
Расположение файла в проекте `hypotez/src/endpoints/gpt4free/g4f/client/models.py` говорит о том, что он является частью клиентского API для gpt4free, отвечающего за выбор и предоставление моделей.

## Классы

### `ClientModels`

**Описание**: Класс `ClientModels` управляет моделями, доступными для клиента, и предоставляет методы для их получения и фильтрации.

**Принцип работы**: Класс инициализируется с экземпляром клиента и, опционально, типами поставщиков для основных и медиа-моделей. Он предоставляет методы для получения конкретных моделей, всех моделей, визуальных моделей и медиа-моделей в зависимости от поставщика и доступных API-ключей.

**Аттрибуты**:

- `client`: Экземпляр клиента, используемый для выполнения запросов к API.
- `provider` (Optional[`ProviderType`]): Тип поставщика для основных моделей (например, текстовых).
- `media_provider` (Optional[`ProviderType`]): Тип поставщика для медиа-моделей (например, изображений и видео).

**Методы**:

- `get(name, default=None)`: Возвращает тип поставщика для заданной модели или поставщика.
- `get_all(api_key: str = None, **kwargs)`: Возвращает список всех доступных моделей от заданного поставщика.
- `get_vision(**kwargs)`: Возвращает список vision-моделей от заданного поставщика.
- `get_media(api_key: str = None, **kwargs)`: Возвращает список media-моделей от заданного поставщика.
- `get_image(**kwargs)`: Возвращает список image-моделей от заданного поставщика.
- `get_video(**kwargs)`: Возвращает список video-моделей от заданного поставщика.

## Функции

### `__init__`

```python
def __init__(self, client, provider: ProviderType = None, media_provider: ProviderType = None):
    """
    Инициализирует экземпляр класса `ClientModels`.

    Args:
        client: Экземпляр клиента, используемый для выполнения запросов к API.
        provider (Optional[ProviderType], optional): Тип поставщика для основных моделей. По умолчанию `None`.
        media_provider (Optional[ProviderType], optional): Тип поставщика для медиа-моделей. По умолчанию `None`.
    """
    ...
```

**Назначение**: Инициализация объекта `ClientModels` с указанием клиента и поставщиков моделей.

**Параметры**:

- `client`: Экземпляр клиента, который будет использоваться для запросов к API.
- `provider` (Optional[`ProviderType`]): Тип поставщика для основных моделей (текстовых). По умолчанию `None`.
- `media_provider` (Optional[`ProviderType`]): Тип поставщика для медиа-моделей (изображений и видео). По умолчанию `None`.

**Как работает функция**:
1. Функция `__init__` принимает экземпляр клиента, а также необязательные типы поставщиков для основных и медиа-моделей.
2.  Присваивает значения атрибутам `self.client`, `self.provider` и `self.media_provider` для сохранения переданных значений.

**Примеры**:

```python
from ..Provider import ProviderUtils
from ..providers.types import ProviderType

class MockClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key

# Создание экземпляра ClientModels с клиентом и поставщиком
client = MockClient(api_key="test_api_key")
provider = ProviderType("test_provider")
media_provider = ProviderType("test_media_provider")

client_models = ClientModels(client=client, provider=provider, media_provider=media_provider)

# Проверка атрибутов
assert client_models.client == client
assert client_models.provider == provider
assert client_models.media_provider == media_provider

# Создание экземпляра ClientModels только с клиентом
client_models = ClientModels(client=client)

# Проверка атрибутов
assert client_models.client == client
assert client_models.provider is None
assert client_models.media_provider is None
```

### `get`

```python
def get(self, name, default=None) -> ProviderType:
    """
    Получает тип поставщика для заданной модели или поставщика.

    Args:
        name: Имя модели или поставщика.
        default: Значение по умолчанию, если модель или поставщик не найдены.

    Returns:
        ProviderType: Тип поставщика для заданной модели или поставщика, или значение по умолчанию, если не найдено.
    """
    ...
```

**Назначение**: Получение типа поставщика для заданной модели или поставщика.

**Параметры**:

- `name`: Имя модели или поставщика, для которого требуется получить тип поставщика.
- `default`: Значение по умолчанию, которое будет возвращено, если модель или поставщик не найдены. По умолчанию `None`.

**Возвращает**:

- `ProviderType`: Тип поставщика для заданной модели или поставщика, или значение по умолчанию, если не найдено.

**Как работает функция**:

1.  Функция `get` принимает имя модели или поставщика (`name`) и необязательное значение по умолчанию (`default`).
2.  Проверяет, содержится ли `name` в `ModelUtils.convert`. Если да, возвращает `best_provider` из `ModelUtils.convert[name]`.
3.  Если `name` не найден в `ModelUtils.convert`, проверяет, содержится ли `name` в `ProviderUtils.convert`. Если да, возвращает `ProviderUtils.convert[name]`.
4.  Если `name` не найден ни в `ModelUtils.convert`, ни в `ProviderUtils.convert`, возвращает значение `default`.

**Примеры**:

```python
from ..Provider import ProviderUtils
from ..providers.types import ProviderType
from ..models import ModelUtils

class MockClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key

# Mock ModelUtils.convert и ProviderUtils.convert для тестирования
ModelUtils.convert = {"model1": Mock()}
ModelUtils.convert["model1"].best_provider = "provider1"
ProviderUtils.convert = {"provider2": "provider_type2"}

# Создание экземпляра ClientModels с клиентом
client = MockClient(api_key="test_api_key")
client_models = ClientModels(client=client)

# Тестирование получения поставщика для модели
provider = client_models.get("model1")
assert provider == "provider1"

# Тестирование получения поставщика для поставщика
provider = client_models.get("provider2")
assert provider == "provider_type2"

# Тестирование получения поставщика с значением по умолчанию
provider = client_models.get("nonexistent", default="default_value")
assert provider == "default_value"

# Тестирование получения поставщика без значения по умолчанию
provider = client_models.get("nonexistent")
assert provider is None
```

### `get_all`

```python
def get_all(self, api_key: str = None, **kwargs) -> list[str]:
    """
    Возвращает список всех доступных моделей от заданного поставщика.

    Args:
        api_key (Optional[str], optional): API ключ для аутентификации. По умолчанию `None`.
        **kwargs: Дополнительные аргументы, передаваемые в `get_models` метод поставщика.

    Returns:
        list[str]: Список доступных моделей от заданного поставщика.
    """
    ...
```

**Назначение**: Получение списка всех доступных моделей от заданного поставщика.

**Параметры**:

- `api_key` (Optional[str]): API-ключ для аутентификации. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы, передаваемые в метод `get_models` поставщика.

**Возвращает**:

- `list[str]`: Список доступных моделей от заданного поставщика.

**Как работает функция**:

1.  Функция `get_all` принимает необязательный API-ключ (`api_key`) и дополнительные аргументы (`**kwargs`).
2.  Если `self.provider` равен `None`, возвращает пустой список.
3.  Если `api_key` равен `None`, использует `self.client.api_key`.
4.  Вызывает метод `get_models` поставщика (`self.provider.get_models`) с переданными аргументами и, если `api_key` не равен `None`, добавляет его в аргументы.
5.  Возвращает список моделей, полученный от `self.provider.get_models`.

**Примеры**:

```python
from ..Provider import ProviderUtils
from ..providers.types import ProviderType

class MockClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key

class MockProvider:
    def get_models(self, **kwargs):
        return ["model1", "model2"]

# Создание экземпляра ClientModels с клиентом и поставщиком
client = MockClient(api_key="test_api_key")
provider = MockProvider()

client_models = ClientModels(client=client, provider=provider)

# Тестирование получения всех моделей с API-ключом из клиента
models = client_models.get_all()
assert models == ["model1", "model2"]

# Тестирование получения всех моделей с переданным API-ключом
models = client_models.get_all(api_key="override_api_key")
assert models == ["model1", "model2"]

# Тестирование получения всех моделей без поставщика
client_models.provider = None
models = client_models.get_all()
assert models == []
```

### `get_vision`

```python
def get_vision(self, **kwargs) -> list[str]:
    """
    Возвращает список vision-моделей от заданного поставщика.

    Args:
        **kwargs: Дополнительные аргументы, передаваемые в `get_all` метод или проверяемые на наличие `vision_models` атрибута.

    Returns:
        list[str]: Список vision-моделей от заданного поставщика.
    """
    ...
```

**Назначение**: Получение списка vision-моделей (моделей компьютерного зрения) от заданного поставщика.

**Параметры**:

- `**kwargs`: Дополнительные аргументы, передаваемые в метод `get_all` или проверяемые на наличие атрибута `vision_models` у поставщика.

**Возвращает**:

- `list[str]`: Список vision-моделей от заданного поставщика.

**Как работает функция**:

1.  Функция `get_vision` принимает дополнительные аргументы (`**kwargs`).
2.  Если `self.provider` равен `None`, возвращает список `model_id` для всех `model_id, model` из `ModelUtils.convert`, где `model` является экземпляром `VisionModel`.
3.  Вызывает метод `get_all` с переданными аргументами.
4.  Если у `self.provider` есть атрибут `vision_models`, возвращает его значение.
5.  Если у `self.provider` нет атрибута `vision_models`, возвращает пустой список.

**Примеры**:

```python
from ..Provider import ProviderUtils
from ..providers.types import ProviderType
from ..models import ModelUtils, VisionModel

class MockClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key

class MockProvider:
    def __init__(self):
        self.vision_models = ["vision_model1", "vision_model2"]

    def get_models(self, **kwargs):
        return []

# Создание экземпляра ClientModels с клиентом и поставщиком
client = MockClient(api_key="test_api_key")
provider = MockProvider()

client_models = ClientModels(client=client, provider=provider)

# Mock ModelUtils.convert для тестирования
ModelUtils.convert = {"model1": VisionModel(), "model2": Mock()}

# Тестирование получения vision-моделей с поставщиком
vision_models = client_models.get_vision()
assert vision_models == ["vision_model1", "vision_model2"]

# Тестирование получения vision-моделей без поставщика
client_models.provider = None
vision_models = client_models.get_vision()
assert vision_models == ["model1"]

# Тестирование получения vision-моделей без vision_models у поставщика
class MockProviderWithoutVisionModels:
    def get_models(self, **kwargs):
        return []

client_models.provider = MockProviderWithoutVisionModels()
vision_models = client_models.get_vision()
assert vision_models == []
```

### `get_media`

```python
def get_media(self, api_key: str = None, **kwargs) -> list[str]:
    """
    Возвращает список media-моделей от заданного поставщика.

    Args:
        api_key (Optional[str], optional): API ключ для аутентификации. По умолчанию `None`.
        **kwargs: Дополнительные аргументы, передаваемые в `get_models` метод поставщика.

    Returns:
        list[str]: Список media-моделей от заданного поставщика.
    """
    ...
```

**Назначение**: Получение списка media-моделей от заданного поставщика.

**Параметры**:

- `api_key` (Optional[str]): API-ключ для аутентификации. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы, передаваемые в метод `get_models` поставщика.

**Возвращает**:

- `list[str]`: Список media-моделей от заданного поставщика.

**Как работает функция**:

1.  Функция `get_media` принимает необязательный API-ключ (`api_key`) и дополнительные аргументы (`**kwargs`).
2.  Если `self.media_provider` равен `None`, возвращает пустой список.
3.  Если `api_key` равен `None`, использует `self.client.api_key`.
4.  Вызывает метод `get_models` медиа-поставщика (`self.media_provider.get_models`) с переданными аргументами и, если `api_key` не равен `None`, добавляет его в аргументы.
5.  Возвращает список моделей, полученный от `self.media_provider.get_models`.

**Примеры**:

```python
from ..Provider import ProviderUtils
from ..providers.types import ProviderType

class MockClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key

class MockMediaProvider:
    def get_models(self, **kwargs):
        return ["media_model1", "media_model2"]

# Создание экземпляра ClientModels с клиентом и медиа-поставщиком
client = MockClient(api_key="test_api_key")
media_provider = MockMediaProvider()

client_models = ClientModels(client=client, media_provider=media_provider)

# Тестирование получения media-моделей с API-ключом из клиента
media_models = client_models.get_media()
assert media_models == ["media_model1", "media_model2"]

# Тестирование получения media-моделей с переданным API-ключом
media_models = client_models.get_media(api_key="override_api_key")
assert media_models == ["media_model1", "media_model2"]

# Тестирование получения media-моделей без медиа-поставщика
client_models.media_provider = None
media_models = client_models.get_media()
assert media_models == []
```

### `get_image`

```python
def get_image(self, **kwargs) -> list[str]:
    """
    Возвращает список image-моделей от заданного поставщика.

    Args:
        **kwargs: Дополнительные аргументы, передаваемые в `get_media` метод или проверяемые на наличие `image_models` атрибута.

    Returns:
        list[str]: Список image-моделей от заданного поставщика.
    """
    ...
```

**Назначение**: Получение списка image-моделей (моделей для обработки изображений) от заданного поставщика.

**Параметры**:

- `**kwargs`: Дополнительные аргументы, передаваемые в метод `get_media` или проверяемые на наличие атрибута `image_models` у медиа-поставщика.

**Возвращает**:

- `list[str]`: Список image-моделей от заданного поставщика.

**Как работает функция**:

1.  Функция `get_image` принимает дополнительные аргументы (`**kwargs`).
2.  Если `self.media_provider` равен `None`, возвращает список `model_id` для всех `model_id, model` из `ModelUtils.convert`, где `model` является экземпляром `ImageModel`.
3.  Вызывает метод `get_media` с переданными аргументами.
4.  Если у `self.media_provider` есть атрибут `image_models`, возвращает его значение.
5.  Если у `self.media_provider` нет атрибута `image_models`, возвращает пустой список.

**Примеры**:

```python
from ..Provider import ProviderUtils
from ..providers.types import ProviderType
from ..models import ModelUtils, ImageModel

class MockClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key

class MockMediaProvider:
    def __init__(self):
        self.image_models = ["image_model1", "image_model2"]

    def get_models(self, **kwargs):
        return []

# Создание экземпляра ClientModels с клиентом и медиа-поставщиком
client = MockClient(api_key="test_api_key")
media_provider = MockMediaProvider()

client_models = ClientModels(client=client, media_provider=media_provider)

# Mock ModelUtils.convert для тестирования
ModelUtils.convert = {"model1": ImageModel(), "model2": Mock()}

# Тестирование получения image-моделей с медиа-поставщиком
image_models = client_models.get_image()
assert image_models == ["image_model1", "image_model2"]

# Тестирование получения image-моделей без медиа-поставщика
client_models.media_provider = None
image_models = client_models.get_image()
assert image_models == ["model1"]

# Тестирование получения image-моделей без image_models у медиа-поставщика
class MockMediaProviderWithoutImageModels:
    def get_models(self, **kwargs):
        return []

client_models.media_provider = MockMediaProviderWithoutImageModels()
image_models = client_models.get_image()
assert image_models == []
```

### `get_video`

```python
def get_video(self, **kwargs) -> list[str]:
    """
    Возвращает список video-моделей от заданного поставщика.

    Args:
        **kwargs: Дополнительные аргументы, передаваемые в `get_media` метод или проверяемые на наличие `video_models` атрибута.

    Returns:
        list[str]: Список video-моделей от заданного поставщика.
    """
    ...
```

**Назначение**: Получение списка video-моделей (моделей для обработки видео) от заданного поставщика.

**Параметры**:

- `**kwargs`: Дополнительные аргументы, передаваемые в метод `get_media` или проверяемые на наличие атрибута `video_models` у медиа-поставщика.

**Возвращает**:

- `list[str]`: Список video-моделей от заданного поставщика.

**Как работает функция**:

1.  Функция `get_video` принимает дополнительные аргументы (`**kwargs`).
2.  Если `self.media_provider` равен `None`, возвращает пустой список.
3.  Вызывает метод `get_media` с переданными аргументами.
4.  Если у `self.media_provider` есть атрибут `video_models`, возвращает его значение.
5.  Если у `self.media_provider` нет атрибута `video_models`, возвращает пустой список.

**Примеры**:

```python
from ..Provider import ProviderUtils
from ..providers.types import ProviderType

class MockClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key

class MockMediaProvider:
    def __init__(self):
        self.video_models = ["video_model1", "video_model2"]

    def get_models(self, **kwargs):
        return []

# Создание экземпляра ClientModels с клиентом и медиа-поставщиком
client = MockClient(api_key="test_api_key")
media_provider = MockMediaProvider()

client_models = ClientModels(client=client, media_provider=media_provider)

# Тестирование получения video-моделей с медиа-поставщиком
video_models = client_models.get_video()
assert video_models == ["video_model1", "video_model2"]

# Тестирование получения video-моделей без медиа-поставщика
client_models.media_provider = None
video_models = client_models.get_video()
assert video_models == []

# Тестирование получения video-моделей без video_models у медиа-поставщика
class MockMediaProviderWithoutVideoModels:
    def get_models(self, **kwargs):
        return []

client_models.media_provider = MockMediaProviderWithoutVideoModels()
video_models = client_models.get_video()
assert video_models == []
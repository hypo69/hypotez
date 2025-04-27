# Модуль моделей для GPT4Free

## Обзор

Модуль `models.py` предоставляет класс `ClientModels`, который используется для взаимодействия с различными моделями GPT4Free. 
Класс позволяет получить список доступных моделей, моделей для обработки изображений, видео и других типов данных, а также 
извлечь информацию о конкретной модели.

## Детали

Модуль `models.py` использует класс `ClientModels` для работы с различными моделями GPT4Free, которые доступны через API. 
Он позволяет определить тип провайдера (например, `ProviderType.G4F_VISION` или `ProviderType.G4F_MEDIA`) и, используя 
методы класса, получить список доступных моделей, моделей для обработки изображений, видео и других типов данных.

## Классы

### `ClientModels`

**Описание**: Класс `ClientModels` предоставляет набор методов для работы с моделями GPT4Free.

**Атрибуты**:

- `client`: Объект клиента GPT4Free.
- `provider`: Тип провайдера для работы с моделями GPT4Free.
- `media_provider`: Тип провайдера для работы с медиа-моделями (например, модели для обработки изображений и видео).

**Методы**:

- `get(name, default=None) -> ProviderType`: Возвращает тип провайдера для заданного имени модели.
- `get_all(api_key: str = None, **kwargs) -> list[str]`: Возвращает список доступных моделей для заданного провайдера.
- `get_vision(**kwargs) -> list[str]`: Возвращает список моделей для обработки изображений.
- `get_media(api_key: str = None, **kwargs) -> list[str]`: Возвращает список моделей для работы с медиа-данными.
- `get_image(**kwargs) -> list[str]`: Возвращает список моделей для обработки изображений.
- `get_video(**kwargs) -> list[str]`: Возвращает список моделей для обработки видео.

## Функции

### `get(name, default=None) -> ProviderType`

**Цель**: Возвращает тип провайдера для заданного имени модели.

**Параметры**:

- `name` (str): Имя модели.
- `default` (Any): Значение по умолчанию, если модель не найдена.

**Возвращает**:

- `ProviderType`: Тип провайдера для заданной модели.

**Пример**:

```python
from hypotez.src.endpoints.gpt4free.g4f.client.models import ClientModels

# Создаем экземпляр ClientModels
models = ClientModels(client)

# Получаем тип провайдера для модели 'text-davinci-003'
provider_type = models.get('text-davinci-003')

# Выводим тип провайдера
print(provider_type)
```

### `get_all(api_key: str = None, **kwargs) -> list[str]`

**Цель**: Возвращает список доступных моделей для заданного провайдера.

**Параметры**:

- `api_key` (str): Ключ API для доступа к моделям.
- `**kwargs`: Дополнительные аргументы для запроса к API.

**Возвращает**:

- `list[str]`: Список доступных моделей.

**Пример**:

```python
from hypotez.src.endpoints.gpt4free.g4f.client.models import ClientModels

# Создаем экземпляр ClientModels
models = ClientModels(client)

# Получаем список доступных моделей
available_models = models.get_all(api_key='your_api_key')

# Выводим список моделей
print(available_models)
```

### `get_vision(**kwargs) -> list[str]`

**Цель**: Возвращает список моделей для обработки изображений.

**Параметры**:

- `**kwargs`: Дополнительные аргументы для запроса к API.

**Возвращает**:

- `list[str]`: Список моделей для обработки изображений.

**Пример**:

```python
from hypotez.src.endpoints.gpt4free.g4f.client.models import ClientModels

# Создаем экземпляр ClientModels
models = ClientModels(client)

# Получаем список моделей для обработки изображений
vision_models = models.get_vision()

# Выводим список моделей
print(vision_models)
```

### `get_media(api_key: str = None, **kwargs) -> list[str]`

**Цель**: Возвращает список моделей для работы с медиа-данными.

**Параметры**:

- `api_key` (str): Ключ API для доступа к моделям.
- `**kwargs`: Дополнительные аргументы для запроса к API.

**Возвращает**:

- `list[str]`: Список моделей для работы с медиа-данными.

**Пример**:

```python
from hypotez.src.endpoints.gpt4free.g4f.client.models import ClientModels

# Создаем экземпляр ClientModels
models = ClientModels(client)

# Получаем список моделей для работы с медиа-данными
media_models = models.get_media(api_key='your_api_key')

# Выводим список моделей
print(media_models)
```

### `get_image(**kwargs) -> list[str]`

**Цель**: Возвращает список моделей для обработки изображений.

**Параметры**:

- `**kwargs`: Дополнительные аргументы для запроса к API.

**Возвращает**:

- `list[str]`: Список моделей для обработки изображений.

**Пример**:

```python
from hypotez.src.endpoints.gpt4free.g4f.client.models import ClientModels

# Создаем экземпляр ClientModels
models = ClientModels(client)

# Получаем список моделей для обработки изображений
image_models = models.get_image()

# Выводим список моделей
print(image_models)
```

### `get_video(**kwargs) -> list[str]`

**Цель**: Возвращает список моделей для обработки видео.

**Параметры**:

- `**kwargs`: Дополнительные аргументы для запроса к API.

**Возвращает**:

- `list[str]`: Список моделей для обработки видео.

**Пример**:

```python
from hypotez.src.endpoints.gpt4free.g4f.client.models import ClientModels

# Создаем экземпляр ClientModels
models = ClientModels(client)

# Получаем список моделей для обработки видео
video_models = models.get_video()

# Выводим список моделей
print(video_models)
```

## Примечания

- Все методы класса `ClientModels` используют API GPT4Free для получения информации о моделях.
- Модуль `models.py` использует модули `ModelUtils`, `ImageModel`, `VisionModel` и `ProviderUtils` для определения типов моделей и 
провайдеров.
- Для работы с API GPT4Free требуется ключ API, который можно получить на сайте GPT4Free.

## Как работает код

Этот модуль позволяет получить доступ к моделям GPT4Free через API. Класс `ClientModels` предоставляет методы для получения списка 
доступных моделей, моделей для обработки изображений, видео и других типов данных, а также для получения информации о конкретной модели.

## Примеры

```python
from hypotez.src.endpoints.gpt4free.g4f.client.models import ClientModels
from hypotez.src.endpoints.gpt4free.g4f.client.client import Client

# Создаем объект клиента GPT4Free
client = Client(api_key='your_api_key')

# Создаем экземпляр ClientModels
models = ClientModels(client)

# Получаем список доступных моделей
available_models = models.get_all()
print(f'Available models: {available_models}')

# Получаем список моделей для обработки изображений
vision_models = models.get_vision()
print(f'Vision models: {vision_models}')

# Получаем список моделей для работы с медиа-данными
media_models = models.get_media()
print(f'Media models: {media_models}')

# Получаем тип провайдера для модели 'text-davinci-003'
provider_type = models.get('text-davinci-003')
print(f'Provider type for model "text-davinci-003": {provider_type}')
```
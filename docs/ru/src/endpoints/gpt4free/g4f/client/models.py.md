# Модуль `models.py`

## Обзор

Модуль `models.py` предназначен для управления моделями, используемыми клиентом, включая получение, фильтрацию и предоставление информации о доступных моделях от различных провайдеров, таких как GPT4Free. Модуль содержит класс `ClientModels`, который инкапсулирует логику для работы с моделями и провайдерами.

## Подробней

Модуль предоставляет методы для получения моделей по имени, получения всех доступных моделей, а также фильтрации моделей по типу (например, vision, media, image, video). Он использует утилиты `ModelUtils` и `ProviderUtils` для преобразования и получения информации о моделях и провайдерах.
Класс `ClientModels` инициализируется с клиентом и, возможно, с указанными провайдерами для основных моделей и медиа-моделей.

## Классы

### `ClientModels`

**Описание**: Класс `ClientModels` управляет моделями, используемыми клиентом, и предоставляет методы для получения информации о доступных моделях от различных провайдеров.

**Принцип работы**:
Класс `ClientModels` инициализируется с клиентом и, возможно, с указанными провайдерами для основных моделей и медиа-моделей. Он предоставляет методы для получения моделей по имени, получения всех доступных моделей, а также фильтрации моделей по типу.

**Аттрибуты**:
- `client`: Клиент, использующий модели.
- `provider` (ProviderType, optional): Провайдер основных моделей. По умолчанию `None`.
- `media_provider` (ProviderType, optional): Провайдер медиа-моделей. По умолчанию `None`.

**Методы**: 
- `get(name, default=None)`: Получает провайдера по имени модели.
- `get_all(api_key: str = None, **kwargs)`: Получает список всех доступных моделей от провайдера.
- `get_vision(**kwargs)`: Получает список vision-моделей.
- `get_media(api_key: str = None, **kwargs)`: Получает список медиа-моделей.
- `get_image(**kwargs)`: Получает список image-моделей.
- `get_video(**kwargs)`: Получает список video-моделей.

## Функции

### `get`

```python
def get(self, name, default=None) -> ProviderType:
    """
    Получает провайдера по имени модели.

    Args:
        name: Имя модели.
        default: Значение по умолчанию, если модель не найдена.

    Returns:
        ProviderType: Провайдер модели или значение по умолчанию.
    """
    ...
```

**Назначение**:
Функция `get` используется для получения провайдера, связанного с указанным именем модели. Она проверяет, существует ли модель в `ModelUtils.convert` или `ProviderUtils.convert`, и возвращает соответствующего провайдера.

**Параметры**:
- `name`: Имя модели, для которой нужно получить провайдера.
- `default`: Значение, которое будет возвращено, если модель не найдена. По умолчанию `None`.

**Возвращает**:
- `ProviderType`: Провайдер, связанный с указанным именем модели. Если модель не найдена, возвращается значение `default`.

**Как работает функция**:
1. Проверяет, есть ли `name` в словаре `ModelUtils.convert`. Если есть, возвращает `best_provider` для этой модели.
2. Если `name` нет в `ModelUtils.convert`, проверяет, есть ли `name` в словаре `ProviderUtils.convert`. Если есть, возвращает соответствующего провайдера.
3. Если `name` нет ни в одном из словарей, возвращает значение `default`.

**ASCII flowchart**:
```
A: Проверяем name в ModelUtils.convert
|
B: name есть в ModelUtils.convert?
| Yes
C: Возвращаем ModelUtils.convert[name].best_provider
| No
D: Проверяем name в ProviderUtils.convert
|
E: name есть в ProviderUtils.convert?
| Yes
F: Возвращаем ProviderUtils.convert[name]
| No
G: Возвращаем default
```

**Примеры**:

```python
# Пример получения провайдера для модели, существующей в ModelUtils.convert
provider = client_models.get("gpt-3.5-turbo")

# Пример получения провайдера для модели, существующей в ProviderUtils.convert
provider = client_models.get("openai")

# Пример получения провайдера для модели, не существующей ни в ModelUtils.convert, ни в ProviderUtils.convert
provider = client_models.get("unknown_model", default="default_provider")
```

### `get_all`

```python
def get_all(self, api_key: str = None, **kwargs) -> list[str]:
    """
    Получает список всех доступных моделей от провайдера.

    Args:
        api_key (str, optional): API ключ для провайдера. По умолчанию `None`.
        **kwargs: Дополнительные аргументы для передачи провайдеру.

    Returns:
        list[str]: Список идентификаторов моделей.
    """
    ...
```

**Назначение**:
Функция `get_all` используется для получения списка всех доступных моделей от указанного провайдера. Она принимает API ключ и дополнительные аргументы, которые передаются провайдеру при запросе моделей.

**Параметры**:
- `api_key` (str, optional): API ключ для аутентификации у провайдера. Если не указан, используется `self.client.api_key`. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы, которые будут переданы в метод `get_models` провайдера.

**Возвращает**:
- `list[str]`: Список идентификаторов доступных моделей.

**Как работает функция**:
1. Проверяет, установлен ли провайдер (`self.provider`). Если нет, возвращает пустой список.
2. Если `api_key` не указан, использует `self.client.api_key`.
3. Вызывает метод `get_models` у провайдера, передавая `kwargs` и `api_key` (если он указан).
4. Возвращает список идентификаторов моделей, полученных от провайдера.

**ASCII flowchart**:
```
A: Проверяем, установлен ли self.provider
|
B: self.provider установлен?
| Yes
C: Проверяем, указан ли api_key
|
D: api_key указан?
| Yes
E: Используем api_key
| No
F: Используем self.client.api_key
|
G: Вызываем self.provider.get_models(**kwargs, api_key=api_key)
|
H: Возвращаем список моделей
```

**Примеры**:

```python
# Пример получения всех моделей без указания API ключа
models = client_models.get_all()

# Пример получения всех моделей с указанием API ключа и дополнительных параметров
models = client_models.get_all(api_key="YOUR_API_KEY", param1="value1", param2="value2")
```

### `get_vision`

```python
def get_vision(self, **kwargs) -> list[str]:
    """
    Получает список vision-моделей.

    Args:
        **kwargs: Дополнительные аргументы для передачи в `get_all`.

    Returns:
        list[str]: Список идентификаторов vision-моделей.
    """
    ...
```

**Назначение**:
Функция `get_vision` используется для получения списка vision-моделей. Она проверяет, установлен ли провайдер, и возвращает список vision-моделей либо из `ModelUtils.convert`, либо из атрибута `vision_models` провайдера.

**Параметры**:
- `**kwargs`: Дополнительные аргументы для передачи в метод `get_all`.

**Возвращает**:
- `list[str]`: Список идентификаторов vision-моделей.

**Как работает функция**:
1. Проверяет, установлен ли провайдер (`self.provider`).
2. Если провайдер не установлен, возвращает список идентификаторов моделей, которые являются экземплярами класса `VisionModel` в `ModelUtils.convert`.
3. Если провайдер установлен, вызывает метод `get_all` с переданными `kwargs`.
4. Проверяет, есть ли у провайдера атрибут `vision_models`. Если есть, возвращает значение этого атрибута.
5. Если атрибута `vision_models` нет, возвращает пустой список.

**ASCII flowchart**:
```
A: Проверяем, установлен ли self.provider
|
B: self.provider установлен?
| Yes
C: Вызываем self.get_all(**kwargs)
|
D: Проверяем, есть ли у self.provider атрибут vision_models
|
E: Атрибут vision_models есть?
| Yes
F: Возвращаем self.provider.vision_models
| No
G: Возвращаем []
| No
H: Возвращаем [model_id for model_id, model in ModelUtils.convert.items() if isinstance(model, VisionModel)]
```

**Примеры**:

```python
# Пример получения vision-моделей без дополнительных параметров
vision_models = client_models.get_vision()

# Пример получения vision-моделей с дополнительными параметрами
vision_models = client_models.get_vision(param1="value1", param2="value2")
```

### `get_media`

```python
def get_media(self, api_key: str = None, **kwargs) -> list[str]:
    """
    Получает список медиа-моделей.

    Args:
        api_key (str, optional): API ключ для провайдера. По умолчанию `None`.
        **kwargs: Дополнительные аргументы для передачи в `get_all`.

    Returns:
        list[str]: Список идентификаторов медиа-моделей.
    """
    ...
```

**Назначение**:
Функция `get_media` используется для получения списка медиа-моделей от указанного провайдера. Она принимает API ключ и дополнительные аргументы, которые передаются провайдеру при запросе моделей.

**Параметры**:
- `api_key` (str, optional): API ключ для аутентификации у провайдера. Если не указан, используется `self.client.api_key`. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы, которые будут переданы в метод `get_models` провайдера.

**Возвращает**:
- `list[str]`: Список идентификаторов медиа-моделей.

**Как работает функция**:
1. Проверяет, установлен ли медиа-провайдер (`self.media_provider`). Если нет, возвращает пустой список.
2. Если `api_key` не указан, использует `self.client.api_key`.
3. Вызывает метод `get_models` у медиа-провайдера, передавая `kwargs` и `api_key` (если он указан).
4. Возвращает список идентификаторов моделей, полученных от медиа-провайдера.

**ASCII flowchart**:
```
A: Проверяем, установлен ли self.media_provider
|
B: self.media_provider установлен?
| Yes
C: Проверяем, указан ли api_key
|
D: api_key указан?
| Yes
E: Используем api_key
| No
F: Используем self.client.api_key
|
G: Вызываем self.media_provider.get_models(**kwargs, api_key=api_key)
|
H: Возвращаем список моделей
```

**Примеры**:

```python
# Пример получения всех медиа-моделей без указания API ключа
media_models = client_models.get_media()

# Пример получения всех медиа-моделей с указанием API ключа и дополнительных параметров
media_models = client_models.get_media(api_key="YOUR_API_KEY", param1="value1", param2="value2")
```

### `get_image`

```python
def get_image(self, **kwargs) -> list[str]:
    """
    Получает список image-моделей.

    Args:
        **kwargs: Дополнительные аргументы для передачи в `get_media`.

    Returns:
        list[str]: Список идентификаторов image-моделей.
    """
    ...
```

**Назначение**:
Функция `get_image` используется для получения списка image-моделей. Она проверяет, установлен ли медиа-провайдер, и возвращает список image-моделей либо из `ModelUtils.convert`, либо из атрибута `image_models` медиа-провайдера.

**Параметры**:
- `**kwargs`: Дополнительные аргументы для передачи в метод `get_media`.

**Возвращает**:
- `list[str]`: Список идентификаторов image-моделей.

**Как работает функция**:
1. Проверяет, установлен ли медиа-провайдер (`self.media_provider`).
2. Если медиа-провайдер не установлен, возвращает список идентификаторов моделей, которые являются экземплярами класса `ImageModel` в `ModelUtils.convert`.
3. Если медиа-провайдер установлен, вызывает метод `get_media` с переданными `kwargs`.
4. Проверяет, есть ли у медиа-провайдера атрибут `image_models`. Если есть, возвращает значение этого атрибута.
5. Если атрибута `image_models` нет, возвращает пустой список.

**ASCII flowchart**:
```
A: Проверяем, установлен ли self.media_provider
|
B: self.media_provider установлен?
| Yes
C: Вызываем self.get_media(**kwargs)
|
D: Проверяем, есть ли у self.media_provider атрибут image_models
|
E: Атрибут image_models есть?
| Yes
F: Возвращаем self.media_provider.image_models
| No
G: Возвращаем []
| No
H: Возвращаем [model_id for model_id, model in ModelUtils.convert.items() if isinstance(model, ImageModel)]
```

**Примеры**:

```python
# Пример получения image-моделей без дополнительных параметров
image_models = client_models.get_image()

# Пример получения image-моделей с дополнительными параметрами
image_models = client_models.get_image(param1="value1", param2="value2")
```

### `get_video`

```python
def get_video(self, **kwargs) -> list[str]:
    """
    Получает список video-моделей.

    Args:
        **kwargs: Дополнительные аргументы для передачи в `get_media`.

    Returns:
        list[str]: Список идентификаторов video-моделей.
    """
    ...
```

**Назначение**:
Функция `get_video` используется для получения списка video-моделей. Она проверяет, установлен ли медиа-провайдер, и возвращает список video-моделей из атрибута `video_models` медиа-провайдера.

**Параметры**:
- `**kwargs`: Дополнительные аргументы для передачи в метод `get_media`.

**Возвращает**:
- `list[str]`: Список идентификаторов video-моделей.

**Как работает функция**:
1. Проверяет, установлен ли медиа-провайдер (`self.media_provider`).
2. Если медиа-провайдер не установлен, возвращает пустой список.
3. Если медиа-провайдер установлен, вызывает метод `get_media` с переданными `kwargs`.
4. Проверяет, есть ли у медиа-провайдера атрибут `video_models`. Если есть, возвращает значение этого атрибута.
5. Если атрибута `video_models` нет, возвращает пустой список.

**ASCII flowchart**:
```
A: Проверяем, установлен ли self.media_provider
|
B: self.media_provider установлен?
| Yes
C: Вызываем self.get_media(**kwargs)
|
D: Проверяем, есть ли у self.media_provider атрибут video_models
|
E: Атрибут video_models есть?
| Yes
F: Возвращаем self.media_provider.video_models
| No
G: Возвращаем []
```

**Примеры**:

```python
# Пример получения video-моделей без дополнительных параметров
video_models = client_models.get_video()

# Пример получения video-моделей с дополнительными параметрами
video_models = client_models.get_video(param1="value1", param2="value2")
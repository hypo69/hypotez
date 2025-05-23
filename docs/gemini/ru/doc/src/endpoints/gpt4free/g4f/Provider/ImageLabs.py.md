# Модуль ImageLabs

## Обзор

Модуль `ImageLabs` представляет собой провайдер для генерации изображений с использованием API ImageLabs.net.  Он реализует асинхронный генератор изображений, который позволяет получить доступ к различным моделям ImageLabs, таким как `sdxl-turbo`, и генерировать изображения по текстовым описаниям.

## Классы

### `class ImageLabs`

**Описание**:  Класс `ImageLabs` реализует провайдер для асинхронной генерации изображений с использованием API ImageLabs.net. Он наследует классы `AsyncGeneratorProvider` и `ProviderModelMixin`, которые обеспечивают базовую функциональность для асинхронных провайдеров и поддержку моделей.

**Наследует**:
 - `AsyncGeneratorProvider`: Класс, который определяет интерфейс для асинхронных генераторов.
 - `ProviderModelMixin`:  Класс, который предоставляет функции для управления моделями.

**Атрибуты**:

- `url (str)`: Базовый URL API ImageLabs.
- `api_endpoint (str)`: URL конечной точки API для генерации изображений.
- `working (bool)`:  Флаг, указывающий, работает ли провайдер.
- `supports_stream (bool)`:  Флаг, указывающий, поддерживает ли провайдер потоковую передачу изображений.
- `supports_system_message (bool)`:  Флаг, указывающий, поддерживает ли провайдер системные сообщения.
- `supports_message_history (bool)`:  Флаг, указывающий, поддерживает ли провайдер историю сообщений.
- `default_model (str)`:  Название модели по умолчанию для генерации изображений.
- `default_image_model (str)`:  Название модели по умолчанию для генерации изображений (та же, что и `default_model`).
- `image_models (list[str])`:  Список доступных моделей для генерации изображений.
- `models (list[str])`:  Список доступных моделей (совпадает с `image_models`).

**Методы**:

- `create_async_generator(model: str, messages: Messages, proxy: str = None, prompt: str = None, negative_prompt: str = "", width: int = 1152, height: int = 896, **kwargs) -> AsyncResult`
    -  **Описание**:  Создает асинхронный генератор для генерации изображений. 
    - **Параметры**:
        - `model (str)`: Название модели для генерации изображений.
        - `messages (Messages)`:  Список сообщений, включая текстовое описание изображения.
        - `proxy (str)`: URL-адрес прокси-сервера (необязательно).
        - `prompt (str)`: Текстовое описание изображения (необязательно).
        - `negative_prompt (str)`: Текстовое описание, которого следует избегать при генерации изображения (необязательно).
        - `width (int)`: Ширина генерируемого изображения (по умолчанию 1152).
        - `height (int)`: Высота генерируемого изображения (по умолчанию 896).
        - `**kwargs`:  Дополнительные ключевые аргументы, которые могут использоваться для настройки генерации изображений.
    - **Возвращает**: `AsyncResult`:  Асинхронный объект, который представляет собой результат генерации изображений.
    - **Принцип работы**:
        - Создает объект `ClientSession` с заголовками запроса.
        - Извлекает текстовое описание изображения (`prompt`) из последнего сообщения в списке `messages`.
        - Формирует JSON-запрос к API ImageLabs, который содержит текстовое описание, параметры модели, размер изображения и т.д.
        - Отправляет POST-запрос к API и получает `task_id`.
        - Периодически опрашивает API о прогрессе выполнения задачи.
        -  Если задача выполнена, возвращает `ImageResponse`, содержащую URL-адрес сгенерированного изображения.
        -  Если задача не выполнена, продолжает опрашивать API до тех пор, пока задача не будет завершена или не возникнет ошибка.
        - Если возникает ошибка, поднимает исключение `Exception` с описанием ошибки.

- `get_model(model: str) -> str`:
    - **Описание**:  Возвращает название модели по умолчанию.
    - **Параметры**:
        - `model (str)`: Название модели (необязательно).
    - **Возвращает**: `str`: Название модели по умолчанию (`default_model`).
    - **Принцип работы**:  Просто возвращает `default_model`.


## Примеры

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider import ImageLabs
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создание списка сообщений
messages = Messages(
    [
        {"role": "user", "content": "Сгенерируй изображение кота, сидящего на подоконнике."},
    ]
)

# Инициализация объекта ImageLabs
image_labs = ImageLabs()

# Создание асинхронного генератора изображений
async_generator = await image_labs.create_async_generator(
    model="sdxl-turbo",
    messages=messages,
    width=512,
    height=512,
)

# Получение сгенерированного изображения
async for image_response in async_generator:
    print(f"URL изображения: {image_response.images[0]}")
```
```markdown
# Модуль DeepInfra

## Обзор

Модуль `DeepInfra` предназначен для взаимодействия с сервисом DeepInfra, который предоставляет доступ к различным AI-моделям, включая модели для генерации текста и изображений. Модуль реализует поддержку этих моделей через API DeepInfra.

## Подробней

Модуль определяет класс `DeepInfra`, который наследуется от `OpenaiTemplate`. Он включает в себя методы для получения списка доступных моделей, создания асинхронных генераторов для текстовых запросов и создания изображений на основе текстовых запросов. Для работы с DeepInfra требуется аутентификация.

## Классы

### `DeepInfra`

**Описание**: Класс для взаимодействия с API DeepInfra.
**Наследует**: `OpenaiTemplate`

**Атрибуты**:
- `url` (str): URL главной страницы DeepInfra.
- `login_url` (str): URL страницы для получения API ключей DeepInfra.
- `api_base` (str): Базовый URL API DeepInfra.
- `working` (bool): Указывает, работает ли провайдер (по умолчанию `True`).
- `needs_auth` (bool): Указывает, требуется ли аутентификация для работы с провайдером (по умолчанию `True`).
- `default_model` (str): Модель, используемая по умолчанию для генерации текста.
- `default_image_model` (str): Модель, используемая по умолчанию для генерации изображений.
- `models` (list): Список доступных текстовых моделей.
- `image_models` (list): Список доступных моделей для генерации изображений.

**Методы**:
- `get_models(**kwargs)`: Получает список доступных моделей.
- `get_image_models(**kwargs)`: Получает список доступных моделей для генерации изображений.
- `create_async_generator(model: str, messages: Messages, stream: bool, prompt: str = None, temperature: float = 0.7, max_tokens: int = 1028, **kwargs) -> AsyncResult`: Создает асинхронный генератор для обработки текстовых запросов.
- `create_async_image(prompt: str, model: str, api_key: str = None, api_base: str = "https://api.deepinfra.com/v1/inference", proxy: str = None, timeout: int = 180, extra_data: dict = {}, **kwargs) -> ImageResponse`: Создает изображение на основе текстового запроса.

## Методы класса

### `get_models`

```python
@classmethod
def get_models(cls, **kwargs):
    """
    Получает список доступных моделей из API DeepInfra.

    Args:
        **kwargs: Дополнительные аргументы.

    Returns:
        list: Список доступных моделей.
    """
```

**Как работает функция**:

Функция `get_models` выполняет следующие действия:
1. Проверяет, был ли уже получен список моделей. Если список `cls.models` не пуст, функция возвращает его.
2. Если список моделей пуст, функция выполняет HTTP-запрос к API DeepInfra для получения списка моделей.
3. Разбирает полученный JSON-ответ и заполняет списки `cls.models` и `cls.image_models` на основе типа модели ("text-generation" или "text-to-image").
4. Расширяет список `cls.models`, добавляя в него модели для генерации изображений.
5. Возвращает список `cls.models`.

**Примеры**:

```python
models = DeepInfra.get_models()
print(models)  # Вывод: список доступных моделей
```

### `get_image_models`

```python
@classmethod
def get_image_models(cls, **kwargs):
    """
    Получает список доступных моделей для генерации изображений из API DeepInfra.

    Args:
        **kwargs: Дополнительные аргументы.

    Returns:
        list: Список доступных моделей для генерации изображений.
    """
```

**Как работает функция**:

Функция `get_image_models` выполняет следующие действия:
1. Проверяет, был ли уже получен список моделей для генерации изображений. Если список `cls.image_models` не пуст, функция возвращает его.
2. Если список пуст, функция вызывает метод `cls.get_models()` для получения списка всех моделей, включая модели для генерации изображений.
3. Возвращает список `cls.image_models`.

**Примеры**:

```python
image_models = DeepInfra.get_image_models()
print(image_models)  # Вывод: список доступных моделей для генерации изображений
```

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    stream: bool,
    prompt: str = None,
    temperature: float = 0.7,
    max_tokens: int = 1028,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для обработки текстовых запросов к API DeepInfra.

    Args:
        model (str): Имя используемой модели.
        messages (Messages): Список сообщений для передачи в модель.
        stream (bool): Флаг, указывающий, использовать ли потоковую передачу данных.
        prompt (str, optional): Дополнительный текст запроса. По умолчанию `None`.
        temperature (float, optional): Температура для генерации текста. По умолчанию `0.7`.
        max_tokens (int, optional): Максимальное количество токенов в ответе. По умолчанию `1028`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий части ответа от API.
    """
```

**Как работает функция**:

Функция `create_async_generator` выполняет следующие действия:
1. Проверяет, является ли выбранная модель моделью для генерации изображений. Если это так, функция создает асинхронное изображение с помощью метода `cls.create_async_image()` и завершает работу.
2. Если модель не является моделью для генерации изображений, функция устанавливает заголовки HTTP-запроса, включая User-Agent, Referer и Origin.
3. Вызывает метод `super().create_async_generator()` для выполнения фактического запроса к API DeepInfra.
4. Передает полученные чанки данных из API DeepInfra в вызывающий код через `yield`.

**Внутренние функции**:

В данной функции отсутствуют внутренние функции.

**Примеры**:

```python
async for chunk in DeepInfra.create_async_generator(
    model="meta-llama/Meta-Llama-3.1-70B-Instruct",
    messages=[{"role": "user", "content": "Hello, how are you?"}],
    stream=True
):
    print(chunk)  # Вывод: чанки ответа от API
```

### `create_async_image`

```python
@classmethod
async def create_async_image(
    cls,
    prompt: str,
    model: str,
    api_key: str = None,
    api_base: str = "https://api.deepinfra.com/v1/inference",
    proxy: str = None,
    timeout: int = 180,
    extra_data: dict = {},
    **kwargs
) -> ImageResponse:
    """
    Создает изображение на основе текстового запроса, используя API DeepInfra.

    Args:
        prompt (str): Текст запроса для генерации изображения.
        model (str): Имя используемой модели для генерации изображений.
        api_key (str, optional): API ключ для аутентификации. По умолчанию `None`.
        api_base (str, optional): Базовый URL API DeepInfra. По умолчанию `"https://api.deepinfra.com/v1/inference"`.
        proxy (str, optional): URL прокси-сервера для использования. По умолчанию `None`.
        timeout (int, optional): Время ожидания ответа от API в секундах. По умолчанию `180`.
        extra_data (dict, optional): Дополнительные данные для передачи в API. По умолчанию `{}`.
        **kwargs: Дополнительные аргументы.

    Returns:
        ImageResponse: Объект `ImageResponse`, содержащий сгенерированное изображение.
    """
```

**Как работает функция**:

Функция `create_async_image` выполняет следующие действия:
1. Устанавливает заголовки HTTP-запроса, включая User-Agent, Referer, Origin и API ключ (если предоставлен).
2. Создает асинхронную сессию с использованием `StreamSession` для выполнения запроса к API DeepInfra.
3. Получает имя модели с помощью метода `cls.get_model()`.
4. Формирует данные запроса, включая текст запроса `prompt` и дополнительные данные `extra_data`.
5. Выполняет POST-запрос к API DeepInfra для генерации изображения.
6. Обрабатывает ответ от API DeepInfra, извлекая URL или данные изображения из JSON-ответа.
7. Создает и возвращает объект `ImageResponse`, содержащий сгенерированное изображение.

**Внутренние функции**:

В данной функции отсутствуют внутренние функции.

**Примеры**:

```python
image_response = await DeepInfra.create_async_image(
    prompt="A beautiful sunset over the ocean",
    model="stabilityai/sd3.5",
    api_key="YOUR_API_KEY"
)
print(image_response.images)  # Вывод: URL или данные сгенерированного изображения
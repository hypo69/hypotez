# Модуль `DeepInfra.py`

## Обзор

Модуль `DeepInfra.py` предоставляет класс `DeepInfra`, который является адаптером для взаимодействия с API DeepInfra. DeepInfra предоставляет доступ к различным моделям генерации текста и изображений. Модуль включает в себя функциональность для получения списка доступных моделей, создания асинхронных генераторов текста и изображений, а также обработки ответов от API DeepInfra.

## Подробней

Этот модуль позволяет использовать модели DeepInfra для генерации контента, интегрируя их в проект `hypotez`. Он поддерживает как текстовые, так и графические модели, обеспечивая гибкость при выборе подходящей модели для конкретной задачи. Для работы с DeepInfra требуется аутентификация через API ключ, который можно получить на сайте DeepInfra.

## Классы

### `DeepInfra`

**Описание**: Класс `DeepInfra` является адаптером для работы с API DeepInfra.

**Наследует**:

- `OpenaiTemplate`: Наследует функциональность от `OpenaiTemplate`, предоставляя базовую структуру для взаимодействия с API, подобными OpenAI.

**Атрибуты**:

- `url` (str): URL главной страницы DeepInfra.
- `login_url` (str): URL страницы для получения API ключей DeepInfra.
- `api_base` (str): Базовый URL API DeepInfra.
- `working` (bool): Указывает, что провайдер находится в рабочем состоянии.
- `needs_auth` (bool): Указывает, что для работы с провайдером требуется аутентификация.
- `default_model` (str): Модель, используемая по умолчанию для генерации текста (`meta-llama/Meta-Llama-3.1-70B-Instruct`).
- `default_image_model` (str): Модель, используемая по умолчанию для генерации изображений (`stabilityai/sd3.5`).
- `models` (list): Список доступных текстовых моделей (инициализируется пустым списком).
- `image_models` (list): Список доступных графических моделей (инициализируется пустым списком).

**Методы**:

- `get_models(**kwargs)`: Получает список доступных моделей из API DeepInfra.
- `get_image_models(**kwargs)`: Получает список доступных графических моделей из API DeepInfra.
- `create_async_generator(model: str, messages: Messages, stream: bool, prompt: str = None, temperature: float = 0.7, max_tokens: int = 1028, **kwargs) -> AsyncResult`: Создает асинхронный генератор для получения текстовых или графических данных от API DeepInfra.
- `create_async_image(prompt: str, model: str, api_key: str = None, api_base: str = "https://api.deepinfra.com/v1/inference", proxy: str = None, timeout: int = 180, extra_data: dict = {}, **kwargs) -> ImageResponse`: Создает асинхронный запрос для генерации изображения через API DeepInfra.

## Функции

### `get_models`

```python
@classmethod
def get_models(cls, **kwargs):
    """Получает список доступных моделей из API DeepInfra.

    Args:
        **kwargs: Дополнительные параметры.

    Returns:
        list: Список доступных моделей.
    """
    ...
```

**Назначение**: Получение списка моделей, доступных в DeepInfra. Если список моделей еще не был получен, функция отправляет запрос к API DeepInfra для получения списка моделей и разделяет их на текстовые и графические модели.

**Параметры**:

- `cls` (DeepInfra): Ссылка на класс `DeepInfra`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:

- `list`: Список доступных моделей.

**Как работает функция**:

1.  **Проверка наличия моделей**: Проверяет, был ли уже получен список моделей (`if not cls.models:`).
2.  **Получение данных из API**: Если список моделей пуст, отправляется GET-запрос к API DeepInfra (`'https://api.deepinfra.com/models/featured'`) для получения списка моделей.
3.  **Обработка ответа**:
    -   Разбирает JSON-ответ от API (`models = response.json()`).
    -   Инициализирует пустые списки `cls.models` и `cls.image_models`.
    -   Проходит по каждой модели в полученном списке (`for model in models:`).
    -   Определяет тип модели (`if model["type"] == "text-generation":` или `elif model["reported_type"] == "text-to-image":`) и добавляет её в соответствующий список (`cls.models` или `cls.image_models`).
4.  **Объединение списков**: Расширяет `cls.models`, добавляя в него элементы из `cls.image_models`.
5.  **Возврат списка моделей**: Возвращает список доступных моделей (`return cls.models`).

**Примеры**:

```python
models = DeepInfra.get_models()
print(models)
```

### `get_image_models`

```python
@classmethod
def get_image_models(cls, **kwargs):
    """Получает список доступных графических моделей из API DeepInfra.

    Args:
        **kwargs: Дополнительные параметры.

    Returns:
        list: Список доступных графических моделей.
    """
    ...
```

**Назначение**: Получает список графических моделей, доступных в DeepInfra. Если список графических моделей еще не был получен, функция вызывает `get_models` для получения полного списка моделей и извлекает из него только графические модели.

**Параметры**:

- `cls` (DeepInfra): Ссылка на класс `DeepInfra`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:

- `list`: Список доступных графических моделей.

**Как работает функция**:

1.  **Проверка наличия графических моделей**: Проверяет, был ли уже получен список графических моделей (`if not cls.image_models:`).
2.  **Получение списка моделей**: Если список графических моделей пуст, вызывается метод `cls.get_models()` для получения полного списка моделей.
3.  **Возврат списка графических моделей**: Возвращает список доступных графических моделей (`return cls.image_models`).

**Примеры**:

```python
image_models = DeepInfra.get_image_models()
print(image_models)
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
    """Создает асинхронный генератор для получения текстовых или графических данных от API DeepInfra.

    Args:
        model (str): Название модели для генерации.
        messages (Messages): Список сообщений для передачи в модель.
        stream (bool): Флаг, указывающий на необходимость потоковой передачи данных.
        prompt (str, optional): Дополнительный текст для запроса. По умолчанию `None`.
        temperature (float, optional): Температура для генерации текста. По умолчанию 0.7.
        max_tokens (int, optional): Максимальное количество токенов в ответе. По умолчанию 1028.
        **kwargs: Дополнительные параметры.

    Yields:
        AsyncResult: Асинхронный результат генерации.
    """
    ...
```

**Назначение**: Создает асинхронный генератор для получения текстовых или графических данных от API DeepInfra. Функция определяет, является ли запрошенная модель моделью генерации изображений, и вызывает соответствующую функцию для обработки запроса.

**Параметры**:

- `cls` (DeepInfra): Ссылка на класс `DeepInfra`.
- `model` (str): Название модели для генерации.
- `messages` (Messages): Список сообщений для передачи в модель.
- `stream` (bool): Флаг, указывающий на необходимость потоковой передачи данных.
- `prompt` (str, optional): Дополнительный текст для запроса. По умолчанию `None`.
- `temperature` (float, optional): Температура для генерации текста. По умолчанию 0.7.
- `max_tokens` (int, optional): Максимальное количество токенов в ответе. По умолчанию 1028.
- `**kwargs`: Дополнительные параметры.

**Как работает функция**:

1.  **Определение типа модели**: Проверяет, является ли запрошенная модель моделью генерации изображений (`if model in cls.get_image_models():`).
2.  **Генерация изображения**: Если модель является моделью генерации изображений, вызывается метод `cls.create_async_image` для создания и возврата изображения.
3.  **Генерация текста**: Если модель является моделью генерации текста, функция использует родительский метод `super().create_async_generator` для создания асинхронного генератора текста.
4.  **Передача заголовков**: Добавляет необходимые заголовки в запрос, включая информацию о браузере и источнике запроса.
5.  **Возврат результата**: Возвращает асинхронный генератор для получения данных от API.

**Примеры**:

```python
async for chunk in DeepInfra.create_async_generator(
    model="meta-llama/Meta-Llama-3.1-70B-Instruct",
    messages=[{"role": "user", "content": "Hello, how are you?"}],
    stream=True
):
    print(chunk)
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
    """Создает асинхронный запрос для генерации изображения через API DeepInfra.

    Args:
        prompt (str): Текст запроса для генерации изображения.
        model (str): Название модели для генерации изображения.
        api_key (str, optional): API ключ для аутентификации. По умолчанию `None`.
        api_base (str, optional): Базовый URL API DeepInfra. По умолчанию "https://api.deepinfra.com/v1/inference".
        proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
        timeout (int, optional): Время ожидания ответа от API. По умолчанию 180.
        extra_data (dict, optional): Дополнительные данные для запроса. По умолчанию `{}`.
        **kwargs: Дополнительные параметры.

    Returns:
        ImageResponse: Объект `ImageResponse` с информацией об изображении.
    """
    ...
```

**Назначение**: Создает асинхронный запрос для генерации изображения через API DeepInfra. Функция отправляет запрос к API с заданным текстом запроса (prompt) и моделью, обрабатывает ответ и возвращает объект `ImageResponse` с информацией об изображении.

**Параметры**:

- `cls` (DeepInfra): Ссылка на класс `DeepInfra`.
- `prompt` (str): Текст запроса для генерации изображения.
- `model` (str): Название модели для генерации изображения.
- `api_key` (str, optional): API ключ для аутентификации. По умолчанию `None`.
- `api_base` (str, optional): Базовый URL API DeepInfra. По умолчанию `"https://api.deepinfra.com/v1/inference"`.
- `proxy` (str, optional): Адрес прокси-сервера. По умолчанию `None`.
- `timeout` (int, optional): Время ожидания ответа от API. По умолчанию 180.
- `extra_data` (dict, optional): Дополнительные данные для запроса. По умолчанию `{}`.
- `**kwargs`: Дополнительные параметры.

**Как работает функция**:

1.  **Настройка заголовков**: Создает словарь с необходимыми заголовками для запроса, включая информацию о браузере, источнике запроса и API ключе (если он предоставлен).
2.  **Создание сессии**: Использует асинхронный `StreamSession` для отправки запроса к API.
3.  **Формирование данных запроса**:
    -   Получает название модели с помощью `cls.get_model(model)`.
    -   Формирует данные для запроса в формате JSON, включая текст запроса (prompt) и дополнительные данные.
4.  **Отправка запроса**: Отправляет POST-запрос к API DeepInfra с сформированными данными.
5.  **Обработка ответа**:
    -   Проверяет статус ответа с помощью `await raise_for_status(response)`.
    -   Разбирает JSON-ответ от API.
    -   Извлекает URL изображения из ответа (`data.get("output", data.get("images", data.get("image_url")))`).
    -   Проверяет, что URL изображения был получен.
    -   Создает и возвращает объект `ImageResponse` с информацией об изображении.

**Примеры**:

```python
image_response = await DeepInfra.create_async_image(
    prompt="A cat sitting on a chair",
    model="stabilityai/sd3.5",
    api_key="YOUR_API_KEY"
)
print(image_response.images)
```
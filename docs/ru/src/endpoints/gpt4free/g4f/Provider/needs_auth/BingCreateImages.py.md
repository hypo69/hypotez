# Модуль BingCreateImages

## Обзор

Модуль `BingCreateImages` предназначен для генерации изображений с использованием Microsoft Designer в Bing. Он предоставляет асинхронный генератор изображений на основе текстового запроса. Этот модуль требует аутентификации через cookie `_U`.

## Подробней

Этот модуль является частью проекта `hypotez` и служит для интеграции с сервисом создания изображений Bing. Он использует асинхронные запросы для генерации изображений и возвращает их в формате, пригодном для дальнейшей обработки. Модуль предназначен для работы в асинхронной среде и использует возможности `asyncio`. Расположен в `hypotez/src/endpoints/gpt4free/g4f/Provider/needs_auth/`.

## Классы

### `BingCreateImages`

**Описание**: Класс `BingCreateImages` реализует функциональность создания изображений через Microsoft Designer в Bing. Он наследует `AsyncGeneratorProvider` и `ProviderModelMixin`, что обеспечивает возможность асинхронной генерации и поддержку моделей.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Аттрибуты**:
- `label` (str): Метка провайдера, `"Microsoft Designer in Bing"`.
- `url` (str): URL для создания изображений, `"https://www.bing.com/images/create"`.
- `working` (bool): Флаг, указывающий на работоспособность провайдера, `True`.
- `needs_auth` (bool): Флаг, указывающий на необходимость аутентификации, `True`.
- `image_models` (List[str]): Список поддерживаемых моделей изображений, `["dall-e-3"]`.
- `models` (List[str]): Псевдоним для `image_models`.
- `cookies` (Optional[Cookies]): Cookie для аутентификации.
- `proxy` (Optional[str]): Прокси-сервер для выполнения запросов.
- `api_key` (Optional[str]): API-ключ для аутентификации.

**Методы**:
- `__init__(self, cookies: Cookies = None, proxy: str = None, api_key: str = None) -> None`: Инициализирует экземпляр класса `BingCreateImages`.
- `create_async_generator(cls, model: str, messages: Messages, prompt: str = None, api_key: str = None, cookies: Cookies = None, proxy: str = None, **kwargs) -> AsyncResult`: Создает асинхронный генератор для создания изображений.
- `generate(self, prompt: str) -> ImageResponse`: Генерирует изображение на основе переданного запроса.

### `__init__`

```python
def __init__(self, cookies: Cookies = None, proxy: str = None, api_key: str = None) -> None:
    """
    Инициализирует экземпляр класса `BingCreateImages`.

    Args:
        cookies (Optional[Cookies], optional): Cookie для аутентификации. По умолчанию `None`.
        proxy (Optional[str], optional): Прокси-сервер для выполнения запросов. По умолчанию `None`.
        api_key (Optional[str], optional): API-ключ для аутентификации. По умолчанию `None`.

    Returns:
        None

    """
    ...
```

**Назначение**: Инициализирует экземпляр класса `BingCreateImages` с заданными параметрами аутентификации и прокси.

**Параметры**:
- `cookies` (Optional[Cookies], optional): Cookie для аутентификации. По умолчанию `None`. Если передается `api_key`, то cookie `_U` устанавливается равным `api_key`.
- `proxy` (Optional[str], optional): Прокси-сервер для выполнения запросов. По умолчанию `None`.
- `api_key` (Optional[str], optional): API-ключ для аутентификации. По умолчанию `None`.

**Как работает функция**:

1.  Проверяет, передан ли `api_key`. Если да и `cookies` не переданы, создает словарь `cookies` и устанавливает значение cookie `_U` равным `api_key`.
2.  Сохраняет переданные `cookies`, `proxy` и `api_key` в атрибуты экземпляра класса.

**Примеры**:

```python
# Пример 1: Инициализация с cookie
cookies = {"_U": "some_api_key"}
bing_images = BingCreateImages(cookies=cookies)

# Пример 2: Инициализация с api_key
bing_images = BingCreateImages(api_key="some_api_key")

# Пример 3: Инициализация с proxy и api_key
bing_images = BingCreateImages(proxy="http://proxy.example.com", api_key="some_api_key")
```

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    prompt: str = None,
    api_key: str = None,
    cookies: Cookies = None,
    proxy: str = None,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для создания изображений.

    Args:
        model (str): Модель для генерации изображений.
        messages (Messages): Список сообщений для формирования запроса.
        prompt (str, optional): Запрос для генерации изображений. По умолчанию `None`.
        api_key (str, optional): API-ключ для аутентификации. По умолчанию `None`.
        cookies (Cookies, optional): Cookie для аутентификации. По умолчанию `None`.
        proxy (str, optional): Прокси-сервер для выполнения запросов. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор для создания изображений.

    """
    ...
```

**Назначение**: Создает асинхронный генератор для создания изображений на основе предоставленных параметров.

**Параметры**:
- `model` (str): Модель для генерации изображений.
- `messages` (Messages): Список сообщений для формирования запроса.
- `prompt` (str, optional): Запрос для генерации изображений. По умолчанию `None`.
- `api_key` (str, optional): API-ключ для аутентификации. По умолчанию `None`.
- `cookies` (Cookies, optional): Cookie для аутентификации. По умолчанию `None`.
- `proxy` (str, optional): Прокси-сервер для выполнения запросов. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор для создания изображений.

**Как работает функция**:

1.  Создает экземпляр класса `BingCreateImages` с переданными `cookies`, `proxy` и `api_key`.
2.  Форматирует запрос изображения с использованием `format_image_prompt` на основе `messages` и `prompt`.
3.  Возвращает асинхронный генератор, который при итерации генерирует изображение, используя метод `generate` экземпляра класса `BingCreateImages`.

**Примеры**:

```python
# Пример 1: Создание асинхронного генератора с использованием сообщений и модели
messages = [{"role": "user", "content": "Generate an image of a cat"}]
generator = BingCreateImages.create_async_generator(model="dall-e-3", messages=messages)

# Пример 2: Создание асинхронного генератора с использованием запроса и API-ключа
prompt = "A dog playing in the park"
generator = BingCreateImages.create_async_generator(model="dall-e-3", prompt=prompt, api_key="some_api_key")
```

### `generate`

```python
async def generate(self, prompt: str) -> ImageResponse:
    """
    Asynchronously creates a markdown formatted string with images based on the prompt.

    Args:
        prompt (str): Prompt to generate images.

    Returns:
        str: Markdown formatted string with images.
    """
    ...
```

**Назначение**: Асинхронно генерирует изображения на основе предоставленного запроса.

**Параметры**:
- `prompt` (str): Запрос для генерации изображений.

**Возвращает**:
- `ImageResponse`: Объект `ImageResponse`, содержащий сгенерированные изображения, запрос и метаданные.

**Вызывает исключения**:
- `MissingAuthError`: Если отсутствует cookie `_U`.

**Как работает функция**:

1.  Получает cookie из `.bing.com` или использует предоставленные в `self.cookies`.
2.  Проверяет наличие cookie `_U`. Если отсутствует, выбрасывает исключение `MissingAuthError`.
3.  Создает асинхронную сессию с использованием `create_session` с cookie и прокси.
4.  Генерирует изображения с использованием `create_images` на основе запроса `prompt`.
5.  Возвращает объект `ImageResponse` с изображениями, запросом и метаданными (URL для предпросмотра, если изображений больше одного).

**Примеры**:

```python
# Пример 1: Генерация изображения с использованием запроса
bing_images = BingCreateImages(api_key="some_api_key")
image_response = await bing_images.generate(prompt="A futuristic cityscape")

# Пример 2: Обработка исключения MissingAuthError
try:
    bing_images = BingCreateImages()
    image_response = await bing_images.generate(prompt="A cat wearing a hat")
except MissingAuthError as ex:
    print(f"Error: {ex}")
```
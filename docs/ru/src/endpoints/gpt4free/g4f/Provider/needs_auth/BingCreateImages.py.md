# Модуль BingCreateImages

## Обзор

Модуль `BingCreateImages` предоставляет асинхронный интерфейс для создания изображений с использованием Microsoft Designer в Bing. Он позволяет генерировать изображения на основе текстовых запросов, используя модель DALL-E 3. Модуль требует аутентификации через cookie "_U".

## Подробней

Этот модуль используется для интеграции с сервисом Bing Image Creator, позволяя пользователям генерировать изображения, используя текстовые подсказки. Он обрабатывает аутентификацию, создает сессию и форматирует вывод в виде markdown-строки с изображениями.
Расположение файла в проекте: `hypotez/src/endpoints/gpt4free/g4f/Provider/needs_auth/BingCreateImages.py` указывает, что этот модуль является частью подсистемы `gpt4free` проекта `hypotez`, отвечающей за взаимодействие с различными провайдерами изображений, требующими аутентификацию.

## Классы

### `BingCreateImages`

**Описание**: Класс `BingCreateImages` является асинхронным генератором изображений, использующим Microsoft Designer в Bing.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Позволяет использовать общие методы и атрибуты для моделей провайдеров.

**Атрибуты**:
- `label` (str): Метка провайдера ("Microsoft Designer in Bing").
- `url` (str): URL для создания изображений ("https://www.bing.com/images/create").
- `working` (bool): Флаг, указывающий, работает ли провайдер (True).
- `needs_auth` (bool): Флаг, указывающий, требуется ли аутентификация (True).
- `image_models` (List[str]): Список поддерживаемых моделей изображений (["dall-e-3"]).
- `models` (List[str]): Псевдоним для `image_models`.
- `cookies` (Cookies): Cookie для аутентификации.
- `proxy` (str): Прокси-сервер для использования.

**Методы**:
- `__init__(self, cookies: Cookies = None, proxy: str = None, api_key: str = None) -> None`: Инициализирует экземпляр класса `BingCreateImages`.
- `create_async_generator(cls, model: str, messages: Messages, prompt: str = None, api_key: str = None, cookies: Cookies = None, proxy: str = None, **kwargs) -> AsyncResult`: Создает асинхронный генератор изображений.
- `generate(self, prompt: str) -> ImageResponse`: Асинхронно генерирует изображения на основе запроса.

## Функции

### `__init__`

```python
def __init__(self, cookies: Cookies = None, proxy: str = None, api_key: str = None) -> None:
    """Инициализирует экземпляр класса `BingCreateImages`.

    Args:
        cookies (Cookies, optional): Cookie для аутентификации. По умолчанию `None`.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        api_key (str, optional): API-ключ для аутентификации. По умолчанию `None`.
    """
```

**Назначение**: Инициализирует экземпляр класса `BingCreateImages`, устанавливая параметры аутентификации и прокси.

**Параметры**:
- `cookies` (Cookies, optional): Cookie для аутентификации. По умолчанию `None`.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `api_key` (str, optional): API-ключ для аутентификации. По умолчанию `None`.

**Как работает функция**:
1. Проверяет, передан ли `api_key`. Если да, то обновляет или создает словарь `cookies` с ключом `"_U"` и значением `api_key`.
2. Сохраняет переданные значения `cookies` и `proxy` в атрибуты экземпляра класса.

```
api_key передан? --> Обновить/создать cookies --> Сохранить cookies и proxy
```

**Примеры**:
```python
# Пример 1: Создание экземпляра с использованием cookies
cookies = {"_U": "some_api_key"}
bing_images = BingCreateImages(cookies=cookies)

# Пример 2: Создание экземпляра с использованием api_key
bing_images = BingCreateImages(api_key="some_api_key")

# Пример 3: Создание экземпляра с использованием proxy и api_key
bing_images = BingCreateImages(api_key="some_api_key", proxy="http://proxy.example.com")
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
    """Создает асинхронный генератор изображений.

    Args:
        cls (BingCreateImages): Класс `BingCreateImages`.
        model (str): Модель для генерации изображений.
        messages (Messages): Список сообщений для формирования запроса.
        prompt (str, optional): Дополнительный запрос для генерации изображений. По умолчанию `None`.
        api_key (str, optional): API-ключ для аутентификации. По умолчанию `None`.
        cookies (Cookies, optional): Cookie для аутентификации. По умолчанию `None`.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор изображений.
    """
```

**Назначение**: Создает асинхронный генератор изображений на основе предоставленных параметров.

**Параметры**:
- `cls` (BingCreateImages): Класс `BingCreateImages`.
- `model` (str): Модель для генерации изображений.
- `messages` (Messages): Список сообщений для формирования запроса.
- `prompt` (str, optional): Дополнительный запрос для генерации изображений. По умолчанию `None`.
- `api_key` (str, optional): API-ключ для аутентификации. По умолчанию `None`.
- `cookies` (Cookies, optional): Cookie для аутентификации. По умолчанию `None`.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор изображений.

**Как работает функция**:
1. Создает экземпляр класса `BingCreateImages` с переданными параметрами аутентификации и прокси.
2. Форматирует запрос изображения, используя предоставленные сообщения и запрос.
3. Возвращает асинхронный генератор, который генерирует изображения на основе форматированного запроса.

```
Создать экземпляр BingCreateImages --> Форматировать запрос изображения --> Вернуть асинхронный генератор
```

**Примеры**:
```python
# Пример 1: Создание асинхронного генератора с использованием сообщений и api_key
messages = [{"role": "user", "content": "Generate an image of a cat"}]
async_generator = BingCreateImages.create_async_generator(model="dall-e-3", messages=messages, api_key="some_api_key")

# Пример 2: Создание асинхронного генератора с использованием сообщений, запроса и proxy
messages = [{"role": "user", "content": "Generate an image of a dog"}]
async_generator = BingCreateImages.create_async_generator(model="dall-e-3", messages=messages, prompt="wearing a hat", proxy="http://proxy.example.com")
```

### `generate`

```python
async def generate(self, prompt: str) -> ImageResponse:
    """
    Асинхронно создает markdown-форматированную строку с изображениями на основе запроса.

    Args:
        prompt (str): Prompt to generate images.

    Returns:
        str: Markdown formatted string with images.
    """
```

**Назначение**: Асинхронно генерирует изображения на основе текстового запроса и возвращает markdown-форматированную строку с изображениями.

**Параметры**:
- `prompt` (str): Текстовый запрос для генерации изображений.

**Возвращает**:
- `ImageResponse`: Объект `ImageResponse`, содержащий сгенерированные изображения, запрос и метаданные.

**Вызывает исключения**:
- `MissingAuthError`: Если отсутствует cookie "_U".

**Как работает функция**:
1. Получает cookie для домена ".bing.com". Если cookie не найдены или отсутствует cookie "_U", вызывает исключение `MissingAuthError`.
2. Создает асинхронную сессию с использованием полученных cookie и прокси.
3. Генерирует изображения с использованием созданной сессии и запроса.
4. Форматирует результат в виде объекта `ImageResponse`, который содержит список изображений и информацию для предварительного просмотра.

```
Получить cookies --> Создать асинхронную сессию --> Сгенерировать изображения --> Форматировать результат в ImageResponse
```

**Примеры**:
```python
# Пример 1: Генерация изображений с использованием запроса
bing_images = BingCreateImages(api_key="some_api_key")
image_response = await bing_images.generate(prompt="A futuristic city")

# Пример 2: Генерация изображений с использованием запроса и cookies
cookies = {"_U": "some_api_key"}
bing_images = BingCreateImages(cookies=cookies)
image_response = await bing_images.generate(prompt="A cat wearing a hat")
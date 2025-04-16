# Модуль MicrosoftDesigner

## Обзор

Модуль `MicrosoftDesigner` предоставляет функциональность для генерации изображений с использованием Microsoft Designer API. Он позволяет создавать изображения на основе текстовых запросов, используя различные модели и размеры изображений. Модуль поддерживает как асинхронную генерацию изображений через генератор, так и прямую генерацию изображений.

## Подробнее

Модуль предназначен для интеграции в проекты, требующие автоматической генерации изображений на основе текстовых описаний. Он использует API Microsoft Designer для создания изображений и предоставляет удобный интерфейс для взаимодействия с ним. Модуль поддерживает различные размеры изображений и позволяет использовать прокси для обхода ограничений сети.

## Классы

### `MicrosoftDesigner`

**Описание**: Класс `MicrosoftDesigner` является основным классом для взаимодействия с Microsoft Designer API. Он предоставляет методы для генерации изображений на основе текстовых запросов.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера, `"Microsoft Designer"`.
- `url` (str): URL Microsoft Designer, `"https://designer.microsoft.com"`.
- `working` (bool): Указывает, работает ли провайдер, `True`.
- `use_nodriver` (bool): Указывает, требуется ли использование nodriver, `True`.
- `needs_auth` (bool): Указывает, требуется ли аутентификация, `True`.
- `default_image_model` (str): Модель изображения по умолчанию, `"dall-e-3"`.
- `image_models` (List[str]): Список поддерживаемых моделей изображений, `[default_image_model, "1024x1024", "1024x1792", "1792x1024"]`.
- `models` (List[str]): Псевдоним для `image_models`.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для генерации изображений.
- `generate`: Генерирует изображение на основе текстового запроса.

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        prompt: str = None,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        """Создает асинхронный генератор для генерации изображений.

        Args:
            model (str): Модель для генерации изображений.
            messages (Messages): Список сообщений для формирования запроса.
            prompt (str, optional): Дополнительный текст запроса. По умолчанию `None`.
            proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Yields:
            AsyncResult: Объект `ImageResponse`, содержащий сгенерированные изображения.
        """
        ...
```

**Назначение**: Метод создает асинхронный генератор, который генерирует изображения на основе предоставленных параметров. Он выбирает размер изображения на основе указанной модели и вызывает метод `generate` для фактической генерации изображения.

**Параметры**:
- `model` (str): Модель для генерации изображений.
- `messages` (Messages): Список сообщений для формирования запроса.
- `prompt` (str, optional): Дополнительный текст запроса. По умолчанию `None`.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий объект `ImageResponse` с сгенерированными изображениями.

**Как работает функция**:
- Определяется размер изображения на основе входной модели. Если модель не является моделью по умолчанию и присутствует в списке поддерживаемых моделей, выбирается соответствующий размер изображения.
- Вызывается метод `generate` с форматированным запросом, размером изображения и прокси (если указан) для генерации изображения.
- Результат генерации возвращается через `yield`.

**Примеры**:

```python
# Пример использования create_async_generator
async for image_response in MicrosoftDesigner.create_async_generator(
    model="1024x1024",
    messages=[{"role": "user", "content": "Generate a cat image"}],
    prompt="High quality",
    proxy="http://your_proxy:8080"
):
    print(image_response.images)
```

### `generate`

```python
    @classmethod
    async def generate(cls, prompt: str, image_size: str, proxy: str = None) -> ImageResponse:
        """Генерирует изображение на основе текстового запроса.

        Args:
            prompt (str): Текстовый запрос для генерации изображения.
            image_size (str): Размер изображения.
            proxy (str, optional): URL прокси-сервера. По умолчанию `None`.

        Returns:
            ImageResponse: Объект `ImageResponse`, содержащий сгенерированные изображения.

        Raises:
            NoValidHarFileError: Если не найден валидный HAR-файл.
        """
        ...
```

**Назначение**: Метод генерирует изображение на основе предоставленного текстового запроса и размера изображения. Он использует учетные данные, полученные из HAR-файла или через `get_access_token_and_user_agent`, и вызывает функцию `create_images` для фактической генерации изображения.

**Параметры**:
- `prompt` (str): Текстовый запрос для генерации изображения.
- `image_size` (str): Размер изображения.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.

**Возвращает**:
- `ImageResponse`: Объект `ImageResponse`, содержащий сгенерированные изображения.

**Вызывает исключения**:
- `NoValidHarFileError`: Если не найден валидный HAR-файл.

**Как работает функция**:
- Сначала пытается получить токен доступа и User-Agent из HAR-файла с помощью функции `readHAR`. Если это не удается (например, файл не найден или не содержит нужной информации), перехватывается исключение `NoValidHarFileError`.
- Если HAR-файл недоступен или не содержит необходимой информации, вызывается асинхронная функция `get_access_token_and_user_agent` для получения токена доступа и User-Agent с использованием веб-драйвера.
- После получения токена доступа и User-Agent вызывается асинхронная функция `create_images` для создания изображений на основе запроса, токена доступа, User-Agent, размера изображения и прокси (если указан).
- Возвращается объект `ImageResponse`, содержащий сгенерированные изображения и исходный запрос.

**Примеры**:

```python
# Пример использования generate
image_response = await MicrosoftDesigner.generate(
    prompt="A futuristic cityscape",
    image_size="1024x1024",
    proxy="http://your_proxy:8080"
)
print(image_response.images)
```

## Функции

### `create_images`

```python
async def create_images(prompt: str, access_token: str, user_agent: str, image_size: str, proxy: str = None, seed: int = None) -> list[str]:
    """Создает изображения на основе текстового запроса, используя API Microsoft Designer.

    Args:
        prompt (str): Текстовый запрос для генерации изображения.
        access_token (str): Токен доступа для аутентификации в API.
        user_agent (str): User-Agent для HTTP-запросов.
        image_size (str): Размер изображения.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        seed (int, optional): Зерно для случайной генерации. По умолчанию `None`.

    Returns:
        list[str]: Список URL сгенерированных изображений.
    """
    ...
```

**Назначение**: Функция `create_images` отправляет запрос к API Microsoft Designer для генерации изображений на основе предоставленного текстового запроса, токена доступа, User-Agent, размера изображения и прокси (если указан).

**Параметры**:
- `prompt` (str): Текстовый запрос для генерации изображения.
- `access_token` (str): Токен доступа для аутентификации в API.
- `user_agent` (str): User-Agent для HTTP-запросов.
- `image_size` (str): Размер изображения.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `seed` (int, optional): Зерно для случайной генерации. По умолчанию `None`.

**Возвращает**:
- `list[str]`: Список URL сгенерированных изображений.

**Как работает функция**:
- Определяет URL для запроса к API Microsoft Designer.
- Генерирует случайное число (seed), если оно не было предоставлено.
- Формирует заголовки запроса, включая User-Agent, токен доступа и другие необходимые параметры.
- Создает объект `FormData` с параметрами запроса, такими как текстовый запрос, размер изображения, seed и другие параметры.
- Отправляет POST-запрос к API Microsoft Designer с использованием `aiohttp.ClientSession`.
- Обрабатывает ответ от API, извлекая URL сгенерированных изображений.
- Если изображения не были сразу получены, функция выполняет опрос API до тех пор, пока изображения не будут сгенерированы.
- Возвращает список URL сгенерированных изображений.

**Примеры**:

```python
# Пример использования create_images
images = await create_images(
    prompt="A cat riding a unicorn",
    access_token="your_access_token",
    user_agent="your_user_agent",
    image_size="1024x1024",
    proxy="http://your_proxy:8080"
)
print(images)
```

### `readHAR`

```python
def readHAR(url: str) -> tuple[str, str]:
    """Читает HAR-файлы для извлечения токена доступа и User-Agent.

    Args:
        url (str): URL для поиска в HAR-файлах.

    Returns:
        tuple[str, str]: Токен доступа и User-Agent.

    Raises:
        NoValidHarFileError: Если не найден валидный HAR-файл.
    """
    ...
```

**Назначение**: Функция `readHAR` читает HAR-файлы (HTTP Archive) для извлечения токена доступа (API key) и User-Agent, необходимых для аутентификации и выполнения запросов к API Microsoft Designer.

**Параметры**:
- `url` (str): URL, который используется для поиска соответствующей записи в HAR-файлах.

**Возвращает**:
- `tuple[str, str]`: Кортеж, содержащий токен доступа (api_key) и User-Agent.

**Вызывает исключения**:
- `NoValidHarFileError`: Если не найден валидный HAR-файл, содержащий необходимую информацию (токен доступа).

**Как работает функция**:
- Функция получает список путей к HAR-файлам с помощью `get_har_files()`.
- Для каждого файла в списке пытается открыть и прочитать содержимое как JSON. Если файл не является валидным JSON, он пропускается.
- Внутри каждого HAR-файла функция итерируется по записям (`entries`) в `log`.
- Для каждой записи проверяется, начинается ли URL запроса (`v['request']['url']`) с заданного URL.
- Если URL совпадает, функция извлекает заголовки запроса с помощью `get_headers(v)`.
- Проверяется наличие заголовков `authorization` и `user-agent` в извлеченных заголовках. Если они присутствуют, соответствующие значения извлекаются.
- Если токен доступа не найден ни в одном из HAR-файлов, функция вызывает исключение `NoValidHarFileError`.
- В случае успешного извлечения токена доступа и User-Agent функция возвращает их в виде кортежа.

**Примеры**:

```python
# Пример использования readHAR
try:
    access_token, user_agent = readHAR("https://designerapp.officeapps.live.com")
    print(f"Access Token: {access_token}")
    print(f"User Agent: {user_agent}")
except NoValidHarFileError as ex:
    print(f"Error: {ex}")
```

### `get_access_token_and_user_agent`

```python
async def get_access_token_and_user_agent(url: str, proxy: str = None) -> tuple[str, str]:
    """Получает токен доступа и User-Agent с использованием веб-драйвера.

    Args:
        url (str): URL для получения токена доступа.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.

    Returns:
        tuple[str, str]: Токен доступа и User-Agent.

    Raises:
        MissingRequirementsError: Если не удалось получить токен доступа.
    """
    ...
```

**Назначение**: Функция `get_access_token_and_user_agent` использует веб-драйвер для получения токена доступа и User-Agent, необходимых для аутентификации и выполнения запросов к API Microsoft Designer.

**Параметры**:
- `url` (str): URL, который используется для получения токена доступа.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.

**Возвращает**:
- `tuple[str, str]`: Кортеж, содержащий токен доступа и User-Agent.

**Вызывает исключения**:
- `MissingRequirementsError`: Если не удалось получить токен доступа.

**Как работает функция**:
- Функция запускает веб-драйвер с использованием `get_nodriver`, передавая URL прокси-сервера (если указан) и путь к пользовательским данным ("designer").
- Открывает указанный URL в браузере с помощью `browser.get(url)`.
- Извлекает User-Agent из браузера с помощью `page.evaluate("navigator.userAgent")`.
- Выполняет JavaScript-код в браузере для извлечения токена доступа из `localStorage`. Код ищет элементы, у которых `credentialType` равен "AccessToken", `expiresOn` больше текущего времени, и `target` содержит "designerappservice".
- Если токен доступа не найден, функция повторяет попытки его получения, ожидая 1 секунду между попытками.
- После успешного извлечения токена доступа и User-Agent функция закрывает страницу и останавливает браузер.
- Возвращает токен доступа и User-Agent в виде кортежа.

**Примеры**:

```python
# Пример использования get_access_token_and_user_agent
try:
    access_token, user_agent = await get_access_token_and_user_agent("https://designer.microsoft.com", proxy="http://your_proxy:8080")
    print(f"Access Token: {access_token}")
    print(f"User Agent: {user_agent}")
except MissingRequirementsError as ex:
    print(f"Error: {ex}")
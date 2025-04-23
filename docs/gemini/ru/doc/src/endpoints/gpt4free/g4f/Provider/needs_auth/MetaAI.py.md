# Модуль MetaAI

## Обзор

Модуль `MetaAI` предоставляет асинхронный интерфейс для взаимодействия с Meta AI. Он включает в себя функциональность для получения доступа к токену, отправки запросов и обработки ответов от Meta AI. Модуль поддерживает как текстовые запросы, так и запросы на генерацию изображений.

## Подробней

Модуль `MetaAI` предназначен для работы с Meta AI API. Он обеспечивает асинхронное взаимодействие с серверами Meta AI, включая получение access token, отправку сообщений и обработку ответов. В модуле реализована поддержка прокси-серверов, что позволяет использовать его в различных сетевых конфигурациях.

## Классы

### `Sources`

**Описание**: Класс `Sources` предназначен для хранения и форматирования списка источников, представленных в виде словарей со ссылками.

**Атрибуты**:
- `list` (List[Dict[str, str]]): Список словарей, где каждый словарь содержит информацию об источнике, включая заголовок (`title`) и ссылку (`link`).

**Методы**:
- `__init__(self, link_list: List[Dict[str, str]]) -> None`: Инициализирует объект `Sources` списком словарей со ссылками.
- `__str__(self) -> str`: Возвращает строковое представление списка источников в формате Markdown.

### `AbraGeoBlockedError`

**Описание**: Класс `AbraGeoBlockedError` представляет собой исключение, которое выбрасывается, когда Meta AI недоступен в определенной географической локации.

### `MetaAI`

**Описание**: Класс `MetaAI` предоставляет асинхронный интерфейс для взаимодействия с Meta AI.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию ответов.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера "Meta AI".
- `url` (str): URL Meta AI "https://www.meta.ai".
- `working` (bool): Флаг, указывающий на работоспособность провайдера (True).
- `default_model` (str): Модель, используемая по умолчанию ('meta-ai').
- `session` (ClientSession): Асинхронная сессия для выполнения HTTP-запросов.
- `cookies` (Cookies): Файлы cookie для аутентификации.
- `access_token` (str): Токен доступа для аутентификации.
- `lsd` (str): Значение lsd, необходимое для запросов.
- `dtsg` (str): Значение dtsg, необходимое для запросов.

**Методы**:
- `__init__(self, proxy: str = None, connector: BaseConnector = None)`: Инициализирует объект `MetaAI`.
- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: Создает асинхронный генератор для получения ответов от Meta AI.
- `update_access_token(self, birthday: str = "1999-01-01")`: Обновляет токен доступа.
- `prompt(self, message: str, cookies: Cookies = None) -> AsyncResult`: Отправляет запрос к Meta AI и возвращает асинхронный генератор ответов.
- `update_cookies(self, cookies: Cookies = None)`: Обновляет файлы cookie для аутентификации.
- `fetch_sources(self, fetch_id: str) -> Sources`: Получает источники для ответа Meta AI.
- `extract_value(text: str, key: str = None, start_str=None, end_str='\',) -> str`: Извлекает значение из текста на основе заданных начального и конечного строк.

## Методы класса

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для получения ответов от Meta AI.

        Args:
            model (str): Используемая модель.
            messages (Messages): Список сообщений для отправки.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий ответы от Meta AI.
        """
        ...
```

### `update_access_token`

```python
    async def update_access_token(self, birthday: str = "1999-01-01"):
        """
        Обновляет токен доступа для Meta AI.

        Args:
            birthday (str, optional): Дата рождения пользователя в формате "YYYY-MM-DD". По умолчанию "1999-01-01".

        Raises:
            ResponseError: Если не удается получить токен доступа.

        Как работает функция:
        - Функция отправляет POST-запрос к API Meta AI для обновления токена доступа.
        - В случае успешного получения, функция извлекает и сохраняет новый токен доступа.

        Примеры:
            >>> await meta_ai_instance.update_access_token(birthday="1990-05-15")
        """
        ...
```

### `prompt`

```python
    async def prompt(self, message: str, cookies: Cookies = None) -> AsyncResult:
        """
        Отправляет запрос к Meta AI и возвращает асинхронный генератор ответов.

        Args:
            message (str): Текст сообщения для отправки.
            cookies (Cookies, optional): Файлы cookie для использования. По умолчанию `None`.

        Yields:
            str: Части ответа от Meta AI.
            ImageResponse: Ответ с изображением, если Meta AI возвращает изображение.
            ImagePreview: Предварительный просмотр изображения, если Meta AI возвращает изображение.
            Sources: Источники, если Meta AI возвращает источники.

        Raises:
            ResponseError: Если происходит ошибка при отправке запроса или получении ответа.

        Как работает функция:
        - Функция отправляет POST-запрос к API Meta AI с заданным сообщением и файлами cookie.
        - Функция обрабатывает потоковый ответ от Meta AI, извлекая текстовые фрагменты, изображения и источники.
        - Если ответ содержит изображения, функция возвращает объекты `ImageResponse` или `ImagePreview`.
        - Если ответ содержит источники, функция возвращает объект `Sources`.
        - Функция генерирует исключение `ResponseError`, если происходит ошибка при отправке запроса или получении ответа.

        Примеры:
            >>> async for chunk in meta_ai_instance.prompt(message="Hello, Meta AI!"):
            ...     print(chunk)
        """
        ...
```

### `update_cookies`

```python
    async def update_cookies(self, cookies: Cookies = None):
        """
        Обновляет файлы cookie для аутентификации.

        Args:
            cookies (Cookies, optional): Файлы cookie для обновления. По умолчанию `None`.

        Raises:
            AbraGeoBlockedError: Если Meta AI недоступен в данной географической локации.
            ResponseError: Если не удается получить файлы cookie.

        Как работает функция:
        - Функция отправляет GET-запрос к Meta AI для обновления файлов cookie.
        - Функция извлекает значения `lsd`, `dtsg` и другие необходимые файлы cookie из ответа.
        - Функция сохраняет обновленные файлы cookie для последующего использования.
        - Функция генерирует исключение `AbraGeoBlockedError`, если Meta AI недоступен в данной географической локации.
        - Функция генерирует исключение `ResponseError`, если не удается получить файлы cookie.

        Примеры:
            >>> await meta_ai_instance.update_cookies(cookies={"cookie_name": "cookie_value"})
        """
        ...
```

### `fetch_sources`

```python
    async def fetch_sources(self, fetch_id: str) -> Sources:
        """
        Получает источники для ответа Meta AI.

        Args:
            fetch_id (str): Идентификатор запроса.

        Returns:
            Sources: Объект `Sources`, содержащий список источников.

        Raises:
            ResponseError: Если происходит ошибка при получении источников.

        Как работает функция:
        - Функция отправляет POST-запрос к API Meta AI для получения источников на основе заданного идентификатора запроса.
        - Функция извлекает список источников из ответа и возвращает объект `Sources`.
        - Функция генерирует исключение `ResponseError`, если происходит ошибка при получении источников.

        Примеры:
            >>> sources = await meta_ai_instance.fetch_sources(fetch_id="1234567890")
            >>> print(sources)
        """
        ...
```

### `extract_value`

```python
    @staticmethod
    def extract_value(text: str, key: str = None, start_str = None, end_str = '\',) -> str:
        """
        Извлекает значение из текста на основе заданных начального и конечного строк.

        Args:
            text (str): Текст, из которого нужно извлечь значение.
            key (str, optional): Ключ для поиска начальной строки. По умолчанию `None`.
            start_str (str, optional): Начальная строка для поиска значения. По умолчанию `None`.
            end_str (str, optional): Конечная строка для поиска значения. По умолчанию `',\`.

        Returns:
            str: Извлеченное значение или `None`, если значение не найдено.

        Как работает функция:
        - Функция ищет начальную строку в тексте. Если `start_str` не задан, используется `key` для формирования начальной строки.
        - Если начальная строка найдена, функция ищет конечную строку после начальной строки.
        - Если конечная строка найдена, функция извлекает значение между начальной и конечной строками и возвращает его.
        - Если начальная или конечная строка не найдена, функция возвращает `None`.

        Примеры:
            >>> MetaAI.extract_value(text='{"key":{"value":"extracted_value"}}', key="key")
            'extracted_value'
        """
        ...
```

## Функции

### `generate_offline_threading_id`

```python
def generate_offline_threading_id() -> str:
    """
    Генерирует offline threading ID.

    Returns:
        str: Сгенерированный offline threading ID.

    Как работает функция:
    - Генерирует случайное 64-битное целое число.
    - Получает текущую метку времени в миллисекундах.
    - Объединяет метку времени и случайное значение.
    - Возвращает строковое представление сгенерированного ID.
    """
    ...
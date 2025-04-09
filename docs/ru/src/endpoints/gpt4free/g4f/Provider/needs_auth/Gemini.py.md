# Модуль для работы с Google Gemini (g4f.Provider.needs_auth.Gemini)

## Обзор

Модуль `Gemini.py` предназначен для взаимодействия с Google Gemini. Он предоставляет асинхронные генераторы для получения ответов от модели Gemini, включая поддержку текстовых и визуальных запросов. Модуль требует аутентификации и использует cookies для поддержания сессии.

## Подробней

Этот модуль является частью проекта `hypotez` и отвечает за интеграцию с сервисом Google Gemini. Он включает в себя функции для автоматического обновления cookies, загрузки изображений и синтеза речи. Модуль также обрабатывает ответы от Gemini, извлекая из них текст, изображения и ссылки на YouTube.

## Классы

### `Gemini`

**Описание**: Класс `Gemini` является асинхронным генератором, который реализует взаимодействие с моделью Google Gemini.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую структуру для асинхронных провайдеров генераторов.
- `ProviderModelMixin`: Предоставляет функциональность для работы с различными моделями, поддерживаемыми провайдером.

**Аттрибуты**:
- `label` (str): Метка провайдера (Google Gemini).
- `url` (str): URL сервиса Gemini.
- `needs_auth` (bool): Указывает, требуется ли аутентификация для работы с провайдером.
- `working` (bool): Указывает, работает ли провайдер в данный момент.
- `use_nodriver` (bool): Указывает, следует ли использовать `nodriver` для автоматической аутентификации.
- `default_model` (str): Модель по умолчанию.
- `default_image_model` (str): Модель для генерации изображений по умолчанию.
- `default_vision_model` (str): Модель для обработки визуальных данных по умолчанию.
- `image_models` (list[str]): Список поддерживаемых моделей для генерации изображений.
- `models` (list[str]): Список поддерживаемых моделей.
- `model_aliases` (dict[str, str]): Псевдонимы моделей.
- `synthesize_content_type` (str): Тип контента для синтеза речи (audio/vnd.wav).
- `_cookies` (Cookies): Cookies для аутентификации.
- `_snlm0e` (str): Значение параметра `SNlM0e`, необходимого для запросов.
- `_sid` (str): Значение параметра `SID`, необходимого для запросов.
- `auto_refresh` (bool): Автоматическое обновление cookies.
- `refresh_interval` (int): Интервал обновления cookies в секундах.
- `rotate_tasks` (dict): Словарь задач для ротации cookies.

**Методы**:
- `nodriver_login()`: Метод для автоматической аутентификации с использованием `nodriver`.
- `start_auto_refresh()`: Запускает задачу для автоматического обновления cookies в фоновом режиме.
- `create_async_generator()`: Создает асинхронный генератор для взаимодействия с моделью Gemini.
- `synthesize()`: Генерирует речь на основе заданного текста.
- `build_request()`: Строит запрос к API Gemini.
- `upload_images()`: Загружает изображения на сервер Gemini.
- `fetch_snlm0e()`: Получает значение параметра `SNlM0e` из cookies.

#### `nodriver_login`

```python
    @classmethod
    async def nodriver_login(cls, proxy: str = None) -> AsyncIterator[str]:
        """
        Автоматическая аутентификация с использованием `nodriver`.

        Args:
            proxy (str, optional): Прокси-сервер для подключения. По умолчанию `None`.

        Yields:
            AsyncIterator[str]: Асинхронный итератор, возвращающий чанки данных.

        Raises:
            ImportError: Если модуль `nodriver` не установлен.
        """
        ...
```

#### `start_auto_refresh`

```python
    @classmethod
    async def start_auto_refresh(cls, proxy: str = None) -> None:
        """
        Запускает задачу для автоматического обновления cookies в фоновом режиме.
        """
        ...
```

#### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        cookies: Cookies = None,
        connector: BaseConnector = None,
        media: MediaListType = None,
        return_conversation: bool = False,
        conversation: Conversation = None,
        language: str = "en",
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для взаимодействия с моделью Gemini.

        Args:
            model (str): Название модели Gemini.
            messages (Messages): Список сообщений для отправки.
            proxy (str, optional): Прокси-сервер для подключения. По умолчанию `None`.
            cookies (Cookies, optional): Cookies для аутентификации. По умолчанию `None`.
            connector (BaseConnector, optional): HTTP-коннектор. По умолчанию `None`.
            media (MediaListType, optional): Список медиафайлов для отправки. По умолчанию `None`.
            return_conversation (bool, optional): Возвращать ли объект Conversation. По умолчанию `False`.
            conversation (Conversation, optional): Объект Conversation. По умолчанию `None`.
            language (str, optional): Язык ответа. По умолчанию "en".
            **kwargs: Дополнительные параметры.

        Yields:
            AsyncResult: Асинхронный генератор, возвращающий результаты от модели Gemini.

        Raises:
            MissingAuthError: Если отсутствует или недействителен cookie "__Secure-1PSID".
            RuntimeError: Если не удалось получить значение SNlM0e.
        """
        ...
```

#### `synthesize`

```python
    @classmethod
    async def synthesize(cls, params: dict, proxy: str = None) -> AsyncIterator[bytes]:
        """
        Генерирует речь на основе заданного текста.

        Args:
            params (dict): Параметры для генерации речи, включая текст.
            proxy (str, optional): Прокси-сервер для подключения. По умолчанию `None`.

        Yields:
            AsyncIterator[bytes]: Асинхронный итератор, возвращающий чанки аудиоданных в формате bytes.

        Raises:
            ValueError: Если отсутствует параметр "text".
        """
        ...
```

#### `build_request`

```python
    def build_request(
        prompt: str,
        language: str,
        conversation: Conversation = None,
        uploads: list[list[str, str]] = None,
        tools: list[list[str]] = []
    ) -> list:
        """
        Строит запрос к API Gemini.

        Args:
            prompt (str): Текст запроса.
            language (str): Язык запроса.
            conversation (Conversation, optional): Объект Conversation. По умолчанию `None`.
            uploads (list[list[str, str]], optional): Список загруженных изображений. По умолчанию `None`.
            tools (list[list[str]], optional): Список инструментов. По умолчанию `[]`.

        Returns:
            list: Сформированный запрос в виде списка.
        """
        ...
```

#### `upload_images`

```python
    async def upload_images(connector: BaseConnector, media: MediaListType) -> list:
        """
        Загружает изображения на сервер Gemini.

        Args:
            connector (BaseConnector): HTTP-коннектор.
            media (MediaListType): Список медиафайлов для загрузки.

        Returns:
            list: Список URL загруженных изображений.
        """
        ...
```

#### `fetch_snlm0e`

```python
    @classmethod
    async def fetch_snlm0e(cls, session: ClientSession, cookies: Cookies):
        """
        Получает значение параметра `SNlM0e` из cookies.

        Args:
            session (ClientSession): HTTP-сессия.
            cookies (Cookies): Cookies для запроса.
        """
        ...
```

### `Conversation`

**Описание**: Класс `Conversation` представляет собой структуру данных для хранения информации о контексте разговора с моделью Gemini.

**Наследует**:
- `JsonConversation`: Базовый класс для представления контекста разговора в формате JSON.

**Аттрибуты**:
- `conversation_id` (str): Идентификатор разговора.
- `response_id` (str): Идентификатор последнего ответа в разговоре.
- `choice_id` (str): Идентификатор выбора ответа.
- `model` (str): Используемая модель.

## Функции

### `iter_filter_base64`

```python
async def iter_filter_base64(chunks: AsyncIterator[bytes]) -> AsyncIterator[bytes]:
    """
    Фильтрует асинхронный итератор байтовых чанков, извлекая полезную нагрузку base64.

    Args:
        chunks (AsyncIterator[bytes]): Асинхронный итератор байтовых чанков.

    Yields:
        AsyncIterator[bytes]: Отфильтрованный асинхронный итератор байтовых чанков.

    Raises:
        ValueError: Если в чанке не найдена строка `search_for`.

    Как работает функция:
    1. Функция принимает асинхронный итератор байтовых чанков `chunks`.
    2. Определяет переменные `search_for` и `end_with`, которые содержат байтовые строки для поиска начала и конца полезной нагрузки base64 соответственно.
    3. Итерируется по чанкам:
        - Если `is_started` равно `True`, это означает, что начало полезной нагрузки уже найдено.
            - Если `end_with` присутствует в текущем чанке, функция извлекает часть чанка до `end_with`, отправляет её и завершает итерацию.
            - В противном случае, функция отправляет текущий чанк.
        - Если `is_started` равно `False`, функция проверяет, содержит ли текущий чанк `search_for`.
            - Если `search_for` присутствует в чанке, функция устанавливает `is_started` в `True`, извлекает часть чанка после `search_for` и отправляет её.
            - Если `search_for` отсутствует в чанке, функция вызывает исключение `ValueError`.

    ASCII flowchart:
    A[Начало]
    |
    B[Принят чанк]
    |
    C{is_started?}
    | Да
    D{end_with in chunk?}
    | Да
    E[Извлечь часть до end_with и отправить]
    |
    F[Завершить]
    C -- Нет
    |
    G{search_for in chunk?}
    | Да
    H[Установить is_started = True и извлечь часть после search_for]
    |
    I[Отправить часть]
    |
    B --
    G -- Нет
    |
    J[Вызвать ValueError]
    |
    K[Конец]

    Примеры:
    - Пример 1:
        chunks = [b'some data [["wrb.fr","XqA3Ic","[\\\\"base64data\\\\']', b'end\\\\']
        Результат: b'base64data'

    - Пример 2:
        chunks = [b'[["wrb.fr","XqA3Ic","[\\\\"base64data', b'moredata\\\\']
        Результат: b'base64datamoredata'
    """
    ...
```

### `iter_base64_decode`

```python
async def iter_base64_decode(chunks: AsyncIterator[bytes]) -> AsyncIterator[bytes]:
    """
    Декодирует асинхронный итератор base64-encoded байтовых чанков.

    Args:
        chunks (AsyncIterator[bytes]): Асинхронный итератор base64-encoded байтовых чанков.

    Yields:
        AsyncIterator[bytes]: Асинхронный итератор декодированных байтовых чанков.

    Как работает функция:
    1.  Инициализирует буфер `buffer` для хранения остатков base64 данных между чанками.
    2.  Инициализирует переменную `rest` для хранения количества байт, которые остались не обработанными после base64 декодирования.
    3.  Итерируется по чанкам:
        - Объединяет текущий чанк с содержимым буфера `buffer`.
        - Вычисляет остаток от деления длины объединенного чанка на 4 (так как base64 декодирование работает с блоками по 4 символа).
        - Сохраняет последние `rest` байт объединенного чанка в буфер `buffer`.
        - Декодирует base64 данные из объединенного чанка, исключая последние `rest` байт, и отправляет декодированные данные.
    4.  После завершения итерации, если в буфере `buffer` остались необработанные данные (`rest > 0`), декодирует base64 данные из буфера, добавляя необходимое количество символов `=` для корректного декодирования, и отправляет декодированные данные.

    ASCII flowchart:

    A[Начало]
    |
    B[Инициализация buffer = b"" и rest = 0]
    |
    C[Принят чанк]
    |
    D[chunk = buffer + chunk]
    |
    E[rest = len(chunk) % 4]
    |
    F[buffer = chunk[-rest:]]
    |
    G[yield base64.b64decode(chunk[:-rest])]
    |
    H[Конец итерации?]
    | Да
    I{rest > 0?}
    | Да
    J[yield base64.b64decode(buffer+rest*b"=")]
    |
    K[Конец]
    H -- Нет
    |
    C --
    I -- Нет
    |
    K --

    Примеры:
    - Пример 1:
        chunks = [b'YWFh', b'YWFh']
        Результат: b'aaa', b'aaa'
    - Пример 2:
        chunks = [b'YWFhYQ']
        Результат: b'aaa'
    - Пример 3:
        chunks = [b'YWFhYWFh']
        Результат: b'aaaaaa'
    """
    ...
```

### `rotate_1psidts`

```python
async def rotate_1psidts(url, cookies: dict, proxy: str | None = None) -> str:
    """
    Обновляет cookie "__Secure-1PSIDTS" путем запроса к сервису Google.

    Args:
        url (str): URL сервиса Google.
        cookies (dict): Текущие cookies.
        proxy (str | None, optional): Прокси-сервер для подключения. По умолчанию `None`.

    Returns:
        str: Новое значение cookie "__Secure-1PSIDTS".

    Raises:
        MissingAuthError: Если cookies недействительны.
        HTTPError: Если произошла ошибка при выполнении HTTP-запроса.

    Как работает функция:
    1.  Создает директорию для хранения cookies, если она не существует.
    2.  Формирует путь к файлу, в котором хранятся cookies.
    3.  Проверяет, был ли файл модифицирован в течение последней минуты, чтобы избежать ошибки "429 Too Many Requests".
    4.  Создает асинхронную HTTP-сессию.
    5.  Выполняет POST-запрос к сервису Google для обновления cookies.
    6.  Проверяет статус ответа. Если статус равен 401, выбрасывает исключение `MissingAuthError`.
    7.  Обновляет cookies на основе ответа от сервера.
    8.  Сохраняет обновленные cookies в файл.
    9.  Возвращает новое значение cookie "__Secure-1PSIDTS".

    ASCII flowchart:

    A[Начало]
    |
    B[Создать директорию для cookies]
    |
    C[Сформировать путь к файлу cookies]
    |
    D{Файл изменен в течение минуты?}
    | Нет
    E[Создать асинхронную HTTP-сессию]
    |
    F[Выполнить POST-запрос к сервису Google]
    |
    G{response.status == 401?}
    | Да
    H[Выбросить MissingAuthError]
    |
    I[Конец]
    G -- Нет
    |
    J[Обновить cookies]
    |
    K[Сохранить cookies в файл]
    |
    L[Вернуть новое значение __Secure-1PSIDTS]
    |
    I --
    D -- Да
    |
    L --

    Примеры:
    - Пример 1:
        url = "https://accounts.google.com/RotateCookies"
        cookies = {"__Secure-1PSID": "some_sid"}
        Результат: "new_1psidts_value" (если запрос успешен)
    """
    ...
# Модуль OpenaiTemplate

## Обзор

Модуль `OpenaiTemplate` предоставляет класс `OpenaiTemplate`, который является шаблоном для взаимодействия с API OpenAI. Он включает в себя функциональность для получения списка моделей, создания асинхронного генератора для обработки сообщений и управления заголовками запросов. Этот класс предназначен для упрощения взаимодействия с API OpenAI и предоставляет абстракцию для различных операций, таких как генерация текста и изображений.

## Подробнее

Модуль `OpenaiTemplate` облегчает интеграцию с OpenAI API, предоставляя инструменты для асинхронного взаимодействия, обработки ошибок и управления параметрами запросов. Он также поддерживает работу с изображениями и предоставляет возможность использования прокси и пользовательских заголовков.

## Классы

### `OpenaiTemplate`

**Описание**: Класс `OpenaiTemplate` является базовым классом для работы с API OpenAI. Он предоставляет методы для получения списка моделей, создания асинхронного генератора для обработки сообщений и управления заголовками запросов.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.
- `RaiseErrorMixin`: Обеспечивает обработку ошибок.

**Атрибуты**:
- `api_base` (str): Базовый URL API OpenAI.
- `api_key` (Optional[str]): Ключ API OpenAI.
- `api_endpoint` (Optional[str]): Конечная точка API OpenAI.
- `supports_message_history` (bool): Указывает, поддерживается ли история сообщений.
- `supports_system_message` (bool): Указывает, поддерживаются ли системные сообщения.
- `default_model` (str): Модель, используемая по умолчанию.
- `fallback_models` (list[str]): Список моделей для использования в случае ошибки.
- `sort_models` (bool): Указывает, нужно ли сортировать модели.
- `ssl` (Optional[bool]): Указывает, использовать ли SSL.

**Методы**:
- `get_models()`: Возвращает список доступных моделей.
- `create_async_generator()`: Создает асинхронный генератор для обработки сообщений.
- `get_headers()`: Возвращает словарь заголовков для запроса.

### `OpenaiTemplate.get_models`

```python
    @classmethod
    def get_models(cls, api_key: str = None, api_base: str = None) -> list[str]:
        """
        Получает список доступных моделей из API OpenAI.

        Args:
            api_key (Optional[str]): Ключ API OpenAI.
            api_base (Optional[str]): Базовый URL API OpenAI.

        Returns:
            list[str]: Список доступных моделей.

        Raises:
            Exception: Если происходит ошибка при получении списка моделей.

        Example:
            >>> models = OpenaiTemplate.get_models(api_key='your_api_key')
            >>> print(models)
            ['model1', 'model2', ...]
        """
```

**Назначение**: Получение списка доступных моделей из API OpenAI.

**Параметры**:
- `api_key` (Optional[str]): Ключ API OpenAI. Если не указан, используется значение `cls.api_key`.
- `api_base` (Optional[str]): Базовый URL API OpenAI. Если не указан, используется значение `cls.api_base`.

**Возвращает**:
- `list[str]`: Список доступных моделей. Если происходит ошибка, возвращается `cls.fallback_models`.

**Вызывает исключения**:
- `Exception`: Если происходит ошибка при выполнении запроса к API OpenAI.

**Как работает функция**:

1. **Проверка наличия моделей в кэше**:
   - Функция проверяет, были ли уже загружены модели в атрибут `cls.models`. Если модели уже загружены, функция сразу возвращает их из кэша.

2. **Подготовка заголовков**:
   - Функция инициализирует пустой словарь `headers` для хранения заголовков запроса.
   - Если `api_base` не передан, используется значение по умолчанию `cls.api_base`.
   - Если `api_key` не передан, но `cls.api_key` определен, используется значение `cls.api_key`.
   - Если `api_key` передан, в заголовок `Authorization` добавляется Bearer token.

3. **Выполнение запроса**:
   - Функция выполняет GET-запрос к конечной точке `/models` API OpenAI с использованием библиотеки `requests`.
   - Проверяется статус ответа с помощью `raise_for_status(response)`, чтобы убедиться, что запрос выполнен успешно.

4. **Обработка ответа**:
   - Функция преобразует JSON-ответ в структуру данных Python.
   - Извлекает список моделей из поля `data` в ответе. Если `data` является словарем, извлекается значение по ключу `data`, иначе используется само значение `data`.
   - Извлекает список моделей, поддерживающих изображения, из поля `image`.
   - Сохраняет список всех моделей в атрибут `cls.models`.
   - Если `cls.sort_models` имеет значение `True`, список моделей сортируется.

5. **Обработка ошибок**:
   - Если во время выполнения запроса или обработки ответа происходит исключение, оно перехватывается.
   - Информация об ошибке логируется с использованием `debug.error(e)`.
   - Возвращается список моделей из `cls.fallback_models`.

6. **Возврат результата**:
   - Если список моделей успешно получен, функция возвращает `cls.models`.

**ASCII flowchart**:

```
    A [Проверка cls.models]
    |
    B [Подготовка заголовков]
    |
    C [Выполнение GET-запроса к API]
    |
    D [Обработка ответа API]
    |
    E [Сохранение моделей в cls.models]
    |
    F [Обработка ошибок]
    |
    G [Возврат cls.models или cls.fallback_models]
```

**Примеры**:

```python
    >>> OpenaiTemplate.get_models(api_key='your_api_key')
    ['gpt-3.5-turbo', 'gpt-4', 'dall-e-3']
    >>> OpenaiTemplate.get_models()
    ['gpt-3.5-turbo', 'gpt-4', 'dall-e-3']
```

### `OpenaiTemplate.create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        timeout: int = 120,
        media: MediaListType = None,
        api_key: str = None,
        api_endpoint: str = None,
        api_base: str = None,
        temperature: float = None,
        max_tokens: int = None,
        top_p: float = None,
        stop: Union[str, list[str]] = None,
        stream: bool = False,
        prompt: str = None,
        headers: dict = None,
        impersonate: str = None,
        extra_parameters: list[str] = ["tools", "parallel_tool_calls", "tool_choice", "reasoning_effort", "logit_bias", "modalities", "audio"],
        extra_data: dict = {},
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для обработки сообщений с использованием API OpenAI.

        Args:
            model (str): Имя модели OpenAI.
            messages (Messages): Список сообщений для отправки в API.
            proxy (Optional[str]): URL прокси-сервера.
            timeout (int): Время ожидания запроса в секундах.
            media (Optional[MediaListType]): Список медиафайлов для отправки.
            api_key (Optional[str]): Ключ API OpenAI.
            api_endpoint (Optional[str]): Конечная точка API OpenAI.
            api_base (Optional[str]): Базовый URL API OpenAI.
            temperature (Optional[float]): Температура для генерации текста.
            max_tokens (Optional[int]): Максимальное количество токенов в ответе.
            top_p (Optional[float]): Значение top_p для генерации текста.
            stop (Optional[Union[str, list[str]]]): Список стоп-слов.
            stream (bool): Указывает, использовать ли потоковый режим.
            prompt (Optional[str]): Дополнительный промпт для отправки.
            headers (Optional[dict]): Дополнительные заголовки для запроса.
            impersonate (Optional[str]): Идентификатор для имитации пользователя.
            extra_parameters (list[str]): Список дополнительных параметров для передачи в API.
            extra_data (dict): Дополнительные данные для передачи в API.
            **kwargs: Дополнительные аргументы.

        Yields:
            Union[str, ToolCalls, Usage, FinishReason, ImageResponse]: Асинхронный генератор, возвращающий части ответа от API OpenAI.

        Raises:
            MissingAuthError: Если не указан API ключ и требуется аутентификация.
            ResponseError: Если получен неподдерживаемый content-type.
            Exception: Если происходит ошибка при выполнении запроса.

        Example:
            >>> async for response in OpenaiTemplate.create_async_generator(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'Hello'}]):
            ...     print(response)
            ...
            Hello!
        """
```

**Назначение**: Создает асинхронный генератор для взаимодействия с API OpenAI.

**Параметры**:
- `model` (str): Имя используемой модели.
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (Optional[str]): URL прокси-сервера (если используется).
- `timeout` (int): Максимальное время ожидания запроса.
- `media` (MediaListType): Список медиафайлов для отправки.
- `api_key` (Optional[str]): Ключ API.
- `api_endpoint` (Optional[str]): Конечная точка API.
- `api_base` (Optional[str]): Базовый URL API.
- `temperature` (float): Параметр температуры для генерации текста.
- `max_tokens` (int): Максимальное количество токенов в ответе.
- `top_p` (float): Параметр top_p для генерации текста.
- `stop` (Union[str, list[str]]): Список стоп-слов.
- `stream` (bool): Флаг, указывающий на использование потокового режима.
- `prompt` (str): Дополнительный промпт.
- `headers` (dict): Дополнительные заголовки.
- `impersonate` (str): Идентификатор для имитации пользователя.
- `extra_parameters` (list[str]): Список дополнительных параметров.
- `extra_data` (dict): Дополнительные данные.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, выдающий части ответа от API OpenAI. Тип возвращаемых значений может быть `str`, `ToolCalls`, `Usage`, `FinishReason`, `ImageResponse`.

**Вызывает исключения**:
- `MissingAuthError`: Если отсутствует ключ API при необходимости аутентификации.
- `ResponseError`: Если получен неподдерживаемый content-type.

**Как работает функция**:

1. **Инициализация**:
   - Проверяет наличие API-ключа и, если необходимо, вызывает исключение `MissingAuthError`, если ключ отсутствует.

2. **Создание сессии**:
   - Создает асинхронную сессию с использованием `StreamSession` для выполнения HTTP-запросов.
   - Устанавливает прокси, заголовки и время ожидания для сессии.

3. **Определение модели и базового URL**:
   - Получает модель с помощью `cls.get_model()`.
   - Определяет базовый URL API.

4. **Обработка запросов на генерацию изображений**:
   - Если модель поддерживает генерацию изображений (проверяется по `cls.image_models`), формирует запрос к API для генерации изображений.
   - Преобразует сообщения в промпт для генерации изображений с помощью `format_image_prompt()`.
   - Отправляет POST-запрос к конечной точке `/images/generations`.
   - Обрабатывает ответ, извлекая URL изображений и возвращая их в виде `ImageResponse`.

5. **Обработка текстовых запросов**:
   - Формирует словарь `data` с параметрами запроса, используя `filter_none()` для удаления параметров со значением `None`.
   - Определяет конечную точку API.
   - Отправляет POST-запрос к API.

6. **Обработка потоковых и не потоковых ответов**:
   - Проверяет `content_type` ответа:
     - Если `content_type` начинается с `application/json`, ответ обрабатывается как JSON.
     - Если `content_type` начинается с `text/event-stream`, ответ обрабатывается как потоковый.
     - В противном случае вызывается исключение `ResponseError`.

7. **Обработка JSON-ответов**:
   - Извлекает данные из JSON-ответа, включая контент сообщения, вызовы инструментов, информацию об использовании и причину завершения.
   - Возвращает извлеченные данные с помощью `yield`.

8. **Обработка потоковых ответов**:
   - Читает потоковые данные с использованием `response.sse()`.
   - Извлекает дельты контента, информацию об использовании и причину завершения.
   - Возвращает извлеченные данные с помощью `yield`.

9. **Обработка ошибок**:
   - В случае ошибки при выполнении запроса или обработке ответа, вызывается `cls.raise_error()` для обработки ошибки.
   - Для потоковых ответов также вызывается `raise_for_status()` для проверки статуса ответа.

**ASCII flowchart**:

```
    A [Проверка API-ключа]
    |
    B [Создание асинхронной сессии]
    |
    C [Определение модели и базового URL]
    |
    D [Проверка поддержки генерации изображений]
    |
    E [Формирование и отправка запроса на генерацию изображений (если поддерживается)]
    |
    F [Формирование словаря данных для текстового запроса]
    |
    G [Отправка POST-запроса к API]
    |
    H [Обработка потоковых и не потоковых ответов]
    |
    I [Обработка JSON-ответов]
    |
    J [Обработка потоковых ответов]
    |
    K [Обработка ошибок]
    |
    L [Возврат результатов через yield]
```

**Примеры**:

```python
    >>> async for response in OpenaiTemplate.create_async_generator(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'Напиши программу hello world на python'}]):
    ...     print(response)
    ...
    print("Hello, World!")
```

### `OpenaiTemplate.get_headers`

```python
    @classmethod
    def get_headers(cls, stream: bool, api_key: str = None, headers: dict = None) -> dict:
        """
        Возвращает словарь заголовков для запроса к API OpenAI.

        Args:
            stream (bool): Указывает, используется ли потоковый режим.
            api_key (Optional[str]): Ключ API OpenAI.
            headers (Optional[dict]): Дополнительные заголовки для запроса.

        Returns:
            dict: Словарь заголовков для запроса.

        Example:
            >>> headers = OpenaiTemplate.get_headers(stream=True, api_key='your_api_key')
            >>> print(headers)
            {'Accept': 'text/event-stream', 'Content-Type': 'application/json', 'Authorization': 'Bearer your_api_key'}
        """
```

**Назначение**: Формирует заголовки для HTTP-запроса к API OpenAI.

**Параметры**:
- `stream` (bool): Указывает, используется ли потоковый режим.
- `api_key` (Optional[str]): Ключ API OpenAI.
- `headers` (Optional[dict]): Дополнительные заголовки.

**Возвращает**:
- `dict`: Словарь заголовков, включающий `Accept`, `Content-Type` и, если предоставлен, `Authorization`.

**Как работает функция**:

1. **Определение типа содержимого `Accept`**:
   - В зависимости от значения параметра `stream` устанавливается заголовок `Accept`:
     - Если `stream` имеет значение `True`, устанавливается `text/event-stream`.
     - Если `stream` имеет значение `False`, устанавливается `application/json`.

2. **Установка типа содержимого `Content-Type`**:
   - Устанавливается заголовок `Content-Type` в значение `application/json`.

3. **Добавление заголовка авторизации**:
   - Если передан `api_key`, формируется заголовок `Authorization` с использованием Bearer token и добавляется в словарь заголовков.

4. **Добавление дополнительных заголовков**:
   - Если переданы дополнительные заголовки в параметре `headers`, они добавляются в словарь заголовков.

5. **Возврат словаря заголовков**:
   - Функция возвращает полученный словарь заголовков.

**ASCII flowchart**:

```
    A [Определение Accept в зависимости от stream]
    |
    B [Установка Content-Type]
    |
    C [Добавление Authorization, если api_key предоставлен]
    |
    D [Добавление дополнительных заголовков]
    |
    E [Возврат словаря заголовков]
```

**Примеры**:

```python
    >>> OpenaiTemplate.get_headers(stream=True, api_key='your_api_key')
    {'Accept': 'text/event-stream', 'Content-Type': 'application/json', 'Authorization': 'Bearer your_api_key'}
    >>> OpenaiTemplate.get_headers(stream=False)
    {'Accept': 'application/json', 'Content-Type': 'application/json'}
```
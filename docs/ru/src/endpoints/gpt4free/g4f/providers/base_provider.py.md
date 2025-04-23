# Модуль `base_provider`

## Обзор

Модуль `base_provider` содержит базовые классы и интерфейсы для реализации провайдеров, используемых для взаимодействия с различными моделями машинного обучения. Он определяет абстрактные классы для синхронных, асинхронных и асинхронных генераторных провайдеров, а также вспомогательные классы и функции для обработки параметров, ошибок и аутентификации.

## Подробней

Этот модуль предоставляет основу для создания новых провайдеров, которые могут быть использованы для генерации текста, обработки изображений и других задач машинного обучения. Он включает в себя абстрактные методы, которые должны быть реализованы в подклассах, а также общую логику для обработки параметров, аутентификации и управления ошибками.

## Содержание

- [Классы](#классы)
    - [AbstractProvider](#abstractprovider)
    - [AsyncProvider](#asyncprovider)
    - [AsyncGeneratorProvider](#asyncgeneratorprovider)
    - [ProviderModelMixin](#providermodelmixin)
    - [RaiseErrorMixin](#raiseerrormixin)
    - [AuthFileMixin](#authfilemixin)
    - [AsyncAuthedProvider](#asyncauthedprovider)
- [Переменные](#переменные)
    - [SAFE_PARAMETERS](#safe_parameters)
    - [BASIC_PARAMETERS](#basic_parameters)
    - [PARAMETER_EXAMPLES](#parameter_examples)

## Переменные

### `SAFE_PARAMETERS`

```python
SAFE_PARAMETERS = [
    "model", "messages", "stream", "timeout",
    "proxy", "media", "response_format",
    "prompt", "negative_prompt", "tools", "conversation",
    "history_disabled",
    "temperature",  "top_k", "top_p",
    "frequency_penalty", "presence_penalty",
    "max_tokens", "stop",
    "api_key", "api_base", "seed", "width", "height",
    "max_retries", "web_search",
    "guidance_scale", "num_inference_steps", "randomize_seed",
    "safe", "enhance", "private", "aspect_ratio", "n",
]
```

Список безопасных параметров, которые могут быть переданы в функцию создания.

### `BASIC_PARAMETERS`

```python
BASIC_PARAMETERS = {
    "provider": None,
    "model": "",
    "messages": [],
    "stream": False,
    "timeout": 0,
    "response_format": None,
    "max_tokens": 4096,
    "stop": ["stop1", "stop2"],
}
```

Словарь основных параметров с их значениями по умолчанию.

### `PARAMETER_EXAMPLES`

```python
PARAMETER_EXAMPLES = {
    "proxy": "http://user:password@127.0.0.1:3128",
    "temperature": 1,
    "top_k": 1,
    "top_p": 1,
    "frequency_penalty": 1,
    "presence_penalty": 1,
    "messages": [{"role": "system", "content": ""}, {"role": "user", "content": ""}],
    "media": [["data:image/jpeg;base64,...", "filename.jpg"]],
    "response_format": {"type": "json_object"},
    "conversation": {"conversation_id": "550e8400-e29b-11d4-a716-...", "message_id": "550e8400-e29b-11d4-a716-..."},
    "seed": 42,
    "tools": [],
}
```

Словарь примеров значений параметров.

## Классы

### `AbstractProvider`

**Описание**:
Абстрактный базовый класс для всех провайдеров.

**Методы**:

- `create_completion`
- `create_async`
- `get_create_function`
- `get_async_create_function`
- `get_parameters`
- `params`

#### `create_completion`

```python
@classmethod
@abstractmethod
def create_completion(
    cls,
    model: str,
    messages: Messages,
    stream: bool,
    **kwargs
) -> CreateResult:
    """
    Создает завершение с заданными параметрами.

    Args:
        model (str): Модель для использования.
        messages (Messages): Сообщения для обработки.
        stream (bool): Использовать ли потоковую передачу.
        **kwargs: Дополнительные именованные аргументы.

    Returns:
        CreateResult: Результат процесса создания.

    Raises:
        NotImplementedError: Если метод не переопределен в производных классах.
    """
```

#### `create_async`

```python
@classmethod
async def create_async(
    cls,
    model: str,
    messages: Messages,
    *,
    timeout: int = None,
    loop: AbstractEventLoop = None,
    executor: ThreadPoolExecutor = None,
    **kwargs
) -> str:
    """
    Асинхронно создает результат на основе заданной модели и сообщений.

    Args:
        cls (type): Класс, на котором вызывается этот метод.
        model (str): Модель для использования при создании.
        messages (Messages): Сообщения для обработки.
        loop (AbstractEventLoop, optional): Используемый цикл событий. По умолчанию `None`.
        executor (ThreadPoolExecutor, optional): Исполнитель для выполнения асинхронных задач. По умолчанию `None`.
        **kwargs: Дополнительные именованные аргументы.

    Returns:
        str: Созданный результат в виде строки.
    """
```

Как работает функция:
- Извлекает текущий цикл событий, если он не был предоставлен.
- Определяет внутреннюю функцию `create_func`, которая вызывает `cls.create_completion` с предоставленными аргументами и объединяет результаты.
- Запускает `create_func` в executor и ожидает завершения с использованием `asyncio.wait_for` и заданного `timeout`.

#### `get_create_function`

```python
@classmethod
def get_create_function(cls) -> callable:
    """
    Возвращает функцию создания.

    Returns:
        callable: Функция создания.
    """
```

#### `get_async_create_function`

```python
@classmethod
def get_async_create_function(cls) -> callable:
    """
    Возвращает асинхронную функцию создания.

    Returns:
        callable: Асинхронная функция создания.
    """
```

#### `get_parameters`

```python
@classmethod
def get_parameters(cls, as_json: bool = False) -> dict[str, Parameter]:
    """
    Возвращает параметры, поддерживаемые провайдером.

    Args:
        cls (type): Класс, на котором вызывается этот метод.
        as_json (bool): Возвращать ли параметры в формате JSON.

    Returns:
        dict[str, Parameter]: Словарь параметров.
    """
```

Как работает функция:
- Извлекает параметры из сигнатуры функции `create_async_generator` (если класс является `AsyncGeneratorProvider`), `create_async` (если класс является `AsyncProvider`) или `create_completion`.
- Фильтрует параметры, оставляя только те, которые находятся в списке `SAFE_PARAMETERS` и поддерживают потоковую передачу (если `stream` не является `False`).
- Если `as_json` равен `True`, преобразует параметры в формат JSON, используя примеры значений и типы данных.

#### `params`

```python
@classmethod
@property
def params(cls) -> str:
    """
    Возвращает параметры, поддерживаемые провайдером.

    Args:
        cls (type): Класс, на котором вызывается этот метод.

    Returns:
        str: Строка, перечисляющая поддерживаемые параметры.
    """
```

Как работает функция:
- Определяет внутреннюю функцию `get_type_name`, которая возвращает имя типа аннотации.
- Формирует строку, перечисляющую поддерживаемые параметры, их типы и значения по умолчанию.

### `AsyncProvider`

**Описание**:
Предоставляет асинхронную функциональность для создания завершений.

**Наследует**:
- `AbstractProvider`

**Методы**:

- `create_completion`
- `create_async`
- `get_create_function`
- `get_async_create_function`

#### `create_completion`

```python
@classmethod
def create_completion(
    cls,
    model: str,
    messages: Messages,
    stream: bool = False,
    **kwargs
) -> CreateResult:
    """
    Создает результат завершения синхронно.

    Args:
        cls (type): Класс, на котором вызывается этот метод.
        model (str): Модель для использования при создании.
        messages (Messages): Сообщения для обработки.
        stream (bool): Указывает, следует ли передавать результаты потоком. По умолчанию `False`.
        **kwargs: Дополнительные именованные аргументы.

    Returns:
        CreateResult: Результат создания завершения.
    """
```

Как работает функция:
- Проверяет, запущен ли цикл событий.
- Запускает асинхронное создание и возвращает результат.

#### `create_async`

```python
@staticmethod
@abstractmethod
async def create_async(
    model: str,
    messages: Messages,
    **kwargs
) -> str:
    """
    Абстрактный метод для создания асинхронных результатов.

    Args:
        model (str): Модель для использования при создании.
        messages (Messages): Сообщения для обработки.
        **kwargs: Дополнительные именованные аргументы.

    Raises:
        NotImplementedError: Если этот метод не переопределен в производных классах.

    Returns:
        str: Созданный результат в виде строки.
    """
```

#### `get_create_function`

```python
@classmethod
def get_create_function(cls) -> callable:
    """
    Возвращает функцию создания.

    Returns:
        callable: Функция создания.
    """
```

#### `get_async_create_function`

```python
@classmethod
def get_async_create_function(cls) -> callable:
    """
    Возвращает асинхронную функцию создания.

    Returns:
        callable: Асинхронная функция создания.
    """
```

### `AsyncGeneratorProvider`

**Описание**:
Предоставляет функциональность асинхронного генератора для потоковой передачи результатов.

**Наследует**:
- `AbstractProvider`

**Атрибуты**:
- `supports_stream` (bool): Флаг, указывающий, поддерживает ли провайдер потоковую передачу.

**Методы**:

- `create_completion`
- `create_async_generator`
- `get_create_function`
- `get_async_create_function`

#### `create_completion`

```python
@classmethod
def create_completion(
    cls,
    model: str,
    messages: Messages,
    stream: bool = True,
    **kwargs
) -> CreateResult:
    """
    Создает результат потокового завершения синхронно.

    Args:
        cls (type): Класс, на котором вызывается этот метод.
        model (str): Модель для использования при создании.
        messages (Messages): Сообщения для обработки.
        stream (bool): Указывает, следует ли передавать результаты потоком. По умолчанию `True`.
        **kwargs: Дополнительные именованные аргументы.

    Returns:
        CreateResult: Результат создания потокового завершения.
    """
```

Как работает функция:
- Преобразует асинхронный генератор в синхронный генератор с использованием `to_sync_generator`.

#### `create_async_generator`

```python
@staticmethod
@abstractmethod
async def create_async_generator(
    model: str,
    messages: Messages,
    stream: bool = True,
    **kwargs
) -> AsyncResult:
    """
    Абстрактный метод для создания асинхронного генератора.

    Args:
        model (str): Модель для использования при создании.
        messages (Messages): Сообщения для обработки.
        stream (bool): Указывает, следует ли передавать результаты потоком. По умолчанию `True`.
        **kwargs: Дополнительные именованные аргументы.

    Raises:
        NotImplementedError: Если этот метод не переопределен в производных классах.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий результаты.
    """
```

#### `get_create_function`

```python
@classmethod
def get_create_function(cls) -> callable:
    """
    Возвращает функцию создания.

    Returns:
        callable: Функция создания.
    """
```

#### `get_async_create_function`

```python
@classmethod
def get_async_create_function(cls) -> callable:
    """
    Возвращает асинхронную функцию создания.

    Returns:
        callable: Асинхронная функция создания.
    """
```

### `ProviderModelMixin`

**Описание**:
Миксин для добавления информации о моделях, поддерживаемых провайдером.

**Атрибуты**:
- `default_model` (str): Модель по умолчанию.
- `models` (list[str]): Список поддерживаемых моделей.
- `model_aliases` (dict[str, str]): Словарь псевдонимов моделей.
- `image_models` (list): Список моделей для работы с изображениями.
- `vision_models` (list): Список моделей для компьютерного зрения.
- `last_model` (str): Последняя использованная модель.

**Методы**:

- `get_models`
- `get_model`

#### `get_models`

```python
@classmethod
def get_models(cls, **kwargs) -> list[str]:
    """
    Возвращает список моделей, поддерживаемых провайдером.

    Args:
        cls (type): Класс, на котором вызывается этот метод.
        **kwargs: Дополнительные именованные аргументы.

    Returns:
        list[str]: Список поддерживаемых моделей.
    """
```

#### `get_model`

```python
@classmethod
def get_model(cls, model: str, **kwargs) -> str:
    """
    Возвращает модель, используя псевдоним или модель по умолчанию, если модель не указана.

    Args:
        cls (type): Класс, на котором вызывается этот метод.
        model (str): Модель для использования.
        **kwargs: Дополнительные именованные аргументы.

    Returns:
        str: Имя модели.

    Raises:
        ModelNotSupportedError: Если модель не поддерживается.
    """
```

Как работает функция:

- Если `model` не указана и `cls.default_model` определена, возвращает `cls.default_model`.
- Если `model` есть в `cls.model_aliases`, возвращает соответствующий псевдоним.
- Если `model` нет в списке `cls.models`, вызывает исключение `ModelNotSupportedError`.
- В противном случае возвращает исходную `model`.

### `RaiseErrorMixin`

**Описание**:
Миксин для обработки ошибок, возвращаемых провайдером.

**Методы**:

- `raise_error`

#### `raise_error`

```python
@staticmethod
def raise_error(data: dict, status: int = None):
    """
    Вызывает исключение на основе данных об ошибке.

    Args:
        data (dict): Данные об ошибке.
        status (int, optional): HTTP-статус код. По умолчанию `None`.

    Raises:
        ResponseError: Если в данных есть сообщение об ошибке.
        MissingAuthError: Если статус 401 и в данных есть сообщение об ошибке.
        PaymentRequiredError: Если статус 402 и в данных есть сообщение об ошибке.
    """
```

Как работает функция:
- Проверяет наличие ключей `"error_message"` или `"error"` в словаре `data`.
- В зависимости от структуры данных об ошибке, вызывает соответствующее исключение (`ResponseError`, `MissingAuthError`, `PaymentRequiredError`).

### `AuthFileMixin`

**Описание**:
Миксин для управления файлом кэша аутентификации.

**Методы**:

- `get_cache_file`

#### `get_cache_file`

```python
@classmethod
def get_cache_file(cls) -> Path:
    """
    Возвращает путь к файлу кэша.

    Returns:
        Path: Путь к файлу кэша.
    """
```

Как работает функция:
- Возвращает путь к файлу кэша аутентификации, который находится в директории cookies и имеет имя `auth_{имя_класса}.json`.

### `AsyncAuthedProvider`

**Описание**:
Предоставляет функциональность асинхронной аутентификации для провайдеров.

**Наследует**:
- `AsyncGeneratorProvider`
- `AuthFileMixin`

**Методы**:

- `on_auth_async`
- `on_auth`
- `get_create_function`
- `get_async_create_function`
- `write_cache_file`
- `create_completion`
- `create_async_generator`

#### `on_auth_async`

```python
@classmethod
async def on_auth_async(cls, **kwargs) -> AuthResult:
    """
    Асинхронно выполняет аутентификацию.

    Args:
        **kwargs: Дополнительные именованные аргументы.

    Returns:
        AuthResult: Результат аутентификации.

    Raises:
        MissingAuthError: Если отсутствует API key.
    """
```

Как работает функция:
- Проверяет наличие API key в аргументах.
- Если API key отсутствует, вызывает исключение `MissingAuthError`.
- В противном случае возвращает `AuthResult`.

#### `on_auth`

```python
@classmethod
def on_auth(cls, **kwargs) -> AuthResult:
    """
    Выполняет аутентификацию.

    Args:
        **kwargs: Дополнительные именованные аргументы.

    Returns:
        AuthResult: Результат аутентификации.
    """
```

Как работает функция:
- Вызывает асинхронный метод `on_auth_async` и возвращает результат.

#### `get_create_function`

```python
@classmethod
def get_create_function(cls) -> callable:
    """
    Возвращает функцию создания.

    Returns:
        callable: Функция создания.
    """
```

#### `get_async_create_function`

```python
@classmethod
def get_async_create_function(cls) -> callable:
    """
    Возвращает асинхронную функцию создания.

    Returns:
        callable: Асинхронная функция создания.
    """
```

#### `write_cache_file`

```python
@classmethod
def write_cache_file(cls, cache_file: Path, auth_result: AuthResult = None):
    """
    Записывает результат аутентификации в файл кэша.

    Args:
        cache_file (Path): Путь к файлу кэша.
        auth_result (AuthResult, optional): Результат аутентификации. По умолчанию `None`.
    """
```

Как работает функция:
- Создает родительские директории для файла кэша, если они не существуют.
- Записывает словарь из `auth_result` в файл кэша в формате JSON.
- Если `auth_result` равен `None`, удаляет файл кэша, если он существует.

#### `create_completion`

```python
@classmethod
def create_completion(
    cls,
    model: str,
    messages: Messages,
    **kwargs
) -> CreateResult:
    """
    Создает завершение с аутентификацией.

    Args:
        model (str): Модель для использования.
        messages (Messages): Сообщения для обработки.
        **kwargs: Дополнительные именованные аргументы.

    Returns:
        CreateResult: Результат создания завершения.
    """
```

Как работает функция:
- Пытается загрузить результат аутентификации из файла кэша.
- Если файл кэша не существует или аутентификация не удалась, выполняет аутентификацию с помощью `cls.on_auth`.
- После успешной аутентификации вызывает `cls.create_authed` для создания завершения с аутентификацией.
- Записывает результат аутентификации в файл кэша.

#### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор с аутентификацией.

    Args:
        model (str): Модель для использования.
        messages (Messages): Сообщения для обработки.
        **kwargs: Дополнительные именованные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор.
    """
```

Как работает функция:
- Пытается загрузить результат аутентификации из файла кэша.
- Если файл кэша не существует или аутентификация не удалась, выполняет асинхронную аутентификацию с помощью `cls.on_auth_async`.
- После успешной аутентификации вызывает `cls.create_authed` для создания завершения с аутентификацией.
- Записывает результат аутентификации в файл кэша.
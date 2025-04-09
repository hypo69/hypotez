# Модуль `base_provider.py`

## Обзор

Модуль `base_provider.py` содержит базовые классы и абстрактные методы для реализации различных провайдеров, используемых для взаимодействия с моделями генерации текста, таких как GPT-4. Он определяет интерфейсы для создания завершений (completion), асинхронной обработки и потоковой передачи результатов.

## Подробнее

Модуль предоставляет абстрактные классы, которые служат основой для создания конкретных реализаций провайдеров. Эти классы определяют основные методы, которые должны быть реализованы в каждом провайдере, такие как `create_completion`, `create_async` и `create_async_generator`. Кроме того, модуль содержит вспомогательные функции и классы для обработки параметров, аутентификации и кэширования.

## Содержание

1.  [Константы](#константы)
2.  [Классы](#классы)
    *   [AbstractProvider](#abstractprovider)
    *   [AsyncProvider](#asyncprovider)
    *   [AsyncGeneratorProvider](#asyncgeneratorprovider)
    *   [ProviderModelMixin](#providermodelmixin)
    *   [RaiseErrorMixin](#raiseerrormixin)
    *   [AuthFileMixin](#authfilemixin)
    *   [AsyncAuthedProvider](#asyncauthedprovider)

## Константы

### `SAFE_PARAMETERS`
Список безопасных параметров, которые можно передавать в функции создания завершений.
### `BASIC_PARAMETERS`
Словарь базовых параметров с значениями по умолчанию.
### `PARAMETER_EXAMPLES`
Словарь, содержащий примеры значений параметров, используемых в запросах к моделям.

## Классы

### `AbstractProvider`

**Описание**:
Абстрактный класс, определяющий интерфейс для всех провайдеров.

**Методы**:

*   `create_completion`
*   `create_async`
*   `get_create_function`
*   `get_async_create_function`
*   `get_parameters`
*   `params`

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
        Create a completion with the given parameters.

        Args:
            model (str): The model to use.
            messages (Messages): The messages to process.
            stream (bool): Whether to use streaming.
            **kwargs: Additional keyword arguments.

        Returns:
            CreateResult: The result of the creation process.
        """
```

**Назначение**:
Абстрактный метод для создания завершения (completion) на основе предоставленных параметров.

**Параметры**:

*   `model` (str): Имя модели, которую необходимо использовать.
*   `messages` (Messages): Список сообщений для обработки.
*   `stream` (bool): Флаг, указывающий, использовать ли потоковую передачу.
*   `**kwargs`: Дополнительные именованные аргументы.

**Возвращает**:

*   `CreateResult`: Результат создания завершения.

**Вызывает исключения**:

*   `NotImplementedError`: Если метод не реализован в подклассе.

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
        Asynchronously creates a result based on the given model and messages.

        Args:
            cls (type): The class on which this method is called.
            model (str): The model to use for creation.
            messages (Messages): The messages to process.
            loop (AbstractEventLoop, optional): The event loop to use. Defaults to None.
            executor (ThreadPoolExecutor, optional): The executor for running async tasks. Defaults to None.
            **kwargs: Additional keyword arguments.

        Returns:
            str: The created result as a string.
        """
```

**Назначение**:
Асинхронный метод для создания результата на основе предоставленной модели и сообщений.

**Параметры**:

*   `cls` (type): Класс, в котором вызывается этот метод.
*   `model` (str): Имя модели, которую необходимо использовать.
*   `messages` (Messages): Список сообщений для обработки.
*   `timeout` (int, optional): Максимальное время ожидания выполнения операции. По умолчанию `None`.
*   `loop` (AbstractEventLoop, optional): Экземпляр event loop для использования. По умолчанию `None`.
*   `executor` (ThreadPoolExecutor, optional): Экземпляр ThreadPoolExecutor для выполнения асинхронных задач. По умолчанию `None`.
*   `**kwargs`: Дополнительные именованные аргументы.

**Возвращает**:

*   `str`: Созданный результат в виде строки.

**Как работает функция**:

1.  Определяет текущий event loop, если он не был передан в качестве аргумента.
2.  Определяет функцию `create_func`, которая вызывает метод `create_completion` для создания завершения.
3.  Запускает `create_func` в executor и ожидает результат в течение заданного времени ожидания.

ASCII схема:

```
Начало -> Получение event loop -> Определение create_func -> Запуск create_func в executor -> Ожидание результата -> Конец
```

**Примеры**:
```python
# Пример вызова create_async с указанием model и messages
result = AbstractProvider.create_async(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello"}])

# Пример вызова create_async с указанием timeout
result = AbstractProvider.create_async(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello"}], timeout=10)
```

#### `get_create_function`

```python
    @classmethod
    def get_create_function(cls) -> callable:
        return cls.create_completion
```

**Назначение**:
Возвращает функцию создания завершения.

**Параметры**:

*   `cls` (type): Класс, для которого вызывается этот метод.

**Возвращает**:

*   `callable`: Функция создания завершения.

#### `get_async_create_function`

```python
    @classmethod
    def get_async_create_function(cls) -> callable:
        return cls.create_async
```

**Назначение**:
Возвращает асинхронную функцию создания.

**Параметры**:

*   `cls` (type): Класс, для которого вызывается этот метод.

**Возвращает**:

*   `callable`: Асинхронная функция создания.

#### `get_parameters`

```python
    @classmethod
    def get_parameters(cls, as_json: bool = False) -> dict[str, Parameter]:
        params = {name: parameter for name, parameter in signature(
            cls.create_async_generator if issubclass(cls, AsyncGeneratorProvider) else
            cls.create_async if issubclass(cls, AsyncProvider) else
            cls.create_completion
        ).parameters.items() if name in SAFE_PARAMETERS
            and (name != "stream" or cls.supports_stream)}
        if as_json:
            def get_type_as_var(annotation: type, key: str, default):
                if key in PARAMETER_EXAMPLES:
                    if key == "messages" and not cls.supports_system_message:
                        return [PARAMETER_EXAMPLES[key][-1]]
                    return PARAMETER_EXAMPLES[key]
                if isinstance(annotation, type):
                    if issubclass(annotation, int):
                        return 0
                    elif issubclass(annotation, float):
                        return 0.0
                    elif issubclass(annotation, bool):
                        return False
                    elif issubclass(annotation, str):
                        return ""
                    elif issubclass(annotation, dict):
                        return {}
                    elif issubclass(annotation, list):
                        return []
                    elif issubclass(annotation, BaseConversation):
                        return {}
                    elif issubclass(annotation, NoneType):
                        return {}
                elif annotation is None:
                    return None
                elif annotation == "str" or annotation == "list[str]":
                    return default
                elif isinstance(annotation, _GenericAlias):
                    if annotation.__origin__ is Optional:
                        return get_type_as_var(annotation.__args__[0])
                else:
                    return str(annotation)
            return { name: (
                param.default
                if isinstance(param, Parameter) and param.default is not Parameter.empty and param.default is not None
                else get_type_as_var(param.annotation, name, param.default) if isinstance(param, Parameter) else param
            ) for name, param in {
                **BASIC_PARAMETERS,
                **params,
                **{"provider": cls.__name__, "model": getattr(cls, "default_model", ""), "stream": cls.supports_stream},
            }.items()}
        return params
```

**Назначение**:
Возвращает параметры, поддерживаемые провайдером.

**Параметры**:

*   `cls` (type): Класс, для которого вызывается этот метод.
*   `as_json` (bool, optional): Если `True`, возвращает параметры в формате JSON. По умолчанию `False`.

**Возвращает**:

*   `dict[str, Parameter]`: Словарь параметров, поддерживаемых провайдером.

**Внутренние функции**:
*   `get_type_as_var(annotation: type, key: str, default)` - вспомогательная функция, которая определяет тип переменной и возвращает соответствующее значение по умолчанию.

**Как работает функция**:

1.  Определяет функцию, которая будет использоваться для получения параметров в зависимости от того, поддерживает ли класс асинхронную генерацию или асинхронный вызов.
2.  Получает параметры из сигнатуры выбранной функции.
3.  Фильтрует параметры, оставляя только те, которые находятся в списке безопасных параметров (`SAFE_PARAMETERS`) и поддерживают потоковую передачу, если это указано.
4.  Если `as_json` равен `True`, преобразует параметры в формат JSON, используя значения по умолчанию и примеры значений из `PARAMETER_EXAMPLES`.
5.  Возвращает словарь параметров.

ASCII схема:

```
Начало -> Определение функции получения параметров -> Получение параметров из сигнатуры -> Фильтрация параметров -> Преобразование в JSON (если необходимо) -> Возврат словаря параметров -> Конец
```

**Примеры**:
```python
# Пример вызова get_parameters без преобразования в JSON
parameters = AbstractProvider.get_parameters()

# Пример вызова get_parameters с преобразованием в JSON
parameters = AbstractProvider.get_parameters(as_json=True)
```

#### `params`

```python
    @classmethod
    @property
    def params(cls) -> str:
        """
        Returns the parameters supported by the provider.

        Args:
            cls (type): The class on which this property is called.

        Returns:
            str: A string listing the supported parameters.
        """
```

**Назначение**:
Возвращает строку с описанием параметров, поддерживаемых провайдером.

**Параметры**:

*   `cls` (type): Класс, для которого вызывается этот метод.

**Возвращает**:

*   `str`: Строка с перечислением поддерживаемых параметров.

**Внутренние функции**:

*   `get_type_name(annotation: type)`: вспомогательная функция, возвращает имя типа аннотации.

**Как работает функция**:

1.  Получает словарь параметров с помощью метода `get_parameters`.
2.  Формирует строку, перечисляющую параметры и их типы, а также значения по умолчанию.

ASCII схема:

```
Начало -> Получение параметров -> Формирование строки с описанием параметров -> Возврат строки -> Конец
```

**Примеры**:
```python
# Пример вызова params
parameters_string = AbstractProvider.params
```

### `AsyncProvider`

**Описание**:
Класс, предоставляющий асинхронную функциональность для создания завершений. Наследует `AbstractProvider`.

**Наследует**:

*   `AbstractProvider`

**Методы**:

*   `create_completion`
*   `create_async`
*   `get_create_function`
*   `get_async_create_function`

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
        Creates a completion result synchronously.

        Args:
            cls (type): The class on which this method is called.
            model (str): The model to use for creation.
            messages (Messages): The messages to process.
            stream (bool): Indicates whether to stream the results. Defaults to False.
            loop (AbstractEventLoop, optional): The event loop to use. Defaults to None.
            **kwargs: Additional keyword arguments.

        Returns:
            CreateResult: The result of the completion creation.
        """
```

**Назначение**:
Синхронно создает результат завершения.

**Параметры**:

*   `cls` (type): Класс, для которого вызывается этот метод.
*   `model` (str): Имя модели, которую необходимо использовать.
*   `messages` (Messages): Список сообщений для обработки.
*   `stream` (bool, optional): Флаг, указывающий, использовать ли потоковую передачу. По умолчанию `False`.
*   `**kwargs`: Дополнительные именованные аргументы.

**Возвращает**:

*   `CreateResult`: Результат создания завершения.

**Как работает функция**:

1.  Получает текущий event loop.
2.  Запускает асинхронный метод `create_async` и возвращает результат.

ASCII схема:

```
Начало -> Получение event loop -> Запуск create_async -> Возврат результата -> Конец
```

**Примеры**:
```python
# Пример вызова create_completion
result = AsyncProvider.create_completion(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello"}])
```

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
        Abstract method for creating asynchronous results.

        Args:
            model (str): The model to use for creation.
            messages (Messages): The messages to process.
            **kwargs: Additional keyword arguments.

        Raises:
            NotImplementedError: If this method is not overridden in derived classes.

        Returns:
            str: The created result as a string.
        """
```

**Назначение**:
Абстрактный метод для создания асинхронных результатов.

**Параметры**:

*   `model` (str): Имя модели, которую необходимо использовать.
*   `messages` (Messages): Список сообщений для обработки.
*   `**kwargs`: Дополнительные именованные аргументы.

**Вызывает исключения**:

*   `NotImplementedError`: Если метод не реализован в подклассе.

**Возвращает**:

*   `str`: Созданный результат в виде строки.

#### `get_create_function`

```python
    @classmethod
    def get_create_function(cls) -> callable:
        return cls.create_completion
```

**Назначение**:
Возвращает функцию создания завершения.

**Параметры**:

*   `cls` (type): Класс, для которого вызывается этот метод.

**Возвращает**:

*   `callable`: Функция создания завершения.

#### `get_async_create_function`

```python
    @classmethod
    def get_async_create_function(cls) -> callable:
        return cls.create_async
```

**Назначение**:
Возвращает асинхронную функцию создания.

**Параметры**:

*   `cls` (type): Класс, для которого вызывается этот метод.

**Возвращает**:

*   `callable`: Асинхронная функция создания.

### `AsyncGeneratorProvider`

**Описание**:
Класс, предоставляющий асинхронную функциональность генератора для потоковой передачи результатов. Наследует `AbstractProvider`.

**Наследует**:

*   `AbstractProvider`

**Атрибуты**:

*   `supports_stream` (bool): Флаг, указывающий, поддерживает ли провайдер потоковую передачу.

**Методы**:

*   `create_completion`
*   `create_async_generator`
*   `get_create_function`
*   `get_async_create_function`

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
        Creates a streaming completion result synchronously.

        Args:
            cls (type): The class on which this method is called.
            model (str): The model to use for creation.
            messages (Messages): The messages to process.
            stream (bool): Indicates whether to stream the results. Defaults to True.
            loop (AbstractEventLoop, optional): The event loop to use. Defaults to None.
            **kwargs: Additional keyword arguments.

        Returns:
            CreateResult: The result of the streaming completion creation.
        """
```

**Назначение**:
Синхронно создает результат потокового завершения.

**Параметры**:

*   `cls` (type): Класс, для которого вызывается этот метод.
*   `model` (str): Имя модели, которую необходимо использовать.
*   `messages` (Messages): Список сообщений для обработки.
*   `stream` (bool, optional): Флаг, указывающий, использовать ли потоковую передачу. По умолчанию `True`.
*   `**kwargs`: Дополнительные именованные аргументы.

**Возвращает**:

*   `CreateResult`: Результат создания потокового завершения.

**Как работает функция**:

1.  Преобразует асинхронный генератор `create_async_generator` в синхронный генератор с помощью функции `to_sync_generator`.
2.  Возвращает синхронный генератор.

ASCII схема:

```
Начало -> Преобразование асинхронного генератора в синхронный -> Возврат синхронного генератора -> Конец
```

**Примеры**:
```python
# Пример вызова create_completion
result = AsyncGeneratorProvider.create_completion(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello"}])
```

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
        Abstract method for creating an asynchronous generator.

        Args:
            model (str): The model to use for creation.
            messages (Messages): The messages to process.
            stream (bool): Indicates whether to stream the results. Defaults to True.
            **kwargs: Additional keyword arguments.

        Raises:
            NotImplementedError: If this method is not overridden in derived classes.

        Returns:
            AsyncResult: An asynchronous generator yielding results.
        """
```

**Назначение**:
Абстрактный метод для создания асинхронного генератора.

**Параметры**:

*   `model` (str): Имя модели, которую необходимо использовать.
*   `messages` (Messages): Список сообщений для обработки.
*   `stream` (bool, optional): Флаг, указывающий, использовать ли потоковую передачу. По умолчанию `True`.
*   `**kwargs`: Дополнительные именованные аргументы.

**Вызывает исключения**:

*   `NotImplementedError`: Если метод не реализован в подклассе.

**Возвращает**:

*   `AsyncResult`: Асинхронный генератор, выдающий результаты.

#### `get_create_function`

```python
    @classmethod
    def get_create_function(cls) -> callable:
        return cls.create_completion
```

**Назначение**:
Возвращает функцию создания завершения.

**Параметры**:

*   `cls` (type): Класс, для которого вызывается этот метод.

**Возвращает**:

*   `callable`: Функция создания завершения.

#### `get_async_create_function`

```python
    @classmethod
    def get_async_create_function(cls) -> callable:
        return cls.create_async_generator
```

**Назначение**:
Возвращает асинхронную функцию генератора.

**Параметры**:

*   `cls` (type): Класс, для которого вызывается этот метод.

**Возвращает**:

*   `callable`: Асинхронная функция генератора.

### `ProviderModelMixin`

**Описание**:
Миксин, предоставляющий функциональность для работы с моделями провайдера.

**Атрибуты**:

*   `default_model` (str): Модель, используемая по умолчанию.
*   `models` (list[str]): Список поддерживаемых моделей.
*   `model_aliases` (dict[str, str]): Словарь псевдонимов моделей.
*   `image_models` (list): Список моделей для обработки изображений.
*   `vision_models` (list): Список моделей для обработки видео.
*   `last_model` (str): Последняя использованная модель.

**Методы**:

*   `get_models`
*   `get_model`

#### `get_models`

```python
    @classmethod
    def get_models(cls, **kwargs) -> list[str]:
        if not cls.models and cls.default_model is not None:
            return [cls.default_model]
        return cls.models
```

**Назначение**:
Возвращает список поддерживаемых моделей.

**Параметры**:

*   `cls` (type): Класс, для которого вызывается этот метод.
*   `**kwargs`: Дополнительные именованные аргументы.

**Возвращает**:

*   `list[str]`: Список поддерживаемых моделей.

**Как работает функция**:

1.  Если список моделей пуст, но задана модель по умолчанию, возвращает список, содержащий только модель по умолчанию.
2.  В противном случае возвращает список поддерживаемых моделей.

ASCII схема:

```
Начало -> Проверка списка моделей -> Если пуст и есть модель по умолчанию: возврат списка с моделью по умолчанию -> Иначе: возврат списка моделей -> Конец
```

**Примеры**:
```python
# Пример вызова get_models
models = ProviderModelMixin.get_models()
```

#### `get_model`

```python
    @classmethod
    def get_model(cls, model: str, **kwargs) -> str:
        if not model and cls.default_model is not None:
            model = cls.default_model
        elif model in cls.model_aliases:
            model = cls.model_aliases[model]
        else:
            if model not in cls.get_models(**kwargs) and cls.models:
                raise ModelNotSupportedError(f"Model is not supported: {model} in: {cls.__name__} Valid models: {cls.models}")
        cls.last_model = model
        debug.last_model = model
        return model
```

**Назначение**:
Возвращает имя модели на основе предоставленного имени и псевдонимов.

**Параметры**:

*   `cls` (type): Класс, для которого вызывается этот метод.
*   `model` (str): Имя модели.
*   `**kwargs`: Дополнительные именованные аргументы.

**Возвращает**:

*   `str`: Имя модели.

**Вызывает исключения**:

*   `ModelNotSupportedError`: Если модель не поддерживается.

**Как работает функция**:

1.  Если имя модели не предоставлено, но задана модель по умолчанию, использует модель по умолчанию.
2.  Если имя модели есть в словаре псевдонимов, использует псевдоним.
3.  Если имя модели не поддерживается, вызывает исключение `ModelNotSupportedError`.
4.  Сохраняет имя модели в атрибуте `last_model` и возвращает его.

ASCII схема:

```
Начало -> Проверка имени модели -> Если не предоставлено и есть модель по умолчанию: использование модели по умолчанию -> Если есть псевдоним: использование псевдонима -> Если модель не поддерживается: вызов исключения -> Сохранение имени модели -> Возврат имени модели -> Конец
```

**Примеры**:
```python
# Пример вызова get_model
model = ProviderModelMixin.get_model(model="gpt-3.5-turbo")
```

### `RaiseErrorMixin`

**Описание**:
Миксин, предоставляющий функциональность для обработки ошибок.

**Методы**:

*   `raise_error`

#### `raise_error`

```python
    @staticmethod
    def raise_error(data: dict, status: int = None):
        if "error_message" in data:
            raise ResponseError(data["error_message"])
        elif "error" in data:
            if isinstance(data["error"], str):
                if status is not None:
                    if status == 401:
                        raise MissingAuthError(f"Error {status}: {data['error']}")
                    elif status == 402:
                        raise PaymentRequiredError(f"Error {status}: {data['error']}")
                    raise ResponseError(f"Error {status}: {data['error']}")
                raise ResponseError(data["error"])
            elif isinstance(data["error"], bool):
                raise ResponseError(data)
            elif "code" in data["error"]:\n                raise ResponseError("\\n".join(\n                    [e for e in [f\'Error {data["error"]["code"]}: {data["error"]["message"]}\', data["error"].get("failed_generation")] if e is not None]\n                ))\n            elif "message" in data["error"]:\n                raise ResponseError(data["error"]["message"])\n            else:\n                raise ResponseError(data["error"])\n        elif ("choices" not in data or not data["choices"]) and "data" not in data:\n            raise ResponseError(f"Invalid response: {json.dumps(data)}")
```

**Назначение**:
Вызывает исключение на основе предоставленных данных об ошибке.

**Параметры**:

*   `data` (dict): Данные об ошибке.
*   `status` (int, optional): HTTP-статус ошибки. По умолчанию `None`.

**Вызывает исключения**:

*   `ResponseError`: Если в данных есть сообщение об ошибке.
*   `MissingAuthError`: Если статус ошибки 401 (необходима аутентификация).
*   `PaymentRequiredError`: Если статус ошибки 402 (необходима оплата).

**Как работает функция**:

1.  Проверяет наличие ключа "error_message" в данных. Если он есть, вызывает исключение `ResponseError` с соответствующим сообщением.
2.  Если ключ "error_message" отсутствует, проверяет наличие ключа "error".
3.  Если ключ "error" содержит строку, вызывает исключение `ResponseError` с соответствующим сообщением и HTTP-статусом (если он предоставлен).
4.  Если ключ "error" содержит логическое значение, вызывает исключение `ResponseError` с данными об ошибке.
5.  Если в данных нет ни "choices", ни "data", вызывает исключение `ResponseError` с сообщением о неверном ответе.

ASCII схема:

```
Начало -> Проверка "error_message" -> Если есть: вызов ResponseError -> Проверка "error" -> Если есть строка: вызов ResponseError с HTTP-статусом -> Если есть bool: вызов ResponseError -> Проверка наличия "choices" или "data" -> Если отсутствуют: вызов ResponseError -> Конец
```

**Примеры**:
```python
# Пример вызова raise_error с сообщением об ошибке
RaiseErrorMixin.raise_error(data={"error_message": "Something went wrong"})

# Пример вызова raise_error с HTTP-статусом
RaiseErrorMixin.raise_error(data={"error": "Unauthorized"}, status=401)
```

### `AuthFileMixin`

**Описание**:
Миксин, предоставляющий функциональность для работы с файлом аутентификации.

**Методы**:

*   `get_cache_file`

#### `get_cache_file`

```python
    @classmethod
    def get_cache_file(cls) -> Path:
        return Path(get_cookies_dir()) / f"auth_{cls.parent if hasattr(cls, 'parent') else cls.__name__}.json"
```

**Назначение**:
Возвращает путь к файлу кэша.

**Параметры**:

*   `cls` (type): Класс, для которого вызывается этот метод.

**Возвращает**:

*   `Path`: Путь к файлу кэша.

**Как работает функция**:

1.  Получает директорию для хранения файлов cookie с помощью функции `get_cookies_dir`.
2.  Формирует имя файла кэша на основе имени класса (или имени родительского класса, если он есть).
3.  Возвращает объект `Path`, представляющий путь к файлу кэша.

ASCII схема:

```
Начало -> Получение директории cookie -> Формирование имени файла кэша -> Возврат пути к файлу кэша -> Конец
```

**Примеры**:
```python
# Пример вызова get_cache_file
cache_file_path = AuthFileMixin.get_cache_file()
```

### `AsyncAuthedProvider`

**Описание**:
Класс, предоставляющий асинхронную функциональность для провайдеров, требующих аутентификацию. Наследует `AsyncGeneratorProvider` и `AuthFileMixin`.

**Наследует**:

*   `AsyncGeneratorProvider`
*   `AuthFileMixin`

**Методы**:

*   `on_auth_async`
*   `on_auth`
*   `get_create_function`
*   `get_async_create_function`
*   `write_cache_file`
*   `create_completion`
*   `create_async_generator`

#### `on_auth_async`

```python
    @classmethod
    async def on_auth_async(cls, **kwargs) -> AuthResult:
       if "api_key" not in kwargs:
           raise MissingAuthError(f"API key is required for {cls.__name__}")
       return AuthResult()
```

**Назначение**:
Асинхронный метод для выполнения аутентификации.

**Параметры**:

*   `cls` (type): Класс, для которого вызывается этот метод.
*   `**kwargs`: Дополнительные именованные аргументы.

**Возвращает**:

*   `AuthResult`: Результат аутентификации.

**Вызывает исключения**:

*   `MissingAuthError`: Если отсутствует API-ключ.

**Как работает функция**:

1.  Проверяет наличие API-ключа в аргументах. Если он отсутствует, вызывает исключение `MissingAuthError`.
2.  Возвращает объект `AuthResult`.

ASCII схема:

```
Начало -> Проверка наличия API-ключа -> Если отсутствует: вызов MissingAuthError -> Возврат AuthResult -> Конец
```

**Примеры**:
```python
# Пример вызова on_auth_async
auth_result = await AsyncAuthedProvider.on_auth_async(api_key="your_api_key")
```

#### `on_auth`

```python
    @classmethod
    def on_auth(cls, **kwargs) -> AuthResult:
        auth_result = cls.on_auth_async(**kwargs)
        if hasattr(auth_result, "__aiter__"):\n            return to_sync_generator(auth_result)\n        return asyncio.run(auth_result)
```

**Назначение**:
Синхронный метод для выполнения аутентификации.

**Параметры**:

*   `cls` (type): Класс, для которого вызывается этот метод.
*   `**kwargs`: Дополнительные именованные аргументы.

**Возвращает**:

*   `AuthResult`: Результат аутентификации.

**Как работает функция**:

1.  Вызывает асинхронный метод `on_auth_async`.
2.  Если результат является асинхронным итератором, преобразует его в синхронный генератор.
3.  Запускает event loop и возвращает результат.

ASCII схема:

```
Начало -> Вызов on_auth_async -> Проверка результата на асинхронный итератор -> Если да: преобразование в синхронный генератор -> Запуск event loop -> Возврат результата -> Конец
```

**Примеры**:
```python
# Пример вызова on_auth
auth_result = AsyncAuthedProvider.on_auth(api_key="your_api_key")
```

#### `get_create_function`

```python
    @classmethod
    def get_create_function(cls) -> callable:
        return cls.create_completion
```

**Назначение**:
Возвращает функцию создания завершения.

**Параметры**:

*   `cls` (type): Класс, для которого вызывается этот метод.

**Возвращает**:

*   `callable`: Функция создания завершения.

#### `get_async_create_function`

```python
    @classmethod
    def get_async_create_function(cls) -> callable:
        return cls.create_async_generator
```

**Назначение**:
Возвращает асинхронную функцию генератора.

**Параметры**:

*   `cls` (type): Класс, для которого вызывается этот метод.

**Возвращает**:

*   `callable`: Асинхронная функция генератора.

#### `write_cache_file`

```python
    @classmethod
    def write_cache_file(cls, cache_file: Path, auth_result: AuthResult = None):
         if auth_result is not None:
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            cache_file.write_text(json.dumps(auth_result.get_dict()))
         elif cache_file.exists():
            cache_file.unlink
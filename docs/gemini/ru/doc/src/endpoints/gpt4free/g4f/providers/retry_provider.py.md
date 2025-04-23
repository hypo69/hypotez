# src/endpoints/gpt4free/g4f/providers/retry_provider.py

## Обзор

Модуль предназначен для реализации логики повторных запросов к различным поставщикам (providers) при генерации текста или других данных. Он содержит классы `IterListProvider` и `RetryProvider`, которые позволяют перебирать список поставщиков, поддерживающих потоковую передачу данных или нет, и повторять запросы в случае сбоев.

## Подробнее

Модуль предоставляет механизмы для обеспечения отказоустойчивости при работе с различными поставщиками, позволяя переключаться между ними в случае ошибок и повторять запросы. Это особенно полезно в ситуациях, когда надежность одного поставщика не гарантирована, и необходимо обеспечить стабильность работы системы.

## Классы

### `IterListProvider`

**Описание**: Класс для последовательного перебора поставщиков из списка и выполнения запросов к ним.

**Атрибуты**:

-   `providers` (List[Type[BaseProvider]]): Список классов поставщиков для использования.
-   `shuffle` (bool): Флаг, указывающий, нужно ли перемешивать список поставщиков. По умолчанию `True`.
-   `working` (bool): Флаг, указывающий, работает ли провайдер.
-   `last_provider` (Type[BaseProvider]): Последний использованный поставщик.

**Методы**:

-   `__init__(providers: List[Type[BaseProvider]], shuffle: bool = True) -> None`: Инициализирует класс `IterListProvider`.
-   `create_completion(model: str, messages: Messages, stream: bool = False, ignore_stream: bool = False, ignored: list[str] = [], **kwargs) -> CreateResult`: Выполняет запрос к поставщикам из списка, с возможностью потоковой передачи ответа.
-   `create_async_generator(model: str, messages: Messages, stream: bool = True, ignore_stream: bool = False, ignored: list[str] = [], **kwargs) -> AsyncResult`: Асинхронно выполняет запрос к поставщикам из списка, с возможностью потоковой передачи ответа.
-   `get_create_function() -> callable`: Возвращает функцию `create_completion`.
-   `get_async_create_function() -> callable`: Возвращает функцию `create_async_generator`.
-   `get_providers(stream: bool, ignored: list[str]) -> list[ProviderType]`: Возвращает список поставщиков, поддерживающих потоковую передачу данных (если требуется) и не находящихся в списке игнорируемых.

### `RetryProvider`

**Описание**: Класс для повторных запросов к поставщикам в случае сбоев. Наследуется от `IterListProvider`.

**Наследует**:

-   `IterListProvider`

**Атрибуты**:

-   `single_provider_retry` (bool): Флаг, указывающий, нужно ли повторять запрос к одному и тому же поставщику в случае сбоя.
-   `max_retries` (int): Максимальное количество повторных попыток для одного поставщика. По умолчанию 3.

**Методы**:

-   `__init__(providers: List[Type[BaseProvider]], shuffle: bool = True, single_provider_retry: bool = False, max_retries: int = 3) -> None`: Инициализирует класс `RetryProvider`.
-   `create_completion(model: str, messages: Messages, stream: bool = False, **kwargs) -> CreateResult`: Выполняет запрос к поставщикам из списка, с возможностью повторных попыток в случае сбоя и потоковой передачи ответа.
-   `create_async_generator(model: str, messages: Messages, stream: bool = True, **kwargs) -> AsyncResult`: Асинхронно выполняет запрос к поставщикам из списка, с возможностью повторных попыток в случае сбоя и потоковой передачи ответа.

## Функции

### `raise_exceptions(exceptions: dict) -> None`

**Назначение**: Генерирует исключение, если во время повторных запросов произошли ошибки.

**Параметры**:

-   `exceptions` (dict): Словарь с исключениями, произошедшими во время работы с поставщиками.

**Возвращает**:

-   `None`

**Вызывает исключения**:

-   `RetryProviderError`: Если какой-либо поставщик столкнулся с исключением.
-   `RetryNoProviderError`: Если не найдено ни одного поставщика.

**Как работает функция**:

Функция проверяет, есть ли исключения в переданном словаре `exceptions`. Если словарь не пуст, это означает, что во время работы с поставщиками произошли ошибки. В этом случае функция формирует сообщение об ошибке, содержащее информацию о каждом поставщике и соответствующем исключении, и генерирует исключение `RetryProviderError`. Если же словарь `exceptions` пуст, функция генерирует исключение `RetryNoProviderError`, указывающее на то, что ни один поставщик не был найден.

### `IterListProvider.__init__`

```python
def __init__(
        self,
        providers: List[Type[BaseProvider]],
        shuffle: bool = True
    ) -> None:
    """
    Initialize the BaseRetryProvider.
    Args:
        providers (List[Type[BaseProvider]]): List of providers to use.
        shuffle (bool): Whether to shuffle the providers list.
        single_provider_retry (bool): Whether to retry a single provider if it fails.
        max_retries (int): Maximum number of retries for a single provider.
    """
    self.providers = providers
    self.shuffle = shuffle
    self.working = True
    self.last_provider: Type[BaseProvider] = None
```

**Назначение**: Инициализация класса `IterListProvider`.

**Параметры**:

-   `providers` (List[Type[BaseProvider]]): Список поставщиков для использования.
-   `shuffle` (bool): Флаг, указывающий, нужно ли перемешивать список поставщиков. По умолчанию `True`.

**Как работает функция**:

Функция инициализирует атрибуты экземпляра класса `IterListProvider`. Она принимает список поставщиков `providers` и флаг `shuffle`, указывающий, нужно ли перемешивать этот список. Если `shuffle` установлен в `True`, список поставщиков перемешивается случайным образом. Также функция инициализирует атрибут `working` в `True`, что указывает на то, что провайдер работает, и атрибут `last_provider` в `None`, который будет хранить последнего использованного поставщика.

**Примеры**:

```python
from g4f.providers import RetryProvider
from g4f.providers import GeminiProChat  #  или любой другой провайдер

providers = [GeminiProChat]  #  или список других провайдеров
iter_provider = RetryProvider(providers=providers, shuffle=True)
```

### `IterListProvider.create_completion`

```python
def create_completion(
        self,
        model: str,
        messages: Messages,
        stream: bool = False,
        ignore_stream: bool = False,
        ignored: list[str] = [],
        **kwargs,
    ) -> CreateResult:
    """
    Create a completion using available providers, with an option to stream the response.
    Args:
        model (str): The model to be used for completion.
        messages (Messages): The messages to be used for generating completion.
        stream (bool, optional): Flag to indicate if the response should be streamed. Defaults to False.
    Yields:
        CreateResult: Tokens or results from the completion.
    Raises:
        Exception: Any exception encountered during the completion process.
    """
    exceptions = {}
    started: bool = False

    for provider in self.get_providers(stream and not ignore_stream, ignored):
        self.last_provider = provider
        debug.log(f"Using {provider.__name__} provider")
        yield ProviderInfo(**provider.get_dict(), model=model if model else getattr(provider, "default_model"))
        try:
            response = provider.get_create_function()(model, messages, stream=stream, **kwargs)
            for chunk in response:
                if chunk:
                    yield chunk
                    if isinstance(chunk, (str, MediaResponse)):
                        started = True
            if started:
                return
        except Exception as e:
            exceptions[provider.__name__] = e
            debug.error(f"{provider.__name__} {type(e).__name__}: {e}")
            if started:
                raise e
            yield e

    raise_exceptions(exceptions)
```

**Назначение**: Создание завершения (completion) с использованием доступных поставщиков, с возможностью потоковой передачи ответа.

**Параметры**:

-   `model` (str): Модель, используемая для завершения.
-   `messages` (Messages): Сообщения, используемые для генерации завершения.
-   `stream` (bool, optional): Флаг, указывающий, должен ли ответ передаваться потоком. По умолчанию `False`.
-   `ignore_stream` (bool, optional): Флаг, указывающий, нужно ли игнорировать потоковую передачу. По умолчанию `False`.
-   `ignored` (list[str], optional): Список поставщиков, которых следует игнорировать. По умолчанию `[]`.
-   `**kwargs`: Дополнительные аргументы, передаваемые в функцию создания поставщика.

**Возвращает**:

-   `CreateResult`: Токены или результаты от завершения.

**Вызывает исключения**:

-   `Exception`: Любое исключение, возникшее во время процесса завершения.

**Как работает функция**:

Функция перебирает доступных поставщиков, полученных с помощью `self.get_providers()`. Для каждого поставщика она пытается получить завершение, используя функцию `provider.get_create_function()`. Если потоковая передача включена, функция передает токены по мере их поступления. Если в процессе работы возникает исключение, оно сохраняется в словаре `exceptions`. Если хотя бы один поставщик успешно начал выдавать токены, функция завершается. В случае, если все поставщики вернули ошибки, функция вызывает `raise_exceptions()` для генерации сводного исключения.

**Примеры**:

```python
from g4f.providers import RetryProvider
from g4f.providers import GeminiProChat  #  или любой другой провайдер

providers = [GeminiProChat]  #  или список других провайдеров
iter_provider = RetryProvider(providers=providers, shuffle=True)

messages = [{"role": "user", "content": "Привет, как дела?"}]
for chunk in iter_provider.create_completion(model="default", messages=messages, stream=True):
    print(chunk)
```

### `IterListProvider.create_async_generator`

```python
async def create_async_generator(
        self,
        model: str,
        messages: Messages,
        stream: bool = True,
        ignore_stream: bool = False,
        ignored: list[str] = [],
        **kwargs
    ) -> AsyncResult:
    """
    Create a completion using available providers, with an option to stream the response.
    Args:
        model (str): The model to be used for completion.
        messages (Messages): The messages to be used for generating completion.
        stream (bool, optional): Flag to indicate if the response should be streamed. Defaults to False.
    Yields:
        AsyncResult: Tokens or results from the completion.
    Raises:
        Exception: Any exception encountered during the completion process.
    """
    exceptions = {}
    started: bool = False

    for provider in self.get_providers(stream and not ignore_stream, ignored):
        self.last_provider = provider
        debug.log(f"Using {provider.__name__} provider")
        yield ProviderInfo(**provider.get_dict(), model=model if model else getattr(provider, "default_model"))
        try:
            response = provider.get_async_create_function()(model, messages, stream=stream, **kwargs)
            if hasattr(response, "__aiter__"):
                async for chunk in response:
                    if chunk:
                        yield chunk
                        if isinstance(chunk, (str, MediaResponse)):
                            started = True
            elif response:
                response = await response
                if response:
                    yield response
                    started = True
            if started:
                return
        except Exception as e:
            exceptions[provider.__name__] = e
            debug.error(f"{provider.__name__} {type(e).__name__}: {e}")
            if started:
                raise e
            yield e

    raise_exceptions(exceptions)
```

**Назначение**: Асинхронное создание завершения (completion) с использованием доступных поставщиков, с возможностью потоковой передачи ответа.

**Параметры**:

-   `model` (str): Модель, используемая для завершения.
-   `messages` (Messages): Сообщения, используемые для генерации завершения.
-   `stream` (bool, optional): Флаг, указывающий, должен ли ответ передаваться потоком. По умолчанию `True`.
-   `ignore_stream` (bool, optional): Флаг, указывающий, нужно ли игнорировать потоковую передачу. По умолчанию `False`.
-   `ignored` (list[str], optional): Список поставщиков, которых следует игнорировать. По умолчанию `[]`.
-   `**kwargs`: Дополнительные аргументы, передаваемые в функцию создания поставщика.

**Возвращает**:

-   `AsyncResult`: Токены или результаты от завершения.

**Вызывает исключения**:

-   `Exception`: Любое исключение, возникшее во время процесса завершения.

**Как работает функция**:

Функция аналогична `create_completion`, но выполняет запросы асинхронно. Она перебирает доступных поставщиков, полученных с помощью `self.get_providers()`. Для каждого поставщика она пытается получить завершение, используя функцию `provider.get_async_create_function()`. Если потоковая передача включена, функция передает токены по мере их поступления. Если в процессе работы возникает исключение, оно сохраняется в словаре `exceptions`. Если хотя бы один поставщик успешно начал выдавать токены, функция завершается. В случае, если все поставщики вернули ошибки, функция вызывает `raise_exceptions()` для генерации сводного исключения.

**Примеры**:

```python
import asyncio
from g4f.providers import RetryProvider
from g4f.providers import GeminiProChat  #  или любой другой провайдер

providers = [GeminiProChat]  #  или список других провайдеров
iter_provider = RetryProvider(providers=providers, shuffle=True)

async def main():
    messages = [{"role": "user", "content": "Привет, как дела?"}]
    async for chunk in iter_provider.create_async_generator(model="default", messages=messages, stream=True):
        print(chunk)

asyncio.run(main())
```

### `IterListProvider.get_providers`

```python
def get_providers(self, stream: bool, ignored: list[str]) -> list[ProviderType]:
    """
    Get a list of providers that support stream and are not in the ignored list.
    Args:
        stream (bool): Whether the providers should support stream.
        ignored (list[str]): List of provider names to ignore.
    Returns:
        list[ProviderType]: List of providers.
    """
    providers = [p for p in self.providers if (p.supports_stream or not stream) and p.__name__ not in ignored]
    if self.shuffle:
        random.shuffle(providers)
    return providers
```

**Назначение**: Получение списка поставщиков, поддерживающих потоковую передачу и не находящихся в списке игнорируемых.

**Параметры**:

-   `stream` (bool): Флаг, указывающий, должна ли поддерживаться потоковая передача.
-   `ignored` (list[str]): Список имен поставщиков, которых следует игнорировать.

**Возвращает**:

-   `list[ProviderType]`: Список поставщиков.

**Как работает функция**:

Функция фильтрует список поставщиков `self.providers` на основе двух критериев: поддержки потоковой передачи (если требуется) и отсутствия в списке игнорируемых. Если `stream` установлен в `True`, в результирующий список включаются только те поставщики, у которых атрибут `supports_stream` также установлен в `True`. Кроме того, из списка исключаются поставщики, имена которых присутствуют в списке `ignored`. Если атрибут `shuffle` установлен в `True`, результирующий список перемешивается случайным образом.

**Примеры**:

```python
from g4f.providers import RetryProvider
from g4f.providers import GeminiProChat, Bing  #  или любой другой провайдер

providers = [GeminiProChat, Bing]  #  или список других провайдеров
iter_provider = RetryProvider(providers=providers, shuffle=True)

stream = True
ignored = [Bing.__name__]
available_providers = iter_provider.get_providers(stream=stream, ignored=ignored)
print(available_providers)
```

### `RetryProvider.__init__`

```python
def __init__(
        self,
        providers: List[Type[BaseProvider]],
        shuffle: bool = True,
        single_provider_retry: bool = False,
        max_retries: int = 3,
    ) -> None:
    """
    Initialize the BaseRetryProvider.
    Args:
        providers (List[Type[BaseProvider]]): List of providers to use.
        shuffle (bool): Whether to shuffle the providers list.
        single_provider_retry (bool): Whether to retry a single provider if it fails.
        max_retries (int): Maximum number of retries for a single provider.
    """
    super().__init__(providers, shuffle)
    self.single_provider_retry = single_provider_retry
    self.max_retries = max_retries
```

**Назначение**: Инициализация класса `RetryProvider`.

**Параметры**:

-   `providers` (List[Type[BaseProvider]]): Список поставщиков для использования.
-   `shuffle` (bool): Флаг, указывающий, нужно ли перемешивать список поставщиков. По умолчанию `True`.
-   `single_provider_retry` (bool): Флаг, указывающий, нужно ли повторять запрос к одному и тому же поставщику в случае сбоя. По умолчанию `False`.
-   `max_retries` (int): Максимальное количество повторных попыток для одного поставщика. По умолчанию 3.

**Как работает функция**:

Функция вызывает конструктор родительского класса `IterListProvider` для инициализации списка поставщиков и флага перемешивания. Затем она инициализирует атрибуты `single_provider_retry` и `max_retries` экземпляра класса `RetryProvider`.

**Примеры**:

```python
from g4f.providers import RetryProvider
from g4f.providers import GeminiProChat  #  или любой другой провайдер

providers = [GeminiProChat]  #  или список других провайдеров
retry_provider = RetryProvider(providers=providers, shuffle=True, single_provider_retry=True, max_retries=5)
```

### `RetryProvider.create_completion`

```python
def create_completion(
        self,
        model: str,
        messages: Messages,
        stream: bool = False,
        **kwargs,
    ) -> CreateResult:
    """
    Create a completion using available providers, with an option to stream the response.
    Args:
        model (str): The model to be used for completion.
        messages (Messages): The messages to be used for generating completion.
        stream (bool, optional): Flag to indicate if the response should be streamed. Defaults to False.
    Yields:
        CreateResult: Tokens or results from the completion.
    Raises:
        Exception: Any exception encountered during the completion process.
    """
    if self.single_provider_retry:
        exceptions = {}
        started: bool = False
        provider = self.providers[0]
        self.last_provider = provider
        for attempt in range(self.max_retries):
            try:
                if debug.logging:
                    print(f"Using {provider.__name__} provider (attempt {attempt + 1})")
                response = provider.get_create_function()(model, messages, stream=stream, **kwargs)
                for chunk in response:
                    if isinstance(chunk, str) or isinstance(chunk, ImageResponse):
                        yield chunk
                        started = True
                if started:
                    return
            except Exception as e:
                exceptions[provider.__name__] = e
                if debug.logging:
                    print(f"{provider.__name__}: {e.__class__.__name__}: {e}")
                if started:
                    raise e
        raise_exceptions(exceptions)
    else:
        yield from super().create_completion(model, messages, stream, **kwargs)
```

**Назначение**: Создание завершения (completion) с использованием доступных поставщиков, с возможностью повторных попыток в случае сбоя и потоковой передачи ответа.

**Параметры**:

-   `model` (str): Модель, используемая для завершения.
-   `messages` (Messages): Сообщения, используемые для генерации завершения.
-   `stream` (bool, optional): Флаг, указывающий, должен ли ответ передаваться потоком. По умолчанию `False`.
-   `**kwargs`: Дополнительные аргументы, передаваемые в функцию создания поставщика.

**Возвращает**:

-   `CreateResult`: Токены или результаты от завершения.

**Вызывает исключения**:

-   `Exception`: Любое исключение, возникшее во время процесса завершения.

**Как работает функция**:

Функция проверяет, установлен ли флаг `self.single_provider_retry`. Если он установлен, функция пытается выполнить запрос к первому поставщику из списка `self.providers` `self.max_retries` раз. В случае успеха функция передает токены по мере их поступления. Если в процессе работы возникает исключение, оно сохраняется в словаре `exceptions`. Если хотя бы один поставщик успешно начал выдавать токены, функция завершается. В случае, если все попытки завершились неудачей, функция вызывает `raise_exceptions()` для генерации сводного исключения. Если флаг `self.single_provider_retry` не установлен, функция вызывает метод `create_completion()` родительского класса `IterListProvider` для выполнения запроса к поставщикам из списка.

**Примеры**:

```python
from g4f.providers import RetryProvider
from g4f.providers import GeminiProChat  #  или любой другой провайдер

providers = [GeminiProChat]  #  или список других провайдеров
retry_provider = RetryProvider(providers=providers, shuffle=True, single_provider_retry=True, max_retries=5)

messages = [{"role": "user", "content": "Привет, как дела?"}]
for chunk in retry_provider.create_completion(model="default", messages=messages, stream=True):
    print(chunk)
```

### `RetryProvider.create_async_generator`

```python
async def create_async_generator(
        self,
        model: str,
        messages: Messages,
        stream: bool = True,
        **kwargs
    ) -> AsyncResult:
    """
    Create a completion using available providers, with an option to stream the response.
    Args:
        model (str): The model to be used for completion.
        messages (Messages): The messages to be used for generating completion.
        stream (bool, optional): Flag to indicate if the response should be streamed. Defaults to False.
    Yields:
        AsyncResult: Tokens or results from the completion.
    Raises:
        Exception: Any exception encountered during the completion process.
    """
    exceptions = {}
    started = False

    if self.single_provider_retry:
        provider = self.providers[0]
        self.last_provider = provider
        for attempt in range(self.max_retries):
            try:
                debug.log(f"Using {provider.__name__} provider (attempt {attempt + 1})")
                response = provider.get_async_create_function()(model, messages, stream=stream, **kwargs)
                if hasattr(response, "__aiter__"):
                    async for chunk in response:
                        if isinstance(chunk, str) or isinstance(chunk, ImageResponse):
                            yield chunk
                            started = True
                else:
                    response = await response
                    if response:
                        yield response
                        started = True
                if started:
                    return
            except Exception as e:
                exceptions[provider.__name__] = e
                if debug.logging:
                    print(f"{provider.__name__}: {e.__class__.__name__}: {e}")
        raise_exceptions(exceptions)
    else:
        async for chunk in super().create_async_generator(model, messages, stream, **kwargs):
            yield chunk
```

**Назначение**: Асинхронное создание завершения (completion) с использованием доступных поставщиков, с возможностью повторных попыток в случае сбоя и потоковой передачи ответа.

**Параметры**:

-   `model` (str): Модель, используемая для завершения.
-   `messages` (Messages): Сообщения, используемые для генерации завершения.
-   `stream` (bool, optional): Флаг, указывающий, должен ли ответ передаваться потоком. По умолчанию `True`.
-   `**kwargs`: Дополнительные аргументы, передаваемые в функцию создания поставщика.

**Возвращает**:

-   `AsyncResult`: Токены или результаты от завершения.

**Вызывает исключения**:

-   `Exception`: Любое исключение, возникшее во время процесса завершения.

**Как работает функция**:

Функция аналогична `create_completion`, но выполняет запросы асинхронно. Она проверяет, установлен ли флаг `self.single_provider_retry`. Если он установлен, функция пытается выполнить запрос к первому поставщику из списка `self.providers` `self.max_retries` раз. В случае успеха функция передает токены по мере их поступления. Если в процессе работы возникает исключение, оно сохраняется в словаре `exceptions`. Если хотя бы один поставщик успешно начал выдавать токены, функция завершается. В случае, если все попытки завершились неудачей, функция вызывает `raise_exceptions()` для генерации сводного исключения. Если флаг `self.single_provider_retry` не установлен, функция вызывает метод `create_async_generator()` родительского класса `IterListProvider` для выполнения запроса к поставщикам из списка.

**Примеры**:

```python
import asyncio
from g4f.providers import RetryProvider
from g4f.providers import GeminiProChat  #  или любой другой провайдер

providers = [GeminiProChat]  #  или список других провайдеров
retry_provider = RetryProvider(providers=providers, shuffle=True, single_provider_retry=True, max_retries=5)

async def main():
    messages = [{"role": "user", "content": "Привет, как дела?"}]
    async for chunk in retry_provider.create_async_generator(model="default", messages=messages, stream=True):
        print(chunk)

asyncio.run(main())
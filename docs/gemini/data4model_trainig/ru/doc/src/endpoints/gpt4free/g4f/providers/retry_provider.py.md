# Модуль для повторных попыток при использовании нескольких провайдеров

## Обзор

Модуль `retry_provider.py` предоставляет классы `IterListProvider` и `RetryProvider`, которые позволяют выполнять запросы к различным провайдерам (например, к моделям GPT) с возможностью повторных попыток в случае неудачи. Это полезно для обеспечения отказоустойчивости и повышения надежности работы системы, когда доступность отдельных провайдеров может быть нестабильной. Модуль также включает функцию `raise_exceptions`, которая генерирует исключения, если ни один из провайдеров не смог успешно обработать запрос.

## Подробнее

Этот модуль предназначен для организации работы с несколькими провайдерами, предоставляющими функциональность, например, генерацию текста. Он позволяет автоматически переключаться между провайдерами при возникновении ошибок и предоставляет механизм повторных попыток.
`IterListProvider` — базовый класс, который перебирает список провайдеров и пытается выполнить запрос с использованием каждого из них по очереди.
`RetryProvider` — расширяет `IterListProvider`, добавляя логику повторных попыток для одного провайдера, прежде чем переходить к следующему.
Функция `raise_exceptions` используется для централизованной обработки исключений, возникающих при работе с провайдерами.

## Классы

### `IterListProvider`

**Описание**: Базовый класс для перебора списка провайдеров и выполнения запросов к ним.

**Атрибуты**:

- `providers` (List[Type[BaseProvider]]): Список провайдеров для использования.
- `shuffle` (bool): Флаг, указывающий, нужно ли перемешивать список провайдеров.
- `working` (bool): Флаг, показывающий, что провайдер работает.
- `last_provider` (Type[BaseProvider]): Последний использованный провайдер.

**Методы**:

- `__init__(providers: List[Type[BaseProvider]], shuffle: bool = True) -> None`: Инициализирует `IterListProvider`.
- `create_completion(model: str, messages: Messages, stream: bool = False, ignore_stream: bool = False, ignored: list[str] = [], **kwargs) -> CreateResult`: Создает завершение, используя доступных провайдеров, с возможностью потоковой передачи ответа.
- `create_async_generator(model: str, messages: Messages, stream: bool = True, ignore_stream: bool = False, ignored: list[str] = [], **kwargs) -> AsyncResult`: Асинхронно создает генератор завершений, используя доступных провайдеров.
- `get_create_function() -> callable`: Возвращает функцию создания завершения.
- `get_async_create_function() -> callable`: Возвращает асинхронную функцию создания завершения.
- `get_providers(stream: bool, ignored: list[str]) -> list[ProviderType]`: Возвращает список провайдеров, поддерживающих потоковую передачу, исключая игнорируемые.

#### `__init__`

```python
def __init__(
    self,
    providers: List[Type[BaseProvider]],
    shuffle: bool = True
) -> None:
    """
    Инициализирует BaseRetryProvider.

    Args:
        providers (List[Type[BaseProvider]]): Список провайдеров для использования.
        shuffle (bool): Нужно ли перемешивать список провайдеров. По умолчанию `True`.
    """
    ...
```

#### `create_completion`

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
    Создает завершение, используя доступных провайдеров, с возможностью потоковой передачи ответа.

    Args:
        model (str): Модель для использования для завершения.
        messages (Messages): Сообщения для генерации завершения.
        stream (bool, optional): Флаг, указывающий, должен ли ответ передаваться потоком. По умолчанию `False`.
        ignore_stream (bool, optional): Флаг, указывающий, следует ли игнорировать потоковую передачу. По умолчанию `False`.
        ignored (list[str], optional): Список провайдеров, которые следует игнорировать. По умолчанию [].
        **kwargs: Дополнительные аргументы для передачи провайдеру.

    Yields:
        CreateResult: Токены или результаты завершения.

    Raises:
        Exception: Любое исключение, возникшее в процессе завершения.

    Как работает функция:
    - Инициализирует пустой словарь `exceptions` для хранения исключений, возникших при использовании различных провайдеров.
    - Устанавливает флаг `started` в `False`, чтобы отслеживать, был ли успешно запущен хотя бы один провайдер.
    - Перебирает провайдеров, возвращаемых методом `get_providers`, с учетом поддержки потоковой передачи и списка игнорируемых провайдеров.
    - Для каждого провайдера пытается создать завершение, вызывая `provider.get_create_function()`.
    - Если потоковая передача включена, перебирает чанки (фрагменты) ответа и передает их вызывающей стороне с помощью `yield`.
    - Если в процессе создания завершения возникает исключение, оно сохраняется в словаре `exceptions` и логируется.
    - Если хотя бы один провайдер успешно начал передавать данные, любые последующие исключения приводят к немедленному прекращению работы функции и передаче исключения выше.
    - Если ни один провайдер не смог успешно обработать запрос, функция вызывает `raise_exceptions` для генерации исключения, объединяющего все возникшие ошибки.
    """
    ...
```

#### `create_async_generator`

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
    Асинхронно создает генератор завершений, используя доступных провайдеров.

    Args:
        model (str): Модель для использования для завершения.
        messages (Messages): Сообщения для генерации завершения.
        stream (bool, optional): Флаг, указывающий, должен ли ответ передаваться потоком. По умолчанию `True`.
        ignore_stream (bool, optional): Флаг, указывающий, следует ли игнорировать потоковую передачу. По умолчанию `False`.
        ignored (list[str], optional): Список провайдеров, которые следует игнорировать. По умолчанию [].
        **kwargs: Дополнительные аргументы для передачи провайдеру.

    Yields:
        AsyncResult: Асинхронный генератор токенов или результатов завершения.

    Raises:
        Exception: Любое исключение, возникшее в процессе завершения.

    Как работает функция:
    - Аналогично `create_completion`, но использует асинхронные вызовы и асинхронные генераторы.
    - Перебирает провайдеров, возвращаемых методом `get_providers`, с учетом поддержки потоковой передачи и списка игнорируемых провайдеров.
    - Для каждого провайдера пытается создать асинхронное завершение, вызывая `provider.get_async_create_function()`.
    - Если возвращенный объект является асинхронным генератором, перебирает чанки (фрагменты) ответа и передает их вызывающей стороне с помощью `yield`.
    - Если в процессе создания завершения возникает исключение, оно сохраняется в словаре `exceptions` и логируется.
    - Если хотя бы один провайдер успешно начал передавать данные, любые последующие исключения приводят к немедленному прекращению работы функции и передаче исключения выше.
    - Если ни один провайдер не смог успешно обработать запрос, функция вызывает `raise_exceptions` для генерации исключения, объединяющего все возникшие ошибки.
    """
    ...
```

#### `get_create_function`

```python
def get_create_function(self) -> callable:
    """
    Возвращает функцию создания завершения.

    Returns:
        callable: Функция create_completion.
    """
    return self.create_completion
```

#### `get_async_create_function`

```python
def get_async_create_function(self) -> callable:
    """
    Возвращает асинхронную функцию создания завершения.

    Returns:
        callable: Функция create_async_generator.
    """
    return self.create_async_generator
```

#### `get_providers`

```python
def get_providers(self, stream: bool, ignored: list[str]) -> list[ProviderType]:
    """
    Возвращает список провайдеров, поддерживающих потоковую передачу, исключая игнорируемые.

    Args:
        stream (bool): Флаг, указывающий, требуется ли поддержка потоковой передачи.
        ignored (list[str]): Список провайдеров, которые следует исключить из результата.

    Returns:
        list[ProviderType]: Список провайдеров, соответствующих критериям.
    """
    ...
```

### `RetryProvider`

**Описание**: Класс для повторных попыток выполнения запросов к провайдерам.

**Наследует**:
- `IterListProvider`: Наследует функциональность перебора списка провайдеров.

**Атрибуты**:

- `single_provider_retry` (bool): Флаг, указывающий, следует ли повторять попытки с одним и тем же провайдером.
- `max_retries` (int): Максимальное количество повторных попыток для одного провайдера.

**Методы**:

- `__init__(providers: List[Type[BaseProvider]], shuffle: bool = True, single_provider_retry: bool = False, max_retries: int = 3) -> None`: Инициализирует `RetryProvider`.
- `create_completion(model: str, messages: Messages, stream: bool = False, **kwargs) -> CreateResult`: Создает завершение, используя доступных провайдеров, с возможностью повторных попыток.
- `create_async_generator(model: str, messages: Messages, stream: bool = True, **kwargs) -> AsyncResult`: Асинхронно создает генератор завершений, используя доступных провайдеров, с возможностью повторных попыток.

#### `__init__`

```python
def __init__(
    self,
    providers: List[Type[BaseProvider]],
    shuffle: bool = True,
    single_provider_retry: bool = False,
    max_retries: int = 3,
) -> None:
    """
    Инициализирует BaseRetryProvider.

    Args:
        providers (List[Type[BaseProvider]]): Список провайдеров для использования.
        shuffle (bool): Нужно ли перемешивать список провайдеров. По умолчанию `True`.
        single_provider_retry (bool): Следует ли повторять попытки с одним и тем же провайдером, если он не работает. По умолчанию `False`.
        max_retries (int): Максимальное количество повторных попыток для одного провайдера. По умолчанию `3`.
    """
    ...
```

#### `create_completion`

```python
def create_completion(
    self,
    model: str,
    messages: Messages,
    stream: bool = False,
    **kwargs,
) -> CreateResult:
    """
    Создает завершение, используя доступных провайдеров, с возможностью потоковой передачи ответа.

    Args:
        model (str): Модель для использования для завершения.
        messages (Messages): Сообщения для генерации завершения.
        stream (bool, optional): Флаг, указывающий, должен ли ответ передаваться потоком. По умолчанию `False`.
        **kwargs: Дополнительные аргументы для передачи провайдеру.

    Yields:
        CreateResult: Токены или результаты завершения.

    Raises:
        Exception: Любое исключение, возникшее в процессе завершения.
    """
    ...
```

#### `create_async_generator`

```python
async def create_async_generator(
    self,
    model: str,
    messages: Messages,
    stream: bool = True,
    **kwargs
) -> AsyncResult:
    """
    Асинхронно создает генератор завершений, используя доступных провайдеров, с возможностью потоковой передачи ответа.

    Args:
        model (str): Модель для использования для завершения.
        messages (Messages): Сообщения для генерации завершения.
        stream (bool, optional): Флаг, указывающий, должен ли ответ передаваться потоком. По умолчанию `True`.
        **kwargs: Дополнительные аргументы для передачи провайдеру.

    Yields:
        AsyncResult: Асинхронный генератор токенов или результатов завершения.

    Raises:
        Exception: Любое исключение, возникшее в процессе завершения.
    """
    ...
```

## Функции

### `raise_exceptions`

```python
def raise_exceptions(exceptions: dict) -> None:
    """
    Вызывает объединенное исключение, если во время повторных попыток возникли какие-либо исключения.

    Args:
        exceptions (dict): Словарь исключений, возникших при использовании различных провайдеров. Ключи - имена провайдеров, значения - исключения.

    Raises:
        RetryProviderError: Если какой-либо провайдер столкнулся с исключением.
        RetryNoProviderError: Если ни один провайдер не найден.
    """
    ...
```

## Примеры

Пример использования `IterListProvider`:

```python
from g4f.providers import RetryProvider, GptGo, ChatBase

providers = [GptGo, ChatBase]  # Список провайдеров
retry_provider = RetryProvider(providers=providers, shuffle=True)

try:
    for message in retry_provider.create_completion(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello"}], stream=True):
        print(message, end="", flush=True)
except Exception as e:
    print(f"Error: {e}")
```

Пример использования `RetryProvider` с повторными попытками для одного провайдера:

```python
from g4f.providers import RetryProvider, GptGo

providers = [GptGo]  # Список провайдеров
retry_provider = RetryProvider(providers=providers, shuffle=False, single_provider_retry=True, max_retries=5)

try:
    for message in retry_provider.create_completion(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello"}], stream=True):
        print(message, end="", flush=True)
except Exception as e:
    print(f"Error: {e}")
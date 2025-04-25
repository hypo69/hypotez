# Модуль типов для провайдеров GPT4Free

## Обзор

Этот модуль определяет типы и абстрактные базовые классы для провайдеров GPT4Free. Он включает в себя определение базового провайдера, а также провайдера с поддержкой повторных попыток (retries).

## Классы

### `BaseProvider`

**Описание**: Абстрактный базовый класс для провайдера.

**Наследует**: `ABC`

**Атрибуты**:
- `url` (str): URL-адрес провайдера.
- `working` (bool): Указывает, работает ли провайдер в данный момент.
- `needs_auth` (bool): Указывает, требуется ли авторизация для провайдера.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных (streaming).
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения.
- `params` (str): Список параметров для провайдера.

**Методы**:
- `get_create_function()`: Получает функцию создания для провайдера.
- `get_async_create_function()`: Получает асинхронную функцию создания для провайдера.
- `get_dict()`: Получает словарь с описанием провайдера.

**Пример**:

```python
from hypotez.src.endpoints.gpt4free.g4f.providers.types import BaseProvider

class MyProvider(BaseProvider):
    """
    Пример реализации провайдера.
    """
    url: str = "https://example.com"
    working: bool = True
    needs_auth: bool = False
    supports_stream: bool = False
    supports_message_history: bool = False
    supports_system_message: bool = False
    params: str = "some_params"

    def get_create_function(self) -> callable:
        """
        Получает функцию создания для провайдера.
        """
        # Реализация функции создания
        pass

    def get_async_create_function(self) -> callable:
        """
        Получает асинхронную функцию создания для провайдера.
        """
        # Реализация асинхронной функции создания
        pass
```

### `BaseRetryProvider`

**Описание**: Базовый класс для провайдера, реализующего логику повторных попыток (retries).

**Наследует**: `BaseProvider`

**Атрибуты**:
- `providers` (List[Type[BaseProvider]]): Список провайдеров, которые будут использоваться для повторных попыток.
- `shuffle` (bool): Указывает, нужно ли перемешивать список провайдеров.
- `exceptions` (Dict[str, Exception]): Словарь с описанием ошибок, возникших при использовании провайдеров.
- `last_provider` (Type[BaseProvider]): Последний использованный провайдер.

**Пример**:

```python
from hypotez.src.endpoints.gpt4free.g4f.providers.types import BaseRetryProvider, BaseProvider

class MyRetryProvider(BaseRetryProvider):
    """
    Пример реализации провайдера с поддержкой повторных попыток.
    """
    providers: List[Type[BaseProvider]] = [MyProvider1, MyProvider2]
    shuffle: bool = True
    exceptions: Dict[str, Exception] = {}
    last_provider: Type[BaseProvider] = None

    def get_create_function(self) -> callable:
        """
        Получает функцию создания для провайдера.
        """
        # Реализация функции создания с учетом повторных попыток
        pass

    def get_async_create_function(self) -> callable:
        """
        Получает асинхронную функцию создания для провайдера.
        """
        # Реализация асинхронной функции создания с учетом повторных попыток
        pass
```

## Типы

- `ProviderType`: Тип, представляющий провайдер. Может быть базовым провайдером или провайдером с поддержкой повторных попыток.

## Классы

### `Streaming`

**Описание**: Класс для работы с потоковыми данными (streaming).

**Атрибуты**:
- `data` (str): Потоковые данные.

**Методы**:
- `__str__()`: Возвращает строковое представление потоковых данных.

**Пример**:

```python
from hypotez.src.endpoints.gpt4free.g4f.providers.types import Streaming

streaming_data = Streaming("Example streaming data")
print(streaming_data)  # Вывод: Example streaming data
```

## Параметры

- `params` (str): Список параметров для провайдера.
- `providers` (List[Type[BaseProvider]]): Список провайдеров, которые будут использоваться для повторных попыток.
- `exceptions` (Dict[str, Exception]): Словарь с описанием ошибок, возникших при использовании провайдеров.
- `last_provider` (Type[BaseProvider]): Последний использованный провайдер.


## Примеры

**Пример создания провайдера:**

```python
from hypotez.src.endpoints.gpt4free.g4f.providers.types import BaseProvider

class MyProvider(BaseProvider):
    """
    Пример реализации провайдера.
    """
    url: str = "https://example.com"
    working: bool = True
    needs_auth: bool = False
    supports_stream: bool = False
    supports_message_history: bool = False
    supports_system_message: bool = False
    params: str = "some_params"

    def get_create_function(self) -> callable:
        """
        Получает функцию создания для провайдера.
        """
        # Реализация функции создания
        pass

    def get_async_create_function(self) -> callable:
        """
        Получает асинхронную функцию создания для провайдера.
        """
        # Реализация асинхронной функции создания
        pass
```

**Пример создания провайдера с поддержкой повторных попыток:**

```python
from hypotez.src.endpoints.gpt4free.g4f.providers.types import BaseRetryProvider, BaseProvider

class MyRetryProvider(BaseRetryProvider):
    """
    Пример реализации провайдера с поддержкой повторных попыток.
    """
    providers: List[Type[BaseProvider]] = [MyProvider1, MyProvider2]
    shuffle: bool = True
    exceptions: Dict[str, Exception] = {}
    last_provider: Type[BaseProvider] = None

    def get_create_function(self) -> callable:
        """
        Получает функцию создания для провайдера.
        """
        # Реализация функции создания с учетом повторных попыток
        pass

    def get_async_create_function(self) -> callable:
        """
        Получает асинхронную функцию создания для провайдера.
        """
        # Реализация асинхронной функции создания с учетом повторных попыток
        pass
```

**Пример работы с потоковыми данными:**

```python
from hypotez.src.endpoints.gpt4free.g4f.providers.types import Streaming

streaming_data = Streaming("Example streaming data")
print(streaming_data)  # Вывод: Example streaming data
```
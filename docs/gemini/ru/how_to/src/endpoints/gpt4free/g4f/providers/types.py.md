### **Как использовать этот блок кода**
=========================================================================================

Описание
-------------------------
Этот блок кода определяет абстрактные базовые классы для провайдеров, используемых для взаимодействия с различными сервисами, например, для генерации текста. Он также включает класс для обработки потоковых данных.

Шаги выполнения
-------------------------
1. **`BaseProvider`**:
   - Это абстрактный базовый класс для всех провайдеров.
   - Определяет общие атрибуты, такие как `url`, `working`, `needs_auth`, `supports_stream`, `supports_message_history`, `supports_system_message` и `params`.
   - Содержит абстрактные методы `get_create_function` и `get_async_create_function`, которые должны быть реализованы в подклассах. Эти методы возвращают синхронную и асинхронную функции для создания запросов к провайдеру.
   - Метод `get_dict` возвращает словарь с основной информацией о провайдере: имя, URL и метку.

2. **`BaseRetryProvider`**:
   - Это базовый класс для провайдеров, которые используют логику повторных попыток (retry).
   - Содержит атрибуты `providers` (список провайдеров для повторных попыток), `shuffle` (флаг для перемешивания списка провайдеров), `exceptions` (словарь исключений) и `last_provider` (последний использованный провайдер).
   - Указывает, что данный провайдер поддерживает потоковую передачу (`supports_stream: bool = True`).

3. **`ProviderType`**:
   - Определяет тип `ProviderType` как объединение `BaseProvider` и `BaseRetryProvider`. Это позволяет использовать любой из этих типов в качестве провайдера.

4. **`Streaming`**:
   - Класс для работы с потоковыми данными.
   - При инициализации принимает строку `data`.
   - Метод `__str__` возвращает строку `data`.

Пример использования
-------------------------

```python
from abc import ABC, abstractmethod
from typing import Union, Dict, Type

class BaseProvider(ABC):
    url: str = None
    working: bool = False
    needs_auth: bool = False
    supports_stream: bool = False
    supports_message_history: bool = False
    supports_system_message: bool = False
    params: str

    @abstractmethod
    def get_create_function() -> callable:
        raise NotImplementedError()

    @abstractmethod
    def get_async_create_function() -> callable:
        raise NotImplementedError()

    @classmethod
    def get_dict(cls) -> Dict[str, str]:
        return {'name': cls.__name__, 'url': cls.url, 'label': getattr(cls, 'label', None)}

class ConcreteProvider(BaseProvider):
    url: str = "https://example.com"
    working: bool = True
    needs_auth: bool = False
    supports_stream: bool = True
    supports_message_history: bool = True
    supports_system_message: bool = True
    params: str = "param1, param2"

    def get_create_function(self) -> callable:
        def create_function():
            return "Request created"
        return create_function

    def get_async_create_function(self) -> callable:
        async def async_create_function():
            return "Async request created"
        return async_create_function

# Пример использования BaseProvider
provider = ConcreteProvider()
print(f"Provider name: {provider.__class__.__name__}")
print(f"Provider URL: {provider.url}")
print(f"Supports streaming: {provider.supports_stream}")
print(f"Create function result: {provider.get_create_function()()}")

from typing import List

class BaseRetryProvider(BaseProvider):
    __name__: str = "RetryProvider"
    supports_stream: bool = True
    last_provider: Type[BaseProvider] = None

    def __init__(
        self, providers: List[Type[BaseProvider]], shuffle: bool = False
    ):
        self.providers = providers
        self.shuffle = shuffle
        self.exceptions = {}
        self.last_provider = None

    def get_create_function(self) -> callable:
        def create_function():
            return "Request created with retry"
        return create_function

    def get_async_create_function(self) -> callable:
        async def async_create_function():
            return "Async request created with retry"
        return async_create_function

# Пример использования BaseRetryProvider
retry_provider = BaseRetryProvider(providers=[ConcreteProvider])
print(f"Retry provider name: {retry_provider.__class__.__name__}")
print(f"Supports streaming: {retry_provider.supports_stream}")
print(f"Create function result: {retry_provider.get_create_function()()}")

from typing import Union

ProviderType = Union[Type[BaseProvider], BaseRetryProvider]

def process_provider(provider: ProviderType):
    print(f"Processing provider: {provider.__name__}")

# Пример использования ProviderType
process_provider(ConcreteProvider)
process_provider(BaseRetryProvider)

class Streaming():
    def __init__(self, data: str) -> None:
        self.data = data

    def __str__(self) -> str:
        return self.data

# Пример использования Streaming
streaming_data = Streaming("This is a stream of data")
print(f"Streaming data: {streaming_data}")
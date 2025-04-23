# Документация для `types.py`

## Обзор

Файл `types.py` определяет типы данных, используемые в клиенте `g4f` для работы с различными провайдерами, такими как `BaseProvider`. В нём определены типы для работы с прокси, итераторами и асинхронными итераторами.

## Детали

Файл содержит определения типов для работы с различными провайдерами, прокси, итераторами и асинхронными итераторами.

## Типы

### `ImageProvider`

```python
ImageProvider = Union[BaseProvider, object]
```

Тип, представляющий провайдера изображений. Может быть экземпляром `BaseProvider` или любым объектом.

### `Proxies`

```python
Proxies = Union[dict, str]
```

Тип, представляющий прокси. Может быть словарём или строкой.

### `IterResponse`

```python
IterResponse = Iterator[Union[ChatCompletion, ChatCompletionChunk]]
```

Тип, представляющий итератор для ответов чат-завершений. Возвращает итератор, который выдаёт экземпляры `ChatCompletion` или `ChatCompletionChunk`.

### `AsyncIterResponse`

```python
AsyncIterResponse = AsyncIterator[Union[ChatCompletion, ChatCompletionChunk]]
```

Тип, представляющий асинхронный итератор для ответов чат-завершений. Возвращает асинхронный итератор, который выдаёт экземпляры `ChatCompletion` или `ChatCompletionChunk`.

## Классы

### `Client`

```python
class Client():
    """
    Клиент для работы с различными провайдерами.

    Attributes:
        api_key (str): Ключ API для аутентификации.
        proxies (Proxies): Прокси для использования при подключении к провайдерам.
        proxy (str): Строка прокси, полученная из `proxies`.

    Methods:
        get_proxy(): Получает прокси из различных источников.
    """
    def __init__(
        self,
        api_key: str = None,
        proxies: Proxies = None,
        **kwargs
    ) -> None:
        """
        Инициализирует экземпляр класса `Client`.

        Args:
            api_key (str, optional): Ключ API для аутентификации. По умолчанию `None`.
            proxies (Proxies, optional): Прокси для использования при подключении к провайдерам. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.
        """
        self.api_key: str = api_key
        self.proxies= proxies 
        self.proxy: str = self.get_proxy()

    def get_proxy(self) -> str | None:
        """
        Получает прокси из различных источников: из переданных `proxies`, из переменной окружения `G4F_PROXY`.

        Returns:
            str | None: Прокси в виде строки или `None`, если прокси не найден.
        """
        if isinstance(self.proxies, str):
            return self.proxies
        elif self.proxies is None:
            return os.environ.get("G4F_PROXY")
        elif "all" in self.proxies:
            return self.proxies["all"]
        elif "https" in self.proxies:
            return self.proxies["https"]
```

#### `Client` Методы

### `get_proxy`

```python
def get_proxy(self) -> str | None:
```

**Назначение**: Функция извлекает прокси-сервер из различных источников: если `self.proxies` является строкой, то возвращает её; если `self.proxies` не установлен, то пытается получить значение из переменной окружения `"G4F_PROXY"`; если в `self.proxies` есть ключ `"all"` или `"https"`, то возвращает соответствующее значение.

**Возвращаемое значение**:
- `str | None`: Значение прокси-сервера, если он найден, или `None`, если прокси-сервер не найден.

**Принцип работы**:
- Проверяет, является ли `self.proxies` строкой. Если да, то функция возвращает это значение.
- Если `self.proxies` равен `None`, функция пытается получить значение переменной окружения `"G4F_PROXY"` и возвращает его.
- Если `self.proxies` является словарём, функция проверяет наличие ключей `"all"` и `"https"` и возвращает соответствующее значение, если оно есть.
- Если ни один из вышеперечисленных вариантов не сработал, функция возвращает `None`.

**Примеры**:
```python
client = Client(proxies="http://proxy.example.com")
print(client.get_proxy())  # Вывод: http://proxy.example.com

os.environ["G4F_PROXY"] = "http://env_proxy.example.com"
client = Client()
print(client.get_proxy())  # Вывод: http://env_proxy.example.com

client = Client(proxies={"all": "http://all_proxy.example.com"})
print(client.get_proxy())  # Вывод: http://all_proxy.example.com

client = Client(proxies={"https": "http://https_proxy.example.com"})
print(client.get_proxy())  # Вывод: http://https_proxy.example.com
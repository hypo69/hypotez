# Документация для модуля `types.py`

## Обзор

Модуль `types.py` содержит абстрактные базовые классы для определения провайдеров, используемых в проекте `hypotez`. Он определяет интерфейсы и базовые атрибуты, необходимые для реализации различных провайдеров, таких как `BaseProvider` и `BaseRetryProvider`. Также содержит класс `Streaming`, используемый для потоковой передачи данных.

## Подробней

Этот модуль предоставляет основные типы и классы, необходимые для работы с различными поставщиками (провайдерами) в системе. `BaseProvider` является основным абстрактным классом, от которого должны наследоваться все провайдеры. `BaseRetryProvider` расширяет `BaseProvider`, добавляя логику повторных попыток с использованием списка провайдеров. Класс `Streaming` используется для представления потоковых данных.

## Классы

### `BaseProvider`

**Описание**: Абстрактный базовый класс для провайдера.

**Атрибуты**:

-   `url` (str): URL провайдера.
-   `working` (bool): Указывает, работает ли провайдер в данный момент.
-   `needs_auth` (bool): Указывает, требуется ли провайдеру аутентификация.
-   `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу.
-   `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
-   `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения.
-   `params` (str): Список параметров для провайдера.

**Методы**:

-   `get_create_function()`: Возвращает функцию создания для провайдера.
-   `get_async_create_function()`: Возвращает асинхронную функцию создания для провайдера.
-   `get_dict()`: Возвращает словарь, содержащий детали провайдера.

### `BaseProvider.get_create_function()`

```python
    @abstractmethod
    def get_create_function() -> callable:
        """
        Get the create function for the provider.

        Returns:
            callable: The create function.
        """
        raise NotImplementedError()
```

**Назначение**: Возвращает функцию создания для провайдера.

**Возвращает**:

-   `callable`: Функция создания.

**Вызывает исключения**:

-   `NotImplementedError`: Если метод не реализован в подклассе.

### `BaseProvider.get_async_create_function()`

```python
    @abstractmethod
    def get_async_create_function() -> callable:
        """
        Get the async create function for the provider.

        Returns:
            callable: The create function.
        """
        raise NotImplementedError()
```

**Назначение**: Возвращает асинхронную функцию создания для провайдера.

**Возвращает**:

-   `callable`: Асинхронная функция создания.

**Вызывает исключения**:

-   `NotImplementedError`: Если метод не реализован в подклассе.

### `BaseProvider.get_dict()`

```python
    @classmethod
    def get_dict(cls) -> Dict[str, str]:
        """
        Get a dictionary representation of the provider.

        Returns:
            Dict[str, str]: A dictionary with provider's details.
        """
        return {'name': cls.__name__, 'url': cls.url, 'label': getattr(cls, 'label', None)}
```

**Назначение**: Возвращает словарь, содержащий детали провайдера.

**Возвращает**:

-   `Dict[str, str]`: Словарь с деталями провайдера, включающий имя, URL и метку (если есть).

**Как работает функция**:

Функция `get_dict` создает и возвращает словарь, содержащий информацию о провайдере. Она использует атрибут `__name__` класса для получения имени провайдера, атрибут `url` для получения URL и, если присутствует атрибут `label`, добавляет его в словарь.

**Примеры**:

```python
class MyProvider(BaseProvider):
    url = "http://example.com"
    label = "Example Provider"

    def get_create_function(self):
        pass

    def get_async_create_function(self):
        pass

provider_dict = MyProvider.get_dict()
print(provider_dict)
# Результат: {'name': 'MyProvider', 'url': 'http://example.com', 'label': 'Example Provider'}
```

### `BaseRetryProvider`

**Описание**: Базовый класс для провайдера, который реализует логику повторных попыток.

**Наследует**: `BaseProvider`

**Атрибуты**:

-   `providers` (List[Type[BaseProvider]]): Список провайдеров для повторных попыток.
-   `shuffle` (bool): Указывает, следует ли перемешивать список провайдеров.
-   `exceptions` (Dict[str, Exception]): Словарь возникших исключений.
-   `last_provider` (Type[BaseProvider]): Последний использованный провайдер.
-   `__name__` (str): Имя класса. Установлено в "RetryProvider".
-   `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу. Всегда `True`.

### `Streaming`

**Описание**: Класс, представляющий потоковые данные.

**Атрибуты**:

-   `data` (str): Данные для потоковой передачи.

**Методы**:

-   `__init__(data: str)`: Конструктор класса.
-   `__str__()`: Возвращает строковое представление данных.

### `Streaming.__init__(data: str)`

```python
    def __init__(self, data: str) -> None:
        self.data = data
```

**Назначение**: Инициализирует экземпляр класса `Streaming`.

**Параметры**:

-   `data` (str): Данные для потоковой передачи.

**Как работает функция**:

Функция `__init__` является конструктором класса `Streaming`. Она принимает параметр `data` и сохраняет его в атрибуте `self.data`.

**Примеры**:

```python
streaming_data = Streaming("Пример потоковых данных")
print(streaming_data.data)
# Результат: "Пример потоковых данных"
```

### `Streaming.__str__()`

```python
    def __str__(self) -> str:
        return self.data
```

**Назначение**: Возвращает строковое представление данных.

**Возвращает**:

-   `str`: Строковое представление данных, содержащихся в атрибуте `self.data`.

**Как работает функция**:

Функция `__str__` возвращает строковое представление данных, хранящихся в атрибуте `self.data`. Это позволяет использовать экземпляр класса `Streaming` в строковых операциях, например, при выводе в консоль.

**Примеры**:

```python
streaming_data = Streaming("Пример потоковых данных")
print(str(streaming_data))
# Результат: "Пример потоковых данных"
```

## Переменные

-   `ProviderType` (Union[Type[BaseProvider], BaseRetryProvider]): Объединение типов `BaseProvider` и `BaseRetryProvider`.

```python
ProviderType = Union[Type[BaseProvider], BaseRetryProvider]
```

## Типы

### `ProviderType`

**Описание**: Union type, представляющий возможные типы провайдеров.

**Типы**:

-   `Type[BaseProvider]`: Тип обычного провайдера.
-   `BaseRetryProvider`: Тип провайдера с логикой повторных попыток.
# Модуль `tiny_factory.py`

## Обзор

Модуль `tiny_factory.py` содержит базовый класс `TinyFactory`, который служит основой для различных типов фабрик. Этот класс облегчает расширение системы, особенно в части кэширования транзакций.

## Подробнее

Модуль предоставляет механизм для создания и управления фабриками, а также для кэширования их состояния. Это позволяет обеспечить консистентность данных при работе с агентами, сгенерированными этими фабриками.

## Классы

### `TinyFactory`

**Описание**: Базовый класс для различных типов фабрик.

**Атрибуты**:
- `all_factories` (dict): Словарь всех созданных фабрик. Ключ - имя фабрики, значение - экземпляр фабрики.
- `name` (str): Имя фабрики, генерируется автоматически при инициализации.
- `simulation_id` (str, optional): ID симуляции, к которой принадлежит фабрика. По умолчанию `None`.

**Методы**:
- `__init__(simulation_id: str = None) -> None`: Инициализирует экземпляр `TinyFactory`.
- `__repr__()`: Возвращает строковое представление объекта `TinyFactory`.
- `set_simulation_for_free_factories(simulation)`: Устанавливает симуляцию для "свободных" фабрик (с `simulation_id is None`).
- `add_factory(factory)`: Добавляет фабрику в список всех фабрик.
- `clear_factories()`: Очищает глобальный список всех фабрик.
- `encode_complete_state() -> dict`: Кодирует полное состояние фабрики.
- `decode_complete_state(state: dict)`: Декодирует полное состояние фабрики.

**Принцип работы**:
Класс `TinyFactory` предоставляет базовую функциональность для создания и управления фабриками в системе. Он включает механизм для отслеживания всех созданных фабрик, установки симуляций для "свободных" фабрик и кэширования состояния фабрик для обеспечения консистентности данных.

## Методы класса

### `__init__`

```python
def __init__(simulation_id: str = None) -> None:
    """
    Инициализирует экземпляр TinyFactory.

    Args:
        simulation_id (str, optional): ID симуляции. По умолчанию None.
    """
    ...
```

**Назначение**: Инициализирует экземпляр класса `TinyFactory`.

**Параметры**:
- `simulation_id` (str, optional): ID симуляции, к которой принадлежит фабрика. По умолчанию `None`.

**Как работает функция**:
Функция инициализирует экземпляр класса `TinyFactory`, присваивает уникальное имя фабрике и добавляет ее в глобальный список всех фабрик.

**Примеры**:

```python
factory1 = TinyFactory(simulation_id="sim1")
print(factory1.name)  # Вывод: Factory <id>

factory2 = TinyFactory()
print(factory2.simulation_id) # Вывод: None
```

### `__repr__`

```python
def __repr__():
    """
    Возвращает строковое представление объекта TinyFactory.
    """
    ...
```

**Назначение**: Возвращает строковое представление объекта `TinyFactory`.

**Возвращает**:
- `str`: Строковое представление объекта `TinyFactory`.

**Как работает функция**:
Функция возвращает строковое представление объекта `TinyFactory`, которое включает имя фабрики.

**Примеры**:

```python
factory = TinyFactory()
print(factory)  # Вывод: TinyFactory(name='Factory <id>')
```

### `set_simulation_for_free_factories`

```python
@staticmethod
def set_simulation_for_free_factories(simulation):
    """
    Устанавливает симуляцию для "свободных" фабрик (с simulation_id is None).
    """
    ...
```

**Назначение**: Устанавливает симуляцию для фабрик, у которых не указан `simulation_id`.

**Параметры**:
- `simulation` (object): Объект симуляции.

**Как работает функция**:
Функция проходит по всем фабрикам в глобальном списке и устанавливает симуляцию для тех, у которых `simulation_id` равен `None`.

**Примеры**:

```python
class Simulation:
    def add_factory(self, factory):
        print(f"Factory {factory.name} added to simulation")

simulation = Simulation()
factory1 = TinyFactory(simulation_id="sim1")
factory2 = TinyFactory()

TinyFactory.set_simulation_for_free_factories(simulation)
# Вывод: Factory Factory <id> added to simulation
```

### `add_factory`

```python
@staticmethod
def add_factory(factory):
    """
    Добавляет фабрику в список всех фабрик.

    Args:
        factory (TinyFactory): Экземпляр фабрики.

    Raises:
        ValueError: Если фабрика с таким именем уже существует.
    """
    ...
```

**Назначение**: Добавляет фабрику в глобальный список всех фабрик.

**Параметры**:
- `factory` (TinyFactory): Экземпляр фабрики.

**Вызывает исключения**:
- `ValueError`: Если фабрика с таким именем уже существует.

**Как работает функция**:
Функция добавляет фабрику в глобальный словарь `all_factories`, проверяя уникальность имени фабрики.

**Примеры**:

```python
factory = TinyFactory()
TinyFactory.add_factory(factory)
print(factory.name in TinyFactory.all_factories)  # Вывод: True
```

### `clear_factories`

```python
@staticmethod
def clear_factories():
    """
    Очищает глобальный список всех фабрик.
    """
    ...
```

**Назначение**: Очищает глобальный список всех фабрик.

**Как работает функция**:
Функция очищает глобальный словарь `all_factories`, удаляя все фабрики из списка.

**Примеры**:

```python
factory = TinyFactory()
TinyFactory.add_factory(factory)
TinyFactory.clear_factories()
print(len(TinyFactory.all_factories))  # Вывод: 0
```

### `encode_complete_state`

```python
def encode_complete_state() -> dict:
    """
    Кодирует полное состояние фабрики.
    """
    ...
```

**Назначение**: Кодирует полное состояние фабрики в словарь.

**Возвращает**:
- `dict`: Словарь, содержащий состояние фабрики.

**Как работает функция**:
Функция создает глубокую копию словаря `__dict__` объекта `TinyFactory` и возвращает ее. Если подклассы имеют несериализуемые элементы, они должны переопределить этот метод.

**Примеры**:

```python
factory = TinyFactory(simulation_id="sim1")
state = factory.encode_complete_state()
print(type(state))  # Вывод: <class 'dict'>
print('name' in state) # Вывод: True
```

### `decode_complete_state`

```python
def decode_complete_state(state: dict):
    """
    Декодирует полное состояние фабрики из словаря.

    Args:
        state (dict): Словарь, содержащий состояние фабрики.
    """
    ...
```

**Назначение**: Декодирует состояние фабрики из словаря.

**Параметры**:
- `state` (dict): Словарь, содержащий состояние фабрики.

**Возвращает**:
- `TinyFactory`: Объект `TinyFactory` с восстановленным состоянием.

**Как работает функция**:
Функция обновляет словарь `__dict__` объекта `TinyFactory` значениями из переданного словаря `state`. Если подклассы имеют несериализуемые элементы, они должны переопределить этот метод.

**Примеры**:

```python
factory = TinyFactory()
state = {'name': 'Factory123', 'simulation_id': 'sim456'}
factory.decode_complete_state(state)
print(factory.name)  # Вывод: Factory123
print(factory.simulation_id)  # Вывод: sim456
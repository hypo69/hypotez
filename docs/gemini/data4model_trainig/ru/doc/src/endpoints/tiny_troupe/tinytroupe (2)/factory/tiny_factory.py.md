# Модуль `tiny_factory.py`

## Обзор

Модуль определяет базовый класс `TinyFactory`, предназначенный для создания различных типов фабрик. Он облегчает расширение системы, особенно в части кэширования транзакций.

## Подробнее

Этот модуль предоставляет основу для создания фабрик в системе `tinytroupe`. Фабрики используются для генерации объектов, и этот модуль предоставляет механизмы для управления и кэширования этих фабрик.

## Классы

### `TinyFactory`

**Описание**:
Базовый класс для различных типов фабрик. Обеспечивает централизованное управление фабриками и поддержку кэширования транзакций.

**Атрибуты**:
- `all_factories` (dict): Словарь, содержащий все созданные фабрики. Ключ - имя фабрики, значение - экземпляр фабрики.
- `name` (str): Имя фабрики. Генерируется автоматически при инициализации.
- `simulation_id` (str, optional): ID симуляции, к которой принадлежит фабрика. По умолчанию `None`.

**Методы**:
- `__init__(self, simulation_id:str=None) -> None`: Инициализирует экземпляр `TinyFactory`.
- `__repr__(self)`: Возвращает строковое представление объекта `TinyFactory`.
- `set_simulation_for_free_factories(simulation)`: Устанавливает симуляцию для фабрик, у которых `simulation_id` равен `None`.
- `add_factory(factory)`: Добавляет фабрику в список всех фабрик.
- `clear_factories()`: Очищает глобальный список всех фабрик.
- `encode_complete_state() -> dict`: Кодирует полное состояние фабрики для кэширования.
- `decode_complete_state(state: dict)`: Декодирует состояние фабрики из кэша.

#### `__init__`

```python
def __init__(self, simulation_id: str = None) -> None:
    """
    Инициализирует экземпляр TinyFactory.

    Args:
        simulation_id (str, optional): ID симуляции. По умолчанию None.

    Returns:
        None
    """
    ...
```

- **Назначение**: Инициализирует экземпляр класса `TinyFactory`. Присваивает фабрике уникальное имя и ID симуляции. Добавляет созданную фабрику в общий список фабрик (`TinyFactory.all_factories`).
- **Параметры**:
    - `simulation_id` (str, optional): ID симуляции, к которой принадлежит фабрика. По умолчанию `None`.
- **Как работает функция**:
    - Присваивает атрибуту `name` уникальное имя, используя функцию `utils.fresh_id()`.
    - Присваивает атрибуту `simulation_id` переданное значение.
    - Вызывает статический метод `TinyFactory.add_factory(self)` для добавления фабрики в общий список.
- **Примеры**:
    ```python
    factory1 = TinyFactory()
    factory2 = TinyFactory(simulation_id="sim_123")
    ```

#### `__repr__`

```python
def __repr__(self):
    """
    Возвращает строковое представление объекта TinyFactory.

    Args:
        self: Экземпляр класса TinyFactory.

    Returns:
        str: Строковое представление объекта.
    """
    ...
```

- **Назначение**: Возвращает строковое представление объекта `TinyFactory`.
- **Как работает функция**:
    - Формирует строку, содержащую имя класса и имя фабрики.
- **Примеры**:
    ```python
    factory = TinyFactory()
    print(factory)  # Выведет что-то вроде: TinyFactory(name='Factory 123')
    ```

#### `set_simulation_for_free_factories`

```python
@staticmethod
def set_simulation_for_free_factories(simulation):
    """
    Устанавливает симуляцию для фабрик, у которых simulation_id равен None.

    Args:
        simulation: Объект симуляции.

    Returns:
        None
    """
    ...
```

- **Назначение**: Устанавливает симуляцию для фабрик, у которых атрибут `simulation_id` равен `None`. Это позволяет привязать фабрики, созданные вне контекста конкретной симуляции, к определенной симуляции.
- **Параметры**:
    - `simulation`: Объект симуляции, к которой нужно привязать фабрики.
- **Как работает функция**:
    - Перебирает все фабрики в `TinyFactory.all_factories`.
    - Если у фабрики `simulation_id` равен `None`, вызывает метод `simulation.add_factory(factory)` для привязки фабрики к симуляции.
- **Примеры**:
    ```python
    from unittest.mock import Mock
    simulation = Mock()  # Создаем фиктивную симуляцию
    TinyFactory.set_simulation_for_free_factories(simulation)
    ```

#### `add_factory`

```python
@staticmethod
def add_factory(factory):
    """
    Добавляет фабрику в список всех фабрик.

    Args:
        factory: Экземпляр фабрики для добавления.

    Raises:
        ValueError: Если фабрика с таким именем уже существует.

    Returns:
        None
    """
    ...
```

- **Назначение**: Добавляет фабрику в общий список фабрик (`TinyFactory.all_factories`). Имена фабрик должны быть уникальными.
- **Параметры**:
    - `factory`: Экземпляр фабрики, который нужно добавить.
- **Как работает функция**:
    - Проверяет, существует ли фабрика с таким же именем в словаре `TinyFactory.all_factories`.
    - Если фабрика с таким именем уже существует, выбрасывает исключение `ValueError`.
    - Если имя уникально, добавляет фабрику в словарь `TinyFactory.all_factories`.
- **Примеры**:
    ```python
    factory = TinyFactory()
    TinyFactory.add_factory(factory)
    ```

#### `clear_factories`

```python
@staticmethod
def clear_factories():
    """
    Очищает глобальный список всех фабрик.

    Args:
        None

    Returns:
        None
    """
    ...
```

- **Назначение**: Очищает глобальный список всех фабрик (`TinyFactory.all_factories`).
- **Как работает функция**:
    - Присваивает атрибуту `TinyFactory.all_factories` пустой словарь.
- **Примеры**:
    ```python
    TinyFactory.clear_factories()
    ```

#### `encode_complete_state`

```python
def encode_complete_state(self) -> dict:
    """
    Кодирует полное состояние фабрики.

    Args:
        self: Экземпляр класса TinyFactory.

    Returns:
        dict: Словарь, содержащий закодированное состояние фабрики.
    """
    ...
```

- **Назначение**: Кодирует полное состояние фабрики для кэширования.
- **Как работает функция**:
    - Создает глубокую копию словаря `__dict__` экземпляра фабрики.
- **Примеры**:
    ```python
    factory = TinyFactory()
    state = factory.encode_complete_state()
    ```

#### `decode_complete_state`

```python
def decode_complete_state(self, state: dict):
    """
    Декодирует состояние фабрики из словаря.

    Args:
        self: Экземпляр класса TinyFactory.
        state (dict): Словарь, содержащий состояние фабрики.

    Returns:
        self: Возвращает экземпляр класса TinyFactory с восстановленным состоянием.
    """
    ...
```

- **Назначение**: Декодирует состояние фабрики из предоставленного словаря. Используется для восстановления состояния фабрики из кэша.
- **Параметры**:
    - `state` (dict): Словарь, содержащий состояние фабрики.
- **Как работает функция**:
    - Обновляет словарь `__dict__` экземпляра фабрики данными из словаря `state`.
    - Возвращает экземпляр фабрики.
- **Примеры**:
    ```python
    factory = TinyFactory()
    state = {'name': 'Factory 456', 'simulation_id': 'sim_456'}
    factory.decode_complete_state(state)
    print(factory.name)  # Выведет: Factory 456
    ```
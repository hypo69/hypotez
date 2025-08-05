# Модуль `tiny_factory.py`

## Обзор

Модуль определяет базовый класс `TinyFactory`, предназначенный для создания различных типов фабрик. Он обеспечивает централизованное управление фабриками, их регистрацию и хранение, а также механизмы кэширования для обеспечения консистентности данных при работе с агентами. Этот класс облегчает расширение системы и управление транзакциями.

## Подробнее

Этот модуль играет важную роль в архитектуре проекта, предоставляя основу для создания и управления фабриками объектов. Он обеспечивает уникальность имен фабрик, позволяет привязывать их к определенным симуляциям и предоставляет механизмы для кэширования состояний фабрик.

## Классы

### `TinyFactory`

**Описание**: Базовый класс для создания различных типов фабрик. Обеспечивает управление фабриками, их регистрацию и кэширование.

**Атрибуты**:

- `all_factories` (dict): Словарь, содержащий все созданные фабрики. Ключ - имя фабрики, значение - объект фабрики.
- `name` (str): Имя фабрики. Генерируется автоматически при создании экземпляра.
- `simulation_id` (str, optional): ID симуляции, к которой привязана фабрика. По умолчанию `None`.

**Методы**:

- `__init__(self, simulation_id: str = None) -> None`
- `__repr__(self)`
- `set_simulation_for_free_factories(simulation)`
- `add_factory(factory)`
- `clear_factories()`
- `encode_complete_state() -> dict`
- `decode_complete_state(state: dict)`

#### `__init__(self, simulation_id: str = None) -> None`

**Назначение**: Инициализирует экземпляр класса `TinyFactory`.

**Параметры**:

- `simulation_id` (str, optional): ID симуляции, к которой привязана фабрика. По умолчанию `None`.

**Как работает функция**:

- Функция присваивает фабрике уникальное имя, используя `utils.fresh_id()`.
- Сохраняет `simulation_id`.
- Добавляет фабрику в глобальный список `TinyFactory.all_factories` с помощью метода `TinyFactory.add_factory(self)`.

#### `__repr__(self)`

**Назначение**: Возвращает строковое представление объекта `TinyFactory`.

**Возвращает**:

- `str`: Строковое представление фабрики в формате "TinyFactory(name='имя_фабрики')".

#### `set_simulation_for_free_factories(simulation)`

**Назначение**: Привязывает "свободные" фабрики (с `simulation_id` равным `None`) к указанной симуляции.

**Параметры**:

- `simulation`: Объект симуляции, к которой нужно привязать фабрики.

**Как работает функция**:

- Перебирает все фабрики в `TinyFactory.all_factories`.
- Если `simulation_id` фабрики равен `None`, добавляет фабрику в симуляцию с помощью метода `simulation.add_factory(factory)`.

#### `add_factory(factory)`

**Назначение**: Добавляет фабрику в глобальный список `TinyFactory.all_factories`.

**Параметры**:

- `factory`: Объект фабрики, который нужно добавить.

**Вызывает исключения**:

- `ValueError`: Если фабрика с таким именем уже существует.

**Как работает функция**:

- Проверяет, существует ли фабрика с таким именем в `TinyFactory.all_factories`.
- Если фабрика с таким именем уже существует, выбрасывает исключение `ValueError`.
- В противном случае добавляет фабрику в `TinyFactory.all_factories`.

#### `clear_factories()`

**Назначение**: Очищает глобальный список всех фабрик.

**Как работает функция**:

- Устанавливает `TinyFactory.all_factories` в пустой словарь.

#### `encode_complete_state() -> dict`

**Назначение**: Кодирует полное состояние фабрики в словарь.

**Возвращает**:

- `dict`: Словарь, содержащий копию `__dict__` объекта фабрики.

**Как работает функция**:

- Создает глубокую копию словаря `__dict__` объекта фабрики.
- Возвращает эту копию.

#### `decode_complete_state(state: dict)`

**Назначение**: Декодирует состояние фабрики из словаря.

**Параметры**:

- `state` (dict): Словарь, содержащий состояние фабрики.

**Возвращает**:

- `self`: Объект фабрики с обновленным состоянием.

**Как работает функция**:

- Создает глубокую копию словаря `state`.
- Обновляет словарь `__dict__` объекта фабрики значениями из `state`.
- Возвращает объект фабрики.

## Примеры

### Создание экземпляра `TinyFactory`

```python
from tinytroupe.factory.tiny_factory import TinyFactory

factory = TinyFactory(simulation_id="sim123")
print(factory)  # Вывод: TinyFactory(name='Factory 1') (Имя может отличаться)
```

### Добавление фабрики

```python
from tinytroupe.factory.tiny_factory import TinyFactory

factory1 = TinyFactory(simulation_id="sim123")
factory2 = TinyFactory(simulation_id="sim456")

print(TinyFactory.all_factories)
```

### Очистка фабрик

```python
from tinytroupe.factory.tiny_factory import TinyFactory

factory1 = TinyFactory(simulation_id="sim123")
factory2 = TinyFactory(simulation_id="sim456")

TinyFactory.clear_factories()

print(TinyFactory.all_factories) # {}
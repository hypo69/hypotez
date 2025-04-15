# Модуль управления симуляцией `tinytroupe`

## Обзор

Модуль предоставляет механизмы для управления симуляциями, включая запуск, остановку, сохранение состояния и использование кэша для ускорения выполнения. Он включает классы `Simulation` и `Transaction`, а также вспомогательные функции для управления симуляциями.

## Подробнее

Этот модуль предназначен для контроля и управления симуляциями в проекте `tinytroupe`. Он позволяет запускать и останавливать симуляции, сохранять их состояние в кэш-файл для последующего восстановления, а также выполнять транзакции с возможностью кэширования результатов. Модуль использует классы агентов, сред и фабрик для моделирования различных аспектов симуляции.

## Классы

### `Simulation`

**Описание**: Класс для управления симуляцией.

**Атрибуты**:
- `id` (str): Идентификатор симуляции. По умолчанию `"default"`.
- `agents` (list): Список агентов в симуляции.
- `name_to_agent` (dict): Словарь, отображающий имя агента в объект агента (`{agent_name: agent, ...}`).
- `environments` (list): Список сред в симуляции.
- `factories` (list): Список фабрик в симуляции (например, экземпляры `TinyPersonFactory`).
- `name_to_factory` (dict): Словарь, отображающий имя фабрики в объект фабрики (`{factory_name: factory, ...}`).
- `name_to_environment` (dict): Словарь, отображающий имя среды в объект среды (`{environment_name: environment, ...}`).
- `status` (str): Статус симуляции (`"stopped"` или `"started"`).
- `cache_path` (str): Путь к файлу кэша. По умолчанию `"./tinytroupe-{id}.cache.json"`.
- `auto_checkpoint` (bool): Флаг автоматического сохранения состояния после каждой транзакции. По умолчанию `False`.
- `has_unsaved_cache_changes` (bool): Флаг, указывающий на наличие несохраненных изменений в кэше.
- `_under_transaction` (bool): Флаг, указывающий на то, что симуляция находится в состоянии транзакции.
- `cached_trace` (list): Список состояний симуляции, используемых для кэширования.
- `cache_misses` (int): Количество промахов кэша.
- `cache_hits` (int): Количество попаданий в кэш.
- `execution_trace` (list): Список состояний выполнения симуляции.

**Методы**:
- `begin(cache_path: str = None, auto_checkpoint: bool = False)`: Отмечает начало управляемой симуляции.
- `end()`: Отмечает конец управляемой симуляции.
- `checkpoint()`: Сохраняет текущий след симуляции в файл.
- `add_agent(agent)`: Добавляет агента в симуляцию.
- `add_environment(environment)`: Добавляет среду в симуляцию.
- `add_factory(factory)`: Добавляет фабрику в симуляцию.
- `_execution_trace_position() -> int`: Возвращает текущую позицию в трассировке выполнения или -1, если трассировка выполнения пуста.
- `_function_call_hash(function_name, *args, **kwargs) -> int`: Вычисляет хэш заданного вызова функции.
- `_skip_execution_with_cache()`: Пропускает текущее выполнение, предполагая, что в той же позиции есть кэшированное состояние.
- `_is_transaction_event_cached(event_hash) -> bool`: Проверяет, соответствует ли данный хэш события соответствующему кэшированному, если таковой имеется.
- `_drop_cached_trace_suffix()`: Удаляет суффикс кэшированного следа, начиная с текущей позиции следа выполнения.
- `_add_to_execution_trace(state: dict, event_hash: int, event_output)`: Добавляет состояние в список execution_trace и вычисляет соответствующий хэш.
- `_add_to_cache_trace(state: dict, event_hash: int, event_output)`: Добавляет состояние в список cached_trace и вычисляет соответствующий хэш.
- `_load_cache_file(cache_path: str)`: Загружает файл кэша из указанного пути.
- `_save_cache_file(cache_path: str)`: Сохраняет файл кэша по указанному пути. Всегда перезаписывает.
- `begin_transaction()`: Начинает транзакцию.
- `end_transaction()`: Завершает транзакцию.
- `is_under_transaction()`: Проверяет, находится ли агент в транзакции.
- `_clear_communications_buffers()`: Очищает буферы связи всех агентов и сред.
- `_encode_simulation_state() -> dict`: Кодирует текущее состояние симуляции, включая агентов, среды и другую релевантную информацию.
- `_decode_simulation_state(state: dict)`: Декодирует данное состояние симуляции, включая агентов, среды и другую релевантную информацию.

#### `Simulation.begin`

```python
def begin(self, cache_path: str = None, auto_checkpoint: bool = False):
    """
    Отмечает начало управляемой симуляции.

    Args:
        cache_path (str, optional): Путь к файлу кэша. Если не указан, используется путь по умолчанию, определенный в классе. По умолчанию `None`.
        auto_checkpoint (bool, optional): Определяет, следует ли автоматически создавать контрольные точки в конце каждой транзакции. По умолчанию `False`.

    Raises:
        ValueError: Если симуляция уже запущена.
    """
    ...
```

#### `Simulation.end`

```python
def end(self):
    """
    Отмечает конец управляемой симуляции.

    Raises:
        ValueError: Если симуляция уже остановлена.
    """
    ...
```

#### `Simulation.checkpoint`

```python
def checkpoint(self):
    """
    Сохраняет текущий след симуляции в файл.
    """
    ...
```

#### `Simulation.add_agent`

```python
def add_agent(self, agent):
    """
    Добавляет агента в симуляцию.

    Args:
        agent: Объект агента для добавления.

    Raises:
        ValueError: Если имя агента уже используется.
    """
    ...
```

#### `Simulation.add_environment`

```python
def add_environment(self, environment):
    """
    Добавляет среду в симуляцию.

    Args:
        environment: Объект среды для добавления.

    Raises:
        ValueError: Если имя среды уже используется.
    """
    ...
```

#### `Simulation.add_factory`

```python
def add_factory(self, factory):
    """
    Добавляет фабрику в симуляцию.

    Args:
        factory: Объект фабрики для добавления.

    Raises:
        ValueError: Если имя фабрики уже используется.
    """
    ...
```

#### `Simulation._execution_trace_position`

```python
def _execution_trace_position(self) -> int:
    """
    Возвращает текущую позицию в трассировке выполнения или -1, если трассировка выполнения пуста.
    """
    ...
```

#### `Simulation._function_call_hash`

```python
def _function_call_hash(self, function_name, *args, **kwargs) -> int:
    """
    Вычисляет хэш заданного вызова функции.
    """
    ...
```

#### `Simulation._skip_execution_with_cache`

```python
def _skip_execution_with_cache(self):
    """
    Пропускает текущее выполнение, предполагая, что в той же позиции есть кэшированное состояние.
    """
    ...
```

#### `Simulation._is_transaction_event_cached`

```python
def _is_transaction_event_cached(self, event_hash) -> bool:
    """
    Проверяет, соответствует ли данный хэш события соответствующему кэшированному, если таковой имеется.

    Args:
        event_hash: Хэш события.

    Returns:
        bool: True, если хэш события соответствует кэшированному, иначе False.
    """
    ...
```

#### `Simulation._drop_cached_trace_suffix`

```python
def _drop_cached_trace_suffix(self):
    """
    Удаляет суффикс кэшированного следа, начиная с текущей позиции следа выполнения.
    """
    ...
```

#### `Simulation._add_to_execution_trace`

```python
def _add_to_execution_trace(self, state: dict, event_hash: int, event_output):
    """
    Добавляет состояние в список execution_trace и вычисляет соответствующий хэш.

    Args:
        state (dict): Состояние для добавления.
        event_hash (int): Хэш события.
        event_output: Вывод события.
    """
    ...
```

#### `Simulation._add_to_cache_trace`

```python
def _add_to_cache_trace(self, state: dict, event_hash: int, event_output):
    """
    Добавляет состояние в список cached_trace и вычисляет соответствующий хэш.

    Args:
        state (dict): Состояние для добавления.
        event_hash (int): Хэш события.
        event_output: Вывод события.
    """
    ...
```

#### `Simulation._load_cache_file`

```python
def _load_cache_file(self, cache_path: str):
    """
    Загружает файл кэша из указанного пути.

    Args:
        cache_path (str): Путь к файлу кэша.
    """
    ...
```

#### `Simulation._save_cache_file`

```python
def _save_cache_file(self, cache_path: str):
    """
    Сохраняет файл кэша по указанному пути. Всегда перезаписывает.

    Args:
        cache_path (str): Путь к файлу кэша.
    """
    ...
```

#### `Simulation.begin_transaction`

```python
def begin_transaction(self):
    """
    Начинает транзакцию.
    """
    ...
```

#### `Simulation.end_transaction`

```python
def end_transaction(self):
    """
    Завершает транзакцию.
    """
    ...
```

#### `Simulation.is_under_transaction`

```python
def is_under_transaction(self):
    """
    Проверяет, находится ли агент в транзакции.
    """
    ...
```

#### `Simulation._clear_communications_buffers`

```python
def _clear_communications_buffers(self):
    """
    Очищает буферы связи всех агентов и сред.
    """
    ...
```

#### `Simulation._encode_simulation_state`

```python
def _encode_simulation_state(self) -> dict:
    """
    Кодирует текущее состояние симуляции, включая агентов, среды и другую релевантную информацию.

    Returns:
        dict: Закодированное состояние симуляции.
    """
    ...
```

#### `Simulation._decode_simulation_state`

```python
def _decode_simulation_state(self, state: dict):
    """
    Декодирует данное состояние симуляции, включая агентов, среды и другую релевантную информацию.

    Args:
        state (dict): Состояние для декодирования.
    """
    ...
```

### `Transaction`

**Описание**: Класс для управления транзакциями в симуляции.

**Атрибуты**:
- `obj_under_transaction`: Объект, находящийся под транзакцией.
- `simulation`: Объект симуляции, в которой выполняется транзакция.
- `function_name` (str): Имя функции, выполняемой в транзакции.
- `function`: Функция, выполняемая в транзакции.
- `args` (tuple): Позиционные аргументы, передаваемые в функцию.
- `kwargs` (dict): Именованные аргументы, передаваемые в функцию.

**Методы**:
- `execute()`: Выполняет транзакцию.
- `_encode_function_output(output) -> dict`: Кодирует заданный вывод функции.
- `_decode_function_output(encoded_output: dict)`: Декодирует заданный закодированный вывод функции.

#### `Transaction.execute`

```python
def execute(self):
    """
    Выполняет транзакцию.

    Returns:
        Результат выполнения функции.
    """
    ...
```

#### `Transaction._encode_function_output`

```python
def _encode_function_output(self, output) -> dict:
    """
    Кодирует заданный вывод функции.

    Args:
        output: Вывод функции для кодирования.

    Returns:
        dict: Закодированный вывод функции.
    """
    ...
```

#### `Transaction._decode_function_output`

```python
def _decode_function_output(self, encoded_output: dict):
    """
    Декодирует заданный закодированный вывод функции.

    Args:
        encoded_output (dict): Закодированный вывод функции.

    Returns:
        Декодированный вывод функции.
    """
    ...
```

## Функции

### `transactional(func)`

```python
def transactional(func):
    """
    Декоратор, который делает функцию симуляционно-транзакционной.
    """
    ...
```

### `reset()`

```python
def reset():
    """
    Сбрасывает все состояние управления симуляцией.
    """
    ...
```

### `_simulation(id="default")`

```python
def _simulation(id="default"):
    """
    Возвращает объект симуляции с заданным идентификатором. Если симуляция с таким идентификатором не существует, создает новую.

    Args:
        id (str, optional): Идентификатор симуляции. По умолчанию `"default"`.

    Returns:
        Simulation: Объект симуляции.
    """
    ...
```

### `begin(cache_path=None, id="default", auto_checkpoint=False)`

```python
def begin(cache_path=None, id="default", auto_checkpoint=False):
    """
    Отмечает начало управляемой симуляции.

    Args:
        cache_path (str, optional): Путь к файлу кэша. По умолчанию `None`.
        id (str, optional): Идентификатор симуляции. По умолчанию `"default"`.
        auto_checkpoint (bool, optional): Флаг автоматического сохранения состояния после каждой транзакции. По умолчанию `False`.

    Raises:
        ValueError: Если симуляция уже запущена.
    """
    ...
```

### `end(id="default")`

```python
def end(id="default")`:
    """
    Отмечает конец управляемой симуляции.

    Args:
        id (str, optional): Идентификатор симуляции. По умолчанию `"default"`.
    """
    ...
```

### `checkpoint(id="default")`

```python
def checkpoint(id="default")`:
    """
    Сохраняет текущее состояние симуляции.

    Args:
        id (str, optional): Идентификатор симуляции. По умолчанию `"default"`.
    """
    ...
```

### `current_simulation()`

```python
def current_simulation():
    """
    Возвращает текущую симуляцию.

    Returns:
        Simulation: Текущая симуляция или `None`, если симуляция не запущена.
    """
    ...
```

### `cache_hits(id="default")`

```python
def cache_hits(id="default"):
    """
    Возвращает количество попаданий в кэш.

    Args:
        id (str, optional): Идентификатор симуляции. По умолчанию `"default"`.

    Returns:
        int: Количество попаданий в кэш.
    """
    ...
```

### `cache_misses(id="default")`

```python
def cache_misses(id="default")`:
    """
    Возвращает количество промахов кэша.

    Args:
        id (str, optional): Идентификатор симуляции. По умолчанию `"default"`.

    Returns:
        int: Количество промахов кэша.
    """
    ...
```

## Параметры класса

- `id` (str): Идентификатор симуляции.
- `agents` (list): Список агентов в симуляции.
- `environments` (list): Список сред в симуляции.
- `factories` (list): Список фабрик в симуляции.
- `status` (str): Статус симуляции.
- `cache_path` (str): Путь к файлу кэша.
- `auto_checkpoint` (bool): Флаг автоматического сохранения.
- `has_unsaved_cache_changes` (bool): Флаг наличия несохраненных изменений.
- `_under_transaction` (bool): Флаг состояния транзакции.
- `cached_trace` (list): Список состояний кэша.
- `cache_misses` (int): Количество промахов кэша.
- `cache_hits` (int): Количество попаданий в кэш.
- `execution_trace` (list): Список состояний выполнения.

## Примеры

### Создание и запуск симуляции

```python
from tinytroupe.control import begin, end, current_simulation

begin(id="my_simulation", cache_path="./my_simulation.cache.json")
simulation = current_simulation()
print(f"Simulation id: {simulation.id}")

end(id="my_simulation")
```

### Добавление агента в симуляцию

```python
from tinytroupe.control import begin, end, current_simulation
from tinytroupe.agent import TinyPerson

begin(id="my_simulation")
simulation = current_simulation()

agent = TinyPerson(name="Alice")
simulation.add_agent(agent)

end(id="my_simulation")
```

### Использование транзакций

```python
from tinytroupe.control import begin, end, transactional
from tinytroupe.agent import TinyPerson

begin(id="my_simulation")

class MyObject:
    def __init__(self):
        self.value = 0

    @transactional
    def increment(self, amount: int) -> int:
        """
        Увеличивает значение объекта на заданную величину.

        Args:
            amount (int): Величина для увеличения значения.

        Returns:
            int: Новое значение объекта.
        """
        self.value += amount
        return self.value

my_object = MyObject()
my_object.increment(5)

end(id="my_simulation")
```
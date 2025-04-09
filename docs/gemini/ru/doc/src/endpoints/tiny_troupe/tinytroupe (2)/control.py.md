# Модуль управления симуляцией Tiny Troupe

## Обзор

Модуль `control.py` предназначен для управления симуляциями в проекте Tiny Troupe. Он предоставляет классы и функции для запуска, остановки, сохранения состояния симуляции, а также для управления транзакциями и кэшированием. Модуль позволяет создавать и управлять агентами, средами и фабриками в рамках симуляции.

## Подробнее

Этот модуль является ключевым компонентом системы симуляции Tiny Troupe. Он предоставляет инструменты для управления жизненным циклом симуляции, включая инициализацию, выполнение и завершение. Модуль также обеспечивает механизмы для кэширования состояний симуляции, что позволяет ускорить повторные прогоны и отладку.

## Содержание

1.  [Классы](#классы)
    *   [Simulation](#simulation)
    *   [Transaction](#transaction)
    *   [SkipTransaction](#skiptransaction)
    *   [CacheOutOfSync](#cacheoutofsync)
    *   [ExecutionCached](#executioncached)
2.  [Функции](#функции)
    *   [reset](#reset)
    *   [_simulation](#_simulation)
    *   [begin](#begin)
    *   [end](#end)
    *   [checkpoint](#checkpoint)
    *   [current\_simulation](#current_simulation)
    *   [cache\_hits](#cache_hits)
    *   [cache\_misses](#cache_misses)
    *   [transactional](#transactional)

## Классы

### `Simulation`

**Описание**: Класс `Simulation` управляет состоянием и выполнением симуляции. Он содержит методы для добавления агентов, сред и фабрик, а также для управления кэшированием и транзакциями.

**Принцип работы**: Класс `Simulation` инициализируется с уникальным идентификатором. Он поддерживает запуск, остановку и сохранение состояния симуляции. Кэширование состояний позволяет оптимизировать повторное выполнение симуляций. Класс также управляет транзакциями, обеспечивая целостность данных во время выполнения симуляции.

**Аттрибуты**:

*   `id` (str): Уникальный идентификатор симуляции.
*   `agents` (list): Список агентов, участвующих в симуляции.
*   `name_to_agent` (dict): Словарь, отображающий имена агентов в их экземпляры.
*   `environments` (list): Список сред, в которых происходит симуляция.
*   `factories` (list): Список фабрик, используемых для создания объектов в симуляции.
*   `name_to_factory` (dict): Словарь, отображающий имена фабрик в их экземпляры.
*   `name_to_environment` (dict): Словарь, отображающий имена сред в их экземпляры.
*   `status` (str): Статус симуляции (`"started"` или `"stopped"`).
*   `cache_path` (str): Путь к файлу кэша.
*   `auto_checkpoint` (bool): Флаг автоматического сохранения состояния после каждой транзакции.
*   `has_unsaved_cache_changes` (bool): Флаг, указывающий на наличие несохраненных изменений в кэше.
*   `_under_transaction` (bool): Флаг, указывающий на то, что симуляция находится в состоянии транзакции.
*   `cached_trace` (list): Список состояний симуляции, сохраненных в кэше.
*   `cache_misses` (int): Количество промахов кэша.
*   `cache_hits` (int): Количество попаданий в кэш.
*   `execution_trace` (list): Список состояний выполнения симуляции.

**Методы**:

*   `__init__(self, id="default", cached_trace: list = None)`: Инициализирует новый экземпляр класса `Simulation`.
*   `begin(self, cache_path: str = None, auto_checkpoint: bool = False)`: Запускает симуляцию.
*   `end(self)`: Останавливает симуляцию.
*   `checkpoint(self)`: Сохраняет текущее состояние симуляции в файл.
*   `add_agent(self, agent)`: Добавляет агента в симуляцию.
*   `add_environment(self, environment)`: Добавляет среду в симуляцию.
*   `add_factory(self, factory)`: Добавляет фабрику в симуляцию.
*   `_execution_trace_position(self) -> int`: Возвращает текущую позицию в трассе выполнения.
*   `_function_call_hash(self, function_name, *args, **kwargs) -> int`: Вычисляет хеш вызова функции.
*   `_skip_execution_with_cache(self)`: Пропускает выполнение, используя кэшированное состояние.
*   `_is_transaction_event_cached(self, event_hash) -> bool`: Проверяет, кэшировано ли событие транзакции.
*   `_drop_cached_trace_suffix(self)`: Удаляет суффикс кэшированной трассы.
*   `_add_to_execution_trace(self, state: dict, event_hash: int, event_output)`: Добавляет состояние в трассу выполнения.
*   `_add_to_cache_trace(self, state: dict, event_hash: int, event_output)`: Добавляет состояние в кэшированную трассу.
*   `_load_cache_file(self, cache_path: str)`: Загружает кэш из файла.
*   `_save_cache_file(self, cache_path: str)`: Сохраняет кэш в файл.
*   `begin_transaction(self)`: Начинает транзакцию.
*   `end_transaction(self)`: Завершает транзакцию.
*   `is_under_transaction(self)`: Проверяет, находится ли симуляция в состоянии транзакции.
*   `_clear_communications_buffers(self)`: Очищает буферы обмена данными агентов и сред.
*   `_encode_simulation_state(self) -> dict`: Кодирует текущее состояние симуляции.
*   `_decode_simulation_state(self, state: dict)`: Декодирует состояние симуляции.

#### `Simulation.__init__`

```python
def __init__(self, id="default", cached_trace: list = None):
```

**Назначение**: Инициализирует новый экземпляр класса `Simulation`.

**Параметры**:

*   `id` (str): Уникальный идентификатор симуляции. По умолчанию `"default"`.
*   `cached_trace` (list, optional): Начальная трасса кэшированных состояний. По умолчанию `None`.

**Как работает функция**:

1.  Инициализация атрибутов класса, таких как `id`, `agents`, `environments`, `factories`, `status`, `cache_path`, `auto_checkpoint`, `has_unsaved_cache_changes`, `_under_transaction`, `cached_trace`, `cache_misses`, `cache_hits`, и `execution_trace`.
2.  Если предоставлена начальная трасса кэшированных состояний (`cached_trace`), она используется для инициализации атрибута `cached_trace`. В противном случае атрибут инициализируется пустым списком.

```
A: Инициализация атрибутов класса
|
B: Проверка наличия начальной трассы кэшированных состояний (cached_trace)
|
C: Инициализация атрибута cached_trace либо предоставленным значением, либо пустым списком
```

**Примеры**:

```python
# Создание экземпляра Simulation с идентификатором "my_simulation"
simulation = Simulation(id="my_simulation")

# Создание экземпляра Simulation с предопределенной трассой кэшированных состояний
cached_trace = [{"state": "initial_state"}]
simulation = Simulation(id="my_simulation", cached_trace=cached_trace)
```

#### `Simulation.begin`

```python
def begin(self, cache_path: str = None, auto_checkpoint: bool = False):
```

**Назначение**: Запускает симуляцию.

**Параметры**:

*   `cache_path` (str, optional): Путь к файлу кэша. Если не указан, используется путь по умолчанию. По умолчанию `None`.
*   `auto_checkpoint` (bool, optional): Флаг автоматического сохранения состояния после каждой транзакции. По умолчанию `False`.

**Как работает функция**:

1.  Проверяет, не была ли уже запущена симуляция. Если симуляция уже запущена, вызывается исключение `ValueError`.
2.  Устанавливает статус симуляции в `"started"`.
3.  Устанавливает путь к файлу кэша, если он был указан.
4.  Устанавливает флаг автоматического сохранения состояния.
5.  Очищает списки агентов, сред и фабрик.
6.  Сбрасывает счетчик автоматических идентификаторов.
7.  Загружает кэш из файла, если он существует.

```
A: Проверка статуса симуляции
|
B: Установка статуса симуляции в "started"
|
C: Установка пути к файлу кэша и флага auto_checkpoint
|
D: Очистка списков агентов, сред и фабрик
|
E: Сброс счетчика автоматических идентификаторов
|
F: Загрузка кэша из файла (если cache_path указан)
```

**Примеры**:

```python
# Запуск симуляции с путем к файлу кэша
simulation = Simulation()
simulation.begin(cache_path="./my_simulation.cache.json")

# Запуск симуляции с автоматическим сохранением состояния
simulation = Simulation()
simulation.begin(auto_checkpoint=True)
```

#### `Simulation.end`

```python
def end(self):
```

**Назначение**: Останавливает симуляцию.

**Как работает функция**:

1.  Проверяет, была ли запущена симуляция. Если симуляция не была запущена, вызывается исключение `ValueError`.
2.  Устанавливает статус симуляции в `"stopped"`.
3.  Сохраняет текущее состояние симуляции в файл.

```
A: Проверка статуса симуляции
|
B: Установка статуса симуляции в "stopped"
|
C: Сохранение текущего состояния симуляции в файл
```

**Примеры**:

```python
# Завершение симуляции
simulation = Simulation()
simulation.begin()
simulation.end()
```

#### `Simulation.checkpoint`

```python
def checkpoint(self):
```

**Назначение**: Сохраняет текущее состояние симуляции в файл.

**Как работает функция**:

1.  Проверяет, есть ли несохраненные изменения в кэше.
2.  Если есть несохраненные изменения, сохраняет кэш в файл.

```
A: Проверка наличия несохраненных изменений в кэше
|
B: Сохранение кэша в файл (если есть несохраненные изменения)
```

**Примеры**:

```python
# Сохранение состояния симуляции
simulation = Simulation()
simulation.begin()
# ... выполнение симуляции ...
simulation.checkpoint()
```

#### `Simulation.add_agent`

```python
def add_agent(self, agent):
```

**Назначение**: Добавляет агента в симуляцию.

**Как работает функция**:

1.  Проверяет, не существует ли уже агент с таким же именем в симуляции. Если существует, вызывается исключение `ValueError`.
2.  Устанавливает идентификатор симуляции для агента.
3.  Добавляет агента в список агентов симуляции.
4.  Добавляет агента в словарь `name_to_agent`, где ключом является имя агента, а значением - сам агент.

```
A: Проверка уникальности имени агента
|
B: Установка идентификатора симуляции для агента
|
C: Добавление агента в список агентов и в словарь name_to_agent
```

**Примеры**:

```python
from tinytroupe.agent import TinyPerson
# Создание агента
agent = TinyPerson(name="Alice")

# Добавление агента в симуляцию
simulation = Simulation()
simulation.add_agent(agent)
```

#### `Simulation.add_environment`

```python
def add_environment(self, environment):
```

**Назначение**: Добавляет среду в симуляцию.

**Как работает функция**:

1.  Проверяет, не существует ли уже среда с таким же именем в симуляции. Если существует, вызывается исключение `ValueError`.
2.  Устанавливает идентификатор симуляции для среды.
3.  Добавляет среду в список сред симуляции.
4.  Добавляет среду в словарь `name_to_environment`, где ключом является имя среды, а значением - сама среда.

```
A: Проверка уникальности имени среды
|
B: Установка идентификатора симуляции для среды
|
C: Добавление среды в список сред и в словарь name_to_environment
```

**Примеры**:

```python
from tinytroupe.environment import TinyWorld
# Создание среды
environment = TinyWorld(name="World")

# Добавление среды в симуляцию
simulation = Simulation()
simulation.add_environment(environment)
```

#### `Simulation.add_factory`

```python
def add_factory(self, factory):
```

**Назначение**: Добавляет фабрику в симуляцию.

**Как работает функция**:

1.  Проверяет, не существует ли уже фабрика с таким же именем в симуляции. Если существует, вызывается исключение `ValueError`.
2.  Устанавливает идентификатор симуляции для фабрики.
3.  Добавляет фабрику в список фабрик симуляции.
4.  Добавляет фабрику в словарь `name_to_factory`, где ключом является имя фабрики, а значением - сама фабрика.

```
A: Проверка уникальности имени фабрики
|
B: Установка идентификатора симуляции для фабрики
|
C: Добавление фабрики в список фабрик и в словарь name_to_factory
```

**Примеры**:

```python
from tinytroupe.factory.tiny_factory import TinyFactory

# Создание фабрики
factory = TinyFactory(name="Factory")

# Добавление фабрики в симуляцию
simulation = Simulation()
simulation.add_factory(factory)
```

#### `Simulation._execution_trace_position`

```python
def _execution_trace_position(self) -> int:
```

**Назначение**: Возвращает текущую позицию в трассе выполнения, или -1, если трасса пуста.

**Как работает функция**:

1.  Вычисляет индекс последнего элемента в списке `execution_trace`.
2.  Если список пуст, возвращает -1.

```
A: Вычисление индекса последнего элемента в execution_trace
|
B: Если execution_trace пуст, возвращает -1
```

**Примеры**:

```python
# Получение текущей позиции в трассе выполнения
simulation = Simulation()
position = simulation._execution_trace_position()
```

#### `Simulation._function_call_hash`

```python
def _function_call_hash(self, function_name, *args, **kwargs) -> int:
```

**Назначение**: Вычисляет хеш вызова функции.

**Параметры**:

*   `function_name` (str): Имя функции.
*   `*args`: Позиционные аргументы функции.
*   `**kwargs`: Именованные аргументы функции.

**Как работает функция**:

1.  Преобразует имя функции, позиционные аргументы и именованные аргументы в строку.
2.  Возвращает хеш этой строки.

```
A: Преобразование имени функции, аргументов в строку
|
B: Вычисление хеша строки
```

**Примеры**:

```python
# Вычисление хеша вызова функции
simulation = Simulation()
hash_value = simulation._function_call_hash("my_function", 1, 2, a=3, b=4)
```

#### `Simulation._skip_execution_with_cache`

```python
def _skip_execution_with_cache(self):
```

**Назначение**: Пропускает выполнение, используя кэшированное состояние.

**Как работает функция**:

1.  Проверяет, существует ли кэшированное состояние в текущей позиции трассы выполнения. Если нет, вызывается исключение `AssertionError`.
2.  Добавляет кэшированное состояние в трассу выполнения.

```
A: Проверка наличия кэшированного состояния
|
B: Добавление кэшированного состояния в трассу выполнения
```

**Примеры**:

```python
# Пропуск выполнения с использованием кэша
simulation = Simulation()
simulation.cached_trace = [("prev_hash", "event_hash", "event_output", {"state": "cached_state"})]
simulation.execution_trace = []
simulation._skip_execution_with_cache()
```

#### `Simulation._is_transaction_event_cached`

```python
def _is_transaction_event_cached(self, event_hash) -> bool:
```

**Назначение**: Проверяет, кэшировано ли событие транзакции.

**Параметры**:

*   `event_hash` (int): Хеш события.

**Как работает функция**:

1.  Проверяет, существует ли кэшированное состояние в текущей позиции трассы выполнения.
2.  Если существует, сравнивает хеш события с хешем события в кэшированном состоянии.
3.  Возвращает `True`, если хеши совпадают, и `False` в противном случае.

```
A: Проверка наличия кэшированного состояния
|
B: Сравнение хеша события с хешем события в кэшированном состоянии
|
C: Возврат True, если хеши совпадают, и False в противном случае
```

**Примеры**:

```python
# Проверка, кэшировано ли событие транзакции
simulation = Simulation()
simulation.cached_trace = [("prev_hash", "cached_event_hash", "event_output", {"state": "cached_state"})]
simulation.execution_trace = []
event_hash = "cached_event_hash"
is_cached = simulation._is_transaction_event_cached(event_hash)
```

#### `Simulation._drop_cached_trace_suffix`

```python
def _drop_cached_trace_suffix(self):
```

**Назначение**: Удаляет суффикс кэшированной трассы.

**Как работает функция**:

1.  Обрезает список `cached_trace` до текущей позиции трассы выполнения.

```
A: Обрезка списка cached_trace
```

**Примеры**:

```python
# Удаление суффикса кэшированной трассы
simulation = Simulation()
simulation.cached_trace = [1, 2, 3, 4, 5]
simulation.execution_trace = [1, 2]
simulation._drop_cached_trace_suffix()
# simulation.cached_trace теперь [1, 2]
```

#### `Simulation._add_to_execution_trace`

```python
def _add_to_execution_trace(self, state: dict, event_hash: int, event_output):
```

**Назначение**: Добавляет состояние в трассу выполнения.

**Параметры**:

*   `state` (dict): Состояние симуляции.
*   `event_hash` (int): Хеш события.
*   `event_output` : Вывод события

**Как работает функция**:

1.  Вычисляет хеш предыдущего состояния в трассе выполнения.
2.  Добавляет кортеж `(previous_hash, event_hash, event_output, state)` в список `execution_trace`.

```
A: Вычисление хеша предыдущего состояния
|
B: Добавление кортежа в execution_trace
```

**Примеры**:

```python
# Добавление состояния в трассу выполнения
simulation = Simulation()
state = {"agent1": {"x": 1, "y": 2}}
event_hash = hash("move_agent")
simulation._add_to_execution_trace(state, event_hash, None)
```

#### `Simulation._add_to_cache_trace`

```python
def _add_to_cache_trace(self, state: dict, event_hash: int, event_output):
```

**Назначение**: Добавляет состояние в кэшированную трассу.

**Параметры**:

*   `state` (dict): Состояние симуляции.
*   `event_hash` (int): Хеш события.
*   `event_output` : Вывод события

**Как работает функция**:

1.  Вычисляет хеш предыдущего состояния в кэшированной трассе.
2.  Добавляет кортеж `(previous_hash, event_hash, event_output, state)` в список `cached_trace`.
3.  Устанавливает флаг `has_unsaved_cache_changes` в `True`.

```
A: Вычисление хеша предыдущего состояния
|
B: Добавление кортежа в cached_trace
|
C: Установка флага has_unsaved_cache_changes в True
```

**Примеры**:

```python
# Добавление состояния в кэшированную трассу
simulation = Simulation()
state = {"agent1": {"x": 1, "y": 2}}
event_hash = hash("move_agent")
simulation._add_to_cache_trace(state, event_hash, None)
```

#### `Simulation._load_cache_file`

```python
def _load_cache_file(self, cache_path: str):
```

**Назначение**: Загружает кэш из файла.

**Параметры**:

*   `cache_path` (str): Путь к файлу кэша.

**Как работает функция**:

1.  Пытается загрузить содержимое файла кэша в список `cached_trace`.
2.  Если файл не найден, устанавливает `cached_trace` в пустой список.

```
A: Попытка загрузки кэша из файла
|
B: Если файл не найден, установка cached_trace в пустой список
```

**Примеры**:

```python
# Загрузка кэша из файла
simulation = Simulation()
simulation._load_cache_file("./my_simulation.cache.json")
```

#### `Simulation._save_cache_file`

```python
def _save_cache_file(self, cache_path: str):
```

**Назначение**: Сохраняет кэш в файл.

**Параметры**:

*   `cache_path` (str): Путь к файлу кэша.

**Как работает функция**:

1.  Сохраняет содержимое списка `cached_trace` в файл кэша.
2.  Устанавливает флаг `has_unsaved_cache_changes` в `False`.

```
A: Сохранение кэша в файл
|
B: Установка флага has_unsaved_cache_changes в False
```

**Примеры**:

```python
# Сохранение кэша в файл
simulation = Simulation()
simulation.cached_trace = [{"state": "state1"}]
simulation._save_cache_file("./my_simulation.cache.json")
```

#### `Simulation.begin_transaction`

```python
def begin_transaction(self):
```

**Назначение**: Начинает транзакцию.

**Как работает функция**:

1.  Устанавливает флаг `_under_transaction` в `True`.
2.  Очищает буферы обмена данными агентов и сред.

```
A: Установка флага _under_transaction в True
|
B: Очистка буферов обмена данными
```

**Примеры**:

```python
# Начало транзакции
simulation = Simulation()
simulation.begin_transaction()
```

#### `Simulation.end_transaction`

```python
def end_transaction(self):
```

**Назначение**: Завершает транзакцию.

**Как работает функция**:

1.  Устанавливает флаг `_under_transaction` в `False`.

```
A: Установка флага _under_transaction в False
```

**Примеры**:

```python
# Завершение транзакции
simulation = Simulation()
simulation.begin_transaction()
# ... выполнение транзакции ...
simulation.end_transaction()
```

#### `Simulation.is_under_transaction`

```python
def is_under_transaction(self):
```

**Назначение**: Проверяет, находится ли симуляция в состоянии транзакции.

**Как работает функция**:

1.  Возвращает значение флага `_under_transaction`.

```
A: Возврат значения флага _under_transaction
```

**Примеры**:

```python
# Проверка, находится ли симуляция в транзакции
simulation = Simulation()
is_under_transaction = simulation.is_under_transaction()
```

#### `Simulation._clear_communications_buffers`

```python
def _clear_communications_buffers(self):
```

**Назначение**: Очищает буферы обмена данными агентов и сред.

**Как работает функция**:

1.  Перебирает всех агентов и вызывает метод `clear_communications_buffer` для каждого агента.
2.  Перебирает все среды и вызывает метод `clear_communications_buffer` для каждой среды.

```
A: Перебор агентов и очистка их буферов
|
B: Перебор сред и очистка их буферов
```

**Примеры**:

```python
# Очистка буферов обмена данными
simulation = Simulation()
# ... добавление агентов и сред ...
simulation._clear_communications_buffers()
```

#### `Simulation._encode_simulation_state`

```python
def _encode_simulation_state(self) -> dict:
```

**Назначение**: Кодирует текущее состояние симуляции, включая агентов, среды и фабрики.

**Как работает функция**:

1.  Создает пустой словарь `state`.
2.  Кодирует состояние каждого агента, среды и фабрики и добавляет их в словарь `state`.
3.  Возвращает словарь `state`.

```
A: Создание пустого словаря state
|
B: Кодирование состояния агентов и добавление в state
|
C: Кодирование состояния сред и добавление в state
|
D: Кодирование состояния фабрик и добавление в state
|
E: Возврат словаря state
```

**Примеры**:

```python
# Кодирование состояния симуляции
simulation = Simulation()
# ... добавление агентов, сред и фабрик ...
state = simulation._encode_simulation_state()
```

#### `Simulation._decode_simulation_state`

```python
def _decode_simulation_state(self, state: dict):
```

**Назначение**: Декодирует состояние симуляции, включая агентов, среды и фабрики.

**Параметры**:

*   `state` (dict): Состояние для декодирования.

**Как работает функция**:

1.  Декодирует состояние каждой фабрики, среды и агента, используя предоставленный словарь `state`.
2.  Если среда или агент не найдены в симуляции, выбрасывается исключение `ValueError`.

```
A: Декодирование состояния фабрик
|
B: Декодирование состояния сред
|
C: Декодирование состояния агентов
```

**Примеры**:

```python
# Декодирование состояния симуляции
simulation = Simulation()
# ... добавление агентов, сред и фабрик ...
encoded_state = simulation._encode_simulation_state()
simulation._decode_simulation_state(encoded_state)
```

### `Transaction`

**Описание**: Класс `Transaction` представляет транзакцию в симуляции. Он используется для выполнения функций с кэшированием и управлением состоянием симуляции.

**Принцип работы**: Класс `Transaction` принимает объект, над которым выполняется транзакция, симуляцию, функцию и аргументы для этой функции. При выполнении транзакции проверяется, можно ли использовать кэшированное состояние. Если кэш доступен, состояние восстанавливается из кэша. Если кэш недоступен, функция выполняется, а ее результат и состояние симуляции кэшируются.

**Аттрибуты**:

*   `obj_under_transaction`: Объект, над которым выполняется транзакция.
*   `simulation`: Симуляция, в которой выполняется транзакция.
*   `function_name`: Имя функции, выполняемой в транзакции.
*   `function`: Функция, выполняемая в транзакции.
*   `args`: Позиционные аргументы функции.
*   `kwargs`: Именованные аргументы функции.

**Методы**:

*   `__init__(self, obj_under_transaction, simulation, function, *args, **kwargs)`: Инициализирует новый экземпляр класса `Transaction`.
*   `execute(self)`: Выполняет транзакцию.
*   `_encode_function_output(self, output) -> dict`: Кодирует вывод функции.
*   `_decode_function_output(self, encoded_output: dict)`: Декодирует закодированный вывод функции.

#### `Transaction.__init__`

```python
def __init__(self, obj_under_transaction, simulation, function, *args, **kwargs):
```

**Назначение**: Инициализирует новый экземпляр класса `Transaction`.

**Параметры**:

*   `obj_under_transaction`: Объект, над которым выполняется транзакция.
*   `simulation`: Симуляция, в которой выполняется транзакция.
*   `function`: Функция, выполняемая в транзакции.
*   `*args`: Позиционные аргументы функции.
*   `**kwargs`: Именованные аргументы функции.

**Как работает функция**:

1.  Инициализирует атрибуты класса, такие как `obj_under_transaction`, `simulation`, `function_name`, `function`, `args` и `kwargs`.
2.  Если объект является экземпляром `TinyPerson`, `TinyWorld` или `TinyFactory`, добавляет его в симуляцию.

```
A: Инициализация атрибутов класса
|
B: Проверка типа объекта и добавление в симуляцию (если необходимо)
```

**Примеры**:

```python
from tinytroupe.agent import TinyPerson

# Создание агента и симуляции
agent = TinyPerson(name="Alice")
simulation = Simulation()

# Создание транзакции для перемещения агента
def move_agent(agent, x, y):
    agent.x = x
    agent.y = y
transaction = Transaction(agent, simulation, move_agent, 10, 20)
```

#### `Transaction.execute`

```python
def execute(self):
```

**Назначение**: Выполняет транзакцию.

**Как работает функция**:

1.  Проверяет, запущена ли симуляция. Если нет, функция выполняется без кэширования.
2.  Если симуляция запущена, проверяет, можно ли использовать кэшированное состояние.
3.  Если кэш доступен, состояние восстанавливается из кэша и возвращается кэшированный результат.
4.  Если кэш недоступен, функция выполняется, ее результат и состояние симуляции кэшируются.

```
A: Проверка статуса симуляции
|
B: Если симуляция запущена: проверка возможности использования кэша
|
C: Если кэш доступен: восстановление состояния из кэша и возврат кэшированного результата
|
D: Если кэш недоступен: выполнение функции, кэширование результата и состояния
```

**Примеры**:

```python
from tinytroupe.agent import TinyPerson

# Создание агента и симуляции
agent = TinyPerson(name="Alice")
simulation = Simulation()
simulation.begin()

# Создание и выполнение транзакции для перемещения агента
def move_agent(agent, x, y):
    agent.x = x
    agent.y = y
transaction = Transaction(agent, simulation, move_agent, 10, 20)
result = transaction.execute()
```

#### `Transaction._encode_function_output`

```python
def _encode_function_output(self, output) -> dict:
```

**Назначение**: Кодирует вывод функции.

**Как работает функция**:

1.  Если вывод является экземпляром `TinyPerson`, `TinyWorld` или `TinyFactory`, кодирует его как ссылку на объект.
2.  Если вывод является одним из типов, поддерживаемых JSON (int, float, str, bool, list, dict, tuple), кодирует его как есть.
3.  В противном случае выбрасывает исключение `ValueError`.

```
A: Проверка типа вывода и кодирование в соответствии с типом
```

**Примеры**:

```python
from tinytroupe.agent import TinyPerson

# Создание агента
agent = TinyPerson(name="Alice")

# Кодирование вывода функции
transaction = Transaction(None, None, None, None)
encoded_output = transaction._encode_function_output(agent)
```

#### `Transaction._decode_function_output`

```python
def _decode_function_output(self, encoded_output: dict):
```

**Назначение**: Декодирует закодированный вывод функции.

**Как работает функция**:

1.  Если закодированный вывод является ссылкой на `TinyPerson`, `TinyWorld` или `TinyFactory`, восстанавливает объект по имени.
2.  Если закодированный вывод является JSON, возвращает его значение.
3.  В противном случае выбрасывает исключение `ValueError`.

```
A: Проверка типа закодированного вывода и декодирование в соответствии с типом
```

**Примеры**:

```python
from tinytroupe.agent import TinyPerson

# Создание агента и кодирование вывода
agent = TinyPerson(name="Alice")
transaction = Transaction(None, None, None, None)
encoded_output = transaction._encode_function_output(agent)

# Декодирование вывода
decoded_output = transaction._decode_function_output(encoded_output)
```

### `SkipTransaction`

**Описание**: Класс исключения, используемый для обозначения пропуска транзакции.

### `CacheOutOfSync`

**Описание**: Класс исключения, используемый для обозначения рассинхронизации кэша.

### `ExecutionCached`

**Описание**: Класс исключения, используемый для обозначения, что выполнение уже кэшировано.

## Функции

###
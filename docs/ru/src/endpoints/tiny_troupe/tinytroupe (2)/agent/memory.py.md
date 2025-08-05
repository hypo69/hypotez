# Модуль `memory.py`

## Обзор

Модуль `memory.py` предоставляет классы для реализации различных типов памяти агента в системе `tinytroupe`. Он включает базовый класс `TinyMemory` и его подклассы `EpisodicMemory` и `SemanticMemory`, каждый из которых предназначен для хранения и извлечения информации определенного типа. Модуль также содержит вспомогательные функции для работы с памятью.

## Подробней

Этот модуль реализует различные типы памяти, которые может использовать агент.
`TinyMemory` - это базовый класс для всех типов памяти.
`EpisodicMemory` позволяет агенту запоминать конкретные события или эпизоды из прошлого.
`SemanticMemory` позволяет агенту хранить и извлекать семантическую информацию, такую как значения, понимания и знания, основанные на концепциях, не связанные с конкретными событиями или эпизодами.

## Классы

### `TinyMemory`

**Описание**: Базовый класс для различных типов памяти.

**Методы**:

- `_preprocess_value_for_storage(value: Any) -> Any`
- `_store(value: Any) -> None`
- `store(value: dict) -> None`
- `store_all(values: list) -> None`
- `retrieve(first_n: int, last_n: int, include_omission_info: bool = True) -> list`
- `retrieve_recent() -> list`
- `retrieve_all() -> list`
- `retrieve_relevant(relevance_target: str, top_k: int = 20) -> list`

### `EpisodicMemory`

**Описание**: Предоставляет агенту возможности эпизодической памяти. Когнитивно, эпизодическая память - это способность помнить конкретные события или эпизоды в прошлом. Этот класс предоставляет простую реализацию эпизодической памяти, где агент может хранить и извлекать сообщения из памяти.

**Наследует**: `TinyMemory`

**Атрибуты**:

- `MEMORY_BLOCK_OMISSION_INFO (dict)`: Информационное сообщение, которое добавляется при извлечении не всех данных из памяти.
- `fixed_prefix_length (int)`: Длина фиксированного префикса.
- `lookback_length (int)`: Длина отрезка для просмотра последних значений.
- `memory (list)`: Список для хранения эпизодов памяти.

**Методы**:

- `__init__(fixed_prefix_length: int = 100, lookback_length: int = 100) -> None`
- `_store(value: Any) -> None`
- `count() -> int`
- `retrieve(first_n: int, last_n: int, include_omission_info: bool = True) -> list`
- `retrieve_recent(include_omission_info: bool = True) -> list`
- `retrieve_all() -> list`
- `retrieve_relevant(relevance_target: str, top_k: int) -> list`
- `retrieve_first(n: int, include_omission_info: bool = True) -> list`
- `retrieve_last(n: int, include_omission_info: bool = True) -> list`

### `SemanticMemory`

**Описание**: В когнитивной психологии семантическая память - это память о значениях, пониманиях и других знаниях, основанных на концепциях, не связанных с конкретными переживаниями. Она не упорядочена во времени и не связана с запоминанием конкретных событий или эпизодов. Этот класс предоставляет простую реализацию семантической памяти, где агент может хранить и извлекать семантическую информацию.

**Наследует**: `TinyMemory`

**Атрибуты**:

- `serializable_attrs (list)`: Список атрибутов, которые могут быть сериализованы.
- `memories (list)`: Список для хранения семантической памяти.
- `semantic_grounding_connector (BaseSemanticGroundingConnector)`: Объект для связи с семантическим обоснованием.

**Методы**:

- `__init__(memories: list = None) -> None`
- `_post_init()`
- `_preprocess_value_for_storage(value: dict) -> Any`
- `_store(value: Any) -> None`
- `retrieve_relevant(relevance_target: str, top_k: int = 20) -> list`
- `_build_document_from(memory) -> Document`
- `_build_documents_from(memories: list) -> list`

## Методы класса `TinyMemory`

### `_preprocess_value_for_storage`

```python
def _preprocess_value_for_storage(self, value: Any) -> Any:
    """
    Preprocesses a value before storing it in memory.
    """
    # by default, we don\'t preprocess the value
    return value
```

**Назначение**: Обрабатывает значение перед сохранением в памяти.

**Параметры**:

- `value` (Any): Значение для обработки.

**Возвращает**:

- `Any`: Обработанное значение.

**Как работает функция**:

Функция по умолчанию не выполняет никаких преобразований и возвращает исходное значение.

### `_store`

```python
def _store(self, value: Any) -> None:
    """
    Stores a value in memory.
    """
    raise NotImplementedError("Subclasses must implement this method.")
```

**Назначение**: Сохраняет значение в памяти.

**Параметры**:

- `value` (Any): Значение для сохранения.

**Вызывает исключения**:

- `NotImplementedError`: Если метод не реализован в подклассе.

**Как работает функция**:

Вызывает исключение `NotImplementedError`, так как метод должен быть реализован в подклассах.

### `store`

```python
def store(self, value: dict) -> None:
    """
    Stores a value in memory.
    """
    self._store(self._preprocess_value_for_storage(value))
```

**Назначение**: Сохраняет значение в памяти, предварительно обработав его.

**Параметры**:

- `value` (dict): Значение для сохранения.

**Как работает функция**:

Функция вызывает метод `_preprocess_value_for_storage` для предварительной обработки значения, а затем вызывает метод `_store` для сохранения обработанного значения в памяти.

### `store_all`

```python
def store_all(self, values: list) -> None:
    """
    Stores a list of values in memory.
    """
    for value in values:
        self.store(value)
```

**Назначение**: Сохраняет список значений в памяти.

**Параметры**:

- `values` (list): Список значений для сохранения.

**Как работает функция**:

Функция перебирает все значения в списке и вызывает метод `store` для сохранения каждого значения в памяти.

### `retrieve`

```python
def retrieve(self, first_n: int, last_n: int, include_omission_info: bool = True) -> list:
    """
    Retrieves the first n and/or last n values from memory. If n is None, all values are retrieved.

    Args:
        first_n (int): The number of first values to retrieve.
        last_n (int): The number of last values to retrieve.
        include_omission_info (bool): Whether to include an information message when some values are omitted.

    Returns:
        list: The retrieved values.
    """
    raise NotImplementedError("Subclasses must implement this method.")
```

**Назначение**: Извлекает первые `n` и/или последние `n` значений из памяти. Если `n` равно `None`, извлекаются все значения.

**Параметры**:

- `first_n` (int): Количество первых значений для извлечения.
- `last_n` (int): Количество последних значений для извлечения.
- `include_omission_info` (bool): Определяет, включать ли информационное сообщение, когда некоторые значения опущены. По умолчанию `True`.

**Возвращает**:

- `list`: Извлеченные значения.

**Вызывает исключения**:

- `NotImplementedError`: Если метод не реализован в подклассе.

**Как работает функция**:

Вызывает исключение `NotImplementedError`, так как метод должен быть реализован в подклассах.

### `retrieve_recent`

```python
def retrieve_recent(self) -> list:
    """
    Retrieves the n most recent values from memory.
    """
    raise NotImplementedError("Subclasses must implement this method.")
```

**Назначение**: Извлекает `n` самых последних значений из памяти.

**Вызывает исключения**:

- `NotImplementedError`: Если метод не реализован в подклассе.

**Как работает функция**:

Вызывает исключение `NotImplementedError`, так как метод должен быть реализован в подклассах.

### `retrieve_all`

```python
def retrieve_all(self) -> list:
    """
    Retrieves all values from memory.
    """
    raise NotImplementedError("Subclasses must implement this method.")
```

**Назначение**: Извлекает все значения из памяти.

**Вызывает исключения**:

- `NotImplementedError`: Если метод не реализован в подклассе.

**Как работает функция**:

Вызывает исключение `NotImplementedError`, так как метод должен быть реализован в подклассах.

### `retrieve_relevant`

```python
def retrieve_relevant(self, relevance_target: str, top_k: int = 20) -> list:
    """
    Retrieves all values from memory that are relevant to a given target.
    """
    raise NotImplementedError("Subclasses must implement this method.")
```

**Назначение**: Извлекает все значения из памяти, которые релевантны данной цели.

**Параметры**:

- `relevance_target` (str): Цель релевантности.
- `top_k` (int): Количество извлекаемых значений. По умолчанию 20.

**Вызывает исключения**:

- `NotImplementedError`: Если метод не реализован в подклассе.

**Как работает функция**:

Вызывает исключение `NotImplementedError`, так как метод должен быть реализован в подклассах.

## Методы класса `EpisodicMemory`

### `__init__`

```python
def __init__(self, fixed_prefix_length: int = 100, lookback_length: int = 100) -> None:
    """
    Initializes the memory.

    Args:
        fixed_prefix_length (int): The fixed prefix length. Defaults to 20.
        lookback_length (int): The lookback length. Defaults to 20.
    """
    self.fixed_prefix_length = fixed_prefix_length
    self.lookback_length = lookback_length

    self.memory = []
```

**Назначение**: Инициализирует память.

**Параметры**:

- `fixed_prefix_length` (int): Длина фиксированного префикса. По умолчанию 100.
- `lookback_length` (int): Длина отрезка для просмотра последних значений. По умолчанию 100.

**Как работает функция**:

Функция инициализирует атрибуты `fixed_prefix_length` и `lookback_length` заданными значениями, а также создает пустой список `memory` для хранения эпизодов памяти.

### `_store`

```python
def _store(self, value: Any) -> None:
    """
    Stores a value in memory.
    """
    self.memory.append(value)
```

**Назначение**: Сохраняет значение в памяти.

**Параметры**:

- `value` (Any): Значение для сохранения.

**Как работает функция**:

Функция добавляет значение в список `memory`.

### `count`

```python
def count(self) -> int:
    """
    Returns the number of values in memory.
    """
    return len(self.memory)
```

**Назначение**: Возвращает количество значений в памяти.

**Возвращает**:

- `int`: Количество значений в списке `memory`.

**Как работает функция**:

Функция возвращает длину списка `memory`.

### `retrieve`

```python
def retrieve(self, first_n: int, last_n: int, include_omission_info: bool = True) -> list:
    """
    Retrieves the first n and/or last n values from memory. If n is None, all values are retrieved.

    Args:
        first_n (int): The number of first values to retrieve.
        last_n (int): The number of last values to retrieve.
        include_omission_info (bool): Whether to include an information message when some values are omitted.

    Returns:
        list: The retrieved values.
    """

    omisssion_info = [EpisodicMemory.MEMORY_BLOCK_OMISSION_INFO] if include_omission_info else []

    # use the other methods in the class to implement
    if first_n is not None and last_n is not None:
        return self.retrieve_first(first_n) + omisssion_info + self.retrieve_last(last_n)
    elif first_n is not None:
        return self.retrieve_first(first_n)
    elif last_n is not None:
        return self.retrieve_last(last_n)
    else:
        return self.retrieve_all()
```

**Назначение**: Извлекает первые `n` и/или последние `n` значений из памяти. Если `n` равно `None`, извлекаются все значения.

**Параметры**:

- `first_n` (int): Количество первых значений для извлечения.
- `last_n` (int): Количество последних значений для извлечения.
- `include_omission_info` (bool): Определяет, включать ли информационное сообщение, когда некоторые значения опущены. По умолчанию `True`.

**Возвращает**:

- `list`: Извлеченные значения.

**Как работает функция**:

Функция использует другие методы класса (`retrieve_first`, `retrieve_last`, `retrieve_all`) для извлечения значений из памяти в зависимости от переданных параметров.  Дополнительно, в зависимости от значения флага `include_omission_info`, добавляет информационное сообщение `omisssion_info` об опущенных значениях.

### `retrieve_recent`

```python
def retrieve_recent(self, include_omission_info: bool = True) -> list:
    """
    Retrieves the n most recent values from memory.
    """
    omisssion_info = [EpisodicMemory.MEMORY_BLOCK_OMISSION_INFO] if include_omission_info else []

    # compute fixed prefix
    fixed_prefix = self.memory[: self.fixed_prefix_length] + omisssion_info

    # how many lookback values remain?
    remaining_lookback = min(
        len(self.memory) - len(fixed_prefix), self.lookback_length
    )

    # compute the remaining lookback values and return the concatenation
    if remaining_lookback <= 0:
        return fixed_prefix
    else:
        return fixed_prefix + self.memory[-remaining_lookback:]
```

**Назначение**: Извлекает `n` самых последних значений из памяти.

**Параметры**:

- `include_omission_info` (bool): Определяет, включать ли информационное сообщение, когда некоторые значения опущены. По умолчанию `True`.

**Возвращает**:

- `list`: Извлеченные значения.

**Как работает функция**:

1.  Определяет, нужно ли включать информацию об опущении.
2.  Вычисляет фиксированный префикс, добавляя к нему информацию об опущении, если это необходимо.
3.  Вычисляет количество значений для просмотра, которые остаются.
4.  Если `remaining_lookback` меньше или равно 0, возвращает фиксированный префикс.
5.  В противном случае возвращает объединение фиксированного префикса и последних значений из памяти.

### `retrieve_all`

```python
def retrieve_all(self) -> list:
    """
    Retrieves all values from memory.
    """
    return copy.copy(self.memory)
```

**Назначение**: Извлекает все значения из памяти.

**Возвращает**:

- `list`: Копия списка `memory`.

**Как работает функция**:

Функция возвращает копию списка `memory`, чтобы избежать изменения исходного списка.

### `retrieve_relevant`

```python
def retrieve_relevant(self, relevance_target: str, top_k: int) -> list:
    """
    Retrieves top-k values from memory that are most relevant to a given target.
    """
    raise NotImplementedError("Subclasses must implement this method.")
```

**Назначение**: Извлекает `top_k` значений из памяти, которые наиболее релевантны данной цели.

**Параметры**:

- `relevance_target` (str): Цель релевантности.
- `top_k` (int): Количество извлекаемых значений.

**Вызывает исключения**:

- `NotImplementedError`: Если метод не реализован в подклассе.

**Как работает функция**:

Вызывает исключение `NotImplementedError`, так как метод должен быть реализован в подклассах.

### `retrieve_first`

```python
def retrieve_first(self, n: int, include_omission_info: bool = True) -> list:
    """
    Retrieves the first n values from memory.
    """
    omisssion_info = [EpisodicMemory.MEMORY_BLOCK_OMISSION_INFO] if include_omission_info else []

    return self.memory[:n] + omisssion_info
```

**Назначение**: Извлекает первые `n` значений из памяти.

**Параметры**:

- `n` (int): Количество извлекаемых значений.
- `include_omission_info` (bool): Определяет, включать ли информационное сообщение, когда некоторые значения опущены. По умолчанию `True`.

**Возвращает**:

- `list`: Список, содержащий первые `n` значений из памяти, с добавленной информацией об опущенных значениях при необходимости.

**Как работает функция**:

Функция возвращает срез списка `memory` от начала до `n`, с добавлением `omisssion_info`, если `include_omission_info` имеет значение `True`.

### `retrieve_last`

```python
def retrieve_last(self, n: int, include_omission_info: bool = True) -> list:
    """
    Retrieves the last n values from memory.
    """
    omisssion_info = [EpisodicMemory.MEMORY_BLOCK_OMISSION_INFO] if include_omission_info else []

    return omisssion_info + self.memory[-n:]
```

**Назначение**: Извлекает последние `n` значений из памяти.

**Параметры**:

- `n` (int): Количество извлекаемых значений.
- `include_omission_info` (bool): Определяет, включать ли информационное сообщение, когда некоторые значения опущены. По умолчанию `True`.

**Возвращает**:

- `list`: Список, содержащий последние `n` значений из памяти, с добавленной информацией об опущенных значениях при необходимости.

**Как работает функция**:

Функция возвращает срез списка `memory` от `-n` до конца, с добавлением `omisssion_info`, если `include_omission_info` имеет значение `True`.

## Методы класса `SemanticMemory`

### `__init__`

```python
def __init__(self, memories: list = None) -> None:
    self.memories = memories

    # @post_init ensures that _post_init is called after the __init__ method
```

**Назначение**: Инициализирует экземпляр класса `SemanticMemory`.

**Параметры**:

- `memories` (list, optional): Список для начальной инициализации семантической памяти. По умолчанию `None`.

**Как работает функция**:

Функция инициализирует атрибут `memories` переданным списком или `None`, если список не передан.
Декоратор `@post_init` гарантирует, что метод `_post_init` будет вызван после завершения `__init__`.

### `_post_init`

```python
def _post_init(self):
    """
    This will run after __init__, since the class has the @post_init decorator.
    It is convenient to separate some of the initialization processes to make deserialize easier.
    """

    if not hasattr(self, 'memories') or self.memories is None:
        self.memories = []

    self.semantic_grounding_connector = BaseSemanticGroundingConnector("Semantic Memory Storage")
    self.semantic_grounding_connector.add_documents(self._build_documents_from(self.memories))
```

**Назначение**: Выполняет постобработку после инициализации, когда экземпляр класса уже создан.

**Как работает функция**:

1.  Проверяет, существует ли атрибут `memories` и не равен ли он `None`. Если это так, инициализирует `self.memories` пустым списком.
2.  Создает экземпляр `BaseSemanticGroundingConnector` с именем "Semantic Memory Storage".
3.  Вызывает метод `_build_documents_from` для преобразования содержимого `self.memories` в список документов, а затем добавляет эти документы в `semantic_grounding_connector`.

### `_preprocess_value_for_storage`

```python
def _preprocess_value_for_storage(self, value: dict) -> Any:
    engram = None

    if value['type'] == 'action':
        engram = f"# Fact\n" + \
                 f"I have performed the following action at date and time {value['simulation_timestamp']}:\n\n" + \
                 f" {value['content']}"

    elif value['type'] == 'stimulus':
        engram = f"# Stimulus\n" + \
                 f"I have received the following stimulus at date and time {value['simulation_timestamp']}:\n\n" + \
                 f" {value['content']}"

    # else: # Anything else here?

    return engram
```

**Назначение**: Преобразует значение перед сохранением в семантической памяти.

**Параметры**:

- `value` (dict): Словарь, содержащий информацию для сохранения.

**Возвращает**:

- `Any`: Преобразованное значение для хранения.

**Как работает функция**:

1.  Проверяет тип значения (`value['type']`).
2.  Если тип `action`, создает строку, описывающую выполненное действие с указанием даты и времени.
3.  Если тип `stimulus`, создает строку, описывающую полученный стимул с указанием даты и времени.
4.  Возвращает полученную строку `engram`.

### `_store`

```python
def _store(self, value: Any) -> None:
    engram_doc = self._build_document_from(self._preprocess_value_for_storage(value))
    self.semantic_grounding_connector.add_document(engram_doc)
```

**Назначение**: Сохраняет значение в семантической памяти.

**Параметры**:

- `value` (Any): Значение для сохранения.

**Как работает функция**:

1.  Вызывает `_preprocess_value_for_storage` для предварительной обработки значения.
2.  Вызывает `_build_document_from` для создания документа из обработанного значения.
3.  Добавляет созданный документ в `semantic_grounding_connector`.

### `retrieve_relevant`

```python
def retrieve_relevant(self, relevance_target: str, top_k: int = 20) -> list:
    """
    Retrieves all values from memory that are relevant to a given target.
    """
    return self.semantic_grounding_connector.retrieve_relevant(relevance_target, top_k)
```

**Назначение**: Извлекает из памяти все значения, релевантные заданной цели.

**Параметры**:

- `relevance_target` (str): Цель для определения релевантности.
- `top_k` (int, optional): Максимальное количество извлекаемых значений. По умолчанию 20.

**Возвращает**:

- `list`: Список релевантных значений.

**Как работает функция**:

Функция вызывает метод `retrieve_relevant` объекта `semantic_grounding_connector` с переданными параметрами и возвращает полученный результат.

### `_build_document_from`

```python
def _build_document_from(memory) -> Document:
    # TODO: add any metadata as well?
    return Document(text=str(memory))
```

**Назначение**: Создает документ из элемента памяти.

**Параметры**:

- `memory`: Элемент памяти для преобразования в документ.

**Возвращает**:

- `Document`: Объект `Document`, представляющий элемент памяти.

**Как работает функция**:

Функция создает объект `Document` из переданного элемента памяти, преобразуя его в строку.  TODO: добавить метаданные.

### `_build_documents_from`

```python
def _build_documents_from(self, memories: list) -> list:
    return [self._build_document_from(memory) for memory in memories]
```

**Назначение**: Создает список документов из списка элементов памяти.

**Параметры**:

- `memories` (list): Список элементов памяти.

**Возвращает**:

- `list`: Список объектов `Document`.

**Как работает функция**:

Функция использует генератор списков для преобразования каждого элемента в списке `memories` в объект `Document` с помощью метода `_build_document_from` и возвращает список этих документов.
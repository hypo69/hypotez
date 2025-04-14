# Модуль `memory.py`

## Обзор

Модуль предоставляет классы для реализации различных типов памяти агента в системе `tinytroupe`. Он включает в себя абстрактный базовый класс `TinyMemory` и его подклассы `EpisodicMemory` и `SemanticMemory`, реализующие эпизодическую и семантическую память соответственно. Модуль обеспечивает механизмы хранения и извлечения информации, а также интеграцию с семантическим заземлением для обработки и хранения семантических данных.

## Подробней

Этот модуль является важной частью архитектуры агента, позволяя ему сохранять и использовать информацию о прошлых событиях и общих знаниях. `TinyMemory` служит основой для различных типов памяти, а `EpisodicMemory` и `SemanticMemory` предоставляют конкретные реализации для хранения и извлечения эпизодических и семантических данных.

## Классы

### `TinyMemory`

**Описание**: Абстрактный базовый класс для различных типов памяти.

**Принцип работы**: Определяет интерфейс для хранения и извлечения данных из памяти агента. Подклассы должны реализовывать методы `_store`, `retrieve`, `retrieve_recent` и `retrieve_all`.

**Методы**:

- `_preprocess_value_for_storage(self, value: Any) -> Any`:
    ```python
    def _preprocess_value_for_storage(self, value: Any) -> Any:
        """
        Предобрабатывает значение перед сохранением в памяти.

        Args:
            value (Any): Значение для предобработки.

        Returns:
            Any: Предобработанное значение.
        """
    ```

- `_store(self, value: Any) -> None`:
    ```python
    def _store(self, value: Any) -> None:
        """
        Сохраняет значение в памяти.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
    ```

- `store(self, value: dict) -> None`:
    ```python
    def store(self, value: dict) -> None:
        """
        Сохраняет значение в памяти, предварительно обработав его.

        Args:
            value (dict): Значение для сохранения.
        """
    ```

- `store_all(self, values: list) -> None`:
    ```python
    def store_all(self, values: list) -> None:
        """
        Сохраняет список значений в памяти.

        Args:
            values (list): Список значений для сохранения.
        """
    ```

- `retrieve(self, first_n: int, last_n: int, include_omission_info:bool=True) -> list`:
    ```python
    def retrieve(self, first_n: int, last_n: int, include_omission_info:bool=True) -> list:
        """
        Извлекает первые `n` и/или последние `n` значения из памяти. Если `n` равен `None`, извлекаются все значения.

        Args:
            first_n (int): Количество первых значений для извлечения.
            last_n (int): Количество последних значений для извлечения.
            include_omission_info (bool): Включать ли информационное сообщение, когда некоторые значения опущены.

        Returns:
            list: Извлеченные значения.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
    ```

- `retrieve_recent(self) -> list`:
    ```python
    def retrieve_recent(self) -> list:
        """
        Извлекает `n` самых последних значений из памяти.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
    ```

- `retrieve_all(self) -> list`:
    ```python
    def retrieve_all(self) -> list:
        """
        Извлекает все значения из памяти.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
    ```

- `retrieve_relevant(self, relevance_target:str, top_k=20) -> list`:
    ```python
    def retrieve_relevant(self, relevance_target:str, top_k=20) -> list:
        """
        Извлекает все значения из памяти, которые релевантны заданной цели.

        Args:
            relevance_target (str): Цель релевантности.
            top_k (int): Количество извлекаемых релевантных значений.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
    ```

### `EpisodicMemory`

**Описание**: Предоставляет возможности эпизодической памяти для агента. Эпизодическая память - это способность помнить конкретные события или эпизоды в прошлом.

**Наследует**: `TinyMemory`

**Атрибуты**:

- `MEMORY_BLOCK_OMISSION_INFO (dict)`: Информация о пропущенных блоках памяти.
- `fixed_prefix_length (int)`: Фиксированная длина префикса.
- `lookback_length (int)`: Длина ретроспективного обзора.
- `memory (list)`: Список для хранения эпизодических воспоминаний.

**Методы**:

- `__init__(self, fixed_prefix_length: int = 100, lookback_length: int = 100) -> None`:
    ```python
    def __init__(self, fixed_prefix_length: int = 100, lookback_length: int = 100) -> None:
        """
        Инициализирует память.

        Args:
            fixed_prefix_length (int): Фиксированная длина префикса. По умолчанию 100.
            lookback_length (int): Длина ретроспективного обзора. По умолчанию 100.
        """
    ```

- `_store(self, value: Any) -> None`:
    ```python
    def _store(self, value: Any) -> None:
        """
        Сохраняет значение в памяти.

        Args:
            value (Any): Значение для сохранения.
        """
    ```

- `count(self) -> int`:
    ```python
    def count(self) -> int:
        """
        Возвращает количество значений в памяти.

        Returns:
            int: Количество значений в памяти.
        """
    ```

- `retrieve(self, first_n: int, last_n: int, include_omission_info:bool=True) -> list`:
    ```python
    def retrieve(self, first_n: int, last_n: int, include_omission_info:bool=True) -> list:
        """
        Извлекает первые `n` и/или последние `n` значения из памяти. Если `n` равен `None`, извлекаются все значения.

        Args:
            first_n (int): Количество первых значений для извлечения.
            last_n (int): Количество последних значений для извлечения.
            include_omission_info (bool): Включать ли информационное сообщение, когда некоторые значения опущены.

        Returns:
            list: Извлеченные значения.
        """
    ```

- `retrieve_recent(self, include_omission_info:bool=True) -> list`:
    ```python
    def retrieve_recent(self, include_omission_info:bool=True) -> list:
        """
        Извлекает `n` самых последних значений из памяти.

        Args:
            include_omission_info (bool): Включать ли информационное сообщение, когда некоторые значения опущены.

        Returns:
            list: Список последних значений из памяти.
        """
    ```

- `retrieve_all(self) -> list`:
    ```python
    def retrieve_all(self) -> list:
        """
        Извлекает все значения из памяти.

        Returns:
            list: Список всех значений из памяти.
        """
    ```

- `retrieve_relevant(self, relevance_target: str, top_k:int) -> list`:
    ```python
    def retrieve_relevant(self, relevance_target: str, top_k:int) -> list:
        """
        Извлекает top-k значений из памяти, которые наиболее релевантны заданной цели.

        Args:
            relevance_target (str): Цель релевантности.
            top_k (int): Количество извлекаемых релевантных значений.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
    ```

- `retrieve_first(self, n: int, include_omission_info:bool=True) -> list`:
    ```python
    def retrieve_first(self, n: int, include_omission_info:bool=True) -> list:
        """
        Извлекает первые `n` значений из памяти.

        Args:
            n (int): Количество первых значений для извлечения.
            include_omission_info (bool): Включать ли информационное сообщение, когда некоторые значения опущены.

        Returns:
            list: Список первых значений из памяти.
        """
    ```

- `retrieve_last(self, n: int, include_omission_info:bool=True) -> list`:
    ```python
    def retrieve_last(self, n: int, include_omission_info:bool=True) -> list:
        """
        Извлекает последние `n` значений из памяти.

        Args:
            n (int): Количество последних значений для извлечения.
            include_omission_info (bool): Включать ли информационное сообщение, когда некоторые значения опущены.

        Returns:
            list: Список последних значений из памяти.
        """
    ```

### `SemanticMemory`

**Описание**: Предоставляет возможности семантической памяти для агента. Семантическая память - это память о значениях, пониманиях и других знаниях, основанных на понятиях, не связанных с конкретными переживаниями.

**Наследует**: `TinyMemory`

**Атрибуты**:

- `serializable_attrs (list)`: Список сериализуемых атрибутов.
- `memories (list)`: Список для хранения семантических воспоминаний.
- `semantic_grounding_connector (BaseSemanticGroundingConnector)`: Коннектор для семантического заземления.

**Методы**:

- `__init__(self, memories: list=None) -> None`:
    ```python
    def __init__(self, memories: list=None) -> None:
        """
        Инициализирует память.

        Args:
            memories (list): Список начальных семантических воспоминаний.
        """
    ```

- `_post_init(self)`:
    ```python
    def _post_init(self):
        """
        Выполняется после __init__. Инициализирует коннектор семантического заземления и добавляет документы.
        """
    ```

- `_preprocess_value_for_storage(self, value: dict) -> Any`:
    ```python
    def _preprocess_value_for_storage(self, value: dict) -> Any:
        """
        Предобрабатывает значение перед сохранением в памяти.

        Args:
            value (dict): Значение для предобработки.

        Returns:
            Any: Предобработанное значение (энграмма).
        """
    ```

- `_store(self, value: Any) -> None`:
    ```python
    def _store(self, value: Any) -> None:
        """
        Сохраняет значение в памяти.

        Args:
            value (Any): Значение для сохранения.
        """
    ```

- `retrieve_relevant(self, relevance_target:str, top_k=20) -> list`:
    ```python
    def retrieve_relevant(self, relevance_target:str, top_k=20) -> list:
        """
        Извлекает все значения из памяти, которые релевантны заданной цели.

        Args:
            relevance_target (str): Цель релевантности.
            top_k (int): Количество извлекаемых релевантных значений.

        Returns:
            list: Список релевантных значений из памяти.
        """
    ```

- `_build_document_from(memory) -> Document`:
    ```python
    def _build_document_from(memory) -> Document:
        """
        Создает документ из памяти.

        Args:
            memory: Память для создания документа.

        Returns:
            Document: Созданный документ.
        """
    ```

- `_build_documents_from(self, memories: list) -> list`:
    ```python
    def _build_documents_from(self, memories: list) -> list:
        """
        Создает список документов из списка воспоминаний.

        Args:
            memories (list): Список воспоминаний для создания документов.

        Returns:
            list: Список созданных документов.
        """
    ```

## Функции

### `_build_document_from`

```python
def _build_document_from(memory) -> Document:
    """
    Создает документ из памяти.

    Args:
        memory: Память для создания документа.

    Returns:
        Document: Созданный документ.
    """
```

**Как работает функция**:

1. Принимает значение `memory` в качестве аргумента.
2. Преобразует значение `memory` в строковое представление.
3. Создает объект `Document` из `llama_index.core` с использованием строкового представления `memory` в качестве текста.
4. Возвращает созданный объект `Document`.

```
memory_data --> Преобразование в строку --> Создание Document --> Document
```

**Примеры**:

```python
from llama_index.core import Document

# Пример вызова функции
memory_data = "Some memory data"
document = _build_document_from(memory_data)

print(type(document))  # Вывод: <class 'llama_index.core.schema.Document'>
print(document.text)   # Вывод: Some memory data
```

### `_build_documents_from`

```python
def _build_documents_from(self, memories: list) -> list:
    """
    Создает список документов из списка воспоминаний.

    Args:
        memories (list): Список воспоминаний для создания документов.

    Returns:
        list: Список созданных документов.
    """
```

**Как работает функция**:

1. Принимает список `memories` в качестве аргумента.
2. Использует генератор списков для итерации по каждому элементу в списке `memories`.
3. Для каждого элемента вызывает функцию `self._build_document_from(memory)`.
4. Возвращает список, содержащий объекты `Document`, созданные из каждого элемента списка `memories`.

```
memories --> Итерация по списку --> Создание Document (self._build_document_from) --> Список Document
```

**Примеры**:

```python
from llama_index.core import Document

class ExampleClass:
    def _build_document_from(self, memory):
        return Document(text=str(memory))

    def _build_documents_from(self, memories: list) -> list:
        return [self._build_document_from(memory) for memory in memories]

# Пример вызова функции
memories_data = ["Memory 1", "Memory 2", "Memory 3"]
example_instance = ExampleClass()
documents = example_instance._build_documents_from(memories_data)

print(type(documents))        # Вывод: <class 'list'>
print(type(documents[0]))     # Вывод: <class 'llama_index.core.schema.Document'>
print(documents[0].text)      # Вывод: Memory 1
print(documents[1].text)      # Вывод: Memory 2
print(documents[2].text)      # Вывод: Memory 3
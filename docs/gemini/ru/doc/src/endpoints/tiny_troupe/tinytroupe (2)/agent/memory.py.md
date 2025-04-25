# Модуль TinyMemory
## Обзор

Данный модуль предоставляет базовые механизмы работы с памятью для агентов в системе TinyTroupe. Модуль реализует две основных концепции памяти: эпизодическую (EpisodicMemory) и семантическую (SemanticMemory).

## Подробней

Модуль `memory.py` в проекте `hypotez` реализует базовые концепции памяти для агентов TinyTroupe. В основе модуля лежит класс `TinyMemory`, от которого наследуются разные типы памяти. 

`TinyMemory` - это базовый класс, реализующий общий интерфейс для всех типов памяти. Он предоставляет методы для хранения (`store`, `store_all`), извлечения (`retrieve`, `retrieve_recent`, `retrieve_all`, `retrieve_relevant`) и подсчета (`count`) данных.

## Классы

### `class TinyMemory`

**Описание**: Базовый класс для разных типов памяти.

**Наследует**:

* `TinyMentalFaculty`

**Атрибуты**:

* `None`

**Методы**:

* `_preprocess_value_for_storage(value: Any) -> Any`: Предварительная обработка значения перед хранением в памяти.
* `_store(value: Any) -> None`: Хранит значение в памяти. 
* `store(value: dict) -> None`: Хранит значение в памяти.
* `store_all(values: list) -> None`: Хранит список значений в памяти.
* `retrieve(first_n: int, last_n: int, include_omission_info:bool=True) -> list`: Извлекает первые `first_n` и/или последние `last_n` значения из памяти.
* `retrieve_recent() -> list`: Извлекает последние `n` значений из памяти.
* `retrieve_all() -> list`: Извлекает все значения из памяти.
* `retrieve_relevant(relevance_target:str, top_k=20) -> list`: Извлекает все значения из памяти, которые релевантны заданному `relevance_target`.

**Пример**:

```python
from tinytroupe.agent.memory import TinyMemory

memory = TinyMemory()

# Храним значение
memory.store({'key': 'value'})

# Извлекаем значения
values = memory.retrieve(first_n=1, last_n=0)

print(values) # [ {'key': 'value'} ]
```


### `class EpisodicMemory`

**Описание**: Реализует эпизодическую память, позволяя агенту хранить и извлекать сообщения из памяти.

**Наследует**:

* `TinyMemory`

**Атрибуты**:

* `fixed_prefix_length (int)`: Длина фиксированного префикса. По умолчанию 100.
* `lookback_length (int)`: Длина периода обратной связи. По умолчанию 100.
* `memory (list)`: Список хранимых значений.

**Методы**:

* `_store(value: Any) -> None`: Хранит значение в памяти.
* `count() -> int`: Возвращает количество значений в памяти.
* `retrieve(first_n: int, last_n: int, include_omission_info:bool=True) -> list`: Извлекает первые `first_n` и/или последние `last_n` значения из памяти.
* `retrieve_recent(include_omission_info:bool=True) -> list`: Извлекает последние `n` значений из памяти.
* `retrieve_all() -> list`: Извлекает все значения из памяти.
* `retrieve_relevant(relevance_target: str, top_k:int) -> list`: Извлекает `top_k` наиболее релевантных значений из памяти по заданному `relevance_target`.
* `retrieve_first(n: int, include_omission_info:bool=True) -> list`: Извлекает первые `n` значений из памяти.
* `retrieve_last(n: int, include_omission_info:bool=True) -> list`: Извлекает последние `n` значений из памяти.

**Пример**:

```python
from tinytroupe.agent.memory import EpisodicMemory

memory = EpisodicMemory()

# Храним сообщения в памяти
memory.store({'role': 'user', 'content': 'Привет!', 'simulation_timestamp': '2023-12-01T12:00:00'})
memory.store({'role': 'assistant', 'content': 'Привет!', 'simulation_timestamp': '2023-12-01T12:01:00'})

# Извлекаем последние два сообщения
messages = memory.retrieve_recent()

print(messages)
# [
#   {'role': 'assistant', 'content': 'Привет!', 'simulation_timestamp': '2023-12-01T12:01:00'},
#   {'role': 'user', 'content': 'Привет!', 'simulation_timestamp': '2023-12-01T12:00:00'},
# ]
```

### `class SemanticMemory`

**Описание**: Реализует семантическую память, позволяя агенту хранить и извлекать семантическую информацию.

**Наследует**:

* `TinyMemory`

**Атрибуты**:

* `memories (list)`: Список хранимых значений.
* `semantic_grounding_connector (BaseSemanticGroundingConnector)`: Объект для работы с семантической информацией.

**Методы**:

* `_preprocess_value_for_storage(value: dict) -> Any`: Предварительная обработка значения перед хранением в памяти.
* `_store(value: Any) -> None`: Хранит значение в памяти.
* `retrieve_relevant(relevance_target:str, top_k=20) -> list`: Извлекает все значения из памяти, которые релевантны заданному `relevance_target`.
* `_build_document_from(memory) -> Document`: Создает объект `Document` из значения памяти.
* `_build_documents_from(self, memories: list) -> list`: Создает список объектов `Document` из списка значений памяти.

**Пример**:

```python
from tinytroupe.agent.memory import SemanticMemory

memory = SemanticMemory()

# Храним информацию в семантической памяти
memory.store({'type': 'action', 'content': 'Я выполнил действие', 'simulation_timestamp': '2023-12-01T12:00:00'})
memory.store({'type': 'stimulus', 'content': 'Я получил стимул', 'simulation_timestamp': '2023-12-01T12:01:00'})

# Извлекаем информацию, релевантную заданному запросу
relevant_info = memory.retrieve_relevant(relevance_target='действие', top_k=1)

print(relevant_info)
# [
#     {'role': 'assistant', 'content': '# Fact\nI have performed the following action at date and time 2023-12-01T12:00:00:\n\n Я выполнил действие', 'simulation_timestamp': '2023-12-01T12:00:00'}
# ]
```


## Внутренние функции

* **`_build_document_from(memory) -> Document`**: 
Создает объект `Document` из значения памяти. 

* **`_build_documents_from(self, memories: list) -> list`**: 
Создает список объектов `Document` из списка значений памяти.
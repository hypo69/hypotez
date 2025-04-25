# Модуль `results_reducer`

## Обзор

Модуль `results_reducer` содержит класс `ResultsReducer`, который используется для  сборки данных, извлекаемых из симуляции `TinyTroupe`. 

## Подробнее

Этот модуль играет важную роль в обработке результатов симуляции `TinyTroupe`, предоставляя инструменты для сбора и форматирования данных, извлеченных из действий персонажей. 

## Классы

### `ResultsReducer`

**Описание**: Класс `ResultsReducer` используется для сбора и сокращения результатов, извлекаемых из симуляции `TinyTroupe`. Он определяет правила сокращения (редукции) данных, основанные на типах событий (стимулы, действия).

**Атрибуты**:

- `results` (dict): Словарь, который хранит сокращенные результаты.
- `rules` (dict): Словарь, который хранит правила сокращения. Ключи - типы событий (стимулы, действия), значения - функции, которые применяются к соответствующим событиям.

**Методы**:

- `add_reduction_rule(trigger: str, func: callable)`: Добавляет новое правило сокращения.
- `reduce_agent(agent: TinyPerson) -> list`:  Сокращает результаты симуляции для заданного агента `TinyPerson`.
- `reduce_agent_to_dataframe(agent: TinyPerson, column_names: list=None) -> pd.DataFrame`:  Преобразовывает сокращенные результаты в `pandas DataFrame`.

#### `add_reduction_rule(trigger: str, func: callable)`

**Назначение**:  Добавляет новое правило сокращения для типа события.

**Параметры**:

- `trigger` (str): Тип события, для которого добавляется правило.
- `func` (callable): Функция, которая будет применена к событиям данного типа.

**Возвращает**: 
- `None`

**Вызывает исключения**:
- `Exception`: Если правило для заданного `trigger` уже существует.

#### `reduce_agent(agent: TinyPerson) -> list`

**Назначение**: Сокращает результаты симуляции для заданного агента `TinyPerson`, применяя определенные правила редукции к событиям из эпизодической памяти агента.

**Параметры**:

- `agent` (`TinyPerson`): Агент `TinyPerson`, для которого необходимо сократить результаты.

**Возвращает**: 
- `list`: Список сокращенных результатов, представляющих события агента.

**Как работает функция**:

- Функция получает агента `TinyPerson` и перебирает все сообщения в его эпизодической памяти. 
- Для каждого сообщения:
    - Если роль сообщения `system`, функция пропускает его. 
    - Если роль сообщения `user`, функция извлекает информацию о стимуле (тип, содержание, источник, время).
    - Если роль сообщения `assistant`, функция извлекает информацию о действии (тип, содержание, цель, время).
- Для каждого стимула или действия, функция проверяет, есть ли правило редукции для его типа.
- Если правило существует, функция применяет его к событию, получая сокращенный результат, который добавляется в список.

**Примеры**: 

```python
from tinytroupe.agent import TinyPerson
from tinytroupe.extraction.results_reducer import ResultsReducer
from tinytroupe.extraction import logger


# Создание инстанса ResultsReducer
reducer = ResultsReducer()


# Определение правила редукции для события "стимул - товар"
def reduce_stimulus_product(focus_agent: TinyPerson, source_agent: TinyPerson, target_agent: TinyPerson, kind: str, event: str, content: dict, timestamp: float):
    """
    Пример правила сокращения для события "стимул - товар"
    
    Args:
        focus_agent (TinyPerson): Агент, для которого сокращаются результаты.
        source_agent (TinyPerson): Источник стимула.
        target_agent (TinyPerson): Целевой агент, к которому применяется стимул.
        kind (str): Тип события ("stimulus" или "action").
        event (str): Тип события ("product").
        content (dict): Содержание стимула.
        timestamp (float): Время события.
    
    Returns:
        dict: Сокращенный результат, содержащий информацию о стимуле и его источнике.
    """
    # Создание сокращенного результата
    return {
        'agent': focus_agent.name,
        'kind': kind,
        'event': event,
        'timestamp': timestamp,
        'content': {
            'product_name': content['name'],
            'source_agent': source_agent.name,
            'source_agent_type': source_agent.type,
            'description': content['description'],
        },
    }

# Добавление правила в ResultsReducer
reducer.add_reduction_rule('product', reduce_stimulus_product)

# Создание агента TinyPerson
agent = TinyPerson(name="Alice", type="human")

# Пример использования метода `reduce_agent`
reduced_results = reducer.reduce_agent(agent)
print(reduced_results)
```


#### `reduce_agent_to_dataframe(agent: TinyPerson, column_names: list=None) -> pd.DataFrame`

**Назначение**: Преобразовывает сокращенные результаты в `pandas DataFrame`.

**Параметры**:

- `agent` (`TinyPerson`): Агент `TinyPerson`, для которого необходимо сократить результаты.
- `column_names` (list): Список названий столбцов для `DataFrame`.

**Возвращает**: 
- `pd.DataFrame`: DataFrame с сокращенными результатами.

**Как работает функция**:

- Функция вычисляет сокращенные результаты для агента, используя метод `reduce_agent`.
- Затем функция создает DataFrame из сокращенных результатов. 
- Если заданы имена столбцов, они будут использованы для DataFrame. 

**Примеры**:

```python
from tinytroupe.agent import TinyPerson
from tinytroupe.extraction.results_reducer import ResultsReducer
from tinytroupe.extraction import logger


# Создание инстанса ResultsReducer
reducer = ResultsReducer()


# Определение правила редукции для события "стимул - товар"
def reduce_stimulus_product(focus_agent: TinyPerson, source_agent: TinyPerson, target_agent: TinyPerson, kind: str, event: str, content: dict, timestamp: float):
    """
    Пример правила сокращения для события "стимул - товар"
    
    Args:
        focus_agent (TinyPerson): Агент, для которого сокращаются результаты.
        source_agent (TinyPerson): Источник стимула.
        target_agent (TinyPerson): Целевой агент, к которому применяется стимул.
        kind (str): Тип события ("stimulus" или "action").
        event (str): Тип события ("product").
        content (dict): Содержание стимула.
        timestamp (float): Время события.
    
    Returns:
        dict: Сокращенный результат, содержащий информацию о стимуле и его источнике.
    """
    # Создание сокращенного результата
    return {
        'agent': focus_agent.name,
        'kind': kind,
        'event': event,
        'timestamp': timestamp,
        'content': {
            'product_name': content['name'],
            'source_agent': source_agent.name,
            'source_agent_type': source_agent.type,
            'description': content['description'],
        },
    }

# Добавление правила в ResultsReducer
reducer.add_reduction_rule('product', reduce_stimulus_product)

# Создание агента TinyPerson
agent = TinyPerson(name="Alice", type="human")

# Пример использования метода `reduce_agent_to_dataframe`
df = reducer.reduce_agent_to_dataframe(agent, column_names=['agent', 'kind', 'event', 'timestamp', 'content'])
print(df)
```

## Параметры класса

- `results` (dict): Словарь, который хранит сокращенные результаты. Ключи - имена агентов, значения - списки сокращенных результатов для каждого агента.
- `rules` (dict): Словарь, который хранит правила сокращения. Ключи - типы событий (стимулы, действия), значения - функции, которые применяются к соответствующим событиям.
 
 
## Примеры

**Пример 1**:  Использование `ResultsReducer` для сокращения результатов симуляции для агента `Alice`:

```python
from tinytroupe.agent import TinyPerson
from tinytroupe.extraction.results_reducer import ResultsReducer

# Создание инстанса ResultsReducer
reducer = ResultsReducer()

# Создание агента TinyPerson
agent = TinyPerson(name="Alice", type="human")

# Сокращение результатов симуляции для агента `Alice`
reduced_results = reducer.reduce_agent(agent)
print(reduced_results)
```

**Пример 2**: Преобразование сокращенных результатов в `pandas DataFrame`:

```python
from tinytroupe.agent import TinyPerson
from tinytroupe.extraction.results_reducer import ResultsReducer

# Создание инстанса ResultsReducer
reducer = ResultsReducer()

# Создание агента TinyPerson
agent = TinyPerson(name="Alice", type="human")

# Сокращение результатов симуляции для агента `Alice`
df = reducer.reduce_agent_to_dataframe(agent, column_names=['agent', 'kind', 'event', 'timestamp', 'content'])
print(df)
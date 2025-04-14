# Модуль для сведения результатов

## Обзор

Модуль `results_reducer.py` предназначен для сведения и обработки результатов, полученных от агентов `TinyPerson` в проекте `hypotez`. Он содержит класс `ResultsReducer`, который позволяет добавлять правила сведения результатов на основе определенных триггеров, а также преобразовывать результаты агентов в структуру `pandas.DataFrame`.

## Подробней

Этот модуль играет важную роль в анализе данных, полученных в результате симуляций с использованием агентов `TinyPerson`. Класс `ResultsReducer` предоставляет механизмы для извлечения значимой информации из эпизодической памяти агентов и представления ее в удобном для анализа формате. Он позволяет определить правила сведения, которые применяются к сообщениям агентов в зависимости от их роли (например, `system`, `user`, `assistant`) и типа события (например, стимул или действие). Полученные результаты могут быть преобразованы в `pandas.DataFrame` для дальнейшего анализа и визуализации.

## Классы

### `ResultsReducer`

**Описание**: Класс предназначен для сведения и обработки результатов, полученных от агентов `TinyPerson`.

**Атрибуты**:
- `results` (dict): Словарь для хранения результатов сведения.
- `rules` (dict): Словарь, содержащий правила сведения, где ключ - это триггер (тип события), а значение - функция сведения.

**Методы**:
- `__init__()`: Инициализирует экземпляр класса `ResultsReducer` с пустыми словарями для результатов и правил.
- `add_reduction_rule(trigger: str, func: callable)`: Добавляет правило сведения для указанного триггера.
- `reduce_agent(agent: TinyPerson) -> list`: Сводит результаты для указанного агента, применяя соответствующие правила сведения.
- `reduce_agent_to_dataframe(agent: TinyPerson, column_names: list=None) -> pd.DataFrame`: Сводит результаты для указанного агента и преобразует их в `pandas.DataFrame`.

**Принцип работы**:

Класс `ResultsReducer` работает следующим образом:

1.  При инициализации создаются два пустых словаря: `self.results` для хранения результатов сведения и `self.rules` для хранения правил сведения.
2.  Метод `add_reduction_rule` позволяет добавлять правила сведения, связывая триггер (тип события) с функцией, которая будет выполнять сведение.
3.  Метод `reduce_agent` выполняет сведение результатов для конкретного агента. Он перебирает все сообщения из эпизодической памяти агента и применяет соответствующие правила сведения в зависимости от роли сообщения (`user` или `assistant`) и типа события.
4.  Метод `reduce_agent_to_dataframe` вызывает `reduce_agent` для получения списка сведенных результатов и преобразует его в `pandas.DataFrame`.

## Методы класса

### `__init__`

```python
def __init__(self):
    """
    Инициализирует экземпляр класса `ResultsReducer`.

    Args:
        Нет

    Returns:
        Нет

    Raises:
        Нет
    """
    ...
```

### `add_reduction_rule`

```python
def add_reduction_rule(self, trigger: str, func: callable):
    """
    Добавляет правило сведения для указанного триггера.

    Args:
        trigger (str): Триггер, определяющий, когда применять правило сведения.
        func (callable): Функция, выполняющая сведение результатов.

    Returns:
        Нет

    Raises:
        Exception: Если правило для указанного триггера уже существует.

    Example:
        >>> reducer = ResultsReducer()
        >>> def my_reduction_rule(agent, event, content):
        ...     return {'agent_name': agent.name, 'event': event, 'content': content}
        >>> reducer.add_reduction_rule('my_event', my_reduction_rule)
    """
    ...
```

### `reduce_agent`

```python
def reduce_agent(self, agent: TinyPerson) -> list:
    """
    Сводит результаты для указанного агента, применяя соответствующие правила сведения.

    Args:
        agent (TinyPerson): Агент, для которого выполняется сведение результатов.

    Returns:
        list: Список сведенных результатов.

    Raises:
        Нет

    Как работает функция:
        1. Инициализируется пустой список `reduction` для хранения сведенных результатов.
        2. Проходится по всем сообщениям в эпизодической памяти агента.
        3. Для каждого сообщения проверяется его роль:
            - Если роль `system`, сообщение игнорируется.
            - Если роль `user`, извлекается тип стимула (`stimulus_type`), содержимое стимула (`stimulus_content`), источник стимула (`stimulus_source`) и временная метка стимула (`stimulus_timestamp`). Если для `stimulus_type` определено правило сведения, оно применяется, и результат добавляется в список `reduction`.
            - Если роль `assistant`, извлекается тип действия (`action_type`), содержимое действия (`action_content`), цель действия (`action_target`) и временная метка действия (`action_timestamp`). Если для `action_type` определено правило сведения, оно применяется, и результат добавляется в список `reduction`.
        4. Возвращается список `reduction` со сведенными результатами.

    Примеры:
        >>> from tinytroupe.agent import TinyPerson
        >>> agent = TinyPerson(name='TestAgent')
        >>> reducer = ResultsReducer()
        >>> def my_reduction_rule(focus_agent, source_agent, target_agent, kind, event, content, timestamp):
        ...     return {'agent_name': focus_agent.name, 'event': event, 'content': content}
        >>> reducer.add_reduction_rule('test_event', my_reduction_rule)
        >>> agent.episodic_memory.store({'role': 'user', 'content': {'stimuli': [{'type': 'test_event', 'content': 'test_content', 'source': 'TestSource'}]}, 'simulation_timestamp': 1})
        >>> reducer.reduce_agent(agent)
        [{'agent_name': 'TestAgent', 'event': 'test_event', 'content': 'test_content'}]
    """
    ...
```

### `reduce_agent_to_dataframe`

```python
def reduce_agent_to_dataframe(self, agent: TinyPerson, column_names: list=None) -> pd.DataFrame:
    """
    Сводит результаты для указанного агента и преобразует их в `pandas.DataFrame`.

    Args:
        agent (TinyPerson): Агент, для которого выполняется сведение результатов.
        column_names (list, optional): Список названий столбцов для `DataFrame`. По умолчанию `None`.

    Returns:
        pd.DataFrame: `DataFrame` с сведенными результатами.

    Raises:
        Нет

    Как работает функция:
        1. Вызывает метод `reduce_agent` для получения списка сведенных результатов.
        2. Преобразует список сведенных результатов в `pandas.DataFrame` с использованием указанных названий столбцов (если они предоставлены).
        3. Возвращает полученный `DataFrame`.

    Примеры:
        >>> import pandas as pd
        >>> from tinytroupe.agent import TinyPerson
        >>> agent = TinyPerson(name='TestAgent')
        >>> reducer = ResultsReducer()
        >>> def my_reduction_rule(focus_agent, source_agent, target_agent, kind, event, content, timestamp):
        ...     return {'agent_name': focus_agent.name, 'event': event, 'content': content}
        >>> reducer.add_reduction_rule('test_event', my_reduction_rule)
        >>> agent.episodic_memory.store({'role': 'user', 'content': {'stimuli': [{'type': 'test_event', 'content': 'test_content', 'source': 'TestSource'}]}, 'simulation_timestamp': 1})
        >>> reducer.reduce_agent_to_dataframe(agent)
           agent_name       event    content
        0  TestAgent  test_event  test_content
    """
    ...
```
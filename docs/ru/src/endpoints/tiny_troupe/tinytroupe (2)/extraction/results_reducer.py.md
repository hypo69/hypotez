# Модуль для сведения результатов агентов
## Обзор

Модуль `results_reducer.py` предназначен для обработки и сведения результатов, полученных от агентов `TinyPerson` в рамках проекта `hypotez`. Он предоставляет функциональность для добавления правил сведения, применения этих правил к данным агентов и преобразования результатов в формат `DataFrame`.

## Подробней

Модуль содержит класс `ResultsReducer`, который управляет правилами сведения и выполняет их применение к эпизодической памяти агентов. Правила сведения позволяют извлекать и обрабатывать информацию из сообщений агентов, разделяя их по ролям (стимулы от пользователя и действия от ассистента). Полученные данные могут быть преобразованы в структурированный формат `DataFrame` для дальнейшего анализа.

## Классы

### `ResultsReducer`

**Описание**: Класс `ResultsReducer` предназначен для сведения (редукции) результатов, полученных от агентов `TinyPerson`. Он позволяет добавлять правила обработки сообщений агентов и преобразовывать результаты в формат `DataFrame`.

**Атрибуты**:
- `results (dict)`: Словарь для хранения результатов сведения.
- `rules (dict)`: Словарь для хранения правил сведения, где ключ - тип триггера, значение - функция для обработки.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `ResultsReducer` с пустыми словарями для хранения результатов и правил.
- `add_reduction_rule`: Добавляет правило сведения для определенного триггера.
- `reduce_agent`: Применяет правила сведения к сообщениям агента и возвращает список извлеченных данных.
- `reduce_agent_to_dataframe`: Преобразует результаты сведения агента в формат `DataFrame`.

#### `__init__`

```python
def __init__(self):
    """
    Инициализирует экземпляр класса `ResultsReducer`.

    Args:
        self: Экземпляр класса `ResultsReducer`.

    Returns:
        None

    Пример:
        >>> reducer = ResultsReducer()
        >>> print(reducer.results)
        {}
        >>> print(reducer.rules)
        {}
    """
    ...
```

#### `add_reduction_rule`

```python
def add_reduction_rule(self, trigger: str, func: callable):
    """
    Добавляет правило сведения для определенного триггера.

    Args:
        trigger (str): Триггер, при котором применяется правило (например, тип стимула или действия).
        func (callable): Функция, выполняющая сведение данных при срабатывании триггера.

    Returns:
        None

    Raises:
        Exception: Если правило для данного триггера уже существует.

    Пример:
        >>> def my_reduction_rule(focus_agent, source_agent, target_agent, kind, event, content, timestamp):
        ...     return {'event': event, 'content': content}
        >>> reducer = ResultsReducer()
        >>> reducer.add_reduction_rule('my_event', my_reduction_rule)
        >>> print(reducer.rules)
        {'my_event': <function my_reduction_rule at 0x...>}
    """
    ...
```

#### `reduce_agent`

```python
def reduce_agent(self, agent: TinyPerson) -> list:
    """
    Применяет правила сведения к сообщениям агента и возвращает список извлеченных данных.

    Args:
        agent (TinyPerson): Агент, для которого выполняется сведение результатов.

    Returns:
        list: Список извлеченных данных, полученных в результате применения правил сведения.

    Как работает функция:
    - Функция извлекает все сообщения из эпизодической памяти агента.
    - Итерируется по сообщениям и применяет правила сведения в зависимости от роли сообщения (`system`, `user`, `assistant`).
    - Для сообщений с ролью `user` извлекает тип стимула (`stimulus_type`), содержимое (`stimulus_content`), источник (`stimulus_source`) и временную метку (`stimulus_timestamp`). Если для `stimulus_type` определено правило, применяет его.
    - Для сообщений с ролью `assistant` извлекает тип действия (`action_type`), содержимое (`action_content`), цель (`action_target`) и временную метку (`action_timestamp`). Если для `action_type` определено правило, применяет его.
    - Возвращает список извлеченных данных.

    Пример:
        >>> from unittest.mock import MagicMock
        >>> agent_mock = MagicMock(spec=TinyPerson)
        >>> agent_mock.episodic_memory.retrieve_all.return_value = [
        ...     {'role': 'user', 'content': {'stimuli': [{'type': 'event1', 'content': 'content1', 'source': 'source1'}]}, 'simulation_timestamp': 100},
        ...     {'role': 'assistant', 'content': {'action': {'type': 'action1', 'content': 'content2', 'target': 'target1'}}, 'simulation_timestamp': 200}
        ... ]
        >>> def rule_event1(focus_agent, source_agent, target_agent, kind, event, content, timestamp):
        ...     return {'event': event, 'content': content}
        >>> def rule_action1(focus_agent, source_agent, target_agent, kind, event, content, timestamp):
        ...     return {'event': event, 'content': content}
        >>> reducer = ResultsReducer()
        >>> reducer.add_reduction_rule('event1', rule_event1)
        >>> reducer.add_reduction_rule('action1', rule_action1)
        >>> result = reducer.reduce_agent(agent_mock)
        >>> print(result)
        [{'event': 'event1', 'content': 'content1'}, {'event': 'action1', 'content': 'content2'}]
    """
    reduction = []
    for message in agent.episodic_memory.retrieve_all():
        if message['role'] == 'system':
            continue  # doing nothing for `system` role yet at least

        elif message['role'] == 'user':
            # User role is related to stimuli only
            stimulus_type = message['content']['stimuli'][0]['type']
            stimulus_content = message['content']['stimuli'][0]['content']
            stimulus_source = message['content']['stimuli'][0]['source']
            stimulus_timestamp = message['simulation_timestamp']

            if stimulus_type in self.rules:
                extracted = self.rules[stimulus_type](focus_agent=agent, source_agent=TinyPerson.get_agent_by_name(stimulus_source), target_agent=agent, kind='stimulus', event=stimulus_type, content=stimulus_content, timestamp=stimulus_timestamp)
                if extracted is not None:
                    reduction.append(extracted)

        elif message['role'] == 'assistant':
            # Assistant role is related to actions only
            if 'action' in message['content']:
                action_type = message['content']['action']['type']
                action_content = message['content']['action']['content']
                action_target = message['content']['action']['target']
                action_timestamp = message['simulation_timestamp']

                if action_type in self.rules:
                    extracted = self.rules[action_type](focus_agent=agent, source_agent=agent, target_agent=TinyPerson.get_agent_by_name(action_target), kind='action', event=action_type, content=action_content, timestamp=action_timestamp)
                    if extracted is not None:
                        reduction.append(extracted)

    return reduction
```

#### `reduce_agent_to_dataframe`

```python
def reduce_agent_to_dataframe(self, agent: TinyPerson, column_names: list=None) -> pd.DataFrame:
    """
    Преобразует результаты сведения агента в формат `DataFrame`.

    Args:
        agent (TinyPerson): Агент, для которого выполняется сведение результатов.
        column_names (list, optional): Список названий столбцов для `DataFrame`. По умолчанию `None`.

    Returns:
        pd.DataFrame: `DataFrame`, содержащий результаты сведения.

    Пример:
        >>> import pandas as pd
        >>> from unittest.mock import MagicMock
        >>> agent_mock = MagicMock(spec=TinyPerson)
        >>> agent_mock.episodic_memory.retrieve_all.return_value = [
        ...     {'role': 'user', 'content': {'stimuli': [{'type': 'event1', 'content': 'content1', 'source': 'source1'}]}, 'simulation_timestamp': 100},
        ...     {'role': 'assistant', 'content': {'action': {'type': 'action1', 'content': 'content2', 'target': 'target1'}}, 'simulation_timestamp': 200}
        ... ]
        >>> def rule_event1(focus_agent, source_agent, target_agent, kind, event, content, timestamp):
        ...     return {'event': event, 'content': content}
        >>> def rule_action1(focus_agent, source_agent, target_agent, kind, event, content, timestamp):
        ...     return {'event': event, 'content': content}
        >>> reducer = ResultsReducer()
        >>> reducer.add_reduction_rule('event1', rule_event1)
        >>> reducer.add_reduction_rule('action1', rule_action1)
        >>> df = reducer.reduce_agent_to_dataframe(agent_mock, column_names=['event', 'content'])
        >>> print(df)
             event   content
        0   event1  content1
        1  action1  content2
    """
    reduction = self.reduce_agent(agent)
    return pd.DataFrame(reduction, columns=column_names)
```
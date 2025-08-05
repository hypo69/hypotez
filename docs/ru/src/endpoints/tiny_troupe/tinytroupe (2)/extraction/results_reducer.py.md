# Модуль `results_reducer.py`

## Обзор

Модуль предназначен для сведения результатов работы агентов `TinyPerson`. Он содержит класс `ResultsReducer`, который агрегирует и обрабатывает информацию из эпизодической памяти агентов, применяя заданные правила сведения.

## Подробней

Этот модуль является частью системы, где агенты взаимодействуют друг с другом, и необходимо собирать и анализировать результаты этих взаимодействий. Класс `ResultsReducer` позволяет определить правила для извлечения значимой информации из сообщений агентов и представления ее в удобном формате, например, в виде DataFrame.
Он использует логирование через модуль `src.logger`.

## Классы

### `ResultsReducer`

**Описание**: Класс для сведения результатов работы агентов `TinyPerson`.

**Атрибуты**:

- `results (dict)`: Словарь для хранения результатов сведения.
- `rules (dict)`: Словарь, содержащий правила сведения, где ключ - это триггер (тип события), а значение - функция, применяемая для сведения.

**Методы**:

- `__init__()`: Инициализирует экземпляр класса `ResultsReducer`, создает пустой словарь для результатов и правил.
- `add_reduction_rule(trigger: str, func: callable)`: Добавляет правило сведения для определенного триггера.
- `reduce_agent(agent: TinyPerson) -> list`: Сводит эпизодическую память агента, применяя правила сведения.
- `reduce_agent_to_dataframe(agent: TinyPerson, column_names: list=None) -> pd.DataFrame`: Сводит эпизодическую память агента в DataFrame.

#### `__init__`
```python
    def __init__(self):
        """
        Инициализирует экземпляр класса `ResultsReducer`.

        Создает пустые словари для хранения результатов сведения (`self.results`)
        и правил сведения (`self.rules`).
        """
        self.results = {}
        self.rules = {}
```

#### `add_reduction_rule`
```python
    def add_reduction_rule(self, trigger: str, func: callable):
        """
        Добавляет правило сведения для определенного триггера.

        Args:
            trigger (str): Триггер, определяющий, когда применять данное правило.
            func (callable): Функция, выполняющая сведение данных.

        Raises:
            Exception: Если правило для данного триггера уже существует.
        """
        if trigger in self.rules:
            raise Exception(f"Rule for {trigger} already exists.")

        self.rules[trigger] = func
```

**Как работает функция**:
Функция `add_reduction_rule` добавляет правило сведения в словарь `self.rules`. Если правило для указанного триггера уже существует, выбрасывается исключение.

**Примеры**:
```python
reducer = ResultsReducer()
def my_reduction_func(focus_agent, source_agent, target_agent, kind, event, content, timestamp):
    return {"event": event, "content": content}

reducer.add_reduction_rule("my_event", my_reduction_func)
```

#### `reduce_agent`
```python
    def reduce_agent(self, agent: TinyPerson) -> list:
        """
        Сводит эпизодическую память агента, применяя правила сведения.

        Args:
            agent (TinyPerson): Агент, эпизодическую память которого необходимо свести.

        Returns:
            list: Список извлеченных данных.
        """
        reduction = []
        for message in agent.episodic_memory.retrieve_all():
            if message['role'] == 'system':
                continue # doing nothing for `system` role yet at least

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

**Как работает функция**:

Функция `reduce_agent` выполняет следующие действия:

1.  Инициализирует пустой список `reduction` для хранения извлеченных данных.
2.  Перебирает все сообщения из эпизодической памяти агента (`agent.episodic_memory.retrieve_all()`).
3.  Проверяет роль каждого сообщения (`message['role']`) и выполняет соответствующие действия:
    *   Если роль `system`, то сообщение игнорируется (пока не обрабатывается).
    *   Если роль `user`, то извлекаются данные о стимуле (тип, содержимое, источник, время) и, если для типа стимула (`stimulus_type`) определено правило в `self.rules`, применяется это правило для извлечения данных. Если извлеченные данные не `None`, они добавляются в список `reduction`.
    *   Если роль `assistant`, то извлекаются данные о действии (тип, содержимое, цель, время) и, если для типа действия (`action_type`) определено правило в `self.rules`, применяется это правило для извлечения данных. Если извлеченные данные не `None`, они добавляются в список `reduction`.
4.  Возвращает список `reduction`, содержащий извлеченные данные.

**Примеры**:
```python
reducer = ResultsReducer()
agent = TinyPerson(name="agent1")
agent.episodic_memory.store({"role": "user", "content": {"stimuli": [{"type": "test_event", "content": "test_content", "source": "agent2"}]}, "simulation_timestamp": 1})

def my_reduction_func(focus_agent, source_agent, target_agent, kind, event, content, timestamp):
    return {"event": event, "content": content}

reducer.add_reduction_rule("test_event", my_reduction_func)
reduction_result = reducer.reduce_agent(agent)
print(reduction_result)  # Вывод: [{'event': 'test_event', 'content': 'test_content'}]
```

#### `reduce_agent_to_dataframe`
```python
    def reduce_agent_to_dataframe(self, agent: TinyPerson, column_names: list=None) -> pd.DataFrame:
        """
        Сводит эпизодическую память агента в DataFrame.

        Args:
            agent (TinyPerson): Агент, эпизодическую память которого необходимо свести.
            column_names (list, optional): Список названий колонок для DataFrame. По умолчанию `None`.

        Returns:
            pd.DataFrame: DataFrame с извлеченными данными.
        """
        reduction = self.reduce_agent(agent)
        return pd.DataFrame(reduction, columns=column_names)
```

**Как работает функция**:
Функция `reduce_agent_to_dataframe` сначала вызывает функцию `self.reduce_agent(agent)` для получения списка извлеченных данных, а затем преобразует этот список в DataFrame с использованием библиотеки `pandas`. Если указан список названий колонок (`column_names`), он используется для задания названий колонок в DataFrame.

**Примеры**:
```python
reducer = ResultsReducer()
agent = TinyPerson(name="agent1")
agent.episodic_memory.store({"role": "user", "content": {"stimuli": [{"type": "test_event", "content": "test_content", "source": "agent2"}]}, "simulation_timestamp": 1})

def my_reduction_func(focus_agent, source_agent, target_agent, kind, event, content, timestamp):
    return {"event": event, "content": content}

reducer.add_reduction_rule("test_event", my_reduction_func)
df = reducer.reduce_agent_to_dataframe(agent, column_names=["event", "content"])
print(df)
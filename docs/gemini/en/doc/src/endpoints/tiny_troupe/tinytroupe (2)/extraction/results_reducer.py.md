# Results Reducer

## Overview

Этот модуль содержит класс `ResultsReducer`, который используется для агрегирования и обработки результатов действий и стимулов, полученных от агентов `TinyPerson`. Класс позволяет создавать правила для обработки различных типов действий и стимулов, а также для агрегации этих результатов в структуру `pandas.DataFrame`.

## Details

`ResultsReducer` предназначен для того, чтобы в унифицированном виде хранить данные о действиях и стимулах, которые произошли в модели `TinyPerson`. Модель агента `TinyPerson` использует  `episodic_memory` для хранения данных о событиях, происходящих с ней,  записанных в виде сообщений. Класс `ResultsReducer` позволяет агрегировать сообщения из `episodic_memory`  в `pandas.DataFrame`  с помощью `reduce_agent_to_dataframe()` для  дальнейшего анализа. 

## Classes

### `ResultsReducer`

**Description:** Класс для агрегации и обработки результатов действий и стимулов от `TinyPerson` агентов.

**Attributes:**

* `results (dict)`: Словарь для хранения результатов. 
* `rules (dict)`: Словарь для хранения правил агрегации.

**Methods:**

* `add_reduction_rule(trigger: str, func: callable)`: Добавление правила агрегации для определенного типа действий или стимулов.
* `reduce_agent(agent: TinyPerson) -> list`: Агрегация результатов от агента.
* `reduce_agent_to_dataframe(agent: TinyPerson, column_names: list=None) -> pd.DataFrame`: Преобразование результатов в `pandas.DataFrame`.


#### `add_reduction_rule(trigger: str, func: callable)`

**Purpose:** Добавление правила агрегации для конкретного типа действия или стимула. 

**Parameters:**

* `trigger (str)`: Тип действия или стимула (например, "visit_product", "add_to_cart").
* `func (callable)`: Функция, которая будет использоваться для агрегации результатов этого типа действия или стимула.

**Returns:**

* `None`

**Raises Exceptions:**

* `Exception`: Если правило для этого типа действия или стимула уже существует.

**How the Function Works:**

* Проверяет, существует ли правило для переданного `trigger`.
* Если правило уже существует, то возбуждает исключение.
* Если правило еще не существует, то добавляет его в `rules` dictionary.

#### `reduce_agent(agent: TinyPerson) -> list`

**Purpose:** Агрегация результатов, полученных от конкретного агента `TinyPerson`,  в список.

**Parameters:**

* `agent (TinyPerson)`: Объект агента, для которого производится агрегация.

**Returns:**

* `list`: Список с результатами агрегации.

**How the Function Works:**

* Получает сообщения из `episodic_memory` агента.
* Для каждого сообщения в `episodic_memory` проверяет его `role`.
* Если сообщение с ролью `user`,  извлекается информация о `stimulus_type`, `stimulus_content`, `stimulus_source` и `stimulus_timestamp`.
* Проверяет, есть ли правило для `stimulus_type` в `rules`.
* Если правило есть, то вызывает функцию из правила и добавляет результат в список `reduction`.
* Если сообщение с ролью `assistant`,  извлекается информация о `action_type`, `action_content`, `action_target` и `action_timestamp`.
* Проверяет, есть ли правило для `action_type` в `rules`.
* Если правило есть, то вызывает функцию из правила и добавляет результат в список `reduction`.
* Возвращает список `reduction` с агрегированными результатами.

#### `reduce_agent_to_dataframe(agent: TinyPerson, column_names: list=None) -> pd.DataFrame`

**Purpose:** Преобразование списка агрегированных результатов в `pandas.DataFrame`.

**Parameters:**

* `agent (TinyPerson)`: Объект агента, для которого производится агрегация.
* `column_names (list, optional)`: Имена столбцов в результирующем `DataFrame`. По умолчанию `None`.

**Returns:**

* `pd.DataFrame`: `DataFrame` с агрегированными результатами.

**How the Function Works:**

* Вызывает `reduce_agent()` для получения списка агрегированных результатов.
* Создает `pandas.DataFrame` из списка результатов.
* Возвращает созданный `DataFrame`.

## Examples

```python
# Create an instance of ResultsReducer
results_reducer = ResultsReducer()

# Define a reduction rule for the 'visit_product' action
def visit_product_rule(focus_agent: TinyPerson, source_agent: TinyPerson, target_agent: TinyPerson, kind: str, event: str, content: str, timestamp: float) -> dict:
    """
    Правило для агрегации результатов посещения товара.
    """
    return {
        'agent_id': focus_agent.id,
        'event_type': event,
        'product_id': content,
        'timestamp': timestamp
    }

# Add the rule to the results reducer
results_reducer.add_reduction_rule(trigger='visit_product', func=visit_product_rule)

# Create a TinyPerson agent
agent = TinyPerson()

# Simulate some actions and stimuli for the agent
# ...

# Reduce the agent's results to a DataFrame
df = results_reducer.reduce_agent_to_dataframe(agent, column_names=['agent_id', 'event_type', 'product_id', 'timestamp'])

# Print the DataFrame
print(df)
```

This example creates a `ResultsReducer` object, defines a rule for `visit_product`, adds the rule, simulates some actions and stimuli for an agent, and then reduces the agent's results to a `pandas.DataFrame`. This `DataFrame` can be used for further analysis of the agent's activities.
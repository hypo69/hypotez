## Как использовать `ResultsReducer`

=========================================================================================

Описание
-------------------------

Класс `ResultsReducer` предназначен для объединения и обработки результатов работы агента `TinyPerson` в виде данных, пригодных для анализа. Он позволяет добавлять правила для обработки определенных типов событий (стимулов или действий) и применяется для преобразования данных агента в структуру `pandas.DataFrame`.

Шаги выполнения
-------------------------

1. **Создание экземпляра `ResultsReducer`**:
   - Инициализирует класс `ResultsReducer`, создавая пустые словари `results` и `rules`.

2. **Добавление правила обработки**:
   - Использует метод `add_reduction_rule` для добавления правила, которое будет использоваться для обработки определенного типа события (например, `stimuli` или `action`).
   - Принимает два параметра:
     - `trigger`: тип события (стимул или действие).
     - `func`: функция, которая будет вызываться для обработки события этого типа.

3. **Сбор данных**:
   - Использует метод `reduce_agent` для сбора данных из эпизодической памяти агента `TinyPerson`.
   - Проходит по всем сообщениям в памяти агента.
   - Проверяет тип роли сообщения (`system`, `user` или `assistant`).
   - Для роли `user` извлекает информацию о стимуле.
   - Для роли `assistant` извлекает информацию о действии.
   - Если тип стимула или действия присутствует в словаре `rules`, вызывает соответствующую функцию, предоставленную в `add_reduction_rule`, для обработки данных.

4. **Создание `pandas.DataFrame`**:
   - Использует метод `reduce_agent_to_dataframe` для преобразования собранных данных в `pandas.DataFrame`.
   - Принимает два параметра:
     - `agent`: объект `TinyPerson`, данные которого необходимо обработать.
     - `column_names`: список названий столбцов для `pandas.DataFrame`.

Пример использования
-------------------------

```python
from tinytroupe.extraction import ResultsReducer
from tinytroupe.agent import TinyPerson

# Создаем экземпляр `ResultsReducer`
reducer = ResultsReducer()

# Добавляем правило для обработки события "text_stimuli"
def process_text_stimuli(focus_agent, source_agent, target_agent, kind, event, content, timestamp):
    # Логика обработки события "text_stimuli"
    # ... 
    return {"timestamp": timestamp, "content": content, "source": source_agent.name}

reducer.add_reduction_rule(trigger="text_stimuli", func=process_text_stimuli)

# Создаем экземпляр `TinyPerson`
agent = TinyPerson(name="Alice")

# Считываем информацию о стимулах из памяти агента
results = reducer.reduce_agent(agent)

# Создаем `pandas.DataFrame` из собранных данных
df = reducer.reduce_agent_to_dataframe(agent, column_names=["timestamp", "content", "source"])

# Выводим `DataFrame`
print(df)
```
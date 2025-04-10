### **Анализ кода модуля `results_reducer.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код достаточно структурирован и логичен.
    - Использование класса `ResultsReducer` позволяет удобно управлять правилами редукции результатов.
    - Наличие метода `add_reduction_rule` позволяет добавлять новые правила редукции.
    - Логика обработки сообщений агентов разделена на основе ролей (user, assistant).
- **Минусы**:
    - Отсутствует подробная документация по классу и методам.
    - Не хватает обработки исключений при вызове правил редукции.
    - Не используются аннотации типов для параметров и возвращаемых значений функций.
    - Не все переменные имеют аннотацию типов.

#### **Рекомендации по улучшению**:
1.  **Добавить документацию**:
    - Добавить docstring для класса `ResultsReducer` с описанием его назначения и основных методов.
    - Добавить docstring для каждого метода класса, описывающий его параметры, возвращаемые значения и возможные исключения.
    - Добавить примеры использования методов в docstring.

2.  **Добавить аннотации типов**:
    - Добавить аннотации типов для всех параметров и возвращаемых значений функций.
    - Добавить аннотации типов для переменных внутри методов.

3.  **Улучшить обработку исключений**:
    - Добавить обработку исключений при вызове правил редукции, чтобы предотвратить падение программы в случае ошибки.
    - Использовать `logger.error` для логирования ошибок.

4.  **Переименовать переменные**:
    - Переименовать переменные `func` в `reduction_func` для лучшей читаемости.

5.  **Улучшить логирование**:
    - Добавить логирование процесса редукции, чтобы упростить отладку и анализ.
    - Логировать важные события, такие как добавление правил редукции, начало и окончание редукции агента, а также ошибки.

6. **Соблюдать PEP8**:
    - Добавить пробелы вокруг операторов присваивания.

#### **Оптимизированный код**:

```python
import pandas as pd
from typing import Callable, Dict, List, Optional
from pathlib import Path

from src.logger import logger  # Импортируем logger из модуля src.logger
from tinytroupe.agent import TinyPerson


class ResultsReducer:
    """
    Класс для редукции результатов, полученных от агентов TinyPerson.

    Args:
        results (Dict): Словарь для хранения результатов редукции.
        rules (Dict[str, Callable]): Словарь, содержащий правила редукции для различных типов событий.
    """

    def __init__(self) -> None:
        """
        Инициализирует ResultsReducer с пустыми результатами и правилами.
        """
        self.results: Dict = {}
        self.rules: Dict[str, Callable] = {}

    def add_reduction_rule(self, trigger: str, reduction_func: Callable) -> None:
        """
        Добавляет правило редукции для указанного триггера.

        Args:
            trigger (str): Триггер, для которого добавляется правило редукции.
            reduction_func (Callable): Функция, которая будет вызываться при срабатывании триггера.

        Raises:
            Exception: Если правило для данного триггера уже существует.

        Example:
            >>> reducer = ResultsReducer()
            >>> def my_rule(focus_agent, source_agent, target_agent, kind, event, content, timestamp):
            ...     return {'event': event, 'content': content}
            >>> reducer.add_reduction_rule('my_event', my_rule)
        """
        if trigger in self.rules:
            raise Exception(f'Rule for {trigger} already exists.')

        self.rules[trigger] = reduction_func
        logger.info(f'Added reduction rule for trigger: {trigger}') # Логируем добавление правила

    def reduce_agent(self, agent: TinyPerson) -> list:
        """
        Выполняет редукцию эпизодической памяти агента на основе заданных правил.

        Args:
            agent (TinyPerson): Агент, эпизодическая память которого нужно редуцировать.

        Returns:
            list: Список результатов редукции.
        """
        reduction: List = []
        for message in agent.episodic_memory.retrieve_all():
            if message['role'] == 'system':
                continue  # doing nothing for `system` role yet at least

            elif message['role'] == 'user':
                # User role is related to stimuli only
                stimulus_type: str = message['content']['stimuli'][0]['type']
                stimulus_content: str = message['content']['stimuli'][0]['content']
                stimulus_source: str = message['content']['stimuli'][0]['source']
                stimulus_timestamp: str = message['simulation_timestamp']

                if stimulus_type in self.rules:
                    try:
                        extracted = self.rules[stimulus_type](
                            focus_agent=agent,
                            source_agent=TinyPerson.get_agent_by_name(stimulus_source),
                            target_agent=agent,
                            kind='stimulus',
                            event=stimulus_type,
                            content=stimulus_content,
                            timestamp=stimulus_timestamp,
                        )
                        if extracted is not None:
                            reduction.append(extracted)
                    except Exception as ex:
                        logger.error(f'Error while applying rule for stimulus type: {stimulus_type}', ex, exc_info=True) # Логируем ошибку

            elif message['role'] == 'assistant':
                # Assistant role is related to actions only
                if 'action' in message['content']:
                    action_type: str = message['content']['action']['type']
                    action_content: str = message['content']['action']['content']
                    action_target: str = message['content']['action']['target']
                    action_timestamp: str = message['simulation_timestamp']

                    if action_type in self.rules:
                        try:
                            extracted = self.rules[action_type](
                                focus_agent=agent,
                                source_agent=agent,
                                target_agent=TinyPerson.get_agent_by_name(action_target),
                                kind='action',
                                event=action_type,
                                content=action_content,
                                timestamp=action_timestamp,
                            )
                            if extracted is not None:
                                reduction.append(extracted)
                        except Exception as ex:
                            logger.error(f'Error while applying rule for action type: {action_type}', ex, exc_info=True) # Логируем ошибку

        return reduction

    def reduce_agent_to_dataframe(self, agent: TinyPerson, column_names: Optional[list] = None) -> pd.DataFrame:
        """
        Редуцирует эпизодическую память агента и преобразует результаты в DataFrame.

        Args:
            agent (TinyPerson): Агент, эпизодическая память которого нужно редуцировать.
            column_names (Optional[list], optional): Список названий столбцов для DataFrame. По умолчанию None.

        Returns:
            pd.DataFrame: DataFrame с результатами редукции.
        """
        reduction: List = self.reduce_agent(agent)
        return pd.DataFrame(reduction, columns=column_names)
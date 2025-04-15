### **Анализ кода модуля `results_reducer.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код структурирован в класс `ResultsReducer`, что способствует организации и повторному использованию.
    - Присутствует логика для обработки различных типов сообщений (`system`, `user`, `assistant`) от агентов.
    - Реализована возможность добавления правил обработки (`reduction_rule`) для разных типов стимулов и действий.
- **Минусы**:
    - Отсутствует docstring для класса `ResultsReducer` и метода `__init__`.
    - Не указаны типы для параметров `func` в `add_reduction_rule`, `column_names` в `reduce_agent_to_dataframe`.
    - В блоках `if` и `elif` повторяется код извлечения данных из `message['content']`.
    - Обработка исключений отсутствует, что может привести к непредсказуемому поведению при возникновении ошибок.
    - Жестко заданы ключи `'role'`, `'content'`, `'stimuli'`, `'type'`, `'source'`, `'simulation_timestamp'`, `'action'`, `'target'` в словарях, что делает код менее гибким.
    - Использование `TinyPerson.get_agent_by_name` внутри циклов может негативно сказаться на производительности, особенно если агентов много.

#### **Рекомендации по улучшению**:

1.  **Добавить docstring для класса и методов**:

    *   Для класса `ResultsReducer` добавить общее описание его назначения.
    *   Для метода `__init__` добавить описание инициализации атрибутов класса.
    *   Для всех остальных методов добавить подробные docstring с описанием аргументов, возвращаемых значений и возможных исключений.

2.  **Указать типы для параметров**:

    *   В методе `add_reduction_rule` указать тип для параметра `func` как `Callable`.
    *   В методе `reduce_agent_to_dataframe` указать тип для параметра `column_names` как `Optional[List[str]]`.

3.  **Рефакторинг извлечения данных**:

    *   Создать отдельные функции для извлечения данных из сообщений разных типов (`user`, `assistant`). Это позволит избежать повторения кода и сделает код более читаемым.

4.  **Обработка исключений**:

    *   Добавить блоки `try...except` для обработки возможных исключений, например, при обращении к несуществующим ключам в словарях или при вызове `TinyPerson.get_agent_by_name` с несуществующим именем агента.
    *   Использовать `logger.error` для логирования ошибок с предоставлением информации об исключении.

5.  **Гибкость структуры данных**:

    *   Использовать константы или переменные для хранения ключей, используемых для доступа к данным в словарях. Это позволит легко изменять структуру данных в будущем, не затрагивая основную логику кода.

6.  **Оптимизация производительности**:

    *   Если возможно, предварительно получить список имен агентов и использовать его для поиска агентов по имени, чтобы избежать многократного вызова `TinyPerson.get_agent_by_name` в цикле.

7.  **Аннотации типов**:

    *   Добавить аннотации типов для всех переменных.

#### **Оптимизированный код**:

```python
import pandas as pd
from typing import Callable, Optional, List, Dict, Any

from src.logger import logger # Импорт модуля logger
from tinytroupe.agent import TinyPerson

class ResultsReducer:
    """
    Класс для сведения результатов работы агентов TinyTroupe.

    Предоставляет функциональность для сведения данных из эпизодической памяти агентов на основе заданных правил.
    """

    def __init__(self) -> None:
        """
        Инициализирует экземпляр класса ResultsReducer.

        Создает пустые словари для хранения результатов и правил сведения.
        """
        self.results: Dict[Any, Any] = {}
        self.rules: Dict[str, Callable] = {}

    def add_reduction_rule(self, trigger: str, func: Callable) -> None:
        """
        Добавляет правило сведения для определенного типа стимула или действия.

        Args:
            trigger (str): Тип стимула или действия, для которого добавляется правило.
            func (Callable): Функция, выполняющая сведение данных.

        Raises:
            Exception: Если правило для указанного типа стимула или действия уже существует.
        """
        if trigger in self.rules:
            raise Exception(f'Rule for {trigger} already exists.')

        self.rules[trigger] = func

    def _extract_stimulus_data(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Извлекает данные о стимуле из сообщения.

        Args:
            message (Dict[str, Any]): Сообщение, содержащее информацию о стимуле.

        Returns:
            Dict[str, Any]: Словарь с извлеченными данными о стимуле.
        """
        stimulus_type: str = message['content']['stimuli'][0]['type']
        stimulus_content: Any = message['content']['stimuli'][0]['content']
        stimulus_source: str = message['content']['stimuli'][0]['source']
        stimulus_timestamp: Any = message['simulation_timestamp']

        return {
            'type': stimulus_type,
            'content': stimulus_content,
            'source': stimulus_source,
            'timestamp': stimulus_timestamp
        }

    def _extract_action_data(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Извлекает данные о действии из сообщения.

        Args:
            message (Dict[str, Any]): Сообщение, содержащее информацию о действии.

        Returns:
            Dict[str, Any]: Словарь с извлеченными данными о действии.
        """
        action_type: str = message['content']['action']['type']
        action_content: Any = message['content']['action']['content']
        action_target: str = message['content']['action']['target']
        action_timestamp: Any = message['simulation_timestamp']

        return {
            'type': action_type,
            'content': action_content,
            'target': action_target,
            'timestamp': action_timestamp
        }

    def reduce_agent(self, agent: TinyPerson) -> list:
        """
        Сводит данные из эпизодической памяти агента на основе заданных правил.

        Args:
            agent (TinyPerson): Агент, данные которого необходимо свести.

        Returns:
            list: Список результатов сведения данных.
        """
        reduction: List[Any] = []
        for message in agent.episodic_memory.retrieve_all():
            try:
                if message['role'] == 'system':
                    continue  # doing nothing for `system` role yet at least

                elif message['role'] == 'user':
                    # User role is related to stimuli only
                    stimulus_data = self._extract_stimulus_data(message)
                    stimulus_type = stimulus_data['type']
                    stimulus_content = stimulus_data['content']
                    stimulus_source = stimulus_data['source']
                    stimulus_timestamp = stimulus_data['timestamp']

                    if stimulus_type in self.rules:
                        extracted = self.rules[stimulus_type](
                            focus_agent=agent,
                            source_agent=TinyPerson.get_agent_by_name(stimulus_source),
                            target_agent=agent,
                            kind='stimulus',
                            event=stimulus_type,
                            content=stimulus_content,
                            timestamp=stimulus_timestamp
                        )
                        if extracted is not None:
                            reduction.append(extracted)

                elif message['role'] == 'assistant':
                    # Assistant role is related to actions only
                    if 'action' in message['content']:
                        action_data = self._extract_action_data(message)
                        action_type = action_data['type']
                        action_content = action_data['content']
                        action_target = action_data['target']
                        action_timestamp = action_data['timestamp']

                        if action_type in self.rules:
                            extracted = self.rules[action_type](
                                focus_agent=agent,
                                source_agent=agent,
                                target_agent=TinyPerson.get_agent_by_name(action_target),
                                kind='action',
                                event=action_type,
                                content=action_content,
                                timestamp=action_timestamp
                            )
                            if extracted is not None:
                                reduction.append(extracted)
            except KeyError as ex:
                logger.error(f'KeyError while processing message: {ex}', exc_info=True)
            except Exception as ex:
                logger.error(f'Error while processing message: {ex}', exc_info=True)

        return reduction

    def reduce_agent_to_dataframe(self, agent: TinyPerson, column_names: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Сводит данные из эпизодической памяти агента в DataFrame.

        Args:
            agent (TinyPerson): Агент, данные которого необходимо свести.
            column_names (Optional[List[str]], optional): Список названий столбцов для DataFrame. По умолчанию None.

        Returns:
            pd.DataFrame: DataFrame с результатами сведения данных.
        """
        reduction = self.reduce_agent(agent)
        return pd.DataFrame(reduction, columns=column_names)
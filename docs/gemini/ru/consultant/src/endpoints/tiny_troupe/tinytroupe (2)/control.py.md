### **Анализ кода модуля `control.py`**

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код разбит на логические блоки, что облегчает понимание структуры.
    - Присутствует базовая структура кэширования.
    - Используется логирование.
- **Минусы**:
    - Отсутствуют аннотации типов для переменных и параметров функций.
    - Не все функции и классы имеют подробные docstring.
    - В некоторых местах используется `print` вместо `logger`.
    - Не везде обрабатываются исключения с использованием `logger.error`.
    - Встречаются устаревшие конструкции, которые можно улучшить.
    - Есть закомментированный код.
    - Не используется `j_loads` для загрузки json.

**Рекомендации по улучшению:**

1.  **Добавить docstring**:
    - Добавить docstring во все классы и функции, описывающие их назначение, параметры, возвращаемые значения и возможные исключения.
    - Перевести docstring на русский язык.
2.  **Аннотации типов**:
    - Добавить аннотации типов для всех переменных и параметров функций для повышения читаемости и облегчения отладки.
3.  **Логирование**:
    - Заменить все `print` на `logger.info` или `logger.debug` в зависимости от уровня важности сообщения.
    - Обернуть потенциально проблемные участки кода в блоки `try...except` и логировать ошибки с использованием `logger.error(e, exc_info=True)`.
4.  **Кэширование**:
    - Рассмотреть возможность использования более эффективных структур данных для кэширования.
5.  **Обработка исключений**:
    - Улучшить обработку исключений, чтобы предоставлять более информативные сообщения об ошибках.
    - Использовать `ex` вместо `e` в блоках `except`.
6.  **Удалить неиспользуемый код**:
    - Удалить закомментированный код.
7.  **Использовать `j_loads`**:
    - Использовать `j_loads` для загрузки json.
8.  **Улучшение стиля кода**:
    - Использовать консистентный стиль кавычек (одинарные).

**Оптимизированный код:**

```python
"""
Модуль для управления моделированием.
=====================================

Модуль содержит класс :class:`Simulation`, который используется для управления симуляциями,
включая кэширование и обработку транзакций.

Пример использования
----------------------

>>> simulation = Simulation(id='my_simulation')
>>> simulation.begin()
>>> # ... выполнение действий в симуляции ...
>>> simulation.end()
"""
import json
import os
import tempfile
from typing import Optional, List, Dict, Any, Tuple

import tinytroupe
import tinytroupe.utils as utils
from src.logger import logger

class Simulation:
    """
    Управляет симуляцией, включая кэширование и обработку транзакций.
    """

    STATUS_STOPPED: str = 'stopped'
    """Статус остановленной симуляции."""
    STATUS_STARTED: str = 'started'
    """Статус запущенной симуляции."""

    def __init__(self, id: str = 'default', cached_trace: Optional[List[Tuple[Any, Any, Any, Dict[str, Any]]]] = None) -> None:
        """
        Инициализирует объект симуляции.

        Args:
            id (str, optional): Уникальный идентификатор симуляции. По умолчанию 'default'.
            cached_trace (Optional[List[Tuple[Any, Any, Any, Dict[str, Any]]]], optional): Кэшированный след симуляции. По умолчанию None.
        """
        self.id: str = id

        self.agents: List[Any] = []
        """Список агентов в симуляции."""
        self.name_to_agent: Dict[str, Any] = {}  # {agent_name: agent, ...}
        """Словарь для быстрого доступа к агентам по имени."""

        self.environments: List[Any] = []
        """Список окружений в симуляции."""

        self.factories: List[Any] = []  # e.g., TinyPersonFactory instances
        """Список фабрик в симуляции."""
        self.name_to_factory: Dict[str, Any] = {}  # {factory_name: factory, ...}
        """Словарь для быстрого доступа к фабрикам по имени."""

        self.name_to_environment: Dict[str, Any] = {}  # {environment_name: environment, ...}
        """Словарь для быстрого доступа к окружениям по имени."""
        self.status: str = Simulation.STATUS_STOPPED
        """Статус симуляции (запущена или остановлена)."""

        self.cache_path: str = f'./tinytroupe-{id}.cache.json'  # default cache path
        """Путь к файлу кэша."""

        self.auto_checkpoint: bool = False
        """Автоматически создавать чекпоинты после каждой транзакции."""

        self.has_unsaved_cache_changes: bool = False
        """Флаг, указывающий на наличие несохраненных изменений в кэше."""

        self._under_transaction: bool = False
        """Флаг, указывающий на то, что симуляция находится в транзакции."""

        if cached_trace is None:
            self.cached_trace: List[Tuple[Any, Any, Any, Dict[str, Any]]] = []
        else:
            self.cached_trace: List[Tuple[Any, Any, Any, Dict[str, Any]]] = cached_trace

        self.cache_misses: int = 0
        """Количество промахов кэша."""
        self.cache_hits: int = 0
        """Количество попаданий в кэш."""

        self.execution_trace: List[Any] = []
        """Список выполненных состояний."""

    def begin(self, cache_path: Optional[str] = None, auto_checkpoint: bool = False) -> None:
        """
        Начинает контролируемую симуляцию.

        Args:
            cache_path (str, optional): Путь к файлу кэша. Если не указан, используется путь по умолчанию.
            auto_checkpoint (bool, optional): Автоматически создавать чекпоинты после каждой транзакции. По умолчанию False.

        Raises:
            ValueError: Если симуляция уже запущена.
        """

        logger.debug(f'Starting simulation, cache_path={cache_path}, auto_checkpoint={auto_checkpoint}.')

        # local import to avoid circular dependencies
        from tinytroupe.agent import TinyPerson
        from tinytroupe.environment import TinyWorld
        from tinytroupe.factory.tiny_factory import TinyFactory

        if self.status == Simulation.STATUS_STOPPED:
            self.status: str = Simulation.STATUS_STARTED
        else:
            raise ValueError('Simulation is already started.')

        if cache_path is not None:
            self.cache_path: str = cache_path

        self.auto_checkpoint: bool = auto_checkpoint

        TinyPerson.clear_agents()
        TinyWorld.clear_environments()
        TinyFactory.clear_factories()

        utils.reset_fresh_id()

        if self.cache_path is not None:
            self._load_cache_file(self.cache_path)

    def end(self) -> None:
        """
        Завершает контролируемую симуляцию.

        Raises:
            ValueError: Если симуляция уже остановлена.
        """
        logger.debug('Ending simulation.')
        if self.status == Simulation.STATUS_STARTED:
            self.status: str = Simulation.STATUS_STOPPED
            self.checkpoint()
        else:
            raise ValueError('Simulation is already stopped.')

    def checkpoint(self) -> None:
        """
        Сохраняет текущее состояние симуляции в файл.
        """
        logger.debug('Checkpointing simulation state.')
        if self.has_unsaved_cache_changes:
            self._save_cache_file(self.cache_path)
        else:
            logger.debug('No unsaved cache changes to save to file.')

    def add_agent(self, agent: Any) -> None:
        """
        Добавляет агента в симуляцию.

        Args:
            agent: Агент для добавления.

        Raises:
            ValueError: Если имя агента уже существует.
        """
        if agent.name in self.name_to_agent:
            raise ValueError(f'Agent names must be unique, but \'{agent.name}\' is already defined.')
        agent.simulation_id: str = self.id
        self.agents.append(agent)
        self.name_to_agent[agent.name]: Any = agent

    def add_environment(self, environment: Any) -> None:
        """
        Добавляет окружение в симуляцию.

        Args:
            environment: Окружение для добавления.

        Raises:
            ValueError: Если имя окружения уже существует.
        """
        if environment.name in self.name_to_environment:
            raise ValueError(f'Environment names must be unique, but \'{environment.name}\' is already defined.')
        environment.simulation_id: str = self.id
        self.environments.append(environment)
        self.name_to_environment[environment.name]: Any = environment

    def add_factory(self, factory: Any) -> None:
        """
        Добавляет фабрику в симуляцию.

        Args:
            factory: Фабрика для добавления.

        Raises:
            ValueError: Если имя фабрики уже существует.
        """
        if factory.name in self.name_to_factory:
            raise ValueError(f'Factory names must be unique, but \'{factory.name}\' is already defined.')
        factory.simulation_id: str = self.id
        self.factories.append(factory)
        self.name_to_factory[factory.name]: Any = factory

    ###################################################################################################
    # Cache and execution chain mechanisms
    ###################################################################################################
    def _execution_trace_position(self) -> int:
        """
        Возвращает текущую позицию в трассе выполнения или -1, если трасса пуста.

        Returns:
            int: Текущая позиция в трассе выполнения.
        """
        return len(self.execution_trace) - 1

    def _function_call_hash(self, function_name: str, *args: Any, **kwargs: Any) -> str:
        """
        Вычисляет хэш для данного вызова функции.

        Args:
            function_name (str): Имя функции.
            *args: Аргументы функции.
            **kwargs: Ключевые аргументы функции.

        Returns:
            str: Хэш вызова функции.
        """
        event: str = str((function_name, args, kwargs))
        return event

    def _skip_execution_with_cache(self) -> None:
        """
        Пропускает текущее выполнение, предполагая наличие кэшированного состояния в той же позиции.

        Raises:
            AssertionError: Если нет кэшированного состояния в текущей позиции выполнения.
        """
        assert len(self.cached_trace) > self._execution_trace_position() + 1, 'There\'s no cached state at the current execution position.'

        self.execution_trace.append(self.cached_trace[self._execution_trace_position() + 1])

    def _is_transaction_event_cached(self, event_hash: str) -> bool:
        """
        Проверяет, соответствует ли данный хэш события соответствующему кэшированному хэшу, если таковой имеется.
        Если соответствующего кэшированного состояния нет, возвращает True.

        Args:
            event_hash (str): Хэш события.

        Returns:
            bool: True, если событие кэшировано или нет кэша для использования, иначе False.

        Raises:
            ValueError: Если позиция трассы выполнения недопустима.
        """
        # there's cache that could be used
        if len(self.cached_trace) > self._execution_trace_position() + 1:
            if self._execution_trace_position() >= -1:
                # here's a graphical depiction of the logic:
                #
                # Cache:         c0:(c_prev_node_hash_0, c_event_hash_0, _,  c_state_0) ------------------> c1:(c_prev_node_hash_1, c_event_hash_1,  _,  c_state_1) -> ...
                # Execution:     e0:(e_prev_node_hash_0, e_event_hash_0, _,  e_state_0) -<being computed>-> e1:(e_prev_node_hash_1, <being computed>, <being computed>, <being computed>)
                #   position = 0 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                #
                #   Must satisfy:
                #     - event_hash == c_event_hash_1
                #     - hash(e0) == c_prev_node_hash_1
                event_hash_match: bool = event_hash == self.cached_trace[self._execution_trace_position() + 1][1]
                prev_node_match: bool = True

                return event_hash_match and prev_node_match

            else:
                raise ValueError('Execution trace position is invalid, must be >= -1, but is ', self._execution_trace_position())

        else:  # no cache to use
            return False

    def _drop_cached_trace_suffix(self) -> None:
        """
        Удаляет суффикс кэшированной трассы, начиная с текущей позиции трассы выполнения.
        Это эффективно обновляет кэш до текущего состояния выполнения и начинает строить новый кэш с этого места.
        """
        self.cached_trace: List[Tuple[Any, Any, Any, Dict[str, Any]]] = self.cached_trace[:self._execution_trace_position() + 1]

    def _add_to_execution_trace(self, state: Dict[str, Any], event_hash: str, event_output: Any) -> None:
        """
        Добавляет состояние в список execution_trace и вычисляет соответствующий хэш.
        Вычисленный хэш сравнивается с хэшем кэшированной трассы в той же позиции,
        и если они не совпадают, выполнение прерывается. Аналогично, event_hash сравнивается
        с хэшем события в кэшированной трассе в той же позиции, и если они не совпадают, выполнение
        прерывается.

        Args:
            state (dict): Текущее состояние симуляции.
            event_hash (str): Хэш события.
            event_output: Выходные данные события.
        """

        # Compute the hash of the previous execution pair, if any
        previous_hash: None = None

        # Create a tuple of (hash, state) and append it to the execution_trace list
        self.execution_trace.append((previous_hash, event_hash, event_output, state))

    def _add_to_cache_trace(self, state: Dict[str, Any], event_hash: str, event_output: Any) -> None:
        """
        Добавляет состояние в список cached_trace и вычисляет соответствующий хэш.

        Args:
            state (dict): Текущее состояние симуляции.
            event_hash (str): Хэш события.
            event_output: Выходные данные события.
        """
        # Compute the hash of the previous cached pair, if any
        previous_hash: Optional[str] = None
        if self.cached_trace:
            previous_hash: str = utils.custom_hash(self.cached_trace[-1])

        # Create a tuple of (hash, state) and append it to the cached_trace list
        self.cached_trace.append((previous_hash, event_hash, event_output, state))

        self.has_unsaved_cache_changes: bool = True

    def _load_cache_file(self, cache_path: str) -> None:
        """
        Загружает файл кэша из данного пути.

        Args:
            cache_path (str): Путь к файлу кэша.
        """
        try:
            with open(cache_path, 'r') as f: # Открываем файл для чтения
                self.cached_trace: List[Tuple[Any, Any, Any, Dict[str, Any]]] = json.load(f) # Преобразуем содержимое файла в структуру данных Python
        except FileNotFoundError:
            logger.info(f'Cache file not found on path: {cache_path}.')
            self.cached_trace: List[Tuple[Any, Any, Any, Dict[str, Any]]] = []

    def _save_cache_file(self, cache_path: str) -> None:
        """
        Сохраняет файл кэша в данный путь. Всегда перезаписывает.

        Args:
            cache_path (str): Путь для сохранения файла кэша.
        """
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile('w', delete=False) as temp: # Создаем временный файл для записи
                json.dump(self.cached_trace, temp, indent=4) # Записываем данные в формате JSON во временный файл

            # Replace the original file with the temporary file
            os.replace(temp.name, cache_path) # Заменяем исходный файл временным файлом
        except Exception as ex:
            logger.error(f'An error occurred while saving cache to {cache_path}: {ex}', exc_info=True) # Логируем ошибку

        self.has_unsaved_cache_changes: bool = False

    ###################################################################################################
    # Transactional control
    ###################################################################################################

    def begin_transaction(self) -> None:
        """
        Начинает транзакцию.
        """
        self._under_transaction: bool = True
        self._clear_communications_buffers()  # TODO <----------------------------------------------------------------

    def end_transaction(self) -> None:
        """
        Завершает транзакцию.
        """
        self._under_transaction: bool = False

    def is_under_transaction(self) -> bool:
        """
        Проверяет, находится ли агент в транзакции.

        Returns:
            bool: True, если агент находится в транзакции, иначе False.
        """
        return self._under_transaction

    def _clear_communications_buffers(self) -> None:
        """
        Очищает буферы связи всех агентов и сред.
        """
        for agent in self.agents:
            agent.clear_communications_buffer()

        for environment in self.environments:
            environment.clear_communications_buffer()
    ###################################################################################################
    # Simulation state handling
    ###################################################################################################

    def _encode_simulation_state(self) -> Dict[str, Any]:
        """
        Кодирует текущее состояние симуляции, включая агентов, среды и другую
        соответствующую информацию.

        Returns:
            dict: Закодированное состояние симуляции.
        """
        state: Dict[str, Any] = {}

        # Encode agents
        state['agents']: List[Any] = []
        for agent in self.agents:
            state['agents'].append(agent.encode_complete_state())

        # Encode environments
        state['environments']: List[Any] = []
        for environment in self.environments:
            state['environments'].append(environment.encode_complete_state())

        # Encode factories
        state['factories']: List[Any] = []
        for factory in self.factories:
            state['factories'].append(factory.encode_complete_state())

        return state

    def _decode_simulation_state(self, state: Dict[str, Any]) -> None:
        """
        Декодирует данное состояние симуляции, включая агентов, среды и другую
        соответствующую информацию.

        Args:
            state (dict): Состояние для декодирования.
        """
        # local import to avoid circular dependencies
        from tinytroupe.agent import TinyPerson
        from tinytroupe.environment import TinyWorld

        logger.debug(f'Decoding simulation state: {state["factories"]}')
        logger.debug(f'Registered factories: {self.name_to_factory}')
        logger.debug(f'Registered agents: {self.name_to_agent}')
        logger.debug(f'Registered environments: {self.name_to_environment}')

        # Decode factories
        for factory_state in state['factories']:
            factory = self.name_to_factory[factory_state['name']]
            factory.decode_complete_state(factory_state)

        # Decode environments
        for environment_state in state['environments']:
            try:
                environment = self.name_to_environment[environment_state['name']]
                environment.decode_complete_state(environment_state)
                if TinyWorld.communication_display:
                    environment.pop_and_display_latest_communications()

            except Exception as ex:
                raise ValueError(f'Environment {environment_state["name"]} is not in the simulation, thus cannot be decoded there.') from ex

        # Decode agents (if they were not already decoded by the environment)
        for agent_state in state['agents']:
            try:
                agent = self.name_to_agent[agent_state['name']]
                agent.decode_complete_state(agent_state)

                # The agent has not yet been decoded because it is not in any environment. So, decode it.
                if agent.environment is None:
                    if TinyPerson.communication_display:
                        agent.pop_and_display_latest_communications()
            except Exception as ex:
                raise ValueError(f'Agent {agent_state["name"]} is not in the simulation, thus cannot be decoded there.') from ex


class Transaction:
    """
    Класс, представляющий транзакцию в симуляции.
    """

    def __init__(self, obj_under_transaction: Any, simulation: Optional[Simulation], function: Any, *args: Any, **kwargs: Any) -> None:
        """
        Инициализирует объект транзакции.

        Args:
            obj_under_transaction: Объект, находящийся под транзакцией.
            simulation (Optional[Simulation]): Симуляция, в которой выполняется транзакция.
            function: Функция, выполняемая в транзакции.
            *args: Аргументы функции.
            **kwargs: Ключевые аргументы функции.

        Raises:
            ValueError: Если объект уже захвачен другой симуляцией или не является экземпляром TinyPerson или TinyWorld.
        """
        # local import to avoid circular dependencies
        from tinytroupe.agent import TinyPerson
        from tinytroupe.environment import TinyWorld
        from tinytroupe.factory.tiny_factory import TinyFactory

        self.obj_under_transaction: Any = obj_under_transaction
        """Объект, над которым выполняется транзакция."""
        self.simulation: Optional[Simulation] = simulation
        """Симуляция, в которой выполняется транзакция."""
        self.function_name: str = function.__name__
        """Имя функции, выполняемой в транзакции."""
        self.function: Any = function
        """Функция, выполняемая в транзакции."""
        self.args: Any = args
        """Аргументы функции."""
        self.kwargs: Any = kwargs
        """Ключевые аргументы функции."""

        #
        # If we have an ongoing simulation, set the simulation id of the object under transaction if it is not already set.
        #
        if simulation is not None:
            if hasattr(obj_under_transaction, 'simulation_id') and obj_under_transaction.simulation_id is not None:
                if obj_under_transaction.simulation_id != simulation.id:
                    raise ValueError(f'Object {obj_under_transaction} is already captured by a different simulation (id={obj_under_transaction.simulation_id}), \
                                    and cannot be captured by simulation id={simulation.id}.')

                logger.debug(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Object {obj_under_transaction} is already captured by simulation {simulation.id}.')
            else:
                # if is a TinyPerson, add the agent to the simulation
                if isinstance(obj_under_transaction, TinyPerson):
                    simulation.add_agent(obj_under_transaction)
                    logger.debug(f'>>>>>>>>>>>>>>>>>>>>>> Added agent {obj_under_transaction} to simulation {simulation.id}.')

                # if is a TinyWorld, add the environment to the simulation
                elif isinstance(obj_under_transaction, TinyWorld):
                    simulation.add_environment(obj_under_transaction)

                # if is a TinyFactory, add the factory to the simulation
                elif isinstance(obj_under_transaction, TinyFactory):
                    simulation.add_factory(obj_under_transaction)
                    logger.debug(f'>>>>>>>>>>>>>>>>>>>>>> Added factory {obj_under_transaction} to simulation {simulation.id}.')

                else:
                    raise ValueError(f'Object {obj_under_transaction} (type = {type(obj_under_transaction)}) is not a TinyPerson or TinyWorld instance, and cannot be captured by the simulation.')

    def execute(self) -> Any:
        """
        Выполняет транзакцию.

        Returns:
            Any: Результат выполнения функции.

        Raises:
            ValueError: Если статус симуляции недопустим.
        """

        output: Any = None

        # Transaction caching will only operate if there is a simulation and it is started
        if self.simulation is None or self.simulation.status == Simulation.STATUS_STOPPED:
            # Compute the function and return it, no caching, since the simulation is not started
            output = self.function(*self.args, **self.kwargs)

        elif self.simulation.status == Simulation.STATUS_STARTED:
            # Compute the event hash
            event_hash: str = self.simulation._function_call_hash(self.function_name, *self.args, **self.kwargs)

            # Check if the event hash is in the cache
            if self.simulation._is_transaction_event_cached(event_hash):
                self.simulation.cache_hits += 1

                # Restore the full state and return the cached output
                logger.info(f'Skipping execution of {self.function_name} with args {self.args} and kwargs {self.kwargs} because it is already cached.')

                self.simulation._skip_execution_with_cache()
                state: Dict[str, Any] = self.simulation.cached_trace[self.simulation._execution_trace_position()][3]  # state
                self.simulation._decode_simulation_state(state)

                # Output encoding/decoding is used to preserve references to TinyPerson and TinyWorld instances
                # mainly. Scalar values (int, float, str, bool) and composite values (list, dict) are
                # encoded/decoded as is.
                encoded_output: Any = self.simulation.cached_trace[self.simulation._execution_trace_position()][2]  # output
                output = self._decode_function_output(encoded_output)

            else:  # not cached
                self.simulation.cache_misses += 1

                # reentrant transactions are not cached, since what matters is the final result of
                # the top-level transaction
                if not self.simulation.is_under_transaction():
                    self.simulation.begin_transaction()

                    # immediately drop the cached trace suffix, since we are starting a new execution from this point on
                    self.simulation._drop_cached_trace_suffix()

                    # Compute the function, cache the result and return it
                    output = self.function(*self.args, **self.kwargs)

                    encoded_output: Dict[str, Any] = self._encode_function_output(output)
                    state: Dict[str, Any] = self.simulation._encode_simulation_state()

                    self.simulation._add_to_cache_trace(state, event_hash, encoded_output)
                    self.simulation._add_to_execution_trace(state, event_hash, encoded_output)

                    self.simulation.end_transaction()

                else:  # reentrant transactions are just run, but not cached
                    output = self.function(*self.args, **self.kwargs)
        else:
            raise ValueError(f'Simulation status is invalid at this point: {self.simulation.status}')

        # Checkpoint if needed
        if self.simulation is not None and self.simulation.auto_checkpoint:
            self.simulation.checkpoint()

        return output

    def _encode_function_output(self, output: Any) -> Dict[str, Any]:
        """
        Кодирует данные функции.

        Args:
            output: Выходные данные функции.

        Returns:
            dict: Закодированные выходные данные функции.
        """
        # local import to avoid circular dependencies
        from tinytroupe.agent import TinyPerson
        from tinytroupe.environment import TinyWorld
        from tinytroupe.factory.tiny_factory import TinyFactory

        # if the output is a TinyPerson, encode it
        if output is None:
            return None
        elif isinstance(output, TinyPerson):
            return {'type': 'TinyPersonRef', 'name': output.name}
        # if it is a TinyWorld, encode it
        elif isinstance(output, TinyWorld):
            return {'type': 'TinyWorldRef', 'name': output.name}
        # if it is a TinyFactory, encode it
        elif isinstance(output, TinyFactory):
            return {'type': 'TinyFactoryRef', 'name': output.name}
        # if it is one of the types supported by JSON, encode it as is
        elif isinstance(output, (int, float, str, bool, list, dict, tuple)):
            return {'type': 'JSON', 'value': output}
        # otherwise, raise an exception
        else:
            raise ValueError(f'Unsupported output type: {type(output)}')

    def _decode_function_output(self, encoded_output: Dict[str, Any]) -> Any:
        """
        Декодирует закодированные данные функции.

        Args:
            encoded_output (dict): Закодированные выходные данные функции.

        Returns:
            Any: Декодированные выходные данные функции.
        """
        # local import to avoid circular dependencies
        from tinytroupe.agent import TinyPerson
        from tinytroupe.environment import TinyWorld
        from tinytroupe.factory.tiny_factory import TinyFactory

        if encoded_output is None:
            return None
        elif encoded_output['type'] == 'TinyPersonRef':
            return TinyPerson.get_agent_by_name(encoded_output['name'])
        elif encoded_output['type'] == 'TinyWorldRef':
            return TinyWorld.get_environment_by_name(encoded_output['name'])
        elif encoded_output['type'] == 'TinyFactoryRef':
            return TinyFactory.get_factory_by_name(encoded_output['name'])
        elif encoded_output['type'] == 'JSON':
            return encoded_output['value']
        else:
            raise ValueError(f'Unsupported output type: {encoded_output["type"]}')


def transactional(func: Any) -> Any:
    """
    Декоратор, делающий функцию транзакционной.

    Args:
        func: Функция для декорирования.

    Returns:
        Any: Обернутая функция.
    """
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """
        Обертка для выполнения транзакции.

        Args:
            *args: Аргументы функции.
            **kwargs: Ключевые аргументы функции.

        Returns:
            Any: Результат выполнения функции.
        """
        obj_under_transaction: Any = args[0]
        simulation: Optional[Simulation] = current_simulation()
        obj_sim_id: Optional[str] = obj_under_transaction.simulation_id if hasattr(obj_under_transaction, 'simulation_id') else None

        logger.debug(f'-----------------------------------------> Transaction: {func.__name__} with args {args[1:]} and kwargs {kwargs} under simulation {obj_sim_id}.')

        transaction = Transaction(obj_under_transaction, simulation, func, *args, **kwargs)
        result: Any = transaction.execute()
        return result

    return wrapper


class SkipTransaction(Exception):
    """
    Исключение, указывающее на пропуск транзакции.
    """
    pass


class CacheOutOfSync(Exception):
    """
    Исключение, выбрасываемое, когда кэшированные и свежевыполненные элементы не синхронизированы.
    """
    pass


class ExecutionCached(Exception):
    """
    Исключение, выбрасываемое, когда предложенное выполнение уже кэшировано.
    """
    pass


###################################################################################################
# Convenience functions
###################################################################################################

_current_simulations: Dict[str, Optional[Simulation]] = {'default': None}
"""Словарь текущих симуляций."""
_current_simulation_id: Optional[str] = None
"""Идентификатор текущей симуляции."""

def reset() -> None:
    """
    Сбрасывает состояние управления симуляцией.
    """
    global _current_simulations, _current_simulation_id
    _current_simulations = {'default': None}

    # TODO Currently, only one simulation can be started at a time. In future versions, this should be
    #      changed to allow multiple simulations to be started at the same time, e.g., for fast
    #      analyses through parallelization.
    _current_simulation_id = None


def _simulation(id: str = 'default') -> Simulation:
    """
    Возвращает объект симуляции по идентификатору.

    Args:
        id (str, optional): Идентификатор симуляции. По умолчанию 'default'.

    Returns:
        Simulation: Объект симуляции.
    """
    global _current_simulations
    if _current_simulations[id] is None:
        _current_simulations[id] = Simulation()

    return _current_simulations[id]


def begin(cache_path: Optional
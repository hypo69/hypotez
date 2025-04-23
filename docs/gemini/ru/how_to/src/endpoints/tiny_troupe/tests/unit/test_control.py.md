### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода содержит набор тестов для проверки функциональности управления симуляциями в библиотеке `tinytroupe`. Он включает тесты для начала, создания контрольных точек и завершения симуляций с использованием различных компонентов, таких как агенты, виртуальные миры и фабрики персонажей.

Шаги выполнения
-------------------------
1. **`test_begin_checkpoint_end_with_agent_only(setup)`**:
   - Функция `remove_file_if_exists` удаляет файл `control_test.cache.json`, если он существует.
   - Функция `control.reset()` сбрасывает состояние управления симуляцией.
   - Проверяется, что текущая симуляция отсутствует.
   - Функция `control.begin("control_test.cache.json")` начинает новую симуляцию.
   - Создаются два агента (`agent_1` и `agent_2`) с использованием функций `create_oscar_the_architect()` и `create_lisa_the_data_scientist()`.
   - Агентам добавляются ментальные способности с помощью `tooluse_faculty`.
   - Определяются атрибуты агентов (`age`, `nationality`) с использованием метода `define`.
   - Функция `control.checkpoint()` создает контрольную точку симуляции.
   - Агенты взаимодействуют, вызывая метод `listen_and_act`.
   - Проверяется, что файл контрольной точки был создан.
   - Функция `control.end()` завершает симуляцию.

2. **`test_begin_checkpoint_end_with_world(setup)`**:
   - Функция `remove_file_if_exists` удаляет файл `control_test_world.cache.json`, если он существует.
   - Функция `control.reset()` сбрасывает состояние управления симуляцией.
   - Проверяется, что текущая симуляция отсутствует.
   - Функция `control.begin("control_test_world.cache.json")` начинает новую симуляцию.
   - Создается виртуальный мир (`world`) с двумя агентами.
   - Функция `world.make_everyone_accessible()` делает всех агентов доступными для взаимодействия.
   - Функция `world.run(2)` запускает симуляцию на два шага.
   - Функция `control.checkpoint()` создает контрольную точку симуляции.
   - Проверяется, что файл контрольной точки был создан.
   - Функция `control.end()` завершает симуляцию.

3. **`test_begin_checkpoint_end_with_factory(setup)`**:
   - Функция `remove_file_if_exists` удаляет файл `control_test_personfactory.cache.json`, если он существует.
   - Функция `control.reset()` сбрасывает состояние управления симуляцией.
   - Определяется вспомогательная функция `aux_simulation_to_repeat`, которая выполняет следующие действия:
     - Функция `control.reset()` сбрасывает состояние управления симуляцией.
     - Функция `control.begin("control_test_personfactory.cache.json")` начинает новую симуляцию.
     - Создается фабрика персонажей (`factory`) с использованием класса `TinyPersonFactory`.
     - Функция `factory.generate_person()` генерирует агента.
     - Функция `control.checkpoint()` создает контрольную точку симуляции.
     - Проверяется, что файл контрольной точки был создан.
     - Функция `control.end()` завершает симуляцию.
   - Выполняются две симуляции с использованием функции `aux_simulation_to_repeat`.
   - Проверяется, что количество промахов кэша равно нулю, а количество попаданий в кэш больше нуля.
   - Проверяется, что атрибуты агентов (возраст, национальность, мини-биография) одинаковы в обеих симуляциях.
   - Проверяется содержимое файла кэша на наличие определенных вызовов методов (`_aux_model_call`, `_setup_agent`).

Пример использования
-------------------------

```python
import pytest
import os
import sys
sys.path.append('../../tinytroupe/')
sys.path.append('../../')
sys.path.append('..')

from tinytroupe.examples import create_oscar_the_architect, create_lisa_the_data_scientist
from tinytroupe.agent import TinyPerson, TinyToolUse
from tinytroupe.environment import TinyWorld
from tinytroupe.control import Simulation
import tinytroupe.control as control
from tinytroupe.factory import TinyPersonFactory
from tinytroupe.enrichment import TinyEnricher
from tinytroupe.extraction import ArtifactExporter
from tinytroupe.tools import TinyWordProcessor

import logging
logger = logging.getLogger("tinytroupe")

import importlib

from testing_utils import *

def test_begin_checkpoint_end_with_agent_only(setup):
    # Функция удаляет файл, если он существует
    remove_file_if_exists("control_test.cache.json")

    control.reset()
    
    assert control._current_simulations["default"] is None, "There should be no simulation running at this point."

    # Функция удаляет файл, если он существует
    remove_file_if_exists("control_test.cache.json")

    control.begin("control_test.cache.json")
    assert control._current_simulations["default"].status == Simulation.STATUS_STARTED, "The simulation should be started at this point."


    exporter = ArtifactExporter(base_output_folder="./synthetic_data_exports_3/")
    enricher = TinyEnricher()
    tooluse_faculty = TinyToolUse(tools=[TinyWordProcessor(exporter=exporter, enricher=enricher)])

    agent_1 = create_oscar_the_architect()
    agent_1.add_mental_faculties([tooluse_faculty])
    agent_1.define("age", 19)
    agent_1.define("nationality", "Brazilian")

    agent_2 = create_lisa_the_data_scientist()
    agent_2.add_mental_faculties([tooluse_faculty])
    agent_2.define("age", 80)
    agent_2.define("nationality", "Argentinian")

    assert control._current_simulations["default"].cached_trace is not None, "There should be a cached trace at this point."
    assert control._current_simulations["default"].execution_trace is not None, "There should be an execution trace at this point."

    control.checkpoint()

    agent_1.listen_and_act("How are you doing?")
    agent_2.listen_and_act("What's up?")

    # Проверка существования файла
    assert os.path.exists("control_test.cache.json"), "The checkpoint file should have been created."

    control.end()

    assert control._current_simulations["default"].status == Simulation.STATUS_STOPPED, "The simulation should be ended at this point."
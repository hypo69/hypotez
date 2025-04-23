### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода содержит набор тестов для проверки функциональности класса `TinyWorld` и его взаимодействия с агентами. Он проверяет, как `TinyWorld` запускается, как агенты получают и обрабатывают сообщения, а также как сохраняется и восстанавливается состояние мира.

Шаги выполнения
-------------------------
1. **`test_run(setup, focus_group_world)`**:
   - Создает пустой мир (`world_1`) и запускает его на два шага. Это проверяет, что мир может функционировать без агентов.
   - Использует мир с агентами (`world_2`), предоставленный через фикстуру `focus_group_world`.
   - Отправляет сообщение всем агентам в `world_2` и запускает мир на два шага.
   - Проверяет целостность сообщений в памяти агентов: убеждается, что ни один агент не является целью действия в своих собственных сообщениях.

2. **`test_broadcast(setup, focus_group_world)`**:
   - Получает мир с агентами (`focus_group_world`).
   - Отправляет широковещательное сообщение всем агентам.
   - Проверяет, получили ли агенты сообщение, сравнивая содержимое первого сообщения в их памяти с отправленным сообщением.

3. **`test_encode_complete_state(setup, focus_group_world)`**:
   - Получает мир с агентами (`focus_group_world`).
   - Кодирует текущее состояние мира с помощью `encode_complete_state()`.
   - Проверяет, что закодированное состояние не равно `None`, содержит имя мира и список агентов.

4. **`test_decode_complete_state(setup, focus_group_world)`**:
   - Получает мир с агентами (`focus_group_world`).
   - Сохраняет имя мира и количество агентов.
   - Кодирует состояние мира.
   - Изменяет имя мира и очищает список агентов, чтобы имитировать повреждение данных.
   - Восстанавливает состояние мира из закодированного состояния с помощью `decode_complete_state()`.
   - Проверяет, что восстановленный мир не равен `None`, имеет исходное имя и содержит исходное количество агентов.

Пример использования
-------------------------

```python
import pytest
import logging
logger = logging.getLogger("tinytroupe")

import sys
sys.path.append('../../tinytroupe/')
sys.path.append('../../')
sys.path.append('..')

from tinytroupe.examples import create_lisa_the_data_scientist, create_oscar_the_architect, create_marcos_the_physician
from tinytroupe.environment import TinyWorld
from testing_utils import *

def test_run(setup, focus_group_world):
    # Тест проверяет запуск мира без агентов и с агентами, а также целостность сообщений.
    world_1 = TinyWorld("Empty land", [])   
    world_1.run(2)

    world_2 = focus_group_world
    world_2.broadcast("Discuss ideas for a new AI product you'd love to have.")
    world_2.run(2)

    for agent in world_2.agents:
        for msg in agent.episodic_memory.retrieve_all():
            if 'action' in msg['content'] and 'target' in msg['content']['action']:
                assert msg['content']['action']['target'] != agent.name, f"{agent.name} should not have any messages with itself as the target."

def test_broadcast(setup, focus_group_world):
    # Тест проверяет, что агенты получают широковещательные сообщения.
    world = focus_group_world
    world.broadcast("""
                Folks, we need to brainstorm ideas for a new baby product. Something moms have been asking for centuries and never got.

                Please start the discussion now.
                """)
    
    for agent in focus_group_world.agents:
        assert "Folks, we need to brainstorm" in agent.episodic_memory.retrieve_first(1)[0]['content']['stimuli'][0]['content'], f"{agent.name} should have received the message."

def test_encode_complete_state(setup, focus_group_world):
    # Тест проверяет кодирование состояния мира.
    world = focus_group_world

    state = world.encode_complete_state()
    
    assert state is not None, "The state should not be None."
    assert state['name'] == world.name, "The state should have the world name."
    assert state['agents'] is not None, "The state should have the agents."

def test_decode_complete_state(setup, focus_group_world):
    # Тест проверяет декодирование состояния мира.
    world = focus_group_world

    name_1 = world.name
    n_agents_1 = len(world.agents)

    state = world.encode_complete_state()
    
    world.name = "New name"
    world.agents = []

    world_2 = world.decode_complete_state(state)

    assert world_2 is not None, "The world should not be None."
    assert world_2.name == name_1, "The world should have the same name."
    assert len(world_2.agents) == n_agents_1, "The world should have the same number of agents."
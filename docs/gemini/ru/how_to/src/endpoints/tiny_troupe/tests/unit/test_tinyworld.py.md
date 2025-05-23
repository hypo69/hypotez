## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код представляет набор тестов для класса `TinyWorld`, который моделирует мир с агентами и взаимодействием между ними. 

Шаги выполнения
-------------------------
1. **Тестирование запуска мира:**
    - Создается пустой мир `world_1`.
    - Запускается мир `world_1` на два шага (`run(2)`).
    - Создается мир `world_2` с агентами.
    - В мир `world_2` рассылается сообщение `broadcast()`.
    - Запускается мир `world_2` на два шага (`run(2)`).
    - Проверяется целостность разговора:
        - Для каждого агента проверяется, что ни у одного из них нет сообщений с самим собой в качестве цели (`target`).
        - **TODO:**  Проверка целостности стимула.
2. **Тестирование рассылки сообщения:**
    - В мир `world` рассылается сообщение `broadcast()`.
    - Для каждого агента проверяется, что он получил сообщение.
3. **Тестирование кодирования полного состояния мира:**
    - Кодируется полное состояние мира `encode_complete_state()`.
    - Проверяется, что полученное состояние не равно `None`.
    - Проверяется, что состояние содержит имя мира `world.name`.
    - Проверяется, что состояние содержит агентов `world.agents`.
4. **Тестирование декодирования полного состояния мира:**
    - Кодируется полное состояние мира `encode_complete_state()`.
    - Изменяются имя и агенты мира.
    - Декодируется состояние обратно в мир `decode_complete_state()`.
    - Проверяется, что мир не равен `None`.
    - Проверяется, что мир имеет исходное имя.
    - Проверяется, что мир имеет исходное количество агентов.

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

@pytest.fixture
def focus_group_world():
    """Создает мир с несколькими агентами для тестирования."""
    agents = [
        create_lisa_the_data_scientist(),
        create_oscar_the_architect(),
        create_marcos_the_physician(),
    ]
    world = TinyWorld("Focus Group", agents)
    return world

@pytest.fixture
def setup():
    """Настройка тестов."""
    logging.basicConfig(level=logging.INFO)
    logger.info("Tests started.")

def test_run(setup, focus_group_world):

    # empty world
    world_1 = TinyWorld("Empty land", [])   
    world_1.run(2)

    # world with agents
    world_2 = focus_group_world
    world_2.broadcast("Discuss ideas for a new AI product you'd love to have.")
    world_2.run(2)

    # check integrity of conversation
    for agent in world_2.agents:
        for msg in agent.episodic_memory.retrieve_all():
            if 'action' in msg['content'] and 'target' in msg['content']['action']:
                assert msg['content']['action']['target'] != agent.name, f"{agent.name} should not have any messages with itself as the target."
            
            # TODO stimulus integrity check?
        
        
def test_broadcast(setup, focus_group_world):

    world = focus_group_world
    world.broadcast("""
                Folks, we need to brainstorm ideas for a new baby product. Something moms have been asking for centuries and never got.

                Please start the discussion now.
                """)
    
    for agent in focus_group_world.agents:
        # did the agents receive the message?
        assert "Folks, we need to brainstorm" in agent.episodic_memory.retrieve_first(1)[0]['content']['stimuli'][0]['content'], f"{agent.name} should have received the message."

def test_encode_complete_state(setup, focus_group_world):
    world = focus_group_world

    # encode the state
    state = world.encode_complete_state()
    
    assert state is not None, "The state should not be None."
    assert state['name'] == world.name, "The state should have the world name."
    assert state['agents'] is not None, "The state should have the agents."

def test_decode_complete_state(setup, focus_group_world):
    world = focus_group_world

    name_1 = world.name
    n_agents_1 = len(world.agents)

    # encode the state
    state = world.encode_complete_state()
    
    # screw up the world
    world.name = "New name"
    world.agents = []

    # decode the state back into the world
    world_2 = world.decode_complete_state(state)

    assert world_2 is not None, "The world should not be None."
    assert world_2.name == name_1, "The world should have the same name."
    assert len(world_2.agents) == n_agents_1, "The world should have the same number of agents."

```
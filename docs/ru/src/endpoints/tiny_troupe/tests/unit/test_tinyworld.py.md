# Модуль тестирования TinyWorld

## Обзор

Модуль `test_tinyworld.py` содержит юнит-тесты для проверки функциональности класса `TinyWorld` и связанных с ним компонентов. `TinyWorld` представляет собой окружение, в котором взаимодействуют агенты, и тесты проверяют корректность создания, запуска, взаимодействия агентов и сохранения/восстановления состояния мира.

## Подробней

Этот модуль предназначен для тестирования различных аспектов работы `TinyWorld`, включая:
- Запуск мира с агентами и без.
- Рассылку сообщений агентам.
- Кодирование и декодирование состояния мира.

Используются фикстуры `setup` и `focus_group_world`, определенные в `testing_utils.py`, для подготовки тестового окружения.

## Функции

### `test_run`

```python
def test_run(setup, focus_group_world):
    """
    Функция проверяет запуск мира с агентами и без агентов.

    Args:
        setup: Фикстура для начальной настройки.
        focus_group_world: Фикстура, представляющая мир с агентами.

    Raises:
        AssertionError: Если целевой агент указан как сам агент в сообщениях.

    Как работает функция:
        - Создает пустой мир (`world_1`) и запускает его на несколько шагов.
        - Создает мир с агентами (`world_2`), отправляет сообщение и запускает его на несколько шагов.
        - Проверяет целостность переписки агентов: удостоверяется, что ни один агент не отправляет сообщения самому себе.
    """
    # empty world
    world_1 = TinyWorld("Empty land", [])   
    world_1.run(2)

    # world with agents
    world_2 = focus_group_world
    world_2.broadcast("Discuss ideas for a new AI product you\'d love to have.")
    world_2.run(2)

    # check integrity of conversation
    for agent in world_2.agents:
        for msg in agent.episodic_memory.retrieve_all():
            if 'action' in msg['content'] and 'target' in msg['content']['action']:
                assert msg['content']['action']['target'] != agent.name, f"{agent.name} should not have any messages with itself as the target."
            
            # TODO stimulus integrity check?
```

### `test_broadcast`

```python
def test_broadcast(setup, focus_group_world):
    """
    Функция проверяет рассылку сообщений агентам в мире.

    Args:
        setup: Фикстура для начальной настройки.
        focus_group_world: Фикстура, представляющая мир с агентами.

    Raises:
        AssertionError: Если агенты не получили отправленное сообщение.

    Как работает функция:
        - Получает мир с агентами из фикстуры `focus_group_world`.
        - Рассылает сообщение всем агентам в мире.
        - Проверяет, получили ли агенты сообщение, путем поиска сообщения в памяти агентов.
    """
    world = focus_group_world
    world.broadcast("""
                Folks, we need to brainstorm ideas for a new baby product. Something moms have been asking for centuries and never got.

                Please start the discussion now.
                """)
    
    for agent in focus_group_world.agents:
        # did the agents receive the message?
        assert "Folks, we need to brainstorm" in agent.episodic_memory.retrieve_first(1)[0]['content']['stimuli'][0]['content'], f"{agent.name} should have received the message."
```

### `test_encode_complete_state`

```python
def test_encode_complete_state(setup, focus_group_world):
    """
    Функция проверяет кодирование полного состояния мира.

    Args:
        setup: Фикстура для начальной настройки.
        focus_group_world: Фикстура, представляющая мир с агентами.

    Raises:
        AssertionError: Если состояние мира не кодируется или содержит неверные данные.

    Как работает функция:
        - Получает мир с агентами из фикстуры `focus_group_world`.
        - Кодирует полное состояние мира с помощью `world.encode_complete_state()`.
        - Проверяет, что состояние не `None`, содержит имя мира и агентов.
    """
    world = focus_group_world

    # encode the state
    state = world.encode_complete_state()
    
    assert state is not None, "The state should not be None."
    assert state['name'] == world.name, "The state should have the world name."
    assert state['agents'] is not None, "The state should have the agents."
```

### `test_decode_complete_state`

```python
def test_decode_complete_state(setup, focus_group_world):
    """
    Функция проверяет декодирование полного состояния мира.

    Args:
        setup: Фикстура для начальной настройки.
        focus_group_world: Фикстура, представляющая мир с агентами.

    Raises:
        AssertionError: Если мир не декодируется или содержит неверные данные.

    Как работает функция:
        - Получает мир с агентами из фикстуры `focus_group_world`.
        - Сохраняет имя и количество агентов в мире.
        - Кодирует состояние мира.
        - Искусственно изменяет имя мира и очищает список агентов.
        - Декодирует состояние мира обратно с помощью `world.decode_complete_state(state)`.
        - Проверяет, что имя мира и количество агентов восстановлены корректно.
    """
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
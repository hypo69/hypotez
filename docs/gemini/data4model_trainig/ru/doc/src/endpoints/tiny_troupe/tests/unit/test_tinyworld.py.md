# Модуль тестирования TinyWorld

## Обзор

Этот модуль содержит unit-тесты для проверки функциональности класса `TinyWorld`, используемого для моделирования виртуальной среды с агентами. Здесь проверяются основные операции, такие как запуск мира, широковещательные сообщения, кодирование и декодирование состояния мира.

## Подробней

Модуль `test_tinyworld.py` выполняет тестирование класса `TinyWorld` и его способности взаимодействовать с агентами, моделировать их поведение и сохранять/восстанавливать состояние мира. В тестах используются фикстуры, определённые в `testing_utils.py`, для создания тестовых окружений с агентами.

## Функции

### `test_run`

```python
def test_run(setup, focus_group_world):
    """
    Тестирует запуск виртуального мира `TinyWorld` в различных конфигурациях.

    Args:
        setup: Фикстура pytest для предварительной настройки тестовой среды.
        focus_group_world: Фикстура pytest, представляющая собой экземпляр `TinyWorld` с предварительно настроенными агентами.

    Raises:
        AssertionError: Если в сообщениях агентов обнаруживаются ссылки на самих себя как на цель действия.

    Как работает функция:
    - Создается пустой мир `world_1` и запускается на 2 шага.
    - Используется мир `world_2` с агентами из фикстуры `focus_group_world`.
    - В `world_2` отправляется широковещательное сообщение агентам.
    - Проверяется целостность сообщений в памяти агентов, чтобы ни один агент не был целью своего же действия.

    Примеры:
    >>> # Для запуска этого теста требуется настроенное окружение pytest и фикстуры
    >>> # Пример вызова: pytest test_tinyworld.py::test_run
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
    Тестирует широковещательную рассылку сообщений агентам в виртуальном мире `TinyWorld`.

    Args:
        setup: Фикстура pytest для предварительной настройки тестовой среды.
        focus_group_world: Фикстура pytest, представляющая собой экземпляр `TinyWorld` с предварительно настроенными агентами.

    Raises:
        AssertionError: Если агенты не получают отправленное сообщение.

    Как работает функция:
    - Получает мир `world` с агентами из фикстуры `focus_group_world`.
    - Отправляет широковещательное сообщение всем агентам.
    - Проверяет, что каждый агент получил сообщение и сохранил его в своей эпизодической памяти.

    Примеры:
    >>> # Для запуска этого теста требуется настроенное окружение pytest и фикстуры
    >>> # Пример вызова: pytest test_tinyworld.py::test_broadcast
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
    Тестирует кодирование полного состояния виртуального мира `TinyWorld`.

    Args:
        setup: Фикстура pytest для предварительной настройки тестовой среды.
        focus_group_world: Фикстура pytest, представляющая собой экземпляр `TinyWorld` с предварительно настроенными агентами.

    Raises:
        AssertionError: Если состояние мира не кодируется корректно.

    Как работает функция:
    - Получает мир `world` из фикстуры `focus_group_world`.
    - Кодирует полное состояние мира с помощью метода `encode_complete_state`.
    - Проверяет, что закодированное состояние не равно `None`, содержит имя мира и информацию об агентах.

    Примеры:
    >>> # Для запуска этого теста требуется настроенное окружение pytest и фикстуры
    >>> # Пример вызова: pytest test_tinyworld.py::test_encode_complete_state
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
    Тестирует декодирование полного состояния виртуального мира `TinyWorld`.

    Args:
        setup: Фикстура pytest для предварительной настройки тестовой среды.
        focus_group_world: Фикстура pytest, представляющая собой экземпляр `TinyWorld` с предварительно настроенными агентами.

    Raises:
        AssertionError: Если состояние мира не декодируется корректно.

    Как работает функция:
    - Получает мир `world` из фикстуры `focus_group_world` и сохраняет его имя и количество агентов.
    - Кодирует полное состояние мира.
    - Изменяет имя мира и очищает список агентов в исходном мире.
    - Декодирует состояние обратно в мир с помощью метода `decode_complete_state`.
    - Проверяет, что после декодирования мир имеет исходное имя и количество агентов.

    Примеры:
    >>> # Для запуска этого теста требуется настроенное окружение pytest и фикстуры
    >>> # Пример вызова: pytest test_tinyworld.py::test_decode_complete_state
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
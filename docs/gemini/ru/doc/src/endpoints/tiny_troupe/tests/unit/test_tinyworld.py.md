# Модуль `test_tinyworld.py`

## Обзор

Этот модуль содержит юнит-тесты для класса `TinyWorld` из библиотеки `tinytroupe`. 

## Подробей

Тесты проверяют функциональность класса `TinyWorld`, в частности:

- Создание миров с агентами и без них
- Запуск симуляции миров
- Проверку целостности диалога между агентами
- Рассылку сообщений агентам 
- Кодирование и декодирование состояния мира

## Классы

### `TinyWorld`

**Описание**: Класс `TinyWorld` представляет собой симуляцию микромира с агентами, которые взаимодействуют друг с другом. 

**Атрибуты**:

- `name` (str): Имя мира.
- `agents` (list): Список агентов, которые присутствуют в мире. 

**Методы**:

- `run(n_steps: int)`: Запускает симуляцию мира на заданное количество шагов. 
- `broadcast(message: str)`: Рассылает сообщение всем агентам в мире. 
- `encode_complete_state()`: Кодирует состояние мира в словарь. 
- `decode_complete_state(state: dict)`: Декодирует состояние мира из словаря.

## Функции

### `test_run(setup, focus_group_world)`

**Назначение**: Тестирует функцию `run` класса `TinyWorld`. 

**Параметры**:

- `setup`: Функция настройки тестовой среды.
- `focus_group_world`: Объект `TinyWorld` с агентами.

**Как работает функция**: 

- Создает пустой мир (`world_1`) и запускает его на 2 шага. 
- Создает мир с агентами (`world_2`) и запускает его на 2 шага. 
- Проверяет, что у агентов в `world_2` нет сообщений с самими собой в качестве получателя. 

**Примеры**:
```python
# Пример запуска пустого мира
world_1 = TinyWorld("Empty land", [])   
world_1.run(2)

# Пример запуска мира с агентами
world_2 = focus_group_world
world_2.broadcast("Discuss ideas for a new AI product you'd love to have.")
world_2.run(2)
```

### `test_broadcast(setup, focus_group_world)`

**Назначение**: Тестирует функцию `broadcast` класса `TinyWorld`.

**Параметры**:

- `setup`: Функция настройки тестовой среды.
- `focus_group_world`: Объект `TinyWorld` с агентами.

**Как работает функция**:

- Рассылает сообщение агентам в `focus_group_world`.
- Проверяет, что все агенты получили сообщение.

**Примеры**:
```python
# Пример рассылки сообщения агентам
world = focus_group_world
world.broadcast("""
    Folks, we need to brainstorm ideas for a new baby product. Something moms have been asking for centuries and never got.

    Please start the discussion now.
    """)

# Проверка, что все агенты получили сообщение
for agent in focus_group_world.agents:
    assert "Folks, we need to brainstorm" in agent.episodic_memory.retrieve_first(1)[0][\'content\'][\'stimuli\'][0][\'content\'], f"{agent.name} should have received the message."

```

### `test_encode_complete_state(setup, focus_group_world)`

**Назначение**: Тестирует функцию `encode_complete_state` класса `TinyWorld`.

**Параметры**:

- `setup`: Функция настройки тестовой среды.
- `focus_group_world`: Объект `TinyWorld` с агентами.

**Как работает функция**:

- Кодирует состояние мира в словарь.
- Проверяет, что словарь содержит имя мира и список агентов.

**Примеры**:
```python
# Пример кодирования состояния мира
world = focus_group_world
state = world.encode_complete_state()

# Проверка, что словарь содержит имя мира и список агентов
assert state is not None, "The state should not be None."
assert state[\'name\'] == world.name, "The state should have the world name."
assert state[\'agents\'] is not None, "The state should have the agents."

```

### `test_decode_complete_state(setup, focus_group_world)`

**Назначение**: Тестирует функцию `decode_complete_state` класса `TinyWorld`.

**Параметры**:

- `setup`: Функция настройки тестовой среды.
- `focus_group_world`: Объект `TinyWorld` с агентами.

**Как работает функция**:

- Кодирует состояние мира в словарь.
- Изменяет имя мира и список агентов.
- Декодирует состояние из словаря.
- Проверяет, что имя мира и список агентов были восстановлены.

**Примеры**:
```python
# Пример декодирования состояния мира
world = focus_group_world
name_1 = world.name
n_agents_1 = len(world.agents)

# Кодирование состояния мира
state = world.encode_complete_state()

# Изменение имени мира и списка агентов
world.name = "New name"
world.agents = []

# Декодирование состояния мира
world_2 = world.decode_complete_state(state)

# Проверка, что имя мира и список агентов были восстановлены
assert world_2 is not None, "The world should not be None."
assert world_2.name == name_1, "The world should have the same name."
assert len(world_2.agents) == n_agents_1, "The world should have the same number of agents."

```
# Testing Utilities for the `tinytroupe` Module

## Overview

This module provides testing utilities for the `tinytroupe` module. It contains functions for managing test files, checking simulation results, and setting up test environments. The module also includes fixtures for creating common test scenarios.

## Details

This module is used for automated testing of the `tinytroupe` module's functionalities. It helps to ensure that the code behaves as expected in various situations. The utilities provided allow for efficient checks on simulation results, file management, and test environment setup.

## Table of Contents

- **Functions**
    - `remove_file_if_exists`
    - `contains_action_type`
    - `contains_action_content`
    - `contains_stimulus_type`
    - `contains_stimulus_content`
    - `terminates_with_action_type`
    - `proposition_holds`
    - `only_alphanumeric`
    - `create_test_system_user_message`
    - `agents_personas_are_equal`
    - `agent_first_name`
    - `get_relative_to_test_path`
- **Fixtures**
    - `focus_group_world`
    - `setup`

## Functions

### `remove_file_if_exists`

**Purpose**: Удаляет файл по заданному пути, если он существует.

**Parameters**:

- `file_path` (str): Путь к файлу.

**Returns**:

- None

**Raises Exceptions**:

- None

**Example**:

```python
>>> remove_file_if_exists("test_file.txt")
```

### `contains_action_type`

**Purpose**: Проверяет, содержит ли заданный список действий действие заданного типа.

**Parameters**:

- `actions` (list): Список действий.
- `action_type` (str): Тип действия.

**Returns**:

- bool: `True`, если список действий содержит действие заданного типа, иначе `False`.

**Raises Exceptions**:

- None

**Example**:

```python
>>> actions = [{"action": {"type": "say"}}, {"action": {"type": "ask"}}]
>>> contains_action_type(actions, "say")
True
>>> contains_action_type(actions, "read")
False
```

### `contains_action_content`

**Purpose**: Проверяет, содержит ли заданный список действий действие с заданным содержанием.

**Parameters**:

- `actions` (list): Список действий.
- `action_content` (str): Содержание действия.

**Returns**:

- bool: `True`, если список действий содержит действие с заданным содержанием, иначе `False`.

**Raises Exceptions**:

- None

**Example**:

```python
>>> actions = [{"action": {"content": "Hello, world!"}}, {"action": {"content": "How are you?"}}]
>>> contains_action_content(actions, "Hello, world!")
True
>>> contains_action_content(actions, "Good morning")
False
```

### `contains_stimulus_type`

**Purpose**: Проверяет, содержит ли заданный список стимулов стимул заданного типа.

**Parameters**:

- `stimuli` (list): Список стимулов.
- `stimulus_type` (str): Тип стимула.

**Returns**:

- bool: `True`, если список стимулов содержит стимул заданного типа, иначе `False`.

**Raises Exceptions**:

- None

**Example**:

```python
>>> stimuli = [{"type": "text"}, {"type": "image"}]
>>> contains_stimulus_type(stimuli, "text")
True
>>> contains_stimulus_type(stimuli, "audio")
False
```

### `contains_stimulus_content`

**Purpose**: Проверяет, содержит ли заданный список стимулов стимул с заданным содержанием.

**Parameters**:

- `stimuli` (list): Список стимулов.
- `stimulus_content` (str): Содержание стимула.

**Returns**:

- bool: `True`, если список стимулов содержит стимул с заданным содержанием, иначе `False`.

**Raises Exceptions**:

- None

**Example**:

```python
>>> stimuli = [{"content": "The quick brown fox"}, {"content": "jumps over the lazy dog"}]
>>> contains_stimulus_content(stimuli, "The quick brown fox")
True
>>> contains_stimulus_content(stimuli, "A cat sits on a mat")
False
```

### `terminates_with_action_type`

**Purpose**: Проверяет, заканчивается ли заданный список действий действием заданного типа.

**Parameters**:

- `actions` (list): Список действий.
- `action_type` (str): Тип действия.

**Returns**:

- bool: `True`, если список действий заканчивается действием заданного типа, иначе `False`.

**Raises Exceptions**:

- None

**Example**:

```python
>>> actions = [{"action": {"type": "say"}}, {"action": {"type": "ask"}}, {"action": {"type": "say"}}]
>>> terminates_with_action_type(actions, "say")
True
>>> terminates_with_action_type(actions, "ask")
False
```

### `proposition_holds`

**Purpose**: Проверяет, является ли заданное утверждение истинным, согласно вызову LLM.
Это может использоваться для проверки свойств текста, которые трудно
проверить механически, например, "текст содержит идеи для товара".

**Parameters**:

- `proposition` (str): Утверждение, которое нужно проверить.

**Returns**:

- bool: `True`, если утверждение истинно, иначе `False`.

**Raises Exceptions**:

- Exception: Если LLM возвращает неожиданный результат.

**Example**:

```python
>>> proposition_holds("The text contains ideas for a product.")
True
>>> proposition_holds("The text is written in French.")
False
```

### `only_alphanumeric`

**Purpose**: Возвращает строку, содержащую только буквенно-цифровые символы.

**Parameters**:

- `string` (str): Строка, из которой нужно удалить небуквенно-цифровые символы.

**Returns**:

- str: Строка, содержащая только буквенно-цифровые символы.

**Raises Exceptions**:

- None

**Example**:

```python
>>> only_alphanumeric("Hello, world!")
"Helloworld"
>>> only_alphanumeric("123abc456")
"123abc456"
```

### `create_test_system_user_message`

**Purpose**: Создает список, содержащий одно системное сообщение и одно пользовательское сообщение.

**Parameters**:

- `user_prompt` (str): Текст пользовательского сообщения.
- `system_prompt` (str): Текст системного сообщения. По умолчанию "You are a helpful AI assistant.".

**Returns**:

- list: Список сообщений.

**Raises Exceptions**:

- None

**Example**:

```python
>>> create_test_system_user_message("Hello, world!")
[{'role': 'system', 'content': 'You are a helpful AI assistant.'}, {'role': 'user', 'content': 'Hello, world!'}]
```

### `agents_personas_are_equal`

**Purpose**: Проверяет, равны ли конфигурации двух агентов.

**Parameters**:

- `agent1` (TinyPerson): Первый агент.
- `agent2` (TinyPerson): Второй агент.
- `ignore_name` (bool): Если `True`, то имя агента не учитывается при сравнении.

**Returns**:

- bool: `True`, если конфигурации агентов равны, иначе `False`.

**Raises Exceptions**:

- None

**Example**:

```python
>>> agent1 = TinyPerson("Alice")
>>> agent2 = TinyPerson("Alice")
>>> agents_personas_are_equal(agent1, agent2)
True
>>> agent3 = TinyPerson("Bob")
>>> agents_personas_are_equal(agent1, agent3)
False
```

### `agent_first_name`

**Purpose**: Возвращает имя агента.

**Parameters**:

- `agent` (TinyPerson): Агент.

**Returns**:

- str: Имя агента.

**Raises Exceptions**:

- None

**Example**:

```python
>>> agent = TinyPerson("Alice")
>>> agent_first_name(agent)
"Alice"
```

### `get_relative_to_test_path`

**Purpose**: Возвращает путь к тестовому файлу с заданным суффиксом.

**Parameters**:

- `path_suffix` (str): Суффикс пути к файлу.

**Returns**:

- str: Путь к тестовому файлу.

**Raises Exceptions**:

- None

**Example**:

```python
>>> get_relative_to_test_path("test_file.txt")
'/path/to/tests/test_file.txt'
```

## Fixtures

### `focus_group_world`

**Purpose**: Создает мир с тремя агентами: Лизой, Оскаром и Маркосом.

**Parameters**:

- None

**Returns**:

- TinyWorld: Мир с тремя агентами.

**Raises Exceptions**:

- None

**Example**:

```python
>>> world = focus_group_world()
>>> world.agents
[<tinytroupe.agent.TinyPerson object at 0x7f8a34564910>, <tinytroupe.agent.TinyPerson object at 0x7f8a345649d0>, <tinytroupe.agent.TinyPerson object at 0x7f8a34564a50>]
```

### `setup`

**Purpose**: Очищает список агентов и список миров перед каждым тестом.

**Parameters**:

- None

**Returns**:

- None

**Raises Exceptions**:

- None

**Example**:

```python
>>> # The setup fixture is automatically called before each test function.
>>> # This ensures that the agent and world lists are clean before each test.
```

## Examples

```python
import pytest
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld
from hypotez.src.endpoints.tiny_troupe.tests.testing_utils import focus_group_world, contains_action_type, agent_first_name

def test_focus_group_world(focus_group_world):
    assert len(focus_group_world.agents) == 3
    assert focus_group_world.name == "Focus group"

def test_contains_action_type():
    actions = [{"action": {"type": "say"}}, {"action": {"type": "ask"}}]
    assert contains_action_type(actions, "say") == True
    assert contains_action_type(actions, "read") == False

def test_agent_first_name():
    agent = TinyPerson("Alice")
    assert agent_first_name(agent) == "Alice"
```

## Conclusion

This module provides a comprehensive set of testing utilities for the `tinytroupe` module, facilitating automated testing and verification of its functionalities. These utilities allow developers to efficiently manage test files, verify simulation results, and set up test environments, contributing to the overall quality and reliability of the codebase.
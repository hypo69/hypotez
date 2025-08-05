# TinyWorld Unit Tests

## Overview

This module contains unit tests for the `TinyWorld` class, which represents a simulated environment for running agent simulations in the `hypotez` project. These tests cover various aspects of `TinyWorld`, including:

- Initialization and running simulations.
- Broadcasting messages to agents.
- Encoding and decoding the complete state of the world.

## Details

The `TinyWorld` class is a crucial part of the `hypotez` project. It provides a framework for simulating interactions between multiple agents within a shared environment. These tests ensure that the `TinyWorld` class functions correctly and consistently.

## Functions

### `test_run(setup, focus_group_world)`

**Purpose**: This function tests the `run` method of the `TinyWorld` class. It checks whether the simulation runs correctly for both an empty world and a world with agents.

**Parameters**:

- `setup`: A fixture that sets up the test environment.
- `focus_group_world`: A fixture that creates a `TinyWorld` instance with agents for testing.

**Returns**:

- `None`.

**Raises Exceptions**:

- `AssertionError`: If any of the assertions within the test fail.

**How the Function Works**:

- The function creates two `TinyWorld` instances:
    - `world_1`: An empty world.
    - `world_2`: A world with agents.
- It runs the simulation for each world using the `run` method.
- The function checks the integrity of conversations between agents by verifying that messages are not sent to the same agent as the sender.
- It also asserts that the state of the world is not `None`.

**Examples**:

```python
# Test with an empty world
test_run(setup, focus_group_world)

# Test with a world containing agents
test_run(setup, focus_group_world)
```

### `test_broadcast(setup, focus_group_world)`

**Purpose**: This function tests the `broadcast` method of the `TinyWorld` class. It checks whether agents receive the broadcast message.

**Parameters**:

- `setup`: A fixture that sets up the test environment.
- `focus_group_world`: A fixture that creates a `TinyWorld` instance with agents for testing.

**Returns**:

- `None`.

**Raises Exceptions**:

- `AssertionError`: If any of the assertions within the test fail.

**How the Function Works**:

- The function broadcasts a message to the `focus_group_world` instance.
- It then checks whether the message was received by each agent in the world.

**Examples**:

```python
# Test broadcasting a message
test_broadcast(setup, focus_group_world)
```

### `test_encode_complete_state(setup, focus_group_world)`

**Purpose**: This function tests the `encode_complete_state` method of the `TinyWorld` class. It checks that the state is encoded correctly and that the returned state is not `None`.

**Parameters**:

- `setup`: A fixture that sets up the test environment.
- `focus_group_world`: A fixture that creates a `TinyWorld` instance with agents for testing.

**Returns**:

- `None`.

**Raises Exceptions**:

- `AssertionError`: If any of the assertions within the test fail.

**How the Function Works**:

- The function encodes the complete state of the `focus_group_world` instance.
- It verifies that the state is not `None` and that it includes the world name and information about the agents.

**Examples**:

```python
# Test encoding the state of the world
test_encode_complete_state(setup, focus_group_world)
```

### `test_decode_complete_state(setup, focus_group_world)`

**Purpose**: This function tests the `decode_complete_state` method of the `TinyWorld` class. It checks that the decoded state restores the world to its original state.

**Parameters**:

- `setup`: A fixture that sets up the test environment.
- `focus_group_world`: A fixture that creates a `TinyWorld` instance with agents for testing.

**Returns**:

- `None`.

**Raises Exceptions**:

- `AssertionError`: If any of the assertions within the test fail.

**How the Function Works**:

- The function encodes the complete state of the `focus_group_world` instance.
- It then modifies the world (changing its name and clearing the agents list).
- The decoded state is used to restore the world to its original state.
- The function verifies that the restored world has the same name and number of agents as the original world.

**Examples**:

```python
# Test decoding the state of the world
test_decode_complete_state(setup, focus_group_world)
```
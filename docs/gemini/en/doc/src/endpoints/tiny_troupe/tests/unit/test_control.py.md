# Module for managing Tiny Troupe simulations.

## Overview
 
The module provides functions for managing simulations in the `Tiny Troupe` environment. 
It allows for creating, running, and saving simulations, including checkpointing during the execution.

## Details

The module interacts with the `Tiny Troupe` environment to manage simulations. It provides functionalities for:

- **Initialization:** Starting a new simulation with a specific cache file.
- **Execution:** Running the simulation for a specific number of steps or until a certain condition is met.
- **Checkpoint:** Saving the simulation state at a particular point in time, allowing to resume from that state later.
- **Termination:** Ending the current simulation and clearing the simulation state.
- **Cache Management:** Handling simulation cache files, including checking for cache hits and misses.

The module uses the following key classes from the `Tiny Troupe` environment:

- **`TinyPerson`:** Represents an individual agent in the simulation.
- **`TinyWorld`:** Represents the simulated environment with agents and objects.
- **`TinyToolUse`:** Provides functionality for tools and their usage by agents.
- **`TinyPersonFactory`:** Creates agents based on predefined specifications.
- **`TinyEnricher`:** Enhances the knowledge and capabilities of agents.
- **`ArtifactExporter`:** Exports simulation data and artifacts.

## Classes

### `Simulation`
**Description**: Represents a Tiny Troupe simulation with its configuration, state, and execution details.

**Attributes**:
- `name` (str): Unique name of the simulation.
- `status` (str): Current status of the simulation (e.g., "STARTED", "STOPPED").
- `cached_trace` (dict):  Dictionary representing the simulation's state cached in the checkpoint file.
- `execution_trace` (list): A list of actions and events that happened during the execution of the simulation. 
- `checkpoint_file` (str): Path to the file used for saving simulation checkpoints.

**Methods**:
- `run(steps: int, verbose: bool = False)`: Executes the simulation for the specified number of steps.
- `checkpoint()`: Saves the current state of the simulation to the checkpoint file.

## Functions

### `begin(checkpoint_file: str, name: str = "default")`
**Purpose**: Initializes a new Tiny Troupe simulation.

**Parameters**:
- `checkpoint_file` (str): Path to the file used for saving simulation checkpoints.
- `name` (str): Unique name for the simulation.

**Returns**:
- `None`

**Raises Exceptions**:
- `None`

**How the Function Works**:
1. The function checks if a simulation with the given name is already running.
2. If not, it creates a new `Simulation` object and associates it with the given name.
3. It sets the simulation status to "STARTED".
4. It initializes the `cached_trace` and `execution_trace` attributes of the simulation.

### `checkpoint(name: str = "default")`
**Purpose**: Saves the current state of the running simulation to a checkpoint file.

**Parameters**:
- `name` (str): The name of the simulation for which to save the checkpoint.

**Returns**:
- `None`

**Raises Exceptions**:
- `None`

**How the Function Works**:
1. The function retrieves the `Simulation` object associated with the given name.
2. If the simulation is running, it saves the `cached_trace` and `execution_trace` to the specified checkpoint file.
3. If the simulation is not running, it logs a warning message.

### `end(name: str = "default")`
**Purpose**: Terminates the currently running simulation.

**Parameters**:
- `name` (str): The name of the simulation to end.

**Returns**:
- `None`

**Raises Exceptions**:
- `None`

**How the Function Works**:
1. The function retrieves the `Simulation` object associated with the given name.
2. If the simulation is running, it sets the simulation status to "STOPPED".
3. It logs a message indicating that the simulation has been ended.

### `cache_hits(name: str = "default")`
**Purpose**: Retrieves the number of cache hits for a specific simulation.

**Parameters**:
- `name` (str): The name of the simulation for which to check cache hits.

**Returns**:
- `int`: The number of cache hits for the specified simulation.

**Raises Exceptions**:
- `None`

**How the Function Works**:
1. The function retrieves the `Simulation` object associated with the given name.
2. If the simulation is running, it returns the number of cache hits based on the number of elements in the `execution_trace` list.
3. If the simulation is not running, it returns 0.

### `cache_misses(name: str = "default")`
**Purpose**: Retrieves the number of cache misses for a specific simulation.

**Parameters**:
- `name` (str): The name of the simulation for which to check cache misses.

**Returns**:
- `int`: The number of cache misses for the specified simulation.

**Raises Exceptions**:
- `None`

**How the Function Works**:
1. The function retrieves the `Simulation` object associated with the given name.
2. If the simulation is running, it returns the number of cache misses based on the number of times the simulation executed a step without finding a matching cached state.
3. If the simulation is not running, it returns 0.

### `reset(name: str = "default")`
**Purpose**: Resets the state of the simulation and removes any existing checkpoint file.

**Parameters**:
- `name` (str): The name of the simulation to reset.

**Returns**:
- `None`

**Raises Exceptions**:
- `None`

**How the Function Works**:
1. The function retrieves the `Simulation` object associated with the given name.
2. If the simulation is running, it sets the status to "STOPPED".
3. It removes the checkpoint file associated with the simulation.
4. It removes the simulation from the `_current_simulations` dictionary, effectively resetting its state.

## Parameter Details

- `checkpoint_file` (str): Path to the file used for saving simulation checkpoints.
- `name` (str): Unique name for the simulation.

## Examples

```python
from tinytroupe.control import Simulation, begin, checkpoint, end, cache_hits, cache_misses, reset

# Starting a new simulation
begin("my_simulation.cache.json")

# Running the simulation for 10 steps
Simulation.run(10)

# Saving a checkpoint
checkpoint()

# Ending the simulation
end()

# Checking for cache hits and misses
cache_hits()
cache_misses()

# Resetting the simulation
reset()
```

## Inner Functions

**Inner Functions**: None

## How the Function Works
 
The module operates by tracking the current simulation state, including the simulation status, cached trace, and execution trace. 
The `begin` function initiates a new simulation and sets up the initial state. 
The `checkpoint` function saves the current state to a checkpoint file, which can be later used to resume the simulation from that point. 
The `end` function terminates the simulation and clears the simulation state.

## Examples

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
    # erase the file if it exists
    remove_file_if_exists("control_test.cache.json")

    control.reset()
    
    assert control._current_simulations["default"] is None, "There should be no simulation running at this point."

    # erase the file if it exists
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

    # check if the file was created
    assert os.path.exists("control_test.cache.json"), "The checkpoint file should have been created."

    control.end()

    assert control._current_simulations["default"].status == Simulation.STATUS_STOPPED, "The simulation should be ended at this point."

def test_begin_checkpoint_end_with_world(setup):
    # erase the file if it exists
    remove_file_if_exists("control_test_world.cache.json")

    control.reset()
    
    assert control._current_simulations["default"] is None, "There should be no simulation running at this point."

    control.begin("control_test_world.cache.json")
    assert control._current_simulations["default"].status == Simulation.STATUS_STARTED, "The simulation should be started at this point."

    world = TinyWorld("Test World", [create_oscar_the_architect(), create_lisa_the_data_scientist()])

    world.make_everyone_accessible()

    assert control._current_simulations["default"].cached_trace is not None, "There should be a cached trace at this point."
    assert control._current_simulations["default"].execution_trace is not None, "There should be an execution trace at this point."

    world.run(2)

    control.checkpoint()

    # check if the file was created
    assert os.path.exists("control_test_world.cache.json"), "The checkpoint file should have been created."

    control.end()

    assert control._current_simulations["default"].status == Simulation.STATUS_STOPPED, "The simulation should be ended at this point."

def test_begin_checkpoint_end_with_factory(setup):
    # erase the file if it exists
    remove_file_if_exists("control_test_personfactory.cache.json")

    control.reset()

    def aux_simulation_to_repeat(iteration, verbose=False):
        control.reset()
    
        assert control._current_simulations["default"] is None, "There should be no simulation running at this point."

        control.begin("control_test_personfactory.cache.json")
        assert control._current_simulations["default"].status == Simulation.STATUS_STARTED, "The simulation should be started at this point."    
        
        factory = TinyPersonFactory("We are interested in experts in the production of the traditional Gazpacho soup.")

        assert control._current_simulations["default"].cached_trace is not None, "There should be a cached trace at this point."
        assert control._current_simulations["default"].execution_trace is not None, "There should be an execution trace at this point."

        agent = factory.generate_person("A Brazilian tourist who learned about Gazpaccho in a trip to Spain.")

        assert control._current_simulations["default"].cached_trace is not None, "There should be a cached trace at this point."
        assert control._current_simulations["default"].execution_trace is not None, "There should be an execution trace at this point."

        control.checkpoint()

        # check if the file was created
        assert os.path.exists("control_test_personfactory.cache.json"), "The checkpoint file should have been created."

        control.end()
        assert control._current_simulations["default"].status == Simulation.STATUS_STOPPED, "The simulation should be ended at this point."

        if verbose:
            logger.debug(f"###################################################################################### Sim Iteration:{iteration}")
            logger.debug(f"###################################################################################### Agent persona configs:{agent._persona}")

        return agent

    assert control.cache_misses() == 0, "There should be no cache misses in this test."
    assert control.cache_hits() == 0, "There should be no cache hits here"

    # FIRST simulation ########################################################
    agent_1 = aux_simulation_to_repeat(1, verbose=True)
    age_1 = agent_1.get("age")
    nationality_1 = agent_1.get("nationality")
    minibio_1 = agent_1.minibio()
    print("minibio_1 =", minibio_1)


    # SECOND simulation ########################################################
    logger.debug(">>>>>>>>>>>>>>>>>>>>>>>>>> Second simulation...")
    agent_2 = aux_simulation_to_repeat(2, verbose=True)
    age_2 = agent_2.get("age")
    nationality_2 = agent_2.get("nationality")
    minibio_2 = agent_2.minibio()
    print("minibio_2 =", minibio_2)

    assert control.cache_misses() == 0, "There should be no cache misses in this test."
    assert control.cache_hits() > 0, "There should be cache hits here."

    assert age_1 == age_2, "The age should be the same in both simulations."
    assert nationality_1 == nationality_2, "The nationality should be the same in both simulations."
    assert minibio_1 == minibio_2, "The minibio should be the same in both simulations."

    #
    # let's also check the contents of the cache file, as raw text, not dict
    #
    with open("control_test_personfactory.cache.json", "r") as f:
        cache_contents = f.read()

    assert "\'_aux_model_call\'" in cache_contents, "The cache file should contain the \'_aux_model_call\' call."
    assert "\'_setup_agent\'" in cache_contents, "The cache file should contain the \'_setup_agent\' call."
    assert "\'define\'" not in cache_contents, "The cache file should not contain the \'define\' methods, as these are reentrant."
    assert "\'define_several\'" not in cache_contents, "The cache file should not contain the \'define_several\' methods, as these are reentrant."

        
```

## Your Behavior During Code Analysis:
 - Inside the code, you might encounter expressions between `<` `>`. For example: `<instruction for gemini model:Loading product descriptions into PrestaShop.>, <next, if available>. These are placeholders where you insert the relevant value. 
- Always refer to the system instructions for processing code in the `hypotez` project (the first set of instructions you translated);
 - Analyze the file's location within the project. This helps understand its purpose and relationship with other files. You will find the file location in the very first line of code starting with `## \\file /...`;
 - Memorize the provided code and analyze its connection with other parts of the project;
 - In these instructions, do not suggest code improvements. Strictly follow point 5. **Example File** when composing the response.
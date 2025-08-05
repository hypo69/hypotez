# Hypotez - Testing Basic TinyTroupe Scenarios

## Overview

This module contains unit tests for basic scenarios using the TinyTroupe library. 

The tests verify core functionalities such as:

- Creating and defining TinyPerson agents
- Executing basic conversational interactions 
- Tracking the simulation execution trace
- Utilizing TinyTools and checking document creation

## Details

This file resides in the `hypotez/src/endpoints/tiny_troupe/tests/scenarios` directory. 

It implements a basic scenario testing framework for the `TinyTroupe` library. 

The `test_basic_scenario_1()` function checks the creation and manipulation of agents, their definitions, and simulation status tracking using `control` module functions.

`test_tool_usage_1()` validates the usage of TinyTools, specifically `TinyWordProcessor`, and asserts that the generated document is correctly saved to the specified file path.


## Classes

### `Simulation`

**Description**: Represents a simulation run in TinyTroupe, enabling execution and tracking of agent interactions. 

**Attributes**:
- `status` (`Simulation.STATUS_STARTED`, `Simulation.STATUS_STOPPED`, `Simulation.STATUS_ENDED`): Indicates the current state of the simulation.
- `execution_trace`: A record of actions and events that occurred during the simulation.
- `cached_trace`: A cached version of the `execution_trace` for further analysis.

**Methods**: 
- `checkpoint()`: Saves the current state of the simulation into the `execution_trace`.


## Functions

### `test_basic_scenario_1`

**Purpose**: Tests the basic scenario of creating and interacting with a TinyPerson agent, tracking the simulation state, and validating simulation traces.

**Parameters**: None

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:
- Initializes the TinyTroupe environment using the `control` module.
- Creates a `TinyPerson` agent using the `create_oscar_the_architect()` function.
- Defines properties for the agent using `agent.define()`.
- Verifies that the simulation is started and the trace is properly captured.
- Executes the `checkpoint()` method to record the current state.
- Triggers interaction with the agent using `agent.listen_and_act()`.
- Ends the simulation using `control.end()`.


### `test_tool_usage_1`

**Purpose**: Tests the usage of TinyTools within a TinyPerson's mental faculties, specifically the `TinyWordProcessor`, and verifies that the generated document is saved to the correct file path.

**Parameters**: None

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:
- Defines a custom `ArtifactExporter` and `TinyEnricher`.
- Creates a `TinyToolUse` faculty with a `TinyWordProcessor` that uses the defined exporter and enricher.
- Adds the `TinyToolUse` faculty to the `Lisa` agent.
- Initiates interactions using `agent.listen_and_act()`, providing an instruction to create a resume document.
- Asserts that the generated document exists in the specified path, verifying its creation. 

**Inner Functions**:
- `contains_action_type(actions: List[dict], action_type: str) -> bool`: Helper function to check if a specific action type exists in the list of actions.


**Examples**:

```python
import pytest
import logging

logger = logging.getLogger("tinytroupe")

import sys
sys.path.append('../../tinytroupe/')
sys.path.append('../../')
sys.path.append('..')


import tinytroupe
from tinytroupe.agent import TinyPerson, TinyToolUse
from tinytroupe.environment import TinyWorld, TinySocialNetwork
from tinytroupe.factory import TinyPersonFactory
from tinytroupe.extraction import ResultsExtractor

from tinytroupe.enrichment import TinyEnricher
from tinytroupe.extraction import ArtifactExporter
from tinytroupe.tools import TinyWordProcessor

from tinytroupe.examples import create_lisa_the_data_scientist, create_oscar_the_architect, create_marcos_the_physician
import tinytroupe.control as control
from tinytroupe.control import Simulation

from testing_utils import *

def test_basic_scenario_1():
    control.reset()

    assert control._current_simulations["default"] is None, "There should be no simulation running at this point."

    control.begin()
    assert control._current_simulations["default"].status == Simulation.STATUS_STARTED, "The simulation should be started at this point."

    agent = create_oscar_the_architect()

    agent.define("age", 19)
    agent.define("nationality", "Brazilian")

    assert control._current_simulations["default"].cached_trace is not None, "There should be a cached trace at this point."
    assert control._current_simulations["default"].execution_trace is not None, "There should be an execution trace at this point."

    control.checkpoint()
    # TODO check file creation

    agent.listen_and_act("How are you doing??")
    agent.define("occupation", "Engineer")

    control.checkpoint()
    # TODO check file creation

    control.end()


def test_tool_usage_1():

    data_export_folder = f"{EXPORT_BASE_FOLDER}/test_tool_usage_1"
    
    exporter = ArtifactExporter(base_output_folder=data_export_folder)
    enricher = TinyEnricher()
    tooluse_faculty = TinyToolUse(tools=[TinyWordProcessor(exporter=exporter, enricher=enricher)])

    lisa = create_lisa_the_data_scientist()

    lisa.add_mental_faculties([tooluse_faculty])

    actions = lisa.listen_and_act(
                            """
                            You have just been fired and need to find a new job. You decide to think about what you 
                            want in life and then write a resume. The file must be titled **exactly** \'Resume\'.
                            Don\'t stop until you actually write the resume.
                            """, return_actions=True)
    
    assert contains_action_type(actions, "WRITE_DOCUMENT"), "There should be a WRITE_DOCUMENT action in the actions list."

    # check that the document was written to a file
    assert os.path.exists(f"{data_export_folder}/Document/Resume.Lisa Carter.docx"), "The document should have been written to a file."
    assert os.path.exists(f"{data_export_folder}/Document/Resume.Lisa Carter.json"), "The document should have been written to a file."
    assert os.path.exists(f"{data_export_folder}/Document/Resume.Lisa Carter.md"), "The document should have been written to a file."

                ```
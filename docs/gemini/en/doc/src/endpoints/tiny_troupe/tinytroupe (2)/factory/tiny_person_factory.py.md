# TinyPersonFactory

## Overview

This module defines the `TinyPersonFactory` class, which is responsible for generating instances of the `TinyPerson` class. The `TinyPersonFactory` class uses OpenAI's large language model (LLM) to generate realistic descriptions of people for use in simulations. It provides methods for creating individual `TinyPerson` instances and lists of `TinyPerson` instances.

## Details

The `TinyPersonFactory` class utilizes the `chevron` library for templating, `openai_utils` for interacting with the OpenAI API, and `utils` for JSON extraction. It also uses the `transactional` decorator to ensure that the creation and setup of `TinyPerson` instances are properly cached for performance optimization. 

## Classes

### `TinyPersonFactory`

**Description**:  This class is a factory that generates `TinyPerson` instances using OpenAI's LLM.

**Inherits**: `TinyFactory`

**Attributes**:

- `context_text` (str): The context text used to generate the `TinyPerson` instances.
- `person_prompt_template_path` (str): The path to the template used to generate the OpenAI prompt for person generation.
- `generated_minibios` (list): A list of minibio strings of previously generated `TinyPerson` instances.
- `generated_names` (list): A list of names of previously generated `TinyPerson` instances.

**Methods**:

- `__init__(self, context_text, simulation_id: str = None)`: Initializes a `TinyPersonFactory` instance with the context text and simulation ID.

- `generate_person_factories(number_of_factories, generic_context_text)`: Generates a list of `TinyPersonFactory` instances using OpenAI's LLM. The function prompts the LLM to generate descriptions of people based on a generic context and the specified number of factories.

- `generate_person(self, agent_particularities: str = None, temperature: float = 1.5, frequency_penalty: float = 0.0, presence_penalty: float = 0.0, attepmpts: int = 10)`: Generates a single `TinyPerson` instance using OpenAI's LLM. It uses a prompt template that includes context, agent particularities, and information about previously generated persons. It also handles potential name collisions by repeatedly generating the person until a unique name is found.

- `generate_people(self, number_of_people: int, agent_particularities: str = None, temperature: float = 1.5, frequency_penalty: float = 0.0, presence_penalty: float = 0.0, attepmpts: int = 10, verbose: bool = False)`: Generates a list of `TinyPerson` instances using OpenAI's LLM. The function calls `generate_person` repeatedly to create the specified number of people. 

- `_aux_model_call(self, messages, temperature, frequency_penalty, presence_penalty)`: Auxiliary method to make a model call using OpenAI's API. This method is designed to be used with the `transactional` decorator to ensure proper caching behavior.

- `_setup_agent(self, agent, configuration)`: Sets up the `TinyPerson` instance with the necessary elements based on the provided configuration. This method is also designed to be used with the `transactional` decorator to ensure proper caching behavior.

## Parameter Details

- `context_text` (str): The context text used to generate the `TinyPerson` instances. This text provides the LLM with information about the simulation environment and the roles of the generated people.

- `agent_particularities` (str):  Specific details about the `TinyPerson` being generated, which might include their profession, background, or personality traits.

- `temperature` (float): A parameter for controlling the randomness of the LLM's output. Higher temperatures lead to more creative and unexpected outputs.

- `frequency_penalty` (float): A parameter for penalizing the LLM from repeating words or phrases. A higher frequency penalty encourages the LLM to generate more diverse outputs.

- `presence_penalty` (float): A parameter for penalizing the LLM from repeating previously generated content. A higher presence penalty discourages the LLM from using the same phrases or concepts multiple times.

- `attepmpts` (int): The maximum number of attempts to generate a unique `TinyPerson` instance. This parameter helps prevent the code from getting stuck in an infinite loop if the LLM repeatedly generates names that have already been used.

- `verbose` (bool): A flag indicating whether to print verbose information during the generation process. This is useful for debugging and monitoring the progress of the generation process.

- `number_of_factories` (int): The number of `TinyPersonFactory` instances to generate.

- `generic_context_text` (str): The generic context text used to generate the `TinyPersonFactory` instances. This text provides the LLM with broad information about the simulation environment and the types of people that will be generated.

- `simulation_id` (str): The ID of the simulation. This is used to track the generation of `TinyPerson` instances within the simulation.

- `messages` (list): A list of messages to be sent to the LLM. This list can include system prompts, user prompts, and previous responses from the LLM.

- `number_of_people` (int): The number of `TinyPerson` instances to generate. This parameter is used to create a list of people for the simulation.


## Examples

```python
# Create a TinyPersonFactory instance with a specific context
factory = TinyPersonFactory(context_text="This is a simulation of a school")

# Generate a TinyPerson instance with default settings
person = factory.generate_person()

# Generate a list of 5 TinyPerson instances with a specific agent particularity
people = factory.generate_people(number_of_people=5, agent_particularities="These people are teachers")

# Generate a list of TinyPersonFactory instances using the provided context
factories = TinyPersonFactory.generate_person_factories(number_of_factories=3, generic_context_text="This is a simulation of a city")
```

## Inner Functions

### `aux_generate(attempt)`

**Purpose**: This inner function generates the agent specifications using OpenAI's LLM and checks for name collisions. It handles name collisions by repeatedly generating the person until a unique name is found.

**Parameters**:

- `attempt` (int): The current attempt number. This is used to track the number of times the LLM has been called to generate an agent specification.

**Returns**:

- `dict | None`: Returns a dictionary containing the agent specification if a unique name is generated, otherwise returns `None`.


### `_aux_model_call(self, messages, temperature, frequency_penalty, presence_penalty)`

**Purpose**: This auxiliary function makes a model call to OpenAI's LLM using the `openai_utils` module and returns the response in JSON format. The function is wrapped in the `transactional` decorator for caching purposes.

**Parameters**:

- `messages` (list): A list of messages to be sent to the LLM.
- `temperature` (float): The temperature to use when sampling from the LLM.
- `frequency_penalty` (float): The frequency penalty to apply when sampling from the LLM.
- `presence_penalty` (float): The presence penalty to apply when sampling from the LLM.

**Returns**:

- `dict | None`: Returns a dictionary containing the LLM response, otherwise returns `None`.

### `_setup_agent(self, agent, configuration)`

**Purpose**: This function sets up the `TinyPerson` instance with the necessary elements based on the provided configuration. It includes persona definitions and ensures that the agent is correctly configured for the simulation. The function is wrapped in the `transactional` decorator for caching purposes.

**Parameters**:

- `agent` (`TinyPerson`): The `TinyPerson` instance to be configured.
- `configuration` (dict): The configuration dictionary containing the agent's details.

**Returns**:

- `None`: The function does not return any value.
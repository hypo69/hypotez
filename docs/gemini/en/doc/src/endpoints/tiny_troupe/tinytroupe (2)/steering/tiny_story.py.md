# TinyStory: TinyTroupe Narrative Generation 

## Overview

This module, `tiny_story.py`, is a crucial component of the TinyTroupe project. It provides functionality for generating narratives within TinyTroupe simulations. The `TinyStory` class acts as a helper mechanism for crafting engaging and realistic stories based on agent interactions and environment details.

## Details

The `TinyStory` class facilitates the creation of narratives that encapsulate the essence of TinyTroupe simulations. It allows users to create stories that are contextualized by the simulation's history, incorporating information about agents, environments, and their interactions.

## Classes

### `TinyStory`

**Description**: The `TinyStory` class is responsible for generating and managing narratives within TinyTroupe simulations. It leverages the `TinyPerson` class to represent agents and the `TinyWorld` class to represent environments, allowing for stories that are grounded in the simulation's context.

**Inherits**: This class does not inherit from any other class.

**Attributes**:

- `environment` (`TinyWorld`): The environment in which the story takes place.
- `agent` (`TinyPerson`): The agent featured in the story.
- `purpose` (`str`): The overarching purpose of the story.
- `current_story` (`str`): The current narrative content.
- `first_n` (`int`): Number of initial interactions to include in the story.
- `last_n` (`int`): Number of recent interactions to include in the story.
- `include_omission_info` (`bool`): Whether to include information about omitted interactions.

**Methods**:

- `__init__(self, environment: TinyWorld = None, agent: TinyPerson = None, purpose: str = "Be a realistic simulation.", context: str = "", first_n: int = 10, last_n: int = 20, include_omission_info: bool = True) -> None`
    - **Purpose**: Initializes a new `TinyStory` instance.
    - **Parameters**:
        - `environment` (`TinyWorld`, optional): The environment for the story. Defaults to `None`.
        - `agent` (`TinyPerson`, optional): The agent in the story. Defaults to `None`.
        - `purpose` (`str`, optional): The story's purpose. Defaults to "Be a realistic simulation.".
        - `context` (`str`, optional): The initial story context. Defaults to "".
        - `first_n` (`int`, optional): Number of initial interactions to include. Defaults to 10.
        - `last_n` (`int`, optional): Number of recent interactions to include. Defaults to 20.
        - `include_omission_info` (`bool`, optional): Include omission information. Defaults to `True`.
    - **Raises Exceptions**:
        - `Exception`: If both `environment` and `agent` are provided, or if neither is provided.
- `start_story(self, requirements: str = "Start some interesting story about the agents.", number_of_words: int = 100, include_plot_twist: bool = False) -> str`
    - **Purpose**: Initiates a new story.
    - **Parameters**:
        - `requirements` (`str`, optional): The requirements for the story. Defaults to "Start some interesting story about the agents.".
        - `number_of_words` (`int`, optional): Desired number of words in the story. Defaults to 100.
        - `include_plot_twist` (`bool`, optional): Include a plot twist. Defaults to `False`.
    - **Returns**:
        - `str`: The starting portion of the story generated.
- `continue_story(self, requirements: str = "Continue the story in an interesting way.", number_of_words: int = 100, include_plot_twist: bool = False) -> str`
    - **Purpose**: Generates a continuation of the existing story.
    - **Parameters**:
        - `requirements` (`str`, optional): The requirements for the continuation. Defaults to "Continue the story in an interesting way.".
        - `number_of_words` (`int`, optional): Desired number of words in the continuation. Defaults to 100.
        - `include_plot_twist` (`bool`, optional): Include a plot twist in the continuation. Defaults to `False`.
    - **Returns**:
        - `str`: The generated continuation of the story.
- `_current_story(self) -> str`
    - **Purpose**: Retrieves the current story with context.
    - **Returns**:
        - `str`: The current story content.

##  How the Class Works

The `TinyStory` class works by leveraging the `TinyPerson` and `TinyWorld` classes to gather information about the agents and environment involved in the simulation. This information is used to generate a narrative that is relevant to the simulation context. The class also uses the `openai_utils` module to interface with OpenAI's language models, allowing for dynamic story generation based on the provided parameters.

The class utilizes a system of templates to guide the story generation process. The templates are used to provide context and specific requirements for the language model, ensuring that the generated narrative is aligned with the user's expectations.

## Examples 

```python
# Creating a TinyStory instance with an agent
agent = TinyPerson()
story = TinyStory(agent=agent, purpose="Tell a story about a hero's journey")

# Starting the story
start = story.start_story(requirements="Start a story about a brave knight on a quest.")
print(start)

# Continuing the story
continuation = story.continue_story(requirements="Continue the story with a twist that changes the knight's perspective.")
print(continuation)
```

This example demonstrates how to create a `TinyStory` instance for an agent and then use the `start_story` and `continue_story` methods to generate a narrative.
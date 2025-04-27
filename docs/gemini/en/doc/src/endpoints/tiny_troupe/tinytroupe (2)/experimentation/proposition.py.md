# Proposition Module

## Overview

This module defines the `Proposition` class, which encapsulates a claim about a target (either a `TinyWorld` or a `TinyPerson`) or multiple targets within the `tinytroupe` simulation environment. 

## Details

The `Proposition` class uses a Large Language Model (LLM) to evaluate whether the given textual claim is true or false based on the provided context. This context is derived from the simulation trajectory of the target(s).

## Classes

### `Proposition`

**Description**:  Represents a propositional claim about a target or targets within the `tinytroupe` simulation.

**Inherits**:  None

**Attributes**:

- `targets` (list): A list of `TinyWorld` or `TinyPerson` objects that are the targets of the proposition.
- `claim` (str): The textual claim of the proposition.
- `first_n` (int): The number of first interactions to consider from the target's trajectory.
- `last_n` (int): The number of last (most recent) interactions to consider from the target's trajectory.
- `value` (bool): The truth value of the proposition (evaluated by the LLM).
- `justification` (str): The justification provided by the LLM for the assigned truth value.
- `confidence` (float): The confidence level expressed by the LLM in the assigned truth value.
- `raw_llm_response` (str): The raw response of the LLM in textual format.

**Methods**:

- `__call__(additional_context=None)`: A convenience method that calls `check()` with the optional `additional_context`.
- `check(additional_context="No additional context available.")`: Evaluates the proposition's truth value against the provided context and additional context.

**How the Class Works**:

The `Proposition` class works by first gathering the relevant simulation context from the specified target(s). This context includes the trajectory of interactions (e.g., actions, statements, thoughts) of the targets, potentially limited to a specified number of initial and/or final interactions. The context is then presented to the LLM along with the propositional claim. The LLM analyzes the context and determines whether the claim is true or false. The LLM's response also includes a justification for its decision and a confidence level indicating the certainty of its evaluation.

**Examples**:

```python
# Example 1: Creating a proposition about a TinyPerson
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld
from tinytroupe.openai_utils import LLMRequest

alice = TinyPerson(name="Alice")
world = TinyWorld(name="My World")

# The proposition is "Alice is happy"
prop = Proposition(alice, "Alice is happy.")
prop() # Evaluate the proposition (calls prop.check())
print(f"Proposition Value: {prop.value}")
print(f"Proposition Justification: {prop.justification}")
print(f"Proposition Confidence: {prop.confidence}")

# Example 2: Creating a proposition about a TinyWorld
prop2 = Proposition(world, "The temperature in the world is warm.")
prop2() # Evaluate the proposition (calls prop.check())
print(f"Proposition Value: {prop2.value}")
print(f"Proposition Justification: {prop2.justification}")
print(f"Proposition Confidence: {prop2.confidence}")

# Example 3: Creating a proposition about multiple targets
prop3 = Proposition([alice, world], "Alice is in the world.")
prop3() # Evaluate the proposition (calls prop.check())
print(f"Proposition Value: {prop3.value}")
print(f"Proposition Justification: {prop3.justification}")
print(f"Proposition Confidence: {prop3.confidence}")
```

## Functions

### `check_proposition`

**Purpose**:  Checks the truth value of a propositional claim without explicitly creating a `Proposition` object.

**Parameters**:

- `target` (TinyWorld, TinyPerson, list): The target or targets of the proposition.
- `claim` (str): The textual claim of the proposition.
- `additional_context` (str): Additional context to provide to the LLM.
- `first_n` (int): The number of first interactions to consider from the target's trajectory.
- `last_n` (int): The number of last (most recent) interactions to consider from the target's trajectory.

**Returns**:

- `bool`: True if the proposition holds true, False otherwise.

**Raises Exceptions**:

- None

**How the Function Works**:

The `check_proposition` function creates a temporary `Proposition` object, evaluates its truth value using the `check()` method, and returns the result. This is useful when you only need to evaluate a proposition once and don't need to store the justification or confidence information.

**Examples**:

```python
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld
from tinytroupe.openai_utils import LLMRequest

alice = TinyPerson(name="Alice")
world = TinyWorld(name="My World")

# Check if Alice is in the world
is_alice_in_world = check_proposition(alice, "Alice is in the world.")
print(f"Alice is in the world: {is_alice_in_world}")
```
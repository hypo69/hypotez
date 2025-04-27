**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use This Code Block
=========================================================================================

Description
-------------------------
This code snippet provides two functions, `rephrase` and `restructure_as_observed_vs_expected`, both utilizing the `llm` decorator from the `tinytroupe.utils` module. The functions leverage a large language model (LLM) to perform semantic-related tasks:
- `rephrase` modifies an observation based on a given rule.
- `restructure_as_observed_vs_expected` extracts key elements (observed event, broken/met expectation, reasoning) from a description.

Execution Steps
-------------------------
1. **Function `rephrase`**:
    - Takes an `observation` (a statement or description) and a `rule` as input.
    - Uses the `llm` decorator to apply an LLM model to process the input.
    - Rephrases or changes the `observation` according to the specified `rule`.
    - Returns the modified `observation` as a string.

2. **Function `restructure_as_observed_vs_expected`**:
    - Takes a `description` as input, which can describe either a real event or an abstract concept.
    - Uses the `llm` decorator to apply an LLM model to analyze the `description`.
    - Identifies if the `description` violates or meets an expectation.
    - Extracts the `OBSERVED` event, `BROKEN/MET EXPECTATION`, and `REASONING` based on the expectation violation or fulfillment.
    - Returns the restructured description with extracted elements as a string.

Usage Example
-------------------------

```python
from tinytroupe.utils.semantics import rephrase, restructure_as_observed_vs_expected

# Rephrasing an observation
observation = "You know, I am so sad these days."
rule = "I am always happy and depression is unknown to me"
modified_observation = rephrase(observation, rule)
print(modified_observation)  # Output: "You know, I am so happy these days."

# Restructuring a description
description = "Ana mentions she loved the proposed new food, a spicier flavor of gazpacho. However, this goes against her known dislike of spicy food."
restructured_description = restructure_as_observed_vs_expected(description)
print(restructured_description)  # Output:
# "OBSERVED: Ana mentions she loved the proposed new food, a spicier flavor of gazpacho.
# BROKEN EXPECTATION: Ana should have mentioned that she disliked the proposed spicier gazpacho.
# REASONING: Ana has a known dislike of spicy food."
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".
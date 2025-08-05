# Normalizer Class Documentation

## Overview

This module contains the `Normalizer` class, which normalizes textual elements like passages, concepts, and other strings. It leverages a caching mechanism to improve performance and ensures consistent ordering of elements.

## Details

The `Normalizer` class facilitates the standardization of textual elements by grouping similar inputs into distinct output elements. It first identifies and clusters similar elements and then maps each input to its corresponding normalized output, utilizing a cache for efficiency.  This class plays a crucial role in various processes within the `hypotez` project, ensuring consistency and uniformity in textual representation.

## Classes

### `Normalizer`

**Description**: This class implements a mechanism for normalizing textual elements, including passages, concepts, and other strings. It uses a caching system to improve performance and ensures consistent ordering of elements.

**Inherits**: None

**Attributes**:

- `elements` (list): A list of unique textual elements to be normalized.
- `n` (int): The number of normalized elements to output.
- `verbose` (bool):  Flag to enable or disable debug message printing. Defaults to `False`.
- `normalized_elements` (dict): A JSON-based structure representing the normalized output. Each key represents a normalized element, and its value is a list of input elements that were merged into it.
- `normalizing_map` (dict): A dictionary that maps each input element to its normalized output, serving as a cache.

**Methods**:

- `__init__(self, elements:List[str], n:int, verbose:bool=False)`: Constructor for the `Normalizer` class. It initializes the attributes and performs the initial normalization process.
- `normalize(self, element_or_elements:Union[str, List[str]]) -> Union[str, List[str]]`: Normalizes the specified element or elements. It utilizes a caching mechanism to improve performance.

## Functions

### `__init__`

**Purpose**: The constructor for the `Normalizer` class initializes its attributes and performs the initial normalization.

**Parameters**:

- `elements` (list): A list of textual elements to be normalized.
- `n` (int): The number of normalized elements to output.
- `verbose` (bool): Flag to enable or disable debug message printing. Defaults to `False`.

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:
1.  Creates a unique list of elements from the input.
2.  Initializes `normalized_elements` and `normalizing_map` dictionaries.
3.  Utilizes `utils.compose_initial_LLM_messages_with_templates` to build messages for the LLM with `normalizer.system.mustache` and `normalizer.user.mustache` templates.
4.  Sends the messages to the LLM using `openai_utils.client().send_message` and receives the normalized elements.
5.  Stores the received normalized elements in the `normalized_elements` attribute.

**Examples**:

```python
# Initialize a Normalizer object
normalizer = Normalizer(elements=["apple", "banana", "apple", "orange"], n=3, verbose=True)
```

### `normalize`

**Purpose**: Normalizes the specified element or elements, using a caching mechanism to improve performance.

**Parameters**:

- `element_or_elements` (Union[str, List[str]]): The element or elements to be normalized.

**Returns**:

- `str`: The normalized element if the input was a string.
- `list`: The normalized elements if the input was a list, preserving the order of elements in the input.

**Raises Exceptions**:

- `ValueError`: If the input `element_or_elements` is neither a string nor a list.

**How the Function Works**:
1.  Processes the input `element_or_elements`, converting strings to lists if necessary.
2.  Iterates through the elements, checking if they are already in the cache ( `normalizing_map` ). If not, adds them to a list `elements_to_normalize`.
3.  If there are elements to normalize:
    - Uses `utils.compose_initial_LLM_messages_with_templates` to build messages for the LLM with `normalizer.applier.system.mustache` and `normalizer.applier.user.mustache` templates.
    - Sends the messages to the LLM using `openai_utils.client().send_message` and receives the normalized elements.
    - Updates the cache (`normalizing_map`) with the new normalized elements.
4.  Returns the normalized elements, preserving the original order.

**Examples**:

```python
# Normalize a single element
normalized_element = normalizer.normalize("apple")

# Normalize a list of elements
normalized_elements = normalizer.normalize(["apple", "banana", "orange"])
```

## Inner Functions:

### `__init__` Inner Functions:

- `utils.compose_initial_LLM_messages_with_templates(..., base_module_folder="extraction", rendering_configs=...)`: Composes messages for the LLM using the specified templates.
- `openai_utils.client().send_message(..., temperature=0.1)`: Sends messages to the LLM and retrieves the response.

### `normalize` Inner Functions:

- `utils.compose_initial_LLM_messages_with_templates(..., base_module_folder="extraction", rendering_configs=...)`: Composes messages for the LLM using the specified templates.
- `openai_utils.client().send_message(..., temperature=0.1)`: Sends messages to the LLM and retrieves the response.

## Parameter Details

- `elements` (list): A list of textual elements to be normalized.
- `n` (int): The number of normalized elements to output.
- `verbose` (bool):  Flag to enable or disable debug message printing. Defaults to `False`.
- `element_or_elements` (Union[str, List[str]]): The element or elements to be normalized.
- `rendering_configs` (dict):  A dictionary containing configurations used for composing messages for the LLM.
- `messages` (list):  A list of messages to be sent to the LLM.

## Examples

```python
# Example 1: Simple Normalization
from tinytroupe.extraction.normalizer import Normalizer

normalizer = Normalizer(elements=["apple", "banana", "apple", "orange"], n=3, verbose=True)
normalized_element = normalizer.normalize("apple")
print(f"Normalized element: {normalized_element}")

# Example 2: Normalizing a list of elements
from tinytroupe.extraction.normalizer import Normalizer

normalizer = Normalizer(elements=["apple", "banana", "apple", "orange"], n=3, verbose=True)
normalized_elements = normalizer.normalize(["apple", "banana", "orange"])
print(f"Normalized elements: {normalized_elements}")
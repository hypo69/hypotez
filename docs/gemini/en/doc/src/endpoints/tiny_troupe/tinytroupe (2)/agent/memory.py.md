# Memory Mechanisms for Tiny Troupe Agents

## Overview

This module implements memory mechanisms for agents within the Tiny Troupe project. These memory systems provide agents with the ability to store and retrieve information, enabling them to learn from past experiences and adapt their behavior.

## Details

The `hypotez/src/endpoints/tiny_troupe/tinytroupe (2)/agent/memory.py` file defines a base `TinyMemory` class and two subclasses: `EpisodicMemory` and `SemanticMemory`.  The `TinyMemory` class serves as the foundation for memory implementation, providing essential methods for storage and retrieval.

- **Episodic Memory:** Represents memory of specific events or episodes, akin to remembering a conversation or a specific action.  It stores messages in chronological order and provides methods for retrieving the first `n` messages, the last `n` messages, and a recent subset based on fixed prefix and lookback lengths.

- **Semantic Memory:**  Represents memory of meanings, understandings, and conceptual knowledge unrelated to specific experiences. It uses LlamaIndex's `BaseSemanticGroundingConnector` to store and retrieve semantic information based on relevance to a given target.

## Classes

### `TinyMemory`

**Description:** Base class for different types of memory mechanisms used by Tiny Troupe agents. It defines the common interface for storage and retrieval.

**Inherits:** N/A

**Attributes:**

- **`self.memories`**: List of memories to store.

**Methods:**

- `_preprocess_value_for_storage(self, value: Any) -> Any:`
    - **Purpose**: Preprocesses a value before storing it in memory. This step allows for any necessary transformations or formatting of the value.
    - **Parameters**:
        - `value (Any)`: The value to be preprocessed.
    - **Returns**: `Any`: The preprocessed value.
    - **How the Function Works**: By default, this method does nothing and simply returns the input value. Subclasses can override this method to perform specific preprocessing.
- `_store(self, value: Any) -> None:`
    - **Purpose**: Stores a value in memory. This method is responsible for actually placing the value into the memory storage.
    - **Parameters**:
        - `value (Any)`: The value to be stored.
    - **Returns**: `None`: The method returns `None`.
    - **How the Function Works**: This method must be implemented by subclasses. The implementation will depend on the specific memory type.
- `store(self, value: dict) -> None:`
    - **Purpose**: Stores a value in memory after preprocessing. This method combines preprocessing and storage.
    - **Parameters**:
        - `value (dict)`: The value to be stored in the memory.
    - **Returns**: `None`: The method returns `None`.
    - **How the Function Works**: Calls `_preprocess_value_for_storage` to preprocess the value and then calls `_store` to store the preprocessed value.
- `store_all(self, values: list) -> None:`
    - **Purpose**: Stores a list of values in memory.
    - **Parameters**:
        - `values (list)`: A list of values to be stored.
    - **Returns**: `None`: The method returns `None`.
    - **How the Function Works**: Iterates through the list of values and calls `store` for each value.
- `retrieve(self, first_n: int, last_n: int, include_omission_info: bool = True) -> list:`
    - **Purpose**: Retrieves values from memory based on specified criteria. This method allows for retrieving the first `n` values, the last `n` values, or both.
    - **Parameters**:
        - `first_n (int)`: The number of first values to retrieve.
        - `last_n (int)`: The number of last values to retrieve.
        - `include_omission_info (bool)`: Whether to include a message indicating that some values have been omitted. Defaults to `True`.
    - **Returns**: `list`: A list containing the retrieved values.
    - **How the Function Works**: This method must be implemented by subclasses. The implementation depends on how the memory is organized and how values are stored.
- `retrieve_recent(self) -> list:`
    - **Purpose**: Retrieves the most recent values from memory. This method provides access to the latest stored information.
    - **Parameters**: None
    - **Returns**: `list`: A list containing the most recent values.
    - **How the Function Works**: This method must be implemented by subclasses. The implementation will vary based on the specific memory structure and how recency is defined.
- `retrieve_all(self) -> list:`
    - **Purpose**: Retrieves all values from memory. This method provides access to the entire memory.
    - **Parameters**: None
    - **Returns**: `list`: A list containing all values stored in memory.
    - **How the Function Works**: This method must be implemented by subclasses. It should return a copy of the underlying memory storage.
- `retrieve_relevant(self, relevance_target: str, top_k=20) -> list:`
    - **Purpose**: Retrieves values from memory that are most relevant to a given target. This method enables searching through memory based on a search term or query.
    - **Parameters**:
        - `relevance_target (str)`: The target to which relevance is measured.
        - `top_k (int)`: The maximum number of relevant values to retrieve.
    - **Returns**: `list`: A list of values sorted by their relevance to the `relevance_target`.
    - **How the Function Works**: This method must be implemented by subclasses. The implementation will depend on how relevance is determined and how values are ranked.


### `EpisodicMemory`

**Description:** Implements episodic memory, which is a cognitive ability for remembering specific events or episodes in the past. This class stores messages in chronological order and provides methods for retrieving recent, first, last, or all stored messages.

**Inherits:** `TinyMemory`

**Attributes:**

- `fixed_prefix_length (int)`: The fixed prefix length used when retrieving recent messages. Defaults to 100. This determines how many of the oldest messages are always included in the recent message retrieval.
- `lookback_length (int)`: The lookback length used when retrieving recent messages. Defaults to 100. This determines how many messages are retrieved from the most recent part of memory.
- `memory (list)`:  A list that stores messages in chronological order. 

**Methods:**

- `_store(self, value: Any) -> None:`
    - **Purpose**: Stores a value in memory. This implementation simply appends the value to the `memory` list.
    - **Parameters**:
        - `value (Any)`: The value to be stored.
    - **Returns**: `None`: The method returns `None`.
    - **How the Function Works**: This method appends the provided `value` to the `memory` list, preserving chronological order.
- `count(self) -> int:`
    - **Purpose**: Returns the number of values stored in memory.
    - **Parameters**: None
    - **Returns**: `int`: The number of elements in the `memory` list.
    - **How the Function Works**: This method simply returns the length of the `memory` list, providing the number of stored messages.
- `retrieve(self, first_n: int, last_n: int, include_omission_info: bool = True) -> list:`
    - **Purpose**: Retrieves values from memory based on specified criteria. This method allows for retrieving the first `n` values, the last `n` values, or both.
    - **Parameters**:
        - `first_n (int)`: The number of first values to retrieve.
        - `last_n (int)`: The number of last values to retrieve.
        - `include_omission_info (bool)`: Whether to include a message indicating that some values have been omitted. Defaults to `True`.
    - **Returns**: `list`: A list containing the retrieved values.
    - **How the Function Works**: This method uses the other methods in the class to retrieve the values. It retrieves the first `n` messages using `retrieve_first` and the last `n` messages using `retrieve_last`. If both `first_n` and `last_n` are specified, it returns the concatenation of the retrieved messages. If only `first_n` is specified, it returns only the first `n` messages. If only `last_n` is specified, it returns only the last `n` messages. If neither `first_n` nor `last_n` are specified, it returns all the messages using `retrieve_all`.
- `retrieve_recent(self, include_omission_info: bool = True) -> list:`
    - **Purpose**: Retrieves the `n` most recent values from memory based on the fixed prefix length and lookback length.
    - **Parameters**:
        - `include_omission_info (bool)`: Whether to include a message indicating that some values have been omitted. Defaults to `True`.
    - **Returns**: `list`: A list containing the most recent messages.
    - **How the Function Works**: This method first retrieves the fixed prefix of the `memory` list, which includes the oldest messages up to the specified `fixed_prefix_length`. Then, it calculates the remaining lookback length (the number of messages to retrieve from the most recent part of memory) and retrieves those messages. Finally, it concatenates the fixed prefix with the retrieved lookback messages and returns the combined list. If the remaining lookback length is less than or equal to 0, the method simply returns the fixed prefix.
- `retrieve_all(self) -> list:`
    - **Purpose**: Retrieves all values from memory.
    - **Parameters**: None
    - **Returns**: `list`: A copy of the `memory` list.
    - **How the Function Works**: This method returns a copy of the `memory` list, ensuring that any modifications to the returned list do not affect the original memory.
- `retrieve_relevant(self, relevance_target: str, top_k: int) -> list:`
    - **Purpose**: Retrieves the top-k values from memory that are most relevant to a given target.
    - **Parameters**:
        - `relevance_target (str)`: The target to which relevance is measured.
        - `top_k (int)`: The maximum number of relevant values to retrieve.
    - **Returns**: `list`: A list of values sorted by their relevance to the `relevance_target`.
    - **How the Function Works**: This method raises a `NotImplementedError`. Subclasses should implement this method to handle the retrieval of relevant values based on their specific logic.
- `retrieve_first(self, n: int, include_omission_info: bool = True) -> list:`
    - **Purpose**: Retrieves the first n values from memory.
    - **Parameters**:
        - `n (int)`: The number of first values to retrieve.
        - `include_omission_info (bool)`: Whether to include a message indicating that some values have been omitted. Defaults to `True`.
    - **Returns**: `list`: A list containing the first `n` messages.
    - **How the Function Works**: This method retrieves the first `n` messages from the `memory` list using list slicing and returns them as a new list.
- `retrieve_last(self, n: int, include_omission_info: bool = True) -> list:`
    - **Purpose**: Retrieves the last n values from memory.
    - **Parameters**:
        - `n (int)`: The number of last values to retrieve.
        - `include_omission_info (bool)`: Whether to include a message indicating that some values have been omitted. Defaults to `True`.
    - **Returns**: `list`: A list containing the last `n` messages.
    - **How the Function Works**: This method retrieves the last `n` messages from the `memory` list using list slicing and returns them as a new list.

### `SemanticMemory`

**Description:**  Implements semantic memory, representing the memory of meanings, understandings, and concept-based knowledge. It uses LlamaIndex's `BaseSemanticGroundingConnector` to store and retrieve semantic information based on relevance to a given target.

**Inherits:** `TinyMemory`

**Attributes:**

- `memories (list)`: A list of memories to store. Defaults to `None`.

**Methods:**

- `_post_init(self) -> None:`
    - **Purpose**: This method is called after the `__init__` method, thanks to the `@post_init` decorator. It ensures that the `memories` attribute is initialized properly and sets up the `semantic_grounding_connector` for storing and retrieving semantic information.
    - **Parameters**: None
    - **Returns**: `None`: The method returns `None`.
    - **How the Function Works**: This method checks if the `memories` attribute is already set. If not, it initializes it as an empty list. Then, it creates a `BaseSemanticGroundingConnector` instance and adds the initial memories as documents to the connector.
- `_preprocess_value_for_storage(self, value: dict) -> Any:`
    - **Purpose**: Preprocesses a value before storing it in semantic memory. This step converts the value into a string format suitable for storage as a document in LlamaIndex.
    - **Parameters**:
        - `value (dict)`: The value to be preprocessed. It is expected to be a dictionary with keys like 'type' (e.g., 'action', 'stimulus'), 'content', and 'simulation_timestamp'.
    - **Returns**: `Any`: The preprocessed value as a string.
    - **How the Function Works**: This method checks the `type` of the input value. If it's 'action', it creates a string representation with a header '# Fact' followed by the action description and timestamp. If it's 'stimulus', it creates a string representation with a header '# Stimulus' followed by the stimulus description and timestamp. Other types of values are not currently handled.
- `_store(self, value: Any) -> None:`
    - **Purpose**: Stores a value in semantic memory after preprocessing. This method converts the value into a `Document` object and stores it in the `semantic_grounding_connector`.
    - **Parameters**:
        - `value (Any)`: The value to be stored.
    - **Returns**: `None`: The method returns `None`.
    - **How the Function Works**: This method first calls `_preprocess_value_for_storage` to preprocess the value. Then, it converts the preprocessed value into a `Document` object using the `_build_document_from` helper method and adds the document to the `semantic_grounding_connector`.
- `retrieve_relevant(self, relevance_target: str, top_k=20) -> list:`
    - **Purpose**: Retrieves the top-k values from memory that are most relevant to a given target. This method leverages the `semantic_grounding_connector` to perform semantic search and retrieve relevant information.
    - **Parameters**:
        - `relevance_target (str)`: The target to which relevance is measured.
        - `top_k (int)`: The maximum number of relevant values to retrieve. Defaults to 20.
    - **Returns**: `list`: A list of values sorted by their relevance to the `relevance_target`.
    - **How the Function Works**: This method calls the `retrieve_relevant` method of the `semantic_grounding_connector`, passing the `relevance_target` and `top_k` values. The `semantic_grounding_connector` performs semantic search and returns a list of documents sorted by their relevance. The method returns the list of documents as a list of strings.
- `_build_document_from(memory) -> Document:`
    - **Purpose**: Helper method to create a `Document` object from a memory value.
    - **Parameters**:
        - `memory (Any)`: The memory value to convert into a document.
    - **Returns**: `Document`: A LlamaIndex `Document` object representing the memory value.
    - **How the Function Works**: This method simply creates a `Document` object with the provided memory value as its text content.
- `_build_documents_from(self, memories: list) -> list:`
    - **Purpose**: Helper method to create a list of `Document` objects from a list of memory values.
    - **Parameters**:
        - `memories (list)`: A list of memory values to convert into documents.
    - **Returns**: `list`: A list of LlamaIndex `Document` objects.
    - **How the Function Works**: This method iterates through the list of memory values and calls `_build_document_from` to create a `Document` object for each value. It then returns the list of created `Document` objects.

## Inner Functions

- None

## How the Code Works

The `TinyMemory` class provides the basic functionality for memory mechanisms in Tiny Troupe agents. It defines the common interface for storing and retrieving information, including methods for preprocessing values, storing them, and retrieving them based on various criteria. 

The `EpisodicMemory` class implements a simple episodic memory system, storing messages in a list in chronological order. It allows for retrieving messages based on their position in the list (first n, last n), and provides methods for retrieving recent messages based on fixed prefix and lookback lengths.

The `SemanticMemory` class implements semantic memory, using LlamaIndex's `BaseSemanticGroundingConnector` to store and retrieve semantic information. The class preprocesses values to create appropriate document representations, stores them in the `semantic_grounding_connector`, and retrieves relevant documents based on a given target using semantic search. 

## Examples

```python
# Creating an instance of EpisodicMemory
memory = EpisodicMemory()

# Storing messages
memory.store({'type': 'stimulus', 'content': 'Hello, world!', 'simulation_timestamp': '2023-12-12T12:00:00'})
memory.store({'type': 'action', 'content': 'I responded: "Greetings!"', 'simulation_timestamp': '2023-12-12T12:01:00'})

# Retrieving the first message
first_message = memory.retrieve_first(1)
print(f'First message: {first_message}') # Output: First message: [{'type': 'stimulus', 'content': 'Hello, world!', 'simulation_timestamp': '2023-12-12T12:00:00'}]

# Retrieving the last message
last_message = memory.retrieve_last(1)
print(f'Last message: {last_message}') # Output: Last message: [{'type': 'action', 'content': 'I responded: "Greetings!"', 'simulation_timestamp': '2023-12-12T12:01:00'}]

# Retrieving the most recent messages
recent_messages = memory.retrieve_recent()
print(f'Recent messages: {recent_messages}') # Output: Recent messages: [{'type': 'stimulus', 'content': 'Hello, world!', 'simulation_timestamp': '2023-12-12T12:00:00'}, {'type': 'action', 'content': 'I responded: "Greetings!"', 'simulation_timestamp': '2023-12-12T12:01:00'}]


# Creating an instance of SemanticMemory
semantic_memory = SemanticMemory()

# Storing a semantic fact
semantic_memory.store({'type': 'action', 'content': 'I learned that the Earth is round.', 'simulation_timestamp': '2023-12-12T12:02:00'})

# Retrieving relevant information
relevant_facts = semantic_memory.retrieve_relevant("Earth is round", top_k=1)
print(f'Relevant facts: {relevant_facts}') # Output: Relevant facts: ['# Fact\nI have performed the following action at date and time 2023-12-12T12:02:00:\n\n I learned that the Earth is round.']
```

## Parameter Details

- `fixed_prefix_length (int)`: This parameter in `EpisodicMemory` determines the number of oldest messages that are always included when retrieving recent messages. A higher value means more of the oldest messages are included.
- `lookback_length (int)`: This parameter in `EpisodicMemory` determines how many messages are retrieved from the most recent part of memory when retrieving recent messages. A higher value means more recent messages are included.
- `top_k (int)`: This parameter in `SemanticMemory` and `TinyMemory` determines the maximum number of relevant values to retrieve. A higher value means more potentially relevant values are returned.
- `include_omission_info (bool)`: This parameter in `EpisodicMemory` and `TinyMemory` controls whether a message indicating that some values have been omitted is included in the retrieved results.
# TinyEnricher Module

## Overview

This module provides the `TinyEnricher` class, which is responsible for enriching content using OpenAI's models. It leverages the `openai_utils` module to interact with OpenAI's API and `utils` module to handle content manipulation and formatting.

## Details

The `TinyEnricher` class utilizes OpenAI's models to enhance textual content by incorporating user-defined requirements. This involves sending text content and associated requirements to the model, receiving enriched text, and extracting relevant code blocks from the response. 

## Classes

### `TinyEnricher`

**Description:** This class utilizes OpenAI's models to enhance textual content by incorporating user-defined requirements. It sends text content and associated requirements to the model, receives enriched text, and extracts relevant code blocks from the response. 

**Inherits:** `JsonSerializableRegistry`

**Attributes:**

- `use_past_results_in_context (bool):` A flag indicating whether to include past results in the context when interacting with the model. 
- `context_cache (list):` A list to store past results for use in the context.

**Methods:**

- `enrich_content(requirements: str, content: str, content_type: str = None, context_info: str = "", context_cache: list = None, verbose: bool = False):` 

**Purpose:** This method enriches the provided text content using OpenAI's models. It incorporates the given requirements and context information to generate enhanced text. 

**Parameters:**

- `requirements (str):` The requirements for enriching the content.
- `content (str):` The text content to be enriched.
- `content_type (str):` The type of content, such as "text", "code", or "HTML".
- `context_info (str):` Additional context information to be used for enrichment.
- `context_cache (list):` A list of previous results to be used in the context.
- `verbose (bool):` A flag indicating whether to print debug messages.

**Returns:**

- `str | None:` Returns the extracted code block from the model's response, or `None` if no code is extracted.

**How the Function Works:**

1.  The function composes LLM messages based on provided requirements, content, context information, and a pre-defined template.
2.  It sends the messages to OpenAI's API, using `openai_utils.client()`, for processing and receives a response.
3.  The response message is logged and potentially printed based on the `verbose` flag.
4.  The function attempts to extract a code block from the response using `utils.extract_code_block`.
5.  The extracted code block or `None` is returned as the enrichment result.

**Examples:**

```python
enricher = TinyEnricher()

requirements = "Generate a Python function that converts a string to uppercase."
content = "This is a sample string."

enriched_content = enricher.enrich_content(requirements, content)

if enriched_content:
    print(f"Enriched content:\n{enriched_content}")
else:
    print("No code block found in the response.")
```

## Parameter Details

- `use_past_results_in_context (bool):`  This parameter determines whether past results should be included in the context when sending messages to OpenAI's models. Setting it to `True` allows the model to consider previous interactions, potentially improving the quality of the enrichment.
- `context_cache (list):` This list stores past results, which are then included in the context when `use_past_results_in_context` is set to `True`. This helps the model maintain context and understand the overall task better.
- `requirements (str):` This parameter defines the specific requirements for enriching the content. It specifies what kind of modifications or transformations the model should apply to the input text.
- `content (str):` This parameter represents the text content that needs to be enriched. It is the actual text data that is passed to the OpenAI model for processing.
- `content_type (str):` This parameter indicates the type of content being passed to the model. This can help the model understand the context and apply appropriate enrichment techniques. For example, setting it to "code" might trigger different behavior than setting it to "text".
- `context_info (str):` This parameter provides additional context information relevant to the enrichment process. It can include details that are not explicitly present in the `content` but are helpful for the model to understand the task.
- `context_cache (list):`  This parameter allows for passing a list of previous results to be used in the context of the enrichment. This can be helpful for preserving the thread of the conversation and providing the model with relevant historical information.
- `verbose (bool):` This parameter controls whether the function should print debugging messages. Setting it to `True` enables verbose output that shows the model's responses and other internal details.

## Examples

```python
enricher = TinyEnricher()

# Example 1: Simple text enrichment
requirements = "Generate a Python function that converts a string to uppercase."
content = "This is a sample string."

result = enricher.enrich_content(requirements, content)
print(f"Enriched content: {result}")

# Example 2: Enriching with context information
requirements = "Write a Python function that takes a list of numbers and returns the sum of all even numbers."
content = "Here is a list of numbers: [1, 2, 3, 4, 5]"
context_info = "The function should only sum even numbers."

result = enricher.enrich_content(requirements, content, context_info=context_info)
print(f"Enriched content: {result}")

# Example 3: Enriching with a context cache
requirements = "Write a Python function that takes a list of words and returns the longest word."
content = "Here is a list of words: ['apple', 'banana', 'cherry']"
context_cache = ["I have already defined a function to find the shortest word in a list"]

result = enricher.enrich_content(requirements, content, context_cache=context_cache)
print(f"Enriched content: {result}")
```
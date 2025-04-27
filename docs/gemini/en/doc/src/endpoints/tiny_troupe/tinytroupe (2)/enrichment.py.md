# Module: Tiny Enricher

## Overview

The `enrichment.py` module is a crucial part of the `hypotez` project, providing a class named `TinyEnricher`. This class is designed to enrich content using a large language model (LLM) based on given requirements and context. 

## Details

The `TinyEnricher` class is responsible for leveraging LLM capabilities to enhance content based on specific requirements. It utilizes a context cache to store past results and optionally incorporates them into the LLM's input for enhanced context awareness. 

## Classes

### `TinyEnricher` 

**Description**: This class handles the enrichment of content using a large language model (LLM). It leverages a context cache to maintain a history of past results, which can be used to enhance the context of the LLM's input.

**Inherits**: `JsonSerializableRegistry`

**Attributes**:

- `use_past_results_in_context (bool)`: A flag to control whether past results from the context cache are used in the LLM input.
- `context_cache (list)`: A list to store past enrichment results.

**Methods**:

- `enrich_content(requirements: str, content:str, content_type:str =None, context_info:str ="", context_cache:list=None, verbose:bool=False)`: This method orchestrates the content enrichment process. 
    - It takes the required parameters, such as `requirements`, `content`, `content_type`, `context_info`, `context_cache`, and `verbose`, and utilizes them to construct an appropriate LLM prompt. 
    - It then uses the OpenAI API to send the prompt and receives a response. 
    - The LLM's response is then processed to extract any code blocks, which are then returned as the enrichment result.

## Functions

## Parameter Details

- `requirements (str)`: This parameter defines the specific requirements for content enrichment. It can include details like the desired output format, desired information to be included, or any specific instructions for the LLM.
- `content (str)`: This parameter represents the raw content that needs to be enriched. It can be text, HTML, code, or any other data type that can be processed by the LLM.
- `content_type (str, optional)`: This parameter provides additional context about the type of content being processed. It can be used by the LLM to better understand the input and generate more relevant results. Defaults to `None`.
- `context_info (str, optional)`: This parameter offers additional information or context related to the content. It can be used to provide the LLM with more insights about the content's source, purpose, or any other relevant details. Defaults to `""`.
- `context_cache (list, optional)`: This parameter allows the user to provide a custom context cache. Defaults to `None`, which means the class will use its internal context cache.
- `verbose (bool, optional)`: This parameter controls the verbosity of the output. If set to `True`, the method will print additional debug messages. Defaults to `False`.

## Examples

```python
# Example 1:  Simple content enrichment
requirements = "Rewrite the following text into a more professional tone."
content = "This is a pretty cool product. You should buy it!"
enricher = TinyEnricher()
enriched_content = enricher.enrich_content(requirements, content)
print(enriched_content) # This will print the enriched content 

# Example 2:  Using a custom context cache
requirements = "Translate this English sentence into Spanish."
content = "This is a very interesting product."
context_cache = ["The product is innovative and well-designed."]
enricher = TinyEnricher()
enriched_content = enricher.enrich_content(requirements, content, context_cache=context_cache)
print(enriched_content) # This will print the translated Spanish sentence

# Example 3: Using a verbose setting 
requirements = "Generate a Python function that calculates the sum of two numbers."
content = ""
enricher = TinyEnricher(verbose=True) # Set verbose to True for additional output 
enriched_content = enricher.enrich_content(requirements, content)
print(enriched_content) # This will print the generated Python function code

```

## How the Class Works

The `TinyEnricher` class works by using the OpenAI API to send requests to the LLM with the specified requirements, content, and context. The API response is then parsed to extract any code blocks that are considered the result of the enrichment process. The context cache is used to store the past results of the enrichment process, and it can be optionally passed to the `enrich_content` method.
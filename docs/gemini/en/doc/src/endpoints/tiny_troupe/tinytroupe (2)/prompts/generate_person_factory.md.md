# Generate Person Factory Prompts

## Overview

This file contains prompts for the "Generate Person Factory" module. It aims to create multiple, specific contexts based on a broad initial context, focusing on generating person descriptions with various demographics, characteristics, and attributes.

## Details

This module is used within the `hypotez` project to provide diverse and detailed inputs for person generation. The goal is to create a range of contexts that can then be utilized to produce different person descriptions using AI models.

## Functions

### `generate_person_factory_prompts`

**Purpose**: Generates multiple person description prompts based on a broad context.

**Parameters**:

- `broad_context` (str): The initial, general context that describes the overall characteristics of the desired person descriptions. 

**Returns**:

- `list[str]`: An array containing multiple person description prompts that are derived from the provided `broad_context`.

**Raises Exceptions**:

- `None`

**How the Function Works**:

The function takes a `broad_context` and parses it to extract key details about the desired person descriptions. These details can include demographics, personality traits, beliefs, economic status, etc. The function then uses this information to generate a list of more specific prompts, each of which will be used to generate a unique person description.

**Examples**:

```python
broad_context = "Generate 3 person descriptions based on the following broad context: Latin American, age between 20 and 40 years old, economic status can vary between poor and rich, it can be religious or not, it can be married or not, it can have children or not, it can be a professional or not, it can be a worker or not"

prompts = generate_person_factory_prompts(broad_context)

print(prompts)
```

Output:

```
["Mexican person that has formed as lawyer but now works in other are, is single, like sports and movies", "Create a Brazilian person that is a doctor, like pets and the nature and love heavy metal.", "Create a Colombian person that is a lawyer, like to read and drink coffee and is married with 2 children."]
```


**Inner Functions**:

- **`_parse_broad_context`**: This function takes the `broad_context` and extracts key details about the desired person descriptions. 
- **`_generate_specific_prompts`**: This function uses the extracted details to generate multiple, specific prompts. 

**Example of `_parse_broad_context`**:

```python
def _parse_broad_context(broad_context: str) -> dict:
    """
    Extracts key details from the broad context.
    
    Args:
        broad_context (str): The initial, general context.
    
    Returns:
        dict: A dictionary containing the extracted details.
    
    Examples:
        >>> _parse_broad_context("Generate 3 person descriptions based on the following broad context: Latin American, age between 20 and 40 years old, economic status can vary between poor and rich, it can be religious or not, it can be married or not, it can have children or not, it can be a professional or not, it can be a worker or not")
        {'region': 'Latin American', 'age_range': '20-40', 'economic_status': ['poor', 'rich'], 'religion': ['yes', 'no'], 'marital_status': ['married', 'single'], 'children': ['yes', 'no'], 'profession': ['yes', 'no'], 'worker': ['yes', 'no']}
    """
    # ...
    
    return extracted_details
```

**Example of `_generate_specific_prompts`**:

```python
def _generate_specific_prompts(extracted_details: dict) -> list[str]:
    """
    Generates specific prompts based on extracted details.
    
    Args:
        extracted_details (dict): The details extracted from the broad context.
    
    Returns:
        list[str]: A list of specific person description prompts.
    
    Examples:
        >>> _generate_specific_prompts({'region': 'Latin American', 'age_range': '20-40', 'economic_status': ['poor', 'rich'], 'religion': ['yes', 'no'], 'marital_status': ['married', 'single'], 'children': ['yes', 'no'], 'profession': ['yes', 'no'], 'worker': ['yes', 'no']})
        ['Mexican person that is a lawyer, likes to read and drink coffee, and is married with 2 children.', 'Create a Brazilian person who is a doctor, enjoys pets and nature, and loves heavy metal.', 'Create a Colombian person who is a lawyer, loves sports and movies, and is single.']
    """
    # ...
    
    return specific_prompts
```
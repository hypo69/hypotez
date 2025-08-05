# Generate Person Prompts Factory

## Overview

This module contains functions for generating prompts to be used in generating person descriptions. 

## Details

This factory is designed to take a broad context about a person and break it down into smaller, more specific contexts.  These specific contexts are then used as prompts to generate individual person descriptions.

## Functions

### `generate_person_contexts(context: str) -> list[str]`

**Purpose**: Takes a general context about a person and creates a list of more specific prompts for generating person descriptions.

**Parameters**:

- `context` (str):  A description of the general person you want to generate.

**Returns**:

- `list[str]`:  A list of more specific prompts for generating person descriptions, based on the input `context`.

**Example**:

```python
>>> context = "Please, generate 3 person(s) description(s) based on the following broad context: Latin American, age between 20 and 40 years old, economic status can vary between poor and rich, it can be religious or not, it can be married or not, it can have children or not, it can be a professional or not, it can be a worker or not"
>>> generate_person_contexts(context)
['Mexican person that has formed as lawyer but now works in other are, is single, like sports and movies', 'Create a Brazilian person that is a doctor, like pets and the nature and love heavy metal.', 'Create a Colombian person that is a lawyer, like to read and drink coffee and is married with 2 children.']
``` 

**How the Function Works**:

1. The function first analyzes the input `context` to identify key details about the person. This includes:
    - Country of Origin
    - Age Range
    - Economic Status
    - Religious Beliefs
    - Marital Status
    - Children
    - Profession
    - Job
2. Based on these details, the function generates a list of more specific prompts. Each prompt includes a combination of specific details, like:
    - "Mexican person" (Country of Origin)
    - "that has formed as lawyer" (Profession)
    - "but now works in other are" (Job)
    - "is single" (Marital Status)
    - "like sports and movies" (Interests) 

The goal is to create prompts that are specific enough to guide the generation of a unique and interesting person description while still staying within the overall parameters of the initial `context`.

**Inner Functions**: (None)
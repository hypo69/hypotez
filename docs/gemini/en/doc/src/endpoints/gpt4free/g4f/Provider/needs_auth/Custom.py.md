# Custom Provider for GPT4Free

## Overview

This module defines custom providers for the GPT4Free service, extending the `OpenaiTemplate` class. 

## Details

This file contains two classes: `Custom` and `Feature`. Both classes inherit from `OpenaiTemplate` and provide custom configurations for interacting with the GPT4Free service.

## Classes

### `Custom`

**Description**: The `Custom` class represents a custom provider for GPT4Free. This provider has a label, working status, and authentication requirements. It also defines an API base URL and a setting to sort models.

**Inherits**: `OpenaiTemplate`

**Attributes**:

- `label (str)`: The label of the provider, which is "Custom Provider".
- `working (bool)`: A boolean indicating whether the provider is currently operational (set to `True`).
- `needs_auth (bool)`: A boolean indicating whether the provider requires authentication (set to `False`).
- `api_base (str)`: The base URL for the provider's API, set to `"http://localhost:8080/v1"`.
- `sort_models (bool)`: A boolean indicating whether models should be sorted (set to `False`).

**Methods**: None

### `Feature`

**Description**: The `Feature` class represents another custom provider for GPT4Free. It inherits from the `Custom` class and provides a specific label and working status.

**Inherits**: `Custom`

**Attributes**:

- `label (str)`: The label of the provider, which is "Feature Provider".
- `working (bool)`: A boolean indicating whether the provider is currently operational (set to `False`).

**Methods**: None

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.Custom import Custom

# Creating a Custom provider instance
custom_provider = Custom()

# Accessing attributes
print(custom_provider.label) # Output: "Custom Provider"
print(custom_provider.working) # Output: True
print(custom_provider.api_base) # Output: "http://localhost:8080/v1"
```

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.Custom import Feature

# Creating a Feature provider instance
feature_provider = Feature()

# Accessing attributes
print(feature_provider.label) # Output: "Feature Provider"
print(feature_provider.working) # Output: False
```
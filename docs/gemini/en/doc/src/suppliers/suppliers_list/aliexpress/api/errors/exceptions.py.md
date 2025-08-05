# AliExpress API Exceptions

## Overview

This module defines custom exceptions used for handling errors related to the AliExpress API. These exceptions provide specific information about the nature of the error encountered during API interactions.

## Details

This module is part of the `hypotez` project, which focuses on product data management. The `aliexpress` package within `hypotez` is responsible for interacting with the AliExpress API to retrieve product information. The `errors` sub-package within `aliexpress` defines custom exceptions to handle specific errors that might occur during API communication.

This module ensures clear error handling and allows developers to distinguish between different types of errors encountered during interactions with the AliExpress API.

## Classes

### `AliexpressException`

**Description**: This is the base class for all AliExpress API exceptions. It provides a common structure and functionality for handling API errors.

**Attributes**:

- `reason` (str): A string describing the reason for the exception.

**Methods**:

- `__str__`(): Returns a string representation of the exception, including the reason.

### `InvalidArgumentException`

**Description**: This exception is raised when provided arguments are not valid or are in an incorrect format.

**Inherits**: `AliexpressException`

### `ProductIdNotFoundException`

**Description**: This exception is raised when a specified product ID cannot be found in the AliExpress API.

**Inherits**: `AliexpressException`

### `ApiRequestException`

**Description**: This exception is raised when a request to the AliExpress API fails, indicating an error in the communication process.

**Inherits**: `AliexpressException`

### `ApiRequestResponseException`

**Description**: This exception is raised when the response received from the AliExpress API is not valid or does not meet expected requirements.

**Inherits**: `AliexpressException`

### `ProductsNotFoudException`

**Description**: This exception is raised when no products are found based on the search criteria provided to the AliExpress API.

**Inherits**: `AliexpressException`

### `CategoriesNotFoudException`

**Description**: This exception is raised when no categories matching the specified criteria are found in the AliExpress API.

**Inherits**: `AliexpressException`

### `InvalidTrackingIdException`

**Description**: This exception is raised when the provided tracking ID is either missing or invalid.

**Inherits**: `AliexpressException`

## Parameter Details

- `reason` (str): A human-readable description of the specific error that occurred.

## Examples

```python
try:
    # Make an API request to AliExpress
    response = api_client.get_product_details(product_id='1234567890')
except ProductIdNotFoundException as ex:
    logger.error(f"Product ID not found: {ex.reason}", ex, exc_info=True)
    # Handle the error appropriately
```

This code demonstrates how to catch a `ProductIdNotFoundException` and handle it gracefully. The `reason` attribute provides a clear error message, and `logger.error` logs the error with detailed information.

## How the Exceptions Work

These custom exceptions provide a structured way to handle errors specific to the AliExpress API. By inheriting from the base `AliexpressException` class, they share common functionality for error reporting and management. 

When an error occurs during API interaction, the corresponding exception is raised. This allows developers to catch the specific exception and handle it based on the nature of the error. 

For instance, if a product ID is not found, the `ProductIdNotFoundException` is raised. This exception informs developers that the product ID provided was incorrect or the product is not available on AliExpress.

## Conclusion

The custom exceptions defined in this module provide a robust mechanism for handling errors that arise from interactions with the AliExpress API. They offer a structured approach to error handling, making it easier for developers to identify and address issues related to the AliExpress API.
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
This code snippet defines three functions for working with URLs:

1. **`extract_url_params(url: str) -> dict | None`**: Extracts query parameters from a URL string.

2. **`is_url(text: str) -> bool`**: Validates if a given text string is a valid URL using the `validators` library.

3. **`url_shortener(long_url: str) -> str | None`**: Shortens a long URL using the TinyURL service.

Execution Steps
-------------------------
1. **`extract_url_params(url: str) -> dict | None`**:
    - The function takes a URL string as input.
    - It parses the URL using `urllib.parse.urlparse` to separate its components.
    - It extracts the query parameters from the parsed URL using `urllib.parse.parse_qs`.
    - The function converts single-valued parameters from a list to a string.
    - It returns a dictionary containing the extracted parameters and their values, or `None` if the URL doesn't contain parameters.

2. **`is_url(text: str) -> bool`**:
    - The function takes a text string as input.
    - It validates the text string using `validators.url` to check if it's a valid URL.
    - It returns `True` if the string is a valid URL, otherwise `False`.

3. **`url_shortener(long_url: str) -> str | None`**:
    - The function takes a long URL string as input.
    - It constructs a URL for TinyURL's API using the input URL.
    - It sends a GET request to the TinyURL API using the constructed URL.
    - If the response status code is 200 (success), it returns the shortened URL from the response text.
    - Otherwise, it returns `None`, indicating an error occurred during URL shortening.


Usage Example
-------------------------

```python
    # Example Usage:
    url = "https://www.example.com?param1=value1&param2=value2"
    params = extract_url_params(url)
    print(params) # Output: {'param1': 'value1', 'param2': 'value2'}

    text = "https://www.example.com"
    is_valid = is_url(text)
    print(is_valid) # Output: True

    long_url = "https://www.example.com/long-url"
    short_url = url_shortener(long_url)
    print(short_url) # Output: (Example: https://tinyurl.com/12345678)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".
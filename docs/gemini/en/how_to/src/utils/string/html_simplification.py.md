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
The `simplify_html` function cleans and simplifies HTML code, focusing on the content within the `<body>` tag. 
It leverages the `Config` object (which can be provided or defaults to `Config()`) to control simplification rules like tag removal, attribute filtering, comment removal, script/style handling, whitespace normalization, and potentially removing container tags without meaningful content (`keep_only_significant` flag). The function aims to extract and present the core content from HTML while retaining desired formatting and elements based on configuration.

Execution Steps
-------------------------
1. **Isolate `<body>` content**: The function first parses the provided HTML using the specified parser (defaulting to `html.parser`) and identifies the `<body>` tag. If `<body>` is not found, it attempts to process the entire content as a fragment.
2. **Process isolated content**: After extracting the `<body>` content, the function:
    - **Removes comments, scripts, styles**: If enabled in `config`, it removes HTML comments, `<script>` tags, and `<style>` tags with their contents.
    - **Removes insignificant containers**: If `keep_only_significant` is True, the function iterates through tags in reverse order, identifying and removing containers that lack meaningful content (no text, no significant child tags). 
    - **Final tag/attribute processing**:
        - **Unwrap tags**: If `config.unwrap_tags` is set, it unwraps (removes) these tags, leaving their contents.
        - **Filter tags**: Removes tags not included in `config.allowed_tags`.
        - **Filter attributes**: Removes attributes from tags unless they are present in `config.allowed_attributes`.
3. **Generate final HTML**: The function retrieves the HTML representation of the processed `soup` object and, if `normalize_whitespace` is enabled, replaces multiple spaces with single spaces and removes leading/trailing whitespace.

Usage Example
-------------------------

```python
from src.utils.string.html_simplification import simplify_html, Config

sample_html = """
    <!DOCTYPE html>
    <html>
    <body>
        <div id="main" class="container">
            <h1>   Пример    HTML   </h1>
            <p style="margin: 10px;" class="main-text first">
                Это <b>первый</b> абзац с <a href="http://example.com" title="Visit">ссылкой</a>.
                Содержит <span class="highlight">   ненужный   </span> & важный текст.
            </p>
        </div>
    </body>
    </html>
    """

# Example 1: Using default config
simplified_html_default = simplify_html(sample_html)
print(simplified_html_default)

# Example 2: Customizing config to allow specific attributes
custom_config = Config(
    allowed_attributes={'a': {'href', 'title'}, 'img': {'src', 'alt'}, '*': {'class', 'id', 'style'}}
)
simplified_html_custom = simplify_html(sample_html, config=custom_config)
print(simplified_html_custom)

# Example 3: Removing insignificant containers and unwrapping certain tags
significant_config = Config(
    allowed_tags={'p', 'b', 'a', 'br', 'img', 'h1', 'hr', 'div'},
    allowed_attributes={'a': {'href'}, 'img': {'src', 'alt'}, '*': {'style'}},
    unwrap_tags={'span', 'footer'},
    keep_only_significant=True
)
simplified_html_significant = simplify_html(sample_html, config=significant_config)
print(simplified_html_significant)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".
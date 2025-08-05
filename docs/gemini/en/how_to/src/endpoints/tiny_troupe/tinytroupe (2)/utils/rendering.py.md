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
[Explanation of what the code does.]

Execution Steps
-------------------------
1. [Description of the first step.]
2. [Description of the second step.]
3. [Continue as needed...]

Usage Example
-------------------------

```python
    [Code usage example]
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".
```

## How to Use the `rendering.py` Module

This module contains utility functions for rendering and formatting text and data in the `tinytroupe` project.

### `inject_html_css_style_prefix()`

**Description:**
This function injects a style prefix to all style attributes in the given HTML string.

**Execution Steps:**
1. It takes an HTML string and a style prefix string as input.
2. It replaces the `style="` string in the HTML with `style="${style_prefix_attributes};"`.
3. It returns the modified HTML string.

**Usage Example:**

```python
html_string = '<div style="color: red;">Hello</div>'
style_prefix = 'font-size: 20px;'

modified_html = inject_html_css_style_prefix(html_string, style_prefix)

print(modified_html)
# Output: <div style="font-size: 20px; color: red;">Hello</div>
```

### `break_text_at_length()`

**Description:**
This function breaks the text (or JSON) at the specified length, inserting a "(...)" string at the break point.

**Execution Steps:**
1. It checks if the input text is a dictionary, and if so, converts it to a JSON string.
2. It checks if the maximum length is specified. If not, it returns the text as is.
3. If the maximum length is specified and the text length exceeds it, it truncates the text to the specified length and adds "(...)" at the end.
4. It returns the truncated text or the original text.

**Usage Example:**

```python
text = "This is a very long text string that needs to be truncated."
max_length = 20

truncated_text = break_text_at_length(text, max_length)

print(truncated_text)
# Output: This is a very long (...)
```

### `pretty_datetime()`

**Description:**
This function returns a pretty string representation of the specified datetime object.

**Execution Steps:**
1. It takes a datetime object as input.
2. It formats the datetime object using the `strftime()` method with the format string "%Y-%m-%d %H:%M".
3. It returns the formatted string.

**Usage Example:**

```python
from datetime import datetime

dt = datetime.now()

pretty_date = pretty_datetime(dt)

print(pretty_date)
# Output: 2023-10-26 15:34 (for example)
```

### `dedent()`

**Description:**
This function dedents the specified text, removing any leading whitespace and indentation.

**Execution Steps:**
1. It uses the `textwrap.dedent()` method to remove leading whitespace and indentation.
2. It strips any leading or trailing whitespace using the `strip()` method.
3. It returns the dedented and stripped text.

**Usage Example:**

```python
text = """
This is a text with indentation.
    This line is indented.
"""

dedented_text = dedent(text)

print(dedented_text)
# Output:
# This is a text with indentation.
# This line is indented.
```

### `wrap_text()`

**Description:**
This function wraps the text at the specified width.

**Execution Steps:**
1. It uses the `textwrap.fill()` method to wrap the text at the specified width.
2. It returns the wrapped text.

**Usage Example:**

```python
text = "This is a very long text string that needs to be wrapped at a specific width."
width = 40

wrapped_text = wrap_text(text, width)

print(wrapped_text)
# Output:
# This is a very long text string that
# needs to be wrapped at a specific
# width.
```

### `RichTextStyle` Class

**Description:**
This class provides a set of static methods for retrieving predefined styles for different types of text.

**Execution Steps:**
1. It defines class variables for different text styles, for example:
    - `STIMULUS_CONVERSATION_STYLE`
    - `STIMULUS_THOUGHT_STYLE`
    - `ACTION_DONE_STYLE`
    - `ACTION_TALK_STYLE`
    - `INTERVENTION_DEFAULT_STYLE`
2. It provides a `get_style_for()` method that takes the kind of text (e.g., "stimulus", "action") and the event type (e.g., "CONVERSATION", "TALK") as input.
3. It returns the corresponding style based on the input parameters.

**Usage Example:**

```python
style = RichTextStyle.get_style_for("stimulus", "CONVERSATION")
print(style)
# Output: bold italic cyan1

style = RichTextStyle.get_style_for("action", "TALK")
print(style)
# Output: bold green3
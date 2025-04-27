**How to Use the `pprint` Function**

=========================================================================================

**Description**
-------------------------
The `pprint` function in `src/utils/printer.py` provides a way to print data to the console in a human-readable format with optional text styling. It supports printing various data types, including dictionaries, lists, strings, and file paths. You can customize the output with colors, background colors, and font styles.

**Execution Steps**
-------------------------
1. **Import the `pprint` function:** Import the `pprint` function from the `src.utils.printer` module.
2. **Call the `pprint` function:** Pass the data you want to print as the first argument.
3. **Specify styling parameters (optional):** You can optionally provide the `text_color`, `bg_color`, and `font_style` parameters to customize the appearance of the output.

**Usage Example**
-------------------------

```python
from src.utils.printer import pprint

# Print a dictionary with green text
pprint({"name": "Alice", "age": 30}, text_color="green")

# Print a list with blue text and bold font
pprint(["apple", "banana", "cherry"], text_color="blue", font_style="bold")

# Print a string with yellow text, red background, and underlined font
pprint("text example", text_color="yellow", bg_color="bg_red", font_style="underline")
```

**Key Points**

- **Data Type Handling:** The `pprint` function automatically handles different data types, providing appropriate formatting.
- **Styling Options:** The `TEXT_COLORS`, `BG_COLORS`, and `FONT_STYLES` dictionaries offer various color, background, and font style options.
- **Error Handling:** The function includes error handling to gracefully handle unsupported data types or printing errors.
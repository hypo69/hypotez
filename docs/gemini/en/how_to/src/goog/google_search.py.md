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
The `GoogleHtmlParser` class provides functionality for parsing HTML from Google Search results pages and converting them into a dictionary. It works with both mobile and desktop versions of the HTML.

Execution Steps
-------------------------
1. The class is initialized with a HTML string and a user agent (either "mobile" or "desktop").
2. The `_clean` method removes unnecessary characters, such as spaces and special characters, from a given string.
3. The `_normalize_dict_key` method normalizes a string for use as a dictionary key by replacing spaces with underscores, removing colons, and converting to lowercase.
4. The `_get_estimated_results` method extracts the estimated number of search results from the HTML.
5. The `_get_organic` method extracts organic search results (without additional features like snippets, featured snippets, etc.) and stores them in a list of dictionaries.
6. The `_get_featured_snippet` method checks for a featured snippet and returns a dictionary containing its title and URL if found.
7. The `_get_knowledge_card` method retrieves a knowledge card and returns a dictionary containing its title, subtitle, description, and additional information if found.
8. The `_get_scrolling_sections` method extracts data from scrollable widgets (e.g., top stories or tweets) and returns a list of dictionaries.
9. The `get_data` method assembles all the extracted data into a comprehensive dictionary.

Usage Example
-------------------------

```python
from src.goog.google_search import GoogleHtmlParser

html_string = """
    <html>
    </html>
"""

parser = GoogleHtmlParser(html_string, user_agent='desktop')
search_data = parser.get_data()

print(search_data)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".
**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use This Code Block
========================================================================================

Description
-------------------------
This code block implements a function called `search_query` that searches for movies or TV series on Google using the Kinopoisk.ru website. It takes a search query and a type of media (movie or series) as inputs.

Execution Steps
-------------------------
1. The function constructs a Google search query that specifically targets the Kinopoisk.ru website for the specified media type.
2. It sends a request to Google's search engine with the constructed query, user agent, and language settings.
3. The response is parsed using BeautifulSoup to extract relevant information, such as links, titles, and descriptions.
4. For each result found, it checks if the link contains a Kinopoisk.ru movie or series ID. If so, it extracts the link, title, and description and returns them in a dictionary.
5. If no relevant results are found, the function returns None.

Usage Example
-------------------------

```python
from apps.search import search_query

# Search for the TV series "The Big Bang Theory"
result = search_query("The Big Bang Theory", type_movie="series")

# Print the search result
print(result)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".
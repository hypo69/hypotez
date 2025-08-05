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
This code block provides functions for performing web searches using DuckDuckGo and scraping text from web pages, then integrating the search results into a user prompt.

Execution Steps
-------------------------
1. **Import necessary libraries**: Imports modules for web requests (`aiohttp`), JSON manipulation (`json`), hashing (`hashlib`), file path handling (`pathlib`), URL parsing (`urllib.parse`), date and time handling (`datetime`), and potential external libraries like `duckduckgo_search`, `bs4` (BeautifulSoup), and `spacy`.
2. **Define classes `SearchResults` and `SearchResultEntry`**: These classes represent the search results and individual search entries, respectively. They store information like title, URL, snippet, and extracted text.
3. **`scrape_text` function**: This function parses HTML content to extract relevant text and images. It searches for specific HTML elements, extracts text, and optionally limits the word count or adds a source link.
4. **`fetch_and_scrape` function**: This asynchronous function fetches the HTML content of a given URL using `aiohttp`, scrapes text using `scrape_text`, and caches the results for faster retrieval later.
5. **`search` function**: This asynchronous function performs a DuckDuckGo search using `ddgs.text`. It filters out Google results, creates `SearchResultEntry` objects, and optionally extracts full text from the URLs.
6. **`do_search` function**: This asynchronous function handles the web search process. It takes a user prompt, extracts a search query if needed, performs the search using `search`, caches the results, and integrates the search results into the prompt, along with instructions for the language model.
7. **`get_search_message` function**: This function wraps `do_search` and provides a synchronous interface for performing searches. It handles potential errors like missing requirements or DuckDuckGo exceptions.
8. **`spacy_get_keywords` function**: This function (optional, depending on `spacy` availability) uses the spaCy library to extract keywords from text, potentially improving search query generation.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.tools.web_search import get_search_message

# Example user prompt
prompt = "What are the benefits of using Python for data science?"

# Perform a web search and integrate results into the prompt
new_prompt = get_search_message(prompt, max_results=3, max_words=500)

# The 'new_prompt' will contain the original prompt along with the web search results
# and instructions for the language model to use the information.

print(new_prompt)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".
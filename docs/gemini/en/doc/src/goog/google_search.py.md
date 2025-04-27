# Module: Google HTML Parser 

## Overview

This module provides the `GoogleHtmlParser` class, designed for parsing HTML content from Google Search results pages. It converts the HTML structure into a structured dictionary, making it easier to extract and analyze the information presented.  The parser supports both mobile and desktop versions of Google Search results. 

## Details

The `GoogleHtmlParser` class utilizes the `lxml` library for parsing HTML content. It extracts various components from the results page, such as:

- **Organic Results:** Regular search results, excluding snippets, featured snippets, and other additional features.
- **Featured Snippet:** Provides the title and URL of the featured snippet, if present.
- **Knowledge Card:** Extracts the title, subtitle, description, and additional information from the knowledge card, if available.
- **Scrolling Sections:**  Gathers data from scrollable widgets like "Top Stories" or "Tweets."

The parser processes the HTML structure, identifies relevant elements, and converts them into a dictionary containing the extracted information. This approach simplifies the process of extracting meaningful data from Google Search results.

## Classes

### `GoogleHtmlParser`

**Description**: This class parses HTML content from Google Search results pages and extracts relevant information into a dictionary. 

**Attributes**:

- `tree (html.Element)`: The HTML document tree obtained through `html.fromstring()`.
- `user_agent (str)`: The user agent used to fetch the Google Search HTML. It can be "mobile" or "desktop".

**Methods**:

- `__init__(self, html_str: str, user_agent: str = 'desktop')`: Initializes the parser, creating the document tree from the provided HTML string.
- `_clean(self, content: str) -> str`: Removes extra spaces and characters from a string.
- `_normalize_dict_key(self, content: str) -> str`: Normalizes a string for use as a dictionary key by replacing spaces with underscores, removing colons, converting to lowercase, and trimming underscores.
- `_get_estimated_results(self) -> int`:  Retrieves the estimated number of search results.
- `_get_organic(self) -> list`: Extracts organic search results without additional features.
- `_get_featured_snippet(self) -> dict | None`: Retrieves the featured snippet, if available.
- `_get_knowledge_card(self) -> dict | None`: Extracts data from the knowledge card.
- `_get_scrolling_sections(self) -> list`: Collects data from scrollable widgets.
- `get_data(self) -> dict`: Returns a dictionary containing all the extracted data from the search results page.

## Functions

### `_clean(self, content: str) -> str`

**Purpose**: This function cleans a string by removing extra spaces and characters.

**Parameters**:

- `content (str)`: The string to clean.

**Returns**:

- `str`: The cleaned string.

**How the Function Works**:

- The function first strips any leading and trailing spaces from the input string.
- It then splits the string into words and joins them back together with a single space between each word.

**Example**:

```python
>>> parser = GoogleHtmlParser('<p>  This is an example  string  with extra spaces.  </p>')
>>> parser._clean('  This is an example  string  with extra spaces.  ')
'This is an example string with extra spaces.'
```


### `_normalize_dict_key(self, content: str) -> str`

**Purpose**: This function normalizes a string for use as a dictionary key.

**Parameters**:

- `content (str)`: The string to normalize.

**Returns**:

- `str`: The normalized string.

**How the Function Works**:

- The function replaces spaces with underscores, removes colons, converts the string to lowercase, and trims any leading or trailing underscores. This ensures that the string can be safely used as a dictionary key.

**Example**:

```python
>>> parser = GoogleHtmlParser('<p>  This is an example  string  with extra spaces.  </p>')
>>> parser._normalize_dict_key('  This: is an example  string  with extra spaces.  ')
'this_is_an_example_string_with_extra_spaces'
```


### `_get_estimated_results(self) -> int`

**Purpose**: This function retrieves the estimated number of search results for desktop Google Search.

**Returns**:

- `int`: The estimated number of search results.

**How the Function Works**:

- The function uses XPath to find the element containing the estimated results count. 
- It then extracts the number from the text content and returns it as an integer.

**Example**:

```python
>>> parser = GoogleHtmlParser('<div id="result-stats">About 1,000,000 results (0.58 seconds)</div>')
>>> parser._get_estimated_results()
1000000
```


### `_get_organic(self) -> list`

**Purpose**: This function extracts organic search results from the Google Search page, excluding any additional features like snippets or featured snippets.

**Returns**:

- `list`: A list of dictionaries, each representing an organic search result.

**How the Function Works**:

- The function iterates over each "g" div element in the HTML, representing a search result.
- It extracts the URL, title, snippet, and rich snippet (if present) for each result.
- It uses XPath to locate the relevant information within each "g" div. 
- The extracted data is then organized into dictionaries and appended to the list.

**Example**:

```python
>>> parser = GoogleHtmlParser('<div class="g"><h3 class="r"><a href="https://www.example.com">Example Title</a></h3><div class="s"><span class="st">This is a snippet.</span></div></div>')
>>> parser._get_organic()
[{'url': 'https://www.example.com', 'title': 'Example Title', 'snippet': 'This is a snippet.', 'rich_snippet': None}]
```


### `_get_featured_snippet(self) -> dict | None`

**Purpose**: This function extracts the featured snippet from the Google Search page, if it exists.

**Returns**:

- `dict | None`: A dictionary containing the title and URL of the featured snippet, or `None` if no featured snippet is found.

**How the Function Works**:

- The function uses XPath to locate the "kp-blk" div element, which represents the featured snippet.
- It then extracts the title and URL from within this element. 
- If both title and URL are found, they are returned as a dictionary; otherwise, `None` is returned.

**Example**:

```python
>>> parser = GoogleHtmlParser('<div class="kp-blk"><h3 class="r"><a href="https://www.example.com">Example Featured Snippet</a></h3></div>')
>>> parser._get_featured_snippet()
{'title': 'Example Featured Snippet', 'url': 'https://www.example.com'}
```

### `_get_knowledge_card(self) -> dict | None`

**Purpose**: This function extracts data from the knowledge card, if it exists.

**Returns**:

- `dict | None`: A dictionary containing the title, subtitle, description, and additional information from the knowledge card, or `None` if no knowledge card is found.

**How the Function Works**:

- The function uses XPath to locate the "kp-wholepage" div element, which represents the knowledge card.
- It then extracts the title, subtitle, and description from within this element.
- It also extracts additional information from "div" elements containing attributes that include ":/". 
- If a knowledge card is found, the extracted data is returned as a dictionary; otherwise, `None` is returned.

**Example**:

```python
>>> parser = GoogleHtmlParser('<div class="kp-wholepage"><h2 class="r"><span>Example Knowledge Card</span></h2><div data-attrid="example:/topic"><span>Example Topic</span><span>Example Description</span></div></div>')
>>> parser._get_knowledge_card()
{'title': 'Example Knowledge Card', 'subtitle': '', 'description': '', 'more_info': [{'example_topic': 'Example Description'}]}
```

### `_get_scrolling_sections(self) -> list`

**Purpose**: This function extracts data from scrollable widgets, such as "Top Stories" or "Tweets".

**Returns**:

- `list`: A list of dictionaries, each representing a scrollable widget.

**How the Function Works**:

- The function uses XPath to locate "g-section-with-header" elements, representing scrollable sections.
- It extracts the title of each section and then iterates over the "g-inner-card" elements within the section.
- For each "g-inner-card", it extracts the title and URL of the data within the section.
- The extracted data is organized into dictionaries and appended to the list.

**Example**:

```python
>>> parser = GoogleHtmlParser('<div class="g-section-with-header"><h3>Top Stories</h3><div class="g-inner-card"><div role="heading">Example Story Title</div><a href="https://www.example.com">Example URL</a></div></div>')
>>> parser._get_scrolling_sections()
[{'section_title': 'Top Stories', 'section_data': [{'title': 'Example Story Title', 'url': 'https://www.example.com'}]}]
```

### `get_data(self) -> dict`

**Purpose**: This function gathers all the extracted data from the Google Search results page and returns it as a dictionary.

**Returns**:

- `dict`: A dictionary containing all the extracted data, including organic results, knowledge card, featured snippet, and data from scrollable widgets.

**How the Function Works**:

- The function calls the respective extraction methods (`_get_estimated_results`, `_get_featured_snippet`, `_get_knowledge_card`, `_get_organic`, `_get_scrolling_sections`) to retrieve the data.
- The extracted data is organized into a single dictionary.

**Example**:

```python
>>> parser = GoogleHtmlParser('<div class="g-section-with-header"><h3>Top Stories</h3><div class="g-inner-card"><div role="heading">Example Story Title</div><a href="https://www.example.com">Example URL</a></div></div>')
>>> parser.get_data()
{'estimated_results': 0, 'featured_snippet': None, 'knowledge_card': None, 'organic_results': [], 'scrolling_widgets': [{'section_title': 'Top Stories', 'section_data': [{'title': 'Example Story Title', 'url': 'https://www.example.com'}]}]}
```
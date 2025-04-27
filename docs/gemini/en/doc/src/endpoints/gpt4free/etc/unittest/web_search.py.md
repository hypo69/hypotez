# Unit Tests for Web Search Functionality

## Overview

This module contains unit tests for the web search functionality within the `hypotez` project. These tests focus on verifying the integration of the `search_tool` with the GPT-4Free API and ensure proper handling of web search results.

## Details

The tests in this file utilize `YieldProviderMock` to simulate the behavior of the actual web search provider and verify that the `search_tool` is correctly invoked with the expected arguments. The tests also validate the format of the tool calls and the expected responses from the GPT-4Free API when using the `search_tool`.

## Classes

### `TestIterListProvider`

**Description**: This class defines a set of unit tests for verifying the web search functionality within the GPT-4Free API.

**Inherits**: `unittest.IsolatedAsyncioTestCase`

**Attributes**: None

**Methods**:

- `test_search()`: Tests the web search functionality by sending a user request to the GPT-4Free API and checking the presence of the `search_tool` invocation in the generated response.

- `test_search2()`: Performs another test for web search functionality, similar to `test_search()`, but focuses on different aspects of the web search configuration.

- `test_search3()`: Conducts a third test for web search functionality, verifying the use of JSON encoding in the `search_tool` call.

## Functions

## Parameter Details

- `query` (str): The search query to be used for the web search.

- `max_results` (int): The maximum number of search results to retrieve.

- `max_words` (int): The maximum number of words to use from the search results for generating the response.

- `backend` (str): Specifies the backend used for web search. Options include "html" or "lite".

- `add_text` (bool): Indicates whether to scrape websites and include extracted text in the response.

- `timeout` (int): The timeout in seconds for scraping websites.

- `region` (str): The geographical region for the search.

- `instructions` (str): Specific instructions for the GPT-4Free API when generating a response based on the search results.

## Examples

```python
# Example of a call to the search_tool:
tool_calls = [
    {
        "function": {
            "arguments": {
                "query": "search query",
                "max_results": 5,
                "max_words": 500,
                "backend": "html",
                "add_text": True,
                "timeout": 5,
                "region": "wt-wt",
                "instructions": "Using the provided web search results, to write a comprehensive reply to the user request.\n"
                                "Make sure to add the sources of cites using [[Number]](Url) notation after the reference. Example: [[0]](http://google.com)",
            },
            "name": "search_tool"
        },
        "type": "function"
    }
]

# Example of a test case:
async def test_search(self):
    client = AsyncClient(provider=YieldProviderMock)
    tool_calls = [
        {
            "function": {
                "arguments": {
                    "query": "search query",  # content of last message: messages[-1]["content"]
                    "max_results": 5,  # maximum number of search results
                    "max_words": 500,  # maximum number of used words from search results for generating the response
                    "backend": "html",  # or "lite", "api": change it to pypass rate limits
                    "add_text": True,  # do scraping websites
                    "timeout": 5,  # in seconds for scraping websites
                    "region": "wt-wt",
                    "instructions": "Using the provided web search results, to write a comprehensive reply to the user request.\n"
                                    "Make sure to add the sources of cites using [[Number]](Url) notation after the reference. Example: [[0]](http://google.com)",
                },
                "name": "search_tool"
            },
            "type": "function"
        }
    ]
    try:
        response = await client.chat.completions.create([{"content": "", "role": "user"}], "", tool_calls=tool_calls)
        self.assertIn("Using the provided web search results", response.choices[0].message.content)
    except DuckDuckGoSearchException as e:
        self.skipTest(f'DuckDuckGoSearchException: {e}')
```
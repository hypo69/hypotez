# Grounding Connectors

## Overview

This module defines various classes that implement the concept of grounding connectors within the `hypotez` project. Grounding connectors serve as a bridge between the agent and external knowledge sources, such as files, web pages, databases, and more. They enable the agent to retrieve relevant information from these sources, effectively grounding its knowledge within the real world.

## Details

The primary goal of grounding connectors is to provide a mechanism for agents to access and utilize information from external sources. This is crucial for building agents that can reason and respond to queries based on a broader context than just their internal memory.

The module implements several types of grounding connectors, each designed for a specific type of knowledge source.

## Classes

### `GroundingConnector`

**Description:**

An abstract base class that defines the common interface for all grounding connectors. It represents the fundamental principles of grounding, including retrieving relevant information based on a given target and listing available sources.

**Inherits:**

- `JsonSerializableRegistry`

**Attributes:**

- `name` (str): The name of the grounding connector.

**Methods:**

- `retrieve_relevant(relevance_target:str, source:str, top_k=20) -> list:`
    - Retrieves all values from memory that are relevant to a given target.
    - **Parameters:**
        - `relevance_target` (str): The target string for relevance retrieval.
        - `source` (str): The source from which to retrieve relevant information.
        - `top_k` (int, optional): The number of top-k relevant results to retrieve. Defaults to 20.
    - **Returns:**
        - `list`: A list of relevant information strings.
    - **Raises Exceptions:**
        - `NotImplementedError`: If the subclass doesn't implement this method.
- `retrieve_by_name(name:str) -> str:`
    - Retrieves a content source by its name.
    - **Parameters:**
        - `name` (str): The name of the content source.
    - **Returns:**
        - `str`: The content source associated with the given name.
    - **Raises Exceptions:**
        - `NotImplementedError`: If the subclass doesn't implement this method.
- `list_sources() -> list:`
    - Lists the names of the available content sources.
    - **Returns:**
        - `list`: A list of source names.
    - **Raises Exceptions:**
        - `NotImplementedError`: If the subclass doesn't implement this method.


### `BaseSemanticGroundingConnector`

**Description:**

A base class for semantic grounding connectors. It inherits from `GroundingConnector` and introduces the concept of indexing and retrieving documents using semantic search techniques based on embeddings.

**Inherits:**

- `GroundingConnector`

**Attributes:**

- `documents` (list): A list of documents stored in the grounding connector.
- `name_to_document` (dict): A dictionary mapping document names to their corresponding documents.

**Methods:**

- `_post_init()`:
    - This method is called after the `__init__` method due to the `@post_init` decorator.
    - It initializes the `index` attribute and ensures that `documents` and `name_to_document` are properly set.
- `retrieve_relevant(relevance_target:str, top_k=20) -> list:`
    - Retrieves all values from memory that are relevant to a given target.
    - **Parameters:**
        - `relevance_target` (str): The target string for relevance retrieval.
        - `top_k` (int, optional): The number of top-k relevant results to retrieve. Defaults to 20.
    - **Returns:**
        - `list`: A list of relevant information strings.
- `retrieve_by_name(name:str) -> list:`
    - Retrieves a content source by its name.
    - **Parameters:**
        - `name` (str): The name of the content source.
    - **Returns:**
        - `list`: A list of content sources associated with the given name.
- `list_sources() -> list:`
    - Lists the names of the available content sources.
    - **Returns:**
        - `list`: A list of source names.
- `add_document(document, doc_to_name_func=None) -> None:`
    - Indexes a document for semantic retrieval.
    - **Parameters:**
        - `document`: The document to be indexed.
        - `doc_to_name_func`: An optional function to extract the name from the document.
- `add_documents(new_documents, doc_to_name_func=None) -> list:`
    - Indexes documents for semantic retrieval.
    - **Parameters:**
        - `new_documents`: A list of documents to be indexed.
        - `doc_to_name_func`: An optional function to extract the name from the document.


### `LocalFilesGroundingConnector`

**Description:**

A specialized grounding connector for local files. It inherits from `BaseSemanticGroundingConnector` and provides methods for indexing and retrieving data from files located within the filesystem.

**Inherits:**

- `BaseSemanticGroundingConnector`

**Attributes:**

- `folders_paths` (list): A list of paths to folders containing the files to be indexed.

**Methods:**

- `_post_init()`:
    - This method is called after the `__init__` method due to the `@post_init` decorator.
    - It initializes the `loaded_folders_paths` attribute and ensures that `folders_paths` is properly set.
- `add_folders(folders_paths:list) -> None:`
    - Adds a path to a folder with files used for grounding.
    - **Parameters:**
        - `folders_paths` (list): A list of folder paths to add to the grounding index.
- `add_folder(folder_path:str) -> None:`
    - Adds a path to a folder with files used for grounding.
    - **Parameters:**
        - `folder_path` (str): The path to the folder to add.
- `add_file_path(file_path:str) -> None:`
    - Adds a path to a file used for grounding.
    - **Parameters:**
        - `file_path` (str): The path to the file to add.
- `_mark_folder_as_loaded(folder_path:str) -> None:`
    - Marks a folder as loaded.
    - **Parameters:**
        - `folder_path` (str): The path to the folder to mark as loaded.

### `WebPagesGroundingConnector`

**Description:**

A grounding connector specifically designed for web pages. It inherits from `BaseSemanticGroundingConnector` and provides methods for retrieving and indexing data from web URLs.

**Inherits:**

- `BaseSemanticGroundingConnector`

**Attributes:**

- `web_urls` (list): A list of web URLs to be indexed and retrieved from.

**Methods:**

- `_post_init()`:
    - This method is called after the `__init__` method due to the `@post_init` decorator.
    - It initializes the `loaded_web_urls` attribute and ensures that `web_urls` is properly set.
- `add_web_urls(web_urls:list) -> None:`
    - Adds the data retrieved from the specified URLs to grounding.
    - **Parameters:**
        - `web_urls` (list): A list of URLs to add to the grounding index.
- `add_web_url(web_url:str) -> None:`
    - Adds the data retrieved from the specified URL to grounding.
    - **Parameters:**
        - `web_url` (str): The URL to add.
- `_mark_web_url_as_loaded(web_url:str) -> None:`
    - Marks a web URL as loaded.
    - **Parameters:**
        - `web_url` (str): The URL to mark as loaded.


## Parameter Details

- `relevance_target` (str): The target string for relevance retrieval. This is the input query or phrase that the grounding connector uses to identify relevant information.
- `source` (str): The source from which to retrieve relevant information. This can be a file path, a web URL, or any other type of identifier that specifies the knowledge source.
- `top_k` (int, optional): The number of top-k relevant results to retrieve. This parameter controls the number of results returned based on their relevance to the target. Defaults to 20.
- `name` (str): The name of the content source or grounding connector. This is used to identify and access specific sources within the grounding system.
- `document`:  A document object representing a unit of content. This can be a file, a web page, or any other piece of text or data that is indexed for retrieval.
- `doc_to_name_func`: An optional function to extract the name from a document. This is helpful for associating documents with specific names or identifiers.
- `folders_paths` (list): A list of paths to folders containing the files to be indexed. This parameter is used to specify the locations of files within the filesystem.
- `folder_path` (str): The path to a folder containing files used for grounding. This is used to add individual folders to the grounding index.
- `file_path` (str): The path to a file used for grounding. This is used to add individual files to the grounding index.
- `web_urls` (list): A list of web URLs to be indexed and retrieved from. This parameter specifies the URLs of web pages that should be included in the grounding index.
- `web_url` (str): The URL of a web page to be added to the grounding index. This is used to add individual URLs to the grounding index.

## Examples

```python
# Creating a local files grounding connector
connector = LocalFilesGroundingConnector(folders_paths=["/path/to/folder1", "/path/to/folder2"])

# Indexing a file
connector.add_file_path("/path/to/file.txt")

# Retrieving relevant information
results = connector.retrieve_relevant("Search query", top_k=10)

# Printing the results
for result in results:
    print(result)

# Creating a web pages grounding connector
web_connector = WebPagesGroundingConnector(web_urls=["https://example.com", "https://another.example.com"])

# Indexing a web URL
web_connector.add_web_url("https://www.wikipedia.org")

# Retrieving relevant information
web_results = web_connector.retrieve_relevant("Information about a specific topic", top_k=5)

# Printing the web results
for web_result in web_results:
    print(web_result)

```

## How it Works

Grounding connectors are essential for agents that need to access and utilize information from external sources. The process generally involves the following steps:

1. **Initialization:** The grounding connector is initialized with the necessary parameters, such as file paths, web URLs, or other configurations.
2. **Indexing:** The grounding connector indexes the specified content sources, such as files or web pages. This involves converting the content into a format that can be efficiently searched and retrieved. In semantic grounding connectors, this often involves creating embeddings for each document.
3. **Retrieval:** When the agent needs to retrieve information, it provides a relevance target or query to the grounding connector. The connector then performs a search based on the target and returns the most relevant results.
4. **Content Processing:** The retrieved content is then processed and incorporated into the agent's knowledge base or used to generate responses to user queries.

## Your Behavior During Code Analysis

- Inside the code, you might encounter expressions between `<` `>`. For example: `<instruction for gemini model:Loading product descriptions into PrestaShop.>, <next, if available>. These are placeholders where you insert the relevant value.
- Always refer to the system instructions for processing code in the `hypotez` project (the first set of instructions you translated);
- Analyze the file's location within the project. This helps understand its purpose and relationship with other files. You will find the file location in the very first line of code starting with `## \\file /...`;
- Memorize the provided code and analyze its connection with other parts of the project;
- In these instructions, do not suggest code improvements. Strictly follow point 5. **Example File** when composing the response.
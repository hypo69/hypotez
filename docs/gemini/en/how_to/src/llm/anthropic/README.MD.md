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

## How to Use This Code Block
=========================================================================================

### Description
This code block defines a reStructuredText (reST) directive for referencing the `src.ai.anthropic` module within documentation.

### Execution Steps
1. The code inserts an `rst` directive that references the `src.ai.anthropic` module in the documentation.
2. This directive ensures that when the documentation is built, the `src.ai.anthropic` module is properly linked and referenced.

### Usage Example
```python
   ```rst
   .. module:: src.ai.anthropic
   ```
```

## How to Use This Code Block
=========================================================================================

### Description
This code block creates a table for navigation within the `hypotez` project's repository, providing links to relevant README files.

### Execution Steps
1. The code generates an HTML table using tags like `<TABLE>`, `<TR>`, and `<TD>`.
2. The table structure is designed to display links to parent and sibling README files within the `hypotez` repository.
3. Each table cell (`<TD>`) contains a link (`<A HREF>`) to a specific README file, directing users to different sections of the project's documentation.
4. The table structure is organized to represent a hierarchical structure of README files.

### Usage Example
```python
<TABLE >
<TR>
<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/README.MD'>[Root ↑]</A>
</TD>
<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/src/README.MD'>src</A> /
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/src/ai/README.MD'>ai</A>
</TD>
<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/src/ai/anthropic/readme.ru.md'>Русский</A>
</TD>
</TABLE>
```

## How to Use This Code Block
=========================================================================================

### Description
This code block creates a header for a README file within the `src.ai.anthropic` directory.

### Execution Steps
1. The code begins with a header (`#`) and a brief description of the module.
2. The header "Claude Anthropic Client" clearly identifies the purpose of the module and its connection to the Anthropic API.

### Usage Example
```python
### README.md

# Claude Anthropic Client
```

## How to Use This Code Block
=========================================================================================

### Description
This code block provides instructions for installing the necessary library (`anthropic`) for interacting with the Claude language model.

### Execution Steps
1. The code block explains the purpose of the installation.
2. It provides a `bash` command (`pip install anthropic`) to install the library using the `pip` package manager.

### Usage Example
```python
## Installation

To use this module, you need to install the `anthropic` library:

```bash
pip install anthropic
```
```

## How to Use This Code Block
=========================================================================================

### Description
This code block demonstrates how to initialize the `ClaudeClient` with the Anthropic API key.

### Execution Steps
1. The code imports the `ClaudeClient` class from the `claude_client` module.
2. It defines a variable `api_key` to store the user's Anthropic API key.
3. It creates an instance of `ClaudeClient` using the provided `api_key`.

### Usage Example
```python
### Initialization

First, initialize the `ClaudeClient` with your Anthropic API key:

```python
from claude_client import ClaudeClient

api_key = "your-api-key"
claude_client = ClaudeClient(api_key)
```
```

## How to Use This Code Block
=========================================================================================

### Description
This code block provides an example of using the `ClaudeClient` to generate text based on a given prompt.

### Execution Steps
1. The code defines a prompt string containing a request for a short story.
2. It calls the `generate_text` method of the `claude_client` instance, passing the prompt as an argument.
3. It stores the generated text in the `generated_text` variable.
4. It prints the generated text to the console.

### Usage Example
```python
### Generate Text

Generate text based on a given prompt:

```python
prompt = "Write a short story about a robot learning to love."
generated_text = claude_client.generate_text(prompt)
print("Generated Text:", generated_text)
```
```

## How to Use This Code Block
=========================================================================================

### Description
This code block demonstrates how to analyze the sentiment of a given text using the `ClaudeClient`.

### Execution Steps
1. The code defines a text string containing a sentence expressing happiness.
2. It calls the `analyze_sentiment` method of the `claude_client` instance, passing the text as an argument.
3. It stores the sentiment analysis result in the `sentiment_analysis` variable.
4. It prints the sentiment analysis result to the console.

### Usage Example
```python
### Analyze Sentiment

Analyze the sentiment of a given text:

```python
text_to_analyze = "I am very happy today!"
sentiment_analysis = claude_client.analyze_sentiment(text_to_analyze)
print("Sentiment Analysis:", sentiment_analysis)
```
```

## How to Use This Code Block
=========================================================================================

### Description
This code block demonstrates how to translate text from one language to another using the `ClaudeClient`.

### Execution Steps
1. The code defines a text string to translate.
2. It specifies the source and target languages using language codes (`en` for English and `es` for Spanish).
3. It calls the `translate_text` method of the `claude_client` instance, passing the text, source language, and target language as arguments.
4. It stores the translated text in the `translated_text` variable.
5. It prints the translated text to the console.

### Usage Example
```python
### Translate Text

Translate text from one language to another:

```python
text_to_translate = "Hello, how are you?"
source_language = "en"
target_language = "es"
translated_text = claude_client.translate_text(text_to_translate, source_language, target_language)
print("Translated Text:", translated_text)
```
```

## How to Use This Code Block
=========================================================================================

### Description
This code block provides a complete example of using the `ClaudeClient`, demonstrating its usage for text generation, sentiment analysis, and text translation.

### Execution Steps
1. The code imports the `ClaudeClient` class from the `claude_client` module.
2. It initializes the `ClaudeClient` with the user's Anthropic API key.
3. It demonstrates the use of the `generate_text`, `analyze_sentiment`, and `translate_text` methods.
4. It prints the results of each operation to the console.

### Usage Example
```python
## Example Code

Here is a complete example of how to use the `ClaudeClient`:\

```python
from claude_client import ClaudeClient

api_key = "your-api-key"
claude_client = ClaudeClient(api_key)

# Generate text
prompt = "Write a short story about a robot learning to love."
generated_text = claude_client.generate_text(prompt)
print("Generated Text:", generated_text)

# Analyze sentiment
text_to_analyze = "I am very happy today!"
sentiment_analysis = claude_client.analyze_sentiment(text_to_analyze)
print("Sentiment Analysis:", sentiment_analysis)

# Translate text
text_to_translate = "Hello, how are you?"
source_language = "en"
target_language = "es"
translated_text = claude_client.translate_text(text_to_translate, source_language, target_language)
print("Translated Text:", translated_text)
```
```

## How to Use This Code Block
=========================================================================================

### Description
This code block defines the `generate_text` method of the `ClaudeClient` class, which generates text based on a given prompt.

### Execution Steps
1. The method takes the `prompt` and `max_tokens_to_sample` as parameters.
2. The code implements the logic for generating text using the `anthropic` library, and the result is returned as a string.

### Usage Example
```python
### `generate_text(prompt, max_tokens_to_sample=100)`

Generates text based on the given prompt.

- **Parameters:**
  - `prompt`: The prompt to generate text from.
  - `max_tokens_to_sample`: The maximum number of tokens to generate.
- **Returns:** The generated text.
```

## How to Use This Code Block
=========================================================================================

### Description
This code block defines the `analyze_sentiment` method of the `ClaudeClient` class, which analyzes the sentiment of a given text.

### Execution Steps
1. The method takes the `text` as a parameter.
2. The code implements the logic for sentiment analysis using the `anthropic` library, and the result is returned as a dictionary containing sentiment information.

### Usage Example
```python
### `analyze_sentiment(text)`

Analyzes the sentiment of the given text.

- **Parameters:**
  - `text`: The text to analyze.
- **Returns:** The sentiment analysis result.
```

## How to Use This Code Block
=========================================================================================

### Description
This code block defines the `translate_text` method of the `ClaudeClient` class, which translates a given text from one language to another.

### Execution Steps
1. The method takes the `text`, `source_language`, and `target_language` as parameters.
2. The code implements the logic for text translation using the `anthropic` library, and the translated text is returned as a string.

### Usage Example
```python
### `translate_text(text, source_language, target_language)`

Translates the given text from the source language to the target language.

- **Parameters:**
  - `text`: The text to translate.
  - `source_language`: The source language code.
  - `target_language`: The target language code.
- **Returns:** The translated text.
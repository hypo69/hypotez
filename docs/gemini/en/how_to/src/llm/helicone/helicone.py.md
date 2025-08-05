**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use the HeliconeAI Class
=========================================================================================

Description
-------------------------
The `HeliconeAI` class provides functionality to interact with the Helicone API for various AI tasks, including text generation, sentiment analysis, text summarization, and translation. The class utilizes the `OpenAI` library to interact with the OpenAI API and uses the `Helicone` library to log API calls for monitoring and analysis.

Execution Steps
-------------------------
1. **Initialize HeliconeAI Instance**: Create an instance of the `HeliconeAI` class, which initializes the `Helicone` and `OpenAI` clients.
2. **Call Functions for AI Tasks**: Use the provided methods within the `HeliconeAI` class to perform AI tasks such as:
    - `generate_poem(prompt: str)`: Generates a poem based on the provided prompt.
    - `analyze_sentiment(text: str)`: Analyzes the sentiment of the given text.
    - `summarize_text(text: str)`: Creates a concise summary of the provided text.
    - `translate_text(text: str, target_language: str)`: Translates the text into the specified target language.
3. **Log API Calls**:  Each function call logs the API request and response using the `Helicone` client.

Usage Example
-------------------------

```python
from src.ai.helicone.helicone import HeliconeAI

helicone_ai = HeliconeAI()

poem = helicone_ai.generate_poem("Write me a poem about a cat.")
print("Generated Poem:\n", poem)

sentiment = helicone_ai.analyze_sentiment("Today was a great day!")
print("Sentiment Analysis:\n", sentiment)

summary = helicone_ai.summarize_text("This is a long text for summarization...")
print("Summary:\n", summary)

translation = helicone_ai.translate_text("Hello, how are you?", "Russian")
print("Translation:\n", translation)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".
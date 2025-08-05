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
The `AIBrowserAgent` class creates a browser agent that uses a language model to perform tasks. The agent can search for information in Google and analyze web pages, and it can be customized with a custom driver.

Execution Steps
-------------------------
1. The `AIBrowserAgent` class is initialized with an OpenAI API key, model name, and search engine.
2. The `run_task` method executes a task provided by the user, which is a text prompt that describes the desired task.
    - It creates a `browser_use` agent, using either the default Playwright driver or a custom driver provided by the user.
    - The agent executes the task and returns the results as a string.
    - The `find_product_alternatives` method searches the web for product alternatives based on a given URL or SKU.
3. The `ask` and `ask_async` methods provide synchronous and asynchronous interfaces for asking questions to the agent. 

Usage Example
-------------------------

```python
from src.ai.openai.chat_openai.browser_agent import AIBrowserAgent

# Initialize the agent
agent = AIBrowserAgent(api_key="YOUR_API_KEY", model_name="gpt-4o-mini", search_engine="google")

# Find product alternatives
sku = '1493001'
product_url = None  # "https://www.apple.com/iphone-14/"  # Replace with a product URL
alternatives = await agent.find_product_alternatives(product_url=product_url, sku=sku)
if alternatives:
    print("Найденные аналоги:")
    print(alternatives)
else:
    print("Не удалось найти аналоги.")

# Ask a question
question = "Какая сейчас погода в Москве?"
answer = await agent.ask_async(question)  # Use the asynchronous method directly
if answer:
    print("Ответ на вопрос:")
    print(answer)
else:
    print("Не удалось получить ответ на вопрос.")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".
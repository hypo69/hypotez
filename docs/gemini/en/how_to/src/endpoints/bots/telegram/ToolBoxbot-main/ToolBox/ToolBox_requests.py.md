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
The code snippet defines a `ToolBox` class, which is the main class for handling requests and interactions with the Telegram bot. It initializes the bot, sets up various request handlers for different scenarios, and provides methods for processing text and image requests.

Execution Steps
-------------------------
1. **Initialization**:
    - The class initializes variables related to buttons and prompts.
    - It loads prompts from the `prompts.json` file.
    - It initializes the Telegram bot using the `TOKEN` environment variable.
    - It sets up various request handlers, such as `start_request`, `restart`, `OneTextArea`, `SomeTextsArea`, `ImageArea`, `FreeArea`, `TariffArea`, etc.

2. **Request Handling**:
    - The class defines methods for different types of requests:
        - `Text_types`: Handles text type selection (e.g., commercial, SMM, etc.).
        - `Basic_tariff` and `Pro_tariff`: Processes tariff selection and payment.
        - `TextCommands`: Handles text requests and sends them to the GPT-4o mini model.
        - `SomeTextsCommand`: Processes requests for multiple texts.
        - `ImageCommand`: Handles image requests and sends them to the FLUX schnell model.
        - `Image_Regen_And_Upscale`: Processes image regeneration and upscaling requests.
        - `FreeCommand`: Handles requests in free mode.

3. **Processing Requests**:
    - The class utilizes the `PromptsCompressor` class for preparing prompts for the AI models.
    - It uses the `__gpt_4o_mini` method for processing text requests using GPT-4o mini.
    - It uses the `__FLUX_schnell` method for processing image requests using FLUX schnell.

Usage Example
-------------------------

```python
# Initialize the ToolBox class
toolbox = ToolBox()

# Handle a start request
@toolbox.bot.message_handler(commands=['start'])
def handle_start(message):
    toolbox.start_request(message)

# Handle a text request
@toolbox.bot.message_handler(func=lambda message: message.text in toolbox.data)
def handle_text_request(message):
    # Determine the request type based on the message text
    if message.text == "text":
        toolbox.Text_types(message)
    elif message.text == "images":
        toolbox.ImageArea(message)
    elif message.text == "free":
        toolbox.FreeArea(message)
    elif message.text == "tariff":
        toolbox.TariffArea(message)

# Run the Telegram bot
toolbox.bot.polling()
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".
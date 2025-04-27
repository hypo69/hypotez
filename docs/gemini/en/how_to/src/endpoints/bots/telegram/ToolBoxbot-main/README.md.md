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

Description
-------------------------
This code snippet generates an HTML string that represents the welcome message for the Toolbox Telegram bot. The message provides an overview of the bot's capabilities, including:

- Content generation for various tasks using neural network models.
- Creative brainstorming and concept suggestion.
- Image generation based on descriptions.
- Podcast, webinar, and video transcription.

Execution Steps
-------------------------
1. The code begins by defining an HTML `<h1>` tag with the text "Toolbox AI".
2. It then defines an `<h3>` tag with the text "🛠 Welcome to Toolbox! This is a universal assistant that can generate content for various work tasks!".
3. The code proceeds to create several `<p>` tags to describe the bot's features and benefits. 
4. It uses bold tags (`<b>`) to highlight important information, such as the need to choose a task, provide input, and receive ready-made content.
5. Finally, the code includes a `P.S.` section to inform users about the free generation limit and available tariff plans.

Usage Example
-------------------------

```python
# This code snippet is meant to be used within a Telegram bot's response message. 
# It is not meant to be executed as a standalone script. 

# Example of how to use the code snippet in a Telegram bot:
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# ... (rest of the bot code)

def start(update: Update, context: CallbackContext):
    """
    Sends the welcome message when the user starts the bot.
    """
    welcome_message = "```python\n                <h1>Toolbox AI</h1>\n<h3>🛠 Welcome to Toolbox! This is a universal assistant that can generate content for various work tasks!</h3>\n\n<p>With Toolbox, you always have powerful neural network-based tools at your fingertips for writing compelling texts, generating creative ideas, and creating visual content. Forget about tasteless templates and the agony of creativity!</p>\n\n<p>🖋 Thanks to neural network models, you can easily create unique texts for SMM, email newsletters, SEO promotion, advertising campaigns, and much more. Just <b>choose the task you need</b>, write the <b>input</b>, and get the <b>ready-made content</b> as a result.</p>\n\n<p>💡 Toolbox will easily brainstorm and suggest fresh creative concepts for implementation.</p>\n\n<p>🖼 In addition to texts, the bot also allows you to generate images based on a description. Create visual content for posts, banners, illustrations from scratch - without photo banks and designers.</p>\n\n<p>🎙 Save time and automate the transcription of podcasts, webinars, and videos using the built-in function.</p>\n\n<p>Ready to try Toolbox and simplify your life? Just choose the command you need. I'll be happy to help with any task!</p>\n\n<p>P.S. You have <b>5 free generations</b> to get acquainted with the service. Then you can choose a tariff plan that covers all your work tasks!</p>\n\n                ```"
    update.message.reply_text(welcome_message, parse_mode='HTML')

# ... (rest of the bot code)
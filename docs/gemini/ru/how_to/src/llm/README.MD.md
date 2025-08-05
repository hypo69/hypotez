## \file hypotez/src/llm/README.MD
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
.. module:: src.llm
:platform: Windows, Unix
:synopsis:  LLM Management for Hypothesis (hypotez) 
"""

<TABLE >
<TR>
<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/README.MD'>[Root ↑]</A>
</TD>
<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/src/README.MD'>src</A> 
</TD>

<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/src/llm/readme.ru.md'>Русский</A>
</TD>
</TABLE>

### **llm Module**: Large Language Model Management for Hypothesis (hypotez)

The **llm** module is responsible for managing interaction with Large Language Models (LLMs) within the Hypothesis project. It provides an abstraction layer for working with various LLM APIs, facilitating seamless integration of different LLM providers.

### **Structure**

The `llm` module comprises of following submodules:

1. **anthropic**
    Provides an interface to Anthropic AI models for tasks related to advanced language understanding and response generation.
    [Go to module](https://github.com/hypo69/hypotez/blob/master/src/llm/anthropic/README.MD)

2. **dialogflow**
    Integrates with Google Dialogflow for natural language understanding (NLU) and conversational AI functionalities.
    [Go to module](https://github.com/hypo69/hypotez/blob/master/src/llm/dialogflow/README.MD)

3. **gemini**
    Facilitates interaction with Gemini AI models, supporting applications that require unique capabilities of Gemini AI.
    [Go to module](https://github.com/hypo69/hypotez/blob/master/src/llm/gemini/README.MD)

4. **helicone**
    Connects to Helicone models, providing access to specialized functions for AI-based solution customization.
    [Go to module](https://github.com/hypo69/hypotez/blob/master/src/llm/helicone/README.MD)

5. **llama**
    Provides an interface to LLaMA (Large Language Model Meta AI) for natural language understanding and generation tasks.
    [Go to module](https://github.com/hypo69/hypotez/blob/master/src/llm/llama/README.MD)

6. **myai**
    Custom AI submodule for specialized model configurations and implementations, offering unique AI functions specific to the project.
    [Go to module](https://github.com/hypo69/hypotez/blob/master/src/llm/myai/README.MD)

7. **openai**
    Integrates with OpenAI API, providing access to models like GPT for tasks including text generation, classification, and translation.
    [Go to module](https://github.com/hypo69/hypotez/blob/master/src/llm/openai/README.MD)

8. **tiny_troupe**
    Connects to Microsoft's AI models, enabling natural language processing and data analysis using smaller, optimized models.
    [Go to module](https://github.com/hypo69/hypotez/blob/master/src/llm/tiny_troupe/README.MD)

9. **revai**
    Integrates with rev.com's model, specializing in processing audio files such as recordings of meetings and calls.
    [Go to module](https://github.com/hypo69/hypotez/blob/master/src/llm/revai/README.MD)

10. **prompts**
    Provides system and command prompts in markdown format for AI models.

### **Contribution**

Contributions are welcome! Feel free to submit a pull request or open an issue if you encounter any problems or have suggestions for improvement.

### **License**

This project is licensed under the MIT License. See the [LICENSE](../../LICENSE) file for details.
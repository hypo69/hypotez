# # \file /src/ai/openai/__init__.py
# -*- coding: utf-8 -*-

# ! .pyenv/bin/python3

""".. Module :: src.ai.openai 
	: Platform: Windows, Unix
	: synopsis: Model of the `Openai` model"""


from .translator import translate
from .model import OpenAIModel
from .chat_open_ai.browser_agent import AIBrowserAgent 


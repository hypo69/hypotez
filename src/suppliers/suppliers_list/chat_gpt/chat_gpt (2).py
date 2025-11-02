## \file /src/suppliers/chat_gpt/chat_gpt (2).py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.chat_gpt 
	:platform: Windows, Unix
	:synopsis:

"""


"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
	:platform: Windows, Unix
	:synopsis:

"""

"""
  :platform: Windows, Unix

"""
"""
  :platform: Windows, Unix
  :platform: Windows, Unix
  :synopsis:
"""
  
""" module: src.suppliers.chat_gpt """




import json
from types import SimpleNamespace
from typing import Dict
from pathlib import Path
from itertools import zip_longest

import header
from src import gs
from src.logger.logger import logger
from src.webdriver.selenium.driver import Driver, Chrome

from src.utils.jjson import j_dumps, j_loads, j_loads_ns
from src.utils.printer import pprint

driver = Driver(Chrome)
locator = j_loads_ns(gs.path.src / 'suppliers' / 'chat_gpt' / 'locators' / 'chat.json')



def determine_sentiment(conversation_pair: Dict[str, str],sentiment:str='positive')  -> str:
    """ Determine sentiment label for a conversation pair """
    user_text = conversation_pair["user"]
    assistant_text = conversation_pair["assistant"]
    
    # Simple rule-based sentiment determination (replace with your actual logic)
    #if "good" in user_text or "good" in assistant_text:
    if sentiment:
        return "positive"
    else:
        return "negative"

def save_conversations_to_jsonl(data, output_file):
    """ Save conversation pairs to a JSONL file """
    ...
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    
    ...

def get_conversation():
    """ Collect conversations from the chatgpt page """
    ...
    conversation_directory = Path(gs.path.google_drive / 'chat_gpt' / 'conversation')
    html_files = conversation_directory.glob("*.html")
    
    all_conversations = []
    
    for html_file in html_files:
        file_uri = html_file.resolve().as_uri()
        driver.get(file_uri)
        
        user_elements = driver.execute_locator(locator.user)
        user_texts = [element.text for element in user_elements]
        ...
        assistant_elements = driver.execute_locator(locator.assistant)
        assistant_texts = [element.text for element in assistant_elements]
        ...

        # Combine two lists into pairs of dictionaries
        conversation_pairs = [
            {"role":"user","content": user}
            {"role":"" "completion": assistant, "sentiment": determine_sentiment({"user": user, "assistant": assistant})}
            for user, assistant in zip_longest(user_texts, assistant_texts, fillvalue="")
        ]
        d =json.dumps(conversation_pairs, ensure_ascii=False, indent=4)
        all_conversations.extend(conversation_pairs)
    
    # Save to JSONL file
    save_conversations_to_jsonl(all_conversations, gs.path.google_drive / 'chat_gpt' / 'conversation' / 'conversations.jsonl')

get_conversation()

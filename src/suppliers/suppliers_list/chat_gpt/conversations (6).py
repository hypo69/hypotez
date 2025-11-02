## \file /src/suppliers/chat_gpt/conversations (6).py
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
import re
from types import SimpleNamespace
from typing import Dict
from pathlib import Path
from itertools import zip_longest
import argparse
import asyncio
from aioconsole import ainput


import header
from src import gs
from src.logger.logger import logger
from src.suppliers.chat_gpt import GptGs
from src.webdriver.selenium.driver import Driver, Chrome, Firefox, Edge
#from src.webdriver import BS
from src.utils.jjson import j_dumps, j_loads, j_loads_ns, clean_string
from src.utils.convertors import dict2csv,json2csv
from src.utils.printer import pprint

locator = j_loads_ns(gs.path.src / 'suppliers' / 'chat_gpt' / 'locators' / 'chat.json')

class GPT_Traigner:
    """  """
    ...
    #driver:BS = BS()
    driver = Driver(Firefox)
    
    def __init__(self):
        """"""
        self.gs = GptGs()

    def determine_sentiment(self, conversation_pair: Dict[str, str], sentiment: str = 'positive') -> str:
        """ Determine sentiment label for a conversation pair """
        user_text = conversation_pair["user"]
        assistant_text = conversation_pair["assistant"]

        if sentiment:
            return "positive"
        else:
            return "negative"

    def save_conversations_to_jsonl(self, data, output_file):
        """ Save conversation pairs to a JSONL file """
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in data:
                f.write(json.dumps(clean_string(item), ensure_ascii=False) + "\n")

    def dump_downloaded_conversations(self):
        """ Collect conversations from the chatgpt page """
        conversation_directory = Path(gs.path.google_drive / 'chat_gpt' / 'conversation')
        html_files = conversation_directory.glob("*.html")

        for html_file in html_files:
            # Clean up the file path
            file_path = html_file.resolve()
            cleaned_path = re.sub(r'^.*?(c:\\)', r'\1', str(file_path))
            file_uri = Path(cleaned_path).as_uri()

            # Get the HTML content
            self.driver.get_url(file_uri)

            user_elements = self.driver.execute_locator(locator.user)
            assistant_elements = self.driver.execute_locator(locator.assistant)

            user_content = [element.text for element in user_elements]
            assistant_content = [element.text for element in assistant_elements]

            data = []

            for i in range(len(user_content)):
                data.append({'role': 'user', 'content': user_content[i]})
                data.append({'role': 'assistant', 'content': assistant_content[i], 'sentiment': 'neutral'})

            # Clean up the content in data
            cleaned_data = []
            for entry in data:
                if 'content' in entry:
                    entry['content'] = re.sub(r'^.*?c:\\', 'c:\\', entry['content'])
                cleaned_data.append(entry)
        
            # Convert file path to CSV path
            csv_file_path = gs.path.google_drive / 'chat_gpt' / 'conversation' / f'{html_file.name}.csv'
            dict2csv(cleaned_data, csv_file_path)

            # Save the cleaned conversations
            jsonl_file_path = gs.path.google_drive / 'chat_gpt' / 'conversation' / 'conversations.json'
            with open(jsonl_file_path, 'w', encoding='utf-8') as file:
                file.write(j_dumps(cleaned_data))

    async def catch_current_chat(self, num_of_chats: int = 10):
        """ Сохраняю текущее состояние чата для обучения модели """
        user_elements = self.driver.execute_locator(locator.user)
        assistant_elements = self.driver.execute_locator(locator.assistant)

        user_content = [element.text for element in user_elements]
        assistant_content = [element.text for element in assistant_elements]

        data = []
        for user_text, assistant_text in zip_longest(user_content, assistant_content):
            data.append({'role': 'user', 'content': user_text})
            if assistant_text:
                data.append({'role': 'assistant', 'content': assistant_text})

        self.gs.update_chat_worksheet(data)
        
    def grab_chat_links():
        """Собиратель ссылокк на чаты. 
        Треует ручной прокрутки списка перед запуском"""

traigner = GPT_Traigner()
traigner.dump_downloaded_conversations()
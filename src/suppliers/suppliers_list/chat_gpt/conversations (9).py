## \file /src/suppliers/chat_gpt/conversations (9).py
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



import re
import argparse
import asyncio
from pathlib import Path
from itertools import zip_longest

import pandas as pd
from aioconsole import ainput

import header
from src import gs
from src.logger.logger import logger
from src.suppliers.chat_gpt import GptGs
from src.webdriver.selenium.driver import Driver, Chrome, Firefox, Edge
from src.utils.jjson import j_dumps, j_loads, j_loads_ns, clean_string
from src.utils.convertors import dict2csv, json2csv
from src.utils.printer import pprint

locator = j_loads_ns(gs.path.src / 'suppliers' / 'chat_gpt' / 'locators' / 'chat.json')


class GPT_Traigner:
    """  """
    ...
    driver = Driver(Chrome)
    
    def __init__(self):
        """"""
        self.gs = GptGs()

    def determine_sentiment(self, conversation_pair: dict[str, str], sentiment: str = 'positive') -> str:
        """ Determine sentiment label for a conversation pair """
        if sentiment:
            return "positive"
        else:
            return "negative"

    def save_conversations_to_jsonl(self, data: list[dict], output_file: str):
        """ Save conversation pairs to a JSONL file """
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in data:
                f.write(j_dumps(clean_string(item)) + "\n")

    def dump_downloaded_conversations(self):
        """ Collect conversations from the chatgpt page """
        conversation_directory = Path(gs.path.google_drive / 'chat_gpt' / 'conversation')
        html_files = conversation_directory.glob("*.html")

        all_data = []

        for local_file_path in html_files:
            # Get the HTML content
            file_uri = local_file_path.resolve().as_uri()
            self.driver.get_url(file_uri)
            
            user_elements = self.driver.execute_locator(locator.user)
            assistant_elements = self.driver.execute_locator(locator.assistant)
            
            user_content = [element.text for element in user_elements] if user_elements else []
            assistant_content = [element.text for element in assistant_elements] if assistant_elements else []

            if not user_content and not assistant_content:
                logger.error(f"Где данные?")
                continue

            data = {
                'role': ['user'] * len(user_content) + ['assistant'] * len(assistant_content),
                'content': user_content + assistant_content,
                'sentiment': ['neutral'] * (len(user_content) + len(assistant_content))
            }
            
            all_data.append(pd.DataFrame(data))

        if all_data:
            all_data_df = pd.concat(all_data, ignore_index=True)

            # Save all accumulated results to a single CSV file
            csv_file_path = gs.path.google_drive / 'chat_gpt' / 'conversation' / 'all_conversations.csv'
            all_data_df.to_csv(csv_file_path, index=False, encoding='utf-8')

            # Save all accumulated results to a single JSONL file
            jsonl_file_path = gs.path.google_drive / 'chat_gpt' / 'conversation' / 'all_conversations.jsonl'
            all_data_df.to_json(jsonl_file_path, orient='records', lines=True, force_ascii=False)

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
        
    def grab_chat_links(self):
        """Собиратель ссылокк на чаты. 
        Треует ручной прокрутки списка перед запуском"""


traigner = GPT_Traigner()
traigner.dump_downloaded_conversations()

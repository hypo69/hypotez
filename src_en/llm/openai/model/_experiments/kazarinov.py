# # \file /src/ai/openai/model/_experiments/kazarinov.py
# -*- coding: utf-8 -*-

# ! .pyenv/bin/python3

""".. module:: src.ai.openai.model._experiments 
	:platform: Windows, Unix
	:synopsis:"""


""":platform: Windows, Unix
	:synopsis:"""

""":platform: Windows, Unix
	:synopsis:"""

""":platform: Windows, Unix"""
""":platform: Windows, Unix
  :platform: Windows, Unix
  :synopsis:"""
  
"""module: src.ai.openai.model._experiments"""


"""HERE SHOULD BE A DESCRIPTION OF THE MODULE OPERATION !"""

import header 
import openai
from src import gs
from src.utils.file import read_text_file
from src.logger.logger import logger
from pathlib import Path

# Loading system instructions
system_instruction_path = Path('../src/ai/openai/model/_experiments/system_instruction.txt')
system_instruction = read_text_file(system_instruction_path)

# Initialization Openai models
class OpenAIChat:
    def __init__(self, api_key: str, system_instruction: str = None):
        openai.api_key = gs.credentials
        self.system_instruction = system_instruction
        self.messages = []

        if self.system_instruction:
            self.messages.append({"role": "system", "content": self.system_instruction})

    def ask(self, prompt: str) -> str:
        """Sending the question to the Openai model and receiving an answer"""
        self.messages.append({"role": "user", "content": prompt})

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.messages,
                max_tokens=150,
                temperature=0.7
            )
            answer = response['choices'][0]['message']['content']
            self.messages.append({"role": "assistant", "content": answer})
            return answer
        except Exception as e:
            logger.error(f"Ошибка: {e}")
            return "Произошла ошибка при обработке запроса."

def chat():
    print("Добро пожаловать в чат с OpenAI!")
    print("Чтобы завершить чат, напишите 'exit'.\n")
    
    # API key input and model initialization
    api_key = input("Введите ваш OpenAI API ключ: ")
    ai = OpenAIChat(api_key=api_key, system_instruction=system_instruction)

    while True:
        # We get a question from the user
        user_input = input("> вопрос\n> ")
        
        if user_input.lower() == 'exit':
            print("Чат завершен.")
            break
        
        # Send a model request and get an answer
        response = ai.ask(prompt=user_input)
        
        # We display the answer
        print(f">> ответ\n>> {response}\n")

if __name__ == "__main__":
    chat()

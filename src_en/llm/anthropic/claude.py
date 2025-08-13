# # \file /src/ai/anthropic/claude.py
# -*- coding: utf-8 -*-

# ! .pyenv/bin/python3

"""клиент Claude
==============



Module: SRC.AI.Anthropic.Claude
[Д smells] (https://github.com/hypo69/hypothez/blob/master/docs/ru/src/ai/anthropic/claude.py.md)"""


# test


import anthropic
from typing import Optional


class ClaudeClient:
    def __init__(self, api_key: str) -> None:
        """The Claude client initializes with the API key provided.

        Args:
            API_KEY (STR): API key for access to Claude services.

        Example:
            >>> Claude_Client = claudeclient ('your_api_key')"""
        self.client = anthropic.Client(api_key)

    def generate_text(self, prompt: str, max_tokens_to_sample: int = 100) -> str:
        """Generates text based on the request.

        Args:
            PROMPT (STR): Request for generating text.
            max_tokens_to_sample (int, Optional): The maximum number of tokens for generation. By default 100.

        Returns:
            STR: generated text.

        Example:
            >>> Claude_Client.generate_text ('Write a Short Story.')
            'A short story ABOUT ...'"""
        response = self.client.completion(
            prompt=prompt,
            model='claude-v1',
            max_tokens_to_sample=max_tokens_to_sample,
            stop_sequences=['\n\nHuman:']
        )
        return response['completion']

    def analyze_sentiment(self, text: str) -> str:
        """Analyzes the tonality of the text provided.

        Args:
            Text (str): text for analysis.

        Returns:
            STR: The result of an analysis of tonality.

        Example:
            >>> Claude_Client.analyze_sentiment ('I am Very Happy!')
            'Positive'"""
        response = self.client.completion(
            prompt=f'Analyze the sentiment of the following text: {text}',
            model='claude-v1',
            max_tokens_to_sample=50,
            stop_sequences=['\n\nHuman:']
        )
        return response['completion']

    def translate_text(self, text: str, source_language: str, target_language: str) -> str:
        """Translates the provided text from the original language into the target language.

        Args:
            Text (str): Text for translation.
            Source_Language (str): the code of the source language.
            Target_language (str): Code of the target language.

        Returns:
            STR: translated text.

        Example:
            >>> Claude_Client.translate_text ('Hello', 'En', 'ES')
            'Hola'"""
        response = self.client.completion(
            prompt=f'Translate the following text from {source_language} to {target_language}: {text}',
            model='claude-v1',
            max_tokens_to_sample=100,
            stop_sequences=['\n\nHuman:']
        )
        return response['completion']


# An example of using a class
if __name__ == '__main__':
    api_key = 'your-api-key'
    claude_client = ClaudeClient(api_key)

    # An example of text generation
    prompt = 'Write a short story about a robot learning to love.'
    generated_text = claude_client.generate_text(prompt)
    print('Generated Text:', generated_text)

    # An example of an analysis of tonality
    text_to_analyze = 'I am very happy today!'
    sentiment_analysis = claude_client.analyze_sentiment(text_to_analyze)
    print('Sentiment Analysis:', sentiment_analysis)

    # An example of the translation of the text
    text_to_translate = 'Hello, how are you?'
    source_language = 'en'
    target_language = 'es'
    translated_text = claude_client.translate_text(text_to_translate, source_language, target_language)
    print('Translated Text:', translated_text)
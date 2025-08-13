# # \file /src/ai/helicone/helicone.py
# -*- coding: utf-8 -*-

# ! .pyenv/bin/python3

""".. module :: src.ai.helicone 
    : Platform: Windows, Unix
    Synopsis:"""


# https://docs.helicone.ai/guides/overview
import header 

from helicone import Helicone
from openai import OpenAI

class HeliconeAI:
    def __init__(self):
        self.helicone = Helicone()
        self.client = OpenAI()

    def generate_poem(self, prompt: str) -> str:
        """Generates a poem based on a given industrial plate.

        Arguments:
            PROMPT (STR): Prompt for generating a poem.

        Returns:
            STR: a generated poem."""
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        self.helicone.log_completion(response)
        return response.choices[0].message.content

    def analyze_sentiment(self, text: str) -> str:
        """Analyzes the tonality of the text.

        Arguments:
            Text (str): text for analysis.

        Returns:
            STR: The result of an analysis of tonality."""
        response = self.client.completions.create(
            model="text-davinci-003",
            prompt=f"Analyze the sentiment of the following text: {text}",
            max_tokens=50
        )
        self.helicone.log_completion(response)
        return response.choices[0].text.strip()

    def summarize_text(self, text: str) -> str:
        """Creates a brief presentation of the text.

        Arguments:
            Text (str): text for presentation.

        Returns:
            STR: A brief presentation of the text."""
        response = self.client.completions.create(
            model="text-davinci-003",
            prompt=f"Summarize the following text: {text}",
            max_tokens=100
        )
        self.helicone.log_completion(response)
        return response.choices[0].text.strip()

    def translate_text(self, text: str, target_language: str) -> str:
        """Translates the text into the specified language.

        Arguments:
            Text (str): Text for translation.
            Target_language (str): target language of translation.

        Returns:
            STR: translated text."""
        response = self.client.completions.create(
            model="text-davinci-003",
            prompt=f"Translate the following text to {target_language}: {text}",
            max_tokens=200
        )
        self.helicone.log_completion(response)
        return response.choices[0].text.strip()

def main():
    helicone_ai = HeliconeAI()

    poem = helicone_ai.generate_poem("Напиши мне стихотворение про кота.")
    print("Generated Poem:\n", poem)

    sentiment = helicone_ai.analyze_sentiment("Сегодня был отличный день!")
    print("Sentiment Analysis:\n", sentiment)

    summary = helicone_ai.summarize_text("Длинный текст для изложения...")
    print("Summary:\n", summary)

    translation = helicone_ai.translate_text("Hello, how are you?", "русский")
    print("Translation:\n", translation)

if __name__ == "__main__":
    main()
# # \file /src/ai/openai/translator.py
# -*- coding: utf-8 -*-

# ! .pyenv/bin/python3

""".. Module :: src.ai.openai
    : Platform: Windows, Unix
    : synopsis: a module for translating text using Openai API."""



import openai
from src import gs
from src.logger.logger import logger

openai.api_key = gs.credentials.openai

def translate(text, source_language, target_language):
    """Translation of the text using Openai API.

    This method sends the text for translation into the specified language using the Openai model and returns the translated text.

    Arguments:
        Text (str): Text for translation.
        Source_Language (str): language of the original text.
        Target_language (str): language for translation.

    Returns:
        STR: translated text.

    Example of use:
        >>> source_text = "Hello, how are you?"
        >>> source_language = "Russian"
        >>> Target_language = "English"
        >>> Translation = Translate_text (Source_text, Source_language, Target_language)
        >>> Print (F "Translate Text: {Translation}")"""
    
    # We form a request to Openai API
    prompt = (
        f"Translate the following text from {source_language} to {target_language}:\n\n"
        f"{text}\n\n"
        f"Translation:"
    )

    try:
        # We send a request to Openai API
        response = openai.Completion.create(
            engine="text-davinci-003",  # Indicate the desired model
            prompt=prompt,
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=0.3
        )

        # We extract a translation from the response of the API
        translation = response.choices[0].text.strip()
        return translation
    except Exception as ex:
        # We log in the error
        logger.error("Error during translation", ex)
        return

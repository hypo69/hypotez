# # \file /src/utils/string/ai_string_utils.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3


"""Utilities for bringing lines to the requirements of training and normalizing answers from language models.
========================================================================================================================

** appointment **

This module provides functions for processing and cleaning the lines, including:
1. Preparation of text data for training sets (shielding of quotation marks, removal of extra gaps,
    Removal/replacement of the symbols of a new line, tabulation, etc.).
2. Normalization of answers from language models (removal of framing code blocks).

.. Module :: src.utils.string.ai_string_utils # example of a new module path"""

import re
from typing import Union, List

# None
# Functions for training data for learning (from string_for_train.py)
# None

def string_for_train(data: Union[str, List[str]]) -> str:
    """Cleans and format data for training.

    Shirts double quotes (`" `) with a symbol of the reverse oblique feature (` \\ `).
    Replaces all the sequences of testicular characters (including gaps,
    Starring `\\ t`, translations of the line` \\ n`, `\\ r`,` \\ f`, `\\ v`) with one gap.
    Removes initial and final gaps.

    Args:
        Data (union [str, list [str]]): input data. Can be a line or
                                      a list of lines.

    Returns:
        STR: a cleaned and united line (if there was a list at the entrance),
             ready for use in training. Returns an empty line,
             If the type of input data is not a string or a list of lines.

    Examples:
        >>> string_for_train ('this is a line with "quotation marks" \\ ny \\ tprings.')
        'This is a line with \\ "quotes \\" and spaces.'
        >>> string_for_train (['first line.', 'second "line" \\ ts \\ nprobeli.'])
        'The first line. Second \\ "line \\" with spaces. '
        >>> string_for_train ('line \ ns \ nperens \ n')
        'Line with transfers'
        >>> string_for_train (None)
        ''
        >>> string_for_train (123)
        ''"""
    cleaned_text: str = ""

    if isinstance(data, str):
        # Shreet screenings
        cleaned_text = data.replace('"', '\\"')
        # Replacement of all sequences of prototype characters (\ s includes \ n, \ t, \ r, \ f, \ v and gap)
        # one gap and pruning of the edges
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        return cleaned_text
    elif isinstance(data, list):
        # Processing each list element
        processed_items = []
        for item in data:
            if isinstance(item, str):
                # Shreet screenings
                cleaned_item = item.replace('"', '\\"')
                # Do not delete \ n, \ t, etc. here separately
                # T.K. The final Re.Sub will process the entire line in its entirety
                processed_items.append(cleaned_item)
            else:
                # Skip non -hollow elements or process differently?
                # In the current implementation, they will be ignored during the unification,
                # But you can add logging or processing errors.
                pass # A clear indication that we do nothing
        # Combining the list elements in one line through a gap
        # The gap between the elements is important so that Re.Sub correctly shares them
        full_text = ' '.join(processed_items)
        # The final removal of repeated and undesirable testable characters (\ n, \ t, etc.),
        # replacing them with one gap and pruning the edges of the entire line
        cleaned_text = re.sub(r'\s+', ' ', full_text).strip()
        return cleaned_text
    else:
        # Return of an empty line for incorrect data type
        return ""

# None
# Functions for normalizing AI answers (from ai_response_normalizer.py)
# None

# List of prefixes and suffixes denoting code blocks in models answers
_NORMALIZER_PREFIXES: list[str] = [
    '```md\n',
    '```md ', # Add the option with a gap
    '```md',
    '```markdown\n',
    '```markdown ', # Add the option with a gap
    '```markdown',
    '```html\n',
    '```html ', # Add the option with a gap
    '```html',
    '```json\n', # Add other possible types
    '```json ',
    '```json',
    '```python\n',
    '```python ',
    '```python',
    '```text\n',
    '```text ',
    '```text',
    '```\n',
    '``` ',
    '```',
]
_NORMALIZER_SUFFIX: str = '```'


def normalize_answer(text: str) -> str:
    """It normalizes the text answer, deleting the framing blocks of the Markdown code.

    Checks whether the line `Text` begins one of the prefixes from the list
    `_Normalizer_prefixes` (for example, '` `` html \\ n', '`` `markdown', '` ``')
    And whether it ends with the suffix `_normalizer_suffix` ('` ``').
    If both conditions are met, removes the corresponding prefix and suffix.
    Otherwise, returns the original line unchanged.

    Args:
        Text (str): the original line of the text that potentially contains
                    Framing code blocks.

    Returns:
        str: normalized line without the initial and final blocks of code,
             Or the original line if the blocks are not found.

    Examples:
        >>> normalize_answer ("` `` html \\ n <p> example </p> \\ n```` ")
        '<p> Example </p> \\ n'
        >>> normalize_answer ("` `` Markdown \ n# headline \ ntext. \ n``` ")
        '# Headline \\ ntek. \\ n '
        >>> normalize_answer ("` `\ np. Text \ n``")
        'Just text \\ n'
        >>> Normalize_answer ("Ordinary text without blocks.")
        'Ordinary text without blocks.'
        >>> normalize_answer ("` `incomplete block")
        '`` `Incomplete block'
        >>> Normalize_answer ("Block at the end``")
        'Block at the end``' '
        >>> normalize_answer ("` `` md Text`` ") # example with a gap after MD
        'Text'"""
    if not isinstance(text, str):
        # You can add error processing or return the empty line/none
        return "" # Or Return Text, if you need to miss non-line

    normalized_text = text # Start with the original text

    for prefix in _NORMALIZER_PREFIXES:
        # Checking the presence of prefix and suffix
        if normalized_text.startswith(prefix) and normalized_text.endswith(_NORMALIZER_SUFFIX):
            # Remove the prefix
            normalized_text = normalized_text.removeprefix(prefix)
            # We delete the suffix
            normalized_text = normalized_text.removesuffix(_NORMALIZER_SUFFIX)
            # Since they found and deleted, you can leave the cycle
            break # Important: we stop the search after the first coincidence

    # You can add .Strip () to remove random spaces at the edges after removing the blocks
    # return normalized_text.strip()
    # However, this may be undesirable if indentation is important inside the block
    return normalized_text

# None
# An example of use (can be made or removed)
# None
if __name__ == '__main__':
    # Examples for string_for_train
    print("--- string_for_train ---")
    test_str = '   Это  строка   с "кавычками"   и    пробелами. '
    print(f"Original: '{test_str}'")
    print(f"Cleaned:  '{string_for_train(test_str)}'")

    # Added test C \ n and \ t
    test_str_ws = '   Строка\tс \n новой строкой\n\nи\t табами.  "кавычка" '
    print(f"Original WS: '{test_str_ws}'")
    print(f"Cleaned WS:  '{string_for_train(test_str_ws)}'")


    test_list = ['Первая строка.', '   Вторая "строка"   с пробелами.', ' Третья    ', '   ']
    print(f"Original list: {test_list}")
    print(f"Cleaned list: '{string_for_train(test_list)}'")

    # Added the list of the list with \ n and \ t
    test_list_ws = ['Первая\nстрока.', ' \tВторая "строка"\t\tс\nпробелами.']
    print(f"Original list WS: {test_list_ws}")
    print(f"Cleaned list WS: '{string_for_train(test_list_ws)}'")


    print(f"Invalid input (int): '{string_for_train(123)}'")
    print(f"Invalid input (None): '{string_for_train(None)}'")


    # Examples for Normalize_answer
    print("\n--- normalize_answer ---")
    tests_norm = [
        "```html\n<p>Пример</p>\n```",
        "```markdown\n# Heading \ ntek. \ N`` '",
        "```\nПросто текст\n```",
        "Обычный текст без блоков.",
        "```Неполный блок",
        "Блок в конце```",
        "```json\n{\"key\": \"value\"}\n```",
        "```md Текст```"
    ]
    for test_case in tests_norm:
        print(f"Original: '{test_case}'")
        print(f"Normalized: '{normalize_answer(test_case)}'")

    print(f"Invalid input (int): '{normalize_answer(123)}'") # type: ignore
# Provider: Phind

## Overview

This module defines a `Phind` provider, which allows accessing the Phind API for generating text responses from user prompts. It handles sending requests to the Phind API and processing the received responses.

## Details

The `Phind` provider works with the Phind API for text generation. It takes a user prompt, sends it to the API with specific configurations (e.g., desired skill level, language, and other options), and returns the response received from Phind. The provider ensures the response is formatted correctly and handles potential errors in the communication with the API.

## Classes

### `class Phind`

**Description**: The `Phind` class represents a provider that interacts with the Phind API for text generation.

**Attributes**:

-   `config (dict)`: Configuration parameters passed from the `hypotez` framework.

**Methods**:

-   `get_response()`: Sends a request to the Phind API with the provided configuration and returns the response received from the API.

## Functions

### `output(chunk)`

**Purpose**: Processes incoming data chunks from the Phind API and prints them to the console.

**Parameters**:

-   `chunk (bytes)`: A single chunk of data received from the Phind API.

**Returns**:

-   `None`

**How the Function Works**:

-   The function checks if the received `chunk` contains special metadata information. If it does, it does not process the chunk further and returns `None`.
-   The function decodes the `chunk` into a string and processes it to remove unnecessary formatting characters.
-   The processed string is printed to the console.
-   If a `JSONDecodeError` occurs during processing, it is caught and ignored.

**Examples**:

-   ```python
    >>> output(b'data:  \r\ndata: \r\ndata: \r\n\r\n')
    >>> output(b'PHIND_METADATA')
    ```

## Inner Functions

There are no inner functions within the `output` function.

## Examples

```python
import sys
import json
import datetime
import urllib.parse

from curl_cffi import requests

config = json.loads(sys.argv[1])
prompt = config['messages'][-1]['content']

skill = 'expert' if config['model'] == 'gpt-4' else 'intermediate'

json_data = json.dumps({
    'question': prompt,
    'options': {
        'skill': skill,
        'date': datetime.datetime.now().strftime('%d/%m/%Y'),
        'language': 'en',
        'detailed': True,
        'creative': True,
        'customLinks': []}}, separators=(',', ':'))

headers = {
    'Content-Type': 'application/json',
    'Pragma': 'no-cache',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'same-origin',
    'Accept-Language': 'en-GB,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Sec-Fetch-Mode': 'cors',
    'Content-Length': str(len(json_data)),
    'Origin': 'https://www.phind.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15',
    'Referer': f'https://www.phind.com/search?q={urllib.parse.quote(prompt)}&source=searchbox',
    'Connection': 'keep-alive',
    'Host': 'www.phind.com',
    'Sec-Fetch-Dest': 'empty'
}


def output(chunk):
    """
    Обрабатывает входящие фрагменты данных от API Phind и выводит их на консоль.

    Args:
        chunk (bytes): Отдельный фрагмент данных, полученный от API Phind.

    Returns:
        None

    How the Function Works:

    - Функция проверяет, содержит ли полученный `chunk` специальную информацию о метаданных. Если да, то она не обрабатывает этот фрагмент и возвращает `None`.
    - Функция декодирует `chunk` в строку и обрабатывает ее для удаления ненужных символов форматирования.
    - Обработанная строка выводится на консоль.
    - Если при обработке возникает `JSONDecodeError`, то он перехватывается и игнорируется.

    Examples:

    >>> output(b'data:  \r\ndata: \r\ndata: \r\n\r\n')
    >>> output(b'PHIND_METADATA')
    """
    try:
        if b'PHIND_METADATA' in chunk:
            return
        
        if chunk == b'data:  \\r\\ndata: \\r\\ndata: \\r\\n\\r\\n':
            chunk = b'data:  \\n\\r\\n\\r\\n'

        chunk = chunk.decode()

        chunk = chunk.replace('data: \\r\\n\\r\\ndata: ', 'data: \\n')
        chunk = chunk.replace('\\r\\ndata: \\r\\ndata: \\r\\n\\r\\n', '\\n\\r\\n\\r\\n')
        chunk = chunk.replace('data: ', '').replace('\\r\\n\\r\\n', '')

        print(chunk, flush=True, end = '')
        
    except json.decoder.JSONDecodeError:
        pass

while True:
    try:
        response = requests.post('https://www.phind.com/api/infer/answer',
                         headers=headers, data=json_data, content_callback=output, timeout=999999, impersonate='safari15_5')
        
        exit(0)
    
    except Exception as e:
        print('an error occured, retrying... |', e, flush=True)
        continue
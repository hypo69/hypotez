**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use This Code Block
=========================================================================================

Description
-------------------------
This code block interacts with the Phind API to retrieve answers to questions based on provided context. It prepares a JSON request with the user's question, model type (gpt-4 or other), and additional parameters like skill level, date, language preferences, and creative options. It then sends the request to Phind's API and processes the streamed response.

Execution Steps
-------------------------
1. **Prepare the Request**:
    - Load configuration details from command line arguments.
    - Extract the user's prompt from the configuration.
    - Determine the skill level based on the model type.
    - Construct a JSON payload containing the user's question, skill level, date, language, and other preferences.
2. **Send the Request**:
    - Define headers for the HTTP request, including content type, user agent, and other necessary information.
    - Send a POST request to the Phind API endpoint `/api/infer/answer` with the prepared JSON payload and headers.
    - Configure the request to stream the response using `content_callback`.
3. **Process the Response**:
    - The `output` function handles the streamed response, filtering out metadata and processing the actual response data.
    - Chunk by chunk, the function decodes the received data, removes special characters, and prints the output to the console.
    - If a JSON decoding error occurs, the function skips the chunk.
4. **Handle Errors**:
    - The code includes a loop that retries the API request in case of errors, such as network issues.
    - Error messages are printed to the console along with the specific exception encountered.

Usage Example
-------------------------

```python
    # Example command line call
    # python phind.py '{"messages":[{"role":"user","content":"What is the meaning of life?"}],"model":"gpt-4"}'
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

```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".
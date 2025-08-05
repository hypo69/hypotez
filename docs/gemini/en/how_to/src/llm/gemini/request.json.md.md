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
This code block defines a JSON schema for a Gemini API request. It specifies the structure and data types of the various fields required for making requests to the Gemini API. 

Execution Steps
-------------------------
1. The code defines a JSON object representing the structure of a Gemini API request.
2. It includes fields such as:
    - `cachedContent`: Stores the cached content of the request, if available.
    - `contents`: An array of objects representing the content of the request.
    - `systemInstruction`: An object containing instructions for the system.
    - `tools`: An array of objects representing tools available for the request.
    - `safetySettings`: An array of objects defining safety settings for the request.
    - `generationConfig`: An object containing configuration parameters for generation.
    - `labels`: A dictionary of string key-value pairs for labeling the request.
3. Each field is defined with a specific data type, such as "string", "integer", or "boolean".
4. Some fields, like "data", "fileUri", and "text", are defined using a union type. This means that the field can accept data of different types depending on the context.
5. The schema also specifies constraints on the data types and allows for specifying additional information, such as the possible values for enums.

Usage Example
-------------------------
```python
from typing import Dict

gemini_request: Dict = {
    "cachedContent": "string",
    "contents": [
        {
            "role": "string",
            "parts": [
                {
                    "text": "string",  # Content type: text
                }
            ]
        }
    ],
    "systemInstruction": {
        "role": "string",
        "parts": [
            {
                "text": "string"  # System instruction text
            }
        ]
    },
    "tools": [
        {
            "functionDeclarations": [
                {
                    "name": "string",
                    "description": "string",
                    "parameters": {
                        "object": {}  # Parameter schema for the function
                    }
                }
            ]
        }
    ],
    "safetySettings": [
        {
            "category": "enum",  # Enum value
            "threshold": "enum"  # Enum value
        }
    ],
    "generationConfig": {
        "temperature": 0.7,
        "topP": 0.5,
        "topK": 40,
        "candidateCount": 10,
        "maxOutputTokens": 500,
        "presencePenalty": 0.0,
        "frequencyPenalty": 0.0,
        "stopSequences": ["\n"],
        "responseMimeType": "text/plain",
        "responseSchema": "schema",
        "seed": 12345,
        "responseLogprobs": False,
        "logprobs": 5,
        "audioTimestamp": False
    },
    "labels": {
        "string": "string"
    }
}

# Send the request to the Gemini API
# ...
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".
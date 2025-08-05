# Gemini Request JSON Schema 

## Overview

This file defines the JSON schema for Gemini requests. This schema serves as a blueprint for constructing requests sent to the Gemini language model. It outlines the structure and types of data that Gemini expects.

## Details

The Gemini request schema includes the following fields:

* `cachedContent`:  This field contains a string that is used to store the cached content of a request.
* `contents`: This field contains a list of objects that represent the content of the request. Each object within the list has the following fields:
    * `role`: This field defines the role of the content. The value of this field is a string that can be any of the following: `system`, `user`, or `assistant`.
    * `parts`: This field contains a list of objects that represent the parts of the content. Each object within the list has the following fields:
        * `text`: This field defines the text of the content. The value of this field is a string.
        * `inlineData`: This field is a union field that contains data that is embedded within the text. The value of this field is an object with the following fields:
            * `mimeType`: This field defines the MIME type of the data. The value of this field is a string.
            * `data`: This field defines the data itself. The value of this field is a string.
        * `fileData`: This field contains data that is a file. The value of this field is an object with the following fields:
            * `mimeType`: This field defines the MIME type of the file. The value of this field is a string.
            * `fileUri`: This field defines the URI of the file. The value of this field is a string.
        * `videoMetadata`: This field contains metadata for a video. The value of this field is an object with the following fields:
            * `startOffset`: This field defines the start offset of the video. The value of this field is an object with the following fields:
                * `seconds`: This field defines the number of seconds in the start offset. The value of this field is an integer.
                * `nanos`: This field defines the number of nanoseconds in the start offset. The value of this field is an integer.
            * `endOffset`: This field defines the end offset of the video. The value of this field is an object with the following fields:
                * `seconds`: This field defines the number of seconds in the end offset. The value of this field is an integer.
                * `nanos`: This field defines the number of nanoseconds in the end offset. The value of this field is an integer.
* `systemInstruction`: This field contains a list of objects that represent the system instruction for the request. Each object within the list has the following fields:
    * `role`: This field defines the role of the system instruction. The value of this field is a string that is `system`.
    * `parts`: This field contains a list of objects that represent the parts of the system instruction. Each object within the list has the following fields:
        * `text`: This field defines the text of the system instruction. The value of this field is a string.
* `tools`: This field contains a list of objects that represent the tools that are available to the Gemini model. Each object within the list has the following fields:
    * `functionDeclarations`: This field contains a list of objects that represent the function declarations for the tools. Each object within the list has the following fields:
        * `name`: This field defines the name of the function. The value of this field is a string.
        * `description`: This field defines the description of the function. The value of this field is a string.
        * `parameters`: This field defines the parameters of the function. The value of this field is an object that defines the parameters. 
* `safetySettings`: This field contains a list of objects that represent the safety settings for the Gemini model. Each object within the list has the following fields:
    * `category`: This field defines the category of the safety setting. The value of this field is an enum.
    * `threshold`: This field defines the threshold for the safety setting. The value of this field is an enum.
* `generationConfig`: This field contains the configuration for the Gemini model. This field is an object with the following fields:
    * `temperature`: This field defines the temperature of the model. The value of this field is a number.
    * `topP`: This field defines the top-p sampling method. The value of this field is a number.
    * `topK`: This field defines the top-k sampling method. The value of this field is a number.
    * `candidateCount`: This field defines the number of candidates to be considered for sampling. The value of this field is an integer.
    * `maxOutputTokens`: This field defines the maximum number of tokens that the model can generate. The value of this field is an integer.
    * `presencePenalty`: This field defines the penalty for the presence of a token in the output. The value of this field is a float.
    * `frequencyPenalty`: This field defines the penalty for the frequency of a token in the output. The value of this field is a float.
    * `stopSequences`: This field defines the stop sequences for the model. The value of this field is a list of strings.
    * `responseMimeType`: This field defines the MIME type of the response. The value of this field is a string.
    * `responseSchema`: This field defines the schema of the response. The value of this field is a schema.
    * `seed`: This field defines the seed for the random number generator. The value of this field is an integer.
    * `responseLogprobs`: This field defines whether to include log probabilities in the response. The value of this field is a boolean.
    * `logprobs`: This field defines the number of log probabilities to include in the response. The value of this field is an integer.
    * `audioTimestamp`: This field defines whether to include audio timestamps in the response. The value of this field is a boolean.
* `labels`: This field contains a dictionary of key-value pairs that represent the labels for the request. The value of this field is a dictionary of strings.

## Examples

Here are some examples of Gemini request schemas:

```json
{
  "cachedContent": "string",
  "contents": [
    {
      "role": "string",
      "parts": [
        {
          "text": "string"
        }
      ]
    }
  ],
  "systemInstruction": {
    "role": "string",
    "parts": [
      {
        "text": "string"
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
            "object"
          }
        }
      ]
    }
  ],
  "safetySettings": [
    {
      "category": "enum",
      "(HarmCategory)",
      "threshold": "enum",
      "(HarmBlockThreshold)"
    }
  ],
  "generationConfig": {
    "temperature": "number",
    "topP": "number",
    "topK": "number",
    "candidateCount": "integer",
    "maxOutputTokens": "integer",
    "presencePenalty": "float",
    "frequencyPenalty": "float",
    "stopSequences": [
      "string"
    ],
    "responseMimeType": "string",
    "responseSchema": "schema",
    "seed": "integer",
    "responseLogprobs": "boolean",
    "logprobs": "integer",
    "audioTimestamp": "boolean"
  },
  "labels": {
    "string": "string"
  }
}
```

```json
{
  "cachedContent": "string",
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": "What is the capital of France?"
        }
      ]
    }
  ],
  "systemInstruction": {
    "role": "system",
    "parts": [
      {
        "text": "You are a helpful assistant."
      }
    ]
  },
  "tools": [],
  "safetySettings": [],
  "generationConfig": {
    "temperature": 0.7,
    "topP": 1.0,
    "topK": 40,
    "candidateCount": 10,
    "maxOutputTokens": 256,
    "presencePenalty": 0.0,
    "frequencyPenalty": 0.0,
    "stopSequences": [
      "\n"
    ],
    "responseMimeType": "text/plain",
    "responseSchema": null,
    "seed": null,
    "responseLogprobs": false,
    "logprobs": null,
    "audioTimestamp": false
  },
  "labels": {}
}
```

```json
{
  "cachedContent": "string",
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": "Write a Python function that takes a list of integers and returns the sum of all even numbers in the list."
        }
      ]
    }
  ],
  "systemInstruction": {
    "role": "system",
    "parts": [
      {
        "text": "You are a helpful assistant."
      }
    ]
  },
  "tools": [],
  "safetySettings": [],
  "generationConfig": {
    "temperature": 0.7,
    "topP": 1.0,
    "topK": 40,
    "candidateCount": 10,
    "maxOutputTokens": 256,
    "presencePenalty": 0.0,
    "frequencyPenalty": 0.0,
    "stopSequences": [
      "\n"
    ],
    "responseMimeType": "text/plain",
    "responseSchema": null,
    "seed": null,
    "responseLogprobs": false,
    "logprobs": null,
    "audioTimestamp": false
  },
  "labels": {}
}
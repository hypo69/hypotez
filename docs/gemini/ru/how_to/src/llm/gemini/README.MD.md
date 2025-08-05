## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода является частью модуля `src.ai.gemini`, который предназначен для взаимодействия с моделями Generative AI от Google. Он представляет собой строку с использованием директивы `.. module::` в формате reStructuredText.

Шаги выполнения
-------------------------
1. **Создание директивы:** `.. module::` - эта директива указывает Sphinx, что следующий текст будет представлять собой описание модуля.
2. **Название модуля:**  `src.ai.gemini` -  указанное здесь название модуля - это путь к модулю в проекте.

Пример использования
-------------------------

```python
                ```rst
.. module:: src.ai.gemini
```
[Русский](https://github.com/hypo69/hypo/tree/master/src/ai/gemini/readme.ru.md)

# Google Generative AI Integration Module

## Overview

The `GoogleGenerativeAi` class is designed to facilitate interaction with Google's Generative AI models. This class provides methods for sending queries, handling responses, managing dialogues, and integrating with various AI functionalities. It includes robust error handling, logging, and configuration options to ensure seamless operation.

## Key Functions

### `__init__(self, api_key: str, model_name: Optional[str] = None, generation_config: Optional[Dict] = None, system_instruction: Optional[str] = None, **kwargs)`

**Purpose**: Initializes the `GoogleGenerativeAi` class with the necessary configurations.

**Details**:\n- Sets up the API key, model name, generation configuration, and system instruction.\n- Defines paths for logging dialogues and storing history.\n- Initializes the Google Generative AI model.

### `config()`

**Purpose**: Retrieves the configuration from a settings file.

**Details**:\n- Reads and parses the configuration file located at `gs.path.src / \'ai\' / \'gemini\' / \'gemini.json\'`.

### `_start_chat(self)`

**Purpose**: Starts a chat session with the AI model.

**Details**:\n- Initializes a chat session with an empty history.

### `_save_dialogue(self, dialogue: list)`

**Purpose**: Saves a dialogue to both text and JSON files.

**Details**:\n- Appends each message in the dialogue to a text file.\n- Appends each message in JSON format to a JSON file.

### `ask(self, q: str, attempts: int = 15) -> Optional[str]`

**Purpose**: Sends a text query to the AI model and retrieves the response.

**Details**:\n- Handles multiple attempts in case of network errors or service unavailability.\n- Logs errors and retries with exponential backoff.\n- Saves the dialogue to history files.

### `chat(self, q: str) -> str`

**Purpose**: Sends a chat message to the AI model and retrieves the response.

**Details**:\n- Uses the chat session initialized by `_start_chat`.\n- Logs errors and returns the response text.

### `describe_image(self, image_path: Path) -> Optional[str]`

**Purpose**: Generates a textual description of an image.

**Details**:\n- Encodes the image in base64 and sends it to the AI model.\n- Returns the generated description or logs an error if the operation fails.

### `upload_file(self, file: str | Path | IOBase, file_name: Optional[str] = None) -> bool`

**Purpose**: Uploads a file to the AI model.

**Details**:\n- Handles file upload and logs the success or failure.\n- Provides retry logic in case of errors.

## Error Handling

The class includes comprehensive error handling for various scenarios:\n- **Network Errors**: Retries with exponential backoff.\n- **Service Unavailability**: Logs errors and retries.\n- **Quota Limits**: Logs and waits before retrying.\n- **Authentication Errors**: Logs and stops further attempts.\n- **Invalid Input**: Logs and retries with a timeout.\n- **API Errors**: Logs and stops further attempts.

## Logging and History

All interactions with the AI models are logged, and dialogues are saved in both text and JSON formats for future analysis. This ensures that all operations are traceable and can be reviewed for debugging or auditing purposes.

## Dependencies

- `google.generativeai`
- `requests`
- `grpc`
- `google.api_core.exceptions`
- `google.auth.exceptions`
- `src.logger`
- `src.utils.printer`
- `src.utils.file`
- `src.utils.date_time`
- `src.utils.convertors.unicode`
- `src.utils.jjson`

## Usage Example

```python
ai = GoogleGenerativeAi(api_key="your_api_key", system_instruction="Instruction")
response = ai.ask("Как дела?")
print(response)
```

This example initializes the `GoogleGenerativeAi` class and sends a query to the AI model, printing the response.

---

For more detailed information, refer to the source code and comments within the `GoogleGenerativeAi` class.
                ```
```
- Эта строка добавляется для документации модуля `src.ai.gemini` в проекте.
- Она является частью директивы `.. module::` и указывает на то, что следующий текст относится к этому модулю.
- В документации используется язык reStructuredText.
-  `[Русский](https://github.com/hypo69/hypo/tree/master/src/ai/gemini/readme.ru.md)` -  эта ссылка добавляется для перехода на русскую версию документации.
- Остальной текст - это описание модуля `src.ai.gemini`, которое будет использоваться в документации.
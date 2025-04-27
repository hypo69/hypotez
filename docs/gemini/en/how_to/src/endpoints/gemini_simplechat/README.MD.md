## Instructions for Using the `GoogleGenerativeAi` Class

This project provides a `GoogleGenerativeAi` class to interact with Google Generative AI (Gemini) models. It allows you to send text prompts, engage in conversations, describe images, and upload files using the Google Gemini API.

### Features:

- Support for various Gemini models.
- Saving conversation history in JSON and text files.
- Working with text, images, and files.
- Error handling with retry mechanisms.
- Customizable generation parameters and system instructions.
- Example usage in `main()` with image and file loading and reading, as well as interactive chat.
- Web interface for interacting with the chatbot.
- Automatic application startup at system launch and the ability to call from the command line (Windows only).

### Requirements:

- Python 3.7 or higher
- Installed libraries (see `requirements.txt`).
- Valid Google Gemini API key (replace in the `config.json` file with your own)
    [Get key here](https://aistudio.google.com/app)

### Installation:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/hypo69/gemini-simplechat-ru.git
   cd gemini-simplechat-ru
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Create or configure the configuration file:**

   In `/config.json` you can place settings that will be required for your work.
   Example:

   ```json
   {
     "path": {
       "external_storage": "chat_data",
       "google_drive": "chat_data",
       "log": "/log",
       "tmp": "/tmp",
       "src": "/src",
       "root": ".",
       "endpoints": "."
     },
     "credentials": {
       "gemini": {
         "model_name": "gemini-1.5-flash-8b-exp-0924",
         "avaible_maodels": [
           "gemini-2.0-flash-exp",
           "gemini-1.5-flash-8b-exp-0924",
           "gemini-1.5-flash",
           "gemini-1.5-flash-8b"
         ],
         "api_key": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" // <- YOUR GEMINI API KEY 
       }
     },
     "fast_api": {
       "host": "127.0.0.1",
       "port": "3000",
       "index_path": "html/index.html"
     },
     "now": ""
   }
   ```

   **Note:** The API key needs to be replaced with your own.

4. **Using the `install.ps1` script to install (Windows only)**

   To automatically install the project and configure application auto-launch, you can use the `install.ps1` script, which will copy all project files to the `AI Assistant` folder in the `%LOCALAPPDATA%` directory. The script will also set up `main.py` to run at system startup through the `run.ps1` script and add the ability to call the application from the command line using the `ai` command.

   **Instructions:**

   1. Copy the `install.ps1` script to the root directory of the project.
   2. Open PowerShell as administrator.
   3. Navigate to the project directory: `cd <path_to_project>`.
   4. Run the script by executing the command: `.\\install.ps1`

       The script will create the `AI Assistant` folder at the path `%LOCALAPPDATA%\\AI Assistant`, copy all project files to it, configure application auto-launch at system startup through the `run.ps1` script, and add the `ai` command for calling the application from the command line.

### Starting the Web Server

To start the web server, use the command:

```bash
python main.py
```

After launching, the web interface will be available at http://127.0.0.1:8000.

### Usage

### Initialization:

```python
from src.ai.gemini import GoogleGenerativeAi
import gs

system_instruction = "You are a helpful assistant. Answer all questions concisely"
ai = GoogleGenerativeAi(api_key=gs.credentials.gemini.api_key, system_instruction=system_instruction)
```

### Methods of the `GoogleGenerativeAi` Class:

- **`__init__(api_key: str, model_name: str = "gemini-2.0-flash-exp", generation_config: Dict = None, system_instruction: Optional[str] = None)`:**
    - Initializes the `GoogleGenerativeAi` object with the API key, model name, and generation settings.
    - The `system_instruction` parameter allows you to set system instructions for the model.

- **`ask(q: str, attempts: int = 15) -> Optional[str]`:**
    - Sends the text prompt `q` to the model and returns the response.
    - `attempts` - the number of attempts if the request fails.

- **`chat(q: str) -> Optional[str]`:**
    - Sends the prompt `q` to the chat, maintaining the conversation history.
    - Returns the model's response.
    - Chat history is saved to a JSON file.

- **`describe_image(image: Path | bytes, mime_type: Optional[str] = 'image/jpeg', prompt: Optional[str] = '') -> Optional[str]`:**
    - Describes the image sent as a file path or bytes.
    - `image`: the path to the image file or the image bytes.
    - `mime_type`: the image mime type.
    - `prompt`: text prompt for describing the image.
    - Returns a text description of the image.

- **`upload_file(file: str | Path | IOBase, file_name: Optional[str] = None) -> bool`:**
    - Uploads the file to the Gemini API.
    - `file`: the path to the file, the file name, or the file object.
    - `file_name`: the file name for the Gemini API.

### Usage Example:

```python
import asyncio
from pathlib import Path
from src.ai.gemini import GoogleGenerativeAi
from src import gs
from src.utils.jjson import j_loads

# Replace with your API key
system_instruction = "You are a helpful assistant. Answer all questions concisely"
ai = GoogleGenerativeAi(api_key=gs.credentials.gemini.api_key, system_instruction=system_instruction)

async def main():
    # Example call to describe_image with a prompt
    image_path = Path(r"test.jpg")  # Replace with the path to your image

    if not image_path.is_file():
        print(
            f"File {image_path} does not exist. Place a file named test.jpg in the root folder with the program"
        )
    else:
        prompt = """Analyze this image. Give the answer in JSON format,
        where the key will be the object name, and the value will be its description.
         If there are people, describe their actions."""

        description = await ai.describe_image(image_path, prompt=prompt)
        if description:
            print("Image Description (with JSON format):")
            print(description)
            try:
                parsed_description = j_loads(description)

            except Exception as ex:
                print("Failed to parse JSON. Received text:")
                print(description)

        else:
            print("Failed to get image description.")

        # Example without JSON output
        prompt = "Analyze this image. List all objects that you can recognize."
        description = await ai.describe_image(image_path, prompt=prompt)
        if description:
            print("Image Description (without JSON format):")
            print(description)

    file_path = Path('test.txt')
    with open(file_path, "w") as f:
        f.write("Hello, Gemini!")

    file_upload = await ai.upload_file(file_path, 'test_file.txt')
    print(file_upload)

    # Chat example
    while True:
        user_message = input("You: ")
        if user_message.lower() == 'exit':
            break
        ai_message = await ai.chat(user_message)
        if ai_message:
            print(f"Gemini: {ai_message}")
        else:
            print("Gemini: Error getting response")


if __name__ == "__main__":
    asyncio.run(main())
```

### Additional Notes:

- **Logging:** All dialogues and errors are recorded in the corresponding files in the `external_storage/gemini_data/log` directory.
    - Logs are saved to the following files: `info.log`, `debug.log`, `errors.log`, `log.json`.
    - **Recommendation:** Regularly clear the `logs` directory to avoid accumulating large files.

- **Chat History:** Chat history is stored in JSON and text files in the `external_storage/gemini_data/history/` directory.
    - Each new dialogue creates new files.
    - **Recommendation:** Regularly clear the `history` directory to avoid accumulating large files.

- **Error Handling:** The program handles network errors, authentication errors, and API errors with a retry mechanism.
- **Auto-Launch:** The `run.ps1` script ensures the application is launched in the background at system startup (Windows only).
- **Calling from the Command Line:** After installation, the application can be called from any directory using the `ai` command. For the `ai` command to work correctly, restart the terminal after installation.

### Remarks:

- Be sure to replace `gs.credentials.gemini.api_key` with your valid Google Gemini API key in the `config.json` file.
- Ensure that you have `google-generativeai`, `requests`, `grpcio`, `google-api-core`, and `google-auth` installed.
- Make sure you have a `test.jpg` file in the root folder with the program or change the path to the image in the `main` example.
- The `install.ps1` script requires running as administrator.

### License:

This project is distributed under [MIT].

### Author:

[hypo69]
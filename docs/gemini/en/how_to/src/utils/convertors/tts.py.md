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
The code snippet provides two functions for speech recognition and text-to-speech conversion:

- `speech_recognizer`: Recognizes speech from an audio file (either downloaded from a URL or provided locally).
- `text2speech`: Converts text into speech and saves it as an audio file.

Execution Steps
-------------------------
**`speech_recognizer` Function:**

1. **Download Audio (if URL provided):** If an audio URL is given, the function downloads the audio file and saves it to a temporary location.
2. **Convert Audio Format:** Converts the audio file (either downloaded or provided) from OGG to WAV format for compatibility with speech recognition libraries.
3. **Initialize Speech Recognizer:** Creates an instance of `sr.Recognizer` from the `speech_recognition` library.
4. **Recognize Speech:** Uses Google Speech Recognition to recognize the speech from the WAV audio file and returns the recognized text.
5. **Handle Errors:** Catches potential errors during the recognition process and returns informative error messages.

**`text2speech` Function:**

1. **Generate Speech:** Uses `gTTS` library to synthesize speech from the provided text.
2. **Save Audio:** Saves the generated speech as an MP3 file in a temporary location.
3. **Convert to WAV:** Converts the MP3 audio to WAV format using `pydub` library.
4. **Log Success:** Logs the path to the generated WAV file using the project logger.
5. **Handle Errors:** Catches potential errors during speech synthesis and conversion, returning an error message.


Usage Example
-------------------------

```python
from src.utils.convertors.tts import speech_recognizer, text2speech

# Speech Recognition Example
recognized_text = speech_recognizer(audio_url='https://example.com/audio.ogg')
print(recognized_text)  # Output: "Привет"

# Text-to-Speech Example
audio_path = asyncio.run(text2speech('Hello, world!', lang='en'))
print(audio_path)  # Output: "/tmp/response.mp3"
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".
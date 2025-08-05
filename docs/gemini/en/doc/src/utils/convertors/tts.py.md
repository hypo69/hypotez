# Module: Speech Recognition and Text-to-Speech Conversion (src.utils.convertors.tts)

## Overview

This module provides functions for speech recognition and text-to-speech conversion. It utilizes external libraries such as `speech_recognition`, `pydub`, and `gTTS` to perform these tasks. 

## Details

The module offers the following functionalities:

* **`speech_recognizer`:** Downloads audio files from URLs or local paths and performs speech recognition using Google Speech Recognition API.
* **`text2speech`:** Converts text to speech in various languages using gTTS and saves the generated audio as a WAV file.

This module plays a vital role in the `hypotez` project by enabling voice-based interactions and speech-related processing tasks.

## Functions

### `speech_recognizer`

**Purpose**:  Downloads an audio file and recognizes speech in it using Google Speech Recognition.

**Parameters**:

- `audio_url` (str, optional): URL of the audio file to be downloaded. Defaults to `None`.
- `audio_file_path` (Path, optional): Local path to an audio file. Defaults to `None`.
- `language` (str): Language code for recognition (e.g., 'ru-RU'). Defaults to 'ru-RU'.

**Returns**:

- `str`: Recognized text from the audio or an error message.

**Raises Exceptions**:

- `Exception`: If an error occurs during audio download, conversion, or speech recognition.

**How the Function Works**:

1.  **Download Audio:** If an `audio_url` is provided, the function downloads the audio file and saves it to a temporary location.
2.  **Audio Conversion:** The downloaded or provided audio file is converted from OGG to WAV format for compatibility with the speech recognition library.
3.  **Speech Recognition:** The WAV audio file is processed by the `speech_recognition` library, and the recognized text is returned.

**Examples**:

```python
# Example 1: Download audio from a URL and recognize speech.
recognized_text = speech_recognizer(audio_url='https://example.com/audio.ogg')
print(recognized_text)  # Output: "Привет" 

# Example 2: Recognize speech from a local file.
audio_file_path = Path('./audio.ogg')
recognized_text = speech_recognizer(audio_file_path=audio_file_path)
print(recognized_text)  # Output: "Hello world!" 
```

### `text2speech`

**Purpose**: Converts text to speech and saves it as an audio file.

**Parameters**:

- `text` (str): The text to be converted into speech.
- `lang` (str, optional): Language code for the speech (e.g., 'ru'). Defaults to 'ru'.

**Returns**:

- `str`: Path to the generated audio file.

**Raises Exceptions**:

- `Exception`: If an error occurs during text-to-speech conversion.

**How the Function Works**:

1.  **Text-to-Speech Conversion:** The `text` is converted to speech using the `gTTS` library, and the audio is saved to a temporary file in MP3 format.
2.  **Audio Conversion:** The generated MP3 audio is then converted to WAV format using `pydub`.

**Examples**:

```python
# Example 1: Convert text to speech in Russian.
audio_path = await text2speech('Привет', lang='ru')
print(audio_path)  # Output: "/tmp/response.mp3" 

# Example 2: Convert text to speech in English.
audio_path = await text2speech('Hello world!', lang='en')
print(audio_path)  # Output: "/tmp/response.mp3" 
```

```python
                ```
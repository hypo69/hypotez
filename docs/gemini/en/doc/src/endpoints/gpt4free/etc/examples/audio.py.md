# Audio Generation and Transcription Using GPT-4Free

## Overview

This module provides a Python script demonstrating the capabilities of the `g4f` library for generating audio and transcribing audio files using the GPT-4Free API. The code leverages the `PollinationsAI` and `Microsoft_Phi_4` providers for audio generation and transcription, respectively. 

## Details

The script utilizes the `AsyncClient` from the `g4f` library to interact with the GPT-4Free API asynchronously. It performs two key tasks:

1. **Audio Generation**: The script uses the `openai-audio` model from the `PollinationsAI` provider to synthesize audio from a text prompt. The `voice` and `format` parameters can be customized to generate audio in different voices and formats.
2. **Audio Transcription**:  The script leverages the `Microsoft_Phi_4` provider to transcribe an audio file (in WAV format). It transmits the audio file to the API and retrieves the transcribed text output. 

## Functions

### `main()`

**Purpose**: This function orchestrates the audio generation and transcription tasks.

**Parameters**: None

**Returns**: None

**Raises Exceptions**: 
- `Exception`: If an error occurs during audio generation or transcription.

**How the Function Works**:
- It establishes an asynchronous client connection with the `PollinationsAI` provider.
- It sends a text prompt to the `openai-audio` model, specifying the desired voice and audio format.
- The generated audio is saved as an MP3 file.
- The function then opens a WAV audio file and sends it to the `Microsoft_Phi_4` provider for transcription.
- The transcribed text is printed to the console.

**Examples**:
```python
# Generate audio with a custom prompt and voice
response = await client.chat.completions.create(
    model="openai-audio",
    messages=[{"role": "user", "content": "This is a test audio for hypotez."}],
    audio={ "voice": "alloy", "format": "mp3" },
)
response.choices[0].message.save("test.mp3") 

# Transcribe an audio file
with open("audio.wav", "rb") as audio_file:
    response = await client.chat.completions.create(
        messages="Transcribe this audio",
        provider=g4f.Provider.Microsoft_Phi_4,
        media=[[audio_file, "audio.wav"]],
        modalities=["text"],
    )
    print(response.choices[0].message.content) 
```

## Parameter Details

- `model`: (str) Specifies the AI model to be used. In this case, `openai-audio` for audio generation and `microsoft-phi-4` for transcription.
- `messages`: (list) A list of messages representing the conversation with the AI model. Each message is a dictionary with keys: `role` (str), `content` (str), and optional `audio` (dict).
- `audio`: (dict)  A dictionary defining the audio parameters for generation.  Keys include: `voice` (str) for the desired voice, and `format` (str) for the audio file format (e.g., "mp3", "wav").
- `provider`: (str) Specifies the provider for accessing the AI model. The code utilizes `g4f.Provider.PollinationsAI` and `g4f.Provider.Microsoft_Phi_4`.
- `media`: (list) A list of media files to be processed. In this case, a single WAV audio file. Each item is a list containing the file object and file name.
- `modalities`: (list) Specifies the modalities (types) of content expected in the response. In this case, "text" for text-based transcription. 

## Examples

```python
# Example 1: Generate audio with a custom prompt and voice
# Example 2: Transcribe an audio file
# ...
```

## Conclusion

This script illustrates a practical use case of the `g4f` library for interacting with GPT-4Free providers. The code demonstrates how to generate audio with different voices and formats and transcribe existing audio files, showcasing the library's versatility for audio processing tasks.